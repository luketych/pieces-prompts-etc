# Suggested Additions to PMST Resources

## Overview
These suggestions enhance the PMST framework by adding more granular, actionable patterns that bridge the gap between high-level phase concepts and day-to-day implementation decisions.

---

## Addition 1: New Resource File - `implementation_patterns.md`

### Proposed Location
`/membrane/.opencode/agent/pmst/resources/implementation_patterns.md`

### Content to Add
```markdown
# Implementation Patterns: From Theory to Practice

## The EDAMIS Pattern (Explore-Decide-Abstract-Mitigate-Implement-Stabilize)

While phases describe the overall mode of work, the EDAMIS pattern provides a tactical framework for executing within those phases, particularly when dealing with technical uncertainty.

### Pattern Overview

```
┌─────────────┐
│   EXPLORE   │ ← Divergent Phase
├─────────────┤
│   DECIDE    │ ← Transition Point
├─────────────┤
│  ABSTRACT   │ ← Architectural Boundary
├─────────────┤
│  MITIGATE   │ ← Risk Reduction
├─────────────┤
│  IMPLEMENT  │ ← Convergent Phase
├─────────────┤
│  STABILIZE  │ ← Stabilization Phase
└─────────────┘
```

### Stage Definitions

#### 1. Explore (Divergent Activity)
**Purpose**: Generate multiple solutions to understand the problem space
**Activities**:
- Implement 3+ different approaches (spikes)
- Gather performance and compatibility data
- Document trade-offs and surprises
- Accept throwaway code

**Deliverables**:
- Working prototypes (even if rough)
- Comparison matrix
- Lessons learned document

**Example**:
```python
# Three parallel spikes for data storage
spike_1_redis = RedisStorageSpike()
spike_2_postgres = PostgresStorageSpike()  
spike_3_dynamodb = DynamoDBStorageSpike()

results = benchmark_all([spike_1, spike_2, spike_3])
```

#### 2. Decide (Convergence Catalyst)
**Purpose**: Make informed architectural decisions based on exploration data
**Activities**:
- Analyze exploration results
- Apply decision criteria
- Document rationale in ADRs
- Get stakeholder buy-in

**Deliverables**:
- Architecture Decision Records
- Technical selection matrix
- Migration plan for unchosen options

**Decision Framework**:
```markdown
| Criteria        | Weight | Option A | Option B | Option C |
|----------------|--------|----------|----------|----------|
| Performance    | 30%    | 8/10     | 6/10     | 9/10     |
| Maintainability| 25%    | 7/10     | 9/10     | 5/10     |
| Cost           | 20%    | 5/10     | 8/10     | 3/10     |
| Scalability    | 25%    | 9/10     | 7/10     | 10/10    |
```

#### 3. Abstract (Boundary Creation)
**Purpose**: Create interfaces that allow future flexibility
**Activities**:
- Design abstract base classes
- Define protocol interfaces
- Create adapter patterns
- Plan extension points

**Deliverables**:
- Interface definitions
- Type hierarchies
- Plugin architecture

**Example**:
```python
from abc import ABC, abstractmethod

class StorageBackend(ABC):
    @abstractmethod
    async def get(self, key: str) -> Optional[bytes]: ...
    
    @abstractmethod
    async def put(self, key: str, value: bytes) -> None: ...
    
    @abstractmethod
    async def delete(self, key: str) -> bool: ...
```

#### 4. Mitigate (Risk Reduction)
**Purpose**: Identify and address risks before full implementation
**Activities**:
- Conduct risk assessment
- Implement circuit breakers
- Create rollback mechanisms
- Design graceful degradation

**Deliverables**:
- Risk register with mitigations
- Failure recovery procedures
- Performance benchmarks
- Security review

**Risk Mitigation Patterns**:
- Circuit breakers for external calls
- Bulkheads for resource isolation
- Timeouts for all operations
- Fallbacks for critical paths
- Monitoring and alerting setup

#### 5. Implement (Convergent Execution)
**Purpose**: Build the production solution with confidence
**Activities**:
- Write production code
- Implement comprehensive tests
- Create documentation
- Perform code reviews

**Deliverables**:
- Production-ready code
- Test suite (unit, integration, e2e)
- API documentation
- Deployment artifacts

**Implementation Principles**:
- Test-driven development
- Continuous integration
- Incremental delivery
- Regular refactoring

#### 6. Stabilize (Hardening)
**Purpose**: Ensure reliability and maintainability
**Activities**:
- Performance optimization
- Security hardening
- Operational readiness
- Knowledge transfer

**Deliverables**:
- Performance benchmarks
- Security audit report
- Runbook documentation
- Team training materials

### When to Use EDAMIS

**Full EDAMIS Cycle Appropriate When**:
- High technical uncertainty
- Critical architectural decisions
- Significant innovation required
- Multiple viable approaches exist
- Cost of wrong decision is high

**Shortened Variations**:

**DAMIS** (Decide-Abstract-Mitigate-Implement-Stabilize):
- When exploration already done
- Working with known patterns
- Time-constrained delivery

**EMIS** (Explore-Mitigate-Implement-Stabilize):
- When decision is predetermined
- Exploring implementation details only
- Prototyping with known architecture

**IS** (Implement-Stabilize):
- Well-understood problem
- Proven solution pattern
- Low risk implementation

### Anti-Patterns to Avoid

#### Skipping Exploration
**Problem**: Jumping straight to implementation with first idea
**Consequence**: Missing better solutions, architectural regret
**Solution**: Always explore when uncertainty exists

#### Analysis Paralysis in Decide
**Problem**: Endless analysis without commitment
**Consequence**: Delayed delivery, team frustration
**Solution**: Time-box decision phase, use "good enough" threshold

#### Over-Abstracting
**Problem**: Creating unnecessary abstraction layers
**Consequence**: Complexity without benefit
**Solution**: YAGNI principle, abstract only proven variation points

#### Under-Mitigating
**Problem**: Ignoring identified risks
**Consequence**: Production failures, emergency fixes
**Solution**: Address top risks before implementation

#### Rushing Implementation
**Problem**: Skipping tests to save time
**Consequence**: Bug accumulation, maintenance nightmare
**Solution**: Tests are part of implementation, not optional

#### Perpetual Stabilization
**Problem**: Never declaring "done"
**Consequence**: Delayed value delivery
**Solution**: Define "good enough" criteria upfront

### Integration with Phase Types

#### During Divergent Phases
- Emphasize Explore heavily
- Multiple EDAMIS cycles in parallel
- Decide points are provisional
- Abstract lightly

#### During Convergent Phases
- Skip or minimize Explore
- Focus on Implement and Stabilize
- Abstract based on proven needs
- Mitigate comprehensively

#### During Stabilization Phases
- Minimal Explore
- Focus entirely on Stabilize
- Mitigate operational risks
- Document everything

#### During Pivot Phases
- Rapid Explore-Decide cycles
- Minimal Abstract (will change)
- Mitigate pivot risks
- Implement MVP only
```

---

## Addition 2: Enhance `phases_and_milestones.md`

### Location to Modify
After line 195 in the "Healthy Patterns" section

### Content to Add
```markdown
### The EDAMIS Implementation Pattern

Within the broader phase structure, teams can use the EDAMIS pattern for tactical execution:

**E**xplore → **D**ecide → **A**bstract → **M**itigate → **I**mplement → **S**tabilize

This pattern provides a repeatable framework for navigating technical decisions:

1. **Explore**: Generate multiple solutions (spikes, prototypes)
2. **Decide**: Make data-driven architectural choices
3. **Abstract**: Create interfaces for future flexibility
4. **Mitigate**: Address risks before full implementation
5. **Implement**: Build with tests and documentation
6. **Stabilize**: Harden for production use

#### Mapping EDAMIS to Phases

- **Divergent Phase**: Heavy on Explore, light on Stabilize
- **Convergent Phase**: Heavy on Implement and Stabilize
- **Stabilization Phase**: Focus on Stabilize, minimal Explore
- **Pivot Phase**: Rapid Explore-Decide cycles

#### Example: Adding Authentication to a System

**Divergent Approach**:
```
Week 1: EXPLORE (OAuth, SAML, Custom JWT)
Week 2: DECIDE (Choose OAuth) + ABSTRACT (AuthProvider interface)
Week 3: MITIGATE (Rate limiting, token refresh)
Week 4: IMPLEMENT (Google OAuth provider)
Week 5: STABILIZE (Security audit, monitoring)
```

**Convergent Approach** (if auth pattern already established):
```
Week 1: MITIGATE (Identify risks) + IMPLEMENT (Use existing pattern)
Week 2: STABILIZE (Testing and hardening)
```

See `implementation_patterns.md` for detailed EDAMIS guidance.
```

---

## Addition 3: New Resource File - `decision_frameworks.md`

### Proposed Location
`/membrane/.opencode/agent/pmst/resources/decision_frameworks.md`

### Content to Add
```markdown
# Decision Frameworks: Making Choices with Confidence

## The Decision Point Protocol

Between exploration and implementation lies the critical decision point. This protocol ensures decisions are made with appropriate rigor.

### Decision Readiness Checklist

Before making an architectural decision, ensure:

- [ ] At least 3 options have been explored (or reason why not)
- [ ] Quantitative data exists (performance, cost, complexity)
- [ ] Qualitative factors are documented (team expertise, maintenance)
- [ ] Stakeholders are identified and consulted
- [ ] Reversibility is understood
- [ ] Migration path exists if wrong

### Decision Documentation Template (ADR)

```markdown
# ADR-[NUMBER]: [DECISION TITLE]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
- What problem are we solving?
- What constraints exist?
- What forces are in play?

## Options Considered

### Option A: [Name]
**Description**: Brief description
**Pros**:
- Advantage 1
- Advantage 2
**Cons**:
- Disadvantage 1
- Disadvantage 2
**Prototype Results**: Link to spike code/data

### Option B: [Name]
[Similar structure]

## Decision
We will use [OPTION] because [PRIMARY REASONS].

## Consequences

### Positive
- What becomes easier
- What risks are reduced

### Negative  
- What becomes harder
- What risks are accepted

### Neutral
- What changes but isn't better/worse

## Reversibility
- How hard to change this decision?
- What would trigger reconsideration?
- Migration path if needed?
```

### Decision Criteria Matrix

Weight different factors based on project phase:

| Factor | Divergent Weight | Convergent Weight | Stabilization Weight |
|--------|-----------------|-------------------|---------------------|
| Learning Potential | 40% | 10% | 5% |
| Implementation Speed | 10% | 30% | 20% |
| Reliability | 10% | 25% | 40% |
| Maintainability | 10% | 20% | 25% |
| Performance | 10% | 10% | 10% |
| Innovation | 20% | 5% | 0% |

### Decision Anti-Patterns

#### Premature Optimization
**Symptom**: Choosing complex solution for unproven need
**Fix**: Start simple, evolve based on real requirements

#### Decision by Committee
**Symptom**: Endless meetings without conclusion
**Fix**: Identify single decision owner with input from others

#### Analysis Paralysis
**Symptom**: Perpetual research without choosing
**Fix**: Time-box exploration, decide with available data

#### Resume-Driven Development
**Symptom**: Choosing trendy tech over practical
**Fix**: Weight "boring" reliability appropriately

#### Not-Invented-Here
**Symptom**: Building everything custom
**Fix**: Explore existing solutions first

### Rapid Decision Protocol (for time-critical choices)

When decision needed in < 1 day:
1. List top 3 options (30 minutes)
2. Identify top 3 criteria (15 minutes)
3. Score each option 1-5 on each criterion (15 minutes)
4. Document decision and reasoning (30 minutes)
5. Set review date to revisit if needed

### Decision Review Triggers

Revisit decisions when:
- Original assumptions prove false
- Context significantly changes
- Performance/reliability issues emerge
- Better options become available
- Team expertise evolves
```

---

## Addition 4: Enhance `landscape_navigation.md`

### Location to Modify
After line 150 (end of Seasonal Changes section)

### Content to Add
```markdown
### Navigation Patterns by Terrain Type

Different terrains benefit from different implementation patterns:

#### Familiar Terrain → Fast Implementation
```
Pattern: IS (Implement-Stabilize)
- Skip exploration (already done)
- Jump to implementation
- Focus on quality and testing
Example: Adding CRUD endpoints when you've built 50 before
```

#### Mapped but Unvisited → Guided Exploration
```
Pattern: DAMIS (Decide-Abstract-Mitigate-Implement-Stabilize)
- Light exploration of specific unknowns
- Leverage existing maps (documentation)
- Abstract early for safety
Example: Implementing OAuth for first time with good library
```

#### Partially Explored → Full EDAMIS
```
Pattern: EDAMIS (Explore-Decide-Abstract-Mitigate-Implement-Stabilize)
- Multiple exploration spikes
- Careful decision process
- Heavy risk mitigation
Example: Adopting new AI capabilities
```

#### Uncharted → Multiple Cycles
```
Pattern: Repeated (Explore-Decide) until clarity, then AMIS
- Many small explorations
- Provisional decisions
- Frequent pivots expected
Example: Creating novel user interaction paradigm
```

### Terrain-Specific Risks and Mitigations

| Terrain Type | Primary Risk | Mitigation Strategy |
|-------------|--------------|---------------------|
| Familiar | Overconfidence | Checklist discipline |
| Mapped/Unvisited | Map inaccuracy | Validate assumptions early |
| Partially Explored | Hidden complexity | Multiple spikes, buffer time |
| Uncharted | Complete failure | Small bets, fast feedback |
```

---

## Addition 5: New Resource File - `abstraction_principles.md`

### Proposed Location
`/membrane/.opencode/agent/pmst/resources/abstraction_principles.md`



### Abstraction Debt

Like technical debt, abstraction debt accumulates when:
- Wrong abstractions are chosen
- Abstractions aren't updated with learning
- Too many or too few abstractions exist

#### Paying Down Abstraction Debt
1. **Identify pain points** - Where do abstractions cause friction?
2. **Measure complexity** - Use metrics like coupling and cohesion
3. **Refactor gradually** - Don't rewrite everything at once
4. **Test thoroughly** - Ensure behavior preservation
5. **Document changes** - Help team understand evolution
```

---

## Addition 6: Create Cross-Reference Index

### Proposed Location
`/membrane/.opencode/agent/pmst/resources/INDEX.md`

### Content to Add
```markdown
# PMST Resource Index

## Quick Navigation by Scenario

### "I need to make a technical decision"
- Start with: `decision_frameworks.md`
- Then see: `implementation_patterns.md` → EDAMIS pattern → Decide stage
- Related: `phases_and_milestones.md` → Convergent phases

### "I'm starting something completely new"
- Start with: `phases_and_milestones.md` → Divergent phases
- Then see: `implementation_patterns.md` → Full EDAMIS cycle
- Related: `landscape_navigation.md` → Uncharted terrain

### "I need to reduce technical risk"
- Start with: `implementation_patterns.md` → Mitigate stage
- Then see: `landscape_navigation.md` → Risk by terrain type
- Related: `north_stars_and_evolution.md` → Technical north stars

### "I'm building on existing patterns"
- Start with: `implementation_patterns.md` → Shortened patterns (IS, DAMIS)
- Then see: `landscape_navigation.md` → Familiar terrain
- Related: `phases_and_milestones.md` → Convergent phases

### "I need to create flexible architecture"
- Start with: `abstraction_principles.md`
- Then see: `implementation_patterns.md` → Abstract stage
- Related: `decision_frameworks.md` → Reversibility

### "Project feels stuck"
- Start with: `perspective_management.md` → Altitude check
- Then see: `phases_and_milestones.md` → Anti-patterns
- Related: `north_stars_and_evolution.md` → North star alignment

### "Time to ship to production"
- Start with: `phases_and_milestones.md` → Stabilization phases
- Then see: `implementation_patterns.md` → Stabilize stage
- Related: `landscape_navigation.md` → Seasonal changes

## Pattern Quick Reference

### Full Patterns
- **EDAMIS**: Explore → Decide → Abstract → Mitigate → Implement → Stabilize
- **Diverge-Converge-Stabilize**: Phase-level progression
- **Discover-Develop-Deploy**: Traditional milestone flow

### Shortened Patterns
- **DAMIS**: When exploration is done
- **AMIS**: When decision is made
- **MIS**: When abstraction exists
- **IS**: When just building known pattern

## Concept Connections

```
Phases (Strategic)
    ↓
Milestones (Tactical)
    ↓
EDAMIS Pattern (Implementation)
    ↓
Linear Tasks (Execution)
```
```
