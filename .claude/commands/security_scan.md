# Security Vulnerability Scanner Command
# Usage: Scan codebase for security vulnerabilities: <DIRECTORY|FILE_PATTERN>

# Parse scan target
Set SCAN_TARGET to $Arguments
Validate that SCAN_TARGET is provided, otherwise error "Please provide directory or file pattern to scan"

# Step 1: Initial Security Scan
Execute these scans in parallel:
- Search for hardcoded secrets (API keys, passwords, tokens)
- Identify SQL query construction patterns
- Find user input handling points
- Locate authentication/authorization code
- Detect cryptographic operations
- Find file I/O operations
- Identify network/HTTP operations
- Search for serialization/deserialization
- Check dependency manifests for known vulnerabilities

# Step 2: OWASP Top 10 Analysis

### A01:2021 - Broken Access Control
- Missing authorization checks on endpoints
- Insecure direct object references (IDOR)
- Missing function-level access control
- CORS misconfiguration
- Path traversal vulnerabilities

### A02:2021 - Cryptographic Failures
- Hardcoded secrets and credentials
- Weak encryption algorithms (MD5, SHA1, DES)
- Missing encryption for sensitive data
- Improper key management
- HTTP instead of HTTPS

### A03:2021 - Injection
- SQL injection (string concatenation in queries)
- NoSQL injection
- Command injection (shell command construction)
- LDAP injection
- XPath injection
- Template injection

### A04:2021 - Insecure Design
- Missing rate limiting
- Lack of input validation
- Missing security headers
- Insufficient logging
- Missing CSRF protection

### A05:2021 - Security Misconfiguration
- Debug mode enabled in production
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Verbose error messages exposing internals

### A06:2021 - Vulnerable Components
- Outdated dependencies with known CVEs
- Unmaintained libraries
- Components with security advisories

### A07:2021 - Authentication Failures
- Weak password policies
- Missing brute force protection
- Session fixation
- Insecure session management
- Missing MFA where required

### A08:2021 - Software and Data Integrity Failures
- Insecure deserialization
- Missing integrity checks on updates
- Unsigned/unverified artifacts
- CI/CD pipeline vulnerabilities

### A09:2021 - Security Logging Failures
- Missing authentication event logging
- Missing access control failure logging
- Logs missing context for forensics
- Log injection vulnerabilities

### A10:2021 - Server-Side Request Forgery (SSRF)
- Unvalidated URL fetching
- Missing allowlist for external requests
- Internal service exposure

# Step 3: Language-Specific Checks

### JavaScript/TypeScript
- eval() and Function() usage
- innerHTML and dangerouslySetInnerHTML
- Prototype pollution
- Regex DoS (ReDoS)

### Python
- pickle/yaml deserialization
- exec() and eval() usage
- subprocess with shell=True
- Jinja2 autoescape disabled

### Java
- XMLDecoder usage
- Runtime.exec() with user input
- ObjectInputStream deserialization
- SQL string concatenation

### Go
- Template injection
- Race conditions
- Unvalidated file paths

# Step 4: Categorize Security Issues

## CRITICAL (Immediate security risk - P0)
- Remote code execution (RCE) vulnerabilities
- SQL injection with database access
- Authentication bypass
- Hardcoded production credentials
- Known CVEs with active exploits

## HIGH (Significant security concern - P1)
- Cross-site scripting (XSS)
- Insecure direct object references
- Sensitive data exposure
- Missing encryption for PII
- Session management flaws

## MEDIUM (Security weakness - P2)
- Security misconfigurations
- Missing security headers
- Verbose error messages
- Outdated dependencies (no active exploits)
- Insufficient logging

## LOW (Hardening opportunity - P3)
- Informational findings
- Best practice deviations
- Minor configuration improvements
- Documentation gaps

# Step 5: Generate Output

## Output Format

### Security Scan Summary
**Target**: [Directory/Pattern scanned]
**Scan Date**: [Date]
**Risk Level**: [CRITICAL/HIGH/MEDIUM/LOW]
**Total Findings**: [Count by severity]

### Executive Summary
[2-3 paragraphs on overall security posture, key risks, and immediate actions needed]

### Vulnerability Statistics
| Severity | Count | OWASP Categories Affected |
|----------|-------|---------------------------|
| CRITICAL | [X] | [A01, A03, ...] |
| HIGH | [X] | [...] |
| MEDIUM | [X] | [...] |
| LOW | [X] | [...] |

### Findings by OWASP Category
| OWASP ID | Category | Findings | Highest Severity |
|----------|----------|----------|------------------|
| A01 | Broken Access Control | [X] | [CRIT/HIGH/MED/LOW] |
| A02 | Cryptographic Failures | [X] | [...] |
| ... | ... | ... | ... |

### Detailed Findings

#### [S1] [Vulnerability Title]
- **Severity**: [CRITICAL/HIGH/MEDIUM/LOW]
- **OWASP Category**: [A01-A10]
- **CWE**: [CWE-XXX if applicable]
- **Location**: `[file:line]`
- **Description**: [What the vulnerability is]
- **Attack Scenario**: [How it could be exploited]

**Vulnerable Code**:
```
[code snippet showing vulnerability]
```

**Secure Fix**:
```
[remediated code]
```

**Remediation Steps**:
1. [Step-by-step fix instructions]

**References**:
- [Link to OWASP documentation]
- [Link to CWE entry]

### Dependency Vulnerabilities
| Package | Current | Vulnerable | Fixed In | CVE | Severity |
|---------|---------|------------|----------|-----|----------|
| [pkg] | [version] | [Yes/No] | [version] | [CVE-XXXX] | [CRIT/HIGH/...] |

### Security Headers Check
| Header | Present | Recommended Value | Status |
|--------|---------|-------------------|--------|
| Content-Security-Policy | [Yes/No] | [value] | [OK/MISSING] |
| X-Frame-Options | [Yes/No] | DENY | [OK/MISSING] |
| X-Content-Type-Options | [Yes/No] | nosniff | [OK/MISSING] |
| Strict-Transport-Security | [Yes/No] | max-age=31536000 | [OK/MISSING] |

### Remediation Roadmap
1. **Immediate (24-48 hours)**: [CRITICAL findings]
2. **Short-term (1 week)**: [HIGH findings]
3. **Medium-term (1 month)**: [MEDIUM findings]
4. **Ongoing**: [LOW findings and hardening]

### Security Testing Recommendations
- Penetration testing scope
- DAST tools to run
- SAST integration suggestions
- Security code review areas

### Compliance Notes
[If applicable: GDPR, HIPAA, PCI-DSS, SOC2 implications]
