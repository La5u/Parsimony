"""Download and import public SWE-bench submissions.

A local manifest is JSON with explicit fields::

    {"agent": "my-agent", "submission_url": "https://...",
     "prediction_url": "https://.../all_preds.jsonl",
     "results_url": "https://.../results.json", "ref": "main"}

``prediction_url`` and ``results_url`` may also be local paths.  The returned
mapping always contains ``agent``, ``submission_url``, ``predictions``,
``resolved``, ``evaluated`` and ``provenance``.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import urlparse
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class Cache:
    """Small URL -> bytes cache. Files are named by SHA256(URL)."""
    def __init__(self, cache_dir: str | os.PathLike[str], timeout: float = 30.0):
        self.cache_dir = Path(cache_dir)
        self.timeout = timeout
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, url: str) -> bytes:
        name = hashlib.sha256(url.encode("utf-8")).hexdigest()
        target = self.cache_dir / name
        try:
            return target.read_bytes()
        except FileNotFoundError:
            pass
        request = Request(url, headers={"User-Agent": "parsimony-artifacts/1"})
        with urlopen(request, timeout=self.timeout) as response:
            data = response.read()
        # A named temporary file plus replace prevents partial cache entries.
        fd, tmp = tempfile.mkstemp(prefix=name + ".", dir=self.cache_dir)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp, target)
        finally:
            try:
                os.unlink(tmp)
            except FileNotFoundError:
                pass
        return data


def _bytes(source: str, cache: Cache) -> bytes:
    if urlparse(source).scheme in {"http", "https"}:
        return cache.get(source)
    return Path(source).read_bytes()


def _json(source: str, cache: Cache) -> Any:
    return json.loads(_bytes(source, cache).decode("utf-8"))


def _github_parts(url: str) -> tuple[str, str, str] | None:
    p = urlparse(url)
    if p.netloc not in {"github.com", "www.github.com"}:
        return None
    bits = p.path.strip("/").split("/")
    if len(bits) < 4 or bits[2] != "tree":
        return None
    return bits[0] + "/" + bits[1], bits[3], "/".join(bits[4:])


def _urls(submission: str, ref: str) -> tuple[str, str, str, str, str]:
    """Return agent hint, prediction URL, result URL, provenance base."""
    gh = _github_parts(submission)
    if gh:
        repo, actual_ref, path = gh
        ref = actual_ref
        base = f"https://raw.githubusercontent.com/{repo}/{ref}/{path}".rstrip("/")
        # The experiments repository publishes predictions in S3 while its
        # results and metadata remain in GitHub.
        if repo.lower() == "swe-bench/experiments" and path.startswith("evaluation/"):
            s3 = "https://swe-bench-submissions.s3.amazonaws.com/" + path.split("evaluation/", 1)[1]
            pred = s3 + "/all_preds.jsonl"
        else:
            pred = base + "/all_preds.jsonl"
        return path.rstrip('/').split('/')[-1], pred, base + "/results/results.json", submission, ref
    name = submission.rstrip("/").split("/")[-1]
    prefix = f"verified/{name}"
    return name, f"https://swe-bench-submissions.s3.amazonaws.com/{prefix}/all_preds.jsonl", \
        f"https://raw.githubusercontent.com/SWE-bench/experiments/{ref}/evaluation/verified/{name}/results/results.json", \
        f"https://github.com/SWE-bench/experiments/tree/{ref}/evaluation/verified/{name}", ref


def _parse_predictions(data: bytes) -> tuple[str, dict[str, str]]:
    agent = ""
    predictions: dict[str, str] = {}
    for line_no, line in enumerate(data.decode("utf-8-sig").splitlines(), 1):
        if not line.strip():
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid prediction JSON on line {line_no}") from exc
        if not isinstance(item, dict) or not item.get("instance_id"):
            raise ValueError(f"prediction line {line_no} lacks instance_id")
        # SWE-bench's public exporter has used both names over time.
        patch = item.get("patch", item.get("model_patch"))
        if not isinstance(patch, str):
            raise ValueError(f"prediction {item['instance_id']} lacks string patch")
        if str(item['instance_id']) in predictions:
            raise ValueError(f"duplicate prediction: {item['instance_id']}")
        predictions[str(item["instance_id"])] = patch
        agent = agent or str(item.get("model_name_or_path") or item.get("agent") or "")
    return agent, predictions


def _result_sets(result: Any) -> tuple[set[str], set[str] | None]:
    if not isinstance(result, dict) or not isinstance(result.get("resolved"), list):
        raise ValueError("results JSON must contain a resolved list")
    resolved = {str(x) for x in result["resolved"]}
    evaluated: set[str] = set(resolved)
    found = False
    for key in ("no_generation", "no_logs", "unresolved", "failed", "not_resolved"):
        values = result.get(key)
        if isinstance(values, list):
            found = True
            evaluated.update(str(x) for x in values)
    # A results file containing only resolved cannot tell us what was run.
    return resolved, (evaluated if found else None)


def _load(agent: str, submission_url: str, prediction_url: str, results_url: str,
          cache: Cache, ref: str) -> dict[str, Any]:
    prediction_bytes = _bytes(prediction_url, cache)
    result_bytes = _bytes(results_url, cache)
    pred_agent, predictions = _parse_predictions(prediction_bytes)
    result = json.loads(result_bytes)
    resolved, evaluated = _result_sets(result)
    return {"agent": agent or pred_agent or "unknown", "submission_url": submission_url,
            "predictions": predictions, "resolved": resolved, "evaluated": evaluated,
            "result_details": result,
            "provenance": {"prediction_url": prediction_url, "results_url": results_url,
                           "prediction_sha256": hashlib.sha256(prediction_bytes).hexdigest(),
                           "results_sha256": hashlib.sha256(result_bytes).hexdigest(),
                           "reported_model": pred_agent,
                           "submission_url": submission_url, "ref": ref}}


def _new_submission(agent: str, submission_url: str, base: str, ref: str,
                    cache: Cache, task_ids: list[str] | None,
                    limit: int | None, include_failed: bool = False) -> dict[str, Any]:
    """Read the per-instance layout used by recent mini-SWE-agent runs."""
    metadata_url = base + "/metadata.yaml"
    result_url = base + "/per_instance_details.json"
    metadata_bytes = _bytes(metadata_url, cache)
    # Deliberately do not add a YAML dependency: this is the one scalar asset
    # needed from the public metadata file.
    match = re.search(rb"(?m)^\s*logs:\s*(s3://[^\s#]+)\s*$", metadata_bytes)
    if match:
        logs_uri = match.group(1).decode('utf-8')
    else:
        # Some current submissions publish logs: null even though per-task
        # patches/reports exist beside the documented trajs prefix in S3.
        match = re.search(rb'(?m)^\s*trajs:\s*(s3://[^\s#]+/trajs)/?\s*$', metadata_bytes)
        if not match:
            raise ValueError('metadata.yaml lacks supported assets.logs/trajs entries')
        logs_uri = match.group(1).decode('utf-8').removesuffix('/trajs') + '/logs'
    parsed = urlparse(logs_uri)
    if parsed.scheme != "s3" or parsed.netloc != "swe-bench-submissions" or not parsed.path.strip("/"):
        raise ValueError("metadata assets.logs is not an official SWE-bench S3 location")
    logs_url = "https://swe-bench-submissions.s3.amazonaws.com/" + parsed.path.lstrip("/").rstrip("/")

    result_bytes = _bytes(result_url, cache)
    raw_details = json.loads(result_bytes.decode("utf-8"))
    if not isinstance(raw_details, dict):
        raise ValueError("per_instance_details.json must be an object")
    resolved: set[str] = set()
    unresolved: set[str] = set()
    no_logs: set[str] = set()
    no_generation: set[str] = set()
    for task, detail in raw_details.items():
        if not isinstance(detail, dict) or type(detail.get("resolved")) is not bool:
            raise ValueError(f"invalid resolved boolean for {task}")
        task = str(task)
        categories = {str(value).lower() for key, value in detail.items()
                      if key in {"category", "result", "status", "failure_category"}}
        if detail["resolved"]:
            resolved.add(task)
        elif "no_logs" in categories:
            no_logs.add(task)
        elif categories & {'no_generation', 'no_submission'}:
            no_generation.add(task)
        else:
            # A per-instance record with resolved=false is an explicit failure.
            unresolved.add(task)

    evaluated = resolved | unresolved | no_logs | no_generation
    candidates = resolved | (unresolved if include_failed else set())
    wanted = candidates if task_ids is None else (candidates & {str(x) for x in task_ids})
    selected = sorted(wanted)
    if limit is not None:
        selected = selected[:limit]
    predictions: dict[str, str] = {}
    locations = {task: logs_url + '/' + task + '/patch.diff' for task in evaluated}
    missing: set[str] = set()
    for task in selected:
        location = logs_url + "/" + task + "/patch.diff"
        try:
            patch = _bytes(location, cache)
        except HTTPError as exc:
            if exc.code == 404:
                exc.close()
                missing.add(task)
                continue
            raise
        predictions[task] = patch.decode("utf-8")
        locations[task] = location

    normalized = {"resolved": sorted(resolved), "unresolved": sorted(unresolved),
                  "no_logs": sorted(no_logs), "no_generation": sorted(no_generation),
                  "missing_patch": sorted(missing)}
    return {"agent": agent or "unknown", "submission_url": submission_url,
            "predictions": predictions, "prediction_locations": locations,
            "resolved": resolved, "evaluated": evaluated, "result_details": normalized,
            "provenance": {"prediction_url": logs_url, "results_url": result_url,
                           "metadata_url": metadata_url,
                           "prediction_sha256": None,
                           "results_sha256": hashlib.sha256(result_bytes).hexdigest(),
                           "metadata_sha256": hashlib.sha256(metadata_bytes).hexdigest(),
                           "reported_model": "", "submission_url": submission_url,
                           "ref": ref, "layout": "mini-swe-agent-per-instance-v1"}}


def _legacy_failures(submission: dict[str, Any], cache: Cache, task_ids: list[str] | None) -> dict[str, Any]:
    """Add explicit failures from per-task ``logs/<task>/report.json`` files.

    Legacy ``results.json`` files list only resolved/no_generation/no_logs, so
    absence from ``resolved`` is not evidence of an evaluated failure. The
    per-task evaluation report is: only ``resolved: false`` with an applied
    patch becomes ``unresolved``; a missing report stays unknown.
    """
    details = submission["result_details"]
    if any(isinstance(details.get(key), list) for key in ("unresolved", "failed", "not_resolved")):
        return submission
    prediction_url = submission["provenance"]["prediction_url"]
    if not prediction_url.startswith("https://swe-bench-submissions.s3.amazonaws.com/"):
        return submission
    logs = prediction_url.rsplit("/", 1)[0] + "/logs"
    listed = set(submission["resolved"])
    for key in ("no_generation", "no_logs"):
        listed.update(str(x) for x in details.get(key) or [])
    candidates = sorted(set(submission["predictions"]) - listed)
    if task_ids is not None:
        candidates = [t for t in candidates if t in set(task_ids)]
    unresolved, unreported = [], []
    for task in candidates:
        try:
            report = json.loads(_bytes(f"{logs}/{task}/report.json", cache).decode("utf-8")).get(task)
        except HTTPError as exc:
            if exc.code != 404:
                raise
            exc.close()
            unreported.append(task)
            continue
        if not isinstance(report, dict) or type(report.get("resolved")) is not bool:
            raise ValueError(f"invalid evaluation report for {task}")
        if report["resolved"]:
            raise ValueError(f"report marks {task} resolved but results.json does not")
        if report.get("patch_exists", True) and report.get("patch_successfully_applied", True):
            unresolved.append(task)
        else:
            unreported.append(task)
    details = dict(details, unresolved=unresolved, no_report=unreported)
    evaluated = (submission["evaluated"] or set(submission["resolved"])) | set(unresolved)
    provenance = dict(submission["provenance"], failure_reports=logs + "/<task>/report.json")
    return dict(submission, result_details=details, evaluated=evaluated, provenance=provenance)


def load_submission(submission: str, cache: Cache, ref: str = "main",
                    task_ids: list[str] | None = None,
                    limit: int | None = None, include_failed: bool = False) -> dict[str, Any]:
    """Load a submission, supporting both monolithic and current layouts."""
    agent, prediction, results, origin, resolved_ref = _urls(submission, ref)
    try:
        # The monolithic layout downloads every prediction at once; selection
        # only limits which failure reports are fetched (with include_failed).
        loaded = _load(agent, origin, prediction, results, cache, resolved_ref)
    except HTTPError as exc:
        if exc.code != 404:
            raise
        exc.close()
        gh = _github_parts(origin)
        if not gh:
            raise
        repo, actual_ref, path = gh
        base = f"https://raw.githubusercontent.com/{repo}/{actual_ref}/{path}".rstrip("/")
        return _new_submission(agent, origin, base, actual_ref, cache, task_ids, limit,
                               include_failed=include_failed)
    return _legacy_failures(loaded, cache, task_ids) if include_failed else loaded


def load_manifest(path: str | os.PathLike[str], cache: Cache) -> dict[str, Any]:
    """Load the explicit JSON manifest format described in this module."""
    manifest = json.loads(Path(path).read_text(encoding="utf-8"))
    required = ("prediction_url", "results_url")
    missing = [key for key in required if not isinstance(manifest.get(key), str)]
    if missing:
        raise ValueError("manifest requires string fields: " + ", ".join(missing))
    ref = str(manifest.get("ref", "main"))
    submission = str(manifest.get("submission_url", path))
    def source(key):
        value = manifest[key]
        return value if urlparse(value).scheme in {'http', 'https'} else str(Path(path).resolve().parent / value)
    return _load(str(manifest.get("agent", "")), submission,
                 source("prediction_url"), source("results_url"), cache, ref)


__all__ = ["Cache", "load_submission", "load_manifest"]
