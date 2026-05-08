#!/usr/bin/env python3
"""Add /agence.html link to footer Ressources block."""
import re
from pathlib import Path

ROOT = Path(__file__).parent


def process(path):
    if path.name == "agence.html":
        return False
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    if 'href="agence.html"' in content or 'href="../agence.html"' in content:
        return False

    # Add in footer Ressources: after /a-propos, before /editeurs
    pat = re.compile(r'(<a href="a-propos\.html">À propos</a>)(<a href="editeurs\.html">)')
    pat2 = re.compile(r'(<a href="\.\./a-propos\.html">À propos</a>)(<a href="\.\./editeurs\.html">)')
    if pat.search(content):
        content = pat.sub(r'\1<a href="agence.html">Agence</a>\2', content, count=1)
    elif pat2.search(content):
        content = pat2.sub(r'\1<a href="../agence.html">Agence</a>\2', content, count=1)
    else:
        return False

    path.write_text(content, encoding="utf-8")
    return True


def main():
    files = list(ROOT.glob("*.html"))
    files.extend((ROOT / "blog").glob("*.html"))
    updated = 0
    for f in files:
        if process(f):
            updated += 1
            print(f"  OK {f.name}")
    print(f"\n{updated} files updated")


if __name__ == "__main__":
    main()
