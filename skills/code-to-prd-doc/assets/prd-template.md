# Product Requirements Document: [Product Name]

**Version:** 1.0
**Generated:** [Date]
**Analysis Scope:** [Repository Path]
**Technology Stack:** [Primary languages and frameworks]

---

## Executive Summary

[2-3 paragraph overview: what the software does, who it serves, core value proposition, and current state of implementation]

---

## 1. Product Overview

### 1.1 Product Vision
[Problem being solved and intended outcome]

### 1.2 Target Users
[User types, their characteristics, and primary use cases]

### 1.3 Technology Stack
[Languages, frameworks, databases, infrastructure, key dependencies]

### 1.4 System Architecture
[High-level architecture: layers, projects, component relationships, deployment model]

---

## 2. Functional Requirements

<!-- Group by feature category. Repeat section 2.N for each category. -->

### 2.1 [Feature Category Name]

#### FR-2.1.1: [Feature Name]
- **Description:** [What the feature does]
- **User Story:** As a [user type], I want to [action] so that [benefit]
- **Acceptance Criteria:**
  - [ ] Given [context], when [action], then [outcome]
  - [ ] Given [context], when [action], then [outcome]
- **Priority:** [Critical | High | Medium | Low]
- **Status:** [Implemented | Partial | Planned]
- **Code Location:** [File paths or module names]

<!-- Repeat FR block for each feature in this category -->

### 2.2 [Next Feature Category]
<!-- Continue pattern -->

---

## 3. Non-Functional Requirements

### 3.1 Performance
- **NFR-3.1.1:** [Requirement with measurable criteria]

### 3.2 Security
- **NFR-3.2.1:** [Security requirement]

### 3.3 Scalability
- **NFR-3.3.1:** [Scalability requirement]

### 3.4 Reliability
- **NFR-3.4.1:** [Reliability/availability requirement]

### 3.5 Usability
- **NFR-3.5.1:** [Usability requirement]

### 3.6 Maintainability
- **NFR-3.6.1:** [Code quality, testability, documentation requirement]

---

## 4. Data Requirements

### 4.1 Data Models
[Key entities, their attributes, and relationships]

### 4.2 Data Storage
[Persistence technology, connection patterns, multi-tenancy]

### 4.3 Data Integrity
[Validation rules, constraints, concurrency control, consistency requirements]

### 4.4 Data Migration
[Migration strategy, seeding, schema evolution approach]

---

## 5. Integration Requirements

### 5.1 External APIs
- **INT-5.1.1:** [Integration name] — [Purpose, protocol, data flow]

### 5.2 Third-Party Services
- **INT-5.2.1:** [Service name] — [Purpose, SDK/client used]

### 5.3 Internal Service Communication
- **INT-5.3.1:** [Service-to-service pattern] — [Protocol, messaging, contracts]

---

## 6. Missing Features and Gaps

### 6.1 Functional Gaps

#### GAP-6.1.1: [Gap Title]
- **Description:** [What is missing]
- **Impact:** [Effect on users or system]
- **Priority:** [Critical | High | Medium | Low]
- **User Story:** As a [user], I want [feature] so that [benefit]
- **Complexity:** [Low | Medium | High]

<!-- Repeat for each gap -->

### 6.2 Non-Functional Gaps

#### GAP-6.2.1: [Gap Title]
- **Description:** [What is missing]
- **Impact:** [Effect on system quality]
- **Priority:** [Critical | High | Medium | Low]

---

## 7. Known Issues and Technical Debt

### 7.1 Logical Issues

#### ISSUE-7.1.1: [Issue Title]
- **Location:** [File path : line number or method name]
- **Description:** [What the issue is]
- **Impact:** [Consequences]
- **Recommended Fix:** [High-level approach]
- **Priority:** [Critical | High | Medium | Low]

### 7.2 Performance Issues

#### PERF-7.2.1: [Issue Title]
- **Location:** [File path : line number or method name]
- **Description:** [Performance concern]
- **Impact:** [Expected system impact]
- **Recommended Fix:** [Optimization approach]
- **Priority:** [Critical | High | Medium | Low]

### 7.3 Security Concerns

#### SEC-7.3.1: [Concern Title]
- **Location:** [Affected files or areas]
- **Description:** [Security issue]
- **Risk Level:** [Critical | High | Medium | Low]
- **Recommended Mitigation:** [Fix approach]

### 7.4 Code Quality Issues

#### QUAL-7.4.1: [Issue Title]
- **Location:** [File paths]
- **Description:** [Quality concern]
- **Recommended Action:** [Improvement approach]
- **Priority:** [High | Medium | Low]

---

## 8. Jira Work Item Mapping

### 8.1 Epic Summary

| Epic ID | Epic Name | Description | Story Count | Total Points |
|---------|-----------|-------------|-------------|--------------|
| EPIC-01 | [Name] | [Brief description] | [N] | [Sum] |

### 8.2 Epics and User Stories

#### EPIC-01: [Epic Name]

**Description:** [Detailed epic description]

| Story ID | Title | User Story | Points | Priority |
|----------|-------|-----------|--------|----------|
| US-01.1 | [Name] | As a [user], I want [action] so that [benefit] | [Est] | [Priority] |
| US-01.2 | [Name] | As a [user], I want [action] so that [benefit] | [Est] | [Priority] |

**Epic Acceptance Criteria:**
- [ ] [Criterion]

<!-- Repeat EPIC block for each epic -->

### 8.3 Technical Tasks

| Task ID | Description | Related Story | Estimate |
|---------|-------------|---------------|----------|
| TASK-01 | [Task description] | US-XX.X | [Points] |

### 8.4 Bug Fix Items

| Bug ID | Description | Related Issue | Estimate | Priority |
|--------|-------------|---------------|----------|----------|
| BUG-01 | [Fix description] | ISSUE-X.X.X | [Points] | [Priority] |

---

## Appendix A: Repository Structure

```
[Tree view of key directories and files analyzed]
```

## Appendix B: Glossary

| Term | Definition |
|------|------------|
| [Term] | [Project-specific definition] |

## Appendix C: Analysis Notes

[Assumptions made, areas requiring further clarification, limitations of the analysis]
