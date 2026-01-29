# 3rd-Party Update E2E

This folder contains a local git repo fixture and a manifest for exercising the
third-party updater end-to-end.

## What it does

- Uses a local git repo at `tests/e2e/fixtures/local_repo` as the upstream source.
- Syncs into `tests/e2e/output/local_prompts` using `scripts/update_3rd_party.py`.
- Moves prompt `.md` files into `viscera/` and snapshots prior versions into
  `history/<timestamp>/` when prompt content changes.

## Quick start

Requires `uv` on your PATH. The runner exits with a message if invoked without `uv`.

```bash
uv run python tests/e2e/run_3rd_party_e2e.py
```

To simulate an upstream change:

```bash
uv run python tests/e2e/run_3rd_party_e2e.py --mutate
```

## Manual workflow

1. Edit a prompt file in `tests/e2e/fixtures/local_repo/prompts/*.md`.
2. Commit the change in that local repo.
3. Run:

```bash
uv run python scripts/update_3rd_party.py --manifest tests/e2e/manifest.json --only e2e-local-prompts
```

The updated prompts will appear under `tests/e2e/output/local_prompts/viscera/` and
new history snapshots (if any) will be in `tests/e2e/output/local_prompts/history/`.
