#!/usr/bin/env python3
# _inject_author_bio.py
# Injects author-bio HTML block + Article/Person JSON-LD schema into blog articles.
# Idempotent: skips files that already contain "author-bio".

import os
import re
import json
import sys

BLOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blog")
TODAY = "2026-05-20"

AUTHOR_BIO_HTML = '''
<!-- Author Bio -->
<div class="author-bio" style="margin-top:48px; padding:28px; background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2); border-radius:16px; display:flex; gap:20px; align-items:flex-start;">
  <div style="flex:0 0 64px; width:64px; height:64px; border-radius:50%; background:linear-gradient(135deg,#6366f1,#a855f7); display:flex; align-items:center; justify-content:center; font-size:28px; color:white;">
    <i class="fas fa-user-tie"></i>
  </div>
  <div>
    <strong style="font-size:16px;">Laurent Duplat</strong>
    <p style="color:var(--text-secondary); font-size:14px; margin:4px 0 8px;">Fondateur · Agents-IA.pro — Expert en agents IA et automatisation pour PME francophones depuis 2024.</p>
    <a href="/a-propos" style="color:var(--primary-light); font-size:13px;">Voir le profil →</a>
  </div>
</div>
'''

SCHEMA_TEMPLATE = '''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "@id": "https://agents-ia.pro/blog/{slug}#article",
  "headline": "{headline}",
  "author": {{
    "@type": "Person",
    "@id": "https://agents-ia.pro/#founder",
    "name": "Laurent Duplat",
    "url": "https://agents-ia.pro/a-propos"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Agents-IA.pro",
    "url": "https://agents-ia.pro"
  }},
  "datePublished": "{date_published}",
  "dateModified": "{today}",
  "inLanguage": "fr",
  "isPartOf": {{ "@id": "https://agents-ia.pro/#website" }}
}}
</script>'''


def extract_title(content):
    """Extract content of <title> tag."""
    m = re.search(r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
    if m:
        # Strip " | Agents-IA.pro" suffix if present
        title = m.group(1).strip()
        title = re.sub(r'\s*[\|–-].*?Agents-IA\.pro.*$', '', title, flags=re.IGNORECASE).strip()
        return title
    return ""


def extract_date_published(content):
    """Extract datePublished from existing JSON-LD."""
    m = re.search(r'"datePublished"\s*:\s*"([^"]+)"', content)
    if m:
        return m.group(1)
    return "2026-01-01"


def has_person_author_schema(content):
    """Check if a Person-typed author schema already exists."""
    return '"@type": "Person"' in content or '"type":"Person"' in content


def inject_bio(content):
    """Inject author-bio HTML before <footer or <!-- FOOTER --> marker."""
    # Try <!-- FOOTER --> first
    marker = '<!-- FOOTER -->'
    if marker in content:
        return content.replace(marker, AUTHOR_BIO_HTML + '\n' + marker, 1)
    # Fallback: before <footer
    if '<footer' in content:
        return content.replace('<footer', AUTHOR_BIO_HTML + '\n<footer', 1)
    # Last resort: before </body>
    return content.replace('</body>', AUTHOR_BIO_HTML + '\n</body>', 1)


def inject_schema(content, slug, headline, date_published):
    """Inject Article/Person schema before </head>."""
    schema = SCHEMA_TEMPLATE.format(
        slug=slug,
        headline=headline.replace('"', '\\"'),
        date_published=date_published,
        today=TODAY,
    )
    return content.replace('</head>', schema + '\n</head>', 1)


def process_file(filepath):
    slug = os.path.splitext(os.path.basename(filepath))[0]

    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    # Idempotency check
    if 'author-bio' in content:
        return 'skipped', slug

    headline = extract_title(content)
    date_published = extract_date_published(content)

    # Inject HTML bio
    content = inject_bio(content)

    # Inject schema only if Person author not yet present
    if not has_person_author_schema(content):
        content = inject_schema(content, slug, headline, date_published)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return 'modified', slug


def main():
    html_files = sorted([
        os.path.join(BLOG_DIR, f)
        for f in os.listdir(BLOG_DIR)
        if f.endswith('.html')
    ])

    modified = []
    skipped = []

    for filepath in html_files:
        status, slug = process_file(filepath)
        if status == 'modified':
            modified.append(slug)
        else:
            skipped.append(slug)

    print(f"\n=== _inject_author_bio.py report ===")
    print(f"Modified : {len(modified)}")
    for s in modified:
        print(f"  + {s}")
    print(f"Skipped  : {len(skipped)}")
    for s in skipped:
        print(f"  ~ {s}")
    print("====================================\n")


if __name__ == '__main__':
    main()
