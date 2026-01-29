# Third-Party Sources

This directory stores upstream prompt/agent collections pulled from external sources.
Each source lives in its own subdirectory and includes `metadata.json`. Prompt files
are stored in `viscera/` so non-prompt assets stay at the root, and updates snapshot
prior prompt states into `history/<timestamp>/` when prompts change.

All update and cleanup commands are expected to be run with `uv`. The helper
scripts exit with a message if run without `uv`.

## Sources

### humanlayer
- **Source**: https://github.com/humanlayer/humanlayer/tree/main/.claude
- **Downloaded**: 2026-01-27
- **Last Updated**: 2026-01-07T11:05:21-08:00
- **Contents**: 33 Claude agents and custom commands
  - 6 agents (codebase analyzer, locator, pattern finder, thoughts analyzer/locator, web search)
  - 27 commands (commit workflows, planning, research, handoffs, etc.)

### joelhooks
- **Source**: https://github.com/joelhooks/opencode-config/tree/main/agent
- **Downloaded**: 2026-01-27
- **Last Updated**: 2026-01-26T10:16:59-08:00
- **Contents**: 7 OpenCode agents
  - 7 agents (archaeologist, explore, refactorer, reviewer, swarm planner/researcher/worker)

### research--ai_prompts
- **Source**: https://github.com/luketych/research--ai_prompts
- **Downloaded**: 2026-01-27
- **Last Updated**: 2025-07-07T13:41:41-07:00
- **Contents**: 7 prompts (prompting technique snippets)
- **Local Changes**: `3rd_party/research--ai_prompts/local` (preserved on update)

## Keeping Sources Updated

This directory tracks upstream locations in `3rd_party/manifest.json` and uses
`scripts/update_3rd_party.py` to sync sources.

### Update Command
```bash
uv run python scripts/update_3rd_party.py
```

### Options
- `--only humanlayer,joelhooks`
- `--dry-run`
- `--report 3rd_party/update_report.json`

### Cleanup History Snapshots
```bash
uv run python scripts/cleanup_3rd_party_history.py
```

### Cleanup Options
- `--only humanlayer,joelhooks`
- `--dry-run`
- `--keep latest`
- `--report 3rd_party/history_cleanup_report.json`

The cleanup helper removes duplicate history snapshots by content digest and keeps
only the earliest (default) or latest snapshot for each unique prompt state.

The updater replaces each source directory while preserving `metadata.json` and any
manifest `preserve` paths, snapshots existing prompts into `history/` when content
changes, and moves prompt files into `viscera/`. Commit metadata is updated when
available.

Supported manifest entry types:
- `git`: requires `source.repo`, optional `ref` and `subdir`
- `url`: requires `source.url`, optional `filename`
- `manual`: tracked for visibility but not auto-updated

## Searching

### By Workflow Stage
```bash
grep -l "workflow_stage: plan" 3rd_party/humanlayer/viscera/*/*.md
grep -l "workflow_stage: research" 3rd_party/humanlayer/viscera/*/*.md
```

### By Use Case
```bash
grep -l "use_cases:.*feature-planning" 3rd_party/humanlayer/viscera/*/*.md
grep -l "use_cases:.*troubleshooting" 3rd_party/humanlayer/viscera/*/*.md
```

### By Tags
```bash
grep -l "tags:.*commit" 3rd_party/humanlayer/viscera/*/*.md
grep -l "tags:.*web-search" 3rd_party/humanlayer/viscera/*/*.md
```

### By Complexity
```bash
grep -l "complexity: simple" 3rd_party/humanlayer/viscera/*/*.md
```

### By Dependencies
```bash
# Find files that depend on specific commands
grep -l "dependencies:.*commit" 3rd_party/humanlayer/viscera/*/*.md
grep -l "dependencies:.*linear" 3rd_party/humanlayer/viscera/*/*.md

# Find files with no dependencies
grep -l "dependencies: \[\]" 3rd_party/humanlayer/viscera/*/*.md
```

### Ask Claude
You can also ask Claude to search for specific functionality:
- "Show me all agents that do codebase analysis"
- "Find prompts for git workflows"
- "What agents require human interaction?"
- "Which commands are autonomous?"
- "Find simple commands for planning"

## Adding New Sources

When adding new sources:
1. Create a new directory named after the source
2. Place prompt files under `viscera/` and keep non-prompt assets at the root
3. Add YAML frontmatter with all metadata fields
4. Create a `metadata.json` with source URL, dates, commit info, and content inventory
5. Add the source to `3rd_party/manifest.json` so it can be refreshed later
6. Update this README with the new source

## Statistics

**humanlayer collection:**
- Total files: 33
- Agents: 6
- Commands: 27
- Workflow stages: plan (9), research (6), execute (3), review (2), debug (1), finalize (5), unknown (7)
- Files with dependencies: 11
- Files with no dependencies: 19
- Most referenced dependencies: `linear` (4), `describe_pr` (3), `commit` (3), `create_plan` (3)

**joelhooks collection:**
- Total files: 7
- Agents: 7
- Commands: 0

**research--ai_prompts collection:**
- Total files: 7
- Prompts: 7
- Agents: 0
- Commands: 0
