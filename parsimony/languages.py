"""Optional Tree-sitter coding-unit backend for JavaScript, TypeScript and Go.

These syntax-derived counts are not semantic complexity and are not comparable
across languages. Tree-sitter dependencies are deliberately imported lazily.
"""
from bisect import bisect_right
from dataclasses import dataclass
from importlib import metadata
from pathlib import Path

SUPPORTED = ("python", "javascript", "typescript", "go")
UNIT_VERSION = "tree-sitter-units-v1"
_PINS = {
    "tree-sitter": "0.26.0",
    "tree-sitter-javascript": "0.25.0",
    "tree-sitter-typescript": "0.23.2",
    "tree-sitter-go": "0.25.0",
}
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
    return "python -m pip install tree-sitter==0.26.0 tree-sitter-javascript==0.25.0 tree-sitter-typescript==0.23.2 tree-sitter-go==0.25.0"


def track(language):
    """Describe a track; Python remains owned by the stdlib AST backend."""
    if language not in SUPPORTED:
        raise ValueError(f"unsupported language: {language}")
    if language == "python":
        return None
    return {"language": language, "unit_version": UNIT_VERSION, "versions": _versions()}


@dataclass
class Parsed:
    language: str
    tree: object
    source: bytes
    line_starts: list


def parse(source, path):
    """Parse source without execution. Invalid or recovered syntax is rejected."""
    language = extension_language(path)
    if language is None or language == "python":
        raise ValueError(f"unsupported Tree-sitter source path: {path}")
    _versions()
    from tree_sitter import Language, Parser
    if language == "javascript":
        import tree_sitter_javascript as grammar
        capsule = grammar.language()
    elif language == "typescript":
        import tree_sitter_typescript as grammar
        capsule = grammar.language_tsx() if Path(path).suffix.lower() == ".tsx" else grammar.language_typescript()
    else:
        import tree_sitter_go as grammar
        capsule = grammar.language()
    parser = Parser(Language(capsule))
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
