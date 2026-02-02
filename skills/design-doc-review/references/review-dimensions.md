# Review Dimensions — Detailed Checklist

Use this checklist to systematically evaluate each dimension. Not every item applies to
every design — skip items that are clearly irrelevant, but document why.

---

## 1. PRD Alignment & Requirements Coverage

- Map every PRD requirement to a specific design section. Build a traceability matrix.
- Classify each requirement: fully addressed, partially addressed, or missing.
- Identify items in the design that are not in the PRD (scope creep).
- Verify non-functional requirements are addressed: performance targets, latency budgets,
  throughput requirements, compliance mandates, accessibility, and UX constraints.
- Check that success metrics and acceptance criteria from the PRD have corresponding
  measurable design elements (instrumentation, metrics, dashboards).
- Assess whether must-have vs nice-to-have prioritization is respected.

---

## 2. Architecture & System Design

### System Architecture
- Architecture style (monolithic, microservices, serverless, hybrid, modular monolith)
  and whether it fits the problem's complexity, team size, and operational maturity.
- Component boundaries, responsibilities, and ownership. Are they well-defined?
- Data flow: synchronous vs asynchronous paths. Are they clearly diagrammed?
- Integration points and external dependencies. Are contracts defined? What if they fail?
- Technology stack choices: justified? Mature? Does the team have experience?

### Alternatives & Trade-offs
- Were alternative architectures considered? Documented with pros/cons?
- Are trade-off decisions explicit (e.g., consistency vs availability, build vs buy)?
- Is the rationale sound, or does it reflect resume-driven development?

### Architectural Quality
- Coupling: Is it loose between components? Are there hidden coupling paths?
- Cohesion: Does each component have a clear, focused responsibility?
- Modularity: Can components be developed, deployed, and scaled independently?
- Extensibility: How hard is it to add new features without modifying existing code?
- Blast radius: If one component fails, what else is affected?

---

## 3. Design Principles & Patterns

### Architectural Patterns
- Is the chosen pattern appropriate (layered, hexagonal, event-driven, CQRS, pipes and
  filters, saga, etc.)?
- Is the pattern applied correctly or just named?
- Are domain boundaries clean (DDD bounded contexts, aggregate roots)?

### SOLID at the Module/Service Level
- **Single Responsibility**: Each service/module has one clear reason to change.
- **Open/Closed**: Can the system be extended without modifying core components?
- **Liskov Substitution**: Are interface contracts honored across implementations?
- **Interface Segregation**: Are interfaces focused? Are clients forced to depend on
  methods they do not use?
- **Dependency Inversion**: Do high-level modules depend on abstractions, not concretions?

### Design Health Indicators
- DRY: Is logic duplicated across services/modules unnecessarily?
- KISS: Is the design as simple as possible for the requirements, or over-engineered?
- YAGNI: Are features or abstractions included that are not required by the PRD?
- Composition over inheritance in interface/service design.
- Principle of least astonishment: Would a new team member find the design intuitive?

### Anti-Patterns to Flag
- God service/module (does too much)
- Distributed monolith (microservices that must deploy together)
- Circular dependencies between components
- Leaky abstractions across service boundaries
- Shared mutable state across services without coordination

---

## 4. Data Architecture

### Data Models
- Schema design: normalization level, denormalization trade-offs, relationships.
- Data types: appropriate, efficient, future-proof (e.g., UUIDs vs auto-increment).
- Indexing strategy: are queries supported? Over-indexing risks?
- Entity relationships: are they clearly defined with cardinality?

### Database Selection
- Is the database type (relational, document, graph, key-value, time-series, columnar)
  appropriate for the access patterns?
- CAP theorem trade-offs: explicit and justified?
- Vendor lock-in risk: assessed?

### Data Consistency & Integrity
- Consistency model: strong, eventual, causal — appropriate for the use case?
- Transaction management: ACID compliance, distributed transaction handling (saga, 2PC)?
- Data validation: where does it happen? Client, API gateway, service, database?
- Idempotency: are write operations idempotent? How are duplicate requests handled?

### Data Lifecycle
- Migration strategy: schema evolution, zero-downtime migrations, backward compatibility.
- Backup strategy: frequency, location, tested recovery?
- Retention and archival policies: defined? Compliant with regulations?
- Data classification: PII, PHI, financial data identified and handled appropriately?

---

## 5. API & Interface Design

- API style (REST, GraphQL, gRPC, WebSocket, async messaging) — appropriate for use case?
- Resource naming: consistent, noun-based, intuitive hierarchy?
- HTTP methods (if REST): correct usage of GET/POST/PUT/PATCH/DELETE?
- Status codes: comprehensive, semantically correct, consistent?
- Versioning strategy: URL path, header, query param? Is migration path clear?
- Contract design: request/response schemas well-defined? Using OpenAPI/Protobuf?
- Backward compatibility: can old clients still work when new fields are added?
- Pagination: cursor-based or offset? Appropriate for data volume?
- Rate limiting and throttling: defined? Per-client? Graceful handling?
- Error responses: structured, consistent, informative without leaking internals?
- Idempotency keys: provided for non-idempotent operations?
- Documentation: auto-generated from schema? Examples included?

---

## 6. Security

### Threat Modeling
- Has a threat model been performed (STRIDE, DREAD, attack trees)?
- What are the trust boundaries? Where does untrusted input enter the system?
- What are the highest-value targets (data, admin access, financial operations)?

### Authentication & Authorization
- Authentication mechanism: OAuth 2.0, OIDC, SAML, mTLS, API keys — appropriate?
- Authorization model: RBAC, ABAC, ReBAC — granularity sufficient?
- Session management: token expiry, refresh strategy, revocation?
- MFA: required for privileged operations?
- Service-to-service auth: mTLS, JWT, service mesh?

### Data Protection
- Encryption at rest: algorithm, key size, managed service vs self-managed?
- Encryption in transit: TLS version (1.2+ minimum), cipher suites, certificate management?
- Key management: KMS, rotation schedule, access controls?
- PII/PHI handling: identified, minimized, access-controlled, audit-logged?

### Application Security (OWASP Top 10)
- Input validation and sanitization at every trust boundary.
- Output encoding to prevent injection (SQL, XSS, command, LDAP).
- CSRF protection for state-changing operations.
- Dependency vulnerability management (SCA tooling, update cadence).
- Secrets management: no hardcoded credentials, use vault/KMS, rotation policy.
- Security headers (CSP, HSTS, X-Frame-Options, X-Content-Type-Options).

### Infrastructure Security
- Network segmentation: private subnets, security groups, least-privilege access.
- DDoS protection: CDN, WAF, rate limiting at edge.
- Container/serverless security: image scanning, runtime protection, least privilege.
- Audit logging: who did what, when, from where. Tamper-proof?

### Privacy by Design
- Data minimization: is only necessary data collected?
- Purpose limitation: is data used only for stated purposes?
- Right to erasure: can user data be fully deleted?
- Consent management: is consent tracked and revocable?

---

## 7. Scalability & Performance

### Horizontal Scalability
- Is the design stateless where possible? Where is state, and how is it managed?
- Load balancing strategy: algorithm, health checks, session affinity (if needed)?
- Auto-scaling policies: metric-based triggers, cool-down periods, min/max instances?
- Database scaling: read replicas, sharding strategy, connection pooling?

### Performance Optimization
- Caching: layers (CDN, API gateway, application, database), invalidation strategy,
  cache-aside vs write-through vs write-behind?
- Database query optimization: N+1 prevention, query plans, index coverage?
- Async processing: message queues, worker pools, backpressure handling?
- Connection pooling: database, HTTP, configured appropriately?
- Payload optimization: compression, pagination, field selection?

### Capacity Planning
- Expected load: requests/sec, concurrent users, data volume growth?
- Peak load patterns: seasonal, time-of-day, event-driven?
- Growth projections: 6-month, 1-year, 3-year?
- Resource requirements at each scale tier?
- Cost projections at 2x, 5x, 10x current scale?
- Known bottlenecks and their scaling ceilings?

---

## 8. Availability & Resilience

### High Availability
- Deployment topology: multi-AZ, multi-region, active-active vs active-passive?
- SLA target: what uptime percentage? Is the architecture capable of delivering it?
- Redundancy: are all critical components redundant? No single points of failure?
- Health checks: liveness, readiness, startup probes defined?
- Zero-downtime deployments: supported? How?

### Fault Tolerance Patterns
- Circuit breakers: configured for external dependencies? Fallback behavior?
- Retry logic: exponential backoff with jitter? Max retries? Idempotency ensured?
- Timeouts: defined for every external call? Appropriate values?
- Bulkheads: resource isolation between critical and non-critical paths?
- Graceful degradation: what features degrade? What is the user experience?

### Disaster Recovery
- RTO and RPO: defined, realistic, tested?
- Backup strategy: automated, encrypted, geographically distributed, tested restore?
- Failover: automated or manual? Documented runbook?
- Data integrity during failover: verified? Reconciliation process?

---

## 9. Observability & Reliability

### Monitoring & Alerting
- Golden signals covered: latency, traffic, errors, saturation?
- Logging: structured (JSON), correlation IDs, appropriate levels, sensitive data redacted?
- Distributed tracing: implemented across service boundaries? Sampling strategy?
- Dashboards: defined for each service? Business metrics included?
- Alerting: SLO-based? Actionable? Routed to on-call? Alert fatigue mitigated?
- SLIs, SLOs, SLAs: defined? Realistic? Error budget policy?

### Error Handling
- Error propagation: how do errors flow across service boundaries?
- User-facing errors: informative but not leaking internals?
- Error recovery: automatic retry, dead letter queues, manual intervention paths?
- Partial failure handling: what happens when one dependency is down?

### Testing Strategy
- Unit tests: coverage targets, mocking strategy?
- Integration tests: scope, test environment, data management?
- End-to-end tests: critical paths covered? Flakiness mitigation?
- Performance/load tests: defined scenarios, success criteria, environment parity?
- Chaos engineering: planned? Steady-state hypothesis defined?
- Contract tests: for API compatibility between services?

---

## 10. Operational Readiness

### Deployment
- CI/CD pipeline: fully automated? Stages (build, test, security scan, deploy)?
- Deployment strategy: blue-green, canary, rolling — appropriate for risk level?
- Rollback: automated? Time to rollback? Data migration rollback?
- Feature flags: used for gradual rollout? Kill switches for new features?

### Migration & Rollout
- Migration plan from current state to new design: phased? Dual-write/dual-read?
- Data migration: zero-downtime? Rollback-safe? Tested at scale?
- Cutover plan: defined? Reversible? Communication plan?
- Backward compatibility during transition period?

### Maintenance & Support
- Runbooks: documented for common operational tasks and incidents?
- On-call procedures: escalation path, contact info, response time expectations?
- Incident response: process documented? Post-mortem culture?
- Dependency updates: process for security patches and version upgrades?

### Documentation
- Architecture diagrams: up-to-date, accessible, version-controlled?
- API documentation: auto-generated, complete, with examples?
- Deployment guides: step-by-step, tested?
- Troubleshooting guides: common issues and resolution steps?
- Decision log / ADRs: key decisions documented with context and rationale?

---

## 11. Cross-Cutting Concerns

### Compliance & Governance
- Regulatory requirements identified and addressed (GDPR, HIPAA, PCI-DSS, SOC2)?
- Data residency requirements: data stored in required regions?
- Audit logging: complete trail of who did what, when? Retention policy?

### Cost Optimization
- Resource right-sizing: over-provisioned or under-provisioned?
- Reserved vs on-demand vs spot analysis?
- Data transfer costs: cross-AZ, cross-region, egress?
- Storage tiering: hot, warm, cold data separated?

### Technical Debt
- Shortcuts acknowledged and documented?
- Remediation plan with timeline?
- Maintenance burden assessed realistically?

### Internationalization & Localization
- Multi-language support: needed? How is it handled?
- Date, time, currency, number formatting: locale-aware?
- RTL language support if applicable?

### Accessibility
- WCAG compliance level targeted?
- Keyboard navigation, screen reader support, color contrast?

### Team & Organizational Fit
- Does the team have the skills to build and operate this design?
- Are there cross-team dependencies? Are they acknowledged and coordinated?
- Is the operational burden sustainable for the team size?
