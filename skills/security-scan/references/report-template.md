# Security Assessment Report Template

Use this template to generate the final report. Fill in every section. Omit subsections only
if the category is genuinely not applicable to the target (note "N/A — [reason]").

---

```markdown
# Security Assessment Report

## 1. Metadata

| Field | Value |
|-------|-------|
| **Target** | [directory or repository name] |
| **Scope** | [files/directories reviewed; any exclusions] |
| **Assessment Date** | [YYYY-MM-DD] |
| **Assessment Type** | Static Code Review (Manual + Automated Pattern Scan) |
| **Assessor** | Claude (AI-assisted security review) |
| **Languages** | [detected languages] |
| **Frameworks** | [detected frameworks] |

---

## 2. Executive Summary

[2–4 paragraphs covering:
- Overall security posture (strong / moderate / weak / critical)
- Key risk areas identified
- Top 3–5 attack scenarios specific to this application
- Immediate actions recommended

Keep this concise and decision-oriented — a CISO should be able to read only this section
and understand the risk level and next steps.]

---

## 3. Findings Summary

### 3.1 Severity Distribution

| Severity | Count | Immediate Action Required |
|----------|------:|---------------------------|
| 🔴 CRITICAL | [X] | Yes — within 24 hours |
| 🟠 HIGH | [X] | Yes — within 1 week |
| 🟡 MEDIUM | [X] | Planned — within 1 month |
| 🔵 LOW | [X] | Backlog |
| ⚪ INFO | [X] | No |
| **Total** | **[X]** | |

### 3.2 OWASP Top 10 Coverage

| OWASP ID | Category | Findings | Highest Severity | Status |
|----------|----------|------:|----------|--------|
| A01 | Broken Access Control | [X] | [CRIT/HIGH/MED/LOW] | [Reviewed / N/A] |
| A02 | Cryptographic Failures | [X] | [...] | [...] |
| A03 | Injection | [X] | [...] | [...] |
| A04 | Insecure Design | [X] | [...] | [...] |
| A05 | Security Misconfiguration | [X] | [...] | [...] |
| A06 | Vulnerable Components | [X] | [...] | [...] |
| A07 | Auth Failures | [X] | [...] | [...] |
| A08 | Integrity Failures | [X] | [...] | [...] |
| A09 | Logging Failures | [X] | [...] | [...] |
| A10 | SSRF | [X] | [...] | [...] |

---

## 4. Detailed Findings

[Sort findings by severity: CRITICAL first, then HIGH, MEDIUM, LOW, INFO.
Use the following template for each finding.]

### [VULN-001] [Vulnerability Title]

| Attribute | Value |
|-----------|-------|
| **Severity** | 🔴 CRITICAL / 🟠 HIGH / 🟡 MEDIUM / 🔵 LOW / ⚪ INFO |
| **CVSS Score** | [X.X] (estimate; note if approximate) |
| **OWASP Category** | [A01–A10]: [Category Name] |
| **CWE** | [CWE-XXX]: [CWE Name] |
| **Location** | `[file:line]` |
| **Status** | Confirmed / Potential (needs runtime verification) |

**Description**

[What the vulnerability is. Be precise — state what is wrong and why it is a security issue.]

**Evidence**

```[language]
// file: [relative/path/to/file.ext], lines [N]–[M]
[vulnerable code snippet — include enough context to understand the issue]
```

**Attack Scenario**

[Step-by-step description of how an attacker would exploit this vulnerability.
Include example payloads where applicable.]

**Remediation**

```[language]
// Secure implementation
[fixed code snippet]
```

**Remediation Steps:**
1. [Specific action to take]
2. [Additional steps if needed]

**References:**
- [CWE link: https://cwe.mitre.org/data/definitions/XXX.html]
- [OWASP link if applicable]
- [Relevant documentation or advisory]

---

[Repeat for each finding: VULN-002, VULN-003, etc.]

---

## 5. Dependency Vulnerabilities

[If dependency manifests were found, list known-vulnerable or outdated packages.]

| Package | Current Version | Known Vulnerable | Fixed In | CVE(s) | Severity |
|---------|----------------|:---:|---------|--------|----------|
| [package-name] | [X.Y.Z] | Yes / No | [X.Y.Z] | [CVE-YYYY-NNNNN] | [CRIT/HIGH/...] |

[If no manifests found or no vulnerabilities identified, state: "No dependency manifests found
in scope" or "No known vulnerabilities identified in current dependency versions."]

---

## 6. Remediation Roadmap

### Immediate (0–48 hours)
- [CRITICAL findings — list VULN-IDs and one-line summaries]

### Short-term (1–2 weeks)
- [HIGH findings]

### Medium-term (1–3 months)
- [MEDIUM findings]
- [Dependency upgrades]

### Ongoing
- [LOW / INFO findings]
- [Process improvements: SAST integration, dependency scanning in CI, security training]

---

## 7. Methodology

This assessment was conducted as a **static code review** combining automated pattern
detection with manual analysis.

**In scope:** [describe what was reviewed]

**Out of scope:** Dynamic application testing (DAST), penetration testing, infrastructure
review, social engineering, physical security.

**Limitations:**
- Static analysis cannot detect all runtime vulnerabilities (e.g., race conditions that
  depend on deployment configuration, business logic flaws requiring application state).
- Dependency vulnerability assessment was based on version comparison against known CVEs
  at the time of review; new vulnerabilities may be disclosed after this assessment.
- Without runtime access, some findings are marked as "Potential" where exploitability
  depends on configuration or deployment context.

**Tools used:** Manual code review, automated regex-based pattern scanning, dependency
manifest analysis.

**Standards referenced:** OWASP Top 10 (2021), CWE/SANS Top 25, NIST SP 800-63B
(authentication), CVSS v3.1 (severity scoring).

