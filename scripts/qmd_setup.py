#!/usr/bin/env python3
import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_COLLECTION = "all-prompts"
DEFAULT_PATTERN = "3rd_party/*/viscera/**/*.md"
FIRST_PARTY_COLLECTION = "first-party"
FIRST_PARTY_PATTERN = "1st_party/**/*.md"
HISTORY_COLLECTION = "all-prompts-history"
HISTORY_PATTERN = "3rd_party/*/history/**/*.md"

CONTEXTS = {
    "/": "Current prompt library across external sources.",
    "/3rd_party/humanlayer/viscera/commands": "Claude commands",
    "/3rd_party/humanlayer/viscera/agents": "Claude agents",
    "/3rd_party/joelhooks/viscera": "OpenCode agents",
    "/3rd_party/research--ai_prompts/viscera": "Prompting techniques",
}

FIRST_PARTY_CONTEXTS = {
    "/": "First-party docs and guidance",
}

HISTORY_CONTEXTS = {
    "/": "Historical prompt snapshots (opt-in)."
}


def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        raise RuntimeError(stderr or stdout or "command failed")
    return result.stdout.strip()


def ensure_uv():
    if os.environ.get("UV") or os.environ.get("UV_RUN_RECURSION_DEPTH"):
        return
    raise RuntimeError("Run with uv: uv run python scripts/qmd_setup.py")


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


def add_collection(qmd, name, repo_root, pattern):
    if collection_exists(name):
        print(f"Collection already exists: {name}")
        return
    run([qmd, "collection", "add", str(repo_root), "--name", name, "--mask", pattern])
    print(f"Added collection: {name}")


def add_contexts(qmd, name, context_map):
    for path_prefix, text in context_map.items():
        if path_prefix == "/":
            target = f"qmd://{name}"
        else:
            target = f"qmd://{name}{path_prefix}"
        run([qmd, "context", "add", target, text])


def main():
    parser = argparse.ArgumentParser(description="Set up QMD collections for main_repo")
    parser.add_argument(
        "--path",
        help="Path to main_repo (defaults to repo root)",
    )
    parser.add_argument(
        "--collection",
        default=DEFAULT_COLLECTION,
        help=f"Collection name (default: {DEFAULT_COLLECTION})",
    )
    parser.add_argument(
        "--pattern",
        default=DEFAULT_PATTERN,
        help=f"Glob pattern (default: {DEFAULT_PATTERN})",
    )
    parser.add_argument(
        "--history-collection",
        default=HISTORY_COLLECTION,
        help=f"History collection name (default: {HISTORY_COLLECTION})",
    )
    parser.add_argument(
        "--history-pattern",
        default=HISTORY_PATTERN,
        help=f"History glob pattern (default: {HISTORY_PATTERN})",
    )
    parser.add_argument(
        "--first-party-collection",
        default=FIRST_PARTY_COLLECTION,
        help=f"First-party collection name (default: {FIRST_PARTY_COLLECTION})",
    )
    parser.add_argument(
        "--first-party-pattern",
        default=FIRST_PARTY_PATTERN,
        help=f"First-party glob pattern (default: {FIRST_PARTY_PATTERN})",
    )
    parser.add_argument(
        "--skip-first-party",
        action="store_true",
        help="Skip creating the first-party collection",
    )
    parser.add_argument(
        "--skip-history",
        action="store_true",
        help="Skip creating the history collection",
    )
    args = parser.parse_args()

    try:
        ensure_uv()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    repo_root = Path(args.path).expanduser().resolve() if args.path else Path(__file__).resolve().parents[1]
    qmd = qmd_binary()
    if not qmd:
        return 2

    try:
        add_collection(qmd, args.collection, repo_root, args.pattern)
        add_contexts(qmd, args.collection, CONTEXTS)

        if not args.skip_first_party:
            add_collection(qmd, args.first_party_collection, repo_root, args.first_party_pattern)
            add_contexts(qmd, args.first_party_collection, FIRST_PARTY_CONTEXTS)

        if not args.skip_history:
            add_collection(qmd, args.history_collection, repo_root, args.history_pattern)
            add_contexts(qmd, args.history_collection, HISTORY_CONTEXTS)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print("\nNext steps:")
    print("- qmd update")
    print("- qmd embed   # optional, enables semantic search")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
