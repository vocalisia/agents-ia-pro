#!/usr/bin/env python3
"""Inject ecosystem block into minimal footers on agents-ia.pro pages."""
import re
from pathlib import Path

ROOT = Path(__file__).parent

ECOSYSTEM_BLOCK_1 = [
    ("https://vocalis.pro", "Vocalis.pro"),
    ("https://vocalis.blog", "Vocalis.blog"),
    ("https://vocalis-ai.org", "Vocalis-AI.org"),
    ("https://ai-due.com", "AI-DUE.com"),
    ("https://tesla-mag.ch", "Tesla-Mag.ch"),
    ("https://master-seller.fr", "Master-Seller.fr"),
    ("https://iapmesuisse.ch", "IAPMESuisse.ch"),
]

ECOSYSTEM_BLOCK_2 = [
    ("https://seo-true.com", "SEO-True.com"),
    ("https://trustly-ai.com", "Trustly-AI.com"),
    ("https://trust-vault.com", "Trust-Vault.com"),
    ("https://agentic-whatsup.com", "Agentic-WhatsUp.com"),
    ("https://lead-gene.com", "Lead-Gene.com"),
    ("https://xn--factureimpaye-6ya.fr", "Factureimpayée.fr"),
]


def build_footer_grid(heading1, heading2):
    html = '<div class="footer-grid">'
    html += f'<div class="footer-links"><h4>{heading1}</h4>'
    for url, label in ECOSYSTEM_BLOCK_1:
        html += f'<a href="{url}" target="_blank" rel="noopener nofollow">{label}</a>'
    html += "</div>"
    html += f'<div class="footer-links"><h4>{heading2}</h4>'
    for url, label in ECOSYSTEM_BLOCK_2:
        html += f'<a href="{url}" target="_blank" rel="noopener nofollow">{label}</a>'
    html += "</div>"
    html += "</div>"
    return html


TARGETS = [
    "agent-commercial.html",
    "agent-support.html",
    "agent.html",
    "categories.html",
    "blog.html",
    "submit.html",
]


def process(path: Path, heading1="Écosystème", heading2="Services IA"):
    if not path.exists():
        return False

    content = path.read_text(encoding="utf-8", errors="ignore")

    # Look for the minimal footer pattern and inject ecosystem-grid BEFORE footer-bottom
    # Pattern: <footer class="footer">\s*<div class="container">\s*<div class="footer-bottom">
    pattern = re.compile(
        r'(<footer class="footer">\s*<div class="container">\s*)(<div class="footer-bottom">)',
        re.DOTALL,
    )

    if not pattern.search(content):
        print(f"  SKIP {path.name}: no minimal footer pattern")
        return False

    # Already injected?
    if "iapmesuisse" in content:
        print(f"  SKIP {path.name}: already has new ecosystem")
        return False

    grid = build_footer_grid(heading1, heading2)
    new_content = pattern.sub(r'\1' + grid + r'\2', content)

    path.write_text(new_content, encoding="utf-8")
    print(f"  UPDATE {path.name}: injected ecosystem grid")
    return True


def main():
    updated = 0
    for name in TARGETS:
        if process(ROOT / name):
            updated += 1
    print(f"\n{updated}/{len(TARGETS)} files updated")


if __name__ == "__main__":
    main()
