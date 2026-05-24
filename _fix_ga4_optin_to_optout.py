#!/usr/bin/env python3
"""
Fix GA4 consent: OPT-IN → OPT-OUT sur agents-ia.pro (agents-ia.pro).

Avant (bug) : analytics_storage: 'denied' par défaut + update si 'accepted'
Après (fix)  : analytics_storage: _c === 'rejected' ? 'denied' : 'granted'
"""
from __future__ import annotations
import sys
from pathlib import Path

GA_ID = "G-B5627RD3TF"
SKIP_DIRS = {"node_modules", ".next", ".vercel", ".git", "rapports-pdf"}

# Exact old lines (as they appear in the files)
OLD_CONSENT   = "  gtag('consent', 'default', { analytics_storage: 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });\n"
OLD_VAR_C     = "  var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;\n"
OLD_IF_ACCEPT = "  if (_c === 'accepted') { gtag('consent', 'update', { analytics_storage: 'granted' }); }\n"

# New lines (opt-out: granted by default, denied only if rejected)
NEW_VAR_C     = "  var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;\n"
NEW_CONSENT   = "  gtag('consent', 'default', { analytics_storage: _c === 'rejected' ? 'denied' : 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });\n"


def fix_text(text: str) -> str | None:
    """Return fixed text, or None if already fixed or pattern not found."""
    if "_c === 'rejected'" in text:
        return None  # already opt-out
    if OLD_CONSENT not in text:
        return None  # unknown pattern
    if OLD_VAR_C not in text or OLD_IF_ACCEPT not in text:
        return None

    # Step 1: insert var _c before the consent line
    text = text.replace(OLD_CONSENT, NEW_VAR_C + NEW_CONSENT)
    # Step 2: remove the old var _c line (now appears after consent)
    text = text.replace(NEW_VAR_C + NEW_CONSENT + OLD_VAR_C,
                        NEW_VAR_C + NEW_CONSENT)
    # Step 3: remove the if (accepted) line
    text = text.replace(OLD_IF_ACCEPT, "")
    return text


def process(path: Path) -> str:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return "error"
    if GA_ID not in text:
        return "skip-no-ga"
    if "_c === 'rejected'" in text:
        return "skip-already-fixed"
    fixed = fix_text(text)
    if fixed is None:
        return "skip-no-match"
    path.write_text(fixed, encoding="utf-8", newline="")
    return "modified"


def main():
    root = Path(__file__).resolve().parent
    html_files = [
        p for p in root.rglob("*.html")
        if not any(part in SKIP_DIRS for part in p.relative_to(root).parts)
    ]
    counts: dict[str, int] = {}
    modified = []
    no_match = []
    for p in html_files:
        r = process(p)
        counts[r] = counts.get(r, 0) + 1
        if r == "modified":
            modified.append(p)
        elif r == "skip-no-match":
            no_match.append(p)

    print(f"Scanned : {len(html_files)} HTML files")
    for k, v in sorted(counts.items()):
        print(f"  {k:<25} : {v}")
    if modified:
        print(f"\nModified ({len(modified)}) — sample:")
        for p in modified[:10]:
            print(f"  {p.relative_to(root)}")
    if no_match:
        print(f"\nNo-match sample:")
        for p in no_match[:5]:
            print(f"  {p.relative_to(root)}")


if __name__ == "__main__":
    main()
