# Code Review Command for Pull Request Analysis
# Usage: Review the code and unit tests in the pull request: <PR_NUMBER|PR_URL|BRANCH_NAME>

# Parse and validate the pull request identifier
Set PR_IDENTIFIER to $Arguments
Validate that PR_IDENTIFIER is provided, otherwise error "Please provide a pull request number, URL, or branch name"

# Step 1: Gather Context (Execute in Parallel)

## 1.1 Fetch PR Information
Execute these commands based on identifier type:
- If PR_IDENTIFIER is a URL: Extract PR number using `gh pr view <URL> --json number`
- If PR_IDENTIFIER is a number: Use `gh pr view <number> --json title,body,author,baseRefName,headRefName,files,additions,deletions`
- If PR_IDENTIFIER is a branch: Use `git fetch origin ${PR_IDENTIFIER}`

## 1.2 Gather Change Context (Run in Parallel)
Execute these simultaneously:
```
# Group 1: PR metadata
gh pr view ${PR_IDENTIFIER} --json title,body,labels,reviewDecision,commits

# Group 2: File changes
gh pr diff ${PR_IDENTIFIER}
gh pr view ${PR_IDENTIFIER} --json files --jq '.files[].path'

# Group 3: Commit history
gh pr view ${PR_IDENTIFIER} --json commits --jq '.commits[].messageHeadline'
git log --oneline origin/main..HEAD (if branch)

# Group 4: Stats
gh pr view ${PR_IDENTIFIER} --json additions,deletions,changedFiles
```

## 1.3 Identify Changed File Types
Categorize files for targeted review:
- Source code files (prioritize)
- Test files (review for coverage)
- Configuration files (security review)
- Documentation files (accuracy check)
- Build/dependency files (vulnerability check)

# Step 2: Parallel Code Analysis

Execute these review streams in parallel, then merge findings:

## Stream A: Security & Risk Analysis
- Scan for hardcoded secrets, API keys, credentials
- Check for SQL injection, XSS, CSRF vulnerabilities
- Review authentication/authorization changes
- Identify sensitive data exposure
- Check dependency changes for known CVEs

## Stream B: Code Quality Analysis
- Evaluate SOLID principles adherence
- Identify code duplication (DRY violations)
- Check naming conventions and readability
- Assess cyclomatic complexity
- Review error handling patterns

## Stream C: Performance Analysis
- Identify N+1 query patterns
- Check for unnecessary loops or computations
- Review database query efficiency
- Evaluate caching opportunities
- Assess memory/resource management

## Stream D: Test Coverage Analysis
- Map changed code to test files
- Identify untested code paths
- Review test quality and assertions
- Check for test anti-patterns
- Verify edge case coverage

# Step 3: Detailed Review Checklist

## 3.1 Code Quality & Design
- [ ] Architectural decisions align with existing patterns
- [ ] SOLID principles followed
- [ ] No code duplication
- [ ] Clear naming conventions
- [ ] Appropriate abstraction levels

## 3.2 Implementation
- [ ] Edge cases handled
- [ ] Error handling is comprehensive
- [ ] Resources properly managed (closed/released)
- [ ] Input validation present
- [ ] Algorithms are efficient

## 3.3 Security (OWASP)
- [ ] No injection vulnerabilities
- [ ] Authentication/authorization correct
- [ ] Sensitive data protected
- [ ] No hardcoded secrets
- [ ] Dependencies are secure

## 3.4 Performance
- [ ] No N+1 queries
- [ ] Efficient algorithms used
- [ ] Caching considered
- [ ] No unnecessary operations
- [ ] Scalability maintained

## 3.5 Testing
- [ ] New code has tests
- [ ] Edge cases tested
- [ ] Tests are meaningful (not just coverage)
- [ ] No test anti-patterns
- [ ] Integration tests if needed

## 3.6 Documentation
- [ ] Complex logic documented
- [ ] Public APIs documented
- [ ] README updated if needed
- [ ] Breaking changes noted

# Step 4: Categorize Findings

## CRITICAL (Must fix before merge)
- Security vulnerabilities (injection, auth bypass, data exposure)
- Data loss or corruption risks
- Breaking changes without migration
- Failing tests or broken functionality

## HIGH (Should fix before merge)
- Significant bugs or logic errors
- Missing critical test coverage
- Major performance regressions
- Design flaws affecting maintainability

## MEDIUM (Consider fixing)
- Code quality issues
- Minor test gaps
- Documentation gaps
- Refactoring opportunities

## LOW (Nice to have)
- Style inconsistencies
- Minor optimizations
- Additional test scenarios
- Code organization improvements

# Step 5: Generate Structured Output

## Output Format

### PR Review Summary
| Field | Value |
|-------|-------|
| **PR** | #[number] - [title] |
| **Author** | [author] |
| **Branch** | [head] → [base] |
| **Files Changed** | [count] |
| **Lines** | +[additions] / -[deletions] |
| **Verdict** | ✅ APPROVE / ⚠️ REQUEST CHANGES / 💬 COMMENT |

### Risk Assessment
| Category | Risk Level | Issues Found |
|----------|------------|--------------|
| Security | [LOW/MED/HIGH/CRIT] | [count] |
| Performance | [LOW/MED/HIGH/CRIT] | [count] |
| Code Quality | [LOW/MED/HIGH/CRIT] | [count] |
| Test Coverage | [LOW/MED/HIGH/CRIT] | [count] |

### Executive Summary
[2-3 sentences: What does this PR do? What's the overall assessment? Key concerns?]

### Findings by Priority

#### CRITICAL Issues
| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | [file] | [line] | [description] | [fix] |

#### HIGH Priority Issues
| # | File | Line | Issue | Recommendation |
|---|------|------|-------|----------------|
| 1 | [file] | [line] | [description] | [fix] |

#### MEDIUM Priority Issues
[Similar table format]

#### LOW Priority Issues
[Similar table format or bullet list]

### Positive Observations
- [Good practices noticed]
- [Well-implemented features]
- [Clean code examples]

### Code Suggestions
For significant issues, provide before/after examples:

**Issue**: [Description]
**File**: `[path/to/file.ext]:[line]`

Before:
```
[problematic code]
```

After:
```
[suggested fix]
```

### Test Coverage Analysis
| Changed File | Test File | Coverage | Status |
|--------------|-----------|----------|--------|
| [source] | [test] | [%] | ✅/⚠️/❌ |

### Action Items Checklist
- [ ] [Required change 1]
- [ ] [Required change 2]
- [ ] [Suggested improvement 1]

### Follow-up Recommendations
- Future PRs or technical debt items
- Monitoring suggestions
- Documentation needs

---

# Review Guidelines

## Efficiency Tips
- Start with high-risk files (auth, payments, data access)
- Check test files alongside source files
- Use file categorization to prioritize effort
- Skip generated/vendored files

## Tone & Approach
- Be constructive and specific
- Explain the "why" behind suggestions
- Acknowledge good work
- Distinguish between blockers and suggestions
- Use "Consider..." for optional improvements
- Use "Must..." for required changes
