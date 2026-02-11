i# Scoring Reference

Detailed rubrics and edge-case guidance for the three scoring criteria,
the overqualification exclusion filter, and NLP-enhanced scoring.

## Overqualification Exclusion — Pre-Filter

This filter runs BEFORE scoring. Any candidate whose detected years of
experience strictly exceed the maximum is removed from the scoring pool.

| JD Pattern | Detected Max | Example |
|-----------|-------------|---------|
| "3–5 years" | 5 | Candidate with 6 years → excluded |
| "5+ years" / "at least 5 years" | 10 (min×2) | Candidate with 11 years → excluded |
| "up to 7 years" / "at most 7" | 7 | Candidate with 8 years → excluded |
| No years mentioned | ∞ (skip filter) | No one excluded |
| User provides explicit max | that value | Use user's value |

### Edge Cases
- If years cannot be determined from a resume, do NOT exclude — keep them and note "years unknown."
- If a candidate's date ranges overlap (parallel jobs), the script merges intervals to avoid inflated counts.
- If the JD states "senior" or "staff" with no numeric years, do NOT infer a max — skip the filter for that candidate.

## Experience Match — Detailed Rubric

| Score | Requirements Met | Notes |
|-------|-----------------|-------|
| 10 | All required languages, frameworks, domains, education met; years within ideal range; semantic similarity ≥ 0.75 | Rare; truly exceptional |
| 9 | All required items met; years in range; similarity ≥ 0.65 | |
| 8 | All but one required item met; years within 1 year of min; similarity ≥ 0.55 | |
| 7 | Missing 1–2 non-critical requirements; strong domain overlap | |
| 6 | Meets ~60% of requirements; relevant adjacent experience | |
| 5 | Meets ~50% of requirements; some transferable skills | |
| 4 | Meets ~30–40% of requirements | |
| 3 | Matches a few keywords; mostly unrelated experience | |
| 2 | Minimal overlap; different domain entirely | |
| 1 | No meaningful overlap with job description | |

### Blended Score Formula (when NLP is available)

```
keyword_score    = (matched_requirements / total_requirements) × 10
semantic_score   = similarity × 10
experience_score = round((keyword_score × 0.6) + (semantic_score × 0.4))
```

When NLP is NOT available, use keyword_score only.

### Edge Cases
- If a candidate lists a language under "familiar with" or "basic", count as half credit.
- "Node.js" and "JavaScript" overlap but are not identical — count both if listed separately but only 1 credit toward the JD requirement.
- Alias pairs to treat as identical: Go/Golang, JS/JavaScript, TS/TypeScript, C#/CSharp, C++/CPP, Shell/Bash.
- If no years of experience can be determined, estimate from graduation date (current year − graduation year − typical gap of 0).

## GitHub Profile — Detailed Rubric

| Score | Contributions (last year) | Language Overlap | Notes |
|-------|--------------------------|-----------------|-------|
| 10 | 1500+ | Strong overlap with 3+ required langs | Very active contributor |
| 9 | 1000–1499 | Strong overlap with 2+ required langs | |
| 8 | 750–999 | Good overlap | |
| 7 | 500–749 | Good overlap | |
| 6 | 300–499 | Some overlap | |
| 5 | 200–299 | Some overlap | |
| 4 | 100–199 | Any overlap | |
| 3 | 50–99 | Any overlap | |
| 2 | 1–49 | Any | Minimal activity |
| 1 | 0 or not found | N/A | No GitHub or empty profile |

### Extracting GitHub Data
When fetching `https://github.com/<username>`:
- Look for contribution count in page text (e.g., "X contributions in the last year")
- Check pinned repositories for language tags
- Also check `https://github.com/<username>?tab=repositories` for fuller language data
- If the profile page cannot be fetched (network disabled), assign score 1 with note

### Edge Cases
- Private profiles with no public contributions → score 2 (profile exists but no data)
- Organization accounts mistakenly extracted → score 1, note "appears to be an org, not a user"

## Awards — Detailed Rubric

| Score | Award Type | Examples |
|-------|-----------|----------|
| 10 | Multiple top-tier competitive programming awards | ICPC World Finals + Google Code Jam finalist |
| 9 | One top-tier award + multiple others | ICPC regional winner + multiple hackathon wins |
| 8 | One major competition award | ICPC regional, major hackathon 1st place |
| 7 | Multiple minor awards or one professional recognition | Several hackathon podiums, patent holder |
| 6 | Academic honors + hackathon participation | Magna cum laude + hackathon participant |
| 5 | Strong academic honors | Summa cum laude, multiple Dean's List |
| 4 | Moderate academic honors | Dean's List, academic scholarship |
| 3 | Minor academic mention | One semester Dean's List |
| 2 | Tangential mention | Club leadership, volunteer recognition |
| 1 | No awards mentioned | |

### Award Keyword Patterns
Search for these patterns (case-insensitive):
- `award`, `won`, `winner`, `finalist`, `placed`, `rank`
- `dean's list`, `honor roll`, `honors`
- `scholarship`, `fellowship`, `grant`
- `cum laude`, `magna`, `summa`
- `ICPC`, `ACM`, `IEEE`, `hackathon`, `Code Jam`, `Codeforces`, `TopCoder`
- `olympiad`, `competition`, `contest`
- `patent`, `publication`, `published`, `journal`, `conference paper`

### NLP-Enhanced Award Scoring (optional)
If sentence-transformers is available, compute similarity between each award
snippet and the reference phrase "prestigious international programming
competition award". Use this as a signal for ranking award prestige:
- similarity ≥ 0.5 → treat as a major/prestigious award
- similarity 0.3–0.5 → treat as a moderate award
- similarity < 0.3 → treat as a minor mention
