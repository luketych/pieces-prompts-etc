---
source: humanlayer
type: command
author: humanlayer-team
created_date: 2025-10-14
updated_date: 2025-10-14
workflow_stage: unknown
labels: []
tags: [automation, full-cycle]
scope: [git, project-management]
requires_human: false
autonomous: false
complexity: simple
dependencies: [commit, describe_pr, linear]
output_format: markdown
use_cases: []
related: []
---

you're working on an experimental feature that didn't get the proper ticketing and pr stuff set up.

assuming you just made a commit, here are the next steps:


1. get the sha of the commit you just made (if you didn't make one, read `.claude/commands/commit.md` and make one)

2. read `.claude/commands/linear.md` - think deeply about what you just implemented, then create a linear ticket about what you just did, and put it in 'in dev' state - it should have ### headers for "problem to solve" and "proposed solution"
3. fetch the ticket to get the recommended git branch name
4. git checkout main
5. git checkout -b 'BRANCHNAME'
6. git cherry-pick 'COMMITHASH'
7. git push -u origin 'BRANCHNAME'
8. gh pr create --fill
9. read '.claude/commands/describe_pr.md' and follow the instructions
