# Code Review Command for Pull Request Analysis
# Usage: Review the code and unit tests in the pull request: <PR_NUMBER|PR_URL|BRANCH_NAME>

# Parse and validate the pull request identifier
Set PR_IDENTIFIER to $Arguments
Validate that PR_IDENTIFIER is provided, otherwise error "Please provide a pull request number, URL, or branch name"

# Step 1: Gather Context
## Fetch PR information and changes
- If PR_IDENTIFIER is a number, use: git fetch origin pull/${PR_IDENTIFIER}/head:pr-${PR_IDENTIFIER}
- If PR_IDENTIFIER is a branch, use: git fetch origin ${PR_IDENTIFIER}
- Get the diff: git diff origin/main...${PR_IDENTIFIER}
- Get commit history: git log --oneline origin/main...${PR_IDENTIFIER}
- List changed files: git diff --name-status origin/main...${PR_IDENTIFIER}

# Step 2: Comprehensive Code Review
Perform a thorough analysis of the pull request covering:

## 2.1 Code Quality & Design
- Analyze architectural decisions and overall design approach
- Evaluate adherence to SOLID principles (Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion)
- Identify opportunities to apply Gang of Four design patterns where appropriate
- Check for code duplication and suggest DRY improvements
- Review naming conventions and code readability

## 2.2 Implementation Review
- Identify potential bugs, edge cases, and error conditions
- Check error handling and exception management
- Review resource management (memory leaks, file handles, connections)
- Validate input sanitization and data validation
- Assess algorithm efficiency and data structure choices

## 2.3 Security Analysis
- Check for common security vulnerabilities (injection, XSS, CSRF, etc.)
- Review authentication and authorization logic
- Identify sensitive data exposure risks
- Validate cryptographic implementations
- Check for dependency vulnerabilities

## 2.4 Performance Considerations
- Identify potential performance bottlenecks
- Review database queries for N+1 problems
- Check for unnecessary loops or computations
- Evaluate caching opportunities
- Consider scalability implications

## 2.5 Test Coverage Analysis
- Calculate test coverage percentage for new/changed code
- Identify untested code paths and edge cases
- Review test quality and assertions
- Check for test anti-patterns (e.g., testing implementation details)
- Suggest additional test scenarios for critical paths
- Verify integration and end-to-end test coverage

## 2.6 Documentation & Maintainability
- Review inline comments and documentation
- Check if public APIs are properly documented
- Verify README updates for new features
- Assess code complexity and suggest simplifications
- Review logging and debugging capabilities

# Step 3: Categorize and Prioritize Findings
Organize all findings into the following priority levels:

## CRITICAL (Must fix before merge)
- Security vulnerabilities
- Data loss risks
- Breaking changes without migration path
- Severe performance regressions
- Failing tests or broken functionality

## HIGH (Should fix before merge)
- Significant bugs or logic errors
- Missing critical test coverage
- Major design flaws
- Performance issues
- Non-backward compatible changes

## MEDIUM (Consider fixing)
- Code quality issues
- Missing non-critical tests
- Documentation gaps
- Minor performance improvements
- Refactoring opportunities

## LOW (Nice to have)
- Style inconsistencies
- Minor optimizations
- Additional test scenarios
- Code organization improvements
- Future enhancement suggestions

# Step 4: Generate Structured Output
Provide a comprehensive review in the following format:

## Executive Summary
- Brief overview of the PR's purpose and scope
- Overall assessment (Approve/Request Changes/Comment)
- Key risks or concerns

## Detailed Findings
[Organize by category and priority as defined above]

## Positive Aspects
- Well-implemented features or improvements
- Good practices observed

## Action Items
- Numbered list of required changes
- Suggested improvements with examples

## Code Examples
- Provide specific code snippets for suggested improvements
- Include "before" and "after" examples where helpful

# Step 5: Follow-up Recommendations
- Suggest follow-up PRs for larger refactoring
- Recommend monitoring or metrics to track
- Identify technical debt to address later

# Note: Focus on constructive feedback that helps improve the code while maintaining a collaborative tone
