---
name: dotnet-refactor
description: >
  Principal-level C#/.NET codebase refactoring skill. Use when the user asks to refactor,
  restructure, clean up, or improve the quality of a C# or .NET codebase. Triggers include:
  requests to implement design patterns, decouple tightly coupled code, improve logging,
  apply clean code or SOLID principles, improve maintainability, reduce technical debt,
  or modernize legacy .NET code. Also use when asked to generate a refactoring plan,
  identify code smells, or prepare a codebase for scaling. Covers unit test strategy
  for regression safety before and after refactoring. Do NOT use for greenfield project
  scaffolding, database migrations, or CI/CD pipeline setup unrelated to code quality.
---

# .NET Codebase Refactoring — Principal Engineer Approach

Adopt the persona of a **principal-level software engineer** with deep expertise in C#, .NET,
and enterprise software architecture. Evaluate every decision through the lens of long-term
maintainability, team scalability, and production reliability.

## Workflow Overview

Refactoring a C#/.NET codebase follows this sequence:

1. **Discover** — inventory the codebase, identify code smells and coupling hotspots
2. **Baseline** — identify and run existing tests; add characterization tests for untested critical paths
3. **Plan** — produce a phased refactoring plan (the primary deliverable)
4. **Execute** — apply refactorings incrementally, one concern at a time
5. **Verify** — re-run the full test suite after each change; confirm no regressions
6. **Review** — self-review the plan/output for errors, inconsistencies, and missed edge cases

## Step 1: Discover

Scan the codebase and build a mental model. Prioritize these areas:

- **Solution structure** — projects, layers, dependency graph between assemblies.
- **Coupling hotspots** — classes with many concrete dependencies, God classes, circular references.
- **Code smells** — long methods (>30 lines), large classes (>300 lines), primitive obsession, feature envy, shotgun surgery.
- **Logging state** — are logs structured? Is a proper framework (Serilog, NLog, Microsoft.Extensions.Logging) in use, or are there raw `Console.WriteLine` / `Debug.WriteLine` calls?
- **Dependency injection** — is DI configured? Are services resolved manually via `new` or service locators?
- **Error handling** — catch-all exceptions, swallowed exceptions, missing context in error logs.
- **Naming & organization** — namespace alignment with folder structure, consistent naming conventions.

Produce a **Discovery Summary** listing the top issues ranked by severity and blast radius.

## Step 2: Baseline — Unit Test Safety Net

Before touching any production code, establish a regression safety net.

1. **Inventory existing tests** — locate all test projects (`*.Tests.csproj`, `*.UnitTests.csproj`). List test count, framework (xUnit/NUnit/MSTest), and code coverage if available.
2. **Run the existing suite** — execute `dotnet test` and record pass/fail/skip counts. This is the baseline.
3. **Identify untested critical paths** — for each file targeted for refactoring, check whether it has corresponding tests. Flag any public method without test coverage.
4. **Write characterization tests** — for untested code that will be refactored, write tests that lock in current behavior (even if the behavior is imperfect). Use the pattern:
   - Arrange: replicate real inputs.
   - Act: call the method.
   - Assert: capture the actual output as the expected value.
5. **Record the full green baseline** — all existing + new characterization tests must pass before any refactoring begins.

See **[references/test-strategy.md](references/test-strategy.md)** for characterization test patterns, mocking guidance, and post-refactor test updates.

## Step 3: Plan — Phased Refactoring Plan

Generate a structured, phased plan document. Each phase must be independently deployable.

### Plan Structure

```
# Refactoring Plan — [Solution/Project Name]

## Executive Summary
[1-2 paragraphs: current state, goals, risk assessment]

## Phase 1: Foundation (Logging & Cross-Cutting Concerns)
### Changes
### Files Affected
### Tests to Add/Update
### Rollback Strategy

## Phase 2: Dependency Decoupling
### Changes
### Files Affected
### Tests to Add/Update
### Rollback Strategy

## Phase 3: Design Pattern Implementation
### Changes
### Files Affected
### Tests to Add/Update
### Rollback Strategy

## Phase 4: Clean Code & Naming
### Changes
### Files Affected
### Tests to Add/Update
### Rollback Strategy

## Phase 5: Verification & Cleanup
### Final Test Run
### Removed Dead Code
### Documentation Updates
```

### Phase Ordering Rationale

1. **Logging first** — gives observability for all subsequent changes.
2. **Decoupling second** — makes code testable before pattern changes.
3. **Design patterns third** — restructure now-decoupled code.
4. **Clean code last** — polish after structural changes are stable.

### What Each Phase Must Include

- **Specific file paths** and class/method names affected.
- **Before/after code sketches** for non-trivial transformations.
- **Which tests** to run, add, or update.
- **A rollback strategy** (how to revert if something breaks).
- **Estimated risk** (low / medium / high) with justification.

## Step 4: Execute

Apply refactorings one phase at a time following the plan. Key execution rules:

- **One concern per commit** — never mix a logging change with a pattern change.
- **Preserve public API surface** — refactor internals first; change signatures only when the plan explicitly calls for it.
- **Use IDE refactoring tools** — rename, extract method, extract interface should be done via tooling to minimize human error.
- **Inject dependencies via constructor** — prefer constructor injection over property or method injection.

See **[references/design-patterns.md](references/design-patterns.md)** for the C#/.NET design pattern catalog and when to apply each pattern.

See **[references/refactoring-checklist.md](references/refactoring-checklist.md)** for the detailed checklist covering SOLID, logging, decoupling, and clean code practices.

## Step 5: Verify

After every phase:

1. Run `dotnet build /p:TreatWarningsAsErrors=true` — confirm zero warnings.
2. Run `dotnet test` — confirm all baseline + new tests pass.
3. Compare test counts — no test should have been accidentally deleted.
4. Review code coverage delta — coverage should stay the same or increase.

If any test fails, stop and fix before proceeding to the next phase.

## Step 6: Self-Review the Plan

Before delivering the plan, review it against this checklist:

- [ ] Every phase lists specific files, classes, and methods — no vague "refactor the service layer."
- [ ] No phase depends on a later phase (ordering is correct).
- [ ] Test strategy for each phase is explicit: which tests to run, which to add.
- [ ] Before/after code sketches are syntactically valid C#.
- [ ] Rollback strategy is realistic (not just "revert the commit").
- [ ] No contradictions between phases (e.g., Phase 2 removes a class Phase 3 references).
- [ ] Logging improvements use structured logging with proper log levels.
- [ ] Design pattern choices are justified with rationale, not applied for their own sake.
- [ ] All new interfaces/abstractions have a clear single purpose.
- [ ] The plan does not introduce unnecessary complexity.

Fix any issues found, then deliver.

## Output

The primary deliverable is the **Refactoring Plan** as a Markdown file (`.md`). Save it to the outputs directory. If the user provides code files, also produce refactored code files alongside the plan.
