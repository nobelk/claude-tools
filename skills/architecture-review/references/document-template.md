# Document Template

Use this structure for `architecture_overview.md`. Every section is required unless explicitly marked optional. Adapt subsections based on what the codebase actually contains — do not include empty sections or generic filler.

## Formatting Rules

- Use Mermaid diagrams (`mermaid` code blocks) for component diagrams and data flow.
- Include file paths as inline code (e.g., `src/services/AuthService.ts`) when referencing code.
- Use tables for structured comparisons (quality ratings, issue categorization).
- Code snippets should be concise — show the pattern, not the whole file.
- Rate quality attributes as: 1 (Critical Deficiency), 2 (Significant Gaps), 3 (Adequate), 4 (Strong), 5 (Exemplary).

---

## Document Structure

```markdown
# Architecture Overview: [Project Name]

**Date**: [Generation Date]
**Codebase Version/Commit**: [If available]
**Scope**: [What was analyzed — directories, services, modules]

---

## Table of Contents

[Auto-generated from sections below]

---

## 1. Executive Summary

[2–3 paragraphs. State: what the system is, its primary architectural style,
the technology stack at a glance, and the top 3 strengths and top 3 concerns.
This section should give a reader the full picture in under 60 seconds.]

---

## 2. Technology Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | e.g., TypeScript | 5.x | Primary language |
| Runtime | e.g., Node.js | 20.x | Server runtime |
| Framework | e.g., Express | 4.x | HTTP framework |
| Database | e.g., PostgreSQL | 15 | Primary data store |
| ORM / Data Access | e.g., Prisma | 5.x | Database abstraction |
| Cache | e.g., Redis | 7.x | Session and data cache |
| Message Broker | e.g., RabbitMQ | 3.x | Async messaging |
| Containerization | e.g., Docker | - | Deployment |
| CI/CD | e.g., GitHub Actions | - | Build pipeline |
| Testing | e.g., Jest, Cypress | - | Unit and E2E tests |
| Monitoring | e.g., Prometheus + Grafana | - | Observability |

[Add or remove rows based on actual stack. Include only what exists.]

---

## 3. Project Structure

[Show the actual directory tree with annotations. Example:]

    project-root/
    ├── src/
    │   ├── controllers/     # HTTP request handlers
    │   ├── services/        # Business logic layer
    │   ├── repositories/    # Data access layer
    │   ├── models/          # Domain entities and DTOs
    │   ├── middleware/       # Express middleware (auth, logging, errors)
    │   ├── config/          # Environment and app configuration
    │   ├── utils/           # Shared utility functions
    │   └── index.ts         # Application entry point
    ├── tests/
    │   ├── unit/
    │   ├── integration/
    │   └── e2e/
    ├── infrastructure/
    │   ├── docker/
    │   └── terraform/
    ├── docs/
    ├── package.json
    └── tsconfig.json

[Describe the purpose of each top-level directory. Note any unusual or
noteworthy structural decisions.]

---

## 4. Architectural Style & System Design

### 4.1 Primary Architecture

[Name the architectural style (e.g., Layered Monolith, Clean Architecture,
Microservices, Event-Driven). Explain how it manifests in the codebase with
specific directory/file references.]

### 4.2 Component Architecture Diagram

[Mermaid diagram showing major components and their relationships:]

    ```mermaid
    graph TB
        Client[Client] --> API[API Gateway]
        API --> Auth[Auth Service]
        API --> Users[User Service]
        API --> Orders[Order Service]
        Users --> DB[(User DB)]
        Orders --> DB2[(Order DB)]
        Orders --> Queue[Message Queue]
        Queue --> Notifications[Notification Service]
    ```

### 4.3 Layer / Module Boundaries

[Describe the boundaries between layers or modules. How is separation
enforced? Are boundaries clean or leaky?]

### 4.4 Data Flow

[Describe how data flows through the system for a representative use case.
Include a sequence or flow diagram if complex:]

    ```mermaid
    sequenceDiagram
        participant C as Client
        participant A as API
        participant S as Service
        participant R as Repository
        participant D as Database
        C->>A: HTTP Request
        A->>S: Validated DTO
        S->>R: Domain Entity
        R->>D: SQL Query
        D-->>R: Result Set
        R-->>S: Domain Entity
        S-->>A: Response DTO
        A-->>C: HTTP Response
    ```

### 4.5 API Design

[If applicable: REST conventions, GraphQL schema design, gRPC service
definitions. Note versioning strategy, error response format, pagination
approach.]

---

## 5. Design Patterns Identified

[For each pattern found, provide: pattern name, where it's used, a brief
code example, and assessment of implementation correctness.]

### 5.1 [Pattern Name]

**Where**: `path/to/file.ext`
**Implementation**: [Brief description]
**Assessment**: [Correct / Partially correct / Misapplied — with explanation]

```[language]
// Concise code snippet showing the pattern
```

[Repeat for each significant pattern. Group by category if many.]

---

## 6. Clean Code Principles Analysis

### 6.1 Principles Well-Applied

[For each principle followed, provide evidence:]

**[Principle Name]**
- Evidence: [Specific file/pattern reference]
- Example: [Brief code snippet or description]

### 6.2 Principles Violated

[For each violation, provide severity, evidence, and impact:]

**[Principle Name]** — Severity: [Critical/High/Medium/Low]
- Violation: [What's wrong]
- Location: `path/to/file.ext`
- Impact: [Why this matters]
- Suggestion: [Specific fix]

---

## 7. Strengths

[List 5–10 concrete strengths, each with evidence. Structure as:]

### 7.1 [Strength Title]

[Description of what's done well, with file path references and code examples
where helpful. Explain why this is architecturally significant.]

---

## 8. Weaknesses & Issues

[Categorize all issues by severity. Each issue must have: description,
location, impact, and recommended fix.]

### 8.1 Critical Issues

[Issues requiring immediate attention — security vulnerabilities, data loss
risks, system stability threats.]

| # | Issue | Location | Impact | Recommendation |
|---|-------|----------|--------|----------------|
| 1 | [Description] | `path/file` | [Impact] | [Fix] |

[Expand on each with details below the table if needed.]

### 8.2 High Priority Issues

[Significant architectural flaws, major maintainability problems.]

### 8.3 Medium Priority Issues

[Code quality issues, minor architectural concerns.]

### 8.4 Low Priority Issues

[Style inconsistencies, minor improvements, nice-to-haves.]

---

## 9. Quality Attribute Assessment

[Rate each attribute 1–5 with justification. Include all applicable attributes.]

| Attribute | Rating | Summary |
|-----------|--------|---------|
| Extensibility | ?/5 | [One-line summary] |
| Robustness | ?/5 | [One-line summary] |
| Availability | ?/5 | [One-line summary] |
| Fault Tolerance | ?/5 | [One-line summary] |
| Maintainability | ?/5 | [One-line summary] |
| Testability | ?/5 | [One-line summary] |
| Security | ?/5 | [One-line summary] |
| Performance | ?/5 | [One-line summary] |
| Scalability | ?/5 | [One-line summary] |
| Observability | ?/5 | [One-line summary] |
| Deployability | ?/5 | [One-line summary] |
| Data Integrity | ?/5 | [One-line summary] |

### 9.1 Extensibility — [Rating]/5

[Detailed analysis with code evidence. What extension points exist? What's
missing? How hard is it to add a new feature?]

### 9.2 Robustness — [Rating]/5

[Detailed analysis. How does the system handle invalid inputs, edge cases,
external failures? Show specific examples.]

[Continue for each attribute. Omit attributes only if truly not applicable
(e.g., Availability for a CLI tool).]

---

## 10. Cross-Cutting Concerns

[Evaluate implementation of shared concerns. Include only those present or
notably absent.]

### 10.1 Error Handling

[Strategy, consistency, gaps. Reference specific error handling patterns.]

### 10.2 Logging & Observability

[Logging approach, structured vs unstructured, log levels, correlation.]

### 10.3 Configuration Management

[How config is loaded, environment handling, secret management.]

### 10.4 Security Implementation

[Auth/authz approach, input validation, data protection.]

[Add sections for: caching, transaction management, API versioning,
rate limiting, i18n — as applicable.]

---

## 11. Dependency Analysis

### 11.1 External Dependencies

[Notable third-party dependencies, their purpose, and any concerns
(outdated versions, known vulnerabilities, license issues, vendor lock-in).]

### 11.2 Internal Coupling

[Assessment of module coupling. Are dependencies well-managed? Are there
circular dependencies? How would you characterize the coupling graph?]

---

## 12. Recommendations

[Concrete, actionable recommendations organized by timeframe.]

### 12.1 Immediate Actions (Week 1–2)

[Quick wins, critical fixes, low-effort/high-impact changes. Be specific
about what to change and where.]

1. **[Action]** — [What to do, which files, expected outcome]
2. ...

### 12.2 Short-Term Improvements (1–3 Months)

[Architectural improvements, refactoring initiatives, tooling upgrades.]

1. **[Action]** — [What to do, rationale, approach outline]
2. ...

### 12.3 Long-Term Roadmap (3–12 Months)

[Strategic architectural changes, migration paths, capability additions.]

1. **[Action]** — [What to do, why, high-level approach, risks]
2. ...

---

## 13. Architecture Decision Log (Optional)

[If architectural decisions are evident from the codebase (e.g., choice of
database, framework, messaging strategy), document them as lightweight ADRs:]

### ADR-001: [Decision Title]

- **Context**: [Why was this decision needed?]
- **Decision**: [What was chosen?]
- **Evidence**: [Where is this visible in the code?]
- **Assessment**: [Was this a good decision? Would you change it today?]

---

## Appendix

### A. File Inventory Summary

| Category | Count | Notable Files |
|----------|-------|---------------|
| Source files | ? | [Key files] |
| Test files | ? | [Key test files] |
| Config files | ? | [Key configs] |
| Documentation | ? | [Key docs] |

### B. Glossary (Optional)

[Domain-specific terms used in the codebase and this document.]
```

---

## Adapting the Template

- **Monorepo / Microservices**: Add a "Service Inventory" section after Section 3, listing each service with its responsibility, tech stack, data store, and API surface. Analyze each service individually in Section 4.
- **Library / SDK**: Replace Availability/Fault Tolerance sections with API Surface Analysis, Backward Compatibility Assessment, and Semantic Versioning Compliance.
- **CLI Tool**: Omit Availability/Scalability. Add Command Structure Analysis and UX Assessment.
- **Frontend Application**: Add sections for State Management, Rendering Strategy, Bundle Analysis, and Accessibility Compliance.
