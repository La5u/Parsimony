"""Static Python footprint analysis. Never imports or executes submitted code."""
from __future__ import annotations

import ast
import difflib
import io
import keyword
import re
import tokenize
from dataclasses import dataclass
from pathlib import PurePosixPath


@dataclass
class FilePatch:
    old: str
    new: str
    hunks: list


def parse_patch(patch: str) -> list[FilePatch]:
    """Parse unified text diffs, rejecting malformed/incomplete hunks."""
    # Do not silently omit implementation renames/binary changes when they
    # accompany supported text edits elsewhere in the same patch.
    for block in re.split(r'(?m)^diff --git ', patch)[1:]:
        header = block.splitlines()[0]
        paths = header.split()
        if len(paths) != 2:
            raise ValueError('unsupported quoted/space-containing diff paths')
        if any(implementation(p) for p in paths) and not re.search(r'(?m)^--- ', block):
            raise ValueError('implementation binary/rename/mode-only diff unsupported')
    lines = patch.splitlines(keepends=True)
    files = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith('--- '):
            i += 1
            continue
        old = lines[i][4:].split('\t')[0].strip()
        i += 1
        if i >= len(lines) or not lines[i].startswith('+++ '):
            raise ValueError('missing +++ file header')
        new = lines[i][4:].split('\t')[0].strip()
        def path(p):
            if p.startswith(('a/', 'b/')):
                p = p[2:]
            if p != '/dev/null' and (p.startswith('/') or '..' in PurePosixPath(p).parts or '"' in p):
                raise ValueError('unsupported or unsafe patch path')
            return p
        f = FilePatch(path(old), path(new), [])
        files.append(f)
        i += 1
        while i < len(lines):
            if lines[i].startswith(('diff --git ', '--- ')):
                break
            match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', lines[i])
            if not match:
                i += 1
                continue
            start, count, newstart, newcount = (int(v) if v is not None else 1 for v in match.groups())
            i += 1
            body = []
            a = b = 0
            while i < len(lines) and (a < count or b < newcount):
                line = lines[i]
                if line.startswith('\\ No newline'):
                    if body:
                        body[-1] = body[-1].rstrip('\r\n')
                    i += 1
                    continue
                if not line or line[0] not in ' +-':
                    raise ValueError('invalid hunk line')
                body.append(line)
                a += line[0] in ' -'
                b += line[0] in ' +'
                i += 1
            if i < len(lines) and lines[i].startswith('\\ No newline'):
                body[-1] = body[-1].rstrip('\r\n')
                i += 1
            if (a, b) != (count, newcount):
                raise ValueError('hunk length mismatch')
            f.hunks.append((start, count, newstart, newcount, body))
    if patch.strip() and not files:
        raise ValueError('no supported unified diff (binary/rename-only patches unsupported)')
    return files


def implementation(path: str) -> bool:
    p = PurePosixPath(path.lower())
    excluded = {'test', 'tests', 'testing', 'docs', 'doc', 'examples', 'benchmarks',
                'vendor', 'vendored', 'third_party', 'third-party', 'external',
                'generated', 'build', 'dist', 'migrations', '__pycache__', '.github',
                '_vendor', '_vendored', 'node_modules', '.venv', 'venv', 'fixtures',
                'testdata', 'test_data', 'documentation'}
    return (p.suffix == '.py' and not excluded.intersection(p.parts)
            and p.name not in {'test.py', 'tests.py'}
            and not p.name.startswith(('test_', 'conftest.', 'setup.', '_vendor'))
            and not p.name.endswith(('_test.py', '_pb2.py', '_pb2_grpc.py')))


def generated(source: str) -> bool:
    return bool(re.search(r'(auto[- ]?generated|generated (?:by|file)|do not edit)', source[:2000], re.I))


def apply_patch(source: str, file: FilePatch) -> str:
    lines = source.splitlines(keepends=True)
    out = []
    cursor = 0
    for start, count, newstart, newcount, body in file.hunks:
        pos = start - 1 if count else start
        if pos < cursor or pos > len(lines):
            raise ValueError('hunk position outside source or overlapping')
        out.extend(lines[cursor:pos])
        if len(out) != (newstart - 1 if newcount else newstart):
            raise ValueError('new hunk position mismatch')
        cursor = pos
        for line in body:
            if line[0] in ' -':
                if cursor >= len(lines) or lines[cursor] != line[1:]:
                    raise ValueError('patch context differs from base commit')
                cursor += 1
            if line[0] in ' +':
                out.append(line[1:])
    out.extend(lines[cursor:])
    return ''.join(out)


def tree(source: str):
    try:
        return ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return None


def docstring_nodes(root):
    if root is None:
        return []
    return [n.body[0] for n in ast.walk(root)
            if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
            and n.body and isinstance(n.body[0], ast.Expr)
            and isinstance(n.body[0].value, ast.Constant)
            and isinstance(n.body[0].value.value, str)]


def without_docstrings(root):
    docs = set(docstring_nodes(root))
    for n in ast.walk(root):
        if isinstance(n, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            n.body = [statement for statement in n.body if statement not in docs]
    return root


def normalized_tokens(source: str) -> list[str]:
    root = tree(source)
    if root is not None:
        # Canonical syntax removes redundant parentheses, quote styles and
        # optional trailing commas as well as whitespace/comments/docstrings.
        source = ast.unparse(without_docstrings(root))
    result = []
    ignored = {tokenize.ENCODING, tokenize.ENDMARKER, tokenize.NL, tokenize.NEWLINE,
               tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT}
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type in ignored:
                continue
            if tok.type == tokenize.NAME:
                result.append(tok.string if keyword.iskeyword(tok.string) else 'ID')
            elif tok.type == tokenize.STRING:
                result.append('STR')
            elif tok.type == tokenize.NUMBER:
                result.append('NUM')
            elif tok.type == getattr(tokenize, 'FSTRING_START', -1):
                result.append('STR_START')
            elif tok.type == getattr(tokenize, 'FSTRING_MIDDLE', -1):
                result.append('STR_PART')
            elif tok.type == getattr(tokenize, 'FSTRING_END', -1):
                result.append('STR_END')
            elif tok.type == tokenize.ERRORTOKEN and tok.string.isspace():
                continue
            else:
                result.append(tok.string)
    except (tokenize.TokenError, IndentationError, SyntaxError) as exc:
        raise ValueError(f'cannot tokenize Python: {exc}') from exc
    return result


def structure(source: str):
    root = tree(source)
    if root is None:
        return None
    nodes = list(ast.walk(without_docstrings(root)))
    # Explicit cyclomatic proxy: function baselines plus decision points.
    complexity = 0
    for n in nodes:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda,
                          ast.If, ast.IfExp, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(n, ast.BoolOp):
            complexity += len(n.values) - 1
        elif isinstance(n, ast.comprehension):
            complexity += 1 + len(n.ifs)
        elif isinstance(n, ast.Match):
            complexity += sum(not (isinstance(c.pattern, ast.MatchAs) and c.pattern.pattern is None
                                   and c.guard is None) for c in n.cases)
    return len(nodes), complexity


def measure(patch: str, get_source=None) -> dict:
    """get_source(path) provides exact base-commit text; otherwise estimate hunks."""
    totals = dict(tokens_added=0, tokens_deleted=0, net_tokens=0, churn=0,
                  files_changed=0, ast_delta=0, complexity_delta=0)
    excluded = []
    mode = 'full_file' if get_source else 'patch_only'
    if not get_source:
        totals['ast_delta'] = totals['complexity_delta'] = None
    for f in parse_patch(patch):
        path = f.new if f.new != '/dev/null' else f.old
        if not implementation(path) or (f.old != '/dev/null' and not implementation(f.old)):
            excluded.append(path)
            continue
        if not f.hunks:
            raise ValueError('file has no text hunks')
        if get_source:
            before = '' if f.old == '/dev/null' else get_source(f.old)
            after = apply_patch(before, f)
        else:
            before = ''.join(line[1:] for h in f.hunks for line in h[4] if line[0] in ' -')
            after = ''.join(line[1:] for h in f.hunks for line in h[4] if line[0] in ' +')
        if generated(before) or generated(after):
            excluded.append(path)
            continue
        a, b = normalized_tokens(before), normalized_tokens(after)
        added = deleted = 0
        for op, a1, a2, b1, b2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if op != 'equal':
                added += b2 - b1
                deleted += a2 - a1
        totals['tokens_added'] += added
        totals['tokens_deleted'] += deleted
        # Count implementation files with actual normalized changes, not formatting-only files.
        totals['files_changed'] += int(a != b)
        if get_source:
            sa, sb = structure(before), structure(after)
            if sa is None or sb is None:
                totals['ast_delta'] = totals['complexity_delta'] = None
            elif totals['ast_delta'] is not None:
                totals['ast_delta'] += sb[0] - sa[0]
                totals['complexity_delta'] += sb[1] - sa[1]
    totals['net_tokens'] = totals['tokens_added'] - totals['tokens_deleted']
    totals['churn'] = totals['tokens_added'] + totals['tokens_deleted']
    return {**totals, 'mode': mode, 'excluded_files': excluded}
