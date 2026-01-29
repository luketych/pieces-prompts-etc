# Phases vs Milestones

## Intent
- Separate mode-of-work guidance (phases) from target-state checkpoints (milestones).
- Ensure milestones reduce uncertainty and create tasks; phases shape how work is done.

## Definitions

### Phase (mindshift / operating mode)
- A phase changes how the team works and what is always-on.
- It sets the dominant focus, constraints, and cadence.
- It can span multiple milestones and may overlap with others.

### Milestone (target state / insight gate)
- A milestone is a concrete state we reach.
- It answers questions we could not answer before and reduces uncertainty.
- It includes proposed tasks and is the input for task creation.

## What belongs in each

### Phase content
- Type (divergent, convergent, stabilization, pivot).
- Focus and always-on objectives (ex: testing, guardrails, documentation).
- Entry criteria and exit criteria.
- Working cadence and constraints that apply throughout the phase.
- Risks and success metrics that describe the mode of work.

### Milestone content
- Objective and deliverables (clear, demonstrable outputs).
- Acceptance criteria (how we know we arrived).
- Questions answered / uncertainty reduced.
- Linear task breakdown (to seed tasks).
- Dependencies and dependents.

## Relationship rules
- A phase contains multiple milestones; milestones drive task creation.
- Phases do not include linear task breakdowns.
- Milestones should not be 1:1 duplicates of phases.
- If a milestone spans phases, assign it to the phase where the dominant mode applies.

## Current overlap in this repo (anti-pattern)
- `actionables/phases/0_backlog/1-decisions_and_policy` and
  `actionables/milestones/0_backlog/1-1-decisions_and_policy_baseline` share objectives
  and deliverables, so phase == milestone in practice.
- The same duplication exists for repo scaffold, integration seams, guardrails, and demo
  delivery, which blurs the mode-of-work vs target-state distinction.

## Desired example (after fix)
- Phase: Direction & Constraints (mindshift)
  - Always-on: decisions logged, constraints enforced, documentation updated.
  - Milestones inside:
    - Packaging model locked and artifact location agreed.
    - Base tag stability policy approved.
    - Demo documentation baseline complete.

- Phase: Build & Integrate (mindshift)
  - Always-on: implementation velocity, integration readiness, fixture quality.
  - Milestones inside:
    - Demo scaffold and templates usable.
    - Integration seams validated with fixtures.

- Phase: Validate & Deliver (mindshift)
  - Always-on: validation coverage, guardrails, delivery readiness.
  - Milestones inside:
    - Guardrails enforced and validation checklist passing.
    - Demo walkthrough packaged and reproducible.

## Anti-patterns and fixes
- 1:1 phase/milestone naming -> rename phases to modes, rename milestones to target states.
- Phase includes acceptance criteria -> move acceptance criteria to milestones.
- Milestone reads like a theme -> rewrite as a concrete state and add questions answered.
