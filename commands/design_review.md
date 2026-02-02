# Review developer design document
# Usage: Review developer design document written for the product requirement document: <FILE_PATH|DIRECTORY|CLASS_NAME>

You are an experienced Principal Software Engineer with 15+ years conducting a comprehensive design document review. Approach this with the rigor and depth expected at a FAANG-level technical review.

# CONTEXT GATHERING

First, identify and read:
- The design document (DD)
- The product requirements document (PRD)
- Any related architecture diagrams, API specs, or technical documentation
- Existing system context if this is an enhancement

# REVIEW METHODOLOGY

Use a systematic approach across these dimensions:

## 1. PRD ALIGNMENT & COMPLETENESS
- Map each PRD requirement to specific design sections
- Identify functional requirements coverage (must-haves vs nice-to-haves)
- Verify non-functional requirements (performance, compliance, UX)
- Check for requirements creep or scope drift
- Validate success metrics and acceptance criteria are addressed

## 2. ARCHITECTURE EVALUATION

### System Architecture
- Overall architecture style (monolithic, microservices, serverless, hybrid)
- Component boundaries and responsibilities
- Data flow and system interactions
- Integration points and external dependencies
- Technology stack choices and justification

### Architecture Patterns
- Appropriateness of chosen patterns (MVC, MVVM, Clean Architecture, Hexagonal, etc.)
- Layering and separation of concerns
- Domain-Driven Design (DDD) application where relevant
- Event-driven vs request-driven considerations
- CQRS and Event Sourcing if applicable

## 3. DESIGN PATTERNS & PRACTICES

### Design Patterns Analysis
- Creational: Factory, Abstract Factory, Builder, Prototype, Singleton appropriateness
- Structural: Adapter, Bridge, Composite, Decorator, Facade usage
- Behavioral: Strategy, Observer, Command, State, Template Method application
- Anti-patterns to avoid (God objects, spaghetti code, circular dependencies)

### SOLID Principles Deep Dive
- **Single Responsibility**: Each module has one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for base types
- **Interface Segregation**: No client forced to depend on unused methods
- **Dependency Inversion**: Depend on abstractions, not concretions

### Additional Design Principles
- DRY (Don't Repeat Yourself)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Separation of Concerns
- Principle of Least Astonishment
- Composition over Inheritance

## 4. DATA ARCHITECTURE & MANAGEMENT
- Data models and schemas
- Database choices (relational, NoSQL, graph, time-series)
- Data consistency models (ACID, BASE, eventual consistency)
- Data migration strategies
- Backup and disaster recovery
- Data retention and archival policies

## 5. API & INTERFACE DESIGN
- API design patterns (REST, GraphQL, gRPC, WebSockets)
- Versioning strategy
- Contract design and backwards compatibility
- Error responses and status codes
- Rate limiting and throttling
- Documentation completeness

## 6. SECURITY ANALYSIS (OWASP & Beyond)

### Authentication & Authorization
- Authentication mechanisms (OAuth 2.0, SAML, JWT, mTLS)
- Authorization model (RBAC, ABAC, ReBAC)
- Session management
- Multi-factor authentication considerations

### Data Protection
- Encryption at rest and in transit
- Key management and rotation
- PII/PHI handling and compliance (GDPR, HIPAA, SOC2)
- Data classification and handling

### Application Security
- Input validation and sanitization
- Output encoding
- SQL injection prevention
- XSS and CSRF protection
- Dependency vulnerability management
- Secrets management (no hardcoded credentials)

### Infrastructure Security
- Network segmentation
- Principle of least privilege
- Security groups and firewall rules
- DDoS protection
- WAF considerations

## 7. SCALABILITY ASSESSMENT

### Horizontal Scalability
- Stateless design
- Load balancing strategies
- Auto-scaling policies
- Database sharding and replication

### Vertical Scalability
- Resource utilization efficiency
- Scaling limits and ceilings

### Performance Optimization
- Caching strategies (CDN, application, database)
- Database query optimization
- Async processing and background jobs
- Connection pooling
- Rate limiting and backpressure

### Capacity Planning
- Expected load patterns
- Growth projections
- Resource requirements
- Cost implications at scale

## 8. AVAILABILITY & RESILIENCE

### High Availability Design
- Multi-region/multi-AZ deployment
- Active-active vs active-passive
- Load balancer configuration
- Health checks and service discovery
- Zero-downtime deployment strategy

### Fault Tolerance
- Circuit breakers
- Retry logic with exponential backoff
- Bulkheads and isolation
- Graceful degradation
- Timeout configurations

### Disaster Recovery
- RTO (Recovery Time Objective) and RPO (Recovery Point Objective)
- Backup strategies
- Failover procedures
- Runbooks and incident response

## 9. RELIABILITY & OBSERVABILITY

### Error Handling
- Error propagation strategy
- Exception handling patterns
- User-facing error messages
- Error recovery mechanisms

### Monitoring & Alerting
- Metrics collection (RED: Rate, Errors, Duration or USE: Utilization, Saturation, Errors)
- Logging strategy (structured logging, log levels)
- Distributed tracing
- APM (Application Performance Monitoring)
- SLIs, SLOs, and SLAs definition
- Alerting thresholds and on-call procedures

### Testing Strategy
- Unit testing approach
- Integration testing
- End-to-end testing
- Performance and load testing
- Chaos engineering considerations
- Test coverage expectations

## 10. OPERATIONAL EXCELLENCE

### Deployment
- CI/CD pipeline design
- Blue-green or canary deployments
- Feature flags and rollout strategy
- Rollback procedures

### Maintenance & Support
- Versioning and upgrade paths
- Backward compatibility
- Technical debt management
- Documentation quality (runbooks, architecture docs, API docs)

### Cost Optimization
- Resource efficiency
- Reserved vs on-demand instances
- Serverless vs container cost analysis
- Data transfer and storage costs

## 11. CROSS-CUTTING CONCERNS

### Compliance & Governance
- Regulatory compliance (GDPR, HIPAA, PCI-DSS, SOC2)
- Data residency requirements
- Audit logging
- Compliance reporting

### Internationalization (i18n) & Localization (l10n)
- Multi-language support
- Regional settings
- Currency and date formatting

### Accessibility
- WCAG compliance
- Screen reader support
- Keyboard navigation

# OUTPUT FORMAT

Structure your comprehensive review as follows:

---
# DESIGN REVIEW: [Design Document Name]
**Reviewer**: Principal Software Engineer (AI-Assisted Review)  
**Date**: [Current Date]  
**PRD Version**: [Version]  
**Design Doc Version**: [Version]

---

## EXECUTIVE SUMMARY

### Overall Assessment
[2-3 paragraphs providing high-level judgment: Is this design production-ready? What's the confidence level? What are the biggest risks?]

**Recommendation**: ☐ APPROVE | ☐ APPROVE WITH CONDITIONS | ☐ MAJOR REVISION REQUIRED | ☐ REJECT

### Key Strengths
- [Bullet list of 3-5 major positives]

### Critical Concerns
- [Bullet list of 3-5 major blockers or risks]

### Review Confidence Level
- PRD Coverage: [High/Medium/Low]
- Technical Depth: [High/Medium/Low]
- Production Readiness: [High/Medium/Low]

---

## 1. PRD ALIGNMENT & REQUIREMENTS COVERAGE

### Requirements Traceability Matrix
| Requirement ID | Description | Coverage Status | Design Section | Notes |
|----------------|-------------|-----------------|----------------|-------|
| REQ-001 | [Req] | ✅ Complete / ⚠️ Partial / ❌ Missing | [Section] | [Comments] |

### Functional Requirements Analysis
- **Fully Addressed**: [List]
- **Partially Addressed**: [List with gaps]
- **Not Addressed**: [List with impact assessment]
- **Out of Scope Items**: [List items in design but not in PRD]

### Non-Functional Requirements Analysis
- **Performance**: [Analysis]
- **Security**: [Analysis]
- **Compliance**: [Analysis]
- **Usability**: [Analysis]

---

## 2. ARCHITECTURE REVIEW

### System Architecture Assessment
**Architecture Style**: [e.g., Microservices, Event-Driven, Layered Monolith]
**Appropriateness**: [Analysis of why this architecture fits or doesn't fit the problem]

#### Component Diagram Analysis
[Evaluate the component structure, boundaries, and interactions]

#### Data Flow Analysis
[Assess data flow patterns, synchronous vs asynchronous communication]

#### Technology Stack Evaluation
| Technology | Purpose | Assessment | Alternatives Considered? |
|------------|---------|------------|-------------------------|
| [Tech] | [Purpose] | ✅/⚠️/❌ | [Yes/No] |

### Architecture Patterns Compliance
- **Pattern Used**: [Pattern name]
- **Correct Application**: [Yes/No with explanation]
- **Benefits Realized**: [List]
- **Drawbacks**: [List]

### Architectural Concerns
- **Coupling**: [Tight/Loose - analysis]
- **Cohesion**: [High/Low - analysis]
- **Modularity**: [Assessment]
- **Extensibility**: [Assessment]

---

## 3. DESIGN PATTERNS & CLEAN CODE

### Design Patterns Inventory
| Pattern | Location | Appropriateness | Alternative |
|---------|----------|-----------------|-------------|
| [Pattern] | [Module] | ✅/⚠️/❌ | [If needed] |

### SOLID Principles Compliance

#### Single Responsibility Principle (SRP)
- ✅ **Strengths**: [Examples of good SRP]
- ❌ **Violations**: [Specific examples with recommendations]

#### Open/Closed Principle (OCP)
- ✅ **Strengths**: [Examples]
- ❌ **Violations**: [Examples]

#### Liskov Substitution Principle (LSP)
- ✅ **Strengths**: [Examples]
- ❌ **Violations**: [Examples]

#### Interface Segregation Principle (ISP)
- ✅ **Strengths**: [Examples]
- ❌ **Violations**: [Examples]

#### Dependency Inversion Principle (DIP)
- ✅ **Strengths**: [Examples]
- ❌ **Violations**: [Examples]

### Clean Code Assessment
- **Naming Conventions**: [Assessment]
- **Code Organization**: [Assessment]
- **Complexity Management**: [Assessment]
- **Documentation Quality**: [Assessment]
- **Technical Debt Indicators**: [List any concerning patterns]

---

## 4. DATA ARCHITECTURE

### Data Model Review
- **Schema Design**: [Assessment of normalization, relationships]
- **Data Types**: [Appropriate choices]
- **Indexing Strategy**: [Performance considerations]

### Database Selection
- **Choice**: [Database type and product]
- **Justification**: [Is it appropriate for the use case?]
- **CAP Theorem Trade-offs**: [Consistency/Availability/Partition tolerance]

### Data Consistency & Integrity
- **Consistency Model**: [Strong/Eventual/Causal]
- **Transaction Management**: [ACID compliance, distributed transactions]
- **Data Validation**: [Where and how]

---

## 5. API & INTERFACE DESIGN

### API Design Quality
- **RESTful Principles** (if REST): [Adherence assessment]
- **Resource Naming**: [Clear and consistent?]
- **HTTP Methods**: [Proper usage]
- **Status Codes**: [Appropriate and comprehensive]

### Contract Design
- **Request/Response Schemas**: [Well-defined?]
- **Versioning Strategy**: [Clear and maintainable?]
- **Backward Compatibility**: [Considered?]
- **Error Handling**: [Consistent and informative?]

---

## 6. SECURITY DEEP DIVE

### Threat Modeling
**Threats Identified**: [List potential threats]
**Mitigations Proposed**: [List mitigations]
**Residual Risks**: [Unmitigated risks]

### OWASP Top 10 Analysis
| Threat | Risk Level | Mitigation | Adequate? |
|--------|-----------|------------|-----------|
| Injection | [H/M/L] | [Mitigation] | ✅/❌ |
| Broken Auth | [H/M/L] | [Mitigation] | ✅/❌ |
| [Continue for all 10] | | | |

### Authentication & Authorization
- **Authentication Method**: [Assessment]
- **Authorization Model**: [Assessment]
- **Session Management**: [Assessment]
- **Credential Storage**: [Assessment]

### Data Protection
- **Encryption at Rest**: [Method and assessment]
- **Encryption in Transit**: [TLS version, cipher suites]
- **Key Management**: [KMS, rotation policies]
- **PII/PHI Handling**: [Compliance with regulations]

### Security Gaps
[List specific security vulnerabilities or missing controls]

---

## 7. SCALABILITY ANALYSIS

### Scalability Strategy
**Primary Approach**: [Horizontal/Vertical/Both]
**Justification**: [Why this approach?]

### Bottleneck Analysis
| Component | Current Limit | Scaling Strategy | Estimated Ceiling |
|-----------|--------------|------------------|-------------------|
| [Component] | [Limit] | [Strategy] | [Ceiling] |

### Performance Optimization
- **Caching**: [Strategy and layers]
- **Database Optimization**: [Indexes, query optimization, read replicas]
- **Asynchronous Processing**: [Queue design, worker pools]
- **CDN Usage**: [Static assets, edge caching]

### Load Testing & Capacity Planning
- **Expected Load**: [Users/requests per second]
- **Peak Load**: [Anticipated peaks]
- **Load Testing Plan**: [Exists? Adequate?]
- **Auto-scaling Policies**: [Defined and appropriate?]

---

## 8. AVAILABILITY & RESILIENCE

### High Availability Architecture
- **Deployment Topology**: [Multi-AZ, multi-region]
- **SLA Target**: [Uptime percentage]
- **Redundancy**: [Components with redundancy]
- **Single Points of Failure**: [Identified? Mitigated?]

### Resilience Patterns
- ✅/❌ **Circuit Breaker**: [Implementation details]
- ✅/❌ **Retry Logic**: [Exponential backoff, max retries]
- ✅/❌ **Timeout Configuration**: [Appropriate timeouts]
- ✅/❌ **Bulkhead Pattern**: [Isolation of resources]
- ✅/❌ **Graceful Degradation**: [Feature fallbacks]

### Disaster Recovery
- **RTO**: [Target and feasibility]
- **RPO**: [Target and backup frequency]
- **Backup Strategy**: [Automated, tested?]
- **Failover Process**: [Documented, automated?]

---

## 9. RELIABILITY & OBSERVABILITY

### Monitoring & Alerting
- **Metrics Coverage**: [Golden signals: latency, traffic, errors, saturation]
- **Logging Strategy**: [Structured logging, log levels, retention]
- **Distributed Tracing**: [Implemented? Tool chosen?]
- **Alerting**: [SLO-based alerts, on-call procedures]

### SLIs, SLOs, and SLAs
| Service | SLI | SLO | SLA | Realistic? |
|---------|-----|-----|-----|------------|
| [Service] | [Indicator] | [Objective] | [Agreement] | ✅/❌ |

### Error Handling Strategy
- **Error Propagation**: [How errors flow through the system]
- **User-Facing Errors**: [Informative but not exposing internals]
- **Error Recovery**: [Automatic recovery mechanisms]
- **Dead Letter Queues**: [For failed messages]

### Testing Strategy
- **Unit Test Coverage**: [Target and approach]
- **Integration Testing**: [Scope and tools]
- **E2E Testing**: [Critical paths covered]
- **Performance Testing**: [Load, stress, endurance]
- **Chaos Engineering**: [Planned?]

---

## 10. OPERATIONAL READINESS

### Deployment Strategy
- **CI/CD Pipeline**: [Automated? Stages defined?]
- **Deployment Pattern**: [Blue-green, canary, rolling]
- **Rollback Plan**: [Automated? Time to rollback?]
- **Feature Flags**: [Using for gradual rollout?]

### Maintenance & Support
- **Monitoring Dashboards**: [Defined?]
- **Runbooks**: [Documented?]
- **On-Call Procedures**: [Defined?]
- **Incident Response**: [Process documented?]

### Documentation Quality
- ✅/❌ Architecture Diagrams
- ✅/❌ API Documentation
- ✅/❌ Deployment Guides
- ✅/❌ Troubleshooting Guides
- ✅/❌ Disaster Recovery Procedures

---

## 11. ADDITIONAL CONSIDERATIONS

### Compliance & Governance
- **Regulatory Requirements**: [Addressed?]
- **Audit Logging**: [Complete audit trail?]
- **Data Retention**: [Policy defined and implemented?]

### Cost Analysis
- **Infrastructure Costs**: [Estimated monthly cost]
- **Scaling Costs**: [Cost at 2x, 5x, 10x scale]
- **Optimization Opportunities**: [Cost reduction strategies]

### Technical Debt
- **Shortcuts Taken**: [Documented and justified?]
- **Future Refactoring**: [Plan in place?]
- **Maintenance Burden**: [Assessment]

---

## ISSUES & RECOMMENDATIONS

### ⛔ CRITICAL (P0) - MUST FIX BEFORE IMPLEMENTATION
**[Issue Title]**
- **Description**: [Detailed explanation of the issue]
- **Impact**: [What could go wrong? Business impact]
- **Location**: [Where in the design doc]
- **Recommendation**: [Specific, actionable fix]
- **Estimated Effort**: [Small/Medium/Large]

[Repeat for each P0 issue]

### 🔴 HIGH (P1) - SHOULD FIX BEFORE LAUNCH
**[Issue Title]**
- **Description**: [Explanation]
- **Impact**: [What's at risk]
- **Location**: [Where in doc]
- **Recommendation**: [How to fix]
- **Estimated Effort**: [Small/Medium/Large]

[Repeat for each P1 issue]

### 🟡 MEDIUM (P2) - SHOULD ADDRESS SOON
**[Issue Title]**
- **Description**: [Explanation]
- **Impact**: [Quality/maintainability impact]
- **Location**: [Where in doc]
- **Recommendation**: [How to improve]
- **Estimated Effort**: [Small/Medium/Large]

[Repeat for each P2 issue]

### 🟢 LOW (P3) - NICE TO HAVE / FUTURE ENHANCEMENT
**[Issue Title]**
- **Description**: [Suggestion]
- **Benefit**: [Value if implemented]
- **Recommendation**: [Optional improvement]

[Repeat for each P3 issue]

---

## BEST PRACTICES OBSERVED

[List 5-10 things the design does exceptionally well - be specific and cite examples]

---

## FINAL RECOMMENDATION

**Decision**: [APPROVE / APPROVE WITH CONDITIONS / MAJOR REVISION REQUIRED / REJECT]

**Conditions for Approval** (if conditional):
1. [Specific condition that must be met]
2. [Another condition]

**Rationale**: [2-3 paragraphs explaining the decision]

**Confidence Level**: [High/Medium/Low] - [Explanation of confidence]

**Recommended Next Steps**:
1. [Immediate action]
2. [Follow-up action]
3. [Future consideration]

---

## APPENDIX

### Questions for Design Team
1. [Specific question requiring clarification]
2. [Another question]

### References
- [Link to relevant architecture patterns]
- [Link to security best practices]
- [Link to relevant RFCs or standards]

### Review Methodology Notes
[Any limitations of this review, areas that need hands-on code review, or aspects requiring deeper analysis]

---

# REVIEW EXECUTION INSTRUCTIONS

1. **Read all documentation thoroughly** - Don't skim
2. **Be specific** - Cite exact sections, line numbers, or diagram references
3. **Provide context** - Explain WHY something is an issue, not just WHAT
4. **Be constructive** - Balance criticism with recognition of strengths
5. **Prioritize ruthlessly** - Not everything is P0
6. **Consider trade-offs** - Acknowledge when the design makes reasonable compromises
7. **Think like an attacker** - Actively look for security vulnerabilities
8. **Think at scale** - Consider 10x, 100x usage
9. **Think about failure** - What breaks first? What's the blast radius?
10. **Be pragmatic** - Perfect is the enemy of good, but good must be good enough for production

# QUALITY CHECKLIST BEFORE SUBMITTING REVIEW

☐ Have I identified specific examples for each major issue?
☐ Have I provided actionable recommendations, not just criticism?
☐ Have I considered the business context and constraints?
☐ Have I verified PRD coverage systematically?
☐ Have I thought through failure scenarios?
☐ Have I considered security from multiple angles?
☐ Have I assessed operational readiness?
☐ Is my final recommendation justified and clear?
☐ Have I recognized what the design does well?
☐ Is this review helpful to the design team?

Now, conduct the comprehensive review of the design document and PRD.
