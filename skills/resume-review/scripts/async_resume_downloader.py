#!/usr/bin/env python3
"""
async_resume_downloader.py — Download one or more resume PDFs from public
URLs using asyncio, with progress reporting, retry logic, and PDF validation.

Uses ONLY the Python standard library (asyncio + urllib.request). Blocking
I/O is offloaded to a thread-pool via asyncio.to_thread so downloads run
concurrently without third-party async HTTP libraries.

Usage:
    # Single URL
    python3 async_resume_downloader.py "https://example.com/resume.pdf"

    # Multiple URLs (downloaded concurrently)
    python3 async_resume_downloader.py "https://a.com/r1.pdf" "https://b.com/r2.pdf"

    # Custom output directory
    python3 async_resume_downloader.py -o ./resumes "https://example.com/resume.pdf"

    # As an importable library
    import asyncio
    from async_resume_downloader import download_resumes
    results = asyncio.run(download_resumes(["https://example.com/resume.pdf"]))
"""

from __future__ import annotations

import argparse
import asyncio
import os
import re
import ssl
import sys
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urlparse
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

MAX_CONCURRENT = 5           # semaphore limit for parallel downloads
MAX_RETRIES = 3              # retry attempts per URL
RETRY_BACKOFF = 1.5          # exponential back-off base (seconds)
TIMEOUT_SECONDS = 60         # socket-level timeout per request
CHUNK_SIZE = 64 * 1024       # 64 KB streaming chunks
MAX_FILE_SIZE = 50_000_000   # 50 MB safety cap per file
PDF_MAGIC = b"%PDF"          # first 4 bytes of every valid PDF
USER_AGENT = "ResumeDownloader/1.0 (Python-urllib)"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def sanitize_filename(url: str, index: int) -> str:
    """Derive a filesystem-safe filename from the URL path.

    Falls back to ``resume_NNN.pdf`` when the URL has no usable basename.
    """
    path = urlparse(url).path
    basename = os.path.basename(unquote(path))
    basename = re.sub(r"[^\w.\-]", "_", basename)

    if not basename or not basename.lower().endswith(".pdf"):
        basename = f"resume_{index:03d}.pdf"
    return basename


def validate_pdf(filepath: Path) -> bool:
    """Return True if the file begins with the ``%PDF`` magic bytes."""
    try:
        with open(filepath, "rb") as fh:
            return fh.read(4) == PDF_MAGIC
    except OSError:
        return False


def _build_ssl_context() -> ssl.SSLContext:
    """Create a default SSL context for HTTPS requests."""
    ctx = ssl.create_default_context()
    return ctx


# ---------------------------------------------------------------------------
# Blocking download (runs inside a thread)
# ---------------------------------------------------------------------------

def _download_blocking(url: str, dest: Path) -> int:
    """Synchronous download of *url* into *dest*.

    Streams the response in chunks to keep memory usage low and enforces
    the ``MAX_FILE_SIZE`` limit.  Returns the number of bytes written.

    This function is intended to be called via ``asyncio.to_thread``.
    """
    req = Request(url, headers={"User-Agent": USER_AGENT})
    ctx = _build_ssl_context()

    with urlopen(req, timeout=TIMEOUT_SECONDS, context=ctx) as resp:
        # Honour Content-Length if the server provides it
        content_length = resp.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_FILE_SIZE:
            raise ValueError(
                f"File too large ({int(content_length):,} bytes "
                f"> {MAX_FILE_SIZE:,} byte limit)"
            )

        downloaded = 0
        with open(dest, "wb") as fh:
            while True:
                chunk = resp.read(CHUNK_SIZE)
                if not chunk:
                    break
                downloaded += len(chunk)
                if downloaded > MAX_FILE_SIZE:
                    raise ValueError(
                        f"Download exceeded {MAX_FILE_SIZE:,} byte limit"
                    )
                fh.write(chunk)

    return downloaded


# ---------------------------------------------------------------------------
# Async wrapper with retry + validation
# ---------------------------------------------------------------------------

async def download_one(
    url: str,
    dest: Path,
    semaphore: asyncio.Semaphore,
) -> dict:
    """Download a single PDF with concurrency control, retries, and validation.

    Returns::

        {
            "url":        str,
            "path":       str,
            "success":    bool,
            "size_bytes": int,
            "elapsed":    float,
            "error":      str | None,
        }
    """
    result: dict = {
        "url": url,
        "path": str(dest),
        "success": False,
        "size_bytes": 0,
        "elapsed": 0.0,
        "error": None,
    }

    async with semaphore:
        for attempt in range(1, MAX_RETRIES + 1):
            t0 = time.monotonic()
            try:
                # Offload blocking I/O to the default thread-pool
                downloaded = await asyncio.to_thread(
                    _download_blocking, url, dest,
                )
                elapsed = time.monotonic() - t0

                # Validate the file is a real PDF
                if not validate_pdf(dest):
                    dest.unlink(missing_ok=True)
                    raise ValueError(
                        "Downloaded file is not a valid PDF "
                        "(missing %PDF header)"
                    )

                result.update(
                    success=True,
                    size_bytes=downloaded,
                    elapsed=round(elapsed, 2),
                )
                print(
                    f"  ✅  {dest.name}  "
                    f"({downloaded:,} bytes in {elapsed:.1f}s)"
                )
                return result

            except (HTTPError, URLError, ValueError, OSError) as exc:
                elapsed = time.monotonic() - t0
                result["elapsed"] = round(elapsed, 2)
                result["error"] = str(exc)

                # Remove any partial file
                dest.unlink(missing_ok=True)

                if attempt < MAX_RETRIES:
                    wait = RETRY_BACKOFF ** attempt
                    print(
                        f"  ⚠️  Attempt {attempt}/{MAX_RETRIES} failed for "
                        f"{dest.name}: {exc}  — retrying in {wait:.1f}s"
                    )
                    await asyncio.sleep(wait)
                else:
                    print(
                        f"  ❌  {dest.name}  FAILED after "
                        f"{MAX_RETRIES} attempts: {exc}"
                    )

    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def download_resumes(
    urls: list[str],
    output_dir: str | Path = ".",
    max_concurrent: int = MAX_CONCURRENT,
) -> list[dict]:
    """Download multiple resume PDFs concurrently.

    Args:
        urls:           Public URLs pointing to PDF files.
        output_dir:     Target directory (created if it doesn't exist).
        max_concurrent: Maximum simultaneous downloads.

    Returns:
        A list of result dicts (one per URL) in the same order as *urls*.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    semaphore = asyncio.Semaphore(max_concurrent)

    # Build unique destination paths
    seen_names: set[str] = set()
    download_pairs: list[tuple[str, Path]] = []

    for idx, url in enumerate(urls):
        name = sanitize_filename(url, idx)
        while name in seen_names:
            stem, ext = os.path.splitext(name)
            name = f"{stem}_{idx}{ext}"
        seen_names.add(name)
        download_pairs.append((url, output_path / name))

    print(f"Downloading {len(urls)} resume(s) → {output_path.resolve()}/\n")

    tasks = [
        download_one(url, dest, semaphore)
        for url, dest in download_pairs
    ]
    results = await asyncio.gather(*tasks)

    # Print summary
    ok = sum(1 for r in results if r["success"])
    fail = len(results) - ok
    total_bytes = sum(r["size_bytes"] for r in results)
    print(
        f"\nDone: {ok} succeeded, {fail} failed, "
        f"{total_bytes:,} bytes total."
    )
    return list(results)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Async download of resume PDFs from public URLs.",
    )
    parser.add_argument(
        "urls",
        nargs="+",
        help="One or more public URLs pointing to PDF files.",
    )
    parser.add_argument(
        "-o", "--output-dir",
        default=".",
        help="Directory to save downloaded PDFs (default: current directory).",
    )
    parser.add_argument(
        "-c", "--max-concurrent",
        type=int,
        default=MAX_CONCURRENT,
        help=f"Max parallel downloads (default: {MAX_CONCURRENT}).",
    )
    args = parser.parse_args()

    results = asyncio.run(
        download_resumes(args.urls, args.output_dir, args.max_concurrent)
    )

    if any(not r["success"] for r in results):
        sys.exit(1)


if __name__ == "__main__":
    main()
