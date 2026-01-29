#!/usr/bin/env python3
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_COLLECTION = "all-prompts"
DEFAULT_HISTORY_COLLECTION = "all-prompts-history"
DEFAULT_FIRST_PARTY_COLLECTION = "first-party"
DEFAULT_MODE = "query"
DEFAULT_LIMIT = 8
DEFAULT_MIN_SCORE = 0.0

SOURCE_ALIASES = {
    "research": "research--ai_prompts",
    "ai_prompts": "research--ai_prompts",
}


def qmd_binary():
    qmd = shutil.which("qmd")
    if not qmd:
        print(
            "qmd not found. Install with: bun install -g https://github.com/tobi/qmd",
            file=sys.stderr,
        )
        return None
    return qmd


def collection_exists(name):
    config_path = Path.home() / ".config" / "qmd" / "index.yml"
    if not config_path.exists():
        return False
    try:
        content = config_path.read_text(encoding="utf-8")
    except OSError:
        return False
    pattern = rf"(?m)^\s*{re.escape(name)}\s*:"
    return re.search(pattern, content) is not None


def ensure_uv():
    if os.environ.get("UV") or os.environ.get("UV_RUN_RECURSION_DEPTH"):
        return
    raise RuntimeError("Run with uv: uv run python scripts/qmd_query.py")


def run_qmd(qmd, mode, query, collection, limit, min_score, full):
    cmd = [
        qmd,
        mode,
        query,
        "-c",
        collection,
        "--json",
        "-n",
        str(limit),
        "--min-score",
        str(min_score),
    ]
    if full:
        cmd.append("--full")
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        raise RuntimeError(stderr or stdout or "qmd query failed")
    payload = result.stdout.strip()
    if not payload:
        return []

    json_start = None
    for token in ("[", "{"):
        idx = payload.find(token)
        if idx != -1:
            json_start = idx if json_start is None else min(json_start, idx)
    if json_start is None:
        if "no results" in payload.lower():
            return []
        raise RuntimeError("qmd did not return JSON output")

    json_end = None
    for token in ("]", "}"):
        idx = payload.rfind(token)
        if idx != -1:
            json_end = idx if json_end is None else max(json_end, idx)
    if json_end is None or json_end < json_start:
        raise RuntimeError("qmd did not return JSON output")

    json_payload = payload[json_start:json_end + 1]
    try:
        return json.loads(json_payload)
    except json.JSONDecodeError:
        raise RuntimeError("Failed to parse qmd JSON output") from None


def normalize_path(path):
    return path.replace("\\", "/")


def dedupe_results(results):
    by_key = {}

    for result in results:
        raw_path = normalize_path(result.get("file", ""))
        path = raw_path
        if path.startswith("qmd://"):
            parts = path.split("/", 3)
            if len(parts) == 4:
                path = parts[3]

        history_match = re.search(r"/history/\d{8}-\d{6}/", path)
        if history_match:
            path = path.replace(history_match.group(0), "/")

        key = path
        current_best = by_key.get(key)
        if not current_best:
            by_key[key] = result
            continue

        is_history = "/history/" in raw_path
        best_is_history = "/history/" in normalize_path(current_best.get("file", ""))
        if best_is_history and not is_history:
            by_key[key] = result
            continue
        if is_history == best_is_history:
            if result.get("score", 0) > current_best.get("score", 0):
                by_key[key] = result

    return list(by_key.values())


def normalize_list(values):
    if not values:
        return []
    items = []
    for value in values:
        for part in value.split(","):
            part = part.strip()
            if part:
                items.append(part)
    return items


def normalize_name(name):
    return name.replace("_", "-").lower()


def resolve_by_normalized_path(base, rel_path):
    current = base
    for part in [p for p in rel_path.split("/") if p]:
        candidate = current / part
        if candidate.exists():
            current = candidate
            continue

        if not current.exists() or not current.is_dir():
            return candidate

        norm_target = normalize_name(part)
        matches = [entry for entry in current.iterdir() if normalize_name(entry.name) == norm_target]
        if len(matches) == 1:
            current = matches[0]
            continue
        if matches:
            matches.sort(key=lambda p: p.name)
            current = matches[0]
            continue

        current = candidate
    return current


def resolve_qmd_display_path(qmd_path, repo_root):
    parts = qmd_path.split("/", 3)
    if len(parts) < 4:
        return repo_root / qmd_path
    rel_path = parts[3]
    return resolve_by_normalized_path(repo_root, rel_path)


def resolve_file_path(display_path, repo_root):
    normalized = normalize_path(display_path)
    if normalized.startswith("qmd://"):
        return resolve_qmd_display_path(normalized, repo_root)
    if normalized.startswith("/"):
        return Path(normalized)
    prefix = f"{repo_root.name}/"
    if normalized.startswith(prefix):
        normalized = normalized[len(prefix):]
    return resolve_by_normalized_path(repo_root, normalized)


def parse_frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    fm_lines = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)

    data = {}
    current_key = None
    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", stripped)
        if match:
            key = match.group(1)
            raw_value = match.group(2).strip()
            current_key = None
            if raw_value == "":
                data[key] = []
                current_key = key
            elif raw_value.startswith("[") and raw_value.endswith("]"):
                inner = raw_value[1:-1].strip()
                if inner:
                    parts = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
                    data[key] = parts
                else:
                    data[key] = []
            else:
                data[key] = raw_value.strip("\"'")
            continue

        if stripped.startswith("-") and current_key:
            value = stripped.lstrip("-").strip().strip("\"'")
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(value)
            continue

    return data


def load_frontmatter(file_path):
    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except OSError:
        return {}
    return parse_frontmatter(content)


def filter_results(results, args, repo_root):
    sources = [SOURCE_ALIASES.get(s, s) for s in normalize_list(args.source)]
    types = normalize_list(args.type)
    stages = normalize_list(args.workflow_stage)
    tags = normalize_list(args.tags)

    needs_frontmatter = bool(stages or tags)
    filtered = []

    for result in results:
        path = normalize_path(result.get("file", ""))

        if not args.include_history and "/history/" in path:
            continue

        if sources:
            if not any(
                f"/3rd_party/{source}/" in path or f"/3rd-party/{source}/" in path
                for source in sources
            ):
                continue

        if types:
            has_agents = "/agents/" in path
            has_commands = "/commands/" in path
            match_type = False
            for t in types:
                if t == "agent" and has_agents:
                    match_type = True
                elif t == "command" and has_commands:
                    match_type = True
                elif t == "prompt" and not has_agents and not has_commands:
                    match_type = True
            if not match_type:
                continue

        if needs_frontmatter:
            file_path = resolve_file_path(path, repo_root)
            fm = load_frontmatter(file_path)
            if stages:
                if fm.get("workflow_stage") not in stages:
                    continue
            if tags:
                fm_tags = fm.get("tags") or []
                if isinstance(fm_tags, str):
                    fm_tags = [fm_tags]
                if not any(tag in fm_tags for tag in tags):
                    continue

        filtered.append(result)

    return filtered


def output_json(results):
    print(json.dumps(results, indent=2))


def output_md(results):
    for result in results:
        title = result.get("title") or result.get("file")
        print(f"---\n# {title}\n")
        print(f"file: {result.get('file')}")
        print(f"docid: {result.get('docid')}")
        print(f"score: {result.get('score')}")
        snippet = result.get("snippet")
        if snippet:
            print("\n" + snippet + "\n")


def output_bundle(results):
    for index, result in enumerate(results, start=1):
        title = result.get("title") or result.get("file")
        body = result.get("body") or result.get("snippet") or ""
        print(f"### {index}. {title}")
        print(f"source: {result.get('file')} | docid: {result.get('docid')} | score: {result.get('score')}")
        print("")
        print(body.rstrip())
        print("\n---\n")


def main():
    parser = argparse.ArgumentParser(description="Query QMD collections with optional filtering")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--collection", default=DEFAULT_COLLECTION)
    parser.add_argument("--history-collection", default=DEFAULT_HISTORY_COLLECTION)
    parser.add_argument("--first-party-collection", default=DEFAULT_FIRST_PARTY_COLLECTION)
    parser.add_argument("--include-history", action="store_true")
    parser.add_argument("--skip-first-party", action="store_true")
    parser.add_argument("--mode", choices=["search", "vsearch", "query"], default=DEFAULT_MODE)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    parser.add_argument("--min-score", type=float, default=DEFAULT_MIN_SCORE)
    parser.add_argument("--format", choices=["json", "md", "bundle"], default="json")
    parser.add_argument("--full", action="store_true", help="Return full document bodies")
    parser.add_argument("--source", action="append", help="Filter by source (repeatable or comma-separated)")
    parser.add_argument("--type", action="append", help="Filter by type: agent, command, prompt")
    parser.add_argument("--workflow-stage", action="append", help="Filter by workflow_stage")
    parser.add_argument("--tags", action="append", help="Filter by tags")
    args = parser.parse_args()

    try:
        ensure_uv()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    qmd = qmd_binary()
    if not qmd:
        return 2

    repo_root = Path(__file__).resolve().parents[1]
    full = args.full or args.format == "bundle"

    try:
        results = run_qmd(
            qmd,
            args.mode,
            args.query,
            args.collection,
            args.limit,
            args.min_score,
            full,
        )
        if args.include_history:
            history_results = run_qmd(
                qmd,
                args.mode,
                args.query,
                args.history_collection,
                args.limit,
                args.min_score,
                full,
            )
            results.extend(history_results)
        if not args.skip_first_party and args.first_party_collection != args.collection:
            if collection_exists(args.first_party_collection):
                first_party_results = run_qmd(
                    qmd,
                    args.mode,
                    args.query,
                    args.first_party_collection,
                    args.limit,
                    args.min_score,
                    full,
                )
                results.extend(first_party_results)
            else:
                print(
                    "First-party collection not found. Run: uv run python scripts/qmd_setup.py",
                    file=sys.stderr,
                )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    filtered = filter_results(results, args, repo_root)
    if args.include_history or not args.skip_first_party:
        filtered = dedupe_results(filtered)
    filtered.sort(key=lambda r: r.get("score", 0), reverse=True)
    filtered = filtered[: args.limit]

    if not filtered:
        print("No results")
        return 0

    if args.format == "md":
        output_md(filtered)
    elif args.format == "bundle":
        output_bundle(filtered)
    else:
        output_json(filtered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
