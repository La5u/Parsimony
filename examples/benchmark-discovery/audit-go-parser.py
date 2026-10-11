#!/usr/bin/env python3
"""Static, metadata-only audit of the seven frozen DeepSWE Go errors.

Run from repository root with the pinned languages Python environment. Raw inputs
stay in --cache (must be under /tmp). --parser is our compiled go/parser helper,
never a target executable. No builds, imports or tests of submitted code occur.
"""
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
import subprocess
import sys
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from parsimony.analysis import apply_patch, generated, implementation, parse_patch
from tree_sitter import Language, Parser
import tree_sitter_go


def sha(data):
    return hashlib.sha256(data).hexdigest()


def fetch(url, cache):
    path = cache / sha(url.encode())
    if not path.exists():
        with urllib.request.urlopen(url, timeout=60) as response:
            data = response.read(16 * 1024 * 1024 + 1)
        if len(data) > 16 * 1024 * 1024:
            raise ValueError('download exceeds 16 MiB bound')
        path.write_bytes(data)
    data = path.read_bytes()
    if len(data) > 16 * 1024 * 1024:
        raise ValueError('cached download exceeds bound')
    return data


def inspect(data, parser, official, cache):
    tree = parser.parse(data)
    errors = []
    unlocalized = []
    stack = [tree.root_node]
    while stack:
        node = stack.pop()
        if node.is_error or node.is_missing:
            errors.append(dict(kind=node.type, missing=node.is_missing,
                               start_byte=node.start_byte, end_byte=node.end_byte,
                               line=data[:node.start_byte].count(b'\n') + 1,
                               end_line=data[:node.end_byte].count(b'\n') + 1))
        if node.has_error and not node.is_error and not node.is_missing and not any(c.has_error for c in node.children):
            unlocalized.append(dict(kind=node.type, start_byte=node.start_byte, end_byte=node.end_byte))
        stack.extend(reversed(node.children))
    source = cache / (sha(data) + '.go')
    source.write_bytes(data)
    result = json.loads(subprocess.check_output([official, str(source)], timeout=30))
    return dict(sha256=sha(data), bytes=len(data), final_newline=data.endswith(b'\n'), tree_sitter_ok=not tree.root_node.has_error,
                tree_sitter_errors=errors, tree_sitter_unlocalized_errors=unlocalized, official_go=result)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cache', required=True, type=Path)
    ap.add_argument('--parser', required=True)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args()
    if not args.cache.resolve().is_relative_to(Path('/tmp')):
        ap.error('raw cache must be under /tmp')
    args.cache.mkdir(parents=True, exist_ok=True)
    versions = {n: importlib.metadata.version(n) for n in ('tree-sitter', 'tree-sitter-go')}
    assert versions == {'tree-sitter': '0.26.0', 'tree-sitter-go': '0.25.0'}, versions
    parser = Parser(Language(tree_sitter_go.language()))
    population_path = Path('examples/deepswe-go/population.json')
    population = json.loads(population_path.read_bytes())
    records = []
    total = 0
    for path in sorted(Path('examples/deepswe-go').glob('*.jsonl')):
        for line_number, line in enumerate(path.read_bytes().splitlines(keepends=True), 1):
            total += 1
            row = json.loads(line)
            if row['analysis_status'] != 'error':
                continue
            provenance = row['provenance']
            assert population['tasks'][row['task_id']] == {k: provenance[k] for k in ('repo', 'base_commit')}
            assert row['analyzer_commit'] == population['analyzer_commit']
            patch = fetch(provenance['patch_location'], args.cache)
            assert sha(patch) == provenance['patch_sha256']
            result = dict(record_file=str(path), record_line=line_number,
                          record_line_sha256=sha(line), record_file_sha256=sha(path.read_bytes()),
                          task_id=row['task_id'], agent=row['agent'], resolved=row['resolved'],
                          analyzer_commit=row['analyzer_commit'], provenance=provenance, files=[])
            for file in parse_patch(patch.decode('utf-8'), language='go'):
                name = file.new if file.new != '/dev/null' else file.old
                if not implementation(name, 'go') or (file.old != '/dev/null' and not implementation(file.old, 'go')):
                    result['files'].append(dict(path=name, excluded='path_scope'))
                    continue
                url = None if file.old == '/dev/null' else (
                    f"https://raw.githubusercontent.com/{provenance['repo']}/{provenance['base_commit']}/{file.old}")
                before = b'' if url is None else fetch(url, args.cache)
                if generated(before.decode('utf-8'), 'go'):
                    result['files'].append(dict(path=name, before_url=url, before_sha256=sha(before), excluded='generated_base'))
                    continue
                offsets = []
                after = apply_patch(before.decode('utf-8'), file, offsets).encode('utf-8')
                result['files'].append(dict(path=name, old_path=file.old, new_path=file.new,
                                           before_url=url, hunk_offsets=offsets,
                                           before=inspect(before, parser, args.parser, args.cache),
                                           after=inspect(after, parser, args.parser, args.cache)))
            failures = [(f['path'], side) for f in result['files'] if 'before' in f
                        for side in ('before', 'after') if not f[side]['tree_sitter_ok']]
            result['first_failure'] = dict(path=failures[0][0], side=failures[0][1])
            invalid = [f['path'] for f in result['files'] if 'after' in f and not f['after']['official_go']['ok']]
            result['classification'] = ('invalid_submitted_syntax' if invalid else
                                        'tree_sitter_eof_semicolon' if row['task_id'].startswith('scriggo-') else
                                        'tree_sitter_new_expression')
            if result['classification'] == 'tree_sitter_eof_semicolon':
                failing = next(f for f in result['files'] if f['path'] == result['first_failure']['path'])
                original = (args.cache / (failing['after']['sha256'] + '.go')).read_bytes()
                result['diagnostic_newline_append'] = inspect(original + b'\n', parser, args.parser, args.cache)
            records.append(result)
    assert total == 3536 and len(records) == 7
    cases = {
        'new_string_expression': 'package p\nvar ptr = new("sample")\n',
        'new_identifier_control': 'package p\nvar ptr = new(string)\n',
        'grouped_const_eof': 'package p\nconst (\n A = iota\n B\n)',
        'grouped_const_newline_control': 'package p\nconst (\n A = iota\n B\n)\n',
        'misplaced_struct_field': 'package p\ntype T struct {}\n Field []string\n',
    }
    experiments = {name: inspect(source.encode(), parser, args.parser, args.cache)
                   for name, source in cases.items()}
    expected = {'new_string_expression': (False, True), 'new_identifier_control': (True, True),
                'grouped_const_eof': (False, True), 'grouped_const_newline_control': (True, True),
                'misplaced_struct_field': (False, False)}
    for name, (ts_ok, go_ok) in expected.items():
        assert experiments[name]['tree_sitter_ok'] == ts_ok
        assert experiments[name]['official_go']['ok'] == go_ok
    assert experiments['grouped_const_eof']['tree_sitter_unlocalized_errors']
    report = dict(schema_version=1, total_records=total, error_records=len(records),
                  parser_versions=versions, records=records, synthetic_experiments=experiments,
                  population_sha256=sha(population_path.read_bytes()),
                  audit_script_sha256=sha(Path(__file__).read_bytes()),
                  official_helper_sha256=sha(Path(__file__).with_name('go-parser-audit.go').read_bytes()),
                  summary=dict(in_scope_file_pairs=sum('before' in f for r in records for f in r['files']),
                               excluded_file_entries=sum('excluded' in f for r in records for f in r['files']),
                               grammar_error_records=sum(r['classification'] != 'invalid_submitted_syntax' for r in records),
                               invalid_syntax_records=sum(r['classification'] == 'invalid_submitted_syntax' for r in records)))
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
