# Security Vulnerability Scanner Command
# Usage: Scan codebase for security vulnerabilities: <DIRECTORY|FILE_PATTERN>

# Parse scan target
Set SCAN_TARGET to $Arguments
Validate that SCAN_TARGET is provided, otherwise error "Please provide directory or file pattern to scan"

# Step 1: Security Analysis
## Comprehensive security scanning
- OWASP Top 10 vulnerability detection
- Input validation and sanitization review
- Authentication and authorization flaws
- Cryptographic implementation analysis
- Dependency vulnerability scanning
- Configuration security assessment

# Step 2: Categorize Security Issues
## CRITICAL (Immediate security risk)
- SQL injection vulnerabilities
- Cross-site scripting (XSS) flaws
- Authentication bypasses
- Sensitive data exposure

## HIGH (Significant security concern)
- Insecure direct object references
- Security misconfigurations
- Known vulnerable dependencies
- Insufficient logging and monitoring

# Step 3: Remediation Plan
- Provide specific code fixes
- Suggest security best practices
- Include secure coding examples
- Recommend security testing approaches
