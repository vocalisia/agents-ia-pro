#!/usr/bin/env python3
"""
Idempotent fix for duplicate GA4 gtag blocks (G-B5627RD3TF).

Problem: two <script> blocks define gtag() and window.dataLayer twice.
Solution: collapse into a single consent-mode v2 block, single source of truth.

Run from repo root: python _fix_ga4_tag.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

GA_ID = "G-B5627RD3TF"

NEW_BLOCK = """<!-- Google Analytics 4 (consent mode v2) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-B5627RD3TF"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;
  gtag('consent', 'default', { analytics_storage: _c === 'rejected' ? 'denied' : 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
  gtag('js', new Date());
  gtag('config', 'G-B5627RD3TF', { anonymize_ip: true });
</script>"""

# Match the legacy duplicated block. Whitespace-tolerant.
# GA4 comment is optional (some pages omit it). Consent logic may use either
# 'rejected' (opt-out) or 'accepted' (opt-in) variant; both are normalised
# to the 'rejected' opt-out form per the user spec.
LEGACY_PATTERN = re.compile(
    r"""(?:<!--\s*Google\s+Analytics\s+4\s*-->\s*)?
\s*<script>\s*
\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*
\s*function\s+gtag\(\)\{dataLayer\.push\(arguments\);\}\s*
\s*var\s+_c\s*=.*?localStorage\.getItem\(['"]ai_cookies['"]\)\s*:\s*null;\s*
\s*gtag\(\s*['"]consent['"]\s*,\s*['"]default['"]\s*,\s*\{[^}]*\}\s*\);\s*
</script>\s*
<script\s+async\s+src=["']https://www\.googletagmanager\.com/gtag/js\?id=G-B5627RD3TF["']\s*>\s*</script>\s*
\s*<script>\s*
\s*window\.dataLayer\s*=\s*window\.dataLayer\s*\|\|\s*\[\];\s*
\s*function\s+gtag\(\)\{dataLayer\.push\(arguments\);\}\s*
\s*gtag\(\s*['"]js['"]\s*,\s*new\s+Date\(\)\s*\);\s*
\s*gtag\(\s*['"]config['"]\s*,\s*['"]G-B5627RD3TF['"]\s*\);\s*
\s*</script>""",
    re.DOTALL | re.VERBOSE,
)

NEW_MARKER = "Google Analytics 4 (consent mode v2)"


def process_file(path: Path) -> str:
    """Return one of: 'modified', 'skip-new', 'skip-no-ga', 'error'."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return "error"

    if NEW_MARKER in text:
        return "skip-new"

    if GA_ID not in text:
        return "skip-no-ga"

    new_text, n = LEGACY_PATTERN.subn(NEW_BLOCK, text)
    if n == 0:
        # Has GA ID but not the exact legacy shape - leave alone, report.
        return "skip-no-match"

    try:
        path.write_text(new_text, encoding="utf-8", newline="")
    except OSError:
        return "error"
    return "modified"


def main() -> int:
    root = Path(__file__).resolve().parent
    # Recurse, but skip node_modules and other build/vendor dirs.
    skip_dirs = {"node_modules", ".next", ".vercel", ".git", "rapports-pdf"}

    targets: list[Path] = []
    for p in root.rglob("*.html"):
        if any(part in skip_dirs for part in p.relative_to(root).parts):
            continue
        targets.append(p)

    counts = {"modified": 0, "skip-new": 0, "skip-no-ga": 0, "skip-no-match": 0, "error": 0}
    modified_paths: list[Path] = []
    no_match_paths: list[Path] = []

    for p in targets:
        result = process_file(p)
        counts[result] += 1
        if result == "modified":
            modified_paths.append(p)
        elif result == "skip-no-match":
            no_match_paths.append(p)

    print(f"Scanned: {len(targets)} HTML files")
    print(f"  modified       : {counts['modified']}")
    print(f"  skip-new (OK)  : {counts['skip-new']}")
    print(f"  skip-no-ga     : {counts['skip-no-ga']}")
    print(f"  skip-no-match  : {counts['skip-no-match']}")
    print(f"  error          : {counts['error']}")

    if modified_paths:
        print("\nSample modified files (up to 10):")
        for p in modified_paths[:10]:
            print(f"  {p.relative_to(root)}")

    if no_match_paths:
        print("\nFiles with GA ID but unrecognized block shape (up to 10):")
        for p in no_match_paths[:10]:
            print(f"  {p.relative_to(root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
