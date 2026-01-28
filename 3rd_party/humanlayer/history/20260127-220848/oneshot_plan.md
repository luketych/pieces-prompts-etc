---
source: humanlayer
type: command
author: humanlayer-team
created_date: 2025-10-14
updated_date: 2025-10-14
workflow_stage: plan
labels: [planning]
tags: []
scope: [project-management]
requires_human: false
autonomous: false
complexity: simple
dependencies: [ralph_impl, ralph_plan]
output_format: markdown
use_cases: [feature-planning]
related: []
---

1. use SlashCommand() to call /ralph_plan with the given ticket number
2. use SlashCommand() to call /ralph_impl with the given ticket number
