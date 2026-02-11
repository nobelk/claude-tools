---
name: resume-analyzer
description: >
  Analyze and rank PDF resumes of candidates for a software engineering position.
  Use this skill when the user uploads one or more PDF resumes (or provides URLs to
  download them from) and a job description and wants candidates scored, ranked, and
  compared. Triggers include: "rank resumes", "score candidates", "analyze resumes",
  "screen applicants", "evaluate candidates", "review resumes for [role]",
  "download and rank resumes", or any request to compare multiple PDF resumes against
  a job posting. Also use when the user asks to extract GitHub profiles from resumes
  and check open-source contributions, or when the user wants award-based scoring.
  Do NOT use for non-recruitment document analysis or for parsing a single resume
  without scoring.
---

# Resume Analyzer Skill

Analyze PDF resumes against a software engineering job description. Download
resumes from URLs if needed, extract and parse each PDF, exclude overqualified
candidates, score the rest on three criteria, rank them, select the top 10,
produce a detailed report, and self-review for accuracy.

## Available Scripts

This skill bundles three scripts in `scripts/`. Every script uses ONLY the
Python standard library plus `pdfplumber`/`pypdf` (pre-installed).

| Script | Purpose | When to Run |
|--------|---------|-------------|
| `scripts/async_resume_downloader.py` | Async-download resume PDFs from public URLs | Step 1 — only when user provides URLs instead of uploading files |
| `scripts/resume_scorer.py` | Extract text from PDFs, parse candidate data, exclude overqualified, compute NLP similarity, write structured JSON | Step 3 — always |

Claude itself performs Steps 4–8 (GitHub fetching, scoring, ranking, report
generation, and self-review) because they require `web_fetch`, judgment calls,
and iterative verification that only Claude can do.

## Workflow Overview

```
User Input (URLs and/or uploaded PDFs + Job Description)
  │
  ▼
Step 1 ── Download PDFs from URLs (async_resume_downloader.py)
  │         Skip if all resumes are already uploaded as files.
  ▼
Step 2 ── Collect all PDFs into one directory
  │         Merge downloaded PDFs with any directly uploaded PDFs.
  ▼
Step 3 ── Extract & parse all resumes (resume_scorer.py)
  │         Outputs structured JSON with candidate data + exclusion list.
  ▼
Step 4 ── Fetch GitHub profiles (Claude via web_fetch)
  │         For each candidate with a GitHub username in the JSON.
  ▼
Step 5 ── Score each candidate on 3 criteria (Claude)
  │         Experience Match (50%) + GitHub (30%) + Awards (20%)
  ▼
Step 6 ── Rank, select top 10, generate report (Claude)
  │
  ▼
Step 7 ── Self-review & re-run if errors found (Claude)
```

---

## Step 1 — Download Resumes from URLs

**When**: The user provides one or more public URLs to PDF resumes.
**Skip if**: All resumes are uploaded directly as PDF files.

Run the async downloader:

```bash
python3 scripts/async_resume_downloader.py \
    -o /home/claude/resumes \
    "https://example.com/alice.pdf" \
    "https://example.com/bob.pdf"
```

Or use it as a library within a Python script:

```python
import asyncio, sys
sys.path.insert(0, "scripts")
from async_resume_downloader import download_resumes

results = asyncio.run(download_resumes(
    urls=["https://example.com/alice.pdf", "https://example.com/bob.pdf"],
    output_dir="/home/claude/resumes",
))

failed = [r for r in results if not r["success"]]
if failed:
    print(f"WARNING: {len(failed)} download(s) failed")
    for f in failed:
        print(f"  - {f['url']}: {f['error']}")
```

**Features**: concurrent downloads (5 parallel), 3 retries with exponential
backoff, %PDF magic-byte validation, 50 MB size cap, safe filename generation.

**Output**: PDF files saved in the specified directory.

**Error handling**: If a URL fails after all retries, the script logs the error
and continues with the remaining URLs. Report any failed downloads to the user
and exclude those candidates from scoring.

## Step 2 — Collect All PDFs

Merge downloaded PDFs (from Step 1) with any user-uploaded PDFs into a single
working directory:

```bash
mkdir -p /home/claude/resumes

# Copy uploaded PDFs (if any)
cp /mnt/user-data/uploads/*.pdf /home/claude/resumes/ 2>/dev/null

# Downloaded PDFs are already in /home/claude/resumes/ from Step 1
```

Also prepare the job description. If uploaded as a PDF or text file, copy it:
```bash
cp /mnt/user-data/uploads/job_description.* /home/claude/jd.txt
```
If the user typed it in chat, write it to a file:
```bash
cat > /home/claude/jd.txt << 'EOF'
<paste job description text here>
EOF
```

## Step 3 — Extract, Parse & Filter (resume_scorer.py)

Run the extraction and parsing script on the collected resumes:

```bash
python3 scripts/resume_scorer.py \
    /home/claude/resumes \
    /home/claude/jd.txt \
    /home/claude/candidates.json
```

**What this script does automatically**:
1. Parses the job description → extracts required languages, frameworks, min/max years, education.
2. Extracts text from every PDF (pdfplumber primary, pypdf fallback).
3. For each resume, parses: name, GitHub username, languages, frameworks, years of experience, awards, education.
4. **Excludes overqualified candidates** — removes anyone whose years exceed the JD maximum. Logs exclusions.
5. Computes **NLP semantic similarity** (if `sentence-transformers` is installed) between each resume and the JD.
6. Writes structured JSON to the output path.

**To enable NLP similarity** (optional, recommended):
```bash
pip install sentence-transformers --break-system-packages
```
If install succeeds, the script automatically computes cosine similarity using
the `all-MiniLM-L6-v2` model. If unavailable, it falls back to keyword-only
matching and notes this in the output.

**Output JSON structure**:
```json
{
  "job_description": {
    "required_languages": ["Python", "Go"],
    "required_frameworks": ["Kubernetes", "Docker"],
    "min_years_experience": 3,
    "max_years_experience": 5,
    "education": ["B.S. in Computer Science"],
    "raw_text": "..."
  },
  "candidates": [
    {
      "filename": "alice_resume.pdf",
      "name": "Alice Chen",
      "github_username": "alicechen",
      "languages": ["Python", "Go", "JavaScript"],
      "frameworks": ["Kubernetes", "Docker", "React"],
      "years_of_experience": 4,
      "awards": ["Dean's List 2019", "ICPC Regional Finalist 2020"],
      "education": ["B.S. in Computer Science"],
      "semantic_similarity": 0.72,
      "raw_text_preview": "..."
    }
  ],
  "excluded_overqualified": [
    {
      "filename": "bob_resume.pdf",
      "name": "Bob Smith",
      "years_of_experience": 12,
      "max_allowed": 5,
      "reason": "Detected 12 years experience exceeds maximum of 5 years"
    }
  ],
  "total_resumes_scanned": 25,
  "total_after_exclusion": 22,
  "total_excluded": 3,
  "nlp_available": true
}
```

## Step 4 — Fetch GitHub Profiles (Claude)

For each candidate in the JSON who has a `github_username`, use `web_fetch` to
retrieve their GitHub profile:

```
https://github.com/<username>
```

Parse the page content for:
- **Contribution count**: look for "N contributions in the last year"
- **Repository languages**: from pinned repos or the repositories tab
- **Cross-reference** languages from the resume with languages in their repos

If network access is unavailable, score all GitHub as **1** and note
"Network unavailable — GitHub scores defaulted to 1" in the report.

## Step 5 — Score Each Candidate (Claude)

For each eligible candidate, assign three scores (1–10):

### 1. Experience Match (weight 50%)

Use the parsed JSON data (`languages`, `frameworks`, `years_of_experience`,
`education`) plus `semantic_similarity` (if available) to score.

**Blended formula (when NLP available)**:
```
keyword_score    = (matched_requirements / total_requirements) × 10
semantic_score   = similarity × 10
experience_score = round((keyword_score × 0.6) + (semantic_score × 0.4))
```
When NLP is NOT available, use `keyword_score` only.

- **9–10**: Meets every requirement; years in ideal range; similarity ≥ 0.65.
- **7–8**: Meets most requirements with minor gaps.
- **5–6**: Meets roughly half the requirements.
- **3–4**: Matches a few requirements.
- **1–2**: Almost no overlap.

### 2. Open-Source / GitHub Profile (weight 30%)

Use the GitHub data fetched in Step 4.

- **9–10**: 1000+ contributions; active in required languages.
- **7–8**: 500–999 contributions; good language overlap.
- **5–6**: 200–499 contributions; some overlap.
- **3–4**: 50–199 contributions or minimal overlap.
- **1–2**: <50 contributions or no GitHub found.

No GitHub profile → score **1**, note "No GitHub profile provided."

### 3. Awards (weight 20%)

Use the `awards` list from the JSON.

- **9–10**: Multiple prestigious competitive programming or industry awards.
- **7–8**: One major award or several minor awards.
- **5–6**: Academic honors or hackathon participation/win.
- **3–4**: Minor mentions (e.g., Dean's List one semester).
- **1–2**: No awards mentioned.

See `references/scoring_rubric.md` for the full point-by-point rubric and edge cases.

### Composite Score

```
composite = (experience × 0.50) + (github × 0.30) + (awards × 0.20)
```

## Step 6 — Rank, Select Top 10, Generate Report (Claude)

Sort all candidates descending by composite score. Tiebreaker: higher experience
score wins. If fewer than 10 remain after exclusion, rank all of them.

Generate a report (`.md` or `.docx`) containing:

1. **Pipeline summary** — total resumes downloaded, scanned, excluded, eligible; NLP availability.
2. **Excluded candidates** — table of name, detected years, max allowed, reason.
3. **Failed downloads** (if any) — URL and error message.
4. **Top 10 summary table** — Rank, Name, Experience Score, GitHub Score, Awards Score, Composite.
5. **Detailed evidence per top-10 candidate**:
   - Experience: requirements matched vs. unmatched, semantic similarity (if used).
   - GitHub: username, contribution count, repo languages, notable repos.
   - Awards: exact award text extracted from resume.

## Step 7 — Self-Review and Verification (Claude)

After generating the report, re-examine every top-10 entry:

- Re-read the `raw_text_preview` for each candidate from the JSON.
- Verify experience match claims against the actual JD requirements.
- Confirm GitHub data is attributed to the correct candidate (no mix-ups).
- Confirm each listed award actually appears in that candidate's resume text.
- Verify no excluded candidate slipped into the top 10.
- Verify no candidate in the top 10 should have been excluded (years > max).
- If downloads failed, confirm those candidates are not scored.

If ANY discrepancy is found:
1. Log the specific error.
2. Re-run scoring for the affected candidate(s).
3. Re-sort and regenerate the report.

Repeat until the report is accurate and error-free.

## Overqualification Exclusion Rules

The `resume_scorer.py` script applies this filter automatically. Rules:

| JD Pattern | Inferred Max | Example |
|-----------|-------------|---------|
| "3–5 years" | 5 | 6 years → excluded |
| "5+ years" | 10 (min×2) | 11 years → excluded |
| "up to 7 years" | 7 | 8 years → excluded |
| No years mentioned | ∞ (skip filter) | No one excluded |
| User provides explicit max | that value | Use user's number |

If years cannot be determined from a resume, do NOT exclude — keep them and
note "years unknown" in the report.

## Important Notes

- **Input flexibility**: The skill handles URLs, uploaded PDFs, or both. Always start by determining the input type before choosing which steps to run.
- **Privacy**: Do not expose personal data beyond name and GitHub username.
- **Language deduplication**: "Go"/"Golang", "JS"/"JavaScript", "TS"/"TypeScript", "C#"/"CSharp", "Shell"/"Bash" are treated as the same. The script handles this automatically.
- **NLP**: Attempt `pip install sentence-transformers --break-system-packages` once. If it fails, proceed with keyword-only and note it.
- **GitHub fetch**: Use `web_fetch`. If network is disabled, default all GitHub scores to 1 with explanation.
- **Conservative scoring**: When in doubt, err on the low side and note the ambiguity.
