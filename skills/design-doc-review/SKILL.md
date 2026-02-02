---
name: design-review
description: >
  Conduct a rigorous, principal-engineer-level review of a software design document
  against its product requirements document (PRD). Use when the user asks to review,
  critique, evaluate, or provide feedback on a design document, technical design,
  architecture proposal, system design, or engineering design spec. Also triggers
  when the user asks to check a design doc against a PRD, validate a technical
  approach, or assess production-readiness of a proposed design.
---

# Design Document Review

Conduct a comprehensive design document review with the rigor expected of a principal
software engineer at a top-tier technology company.

## Workflow

### 1. Gather Context

Read all relevant documents before forming any opinions:

- **Design document (DD)** — the primary artifact under review
- **Product requirements document (PRD)** — the source of truth for what must be built
- **Supporting materials** — architecture diagrams, API specs, data models, existing system
  documentation, ADRs (Architecture Decision Records), prior design docs for the same system

If any referenced document is missing or inaccessible, note it as a gap and state what
assumptions are being made in its absence.

### 2. Systematic Review

Evaluate the design across every applicable dimension listed below. For each dimension,
assess what is well-designed, what is missing, and what is risky. Always cite specific
sections, diagrams, or statements from the design document.

Consult **[references/review-dimensions.md](references/review-dimensions.md)** for the
detailed checklist of questions and criteria to evaluate in each dimension.

**Review Dimensions** (evaluate every applicable dimension):

1. **PRD Alignment & Requirements Coverage** — Trace each requirement to the design.
   Identify gaps, partial coverage, scope creep, and unaddressed non-functional requirements.

2. **Architecture & System Design** — Evaluate architecture style, component boundaries,
   data flow, integration points, technology choices, coupling/cohesion, and extensibility.
   Assess whether alternatives were considered and trade-offs justified.

3. **Design Principles & Patterns** — Assess application of SOLID, DRY, KISS, YAGNI,
   separation of concerns. Evaluate architectural pattern choices (not GoF code patterns
   — those belong in code review). Identify anti-patterns.

4. **Data Architecture** — Review data models, database selection, consistency models,
   schema design, indexing, migration strategy, backup/retention, and CAP trade-offs.

5. **API & Interface Design** — Evaluate API style, resource naming, versioning, contract
   design, backward compatibility, error handling, pagination, rate limiting, and documentation.

6. **Security** — Perform threat modeling. Evaluate authentication, authorization, data
   protection, input validation, secrets management, infrastructure security, and
   compliance (OWASP Top 10, GDPR, HIPAA, PCI-DSS, SOC2 as applicable).

7. **Scalability & Performance** — Assess horizontal/vertical scaling strategy, caching,
   async processing, connection pooling, database optimization, capacity planning, and
   cost at scale.

8. **Availability & Resilience** — Evaluate HA topology, fault tolerance patterns (circuit
   breakers, retries, bulkheads, graceful degradation), disaster recovery (RTO/RPO), and
   single points of failure.

9. **Observability & Reliability** — Review monitoring, logging, distributed tracing,
   alerting, SLI/SLO/SLA definitions, error handling strategy, and testing strategy
   (unit, integration, e2e, load, chaos).

10. **Operational Readiness** — Assess CI/CD pipeline, deployment strategy (blue-green,
    canary), rollback plan, feature flags, runbooks, on-call procedures, and documentation.

11. **Cross-Cutting Concerns** — Evaluate compliance/governance, cost optimization,
    technical debt acknowledgment, i18n/l10n, accessibility, privacy by design, and
    migration/rollout plan from current state.

### 3. Produce the Review

Generate the review document using the template in
**[references/output-template.md](references/output-template.md)**.

**Output rules:**

- Save the review as a markdown file.
- Every finding must cite the specific section of the design document it refers to.
- Every issue must include an actionable recommendation — never just state the problem.
- Be direct and specific. Replace all placeholder language with real analysis.
- Assign severity honestly: not everything is P0. Use the full range from P0 to P3.
- Recognize genuine strengths. A credible review is balanced.

## Review Principles

Apply these throughout the review:

- **Be specific** — cite exact sections, diagrams, or statements. Never make vague claims.
- **Explain why** — state the impact of each issue, not just what is wrong.
- **Be constructive** — pair every criticism with an actionable recommendation.
- **Prioritize ruthlessly** — distinguish blockers from nice-to-haves.
- **Consider trade-offs** — acknowledge when the design makes reasonable compromises.
- **Think adversarially** — look for security vulnerabilities, failure modes, edge cases.
- **Think at scale** — consider 10x and 100x the expected load.
- **Think about failure** — what breaks first? What is the blast radius?
- **Assess alternatives** — were other approaches considered? Is the justification sound?
- **Be pragmatic** — perfect is the enemy of shipped, but shipped must be safe.
