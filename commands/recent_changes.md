# Recent Changes Analysis Command
# Usage: Analyze git commits from the last month: [DAYS_BACK] [BRANCH]

# Parse inputs
Set DAYS_BACK to first argument from $Arguments, default to 30
Set BRANCH to second argument from $Arguments, default to current branch
Validate DAYS_BACK is a positive number

## Objective
Analyze all git commits made in the specified time period and provide a clear, accurate summary and timeline of changes made by engineers.

---

## Phase 1: Data Collection (Execute in Parallel)

### Group 1: Commit History
```bash
# Get all commits with details
git log --since="${DAYS_BACK} days ago" --pretty=format:"%H|%h|%an|%ae|%ad|%s" --date=short

# Get commit count
git rev-list --count --since="${DAYS_BACK} days ago" HEAD

# Get detailed stats
git log --since="${DAYS_BACK} days ago" --stat --pretty=format:"%H"
```

### Group 2: File Changes
```bash
# Files changed with frequency
git log --since="${DAYS_BACK} days ago" --name-only --pretty=format: | sort | uniq -c | sort -rn | head -20

# Insertions/deletions summary
git log --since="${DAYS_BACK} days ago" --shortstat --pretty=format: | grep -E "files? changed"
```

### Group 3: Author Statistics
```bash
# Commits per author
git shortlog -sn --since="${DAYS_BACK} days ago"

# Lines changed per author
git log --since="${DAYS_BACK} days ago" --format='%an' --numstat | awk 'NF==1 {author=$0} NF==3 {added[author]+=$1; removed[author]+=$2} END {for(a in added) print added[a], removed[a], a}'
```

### Group 4: Change Patterns
```bash
# Commits by day of week
git log --since="${DAYS_BACK} days ago" --format='%ad' --date=format:'%A' | sort | uniq -c

# Commits by hour
git log --since="${DAYS_BACK} days ago" --format='%ad' --date=format:'%H' | sort | uniq -c
```

---

## Phase 2: Analysis

### Commit Classification
Categorize each commit by analyzing the commit message:

| Category | Keywords/Patterns |
|----------|-------------------|
| **Feature** | feat, add, new, implement, introduce |
| **Bug Fix** | fix, bug, patch, resolve, issue |
| **Refactor** | refactor, restructure, reorganize, clean |
| **Documentation** | doc, readme, comment, changelog |
| **Test** | test, spec, coverage, jest, pytest |
| **Build/CI** | build, ci, deploy, pipeline, github action |
| **Style** | style, format, lint, prettier |
| **Performance** | perf, optimize, speed, cache |
| **Security** | security, auth, vulnerability, CVE |
| **Dependency** | deps, upgrade, bump, update package |
| **Chore** | chore, misc, maintenance |

### Impact Assessment
For each significant change, assess:
- Files affected (count and which areas)
- Lines changed (additions/deletions)
- Breaking changes (API changes, schema migrations)
- Dependencies added/removed

---

## Output Format

### Executive Summary
| Metric | Value |
|--------|-------|
| **Period** | [Start Date] to [End Date] |
| **Total Commits** | [Count] |
| **Contributors** | [Count] |
| **Files Changed** | [Count] |
| **Lines Added** | +[Count] |
| **Lines Removed** | -[Count] |
| **Most Active Day** | [Day, Count commits] |

### Key Highlights
[3-5 bullet points of the most significant changes]

---

### Change Distribution

#### By Category
| Category | Commits | % | Trend |
|----------|---------|---|-------|
| Features | [X] | [Y]% | [↑↓→] |
| Bug Fixes | [X] | [Y]% | |
| Refactoring | [X] | [Y]% | |
| Documentation | [X] | [Y]% | |
| Tests | [X] | [Y]% | |
| Other | [X] | [Y]% | |

#### By Week
| Week | Commits | Highlights |
|------|---------|------------|
| Week 4 (Most Recent) | [X] | [Key changes] |
| Week 3 | [X] | [Key changes] |
| Week 2 | [X] | [Key changes] |
| Week 1 (Oldest) | [X] | [Key changes] |

---

### Contributor Summary

| Contributor | Commits | Lines (+/-) | Focus Areas |
|-------------|---------|-------------|-------------|
| [Name] | [X] | +[Y]/-[Z] | [Main areas of work] |
| [Name] | [X] | +[Y]/-[Z] | [Main areas of work] |

---

### Timeline of Changes

#### Week 4: [Date Range]
```
[Date] ──┬── [commit hash] [Author]: [Message]
         ├── [commit hash] [Author]: [Message]
         └── [commit hash] [Author]: [Message]

[Date] ──┬── [commit hash] [Author]: [Message]
         └── [commit hash] [Author]: [Message]
```

#### Week 3: [Date Range]
```
[Similar format...]
```

#### Week 2: [Date Range]
```
[Similar format...]
```

#### Week 1: [Date Range]
```
[Similar format...]
```

---

### Detailed Change Log

#### Features Added
| Date | Commit | Author | Description | Files |
|------|--------|--------|-------------|-------|
| [Date] | [hash] | [Author] | [Message] | [Count] |

#### Bugs Fixed
| Date | Commit | Author | Description | Files |
|------|--------|--------|-------------|-------|
| [Date] | [hash] | [Author] | [Message] | [Count] |

#### Refactoring
| Date | Commit | Author | Description | Impact |
|------|--------|--------|-------------|--------|
| [Date] | [hash] | [Author] | [Message] | [Assessment] |

#### Other Notable Changes
| Date | Commit | Category | Author | Description |
|------|--------|----------|--------|-------------|
| [Date] | [hash] | [Type] | [Author] | [Message] |

---

### Hot Spots (Most Changed Files)

| File | Changes | Authors | Type of Changes |
|------|---------|---------|-----------------|
| [path/to/file] | [X] times | [Names] | [feat/fix/refactor] |
| [path/to/file] | [X] times | [Names] | [feat/fix/refactor] |
| [path/to/file] | [X] times | [Names] | [feat/fix/refactor] |

---

### Potential Concerns

#### High Churn Files
Files changed frequently may indicate:
- Unstable requirements
- Technical debt
- Need for refactoring

| File | Changes | Concern Level |
|------|---------|---------------|
| [path] | [X] | High/Medium/Low |

#### Large Commits
Commits with many file changes may need review:

| Commit | Files | Lines | Author | Description |
|--------|-------|-------|--------|-------------|
| [hash] | [X] | +[Y]/-[Z] | [Name] | [Message] |

---

### Activity Patterns

#### Daily Distribution
```
Mon: ████████████ (XX commits)
Tue: ██████████████████ (XX commits)
Wed: ████████████████ (XX commits)
Thu: ██████████████ (XX commits)
Fri: ██████████ (XX commits)
Sat: ███ (XX commits)
Sun: ██ (XX commits)
```

#### Hourly Distribution (Peak Hours)
```
09:00-12:00: ████████████████ (XX commits)
12:00-15:00: ██████████████ (XX commits)
15:00-18:00: ████████████████████ (XX commits)
```

---

### Summary Statistics

```
REPOSITORY ACTIVITY SUMMARY
===========================
Period: [Start] to [End] ([X] days)

Commits:     [Total] total
             [X] features, [Y] fixes, [Z] refactors

Contributors: [X] active developers
              Most active: [Name] ([X] commits)

Code Churn:  +[X] lines added
             -[Y] lines removed
             [Z] files modified

Velocity:    [X] commits/week average
             [Y] commits/day average

Hot Areas:   [Top 3 directories/modules]
```

---

## Usage Examples

```bash
# Last 30 days (default)
/recent_changes

# Last 7 days
/recent_changes 7

# Last 14 days on main branch
/recent_changes 14 main

# Last 60 days
/recent_changes 60
```

## Notes

- Merge commits are included but flagged separately
- Bot commits (dependabot, etc.) are identified and can be filtered
- Empty commits are excluded from analysis
- Binary file changes are noted but not counted in line statistics
