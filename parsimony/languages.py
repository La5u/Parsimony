"""Optional coding-unit backends for JavaScript, TypeScript and Go.

JavaScript and TypeScript use the official TypeScript parser (pinned npm package,
run by Node through ``typescript_units.cjs``); Go uses Tree-sitter. These
syntax-derived counts are not semantic complexity and are not comparable across
languages or backends. Dependencies are deliberately loaded lazily.
"""
import atexit
import json
import os
import shutil
import subprocess
from bisect import bisect_right
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

SUPPORTED = ("python", "javascript", "typescript", "go")
UNIT_VERSION = "tree-sitter-units-v1"
TYPESCRIPT_UNIT_VERSION = "typescript-compiler-units-v1"
_PINS = {
    "tree-sitter": "0.26.0",
    "tree-sitter-go": "0.25.0",
}
TYPESCRIPT_PIN = "5.9.3"
_WORKER = Path(__file__).with_name("typescript_units.cjs")
_EXTENSIONS = {
    ".js": "javascript", ".jsx": "javascript", ".mjs": "javascript", ".cjs": "javascript",
    ".ts": "typescript", ".tsx": "typescript", ".mts": "typescript", ".cts": "typescript",
    ".go": "go", ".py": "python",
}
# Pure syntax containers and expression wrappers do not represent useful units.
_WRAPPERS = {
    "program", "source_file", "statement_list", "expression_statement", "expression", "parenthesized_expression",
    "arguments", "argument_list", "formal_parameters", "parameter_list", "type_annotation", "type_arguments",
    "named_imports", "import_clause", "export_clause",
    "jsx_expression", "template_substitution", "class_body", "switch_body", "else_clause",
}
_BLOCKS = {"statement_block", "block", "class_body", "switch_body"}
_BRANCHES = {"if_statement", "conditional_expression", "switch_case", "for_statement", "for_in_statement",
             "while_statement", "do_statement", "catch_clause", "ternary_expression", "communication_case",
             "expression_case", "type_case"}
_FUNCTIONS = {"function_declaration", "function_expression", "arrow_function", "method_definition",
              "method_declaration", "function_literal"}
_COMMENTS = {"comment", "hash_bang_line"}
# Significant anonymous terminals are folded into their named parent's label,
# so an expression/operator or declaration/modifier remains one syntax unit.
_OPERATORS = {
    "+", "-", "*", "/", "%", "**", "=", "+=", "-=", "*=", "/=", "%=", "&&=", "||=", "??=",
    "&=", "|=", "^=", "<<=", ">>=", ">>>=", ":=", "<-", "&^", "&^=", "==", "===", "!=", "!==",
    "<", ">", "<=", ">=", "&&", "||", "??", "!", "~", "&", "|", "^", "<<", ">>", ">>>", "=>", "...",
    "++", "--", "?", ":", "as", "in", "of", "instanceof", "typeof", "void", "delete", "new", "await",
    "const", "let", "var", "async", "public", "private", "protected", "static", "readonly", "export",
    "default", "implements", "go", "defer", "chan", "fallthrough", "range", "select", "type", "func",
    "package", "import", "var", "return", "break", "continue", "goto", "map", "struct", "interface",
}


def extension_language(path):
    """Return the supported language for a source path, or None."""
    return _EXTENSIONS.get(Path(path).suffix.lower())


def _versions():
    try:
        actual = {name: metadata.version(name) for name in _PINS}
    except metadata.PackageNotFoundError as exc:
        raise ValueError(f"Tree-sitter backend dependency missing; install exact pins: {_install_help()}") from exc
    wrong = [f"{name}=={_PINS[name]} (found {actual[name]})" for name in _PINS if actual[name] != _PINS[name]]
    if wrong:
        raise ValueError(f"Tree-sitter backend requires exact versions: {', '.join(wrong)}; install: {_install_help()}")
    return actual


def _install_help():
    return "python -m pip install tree-sitter==0.26.0 tree-sitter-go==0.25.0"


_TYPESCRIPT_HELP = ("JavaScript/TypeScript tracks need Node.js and the pinned parser: run `npm ci` in the "
                    f"repository root (typescript=={TYPESCRIPT_PIN}), or set PARSIMONY_TYPESCRIPT_DIR to a "
                    "directory whose node_modules contains it")


class _TypeScriptWorker:
    """One long-lived Node process; requests and responses are line-delimited JSON."""
    def __init__(self):
        node = os.environ.get("PARSIMONY_NODE") or shutil.which("node")
        if not node:
            raise ValueError(f"Node.js not found. {_TYPESCRIPT_HELP}")
        self.process = subprocess.Popen([node, str(_WORKER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, encoding="utf-8")
        header = self.process.stdout.readline()
        if not header:
            error = self.process.stderr.read().strip().splitlines()
            self.close()
            raise ValueError(f"TypeScript parser unavailable ({error[-1] if error else 'no output'}). {_TYPESCRIPT_HELP}")
        self.version = json.loads(header)["typescript"]

    def request(self, path, source):
        self.process.stdin.write(json.dumps({"path": path, "source": source}) + "\n")
        self.process.stdin.flush()
        line = self.process.stdout.readline()
        if not line:
            raise RuntimeError("TypeScript parser process exited unexpectedly")
        response = json.loads(line)
        if response.get("fatal"):
            raise RuntimeError(f"TypeScript parser failed: {response['error']}")
        return response

    def close(self):
        self.process.stdin.close()
        self.process.wait(timeout=10)
        self.process.stdout.close()
        self.process.stderr.close()


_worker = None


def _typescript():
    global _worker
    if _worker is None:
        _worker = _TypeScriptWorker()
        atexit.register(_worker.close)
    if _worker.version != TYPESCRIPT_PIN:
        raise ValueError(f"TypeScript parser requires typescript=={TYPESCRIPT_PIN} (found {_worker.version}). "
                         f"{_TYPESCRIPT_HELP}")
    return _worker


def track(language):
    """Describe a track; Python remains owned by the stdlib AST backend."""
    if language not in SUPPORTED:
        raise ValueError(f"unsupported language: {language}")
    if language == "python":
        return None
    if language in ("javascript", "typescript"):
        _typescript()
        return {"language": language, "unit_version": TYPESCRIPT_UNIT_VERSION,
                "versions": {"typescript": TYPESCRIPT_PIN}}
    return {"language": language, "unit_version": UNIT_VERSION, "versions": _versions()}


@dataclass
class Parsed:
    language: str
    tree: object
    source: bytes
    line_starts: list


@dataclass
class CompilerParsed:
    """Units, tokens and structure computed by the TypeScript parser worker."""
    language: str
    units: list
    plain: list
    tokens: list
    structure: tuple


def _rows(pairs):
    result = []
    for row, label in pairs:
        if result and result[-1][0] == row:
            result[-1][1].append(label)
        else:
            result.append((row, [label]))
    return [tuple(labels) for _, labels in result]


def parse(source, path):
    """Parse source without execution. Invalid or recovered syntax is rejected."""
    language = extension_language(path)
    if language is None or language == "python":
        raise ValueError(f"unsupported source path for the language backends: {path}")
    if language in ("javascript", "typescript"):
        text = source.decode("utf-8") if isinstance(source, bytes) else source
        response = _typescript().request(path, text)
        if not response["ok"]:
            raise ValueError(f"invalid or recovered {language} syntax: {response['error']}")
        return CompilerParsed(language, _rows(response["units"]), _rows(response["plain"]),
                              _rows(response["tokens"]), tuple(response["structure"]))
    _versions()
    from tree_sitter import Language, Parser
    import tree_sitter_go as grammar
    parser = Parser(Language(grammar.language()))
    data = source.encode("utf-8") if isinstance(source, str) else bytes(source)
    tree = parser.parse(data)
    if tree.root_node.has_error:
        raise ValueError(f"invalid or recovered {language} syntax")
    # Use byte offsets, not the binding's Point objects: repeated point access
    # on large trees can corrupt memory with the Python 3.14 wheel of 0.26.0.
    return Parsed(language, tree, data, [0] + [i + 1 for i, c in enumerate(data) if c == 10])


def _label(node, keep_values, source):
    kind = node.type
    value_kinds = {"identifier", "type_identifier", "property_identifier", "field_identifier",
                   "shorthand_property_identifier", "number", "int_literal", "float_literal", "string",
                   "interpreted_string_literal", "raw_string_literal", "string_literal", "true", "false", "null", "nil"}
    if kind in _COMMENTS:
        return None
    if keep_values and kind in value_kinds:
        text = source[node.start_byte:node.end_byte].decode('utf-8', 'replace')
        if kind in {"string", "string_literal", "interpreted_string_literal", "raw_string_literal"} and len(text) >= 2:
            text = text[1:-1]
        return f"{kind}:{text}"
    if keep_values and node.child_count == 0:
        return f"{kind}:{source[node.start_byte:node.end_byte].decode('utf-8', 'replace')}"
    return kind


def _unit_label(node, keep_values, source):
    label = _label(node, keep_values, source)
    if label is None:
        return None
    punctuation = {'(', ')', '{', '}', '[', ']', ',', ';', '.', '\"', "'", '`'}
    terminals = [child.type for child in node.children
                 if not child.is_named and child.type not in punctuation]
    return label + ("[" + ",".join(terminals) + "]" if terminals else "")


def unit_lines(parsed, keep_values=True):
    """Return preorder syntax units grouped by source row, with block-end markers."""
    if isinstance(parsed, CompilerParsed):
        return parsed.units if keep_values else parsed.plain
    result = []
    def add(row, label):
        if label is None:
            return
        if result and result[-1][0] == row:
            result[-1][1].append(label)
        else:
            result.append((row, [label]))
    stack = [parsed.tree.root_node]
    while stack:
        node = stack.pop()
        if isinstance(node, tuple):
            add(node[1], "EndBlock")
            continue
        if node.type in _COMMENTS:
            continue
        if node.is_named and node.type not in _WRAPPERS:
            add(bisect_right(parsed.line_starts, node.start_byte), _unit_label(node, keep_values, parsed.source))
        # The marker sits beneath descendants and is visited after the block.
        if node.type in _BLOCKS:
            stack.append(("end", bisect_right(parsed.line_starts, node.end_byte)))
        # A literal is one value-sensitive unit, not a unit per escape/fragment.
        if node.type not in {'string', 'string_literal', 'interpreted_string_literal', 'raw_string_literal'}:
            stack.extend(reversed(node.children))
    return [tuple(labels) for _, labels in result]


def token_lines(parsed):
    """Normalized significant lexical leaves, grouped by source row."""
    if isinstance(parsed, CompilerParsed):
        return parsed.tokens
    result = []
    stack = [parsed.tree.root_node]
    while stack:
        node = stack.pop()
        if node.type in _COMMENTS:
            continue
        if node.child_count == 0:
            # Slice our owned bytes: avoid Node.text's native slice path on Python 3.14.
            value = parsed.source[node.start_byte:node.end_byte].decode('utf-8', 'replace')
            if node.is_named or node.type in _OPERATORS:
                token = f"{node.type}:{value}"
                row = bisect_right(parsed.line_starts, node.start_byte)
                if result and result[-1][0] == row:
                    result[-1][1].append(token)
                else:
                    result.append((row, [token]))
        else:
            stack.extend(reversed(node.children))
    return [tuple(tokens) for _, tokens in result]


def structure(parsed):
    """Return named-node count and a simple branch-count cyclomatic proxy."""
    if isinstance(parsed, CompilerParsed):
        return parsed.structure
    count = branches = 0
    stack = [parsed.tree.root_node]
    while stack:
        node = stack.pop()
        if node.is_named and node.type not in _COMMENTS:
            count += 1
            if node.type in _FUNCTIONS:
                branches += 1
            if node.type in _BRANCHES:
                branches += 1
            if node.type == "binary_expression":
                branches += sum(child.type in {"&&", "||", "and", "or"} for child in node.children)
        stack.extend(node.children)
    return count, branches
