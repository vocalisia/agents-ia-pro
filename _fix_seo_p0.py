"""P0/P1 SEO fixes for agents-ia.pro:
1. Remove duplicate canonical L8 from index.html
2. Fix canonical URLs: strip .html (cleanUrls=true on Vercel)
3. Fix sitemap.xml: strip .html from <loc> entries
4. Fix og-image.png -> og-image.svg (real file is SVG, .png = 404)
5. Expand llms.txt (3 URLs -> all ~70 pages)
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_DIRS = {"node_modules", ".next", ".vercel", ".git", "rapports-pdf"}
BASE_URL = "https://agents-ia.pro"

results = {}

# --- 1. Remove duplicate canonical in index.html ---
idx = ROOT / "index.html"
text = idx.read_text(encoding="utf-8")
lines = text.splitlines(keepends=True)
# Find all canonical line indices
can_lines = [i for i, l in enumerate(lines) if 'rel="canonical"' in l]
if len(can_lines) >= 2:
    # Remove the first occurrence (early duplicate, keep the one in Canonical&Hreflang section)
    del lines[can_lines[0]]
    idx.write_text("".join(lines), encoding="utf-8")
    results["index_canonical_dedup"] = f"removed duplicate at original L{can_lines[0]+1}"
else:
    results["index_canonical_dedup"] = "already ok (1 canonical)"

# --- 2. Fix canonical .html -> clean URL in root HTML files ---
CANONICAL_RE = re.compile(
    r'(<link rel="canonical" href="https://agents-ia\.pro/)([^"]+)(\.html)(")'
)
canonical_fixed = []
for path in ROOT.glob("*.html"):
    text = path.read_text(encoding="utf-8")
    new_text = CANONICAL_RE.sub(r'\1\2\4', text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        canonical_fixed.append(path.name)
results["canonical_clean_urls"] = f"fixed {len(canonical_fixed)} files: {canonical_fixed}"

# --- 3. Fix og-image.png -> og-image.svg ---
OG_PNG_RE = re.compile(r'og-image\.png')
og_fixed = []
for path in ROOT.rglob("*.html"):
    if any(p in SKIP_DIRS for p in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    new_text = OG_PNG_RE.sub("og-image.svg", text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        og_fixed.append(str(path.relative_to(ROOT)))
results["og_image_fix"] = f"fixed {len(og_fixed)} files"

# --- 4. Fix sitemap.xml: strip .html from <loc> entries ---
sitemap = ROOT / "sitemap.xml"
if sitemap.exists():
    sm_text = sitemap.read_text(encoding="utf-8")
    # Strip .html from <loc>...</loc> entries but preserve blog/ paths only if they were there
    sm_new = re.sub(
        r'(<loc>https://agents-ia\.pro/(?!blog/|de/blog/|en/blog/|es/blog/|it/blog/|nl/blog/|pt/blog/)([^<]*))\.html(</loc>)',
        r'\1\3',
        sm_text
    )
    if sm_new != sm_text:
        count = sm_text.count(".html</loc>") - sm_new.count(".html</loc>")
        sitemap.write_text(sm_new, encoding="utf-8")
        results["sitemap_clean_urls"] = f"fixed {count} .html -> clean URLs"
    else:
        results["sitemap_clean_urls"] = "already clean"

# --- 5. Expand llms.txt ---
# Collect all root + multilang HTML pages (exclude rapports-pdf, blog mirrors, legal dupes)
pages = []
# Root pages
for p in sorted(ROOT.glob("*.html")):
    slug = p.stem
    if slug in ("newsletter-issue-13-2026-04-29", "404"):
        continue
    url = f"{BASE_URL}/{slug}" if slug != "index" else BASE_URL + "/"
    pages.append(url)
# Blog pages
for p in sorted((ROOT / "blog").glob("*.html")):
    pages.append(f"{BASE_URL}/blog/{p.stem}")
# Multilang index pages
for lang in ["en", "de", "nl", "es", "it", "pt"]:
    lang_dir = ROOT / lang
    if lang_dir.exists():
        pages.append(f"{BASE_URL}/{lang}/")

llms_content = f"""# Agents-IA.pro - LLM Access File
> Marketplace #1 d'agents IA pour PME francophones. 500+ agents IA vérifiés.
> Fondée par Laurent Duplat, basée en Suisse.

## Sitemap complet ({len(pages)} URLs)

""" + "\n".join(f"- {url}" for url in pages)

(ROOT / "llms.txt").write_text(llms_content, encoding="utf-8")
results["llms_txt"] = f"expanded to {len(pages)} URLs"

# --- Report ---
for k, v in results.items():
    print(f"{k}: {v}")
