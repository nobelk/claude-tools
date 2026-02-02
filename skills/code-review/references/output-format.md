# Output Format

Use this template for the final review output. Omit sections that have no findings (except the Summary and Praise sections, which are always required). Adapt table columns as needed.

---

## PR Review Summary

| Field | Value |
|-------|-------|
| **PR** | #[number] — [title] |
| **Author** | [author] |
| **Branch** | `[head]` → `[base]` |
| **Changed** | [file count] files, +[additions] / −[deletions] lines |
| **Verdict** | ✅ **APPROVE** / ⚠️ **REQUEST CHANGES** / 💬 **COMMENT** |

## Risk Assessment

| Category | Risk | Issues |
|----------|------|--------|
| Security | LOW / MED / HIGH / CRIT | [count] |
| Correctness | LOW / MED / HIGH / CRIT | [count] |
| Performance | LOW / MED / HIGH / CRIT | [count] |
| Test Coverage | LOW / MED / HIGH / CRIT | [count] |
| Data Integrity | LOW / MED / HIGH / CRIT | [count] |

## Executive Summary

2–3 sentences: What does this PR do? Overall assessment? Key concerns?

## Findings

### Critical

| # | File:Line | Issue | Recommendation |
|---|-----------|-------|----------------|
| 1 | `path/to/file.ext:42` | [description + why it matters] | [concrete fix] |

### High

Same format.

### Medium

Same format or bullet list.

### Low

Bullet list.

### Praise

- [Good practice, clean code, or clever solution worth calling out]

## Code Suggestions

For each CRITICAL or HIGH finding, provide a before/after diff:

**Issue**: [description]
**File**: `path/to/file.ext:42`

```diff
- [problematic code]
+ [suggested fix]
```

## Test Coverage

| Changed File | Corresponding Test | Assessment |
|--------------|--------------------|------------|
| `src/auth/login.ts` | `tests/auth/login.test.ts` | ✅ Covered |
| `src/billing/charge.ts` | — | ❌ No tests |

## Action Items

Ordered by priority:

1. **[Must]** [Required change]
2. **[Must]** [Required change]
3. **[Should]** [Strong recommendation]
4. **[Consider]** [Optional improvement]

## Follow-up

- Technical debt or future work items surfaced by this review.
- Monitoring or rollout recommendations (feature flag, canary, etc.).
