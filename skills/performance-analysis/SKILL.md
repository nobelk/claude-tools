---
name: perf-analysis
description: >
  Comprehensive application performance analysis, profiling, and bottleneck detection.
  Use this skill when the user asks to: (1) Review code for performance issues, bottlenecks,
  or antipatterns, (2) Profile or diagnose a running .NET/C# application, (3) Analyze memory
  leaks, CPU hotspots, database query issues, or concurrency problems, (4) Conduct a
  performance audit of a codebase or repository, (5) Generate a performance analysis report.
  Triggers on keywords: performance review, performance analysis, profiling, bottleneck,
  memory leak, slow query, N+1, thread contention, GC pressure, load test, perf audit.
  Supports any language but includes dedicated .NET/C# diagnostic tooling.
---

# Performance Analysis Skill

Conduct rigorous performance reviews matching the depth and rigor of a senior software engineer's audit. Identify antipatterns, leaks, absence of best practices, and quantify impact.

## Workflow

Performance analysis involves these steps:

1. **Determine scope** — identify target (files, project, running process)
2. **Read antipatterns reference** — load `references/antipatterns.md` for the checklist
3. **Static analysis** — scan code for all antipattern categories
4. **Runtime diagnostics** (if applicable) — run profiling tools
5. **Classify findings** — assign severity and category
6. **Generate report** — follow the output template

### Step 1: Determine Scope

Identify what to analyze:
- **Code files/repository** → static analysis (Steps 2-3)
- **Running .NET process** → runtime diagnostics (Step 4) + static analysis
- **Profiling data provided** → interpret and report (Steps 5-6)

If the codebase contains C#/.NET code, read `references/dotnet-diagnostics.md` for tool commands.

### Step 2: Load the Antipatterns Checklist

Read `references/antipatterns.md`. Use it as a comprehensive checklist — systematically evaluate the code against every applicable category:

1. CPU & Algorithmic
2. Memory & GC
3. Database & ORM
4. I/O & Network
5. Concurrency & Threading
6. Caching
7. Serialization
8. Logging & Observability
9. Configuration & Deployment
10. Architecture

Do not skip categories. For each category, explicitly confirm whether issues were found or the code is clean in that area.

### Step 3: Static Analysis

For each source file in scope, scan for:

**Algorithmic complexity** — nested loops, repeated linear searches, unnecessary sorts, recomputed invariants.

**Resource management** — unclosed streams/connections/clients, missing `using`/`Dispose`/`try-finally`, `HttpClient` instantiation per request.

**Database access** — N+1 patterns (lazy loading in loops), `SELECT *`, missing pagination, string-concatenated SQL, missing `AsNoTracking()` (EF Core).

**Async correctness** — `.Result`/`.Wait()` on async code, `async void`, missing `ConfigureAwait(false)` in libraries, `Task.Run` wrapping async methods.

**Memory patterns** — unbounded collections, static caches without eviction, event handler subscriptions without unsubscription, large closures in hot paths, excessive boxing.

**String handling** — concatenation in loops, missing `StringBuilder`, string interpolation in disabled log levels.

**Caching** — expensive repeated computations without memoization, cache without TTL, missing cache-aside pattern.

**Configuration** — debug settings in production paths, untuned connection pools, missing server GC (ASP.NET), missing compression.

**Concurrency** — coarse locks, inconsistent lock ordering, unbounded task spawning, shared mutable state without synchronization.

### Step 4: Runtime Diagnostics (.NET / C#)

When the user provides a running process PID or a project to run, use the diagnostic script or run tools directly.

**Automated collection** — run `scripts/dotnet_perf_check.sh`:
```bash
# Against a running process
bash scripts/dotnet_perf_check.sh --pid <PID> --duration 15 --output ./perf_output

# Against a project (builds, runs, profiles)
bash scripts/dotnet_perf_check.sh --project <path.csproj> --duration 15 --output ./perf_output

# Quick counter-only check
bash scripts/dotnet_perf_check.sh --pid <PID> --counters-only --output ./perf_output
```

**Manual tool usage** — for targeted investigation, run individual tools. Refer to `references/dotnet-diagnostics.md` for complete command reference:

- `dotnet-counters` — live GC, threadpool, exception, and request metrics.
- `dotnet-trace` — CPU sampling profiles, GC event traces, allocation tracking.
- `dotnet-dump` — heap analysis, `dumpheap -stat`, `gcroot` for leak detection.
- `dotnet-gcdump` — lightweight GC heap snapshots safe for production.
- BenchmarkDotNet — micro-benchmark suspicious hot paths.

**Interpret collected data** using the interpretation guide in `references/dotnet-diagnostics.md` § "Interpreting Results".

### Step 5: Classify Findings

Assign each finding a severity:

| Severity | Criteria | Action |
|----------|----------|--------|
| 🔴 CRITICAL | Causes outages, OOM, or data loss under production load | Fix before deployment |
| 🟠 HIGH | Significant latency/resource waste visible to users | Fix in current sprint |
| 🟡 MEDIUM | Noticeable impact under load; functional but suboptimal | Fix within 1-2 sprints |
| 🔵 LOW | Minor optimization; address during refactoring | Backlog |

Assign each finding a confidence:
- **High** — confirmed via profiling, reproduction, or unambiguous code pattern.
- **Medium** — identified via static analysis; runtime impact estimated.
- **Low** — potential issue; may not be hit in production paths.

Assign each finding a category: CPU, Memory, Database, I/O, Concurrency, Caching, Serialization, Logging, Configuration, Architecture.

### Step 6: Generate Report

Read `references/output-template.md` and follow the template structure. Key requirements:

- Every finding must have: ID, severity, category, file location, problem description, code evidence, recommended fix with code, expected improvement, and verification method.
- Findings are ordered by severity (critical first), then by estimated impact.
- Include an executive summary with risk level assessment.
- Include quick wins (low effort, high impact) as a separate section.
- Include monitoring and load testing recommendations.
- If runtime diagnostics were collected, include the metrics baseline table and list commands run.

Output the report as a Markdown file saved to `/mnt/user-data/outputs/`.

## Key Principles

- **Be exhaustive** — check every antipattern category, not just obvious ones. Missing best practices (no caching, no compression, no health checks) are findings too.
- **Be specific** — every finding must reference a file and line. Generic advice without code location is not acceptable.
- **Quantify impact** — use Big-O for algorithmic issues, estimate multipliers for N+1 queries, reference counter thresholds for runtime metrics.
- **Provide working fixes** — code examples must be correct, complete, and idiomatic for the target language/framework.
- **Prioritize ruthlessly** — the report should clearly communicate what to fix first and why.
