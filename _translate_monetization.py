#!/usr/bin/env python3
"""Translate editeurs.html, newsletter.html, rapports.html into EN/DE/NL via Mammouth API.
Preserves all HTML/CSS/SVG/JSON-LD structure, only translates visible text + meta content.
Handles:
- <title>, meta description, meta keywords
- og:* content
- Visible text between tags
- alt / title / aria-label / placeholder attributes
- JSON-LD "name", "description", "headline" values
- <html lang="...">
- canonical / hreflang self-reference
- Path prefixes: href="foo.html" → href="../foo.html" for internal links
"""
import os
import re
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path

# Force UTF-8 on Windows stdout
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_KEY = "sk-OIW5l3prNgJ7ZtVRA0g5RA"
API_URL = "https://api.mammouth.ai/v1/chat/completions"
MODEL = "gpt-4.1"

ROOT = Path(__file__).parent

LANGS = {
    "en": {
        "name": "English (en-US)",
        "html_lang": "en-US",
        "og_locale": "en_US",
        "title_suffix": "en",
        "system": (
            "You are a professional French→English (en-US) HTML translator for Agents-IA.pro. "
            "Natural business English, SEO-friendly, direct tone (not corporate jargon)."
        ),
    },
    "de": {
        "name": "German (de-DE)",
        "html_lang": "de-DE",
        "og_locale": "de_DE",
        "title_suffix": "de",
        "system": (
            "You are a professional French→German (de-DE) HTML translator for Agents-IA.pro. "
            "Natural business German, formal (Sie), SEO-friendly."
        ),
    },
    "nl": {
        "name": "Dutch (nl-NL)",
        "html_lang": "nl-NL",
        "og_locale": "nl_NL",
        "title_suffix": "nl",
        "system": (
            "You are a professional French→Dutch (nl-NL) HTML translator for Agents-IA.pro. "
            "Natural business Dutch, formal (u), SEO-friendly."
        ),
    },
}

SYSTEM_BASE = """
STRICT RULES:
1. Output ONLY the translated HTML. No markdown, no commentary, no code fences.
2. Preserve EXACTLY: all HTML tags, attributes, classes, ids, CSS inline styles, CSS classes, JavaScript code, SVG markup, URLs, email addresses, phone numbers, currency values and symbols (€, CHF, USD), numeric values.
3. Translate ONLY: visible text content between tags, meta content values (title, description, keywords, og:title, og:description, og:site_name, twitter:*), JSON-LD string values ("name", "description", "headline", "jobTitle", "knowsAbout"), alt/title/aria-label/placeholder attributes, text inside SVG <text> elements.
4. Do NOT translate: brand names (Agents-IA.pro, Vocalis, VAULT 369 LTD, Stripe, Beehiiv, ElevenLabs, Make, Apify, Perplexity, OpenAI, Claude, GPT, Gemini, Mammouth, IndexNow, Laurent Duplat), product-specific names, technical terms (API, SaaS, CRM, PBN, SEO, GEO, RGPD→GDPR in EN, DPA), URLs, hex colors.
5. RGPD → keep as "RGPD" in FR/DE/NL; translate to "GDPR" in EN only.
6. CNIL → keep as "CNIL" (French data protection authority proper name).
7. Keep price suffixes consistent: "€/mois" → "/month" (EN), "/Monat" (DE), "/maand" (NL); "€ HT" → "€ excl. VAT" (EN), "€ netto" (DE), "€ excl. btw" (NL).
8. JSON-LD "inLanguage" field: change "fr" → target language code (en/de/nl).
9. Preserve canonical/hreflang structure; caller will adjust URLs.
10. Output clean UTF-8.
"""


def call_api(system_prompt, fragment, retries=3):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": fragment},
        ],
        "temperature": 0.3,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 agents-ia-translator/1.0",
        },
        method="POST",
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=300) as resp:
                body = resp.read().decode("utf-8")
                obj = json.loads(body)
                content = obj["choices"][0]["message"]["content"]
                content = re.sub(r"^```(?:html)?\s*", "", content.strip())
                content = re.sub(r"\s*```$", "", content)
                return content
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code}: {e.read().decode('utf-8','ignore')[:400]}"
            print(f"    attempt {attempt+1} err: {last_err}")
            time.sleep(2**attempt)
        except Exception as e:
            last_err = str(e)
            print(f"    attempt {attempt+1} err: {last_err}")
            time.sleep(2**attempt)
    raise RuntimeError(f"API failed after {retries}: {last_err}")


def split_chunks(html, max_chars=60000):
    if len(html) <= max_chars:
        return [html]
    chunks = []
    pos = 0
    n = len(html)
    while pos < n:
        end = min(pos + max_chars, n)
        if end >= n:
            chunks.append(html[pos:])
            break
        best = -1
        for tag in ("</section>", "</div>", "</article>", "</script>", "</svg>", "</footer>"):
            idx = html.rfind(tag, pos + max_chars // 2, end)
            if idx > best:
                best = idx + len(tag)
        if best < 0:
            gt = html.rfind(">", pos + max_chars // 2, end)
            best = gt + 1 if gt > 0 else end
        chunks.append(html[pos:best])
        pos = best
    return chunks


def fix_metadata(html, lang_code, lang_cfg, base_slug):
    """Post-process: fix lang, canonical, og:locale, hreflang, relative paths."""
    # <html lang="..."> → target
    html = re.sub(r'(<html[^>]*\blang=")[^"]+(")', r'\1' + lang_cfg["html_lang"] + r'\2', html, count=1)

    # canonical → /<lang>/<slug>
    html = re.sub(
        r'(<link[^>]*rel="canonical"[^>]*href=")https://agents-ia\.pro/' + re.escape(base_slug) + r'(")',
        rf'\1https://agents-ia.pro/{lang_code}/{base_slug}\2',
        html,
    )

    # og:url
    html = re.sub(
        r'(<meta[^>]*property="og:url"[^>]*content=")https://agents-ia\.pro/' + re.escape(base_slug) + r'(")',
        rf'\1https://agents-ia.pro/{lang_code}/{base_slug}\2',
        html,
    )

    # og:locale → target
    html = re.sub(
        r'(<meta[^>]*property="og:locale"[^>]*content=")[^"]+(")',
        r'\1' + lang_cfg["og_locale"] + r'\2',
        html,
        count=1,
    )

    # JSON-LD inLanguage
    html = re.sub(r'"inLanguage":\s*"fr"', f'"inLanguage": "{lang_code}"', html)

    # Fix internal relative HTML links (e.g., href="blog.html" → href="../<lang>/blog.html" or just remain if we subdir)
    # Since the target is in /<lang>/, the links should all point to same-level /<lang>/ OR root.
    # Strategy: change href="index.html" → href="/<lang>/" or root, and href="foo.html" → href="foo.html" (same dir)
    # But nav anchors like index.html#contact stay relative within /<lang>/ subdir.
    # So we keep them as-is (they'll resolve to /<lang>/foo.html which we'll create).

    # Add alternate hreflang block if not present (we'll add at caller level)

    # Fix CSS/JS relative refs: href="css/style.css" → href="../css/style.css", src="js/app.js" → ../
    html = re.sub(r'href="css/', 'href="../css/', html)
    html = re.sub(r'src="js/', 'src="../js/', html)
    html = re.sub(r'href="favicon\.svg"', 'href="../favicon.svg"', html)

    return html


def inject_hreflang_block(html, base_slug):
    """Inject hreflang alternates right after canonical tag."""
    hreflang_block = (
        f'<link rel="alternate" hreflang="fr" href="https://agents-ia.pro/{base_slug}">\n'
        f'    <link rel="alternate" hreflang="en" href="https://agents-ia.pro/en/{base_slug}">\n'
        f'    <link rel="alternate" hreflang="de" href="https://agents-ia.pro/de/{base_slug}">\n'
        f'    <link rel="alternate" hreflang="nl" href="https://agents-ia.pro/nl/{base_slug}">\n'
        f'    <link rel="alternate" hreflang="x-default" href="https://agents-ia.pro/{base_slug}">'
    )
    # Insert after the first canonical
    pattern = re.compile(r'(<link[^>]*rel="canonical"[^>]*>)', re.IGNORECASE)
    return pattern.sub(r'\1\n    ' + hreflang_block, html, count=1)


def translate_file(src_path, lang_code, lang_cfg):
    slug = src_path.name
    dst_dir = ROOT / lang_code
    dst_dir.mkdir(exist_ok=True)
    dst_path = dst_dir / slug

    if dst_path.exists():
        print(f"  SKIP {lang_code}/{slug} (exists)")
        return

    print(f"\n=== Translating {slug} → {lang_code} ===")
    html = src_path.read_text(encoding="utf-8", errors="ignore")
    print(f"  size: {len(html)} chars")

    system_prompt = lang_cfg["system"] + "\n" + SYSTEM_BASE
    chunks = split_chunks(html)
    print(f"  chunks: {len(chunks)}")

    translated = []
    for i, ch in enumerate(chunks, 1):
        print(f"  chunk {i}/{len(chunks)}: {len(ch)} chars")
        t = call_api(system_prompt, ch)
        translated.append(t)

    result = "".join(translated)
    result = fix_metadata(result, lang_code, lang_cfg, slug)
    result = inject_hreflang_block(result, slug)

    dst_path.write_text(result, encoding="utf-8")
    print(f"  OK {dst_path} ({len(result)} bytes)")


def main():
    files = ["editeurs.html", "newsletter.html", "rapports.html"]
    for fname in files:
        src = ROOT / fname
        if not src.exists():
            print(f"MISSING {src}")
            continue
        for lang_code, cfg in LANGS.items():
            try:
                translate_file(src, lang_code, cfg)
                time.sleep(2)
            except Exception as e:
                print(f"  FAIL {fname} {lang_code}: {e}")

    # Also inject hreflang into the FR original pages
    print("\n=== Injecting hreflang into FR originals ===")
    for fname in files:
        src = ROOT / fname
        if not src.exists():
            continue
        html = src.read_text(encoding="utf-8", errors="ignore")
        if 'hreflang="en"' in html:
            print(f"  SKIP {fname} (already has hreflang)")
            continue
        html = inject_hreflang_block(html, fname)
        src.write_text(html, encoding="utf-8")
        print(f"  OK {fname}")


if __name__ == "__main__":
    main()
