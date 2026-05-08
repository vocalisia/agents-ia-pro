#!/usr/bin/env python3
"""Add Éditeurs + Newsletter + Rapports links to nav + footer Ressources."""
import re
from pathlib import Path

ROOT = Path(__file__).parent

NEW_NAV_AFTER_BLOG = '            <a href="blog.html" class="nav-link">Blog</a>\n            <a href="editeurs.html" class="nav-link">Éditeurs</a>'
NEW_FOOTER_RESOURCES_ADDITIONS = '<a href="editeurs.html">Éditeurs</a><a href="newsletter.html">Newsletter</a><a href="rapports.html">Rapports B2B</a>'


def process(path: Path):
    name = path.name
    if name in ("editeurs.html", "newsletter.html", "rapports.html"):
        return False
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False

    original = content
    modified = False

    # 1. Insert "Éditeurs" in nav right after Blog (only if not already present)
    # Pattern to detect already-inserted: <a href="editeurs.html" class="nav-link">
    if 'editeurs.html" class="nav-link">' not in content:
        pat = re.compile(r'(<a\s+href="blog\.html"\s+class="nav-link">Blog</a>)(?!\s*<a\s+href="editeurs)')
        m = pat.search(content)
        if m:
            # Only insert if this is in a nav context (check <nav> wrapper exists before match)
            before = content[:m.start()]
            if '<nav' in before.lower():
                content = pat.sub(r'\1\n            <a href="editeurs.html" class="nav-link">Éditeurs</a>', content, count=1)
                modified = True

    # 2. Add footer Ressources links (only if missing)
    if 'href="editeurs.html"' not in content or 'href="newsletter.html"' not in content or 'href="rapports.html"' not in content:
        # Anchor on existing footer resources pattern: <a href="blog.html">Blog</a><a href="a-propos.html">À propos</a>
        pat = re.compile(r'(<a href="blog\.html">Blog</a>\s*<a href="a-propos\.html">À propos</a>)(?!\s*<a href="editeurs)')
        m = pat.search(content)
        if m:
            content = pat.sub(r'\1' + NEW_FOOTER_RESOURCES_ADDITIONS, content, count=1)
            modified = True

    if modified and content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    files = list(ROOT.glob("*.html"))
    files.extend((ROOT / "blog").glob("*.html"))
    updated = 0
    for f in files:
        if process(f):
            updated += 1
            print(f"  OK {f.name}")
    print(f"\n{updated}/{len(files)} files updated")


if __name__ == "__main__":
    main()
