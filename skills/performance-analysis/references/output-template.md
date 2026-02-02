# Performance Analysis Report Template

Use this template for the final report output. Adapt sections based on findings — omit sections with no findings, expand sections with critical issues.

---

## Report Structure

```markdown
# Performance Analysis Report

**Target**: [repository / solution / project / file(s) analyzed]
**Date**: [YYYY-MM-DD]
**Scope**: [Full codebase / module / specific files]
**Runtime**: [.NET 8, .NET 6, Node.js, etc. — if identified]

---

## Executive Summary

[2-4 sentences: overall performance health, most critical risk, key recommendation.
State whether the codebase is production-ready from a performance perspective.]

**Risk Level**: [🔴 Critical / 🟡 Moderate / 🟢 Healthy]
**Critical Issues**: [N]
**High Priority**: [N]
**Medium Priority**: [N]
**Low Priority**: [N]

---

## Findings Overview

| ID | Severity | Category | Location | Issue | Est. Impact |
|----|----------|----------|----------|-------|-------------|
| P-01 | 🔴 CRIT | Memory | `OrderService.cs:87` | Unbounded cache growth | OOM under load |
| P-02 | 🟠 HIGH | Database | `ReportRepo.cs:42` | N+1 query in GetOrders | 50x excess queries |
| P-03 | 🟡 MED | CPU | `Parser.cs:120` | Regex compiled per call | ~30% CPU overhead |
| P-04 | 🔵 LOW | Logging | `Startup.cs:15` | String interpolation in logs | Minor alloc overhead |

---

## Detailed Findings

### P-01: [Descriptive Issue Title]

**Severity**: 🔴 CRITICAL
**Category**: [CPU | Memory | Database | I/O | Concurrency | Caching | Serialization | Configuration | Architecture]
**Location**: `[file:line]`
**Confidence**: [High | Medium — based on static analysis vs runtime data]

**Problem**
[Clear explanation of the issue, why it matters, and how it manifests at runtime.
Include the trigger condition: "This occurs when..." or "Under load, this causes..."]

**Evidence**
[Code snippet, counter output, trace excerpt, or query log that demonstrates the issue.]

```csharp
// Current problematic code
```

**Recommendation**
[Specific fix with code example. Explain why the fix works.]

```csharp
// Recommended fix
```

**Expected Improvement**
[Quantified when possible: "Reduces query count from O(n) to O(1)", "Eliminates ~500 MB/hour leak",
"Reduces P99 latency by ~200ms".]

**Verification**
[How to confirm the fix works: specific dotnet-counters to watch, benchmark to run,
load test scenario, or log query to check.]

---

[Repeat ### P-XX for each finding, ordered by severity then impact.]

---

## Diagnostic Commands Run

[List the diagnostic tools and commands executed during the analysis, if applicable.]

| Tool | Command | Purpose |
|------|---------|---------|
| dotnet-counters | `dotnet-counters monitor --process-id <PID> --counters System.Runtime` | GC and threadpool metrics |
| dotnet-trace | `dotnet-trace collect --process-id <PID> --profile cpu-sampling` | CPU hot path identification |

---

## Performance Metrics Baseline

[If runtime diagnostics were captured, summarize key metrics here.]

| Metric | Value | Assessment |
|--------|-------|------------|
| Working set (MB) | | |
| Gen 0 GC count / min | | |
| Gen 2 GC count / min | | |
| ThreadPool queue length | | |
| Requests / second | | |
| P50 / P99 latency (ms) | | |

---

## Quick Wins

[Ordered list of low-effort, high-impact fixes that can be implemented immediately.]

1. [Quick win with expected impact]
2. [Quick win with expected impact]

---

## Long-Term Recommendations

[Architectural or structural changes that require more effort but deliver sustained improvement.]

1. [Recommendation with rationale]
2. [Recommendation with rationale]

---

## Monitoring Recommendations

[Metrics and alerts to set up for ongoing performance observability.]

- **Key metrics to track**: [list]
- **Alert thresholds**: [list with specific values]
- **Dashboard suggestions**: [what to visualize]

---

## Load Testing Recommendations

[Suggested scenarios to validate performance under realistic conditions.]

| Scenario | Tool | Target | Success Criteria |
|----------|------|--------|------------------|
| Sustained load | k6 / NBomber | 500 RPS for 10 min | P99 < 200ms, no errors |
| Spike test | k6 / NBomber | 0 → 2000 RPS | Recovery within 30s |
| Soak test | k6 / NBomber | 200 RPS for 4 hours | No memory growth |
```

---

## Severity Definitions

Use these consistently across all reports:

- **🔴 CRITICAL**: Causes outages, data loss, or OOM under production load. Fix before deployment.
- **🟠 HIGH**: Significant latency or resource waste visible to users. Fix in current sprint.
- **🟡 MEDIUM**: Noticeable impact under load; suboptimal but functional. Schedule within 1-2 sprints.
- **🔵 LOW**: Minor optimization opportunity. Address during normal refactoring.

## Confidence Levels

- **High**: Issue confirmed through runtime profiling, reproduction, or definitive code pattern.
- **Medium**: Issue identified through static analysis; runtime impact estimated but not measured.
- **Low**: Potential issue based on code pattern; may not be exercised in production paths.
