#!/usr/bin/env python3
"""Add /a-propos.html link to nav and footer Ressources on all FR pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent


def process(path: Path):
    if "a-propos" in path.name:
        return False
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False

    original = content
    modified = False

    # 1. Add to nav (after Blog link)
    # Pattern: <a href="blog.html" class="nav-link">Blog</a>
    nav_pattern = re.compile(
        r'(<a\s+href="blog\.html"\s+class="nav-link">Blog</a>)',
        re.IGNORECASE,
    )
    if nav_pattern.search(content) and 'href="a-propos' not in content[:content.find('</nav>') if '</nav>' in content else len(content)]:
        content = nav_pattern.sub(r'\1\n            <a href="a-propos.html" class="nav-link">À propos</a>', content, count=1)
        modified = True

    # 2. Add to footer Ressources block
    # Patterns like <h4>Ressources</h4>\s*<a href="blog.html">Blog</a>
    res_pattern = re.compile(
        r'(<h4>Ressources</h4>\s*<a href="blog\.html">Blog</a>)(?!\s*<a href="a-propos)',
        re.IGNORECASE | re.DOTALL,
    )
    if res_pattern.search(content):
        content = res_pattern.sub(r'\1<a href="a-propos.html">À propos</a>', content, count=1)
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
        try:
            if process(f):
                updated += 1
                print(f"  UPDATE {f.name}")
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")
    print(f"\n{updated}/{len(files)} files updated")


if __name__ == "__main__":
    main()
