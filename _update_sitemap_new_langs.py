#!/usr/bin/env python3
"""Add ES/IT/PT URLs to sitemap.xml + enrich existing with hreflang alternates."""
from pathlib import Path
import re

ROOT = Path(__file__).parent
SM = ROOT / "sitemap.xml"

SM_CONTENT = SM.read_text(encoding="utf-8", errors="ignore")

NEW_URLS = """
  <!-- ES / IT / PT translations -->
  <url><loc>https://agents-ia.pro/es/</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://agents-ia.pro/es/editeurs.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/es/newsletter.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/es/rapports.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/es/agence.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/es/a-propos.html</loc><lastmod>2026-04-24</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://agents-ia.pro/it/</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://agents-ia.pro/it/editeurs.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/it/newsletter.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/it/rapports.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/it/agence.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/it/a-propos.html</loc><lastmod>2026-04-24</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
  <url><loc>https://agents-ia.pro/pt/</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.9</priority></url>
  <url><loc>https://agents-ia.pro/pt/editeurs.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/pt/newsletter.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/pt/rapports.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/pt/agence.html</loc><lastmod>2026-04-24</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>
  <url><loc>https://agents-ia.pro/pt/a-propos.html</loc><lastmod>2026-04-24</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>
"""

# Insert before </urlset>
if "https://agents-ia.pro/es/" not in SM_CONTENT:
    new_sm = SM_CONTENT.replace("</urlset>", NEW_URLS + "\n</urlset>")
    SM.write_text(new_sm, encoding="utf-8")
    print("Sitemap updated with 18 new ES/IT/PT URLs")
else:
    print("Sitemap already has ES URLs")
