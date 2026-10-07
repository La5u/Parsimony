#!/usr/bin/env python3
"""NONPUBLISHED standalone fresh-code pilot; never executes submissions.

Usage: --export MODEL=Scenario.codegeneration_1_0.2_eval_all.json=/local/export
(repeat up to six times) --output-dir /external/new-directory
Source filenames disclose upstream configuration, not a verified runtime config.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import warnings

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from urllib.parse import quote

from parsimony.analysis import unit_lines, without_docstrings
from parsimony import benchmark

POPULATION_MANIFEST = ROOT / 'examples/livecodebench-pilot/population.json'
MAX_BYTES = 120_000_000
MAX_TASKS = 1055
POLICY = 'index 0 fixed before inspecting outcomes; no best-of selection'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def membership_hash(ids):
    return digest(json.dumps(sorted(ids), ensure_ascii=True, separators=(',', ':')).encode())


def load_manifest():
    raw = POPULATION_MANIFEST.read_bytes()
    manifest = json.loads(raw)
    ids = manifest.get('task_ids')
    if (not isinstance(ids, list) or not ids
            or any(not isinstance(qid, str) or not qid for qid in ids)
            or len(set(ids)) != len(ids)
            or type(manifest.get('population_size')) is not int
            or len(ids) != manifest['population_size']
            or membership_hash(ids) != manifest.get('membership_sha256')):
        raise ValueError('invalid frozen population manifest')
    return manifest, digest(raw)


def load_export(path, num_samples):
    path = Path(path)
    if path.stat().st_size > MAX_BYTES:
        raise ValueError('export exceeds byte bound')
    raw = path.read_bytes()
    records = json.loads(raw)
    if not isinstance(records, list) or not 0 < len(records) <= MAX_TASKS:
        raise ValueError('expected 1..1055 task records')
    seen = set()
    for record in records:
        if not isinstance(record, dict):
            raise ValueError('task must be an object')
        qid = record.get('question_id')
        if not isinstance(qid, str) or not qid or qid in seen:
            raise ValueError('missing or duplicate question_id')
        seen.add(qid)
        codes, grades = record.get('code_list'), record.get('graded_list')
        if (not isinstance(codes, list) or not isinstance(grades, list)
                or len(codes) != num_samples or len(grades) != num_samples
                or any(not isinstance(c, str) for c in codes)
                or any(type(g) is not bool for g in grades)):
            raise ValueError('code_list/graded_list must match declared samples and contain strings/bools')
        try:
            for code in codes:
                code.encode('utf-8')
        except UnicodeEncodeError as exc:
            raise ValueError('invalid Unicode code') from exc
    return records, digest(raw)


def measure(records):
    rows = []
    for record in sorted(records, key=lambda r: r['question_id']):
        code = record['code_list'][0]
        row = dict(question_id=record['question_id'], attempt_index=0,
                   upstream_solved=record['graded_list'][0], code_sha256=digest(code.encode()),
                   status='missing_code', units_added=None, units_deleted=None, net_units=None)
        if code.strip():
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    tree = ast.parse(code)
                count = sum(len(run) for run in unit_lines(without_docstrings(tree)))
                row.update(status='measured', units_added=count, units_deleted=0, net_units=count)
            except (SyntaxError, ValueError, RecursionError):
                row['status'] = 'parse_error'
        rows.append(row)
    return rows


def summarize(rows):
    measured = [r['net_units'] for r in rows if r['status'] == 'measured']
    solved = [r['net_units'] for r in rows if r['status'] == 'measured' and r['upstream_solved']]
    return dict(full_population=len(rows), upstream_solved=sum(r['upstream_solved'] for r in rows),
                upstream_solved_fraction=sum(r['upstream_solved'] for r in rows) / len(rows),
                measured_population=len(measured), solved_measured_population=len(solved),
                mean_measured_all_outcomes=sum(measured) / len(measured) if measured else None,
                mean_measured_solved_only=sum(solved) / len(solved) if solved else None,
                missing_code=sum(r['status'] == 'missing_code' for r in rows),
                parse_errors=sum(r['status'] == 'parse_error' for r in rows))


def analyzer_identity():
    if sys.version_info[:3] != (3, 14, 7):
        raise ValueError('measurement requires Python 3.14.7')
    def git(*args):
        return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()
    if git('status', '--porcelain', '--untracked-files=no'):
        raise ValueError('tracked analyzer checkout is dirty')
    script = Path(__file__).resolve()
    for label, path in (('pilot script', script), ('population manifest', POPULATION_MANIFEST)):
        relative = path.relative_to(ROOT).as_posix()
        try:
            git('ls-files', '--error-unmatch', '--', relative)
            committed = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'HEAD:{relative}'])
        except subprocess.CalledProcessError as exc:
            raise ValueError(f'{label} must be git tracked and present in HEAD') from exc
        if committed != path.read_bytes():
            raise ValueError(f'{label} must be byte-equal to HEAD')
    commit, source_hash = benchmark.analyzer_identity()
    if commit != git('rev-parse', 'HEAD'):
        raise ValueError('analyzer identity must match clean HEAD')
    return dict(commit=commit, tracked_checkout_clean=True,
                python=sys.version.split()[0], source_sha256=source_hash,
                script_sha256=digest(script.read_bytes()),
                unit_definition='sum(len(run) for run in unit_lines(without_docstrings(ast.parse(code))))')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export', action='append', required=True, metavar='MODEL=SOURCE_FILENAME=LOCAL_PATH')
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--source-revision', required=True)

    args = parser.parse_args(argv)
    try:
        if not re.fullmatch(r'[0-9a-fA-F]{40}', args.source_revision):
            raise ValueError('source revision must be a 40hex commit')
        revision = args.source_revision.lower()
        output = args.output_dir.resolve()
        if output == ROOT or ROOT in output.parents:
            raise ValueError('output directory must be external to checkout')
        identity = analyzer_identity()
        manifest, manifest_hash = load_manifest()
        if manifest.get('revision') != revision:
            raise ValueError('source revision must match frozen manifest')
        if not 1 <= len(args.export) <= 6:
            raise ValueError('pilot accepts at most six models')
        prepared, models = [], set()
        for spec in args.export:
            model, filename, local = spec.split('=', 2)
            if not re.fullmatch(r'[A-Za-z0-9_.()-]+', model) or model in models:
                raise ValueError('invalid or duplicate model name')
            models.add(model)
            match = re.fullmatch(r'Scenario\.codegeneration_(\d+)_(\d+(?:\.\d+)?)_eval_all\.json', filename)
            if not match or not 1 <= int(match[1]) <= 10:
                raise ValueError('invalid source configuration filename')
            samples, temperature = int(match[1]), float(match[2])
            bindings = [binding for binding in manifest['source_bindings']
                        if binding['model'] == model and binding['filename'] == filename]
            if len(bindings) != 1:
                raise ValueError('model and filename must have a frozen source binding')
            records, artifact_hash = load_export(local, samples)
            if artifact_hash != bindings[0]['sha256']:
                raise ValueError('artifact SHA256 must match frozen source binding')
            membership = membership_hash(r['question_id'] for r in records)
            if (len(records) != manifest['population_size']
                    or membership != manifest['membership_sha256']
                    or set(r['question_id'] for r in records) != set(manifest['task_ids'])):
                raise ValueError('records must match full frozen task population')
            rows = measure(records)
            metadata = dict(publication_status='NONPUBLISHED', track='standalone complete-file Python footprint',
                            measurement_scope='complete file; not repository scope',
                            source_revision=revision,
                            source_url=f'https://raw.githubusercontent.com/LiveCodeBench/submissions/{revision}/{quote(model, safe="")}/{quote(filename, safe="")}',
                            not_published_swe_patch_analyzer=True, target_code_executed=False,
                            model=model, source_reported_model=model, source_config_filename=filename,
                            source_reported_num_samples=samples, source_reported_temperature=temperature,
                            configuration_evidence='filename only; not independently verified',
                            population_manifest_sha256=manifest_hash,
                            input_artifact_sha256=artifact_hash, full_task_membership_sha256=membership,
                            attempt_policy=POLICY, analyzer_identity=identity, summary=summarize(rows))
            row_bytes = ''.join(json.dumps(row, sort_keys=True) + '\n' for row in rows).encode()
            metadata['rows_sha256'] = digest(row_bytes)
            prepared.append((model, row_bytes, metadata))
        output.mkdir(parents=True, exist_ok=False)
        for model, row_bytes, metadata in prepared:
            (output / f'{model}.rows.jsonl').write_bytes(row_bytes)
            (output / f'{model}.metadata.json').write_text(json.dumps(metadata, indent=2, sort_keys=True) + '\n')
        (output / 'summary.json').write_text(json.dumps({m: meta['summary'] for m, _, meta in prepared}, indent=2) + '\n')
    except (ValueError, OSError) as exc:
        parser.error(str(exc))


if __name__ == '__main__':
    main()
