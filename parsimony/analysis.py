"""Static Python footprint analysis. Never imports or executes submitted code."""
from __future__ import annotations

import ast
import difflib
import io
import keyword
import re
import tokenize
import warnings
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
    excluded = {'test', 'tests', 'docs', 'doc', 'examples', 'benchmarks',
                'vendor', 'vendored', 'third_party', 'third-party', 'external',
                'generated', 'build', 'dist', '__pycache__', '.github',
                '_vendor', '_vendored', 'node_modules', '.venv', 'venv', 'fixtures',
                'testdata', 'test_data', 'documentation'}
    parts = p.parts
    # Django's db/migrations package is framework implementation; migration
    # script directories elsewhere remain excluded. Keep numbered scripts out.
    django_migrations_core = (len(parts) >= 4 and parts[:3] == ('django', 'db', 'migrations')
                              and not re.match(r'^\d{4,}_.*\.py$', p.name))
    # Likewise django/test/ is the public testing framework (TestCase, Client,
    # runner), not the project's own tests.
    django_test_framework = len(parts) >= 3 and parts[:2] == ('django', 'test')
    # A top-level testing/ directory is a test suite (pytest); nested ones such as
    # sympy/testing/ or lib/matplotlib/testing/ are shipped library code.
    return (p.suffix == '.py' and parts[0] != 'testing' and not (excluded.intersection(parts)
                                       - ({'migrations'} if django_migrations_core else set())
                                       - ({'test'} if django_test_framework else set()))
            and ('migrations' not in parts or django_migrations_core)
            and p.name not in {'test.py', 'tests.py'}
            and not p.name.startswith(('test_', 'conftest.', 'setup.', '_vendor'))
            and not p.name.endswith(('_test.py', '_pb2.py', '_pb2_grpc.py')))


def generated(source: str) -> bool:
    # Require an explicit header comment, not a prose occurrence in a docstring
    # or ordinary implementation (e.g. "features generated by each transformer").
    header = source[:2000].splitlines()[:20]
    return any(re.search(r'^\s*#\s*(?:this file (?:is|was) )?'
                         r'(?:auto[- ]?generated|generated (?:by|file)|do not edit)\b', line, re.I)
               for line in header)


def locate(lines, old, expected, cursor):
    """Line index where ``old`` matches exactly, preferring ``expected``.

    Like ``git apply``, a hunk whose exact context sits at a shifted line
    number is applied at the nearest match (never before ``cursor``); context
    is never fuzzed. Equidistant matches are ambiguous and rejected.
    """
    def fits(i):
        return cursor <= i <= len(lines) - len(old) and lines[i:i + len(old)] == old
    if fits(expected) or not old:
        return expected
    for distance in range(1, len(lines) + 1):
        hits = [i for i in (expected - distance, expected + distance) if fits(i)]
        if len(hits) == 2:
            raise ValueError('ambiguous hunk position')
        if hits:
            return hits[0]
        if expected - distance < cursor and expected + distance > len(lines) - len(old):
            break
    raise ValueError('patch context differs from base commit')


def apply_patch(source: str, file: FilePatch, offsets: list | None = None) -> str:
    """Apply hunks strictly by content; shifted positions are appended to ``offsets``."""
    lines = source.splitlines(keepends=True)
    out = []
    cursor = 0
    shift = 0
    for start, count, newstart, newcount, body in file.hunks:
        stated = start - 1 if count else start
        if stated + shift < cursor or stated + shift > len(lines):
            raise ValueError('hunk position outside source or overlapping')
        old = [line[1:] for line in body if line[0] in ' -']
        pos = locate(lines, old, stated + shift, cursor)
        if pos != stated and offsets is not None:
            offsets.append(pos - stated)
        shift = pos - stated
        out.extend(lines[cursor:pos])
        if len(out) != (newstart - 1 if newcount else newstart) + shift:
            raise ValueError('new hunk position mismatch')
        cursor = pos
        for line in body:
            if line[0] in ' -':
                cursor += 1
            if line[0] in ' +':
                out.append(line[1:])
    out.extend(lines[cursor:])
    return ''.join(out)


def tree(source: str):
    try:
        # Target repositories' own invalid escapes etc. are not analysis problems.
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', SyntaxWarning)
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


def lexemes(source: str) -> list[tuple[int, str, str]]:
    """(line, kind, text) for every significant token; kind selects normalization."""
    kinds = {tokenize.NAME: 'name', tokenize.STRING: 'str', tokenize.NUMBER: 'num',
             getattr(tokenize, 'FSTRING_START', -1): 'fstart',
             getattr(tokenize, 'FSTRING_MIDDLE', -1): 'fmiddle',
             getattr(tokenize, 'FSTRING_END', -1): 'fend'}
    ignored = {tokenize.ENCODING, tokenize.ENDMARKER, tokenize.NL, tokenize.NEWLINE,
               tokenize.COMMENT}
    result = []
    try:
        for tok in tokenize.generate_tokens(io.StringIO(source).readline):
            if tok.type in ignored or (tok.type == tokenize.ERRORTOKEN and tok.string.isspace()):
                continue
            if tok.type in (tokenize.INDENT, tokenize.DEDENT):
                # Block structure changes behavior; use canonical symbols rather
                # than indentation whitespace (also works for lexical fallback).
                result.append((tok.start[0], 'other', 'INDENT' if tok.type == tokenize.INDENT else 'DEDENT'))
            else:
                result.append((tok.start[0], kinds.get(tok.type, 'other'), tok.string))
    except (tokenize.TokenError, IndentationError, SyntaxError) as exc:
        raise ValueError(f'cannot tokenize Python: {exc}') from exc
    return result


PLACEHOLDERS = {'str': 'STR', 'num': 'NUM', 'fstart': 'STR_START', 'fmiddle': 'STR_PART', 'fend': 'STR_END'}


def group_lines(tokens, keep_values: bool = True) -> list[tuple]:
    """Group lexemes by line; without values, identifiers/literals become placeholders."""
    lines = {}
    for line, kind, text in tokens:
        if kind == 'name':
            value = text if keep_values or keyword.iskeyword(text) else 'ID'
        elif kind in ('fstart', 'fend'):
            value = PLACEHOLDERS[kind]
        elif kind in PLACEHOLDERS:
            value = text if keep_values else PLACEHOLDERS[kind]
        else:
            value = text
        lines.setdefault(line, []).append(value)
    return [tuple(lines[n]) for n in sorted(lines)]


def canonical(root) -> str:
    # Canonical syntax removes redundant parentheses, quote styles and
    # optional trailing commas as well as whitespace/comments/docstrings.
    return ast.unparse(without_docstrings(root))


def token_lines(source: str, keep_values: bool = True, canonical_form: bool = True) -> list[tuple]:
    """Normalized tokens grouped by (canonical) source line.

    ``canonical_form`` re-renders parseable code with ``ast.unparse`` first;
    callers must use the same setting for both sides of a comparison.
    """
    root = tree(source) if canonical_form else None
    return group_lines(lexemes(canonical(root) if root is not None else source), keep_values)


def normalized_tokens(source: str, keep_values: bool = False, canonical_form: bool = True) -> list[str]:
    return [t for line in token_lines(source, keep_values, canonical_form) for t in line]


MAX_EDIT_DISTANCE = 1500


def myers(a, b, max_d=MAX_EDIT_DISTANCE):
    """Minimal (LCS) alignment as (added, deleted), or None beyond max_d edits.

    O((N+M)D) time: fast for the local edits typical of patches regardless of
    how repetitive the sequences are (unlike difflib's quadratic worst case).
    """
    n, m = len(a), len(b)
    v = {1: 0}
    for d in range(max_d + 1):
        for k in range(-d, d + 1, 2):
            x = v[k + 1] if k == -d or (k != d and v[k - 1] < v[k + 1]) else v[k - 1] + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x
            if x >= n and y >= m:
                lcs = (n + m - d) // 2
                return m - lcs, n - lcs
    return None


def myers_blocks(a, b, max_d=MAX_EDIT_DISTANCE):
    """Minimal alignment as a list of changed (a1, a2, b1, b2) blocks, or None."""
    n, m = len(a), len(b)
    v = {1: 0}
    trace = []
    for d in range(max_d + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            x = v[k + 1] if k == -d or (k != d and v[k - 1] < v[k + 1]) else v[k - 1] + 1
            y = x - k
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x
            if x >= n and y >= m:
                break
        else:
            continue
        break
    else:
        return None
    # Backtrack, collecting matched pairs, then derive the changed gaps.
    matches = []
    x, y = n, m
    for d in range(len(trace) - 1, -1, -1):
        v = trace[d]
        k = x - y
        prev_k = k + 1 if k == -d or (k != d and v[k - 1] < v[k + 1]) else k - 1
        prev_x = v[prev_k]
        prev_y = prev_x - prev_k
        while x > prev_x and y > prev_y:
            x -= 1
            y -= 1
            matches.append((x, y))
        x, y = prev_x, prev_y
    matches.reverse()
    blocks = []
    i = j = 0
    for mx, my in matches + [(n, m)]:
        if mx > i or my > j:
            blocks.append((i, mx, j, my))
        i, j = mx + 1, my + 1
    return blocks


MAX_GLOBAL_EDIT_DISTANCE = 500


def token_diff(a_lines, b_lines):
    """(added, deleted, approximate) for line-grouped token sequences.

    Normally an exact minimal token edit script (Myers after trimming the common
    prefix/suffix), fast for the local edits typical of patches. Rewrites beyond
    MAX_GLOBAL_EDIT_DISTANCE are approximated by anchoring unchanged lines and
    aligning changed blocks minimally (difflib for huge blocks); these results
    are flagged approximate because line anchoring can overstate churn.
    """
    a = [t for line in a_lines for t in line]
    b = [t for line in b_lines for t in line]
    start = 0
    while start < len(a) and start < len(b) and a[start] == b[start]:
        start += 1
    end = 0
    while end < len(a) - start and end < len(b) - start and a[-1 - end] == b[-1 - end]:
        end += 1
    counts = myers(a[start:len(a) - end], b[start:len(b) - end], MAX_GLOBAL_EDIT_DISTANCE)
    if counts is not None:
        return counts[0], counts[1], False
    # Line anchoring: minimal when few lines changed, else difflib (fast on varied lines).
    blocks = myers_blocks(a_lines, b_lines, max_d=200)
    if blocks is None:
        blocks = [(a1, a2, b1, b2) for op, a1, a2, b1, b2 in
                  difflib.SequenceMatcher(None, a_lines, b_lines, autojunk=False).get_opcodes()
                  if op != 'equal']
    added = deleted = 0
    for a1, a2, b1, b2 in blocks:
        block_a = [t for line in a_lines[a1:a2] for t in line]
        block_b = [t for line in b_lines[b1:b2] for t in line]
        counts = myers(block_a, block_b) if block_a and block_b else (len(block_b), len(block_a))
        if counts is None:
            counts = [0, 0]
            for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, block_a, block_b,
                                                              autojunk=False).get_opcodes():
                if op != 'equal':
                    counts[0] += j2 - j1
                    counts[1] += i2 - i1
        added += counts[0]
        deleted += counts[1]
    return added, deleted, True


# Syntax that is not a coding unit of its own: load/store markers, operators
# (folded into their expression's label) and pure containers.
NON_UNITS = (ast.expr_context, ast.operator, ast.unaryop, ast.cmpop, ast.boolop,
             ast.Module, ast.Expr, ast.arguments, ast.withitem, ast.FormattedValue)


def unit_labels(node, keep_values=True):
    """Coding units a node contributes: one per statement, expression, name or literal.

    A comparison chain counts one unit per comparison and a boolean operation
    one per extra operand. Without values, identifiers/literals become their
    node type, like ``structural_churn``'s placeholders.
    """
    kind = type(node).__name__
    if isinstance(node, NON_UNITS):
        return []
    if isinstance(node, ast.Compare):
        return [f'Compare:{type(op).__name__}' for op in node.ops]
    if isinstance(node, ast.BoolOp):
        return [f'BoolOp:{type(node.op).__name__}'] * (len(node.values) - 1)
    if isinstance(node, (ast.BinOp, ast.AugAssign, ast.UnaryOp)):
        return [f'{kind}:{type(node.op).__name__}']
    if isinstance(node, (ast.Global, ast.Nonlocal)):
        return [f'{kind}:{name}' if keep_values else kind for name in node.names]
    if not keep_values:
        return [kind]
    if isinstance(node, ast.Constant):
        return [f'Constant:{node.value!r}']
    # Identifiers (Name.id, Attribute.attr, FunctionDef.name, arg.arg, keyword.arg,
    # alias names, ImportFrom.module, MatchClass.kwd_attrs, ...) are part of the unit.
    names = [value for field, value in ast.iter_fields(node) if isinstance(value, str)]
    names += [item for field, value in ast.iter_fields(node) if isinstance(value, list)
              for item in value if isinstance(item, str)]
    return [':'.join([kind, *names])]


END_BLOCK = 'EndBlock'


def unit_lines(root, keep_values=True) -> list[tuple]:
    """Preorder coding units of a docstring-free tree, grouped into runs by source line.

    Each statement block (a body, ``else`` or ``finally``) ends with one
    ``EndBlock`` unit, so moving a statement into or out of a block is an edit
    and every level of nesting costs a unit.
    """
    lines = []
    stack = [(root, 0)]
    while stack:
        node, line = stack.pop()
        if node is END_BLOCK:
            labels = [END_BLOCK]
        else:
            line = getattr(node, 'lineno', line)
            labels = unit_labels(node, keep_values)
        if labels:
            if lines and lines[-1][0] == line:
                lines[-1][1].extend(labels)
            else:
                lines.append((line, labels))
        if node is END_BLOCK:
            continue
        children = []
        for field, value in ast.iter_fields(node):
            if isinstance(value, ast.AST):
                children.append(value)
            elif isinstance(value, list):
                children.extend(item for item in value if isinstance(item, ast.AST))
                if (field in ('body', 'orelse', 'finalbody') and value and isinstance(value[0], ast.stmt)
                        and not isinstance(node, ast.Module)):
                    children.append(END_BLOCK)
        stack.extend((child, line) for child in reversed(children))
    return [tuple(labels) for _, labels in lines]


def structure(source: str, stripped=None):
    """AST node count and cyclomatic proxy; ``stripped`` is a tree already without docstrings."""
    if stripped is None:
        root = tree(source)
        if root is None:
            return None
        stripped = without_docstrings(root)
    nodes = list(ast.walk(stripped))
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
    """get_source(path) provides exact base-commit text; otherwise estimate hunks.

    The primary footprint counts coding units (``unit_lines``); normalized
    lexical tokens remain a diagnostic. Unit fields are None when any measured
    file does not parse on both sides, since units need a syntax tree.
    """
    totals = dict(units_added=0, units_deleted=0, net_units=0, churn=0, structural_churn=0,
                  tokens_added=0, tokens_deleted=0, net_tokens=0, token_churn=0,
                  files_changed=0, ast_delta=0, complexity_delta=0)
    unit_fields = ('units_added', 'units_deleted', 'net_units', 'churn', 'structural_churn')
    units_known = True
    offsets = []
    excluded = []
    touched = []
    lexical = []
    approximate = []
    mode = 'full_file' if get_source else 'patch_only'
    if not get_source:
        totals['ast_delta'] = totals['complexity_delta'] = None
    for f in parse_patch(patch):
        path = f.new if f.new != '/dev/null' else f.old
        touched.append(path)
        if not implementation(path) or (f.old != '/dev/null' and not implementation(f.old)):
            excluded.append(path)
            continue
        if not f.hunks:
            raise ValueError('file has no text hunks')
        if get_source:
            before = '' if f.old == '/dev/null' else get_source(f.old)
            after = apply_patch(before, f, offsets)
        else:
            before = ''.join(line[1:] for h in f.hunks for line in h[4] if line[0] in ' -')
            after = ''.join(line[1:] for h in f.hunks for line in h[4] if line[0] in ' +')
        # Only the base commit decides: a patch must not hide its own edits by
        # adding a generated-file header. New files are always the patch's own code.
        if f.old != '/dev/null' and generated(before):
            excluded.append(path)
            continue
        # Canonicalize both sides or neither: mixing an ast.unparse rendering
        # with raw tokens would count formatting differences as edits.
        roots = tree(before), tree(after)
        parsed = None not in roots
        if not parsed:
            lexical.append(path)
        la, lb = (lexemes(canonical(root) if parsed else text) for root, text in zip(roots, (before, after)))
        a, b = group_lines(la), group_lines(lb)
        added, deleted, rough = token_diff(a, b)
        totals['tokens_added'] += added
        totals['tokens_deleted'] += deleted
        if parsed:
            # canonical() already stripped docstrings from these trees.
            added, deleted, rough_units = token_diff(*(unit_lines(root) for root in roots))
            # Diagnostic: identifier/literal-insensitive unit churn.
            s_added, s_deleted, s_rough = token_diff(*(unit_lines(root, False) for root in roots))
            totals['units_added'] += added
            totals['units_deleted'] += deleted
            totals['structural_churn'] += s_added + s_deleted
            rough = rough or rough_units or s_rough
        else:
            units_known = False
        if rough:
            approximate.append(path)
        # Count implementation files with actual normalized changes, not formatting-only files.
        totals['files_changed'] += int(a != b)
        if get_source:
            # Stripping docstrings twice would also drop a string statement that became first.
            sa, sb = (structure('', stripped=root) if parsed else None for root in roots)
            if sa is None or sb is None:
                totals['ast_delta'] = totals['complexity_delta'] = None
            elif totals['ast_delta'] is not None:
                totals['ast_delta'] += sb[0] - sa[0]
                totals['complexity_delta'] += sb[1] - sa[1]
    totals['net_tokens'] = totals['tokens_added'] - totals['tokens_deleted']
    totals['token_churn'] = totals['tokens_added'] + totals['tokens_deleted']
    totals['net_units'] = totals['units_added'] - totals['units_deleted']
    totals['churn'] = totals['units_added'] + totals['units_deleted']
    if not units_known:
        totals.update(dict.fromkeys(unit_fields))
    return {**totals, 'mode': mode, 'touched_files': touched, 'excluded_files': excluded,
            'lexical_files': lexical, 'approximate_files': approximate, 'offset_hunks': len(offsets)}
