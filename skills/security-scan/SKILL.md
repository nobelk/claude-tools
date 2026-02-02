---
name: security-scan
description: >
  Perform a rigorous, senior-engineer-grade security vulnerability assessment of a codebase.
  Use when the user asks to: scan code for security issues, perform a security review or audit,
  find vulnerabilities, check for OWASP Top 10 issues, assess security posture, review code for
  security best practices, check dependencies for CVEs, or any task involving security analysis
  of source code, configuration files, or infrastructure-as-code. Supports all major languages
  (JavaScript/TypeScript, Python, Java, Go, C/C++, Ruby, PHP, C#, Rust, Swift, Kotlin) and
  frameworks. Produces a structured report aligned with OWASP, CWE, and CVSS standards.
---

# Security Vulnerability Scanner

Perform a comprehensive security assessment following the methodology a senior security engineer
would use during a manual code audit, augmented by automated pattern detection.

## Workflow Overview

1. **Reconnaissance** — understand the codebase (languages, frameworks, architecture, dependencies)
2. **Automated pattern scan** — run `scripts/pattern_scanner.py` against the target
3. **Manual deep-dive** — analyze critical areas the script cannot reliably assess
4. **OWASP Top 10 analysis** — systematic review; see `references/owasp-top10.md`
5. **Language-specific checks** — see `references/language-checks.md`
6. **Dependency audit** — inspect manifests for known-vulnerable packages
7. **Threat modeling** — consider attack surface specific to the application
8. **Severity classification** — assign CVSS-aligned severity per finding
9. **Report generation** — produce structured report; see `references/report-template.md`

---

## Step 1: Reconnaissance

Before scanning, characterize the target to scope the review.

Determine:
- Primary languages and frameworks (inspect file extensions, imports, config files)
- Application type (web app, API, CLI, library, mobile, IaC)
- Entry points (HTTP routes, CLI args, message queues, cron jobs)
- Data stores (databases, caches, file storage, cloud services)
- Authentication / authorization model in use
- Deployment target (cloud provider, container, serverless, on-prem)
- Dependency manifests (`package.json`, `requirements.txt`, `go.mod`, `pom.xml`, `Gemfile`, `Cargo.toml`, `*.csproj`, etc.)

Use `find`, `grep`, and directory listing to build this picture quickly.

---

## Step 2: Automated Pattern Scan

Run the bundled scanner against the target directory:

```bash
python3 /path/to/security-scan/scripts/pattern_scanner.py <TARGET_DIR> [--lang <LANG>] [--output json|text]
```

The script searches for high-signal vulnerability patterns (hardcoded secrets, injection sinks, dangerous function calls, insecure configurations) and outputs findings with file paths and line numbers. Use its output as the starting evidence base; every finding must be manually verified in Step 3.

If the script is unavailable or the target requires deeper analysis, use `grep -rn` with patterns from `references/language-checks.md`.

---

## Step 3: Manual Deep-Dive

Focus manual analysis on areas automated scanning cannot reliably assess:

**Authentication & session management** — verify password hashing (bcrypt/argon2/scrypt, not MD5/SHA1), session token entropy, cookie flags (Secure, HttpOnly, SameSite), token expiration, MFA implementation.

**Authorization & access control** — trace every privileged endpoint; confirm authorization checks are present and correct. Look for IDOR by checking whether object lookups are scoped to the authenticated user. Verify role-based checks are applied server-side, not just in the UI.

**Input validation & output encoding** — trace user-controlled data from entry point to sink. Confirm parameterized queries (not string concatenation) for SQL. Confirm context-appropriate output encoding for HTML, JavaScript, URL, and CSS contexts. Check file upload handling (type validation, storage location, filename sanitization).

**Cryptography** — verify use of vetted libraries (not hand-rolled crypto), strong algorithms (AES-256-GCM, RSA-2048+, ECDSA P-256+, SHA-256+), proper IV/nonce handling, secure key storage (not in source), and TLS 1.2+ enforcement.

**Error handling & logging** — ensure stack traces and internal details are not exposed to users. Verify security-relevant events are logged (auth failures, access denied, input validation failures) with sufficient context for forensics but without logging sensitive data (passwords, tokens, PII).

**Business logic** — review workflows for race conditions, TOCTOU bugs, price/quantity manipulation, privilege escalation through state manipulation, and abuse of multi-step processes.

---

## Step 4: OWASP Top 10 Analysis

Read `references/owasp-top10.md` for the detailed checklist organized by OWASP 2021 category (A01–A10). Systematically evaluate each category against the codebase. Record which categories have findings and which are not applicable.

---

## Step 5: Language-Specific Checks

Read `references/language-checks.md` and apply the section(s) matching the target's languages. These contain language-idiomatic vulnerability patterns and dangerous API usage.

---

## Step 6: Dependency Audit

Inspect each dependency manifest found in Step 1:

- Extract package names and pinned versions.
- For well-known vulnerable packages, flag them (e.g., `lodash` < 4.17.21, `log4j` < 2.17.1).
- Note unpinned or floating version ranges that could pull vulnerable versions.
- Flag dependencies with no recent maintenance (>2 years since last release) as elevated risk.
- If internet access is available, cross-reference against known CVE databases.

---

## Step 7: Threat Modeling (Lightweight)

Based on Steps 1–6, identify the top 3–5 attack scenarios most relevant to this application:

- What is the most valuable asset an attacker would target? (user data, credentials, financial transactions, admin access)
- What is the most exposed attack surface? (public API, file upload, authentication flow)
- What would a skilled attacker try first given the findings so far?

Summarize these scenarios in the report's Executive Summary.

---

## Step 8: Severity Classification

Assign each finding a severity using this CVSS-aligned rubric:

| Severity | CVSS Range | Criteria |
|----------|-----------|----------|
| **CRITICAL** | 9.0–10.0 | Remotely exploitable with no/low privilege required, leads to full system compromise, data breach, or RCE. Active exploits may exist. |
| **HIGH** | 7.0–8.9 | Exploitable with some prerequisites, significant impact on confidentiality, integrity, or availability. |
| **MEDIUM** | 4.0–6.9 | Requires specific conditions or chained exploitation, moderate impact. |
| **LOW** | 0.1–3.9 | Minimal impact, defense-in-depth improvement, best-practice deviation. |
| **INFORMATIONAL** | 0.0 | Observation or recommendation with no direct exploitability. |

Each finding must include: a unique ID, title, severity, OWASP category (A01–A10), CWE ID, affected file(s) and line(s), description, evidence (code snippet), attack scenario, remediation with secure code example, and references.

---

## Step 9: Report Generation

Read `references/report-template.md` for the full report structure. Generate the report as a Markdown file in `/mnt/user-data/outputs/`. The report must include:

1. Metadata (target, date, scope, assessor)
2. Executive summary (security posture, key risks, top recommended actions)
3. Findings summary table (severity counts, OWASP distribution)
4. Detailed findings (sorted CRITICAL → LOW)
5. Dependency vulnerability table
6. Remediation roadmap (immediate / short-term / medium-term / ongoing)
7. Methodology note

Ensure the report is self-contained: another engineer should be able to reproduce and verify each finding using only the report.

---

## Key Principles

- **Evidence-based** — every finding must reference specific file(s) and line(s) with a code snippet. Never report a vulnerability without evidence.
- **Verify before reporting** — the automated scanner produces candidates; manually confirm exploitability before including in the report.
- **No false positives in final report** — if uncertain, note it as "Potential" with the caveat and lower the severity.
- **Actionable remediation** — every finding must include a concrete fix with a secure code example, not just "fix this."
- **Scope honesty** — clearly state what was and was not reviewed. A static review cannot find all runtime issues; note this in the methodology section.
