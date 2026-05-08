#!/usr/bin/env python3
"""Update ecosystem footer block on all agents-ia.pro pages.
Replace single Ecosystem block with expanded 13-site network (split 7+6 for balance).
Handles FR, EN, DE, NL variants + minified HTML.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Each row: (heading_pattern, new_block_html, lang_suffix_for_second_block)
LANGS = {
    "fr": {
        "heading_variants": ["Écosystème", "Ecosysteme", "Ecosystème"],
        "heading": "Écosystème",
        "heading2": "Services IA",
        "resources": "Ressources",
    },
    "en": {
        "heading_variants": ["Ecosystem"],
        "heading": "Ecosystem",
        "heading2": "AI Services",
        "resources": "Resources",
    },
    "de": {
        "heading_variants": ["Ökosystem", "Oekosystem"],
        "heading": "Ökosystem",
        "heading2": "KI-Services",
        "resources": "Ressourcen",
    },
    "nl": {
        "heading_variants": ["Ecosysteem"],
        "heading": "Ecosysteem",
        "heading2": "AI-Diensten",
        "resources": "Hulpbronnen",
    },
}

# 13 external sites + self (14th as regular link)
ECOSYSTEM_BLOCK_1 = [
    ("https://vocalis.pro", "Vocalis.pro", "nofollow"),
    ("https://vocalis.blog", "Vocalis.blog", "nofollow"),
    ("https://vocalis-ai.org", "Vocalis-AI.org", "nofollow"),
    ("https://ai-due.com", "AI-DUE.com", "nofollow"),
    ("https://tesla-mag.ch", "Tesla-Mag.ch", "nofollow"),
    ("https://master-seller.fr", "Master-Seller.fr", "nofollow"),
    ("https://iapmesuisse.ch", "IAPMESuisse.ch", "nofollow"),
]

ECOSYSTEM_BLOCK_2 = [
    ("https://seo-true.com", "SEO-True.com", "nofollow"),
    ("https://trustly-ai.com", "Trustly-AI.com", "nofollow"),
    ("https://trust-vault.com", "Trust-Vault.com", "nofollow"),
    ("https://agentic-whatsup.com", "Agentic-WhatsUp.com", "nofollow"),
    ("https://lead-gene.com", "Lead-Gene.com", "nofollow"),
    ("https://xn--factureimpaye-6ya.fr", "Factureimpayée.fr", "nofollow"),
]


def build_block(heading, links):
    html = f'<div class="footer-links"><h4>{heading}</h4>'
    for url, label, rel in links:
        html += f'<a href="{url}" target="_blank" rel="noopener {rel}">{label}</a>'
    html += "</div>"
    return html


def process_file(path: Path):
    content = path.read_text(encoding="utf-8", errors="ignore")
    original = content
    modified = False

    for lang_code, labels in LANGS.items():
        heading2 = labels["heading2"]

        for variant in labels["heading_variants"]:
            pattern = re.compile(
                r'<div class="footer-links">\s*<h4>\s*' + re.escape(variant) + r'\s*</h4>.*?</div>',
                re.DOTALL,
            )

            match = pattern.search(content)
            if not match:
                continue

            new_block_1 = build_block(variant, ECOSYSTEM_BLOCK_1)
            new_block_2 = build_block(heading2, ECOSYSTEM_BLOCK_2)
            replacement = new_block_1 + new_block_2

            new_content = pattern.sub(replacement, content, count=1)
            if new_content != content:
                content = new_content
                modified = True
                print(f"  [{lang_code}/{variant}] {path.name}: replaced Ecosystem block")
                break

    if modified and content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    # Collect all HTML files (root, en/, de/, nl/, blog/)
    html_files = []
    html_files.extend(ROOT.glob("*.html"))
    for sub in ["en", "de", "nl", "blog"]:
        d = ROOT / sub
        if d.exists():
            html_files.extend(d.glob("*.html"))

    print(f"Found {len(html_files)} HTML files\n")

    updated = 0
    for f in html_files:
        try:
            if process_file(f):
                updated += 1
        except Exception as e:
            print(f"  ERROR {f.name}: {e}")

    print(f"\n{updated}/{len(html_files)} files updated")


if __name__ == "__main__":
    main()
