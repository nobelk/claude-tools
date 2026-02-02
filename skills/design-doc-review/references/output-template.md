# Output Template

Use this template to structure the review output. Replace all bracketed placeholders
with actual analysis. Do not leave any placeholder text in the final output.

---

## Severity Definitions

Use these consistently when classifying issues:

| Severity | Label | Meaning | Action Required |
|----------|-------|---------|-----------------|
| P0 | ⛔ Critical | Blocks implementation. Security vulnerability, data loss risk, fundamental architecture flaw, or regulatory violation. | Must fix before implementation begins. |
| P1 | 🔴 High | Significant risk to production success. Will cause outages, performance degradation, or major technical debt if not addressed. | Must fix before launch. |
| P2 | 🟡 Medium | Quality, maintainability, or efficiency concern. Will not block launch but increases operational risk or cost. | Should address in near-term. |
| P3 | 🟢 Low | Improvement suggestion. Best practice that would strengthen the design but is not urgent. | Address when convenient. |

---

## Template

```markdown
# Design Review: [Design Document Title]

| Field | Value |
|-------|-------|
| **Reviewer** | Principal Software Engineer (AI-Assisted Review) |
| **Review Date** | [Current Date] |
| **Design Doc Version** | [Version or "not specified"] |
| **PRD Version** | [Version or "not specified"] |

---

## Executive Summary

### Overall Assessment

[2–3 paragraphs providing a direct, high-level judgment. State whether the design is
production-ready. Identify the single biggest risk. State the overall confidence level
in the design's ability to meet the PRD requirements safely and at scale.]

**Recommendation:** [Select exactly one]

- ✅ **APPROVE** — Production-ready as written.
- ✅ **APPROVE WITH CONDITIONS** — Viable with specified changes before implementation.
- 🔄 **MAJOR REVISION REQUIRED** — Fundamental issues must be reworked. Re-review needed.
- ❌ **REJECT** — Approach is not viable. Needs a fundamentally different design.

### Key Strengths

[3–5 specific, cited strengths. Example: "The event-driven architecture in Section 4.2
cleanly decouples order processing from inventory, enabling independent scaling."]

### Critical Concerns

[3–5 specific, cited concerns with brief impact statements.]

### Confidence Assessment

| Dimension | Confidence | Notes |
|-----------|------------|-------|
| PRD Coverage | High / Medium / Low | [Brief justification] |
| Technical Soundness | High / Medium / Low | [Brief justification] |
| Production Readiness | High / Medium / Low | [Brief justification] |
| Security Posture | High / Medium / Low | [Brief justification] |

---

## 1. PRD Alignment & Requirements Coverage

### Requirements Traceability Matrix

| Requirement | Coverage | Design Section | Notes |
|-------------|----------|----------------|-------|
| [Req description] | ✅ Full / ⚠️ Partial / ❌ Missing | [Section ref] | [Gap or comment] |

### Functional Requirements Summary

- **Fully addressed:** [List with section references]
- **Partially addressed:** [List with specific gaps]
- **Not addressed:** [List with impact assessment]
- **Out of scope (in design but not in PRD):** [List — flag scope creep]

### Non-Functional Requirements Summary

- **Performance:** [Assessment against PRD targets]
- **Security:** [Assessment against PRD requirements]
- **Compliance:** [Assessment against regulatory requirements]
- **Usability / Accessibility:** [Assessment]

---

## 2. Architecture & System Design

### Architecture Assessment

- **Style:** [e.g., Event-driven microservices]
- **Appropriateness:** [Analysis of fit for the problem, team, and scale]
- **Alternatives considered:** [Were they? Are they documented?]

### Component Analysis

[Evaluate component boundaries, responsibilities, and interactions.
Identify any components with unclear ownership or overlapping responsibilities.]

### Data Flow Analysis

[Assess synchronous vs asynchronous paths. Identify bottlenecks or
single-threaded paths that could limit throughput.]

### Technology Stack

| Technology | Purpose | Assessment | Risk |
|------------|---------|------------|------|
| [Tech] | [Why it's used] | ✅ / ⚠️ / ❌ | [Lock-in, maturity, team experience] |

### Architectural Concerns

- **Coupling:** [Tight/Loose — specific examples]
- **Cohesion:** [High/Low — specific examples]
- **Extensibility:** [How hard is it to add the next feature?]
- **Blast radius:** [If component X fails, what else breaks?]

---

## 3. Design Principles & Patterns

### Pattern Assessment

| Pattern | Where Used | Appropriate? | Notes |
|---------|-----------|-------------|-------|
| [Pattern] | [Section] | ✅ / ⚠️ / ❌ | [Assessment] |

### Design Principle Compliance

[Assess SOLID, DRY, KISS, YAGNI at the module/service level.
Call out specific violations with section references.]

### Anti-Patterns Identified

[List any anti-patterns found: god services, distributed monolith,
circular dependencies, leaky abstractions, shared mutable state, etc.]

---

## 4. Data Architecture

### Data Model Assessment

- **Schema design:** [Normalization, relationships, data types]
- **Database choice:** [Appropriate for access patterns? CAP trade-offs?]
- **Indexing:** [Supports expected query patterns?]

### Data Consistency & Integrity

- **Consistency model:** [Strong/Eventual/Causal — appropriate?]
- **Transaction handling:** [ACID/Saga/2PC — appropriate?]
- **Idempotency:** [Write operations idempotent?]

### Data Lifecycle

- **Migration strategy:** [Zero-downtime? Rollback-safe?]
- **Backup & recovery:** [Defined? Tested?]
- **Retention & archival:** [Policy defined? Compliant?]
- **Data classification:** [PII/PHI identified and protected?]

---

## 5. API & Interface Design

### API Quality Assessment

- **Style:** [REST/GraphQL/gRPC — appropriate?]
- **Resource naming:** [Consistent? Intuitive?]
- **Versioning:** [Strategy defined? Migration path clear?]
- **Error handling:** [Consistent? Informative? Secure?]

### Contract Design

- **Schema definition:** [OpenAPI/Protobuf? Well-defined?]
- **Backward compatibility:** [Maintained? Strategy for breaking changes?]
- **Pagination:** [Appropriate strategy for data volumes?]
- **Rate limiting:** [Defined? Per-client? Graceful?]
- **Idempotency keys:** [Provided for non-idempotent operations?]

---

## 6. Security

### Threat Model Summary

- **Trust boundaries identified:** [List]
- **Key threats:** [Top 3–5 threats with severity]
- **Mitigations proposed:** [For each threat]
- **Residual risks:** [Accepted risks with justification]

### OWASP Top 10 Assessment

| Threat Category | Risk | Mitigation | Adequate? |
|-----------------|------|-----------|-----------|
| Injection | H/M/L | [Mitigation] | ✅ / ❌ |
| Broken Authentication | H/M/L | [Mitigation] | ✅ / ❌ |
| Sensitive Data Exposure | H/M/L | [Mitigation] | ✅ / ❌ |
| [Continue for all relevant categories] | | | |

### Authentication & Authorization

- **Authentication:** [Method, assessment]
- **Authorization:** [Model, granularity assessment]
- **Session management:** [Token lifecycle, revocation]

### Data Protection

- **Encryption at rest:** [Method, key management]
- **Encryption in transit:** [TLS version, cert management]
- **PII/PHI handling:** [Identified, minimized, protected?]
- **Privacy by design:** [Data minimization, consent, right to erasure]

### Security Gaps

[List specific vulnerabilities or missing controls, each with severity and recommendation.]

---

## 7. Scalability & Performance

### Scaling Strategy

- **Approach:** [Horizontal/Vertical/Both]
- **Statelessness:** [Where is state? How is it managed?]
- **Auto-scaling:** [Policies defined? Metrics-based triggers?]

### Bottleneck Analysis

| Component | Current Limit | Scaling Strategy | Estimated Ceiling |
|-----------|--------------|------------------|-------------------|
| [Component] | [Limit] | [Strategy] | [Ceiling] |

### Performance Optimization

- **Caching:** [Layers, invalidation strategy]
- **Database:** [Query optimization, read replicas, connection pooling]
- **Async processing:** [Queue design, backpressure handling]

### Capacity & Cost Projections

- **Current expected load:** [RPS, concurrent users, data volume]
- **Cost at 1x / 5x / 10x:** [Estimates]
- **First bottleneck at scale:** [What breaks first?]

---

## 8. Availability & Resilience

### High Availability

- **Topology:** [Multi-AZ/Region, active-active/passive]
- **SLA target:** [Uptime %, achievable with this architecture?]
- **Single points of failure:** [Identified and mitigated?]

### Resilience Patterns

| Pattern | Implemented? | Details |
|---------|-------------|---------|
| Circuit breaker | ✅ / ❌ | [Config, fallback behavior] |
| Retry with backoff | ✅ / ❌ | [Max retries, jitter, idempotency] |
| Timeouts | ✅ / ❌ | [Values for each external call] |
| Bulkhead | ✅ / ❌ | [Resource isolation details] |
| Graceful degradation | ✅ / ❌ | [Feature fallback plan] |

### Disaster Recovery

- **RTO:** [Target, feasibility]
- **RPO:** [Target, backup frequency]
- **Failover:** [Automated/manual? Tested?]
- **Runbook:** [Documented?]

---

## 9. Observability & Reliability

### Monitoring & Alerting

- **Golden signals:** [Latency, traffic, errors, saturation — all covered?]
- **Logging:** [Structured? Correlation IDs? Sensitive data redacted?]
- **Distributed tracing:** [Implemented? Sampling strategy?]
- **Alerting:** [SLO-based? Actionable? On-call routing?]

### SLIs, SLOs, SLAs

| Service | SLI | SLO | Realistic? |
|---------|-----|-----|------------|
| [Service] | [Indicator] | [Objective] | ✅ / ❌ |

### Error Handling

- **Error propagation:** [Across service boundaries]
- **User-facing errors:** [Informative, not leaking internals?]
- **Dead letter queues:** [For failed async messages?]

### Testing Strategy

- **Unit tests:** [Coverage target, approach]
- **Integration tests:** [Scope, environment]
- **E2E tests:** [Critical paths]
- **Performance tests:** [Scenarios, success criteria]
- **Chaos engineering:** [Planned?]
- **Contract tests:** [API compatibility?]

---

## 10. Operational Readiness

### Deployment

- **CI/CD:** [Automated? Stages?]
- **Strategy:** [Blue-green/canary/rolling]
- **Rollback:** [Automated? Time to rollback?]
- **Feature flags:** [Gradual rollout? Kill switches?]

### Migration & Rollout Plan

- **Migration approach:** [Phased? Dual-write? Big-bang?]
- **Data migration:** [Zero-downtime? Rollback-safe?]
- **Cutover plan:** [Defined? Reversible?]
- **Backward compatibility during transition:** [Maintained?]

### Documentation & Runbooks

| Document | Status |
|----------|--------|
| Architecture diagrams | ✅ / ❌ |
| API documentation | ✅ / ❌ |
| Deployment guide | ✅ / ❌ |
| Runbooks | ✅ / ❌ |
| Troubleshooting guide | ✅ / ❌ |
| ADRs / Decision log | ✅ / ❌ |

---

## 11. Cross-Cutting Concerns

### Compliance

- **Regulatory:** [GDPR, HIPAA, PCI-DSS, SOC2 — addressed?]
- **Audit logging:** [Complete? Tamper-proof? Retention?]
- **Data residency:** [Requirements met?]

### Cost

- **Estimated monthly cost:** [Breakdown]
- **Cost at scale:** [2x, 5x, 10x projections]
- **Optimization opportunities:** [Right-sizing, reserved instances, tiering]

### Technical Debt

- **Shortcuts documented:** [With justification and remediation timeline]
- **Maintenance burden:** [Sustainable for team size?]

### Other

- **i18n/l10n:** [Needed? Addressed?]
- **Accessibility:** [WCAG level? Addressed?]
- **Team fit:** [Skills, cross-team dependencies, operational burden]

---

## Findings

### ⛔ P0 — Critical (Must Fix Before Implementation)

**[Issue Title]**
- **Location:** [Design doc section reference]
- **Description:** [Specific explanation of the issue]
- **Impact:** [What goes wrong if not fixed — business and technical impact]
- **Recommendation:** [Specific, actionable fix]
- **Effort:** S / M / L

[Repeat for each P0]

---

### 🔴 P1 — High (Must Fix Before Launch)

**[Issue Title]**
- **Location:** [Section reference]
- **Description:** [Explanation]
- **Impact:** [Risk if not addressed]
- **Recommendation:** [How to fix]
- **Effort:** S / M / L

[Repeat for each P1]

---

### 🟡 P2 — Medium (Address in Near-Term)

**[Issue Title]**
- **Location:** [Section reference]
- **Description:** [Explanation]
- **Impact:** [Quality/maintenance/efficiency impact]
- **Recommendation:** [How to improve]
- **Effort:** S / M / L

[Repeat for each P2]

---

### 🟢 P3 — Low (Improvement Suggestions)

**[Issue Title]**
- **Description:** [Suggestion]
- **Benefit:** [Value if implemented]
- **Recommendation:** [Optional improvement]

[Repeat for each P3]

---

## Strengths

[List 5–10 specific things the design does well. Cite sections. Be genuine —
a credible review recognizes good work. Examples: clean separation of concerns,
thoughtful error handling, well-defined SLOs, thorough threat modeling.]

---

## Final Recommendation

**Decision:** [APPROVE / APPROVE WITH CONDITIONS / MAJOR REVISION REQUIRED / REJECT]

**Conditions for approval** (if conditional):
1. [Specific, verifiable condition]
2. [Another condition]

**Rationale:** [2–3 paragraphs explaining the decision. Reference the most
important strengths and concerns. Be direct about what tipped the balance.]

**Next Steps:**
1. [Immediate action required]
2. [Follow-up action with timeline]
3. [Longer-term consideration]

---

## Appendix

### Open Questions for the Design Team

1. [Specific question requiring clarification — explain why it matters]
2. [Another question]

### Assumptions Made During Review

[List any assumptions made due to missing information or ambiguous design sections.]

### Review Limitations

[Note areas that could not be fully assessed — e.g., performance characteristics
requiring load testing, security requiring penetration testing, or operational
aspects requiring production traffic observation.]

