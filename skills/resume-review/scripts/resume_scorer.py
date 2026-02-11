#!/usr/bin/env python3
"""
resume_scorer.py — Extract text from PDF resumes, parse candidate info,
compute overqualification flags, optionally run NLP semantic similarity,
and produce a JSON structure ready for scoring and ranking.

Usage:
    python3 scripts/resume_scorer.py <resume_dir> <job_description_path> <output_json>

Arguments:
    resume_dir            Directory containing PDF resume files
    job_description_path  Path to the job description (text or PDF)
    output_json           Path to write extracted candidate data as JSON
"""

import json
import os
import re
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------

def extract_text_pdfplumber(pdf_path):
    """Primary extractor using pdfplumber."""
    try:
        import pdfplumber
        text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception:
        return ""


def extract_text_pypdf(pdf_path):
    """Fallback extractor using pypdf."""
    try:
        from pypdf import PdfReader
        reader = PdfReader(pdf_path)
        return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception:
        return ""


def extract_text(pdf_path):
    """Extract text with pdfplumber; fall back to pypdf if empty."""
    text = extract_text_pdfplumber(pdf_path)
    if not text:
        text = extract_text_pypdf(pdf_path)
    return text


# ---------------------------------------------------------------------------
# Language / framework alias deduplication
# ---------------------------------------------------------------------------

LANGUAGE_ALIASES = {
    "golang": "Go",
    "go": "Go",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "csharp": "C#",
    "c#": "C#",
    "c++": "C++",
    "cpp": "C++",
    "objective-c": "Objective-C",
    "objc": "Objective-C",
    "shell": "Shell/Bash",
    "bash": "Shell/Bash",
}


def normalize_language(lang):
    """Return the canonical name for a language, deduplicating aliases."""
    return LANGUAGE_ALIASES.get(lang.lower(), lang)


def deduplicate_languages(lang_list):
    """Deduplicate a list of languages using canonical names."""
    seen = {}
    for lang in lang_list:
        canonical = normalize_language(lang)
        if canonical not in seen:
            seen[canonical] = lang  # keep first form encountered
    return list(seen.keys())


# ---------------------------------------------------------------------------
# Candidate info extraction
# ---------------------------------------------------------------------------

COMMON_LANGUAGES = [
    "Python", "Java", "JavaScript", "TypeScript", "C++", "C#", "C",
    "Go", "Golang", "Rust", "Ruby", "PHP", "Swift", "Kotlin", "Scala",
    "R", "MATLAB", "Perl", "Haskell", "Elixir", "Clojure", "Dart",
    "Objective-C", "Lua", "Shell", "Bash", "SQL", "HTML", "CSS",
]

COMMON_FRAMEWORKS = [
    "React", "Angular", "Vue", "Next.js", "Nuxt", "Django", "Flask",
    "FastAPI", "Spring", "Spring Boot", "Rails", "Ruby on Rails",
    "Express", "Node.js", "TensorFlow", "PyTorch", "Keras",
    "Kubernetes", "Docker", "AWS", "GCP", "Azure", "Terraform",
    "Ansible", ".NET", "ASP.NET", "Laravel", "Symfony", "Svelte",
    "GraphQL", "REST", "gRPC", "Kafka", "RabbitMQ", "Redis",
    "PostgreSQL", "MySQL", "MongoDB", "Elasticsearch", "Spark",
    "Hadoop", "Airflow", "dbt", "Snowflake", "BigQuery",
]

AWARD_KEYWORDS = [
    "award", "honor", "honours", "prize", "dean's list", "deans list",
    "scholarship", "fellowship", "icpc", "hackathon", "code jam",
    "codeforces", "topcoder", "leetcode", "kaggle", "olympiad",
    "competition winner", "first place", "1st place", "gold medal",
    "silver medal", "bronze medal", "cum laude", "magna cum laude",
    "summa cum laude", "valedictorian", "salutatorian", "patent",
    "publication", "published", "best paper", "acm", "ieee",
    "won", "winner", "finalist", "placed", "rank",
]

# Lines starting with these patterns are unlikely to be a person's name.
NAME_BLACKLIST_PATTERNS = [
    r'^(resume|curriculum\s*vitae|cv|objective|summary|profile|contact)',
    r'^(http|www|phone|email|address|linkedin|github)',
]


def extract_name(text):
    """Heuristic: first non-empty, non-header, non-contact line is the name."""
    for line in text.split("\n"):
        line = line.strip()
        if not line or len(line) > 60:
            continue
        # Skip common resume headers
        if any(re.match(pat, line, re.I) for pat in NAME_BLACKLIST_PATTERNS):
            continue
        # Skip lines that look like contact info
        if re.search(r'@|\.com|\.org|\.edu|\d{3}[\-\.]\d{3}|\d{5}', line):
            continue
        # Skip lines that are ALL CAPS and short (likely section headers)
        if line.isupper() and len(line.split()) <= 2 and len(line) < 20:
            continue
        return line
    return "Unknown"


def extract_github(text):
    """Extract GitHub username from resume text."""
    patterns = [
        r'github\.com/([A-Za-z0-9_-]+)(?:[/\s?#]|$)',
        r'GitHub\s*:\s*(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_-]+)',
        r'GitHub\s*:\s*@?([A-Za-z0-9_-]+)',
    ]
    false_positives = {"in", "com", "io", "org", "profile", "settings",
                       "topics", "explore", "features", "enterprise",
                       "pricing", "login", "join", "about"}
    for pat in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            username = match.group(1)
            if username.lower() not in false_positives:
                return username
    return None


def extract_languages(text, required_languages=None):
    """Find programming languages mentioned in the text, with deduplication."""
    found = []
    search_list = required_languages if required_languages else COMMON_LANGUAGES
    for lang in search_list:
        if len(lang) <= 2:
            # Short names (C, R) — case-sensitive exact word boundary
            if re.search(r'(?<![A-Za-z])' + re.escape(lang) + r'(?![A-Za-z])', text):
                found.append(lang)
        else:
            if re.search(r'\b' + re.escape(lang) + r'\b', text, re.IGNORECASE):
                found.append(lang)
    return deduplicate_languages(found)


def extract_frameworks(text, required_frameworks=None):
    """Find frameworks/tools mentioned in the text."""
    found = []
    search_list = required_frameworks if required_frameworks else COMMON_FRAMEWORKS
    for fw in search_list:
        if re.search(r'\b' + re.escape(fw) + r'\b', text, re.IGNORECASE):
            found.append(fw)
    return list(set(found))


def extract_years_of_experience(text):
    """Estimate total years of experience, handling overlapping ranges."""
    # 1. Check for explicit statements like "10+ years" or "10 years of experience"
    explicit = re.findall(
        r'(\d+)\+?\s*years?\s*(?:of\s+)?(?:professional\s+)?(?:experience|exp)',
        text, re.I,
    )
    if explicit:
        return max(int(y) for y in explicit)

    # 2. Parse date ranges and merge overlapping intervals
    year_ranges = re.findall(
        r'(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+)?'
        r'(\d{4})\s*[-–—]+\s*'
        r'(?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+)?'
        r'(\d{4}|[Pp]resent|[Cc]urrent|[Nn]ow)',
        text,
    )
    if not year_ranges:
        return None

    current_year = datetime.now().year
    intervals = []
    for start_str, end_str in year_ranges:
        start_y = int(start_str)
        end_y = current_year if end_str.lower() in ("present", "current", "now") else int(end_str)
        if 1970 <= start_y <= current_year and start_y <= end_y <= current_year + 1:
            intervals.append((start_y, end_y))

    if not intervals:
        return None

    # Merge overlapping intervals to avoid double-counting parallel jobs
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        prev_start, prev_end = merged[-1]
        if start <= prev_end:
            merged[-1] = (prev_start, max(prev_end, end))
        else:
            merged.append((start, end))

    total = sum(end - start for start, end in merged)
    return total if total > 0 else None


def extract_max_years_from_jd(text):
    """Extract the maximum years of experience from a job description.

    Returns:
        (min_years, max_years) tuple. max_years may be None if not determinable.
    """
    # Range pattern: "3-5 years", "3–5 years", "3 to 5 years"
    range_match = re.search(
        r'(\d+)\s*[-–—]\s*(\d+)\s*(?:\+?\s*)?years?', text, re.I
    )
    if range_match:
        return int(range_match.group(1)), int(range_match.group(2))

    range_match2 = re.search(
        r'(\d+)\s+to\s+(\d+)\s*(?:\+?\s*)?years?', text, re.I
    )
    if range_match2:
        return int(range_match2.group(1)), int(range_match2.group(2))

    # "at most N years" / "up to N years" / "no more than N years"
    max_match = re.search(
        r'(?:at most|up to|no more than|maximum of?|max)\s*(\d+)\s*years?',
        text, re.I,
    )
    if max_match:
        return None, int(max_match.group(1))

    # Min-only pattern: "5+ years" / "at least 5 years" / "minimum 5 years"
    min_match = re.search(
        r'(\d+)\+?\s*years?', text, re.I
    )
    if min_match:
        min_y = int(min_match.group(1))
        return min_y, min_y * 2  # Default max = min × 2

    return None, None


def extract_awards(text):
    """Return list of award-related snippets found in the resume."""
    awards = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            continue
        for kw in AWARD_KEYWORDS:
            if kw.lower() in stripped.lower():
                awards.append(stripped)
                break
    return list(set(awards))


def extract_education(text):
    """Extract education degree mentions (capped to avoid greedy over-match).

    Uses word-boundary anchors to prevent false matches inside words
    (e.g. 'systems' falsely matching 'M.S.').
    """
    degrees = []
    patterns = [
        r"\b(Ph\.?D\.?|Doctor(?:ate)?)\s+(?:in|of)\s+[\w\s]{3,40}",
        r"\b(Master'?s?|M\.S\.?|M\.A\.?|M\.Eng\.?|MBA)\s+(?:in|of)\s+[\w\s]{3,40}",
        r"\b(Bachelor'?s?|B\.S\.?|B\.A\.?|B\.Eng\.?|B\.Tech)\s+(?:in|of)\s+[\w\s]{3,40}",
        r"\b(Associate'?s?|A\.S\.?|A\.A\.?)\s+(?:in|of)\s+[\w\s]{3,40}",
    ]
    for pat in patterns:
        for match in re.finditer(pat, text, re.IGNORECASE):
            degrees.append(match.group(0).strip())
    return degrees


# ---------------------------------------------------------------------------
# NLP semantic similarity (optional)
# ---------------------------------------------------------------------------

def compute_semantic_similarity(jd_text, resume_text):
    """Compute cosine similarity between JD and resume using sentence-transformers.

    Returns a float 0.0–1.0, or None if the library is unavailable.
    """
    try:
        from sentence_transformers import SentenceTransformer, util

        model = SentenceTransformer("all-MiniLM-L6-v2")
        # Truncate long texts to fit model context (max ~256 tokens for speed)
        jd_chunk = jd_text[:2000]
        resume_chunk = resume_text[:2000]
        jd_emb = model.encode(jd_chunk, convert_to_tensor=True)
        res_emb = model.encode(resume_chunk, convert_to_tensor=True)
        similarity = util.cos_sim(jd_emb, res_emb).item()
        return round(similarity, 4)
    except Exception as e:
        print(f"NLP similarity unavailable: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Job description parsing
# ---------------------------------------------------------------------------

def parse_job_description(jd_path):
    """Parse a job description from a text or PDF file."""
    if jd_path.lower().endswith(".pdf"):
        text = extract_text(jd_path)
    else:
        with open(jd_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

    min_years, max_years = extract_max_years_from_jd(text)

    return {
        "raw_text": text,
        "required_languages": extract_languages(text),
        "required_frameworks": extract_frameworks(text),
        "min_years_experience": min_years,
        "max_years_experience": max_years,
        "education": extract_education(text),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def process_resumes(resume_dir, jd_path, output_path):
    """Process all PDF resumes in a directory and write JSON output."""
    jd = parse_job_description(jd_path)

    # Attempt NLP model load once (shared across candidates)
    nlp_available = False
    try:
        from sentence_transformers import SentenceTransformer
        nlp_available = True
        print("NLP model (sentence-transformers) available — will compute semantic similarity.")
    except ImportError:
        print("sentence-transformers not installed — using keyword-only matching.", file=sys.stderr)

    candidates = []
    excluded = []

    pdf_files = sorted(
        f for f in os.listdir(resume_dir)
        if f.lower().endswith(".pdf")
    )

    for filename in pdf_files:
        pdf_path = os.path.join(resume_dir, filename)
        text = extract_text(pdf_path)
        if not text:
            print(f"WARNING: Could not extract text from {filename}", file=sys.stderr)
            continue

        years = extract_years_of_experience(text)

        # --- Overqualification exclusion ---
        max_yrs = jd["max_years_experience"]
        if max_yrs is not None and years is not None and years > max_yrs:
            excluded.append({
                "filename": filename,
                "name": extract_name(text),
                "years_of_experience": years,
                "max_allowed": max_yrs,
                "reason": f"Detected {years} years experience exceeds maximum of {max_yrs} years",
            })
            continue

        # --- Semantic similarity (if available) ---
        similarity = None
        if nlp_available:
            similarity = compute_semantic_similarity(jd["raw_text"], text)

        candidate = {
            "filename": filename,
            "name": extract_name(text),
            "github_username": extract_github(text),
            "languages": extract_languages(text, jd["required_languages"] + COMMON_LANGUAGES),
            "frameworks": extract_frameworks(text, jd["required_frameworks"] + COMMON_FRAMEWORKS),
            "years_of_experience": years,
            "awards": extract_awards(text),
            "education": extract_education(text),
            "semantic_similarity": similarity,
            "raw_text_preview": text[:4000],  # Increased for better self-review
        }
        candidates.append(candidate)

    output = {
        "job_description": {
            "required_languages": jd["required_languages"],
            "required_frameworks": jd["required_frameworks"],
            "min_years_experience": jd["min_years_experience"],
            "max_years_experience": jd["max_years_experience"],
            "education": jd["education"],
            "raw_text": jd["raw_text"],
        },
        "candidates": candidates,
        "excluded_overqualified": excluded,
        "total_resumes_scanned": len(pdf_files),
        "total_after_exclusion": len(candidates),
        "total_excluded": len(excluded),
        "nlp_available": nlp_available,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Scanned {len(pdf_files)} resumes: {len(candidates)} eligible, "
          f"{len(excluded)} excluded (overqualified). Output → {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(__doc__)
        sys.exit(1)

    resume_dir = sys.argv[1]
    jd_path = sys.argv[2]
    output_json = sys.argv[3]

    if not os.path.isdir(resume_dir):
        print(f"Error: {resume_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    if not os.path.isfile(jd_path):
        print(f"Error: {jd_path} not found", file=sys.stderr)
        sys.exit(1)

    process_resumes(resume_dir, jd_path, output_json)
