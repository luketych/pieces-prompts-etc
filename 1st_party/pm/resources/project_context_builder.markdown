# Project Context Builder: Initial Assessment Framework

## Purpose

Before creating meaningful phases and milestones, we need to understand the project's context, constraints, and characteristics. This framework helps classify projects and determine appropriate planning approaches.

## Core Context Questions

### Project Classification

#### 1. Project Origin
- **Greenfield**: Starting from scratch
  - → More divergent phases early
  - → Higher uncertainty tolerance
  - → Flexible architecture decisions
  
- **Legacy Modernization**: Updating existing system
  - → More stabilization phases
  - → Careful migration planning
  - → Backward compatibility concerns
  
- **Feature Addition**: Extending current product
  - → Balanced phase mix
  - → Integration focus
  - → Consistency requirements

#### 2. Scope Certainty
- **Fixed Scope**: Requirements well-defined
  - → Convergent-heavy approach
  - → Detailed milestone planning possible
  - → Traditional phase sequence
  
- **Evolving Requirements**: Learning as we build
  - → Divergent-convergent cycles
  - → Shorter milestone horizons
  - → Frequent pivot checkpoints
  
- **Exploratory**: Discovering what to build
  - → Divergent-first approach
  - → Research-oriented milestones
  - → Flexible phase transitions

#### 3. Target Audience
- **B2B Enterprise**:
  - → Reliability and security focus
  - → Longer stabilization phases
  - → Compliance considerations
  
- **B2C Consumer**:
  - → User experience priority
  - → Rapid iteration capability
  - → A/B testing infrastructure
  
- **Internal Tool**:
  - → Efficiency over polish
  - → Quick divergent phases
  - → Informal validation

- **Developer Tool/API**:
  - → Documentation emphasis
  - → Stability guarantees
  - → Versioning strategy

#### 4. Team Structure
- **Solo Developer**:
  - → All perspectives self-managed
  - → Simplified communication
  - → Risk of perspective blindness
  
- **Small Team (2-5)**:
  - → Informal phase coordination
  - → Shared context easy
  - → Flexible role boundaries
  
- **Large Team (6+)**:
  - → Formal phase gates
  - → Explicit handoffs
  - → Specialized perspectives

#### 5. Time Constraints
- **Urgent Deadline**:
  - → Convergent bias
  - → Minimum viable milestones
  - → Debt acceptance
  
- **Flexible Timeline**:
  - → Full phase cycles
  - → Quality emphasis
  - → Exploration space
  
- **Ongoing/Indefinite**:
  - → Sustainable pace
  - → Regular stabilization
  - → Evolution capability

### Technical Context

#### 6. Technical Maturity
- **Proven Stack**: Well-known technologies
  - → Predictable milestones
  - → Known landscape
  - → Reference architectures
  
- **Mixed Stack**: Some new elements
  - → Learning milestones
  - → Moderate uncertainty
  - → Spike investigations
  
- **Bleeding Edge**: Unproven technologies
  - → High uncertainty
  - → Research phases
  - → Fallback planning

#### 7. Integration Complexity
- **Standalone**: Minimal external dependencies
  - → Independent planning
  - → Full control
  - → Simple deployment
  
- **Moderate Integration**: Some external systems
  - → Coordination milestones
  - → API boundaries
  - → Version management
  
- **Heavy Integration**: Many dependencies
  - → Complex scheduling
  - → Dependency phases
  - → Integration milestones

#### 8. Data Sensitivity
- **Public Data**: No privacy concerns
  - → Open development
  - → Public testing
  - → Community involvement
  
- **Business Data**: Moderate sensitivity
  - → Access controls
  - → Audit requirements
  - → Compliance checks
  
- **Regulated Data**: HIPAA, PCI, GDPR
  - → Security-first phases
  - → Compliance milestones
  - → Audit preparation

### Business Context

#### 9. Revenue Model
- **Direct Sales**: Users pay directly
  - → Feature completeness important
  - → Quality expectations high
  - → Customer support needs
  
- **Subscription/SaaS**: Recurring revenue
  - → Reliability crucial
  - → Feature velocity important
  - → Churn reduction focus
  
- **Indirect/Ad-supported**: Users don't pay
  - → Scale considerations
  - → Engagement metrics
  - → Cost optimization
  
- **Non-revenue**: Internal/OSS
  - → Different success metrics
  - → Community consideration
  - → Sustainability planning

#### 10. Risk Tolerance
- **Risk-Averse**: Cannot fail
  - → Heavy stabilization
  - → Extensive testing
  - → Conservative phases
  
- **Moderate Risk**: Some failure acceptable
  - → Balanced approach
  - → Calculated experiments
  - → Recovery planning
  
- **Risk-Friendly**: Fail fast mentality
  - → Aggressive divergence
  - → Rapid pivots
  - → Learning emphasis

## Context Synthesis

### Project Profiles

Based on answers above, projects typically fall into these profiles:

#### The Explorer Profile
- Greenfield + Evolving requirements + Risk-friendly
- **Phase Pattern**: Heavy divergent → Select → Convergent → Stabilize
- **Milestone Style**: Learning-focused, flexible scope
- **Planning Horizon**: 2-4 weeks maximum

#### The Settler Profile  
- Feature addition + Fixed scope + Moderate risk
- **Phase Pattern**: Plan → Build → Test → Deploy → Maintain
- **Milestone Style**: Deliverable-focused, clear boundaries
- **Planning Horizon**: 4-8 weeks comfortable

#### The Renovator Profile
- Legacy modernization + Risk-averse + Heavy integration
- **Phase Pattern**: Assess → Stabilize → Migrate → Validate
- **Milestone Style**: Risk-reduction, incremental progress
- **Planning Horizon**: 2-4 weeks with buffers

#### The Sprinter Profile
- Urgent deadline + Proven stack + Direct sales
- **Phase Pattern**: Minimal divergent → Rapid convergent → Ship → Stabilize later
- **Milestone Style**: MVP-focused, debt acceptance
- **Planning Horizon**: Daily to weekly

#### The Marathon Runner Profile
- Ongoing + Enterprise + Regulated data
- **Phase Pattern**: Cycles of Plan → Build → Stabilize → Assess
- **Milestone Style**: Sustainable, quality-focused
- **Planning Horizon**: 4-12 weeks

## Initial Context Interview

### Quick Start Questions (5 minutes)

1. **What are you building?** (one sentence)
2. **Who is it for?** (target user)
3. **When does it need to be done?** (timeline)
4. **What already exists?** (greenfield vs existing)
5. **How many people are building it?** (team size)

### Deeper Context Questions (10 minutes)

6. **What's the biggest risk?** (technical/business/timeline)
7. **What can't you compromise on?** (quality/speed/scope)
8. **What's already decided?** (constraints)
9. **What's still unknown?** (uncertainties)
10. **How will you know it's successful?** (metrics)

### Technical Context Questions (10 minutes)

11. **What technologies are you using?** (stack)
12. **What systems must this integrate with?** (dependencies)
13. **What are the performance requirements?** (scale/speed)
14. **What are the security requirements?** (data/access)
15. **What's your deployment environment?** (infrastructure)

## Context Evolution

Context isn't static. Reassess when:

### Triggers for Context Review
- Major pivot or strategic change
- Team size changes significantly
- Requirements substantially change
- Technology decisions prove wrong
- Timeline dramatically shifts
- Integration scope expands
- Regulation requirements emerge
- Business model changes

### Context Drift Indicators
- Phases feeling wrong
- Milestones consistently missed
- Team confusion about priorities
- Stakeholder misalignment
- Unexpected blockers frequent
- Original assumptions invalid
- Success metrics irrelevant

## Using Context for Planning

### Context → Phase Emphasis

**High Uncertainty Contexts** need:
- More divergent phases
- Shorter milestones
- Flexible planning
- Learning metrics

**High Constraint Contexts** need:
- More convergent phases
- Detailed milestones
- Rigid planning
- Compliance metrics

**High Integration Contexts** need:
- Coordination phases
- Integration milestones
- Dependency planning
- Interface metrics

### Context → Milestone Structure

**Explorer Contexts** create milestones that:
- Answer questions
- Test hypotheses
- Produce insights
- Enable decisions

**Builder Contexts** create milestones that:
- Deliver features
- Meet specifications
- Pass tests
- Ship to users

**Maintainer Contexts** create milestones that:
- Reduce debt
- Improve quality
- Enhance performance
- Increase stability

## Context Documentation Template

```markdown
# Project Context

## Quick Classification
- Origin: [Greenfield/Legacy/Feature]
- Scope: [Fixed/Evolving/Exploratory]
- Audience: [B2B/B2C/Internal/Developer]
- Team: [Solo/Small/Large]
- Timeline: [Urgent/Flexible/Ongoing]

## Technical Context
- Stack Maturity: [Proven/Mixed/Bleeding Edge]
- Integration: [Standalone/Moderate/Heavy]
- Data Sensitivity: [Public/Business/Regulated]

## Business Context
- Revenue Model: [Direct/Subscription/Indirect/None]
- Risk Tolerance: [Averse/Moderate/Friendly]

## Key Constraints
1. [Constraint 1]
2. [Constraint 2]
3. [Constraint 3]

## Major Uncertainties
1. [Unknown 1]
2. [Unknown 2]
3. [Unknown 3]

## Success Metrics
1. [Metric 1]
2. [Metric 2]
3. [Metric 3]

## Profile Match
Best fits: [Explorer/Settler/Renovator/Sprinter/Marathon]

## Recommended Approach
- Phase Pattern: [Recommended sequence]
- Milestone Style: [Recommended style]
- Planning Horizon: [Recommended duration]
```

This context becomes the foundation for all subsequent planning.
