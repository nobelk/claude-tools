---
name: architecture-review
description: "Comprehensive architecture analysis and review of any codebase, producing an industry-standard architecture design document (architecture_overview.md). Use when the user asks to: (1) Review or analyze code architecture, (2) Create an architecture overview or design document, (3) Assess code quality, design patterns, or clean code principles, (4) Identify architectural strengths, weaknesses, or technical debt, (5) Evaluate a codebase for extensibility, robustness, availability, fault tolerance, or other quality attributes, (6) Generate an architecture decision record or architecture assessment. Triggers on terms like 'architecture review', 'code review', 'architecture overview', 'design document', 'codebase analysis', 'technical assessment', or 'architecture audit'."
---

# Architecture Review Skill

Generate an industry-standard architecture design document by systematically analyzing a codebase across structure, patterns, principles, quality attributes, and risk dimensions.

## Workflow

The review has four sequential phases. Complete each fully before proceeding.

### Phase 1: Codebase Exploration

Map the codebase systematically. Spend significant time here — thoroughness prevents hallucinations later.

1. **Project identification** — Run `find` and `ls` to map the full directory tree (exclude `node_modules`, `vendor`, `.git`, `build`, `dist`, `__pycache__`). Identify the project type (web app, API, library, CLI, monorepo, microservices) from config files (`package.json`, `pom.xml`, `go.mod`, `Cargo.toml`, `requirements.txt`, `*.csproj`, `build.gradle`, `Makefile`, etc.).

2. **Entry points & configuration** — Locate main entry points, routing/endpoint definitions, DI/IoC containers, middleware pipelines, and environment configurations.

3. **Component deep-dive** — Read every significant source file. Prioritize files by import frequency and centrality. Document class hierarchies, interface definitions and implementations, module boundaries, and data flow paths from input to output.

4. **Infrastructure** — Review Docker/compose files, CI/CD configs, IaC (Terraform, CloudFormation), database migrations, and deployment scripts.

5. **Tests & documentation** — Assess test structure, coverage patterns, and existing documentation quality.

**Critical rule**: Every claim in the final document must trace to a specific file or code pattern observed during this phase. Take detailed notes.

### Phase 2: Analysis

Apply the analysis framework in `references/analysis-framework.md`. This covers:
- Design patterns (creational, structural, behavioral, architectural)
- Clean code principles (SOLID, DRY, KISS, YAGNI, Separation of Concerns, Law of Demeter)
- Quality attributes (extensibility, robustness, availability, fault tolerance, maintainability, testability, security, performance, scalability, observability, deployability, data integrity)
- Anti-pattern detection

For each finding, record the specific file path and code evidence.

### Phase 3: Document Generation

Produce `architecture_overview.md` following the structure in `references/document-template.md`. Key requirements:

- **Every section must contain evidence** — file paths, code snippets, or concrete observations. No generic filler.
- **Rate quality attributes 1–5** with justification tied to code.
- **Categorize issues by severity** — Critical, High, Medium, Low — with specific file references.
- **Recommendations must be actionable** — include specific refactoring steps, not vague advice.
- Use Mermaid diagrams for component architecture and data flow where appropriate.

### Phase 4: Verification & Optimization

Re-read the generated document against the codebase:

1. **Cross-reference check** — Verify every file path, class name, and code snippet exists in the codebase. Remove or correct anything unverifiable.
2. **Hallucination scan** — Flag any claim not directly supported by observed code. Remove speculative statements.
3. **Completeness audit** — Confirm all major components are covered. Check no significant source file was overlooked.
4. **Quality pass** — Tighten prose, remove redundancy, ensure consistent terminology, and verify all severity ratings are calibrated.
5. **Optimize** — Add any missing analysis dimensions, improve recommendation specificity, ensure the executive summary accurately reflects the full document.

Output the final `architecture_overview.md` only after all verification steps pass.

## References

- **Analysis framework** (patterns, principles, quality attributes, anti-patterns): See `references/analysis-framework.md` — read before starting Phase 2.
- **Document template** (section structure, formatting, examples): See `references/document-template.md` — read before starting Phase 3.
