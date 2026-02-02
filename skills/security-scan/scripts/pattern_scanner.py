#!/usr/bin/env python3
"""
Security Pattern Scanner — automated first-pass vulnerability detection.

Searches a codebase for high-signal patterns that indicate potential security vulnerabilities.
Outputs findings with file paths and line numbers for manual verification.

Usage:
    python3 pattern_scanner.py <TARGET_DIR> [--lang <LANG>] [--output json|text] [--exclude <PATTERN>]

Examples:
    python3 pattern_scanner.py ./src
    python3 pattern_scanner.py ./src --lang python --output json
    python3 pattern_scanner.py ./src --exclude "node_modules|vendor|\\.min\\.js"
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Optional

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    rule_id: str
    title: str
    severity: str          # CRITICAL, HIGH, MEDIUM, LOW, INFO
    owasp: str             # A01–A10
    cwe: str               # CWE-XXX
    file: str
    line: int
    matched_text: str
    description: str
    category: str          # grouping label

@dataclass
class Rule:
    rule_id: str
    title: str
    severity: str
    owasp: str
    cwe: str
    category: str
    description: str
    pattern: str           # regex pattern
    languages: list        # file extensions to search (empty = all)
    exclude_pattern: str = ""  # regex to exclude false positives

# ---------------------------------------------------------------------------
# Rule definitions
# ---------------------------------------------------------------------------

RULES: list[Rule] = [
    # --- A02: Cryptographic Failures — Hardcoded Secrets ---
    Rule("SEC-001", "Hardcoded Password", "CRITICAL", "A02", "CWE-798",
         "Hardcoded Secrets",
         "Password appears to be hardcoded in source code.",
         r"""(?i)(?:password|passwd|pwd)\s*[:=]\s*["'][^"']{4,}["']""",
         [], r"(?i)example|placeholder|test|dummy|changeme|xxx|\.env\.example"),
    Rule("SEC-002", "Hardcoded API Key or Token", "CRITICAL", "A02", "CWE-798",
         "Hardcoded Secrets",
         "API key or token appears to be hardcoded in source code.",
         r"""(?i)(?:api[_-]?key|api[_-]?secret|auth[_-]?token|access[_-]?token|secret[_-]?key|private[_-]?key)\s*[:=]\s*["'][A-Za-z0-9+/=_\-]{16,}["']""",
         [], r"(?i)example|placeholder|test|dummy|xxx|your[_-]"),
    Rule("SEC-003", "AWS Credentials in Source", "CRITICAL", "A02", "CWE-798",
         "Hardcoded Secrets",
         "AWS access key or secret key found in source code.",
         r"""(?:AKIA[0-9A-Z]{16}|(?i)aws_secret_access_key\s*[:=]\s*["'][^"']{20,}["'])""",
         []),
    Rule("SEC-004", "Private Key in Source", "CRITICAL", "A02", "CWE-321",
         "Hardcoded Secrets",
         "Private key material found in source code.",
         r"""-----BEGIN\s(?:RSA\s)?PRIVATE KEY-----""",
         []),

    # --- A02: Weak Cryptography ---
    Rule("SEC-010", "Weak Hash Algorithm (MD5)", "HIGH", "A02", "CWE-327",
         "Weak Cryptography",
         "MD5 is cryptographically broken and should not be used for security purposes.",
         r"""(?i)(?:hashlib\.md5|md5\(|MD5\.Create|MessageDigest\.getInstance\s*\(\s*["']MD5|crypto\.createHash\s*\(\s*["']md5)""",
         []),
    Rule("SEC-011", "Weak Hash Algorithm (SHA1)", "MEDIUM", "A02", "CWE-327",
         "Weak Cryptography",
         "SHA-1 is deprecated for security use. Use SHA-256 or stronger.",
         r"""(?i)(?:hashlib\.sha1|sha1\(|SHA1\.Create|MessageDigest\.getInstance\s*\(\s*["']SHA-?1|crypto\.createHash\s*\(\s*["']sha1)""",
         []),
    Rule("SEC-012", "Insecure Cipher (DES/RC4/ECB)", "HIGH", "A02", "CWE-327",
         "Weak Cryptography",
         "DES, RC4, and ECB mode are insecure encryption methods.",
         r"""(?i)(?:DES/|/ECB/|RC4|Blowfish|DESede|Cipher\.getInstance\s*\(\s*["']DES|AES/ECB)""",
         []),
    Rule("SEC-013", "TLS Verification Disabled", "HIGH", "A02", "CWE-295",
         "Weak Cryptography",
         "TLS certificate verification is disabled, allowing MITM attacks.",
         r"""(?i)(?:verify\s*=\s*False|verify_ssl\s*=\s*False|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*["']0|InsecureSkipVerify\s*:\s*true|CURLOPT_SSL_VERIFYPEER\s*,\s*(?:false|0))""",
         []),

    # --- A03: Injection — SQL ---
    Rule("SEC-020", "Potential SQL Injection (String Concatenation)", "CRITICAL", "A03", "CWE-89",
         "SQL Injection",
         "SQL query appears to be constructed via string concatenation with variables.",
         r"""(?:execute|query|prepare|cursor\.execute|\.query)\s*\(\s*(?:f["']|["'].*?["']\s*(?:\+|%|\.\s*format))""",
         [".py", ".js", ".ts", ".java", ".php", ".rb", ".go", ".cs"]),
    Rule("SEC-021", "SQL Injection (Go fmt.Sprintf)", "CRITICAL", "A03", "CWE-89",
         "SQL Injection",
         "SQL query constructed with fmt.Sprintf is vulnerable to injection.",
         r"""fmt\.Sprintf\s*\(\s*["'](?:SELECT|INSERT|UPDATE|DELETE|DROP|ALTER)\b""",
         [".go"]),

    # --- A03: Injection — Command ---
    Rule("SEC-030", "Command Injection (Python os.system)", "CRITICAL", "A03", "CWE-78",
         "Command Injection",
         "os.system() executes shell commands and is vulnerable to injection.",
         r"""os\.system\s*\(""",
         [".py"]),
    Rule("SEC-031", "Command Injection (subprocess shell=True)", "HIGH", "A03", "CWE-78",
         "Command Injection",
         "subprocess with shell=True is vulnerable to command injection.",
         r"""subprocess\.(?:call|run|Popen|check_output|check_call)\s*\([^)]*shell\s*=\s*True""",
         [".py"]),
    Rule("SEC-032", "Command Injection (child_process.exec)", "HIGH", "A03", "CWE-78",
         "Command Injection",
         "child_process.exec passes input through a shell; use execFile instead.",
         r"""(?:child_process\.exec|exec)\s*\(""",
         [".js", ".ts"], r"(?:execFile|execSync\s*\(\s*[\"'][^\"']*[\"']\s*\))"),
    Rule("SEC-033", "Command Injection (Runtime.exec)", "HIGH", "A03", "CWE-78",
         "Command Injection",
         "Runtime.exec with string argument is vulnerable to command injection.",
         r"""Runtime\.getRuntime\s*\(\s*\)\.exec\s*\(""",
         [".java"]),

    # --- A03: Injection — Code ---
    Rule("SEC-040", "Code Injection (eval)", "HIGH", "A03", "CWE-94",
         "Code Injection",
         "eval() executes arbitrary code and is dangerous with any user input.",
         r"""\beval\s*\(""",
         [".py", ".js", ".ts", ".rb", ".php"],
         r"(?i)(?:eslint|jshint|noinspection|# noqa)"),
    Rule("SEC-041", "Code Injection (exec in Python)", "HIGH", "A03", "CWE-94",
         "Code Injection",
         "exec() executes arbitrary Python code.",
         r"""\bexec\s*\(""",
         [".py"]),

    # --- A03: Injection — XSS ---
    Rule("SEC-050", "XSS via innerHTML", "MEDIUM", "A03", "CWE-79",
         "Cross-Site Scripting",
         "innerHTML assignment can introduce XSS if value contains user input.",
         r"""\.innerHTML\s*=""",
         [".js", ".ts", ".jsx", ".tsx", ".vue"]),
    Rule("SEC-051", "XSS via dangerouslySetInnerHTML", "MEDIUM", "A03", "CWE-79",
         "Cross-Site Scripting",
         "dangerouslySetInnerHTML bypasses React's XSS protection.",
         r"""dangerouslySetInnerHTML""",
         [".js", ".ts", ".jsx", ".tsx"]),
    Rule("SEC-052", "XSS via document.write", "MEDIUM", "A03", "CWE-79",
         "Cross-Site Scripting",
         "document.write can introduce XSS vulnerabilities.",
         r"""document\.write\s*\(""",
         [".js", ".ts", ".html"]),

    # --- A03: Injection — Template ---
    Rule("SEC-060", "Server-Side Template Injection (Python)", "HIGH", "A03", "CWE-1336",
         "Template Injection",
         "render_template_string with user input enables SSTI.",
         r"""render_template_string\s*\(""",
         [".py"]),
    Rule("SEC-061", "Jinja2 Autoescape Disabled", "MEDIUM", "A03", "CWE-79",
         "Template Injection",
         "Jinja2 Environment with autoescape disabled allows XSS.",
         r"""Environment\s*\([^)]*autoescape\s*=\s*False""",
         [".py"]),

    # --- A05: Security Misconfiguration ---
    Rule("SEC-070", "Debug Mode Enabled", "MEDIUM", "A05", "CWE-489",
         "Security Misconfiguration",
         "Debug mode should be disabled in production deployments.",
         r"""(?i)(?:DEBUG\s*=\s*True|debug\s*:\s*true|app\.debug\s*=\s*True|NODE_ENV\s*[:=]\s*["']?development)""",
         [".py", ".js", ".ts", ".env", ".yaml", ".yml", ".json", ".toml"]),
    Rule("SEC-071", "Stack Trace Exposure", "LOW", "A05", "CWE-209",
         "Security Misconfiguration",
         "Stack traces may expose internal details to attackers.",
         r"""(?i)(?:traceback\.print_exc|e\.printStackTrace|\.stack\s|print_r\s*\(\s*\$e|full_exception_chain)""",
         [".py", ".java", ".php", ".js", ".ts"]),

    # --- A07: Authentication Failures ---
    Rule("SEC-080", "Insecure Randomness", "MEDIUM", "A07", "CWE-330",
         "Authentication Failures",
         "Math.random() / random.random() are not cryptographically secure for tokens.",
         r"""(?:Math\.random\s*\(\)|random\.random\s*\(\)|random\.randint\s*\(|rand\(\))""",
         [".py", ".js", ".ts", ".rb", ".php"]),

    # --- A08: Integrity Failures — Deserialization ---
    Rule("SEC-090", "Insecure Deserialization (pickle)", "CRITICAL", "A08", "CWE-502",
         "Insecure Deserialization",
         "pickle.loads on untrusted data can lead to arbitrary code execution.",
         r"""pickle\.loads?\s*\(""",
         [".py"]),
    Rule("SEC-091", "Insecure Deserialization (YAML unsafe)", "HIGH", "A08", "CWE-502",
         "Insecure Deserialization",
         "yaml.load without SafeLoader can execute arbitrary Python objects.",
         r"""yaml\.(?:load|unsafe_load)\s*\(""",
         [".py"], r"Loader\s*=\s*(?:Safe|Base)Loader"),
    Rule("SEC-092", "Insecure Deserialization (Java ObjectInputStream)", "HIGH", "A08", "CWE-502",
         "Insecure Deserialization",
         "ObjectInputStream.readObject() on untrusted data is dangerous.",
         r"""ObjectInputStream.*readObject\s*\(|new\s+ObjectInputStream""",
         [".java"]),
    Rule("SEC-093", "Insecure Deserialization (PHP unserialize)", "HIGH", "A08", "CWE-502",
         "Insecure Deserialization",
         "unserialize() on untrusted data can lead to object injection.",
         r"""unserialize\s*\(""",
         [".php"]),
    Rule("SEC-094", "Insecure Deserialization (.NET BinaryFormatter)", "HIGH", "A08", "CWE-502",
         "Insecure Deserialization",
         "BinaryFormatter.Deserialize on untrusted data is dangerous.",
         r"""BinaryFormatter.*Deserialize|new\s+BinaryFormatter""",
         [".cs"]),

    # --- A10: SSRF ---
    Rule("SEC-100", "Potential SSRF (Python requests)", "MEDIUM", "A10", "CWE-918",
         "SSRF",
         "Server-side HTTP request with potentially user-controlled URL.",
         r"""requests\.(?:get|post|put|delete|patch|head)\s*\(""",
         [".py"]),
    Rule("SEC-101", "Potential SSRF (Node fetch/axios)", "MEDIUM", "A10", "CWE-918",
         "SSRF",
         "Server-side HTTP request with potentially user-controlled URL.",
         r"""(?:fetch|axios\.(?:get|post|put|delete|patch))\s*\(""",
         [".js", ".ts"]),
    Rule("SEC-102", "Potential SSRF (Java)", "MEDIUM", "A10", "CWE-918",
         "SSRF",
         "Server-side HTTP request with potentially user-controlled URL.",
         r"""(?:URL\s*\(|HttpURLConnection|HttpClient\.send|WebClient)""",
         [".java"]),
    Rule("SEC-103", "Potential SSRF (Go)", "MEDIUM", "A10", "CWE-918",
         "SSRF",
         "Server-side HTTP request with potentially user-controlled URL.",
         r"""http\.(?:Get|Post|Head)\s*\(""",
         [".go"]),

    # --- A01: Broken Access Control — CORS ---
    Rule("SEC-110", "Permissive CORS Configuration", "MEDIUM", "A01", "CWE-942",
         "Access Control",
         "CORS wildcard (*) may allow unintended cross-origin access.",
         r"""(?i)(?:Access-Control-Allow-Origin\s*[:=]\s*["']\*|cors\(\s*\{[^}]*origin\s*:\s*(?:true|["']\*))""",
         []),

    # --- A04: Insecure Design ---
    Rule("SEC-120", "Missing CSRF Token Check", "MEDIUM", "A04", "CWE-352",
         "Insecure Design",
         "POST/PUT/DELETE endpoint without apparent CSRF protection.",
         r"""(?i)(?:@csrf_exempt|csrf\s*:\s*false|disable.*csrf)""",
         [".py", ".js", ".ts", ".java", ".php", ".rb"]),

    # --- File operations ---
    Rule("SEC-130", "Path Traversal Risk", "MEDIUM", "A01", "CWE-22",
         "Path Traversal",
         "File operation with potentially user-controlled path.",
         r"""(?:open\s*\(.*(?:request|req|params|args|input)|fs\.(?:readFile|writeFile|createReadStream)\s*\(.*(?:req|params|query))""",
         [".py", ".js", ".ts"]),

    # --- Logging ---
    Rule("SEC-140", "Sensitive Data in Logs", "MEDIUM", "A09", "CWE-532",
         "Logging Failures",
         "Logging statement that may include sensitive data (password, token, secret).",
         r"""(?i)(?:log(?:ger)?\.(?:info|warn|debug|error|log)|console\.log|print)\s*\([^)]*(?:password|token|secret|api.key|credit.card|ssn)""",
         []),
]

# ---------------------------------------------------------------------------
# File extension mapping
# ---------------------------------------------------------------------------

LANG_EXTENSIONS: dict[str, list[str]] = {
    "python":     [".py"],
    "javascript": [".js", ".jsx", ".mjs", ".cjs"],
    "typescript": [".ts", ".tsx"],
    "java":       [".java"],
    "go":         [".go"],
    "ruby":       [".rb", ".erb"],
    "php":        [".php"],
    "csharp":     [".cs"],
    "c":          [".c", ".h"],
    "cpp":        [".cpp", ".cc", ".cxx", ".hpp", ".hxx", ".h"],
    "rust":       [".rs"],
    "swift":      [".swift"],
    "kotlin":     [".kt", ".kts"],
}

BINARY_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".woff", ".woff2", ".ttf",
                     ".eot", ".otf", ".zip", ".gz", ".tar", ".jar", ".war", ".class",
                     ".pyc", ".pyo", ".o", ".so", ".dll", ".exe", ".pdf", ".mp3", ".mp4"}

SKIP_DIRS = {"node_modules", ".git", ".svn", "__pycache__", ".tox", ".venv", "venv",
             "vendor", "dist", "build", ".next", ".nuxt", "target", "bin", "obj",
             ".idea", ".vscode", ".gradle", ".m2"}

# ---------------------------------------------------------------------------
# Scanner logic
# ---------------------------------------------------------------------------

def should_skip_dir(dirname: str) -> bool:
    return dirname in SKIP_DIRS or dirname.startswith(".")

def should_scan_file(filepath: Path, lang_filter: Optional[str]) -> bool:
    ext = filepath.suffix.lower()
    if ext in BINARY_EXTENSIONS:
        return False
    if lang_filter:
        allowed = LANG_EXTENSIONS.get(lang_filter, [])
        return ext in allowed
    return True

def rule_applies(rule: Rule, filepath: Path) -> bool:
    if not rule.languages:
        return True
    return filepath.suffix.lower() in rule.languages

def scan_file(filepath: Path, rules: list[Rule]) -> list[Finding]:
    findings = []
    try:
        content = filepath.read_text(errors="replace")
    except (PermissionError, OSError):
        return findings

    lines = content.split("\n")
    for rule in rules:
        if not rule_applies(rule, filepath):
            continue
        try:
            pattern = re.compile(rule.pattern)
        except re.error:
            continue
        for i, line in enumerate(lines, start=1):
            if pattern.search(line):
                # Check exclusion pattern
                if rule.exclude_pattern:
                    try:
                        if re.search(rule.exclude_pattern, line):
                            continue
                    except re.error:
                        pass
                findings.append(Finding(
                    rule_id=rule.rule_id,
                    title=rule.title,
                    severity=rule.severity,
                    owasp=rule.owasp,
                    cwe=rule.cwe,
                    file=str(filepath),
                    line=i,
                    matched_text=line.strip()[:200],
                    description=rule.description,
                    category=rule.category,
                ))
    return findings

def scan_directory(target: str, lang_filter: Optional[str],
                   exclude_pattern: Optional[str]) -> list[Finding]:
    target_path = Path(target).resolve()
    if not target_path.exists():
        print(f"Error: target '{target}' does not exist.", file=sys.stderr)
        sys.exit(1)

    exclude_re = re.compile(exclude_pattern) if exclude_pattern else None
    all_findings: list[Finding] = []

    if target_path.is_file():
        return scan_file(target_path, RULES)

    for dirpath, dirnames, filenames in os.walk(target_path):
        # Skip irrelevant directories
        dirnames[:] = [d for d in dirnames if not should_skip_dir(d)]

        for filename in filenames:
            filepath = Path(dirpath) / filename
            rel_path = filepath.relative_to(target_path)

            if exclude_re and exclude_re.search(str(rel_path)):
                continue
            if not should_scan_file(filepath, lang_filter):
                continue

            findings = scan_file(filepath, RULES)
            # Store relative paths for cleaner output
            for f in findings:
                f.file = str(rel_path)
            all_findings.extend(findings)

    return all_findings

# ---------------------------------------------------------------------------
# Output formatting
# ---------------------------------------------------------------------------

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}

def format_text(findings: list[Finding]) -> str:
    if not findings:
        return "✅ No potential vulnerabilities detected by automated pattern scan.\n"

    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 5), f.rule_id, f.file, f.line))

    # Summary
    counts = {}
    for f in findings:
        counts[f.severity] = counts.get(f.severity, 0) + 1
    summary_parts = [f"{sev}: {counts.get(sev, 0)}"
                     for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]
                     if counts.get(sev, 0) > 0]

    lines = [
        f"🔍 Pattern Scan Results — {len(findings)} potential finding(s)",
        f"   Severity: {', '.join(summary_parts)}",
        "",
        "⚠️  These are candidates only. Each must be manually verified.",
        "=" * 78,
        "",
    ]

    current_severity = None
    for f in findings:
        if f.severity != current_severity:
            current_severity = f.severity
            lines.append(f"--- {f.severity} ---\n")
        lines.append(
            f"[{f.rule_id}] {f.title}\n"
            f"  Severity: {f.severity} | OWASP: {f.owasp} | {f.cwe}\n"
            f"  File:     {f.file}:{f.line}\n"
            f"  Match:    {f.matched_text}\n"
            f"  Detail:   {f.description}\n"
        )
    return "\n".join(lines)

def format_json(findings: list[Finding]) -> str:
    findings.sort(key=lambda f: (SEVERITY_ORDER.get(f.severity, 5), f.rule_id, f.file, f.line))
    return json.dumps({
        "total": len(findings),
        "counts": {sev: sum(1 for f in findings if f.severity == sev)
                   for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"]},
        "findings": [asdict(f) for f in findings],
    }, indent=2)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Security pattern scanner — first-pass automated vulnerability detection.")
    parser.add_argument("target", help="Directory or file to scan")
    parser.add_argument("--lang", choices=list(LANG_EXTENSIONS.keys()),
                        help="Filter to a specific language")
    parser.add_argument("--output", choices=["text", "json"], default="text",
                        help="Output format (default: text)")
    parser.add_argument("--exclude", type=str, default=None,
                        help="Regex pattern to exclude files/directories")
    args = parser.parse_args()

    findings = scan_directory(args.target, args.lang, args.exclude)

    if args.output == "json":
        print(format_json(findings))
    else:
        print(format_text(findings))

if __name__ == "__main__":
    main()
