---
name: code-review
description: >
  Rigorous pull request code review matching a senior software engineer's
  standard. Use when asked to review a pull request, PR, merge request, diff,
  branch, or code changes. Accepts a PR number, URL, or branch name. Produces
  a structured review covering correctness, security, performance, testing,
  design, observability, and more using the GitHub CLI (`gh`).
---

# Code Review Skill

Perform a thorough, senior-engineer-grade code review of a pull request.

## Prerequisites

- `gh` CLI authenticated and available on PATH.
- Repository already cloned and working directory inside the repo root.

## Workflow

### 1. Resolve the PR identifier

Accept a PR number, URL, or branch name from the user.

```bash
# Normalize to a PR number
gh pr view <IDENTIFIER> --json number -q '.number'
```

If the identifier is a branch with no open PR, review the diff against the default branch instead:
```bash
git fetch origin <branch>
git diff origin/main...origin/<branch>
```

### 2. Gather context

Fetch metadata and diff in parallel:

```bash
# Metadata
gh pr view <PR> --json title,body,author,baseRefName,headRefName,labels,additions,deletions,changedFiles,commits,reviewDecision

# Full diff
gh pr diff <PR>

# File list
gh pr view <PR> --json files -q '.files[].path'
```

### 3. Triage changed files

Categorize every changed file to focus effort:

| Priority | Category | Examples |
|----------|----------|----------|
| **P0** | Auth, payments, crypto, data access | `auth/`, `billing/`, `middleware/` |
| **P1** | Core business logic, API routes | `services/`, `controllers/`, `api/` |
| **P2** | Tests | `*_test.*`, `__tests__/`, `spec/` |
| **P3** | Config, CI/CD, build | `Dockerfile`, `.github/`, `*.yml` |
| **P4** | Docs, comments, formatting-only | `README`, `CHANGELOG`, `*.md` |
| Skip | Generated / vendored / lockfiles | `package-lock.json`, `*.pb.go`, `vendor/` |

Review P0 files first and most carefully. Skip generated/vendored files unless they are hand-edited.

### 4. Analyze the diff

Read the full review checklist in [references/review-checklist.md](references/review-checklist.md) and evaluate every changed file against the applicable categories. Focus on what changed, not pre-existing issues (unless a change makes an existing problem worse).

Key review dimensions (details in the checklist):

1. **Correctness & Logic** — off-by-one, null/empty, race conditions, state transitions
2. **Security** — injection, auth/z, secrets, input validation, dependency CVEs
3. **Design & Architecture** — abstraction, coupling, SOLID, consistency with codebase patterns
4. **Error Handling & Resilience** — failure modes, retries, timeouts, resource cleanup
5. **Performance & Scalability** — N+1 queries, unbounded loops, missing indexes, memory
6. **Concurrency & Thread Safety** — locks, atomicity, shared mutable state
7. **Testing** — coverage of new code paths, edge cases, assertion quality, no anti-patterns
8. **API & Contract** — backward compatibility, versioning, documentation of public APIs
9. **Data Integrity** — migrations, transactions, idempotency, schema changes
10. **Observability** — logging, metrics, tracing, alerting for new failure modes
11. **Configuration & Environment** — feature flags, env-specific behavior, secrets management
12. **Documentation** — inline comments for complex logic, README updates, changelog

### 5. Classify findings

| Severity | Definition | Merge policy |
|----------|-----------|--------------|
| **CRITICAL** | Security vulnerability, data loss/corruption, crash in production | Must fix |
| **HIGH** | Significant bug, missing critical tests, major perf regression, design flaw | Should fix |
| **MEDIUM** | Code quality, minor test gaps, missing docs, refactoring opportunity | Consider fixing |
| **LOW** | Style nits, minor optimizations, nice-to-have tests | Optional |
| **PRAISE** | Particularly clean code, clever solution, good test — call it out | — |

### 6. Produce the review

Use the output template in [references/output-format.md](references/output-format.md).

Key principles for the write-up:

- **Be specific.** Cite file paths and line ranges. Quote the problematic code.
- **Explain why.** Every finding needs a rationale — what could go wrong, what principle is violated.
- **Provide fixes.** For CRITICAL and HIGH issues, include a concrete code suggestion.
- **Acknowledge good work.** Always include a Praise section.
- **Separate blockers from suggestions.** Use "Must…" for required changes and "Consider…" for optional improvements.
- **Stay constructive.** Review the code, not the author.

## Notes

- For very large PRs (>50 files or >1000 lines changed), summarize the overall change first, then focus detailed review on P0–P1 files. Note which files received lighter review.
- If the PR description or commit messages are unclear, flag this as a MEDIUM finding — good PR hygiene is part of the review.
- When unsure about project conventions, note the ambiguity rather than asserting a style preference.
