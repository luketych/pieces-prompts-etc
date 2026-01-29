#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if result.returncode != 0:
        stderr = result.stderr.strip()
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{stderr}")
    return result.stdout.strip()


def require_uv():
    uv_path = shutil.which("uv")
    if not uv_path:
        raise RuntimeError("uv not found. Install uv to run this script.")
    return uv_path


def ensure_uv_env():
    if os.environ.get("UV") or os.environ.get("UV_RUN_RECURSION_DEPTH"):
        return
    raise RuntimeError("Run with uv: uv run python tests/e2e/run_3rd_party_e2e.py")


def ensure_repo(repo_path):
    git_dir = repo_path / ".git"
    if not git_dir.exists():
        run(["git", "init", "-b", "main"], cwd=repo_path)

    try:
        run(["git", "rev-parse", "--verify", "HEAD"], cwd=repo_path)
        return
    except RuntimeError:
        pass

    files = [
        "README.md",
        "prompts/alpha.md",
        "prompts/beta.md",
        "assets/config.json",
    ]
    run(["git", "add", *files], cwd=repo_path)
    run(["git", "commit", "-m", "Initial prompts"], cwd=repo_path)


def mutate_repo(repo_path):
    prompt_path = repo_path / "prompts/alpha.md"
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
    content = prompt_path.read_text(encoding="utf-8")
    content += f"\n\nUpdate: {timestamp}\n"
    prompt_path.write_text(content, encoding="utf-8")
    run(["git", "add", "prompts/alpha.md"], cwd=repo_path)
    run(["git", "commit", "-m", "Update alpha prompt"], cwd=repo_path)


def list_history(history_path):
    if not history_path.exists():
        return []
    snapshots = [entry.name for entry in history_path.iterdir() if entry.is_dir()]
    snapshots.sort()
    return snapshots


def run_update(repo_root, manifest_path, entry_id):
    uv_path = require_uv()
    cmd = [
        uv_path,
        "run",
        "python",
        str(repo_root / "scripts" / "update_3rd_party.py"),
        "--manifest",
        str(manifest_path),
        "--only",
        entry_id,
    ]
    result = subprocess.run(cmd, cwd=repo_root, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def main():
    parser = argparse.ArgumentParser(description="Run local 3rd-party update e2e")
    parser.add_argument(
        "--mutate",
        action="store_true",
        help="Modify a prompt and run a second update",
    )
    args = parser.parse_args()

    try:
        ensure_uv_env()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parents[2]
    fixture_repo = repo_root / "tests" / "e2e" / "fixtures" / "local_repo"
    manifest_path = repo_root / "tests" / "e2e" / "manifest.json"
    dest_path = repo_root / "tests" / "e2e" / "output" / "local_prompts"
    history_path = dest_path / "history"

    ensure_repo(fixture_repo)

    before = list_history(history_path)
    run_update(repo_root, manifest_path, "e2e-local-prompts")
    after = list_history(history_path)

    print("Initial update complete")
    print(f"History snapshots: {len(after)} (was {len(before)})")

    if args.mutate:
        mutate_repo(fixture_repo)
        before_mutation = list_history(history_path)
        run_update(repo_root, manifest_path, "e2e-local-prompts")
        after_mutation = list_history(history_path)
        print("Mutation update complete")
        print(
            "History snapshots: "
            f"{len(after_mutation)} (was {len(before_mutation)})"
        )

    return 0


if __name__ == "__main__":
    sys.exit(main())
