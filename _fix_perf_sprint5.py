"""Sprint 5 perf fixes for agents-ia.pro static HTML.

Cause of failure of Sprint 4: Sprint 4 only patched `src/app/layout.tsx`
(Next.js), but production serves the static `.html` files at repo root
(`vercel.json` -> `outputDirectory: "."`). So FontAwesome + Google Fonts
still loaded render-blocking.

Lighthouse evidence (reports/lighthouse-results/agents_ia_pro.json):
- font-awesome 6.5.0 all.min.css: 947ms blocking
- fonts.googleapis.com Inter css2: 825ms blocking
- Total: 1772ms (close to reported 2710ms est savings)
- CLS culprit: `section.hero-v2 > div.hv2-grid > div > div.cta-row`
  (FA icons appearing after first paint shift CTA buttons)

Fixes applied to every HTML file (root + de/en/es/it/nl/pt/blog/...):
1. Replace render-blocking
     `<link rel="stylesheet" href="...font-awesome...">`
   with async pattern:
     `<link rel="preload" as="style" href="..." onload="this.onload=null;this.rel='stylesheet'">`
   + `<noscript>` fallback.
2. Same async pattern for Google Fonts Inter stylesheet.
3. Inject anti-CLS reserve-space CSS for FA icons in `.cta-row`
   and inline-flex containers so their slot is reserved before FA loads.

Design / GA4 consent / content / structure: UNTOUCHED (hard locks).
Idempotent: re-runs are safe; already-patched files are skipped.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_DIRS = {
    "node_modules",
    ".next",
    ".vercel",
    ".git",
    "rapports-pdf",  # PDF source HTML, not served as web pages
}

# --- target regexes --------------------------------------------------------

FA_BLOCKING_RE = re.compile(
    r'<link\s+rel="stylesheet"\s+'
    r'href="(https://cdnjs\.cloudflare\.com/ajax/libs/font-awesome/[^"]+)"\s*/?>',
    re.IGNORECASE,
)

GF_BLOCKING_RE = re.compile(
    r'<link\s+href="(https://fonts\.googleapis\.com/css2\?family=Inter[^"]+)"\s+'
    r'rel="stylesheet"\s*/?>',
    re.IGNORECASE,
)

# Marker so we never inject the CLS-fix <style> twice.
CLS_MARKER = "data-perf-sprint5-cls"

CLS_RESERVE_STYLE = (
    f'<style id="{CLS_MARKER}">'
    # Reserve a slot for FA <i class="fas|far|fab"> icons before the
    # web font loads. They are inline-block in the FA stylesheet anyway;
    # we just give them a min-width so layout does not shift when FA
    # finally swaps the empty glyph for the rendered one.
    ".cta-row .fas,.cta-row .far,.cta-row .fab,"
    ".cta-row [class^='fa-'],.cta-row [class*=' fa-']"
    "{display:inline-block;min-width:1em;text-align:center;}"
    # Same trick for the hero search icon (`i.search-icon` is positioned
    # absolutely; absolute children do not cause CLS by themselves, but
    # we still want it to have stable dimensions).
    ".hero-v2 .search-hero i.search-icon{min-width:1em;text-align:center;}"
    # Generic safety net: any inline FA icon next to text should reserve
    # space too. Scoped to common nav/button containers to avoid touching
    # design elsewhere.
    ".nav-link .fas,.nav-link .far,.btn .fas,.btn .far,"
    "a.cta-primary .fas,a.cta-secondary .fas"
    "{display:inline-block;min-width:1em;text-align:center;}"
    "</style>"
)


def _async_fa(url: str) -> str:
    """Render-non-blocking FontAwesome link snippet."""
    return (
        f'<link rel="preload" as="style" href="{url}" '
        f'onload="this.onload=null;this.rel=\'stylesheet\'">'
        f'<noscript><link rel="stylesheet" href="{url}"></noscript>'
    )


def _async_gf(url: str) -> str:
    """Render-non-blocking Google Fonts link snippet."""
    return (
        f'<link rel="preload" as="style" href="{url}" '
        f'onload="this.onload=null;this.rel=\'stylesheet\'">'
        f'<noscript><link href="{url}" rel="stylesheet"></noscript>'
    )


def _patch_html(text: str) -> tuple[str, dict[str, bool]]:
    """Apply Sprint 5 fixes. Returns (new_text, changes_made)."""
    changes = {"fa_async": False, "gf_async": False, "cls_style": False}

    def _fa_sub(m: re.Match[str]) -> str:
        changes["fa_async"] = True
        return _async_fa(m.group(1))

    def _gf_sub(m: re.Match[str]) -> str:
        changes["gf_async"] = True
        return _async_gf(m.group(1))

    new_text = FA_BLOCKING_RE.sub(_fa_sub, text)
    new_text = GF_BLOCKING_RE.sub(_gf_sub, new_text)

    if CLS_MARKER not in new_text and "</head>" in new_text:
        new_text = new_text.replace(
            "</head>", f"{CLS_RESERVE_STYLE}\n</head>", 1
        )
        changes["cls_style"] = True

    return new_text, changes


def _walk_html_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*.html"):
        rel_parts = path.relative_to(ROOT).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        files.append(path)
    return files


def main() -> None:
    files = _walk_html_files()
    totals = {"fa_async": 0, "gf_async": 0, "cls_style": 0, "untouched": 0}
    touched: list[str] = []

    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # Some legacy files may be cp1252; skip silently rather than
            # corrupt them. Production HTML is utf-8.
            continue

        new_text, changes = _patch_html(text)

        if new_text == text:
            totals["untouched"] += 1
            continue

        path.write_text(new_text, encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        touched.append(rel)
        for key, did in changes.items():
            if did:
                totals[key] += 1

    print(f"Scanned: {len(files)} HTML files")
    print(f"Patched: {len(touched)} files")
    print(f"  - FontAwesome -> async: {totals['fa_async']}")
    print(f"  - Google Fonts Inter -> async: {totals['gf_async']}")
    print(f"  - Anti-CLS <style> injected: {totals['cls_style']}")
    print(f"  - Already up to date: {totals['untouched']}")
    if touched[:5]:
        print("Sample touched files:")
        for rel in touched[:5]:
            print(f"  {rel}")


if __name__ == "__main__":
    main()
