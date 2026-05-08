#!/usr/bin/env python3
"""Translate 5 fresh blog articles to EN/DE/NL via Mammouth API."""
import os
import re
import sys
import time
import json
import urllib.request
import urllib.error
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_KEY = "sk-OIW5l3prNgJ7ZtVRA0g5RA"
API_URL = "https://api.mammouth.ai/v1/chat/completions"
MODEL = "gpt-4.1"

ROOT = Path(__file__).parent
BLOG_SRC = ROOT / "blog"

ARTICLES = [
    "gpt5-vs-claude-opus-agents-ia-2026.html",
    "prix-agent-ia-2026-tarifs-reels.html",
    "agent-ia-vocal-assurance-cas-usage.html",
    "agents-ia-whatsapp-business-guide-2026.html",
    "rgpd-agents-ia-cnil-2026-checklist.html",
]

LANGS = {
    "en": {
        "html_lang": "en-US",
        "og_locale": "en_US",
        "system": "You are a professional French→English (en-US) HTML translator for Agents-IA.pro. Natural business English, SEO-friendly, direct tone.",
    },
    "de": {
        "html_lang": "de-DE",
        "og_locale": "de_DE",
        "system": "You are a professional French→German (de-DE) HTML translator for Agents-IA.pro. Natural business German, formal (Sie), SEO-friendly.",
    },
    "nl": {
        "html_lang": "nl-NL",
        "og_locale": "nl_NL",
        "system": "You are a professional French→Dutch (nl-NL) HTML translator for Agents-IA.pro. Natural business Dutch, formal (u), SEO-friendly.",
    },
}

SYSTEM_BASE = """
STRICT RULES:
1. Output ONLY translated HTML. No markdown, no fences, no commentary.
2. Preserve EXACTLY: all HTML tags, attributes, classes, ids, CSS inline styles, JavaScript, SVG, URLs, emails, phone numbers, currency values, hex colors, numeric values, JSON-LD structure.
3. Translate: visible text, meta content (title, description, keywords, og:*, article:*), JSON-LD "headline"/"description"/"name"/"articleSection"/"keywords", alt/title/aria-label/placeholder.
4. Do NOT translate: brand names (Agents-IA.pro, Vocalis, VAULT 369 LTD, Stripe, Beehiiv, ElevenLabs, Make, Apify, Perplexity, OpenAI, Claude, GPT, Gemini, Mammouth, IndexNow, Laurent Duplat, WhatsApp Business, Vapi, Bland, Retell), product names, technical acronyms (API, SaaS, CRM, PBN, SEO, GEO, DPA, DPIA).
5. RGPD → "GDPR" in EN only. CNIL → keep "CNIL" in all languages (proper name).
6. JSON-LD "inLanguage": "fr" → target lang code.
7. Preserve <html lang="fr"> — will be patched post-processing.
8. Output clean UTF-8.
"""


def call_api(system, user, retries=3):
    payload = {
        "model": MODEL,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "temperature": 0.3,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 agents-ia-blog-translator/1.0",
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
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
            print(f"    attempt {attempt+1} err: {last_err}")
            time.sleep(2 ** attempt)
    raise RuntimeError(f"API failed: {last_err}")


def split_chunks(html, max_chars=55000):
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
        for tag in ("</section>", "</div>", "</article>", "</script>", "</svg>", "</footer>", "</p>"):
            idx = html.rfind(tag, pos + max_chars // 2, end)
            if idx > best:
                best = idx + len(tag)
        if best < 0:
            gt = html.rfind(">", pos + max_chars // 2, end)
            best = gt + 1 if gt > 0 else end
        chunks.append(html[pos:best])
        pos = best
    return chunks


def fix_metadata(html, lang_code, lang_cfg, article_slug):
    """Post-process lang, canonical, og:locale, hreflang, internal paths."""
    html = re.sub(r'(<html[^>]*\blang=")[^"]+(")', r'\1' + lang_cfg["html_lang"] + r'\2', html, count=1)
    html = re.sub(
        r'(<link[^>]*rel="canonical"[^>]*href=")https://agents-ia\.pro/blog/' + re.escape(article_slug) + r'(")',
        rf'\1https://agents-ia.pro/{lang_code}/blog/{article_slug}\2',
        html,
    )
    html = re.sub(
        r'(<meta[^>]*property="og:url"[^>]*content=")https://agents-ia\.pro/blog/' + re.escape(article_slug) + r'(")',
        rf'\1https://agents-ia.pro/{lang_code}/blog/{article_slug}\2',
        html,
    )
    html = re.sub(r'(<meta[^>]*property="og:locale"[^>]*content=")[^"]+(")', r'\1' + lang_cfg["og_locale"] + r'\2', html, count=1)
    html = re.sub(r'"inLanguage":\s*"fr"', f'"inLanguage": "{lang_code}"', html)

    # Fix relative paths: blog article is in <lang>/blog/ so .. = <lang>/, ../.. = root
    # But the original has href="../index.html" etc.; keeping them means they'd point to /<lang>/<foo>.
    # We want articles in /<lang>/blog/ to link to /<lang>/index.html, /<lang>/blog.html, /<lang>/a-propos.html
    # The original has:
    #   href="../index.html" → pointing to /blog/.. = root index.html (FR)
    #   href="../blog.html"  → root blog (FR)
    # After translation these should be:
    #   href="../index.html" → /<lang>/blog/.. = /<lang>/index.html (wait, we don't have /<lang>/blog/ so path must adjust)
    # Actually we put translated articles in /<lang>/blog/*.html. From there:
    #   ../ = /<lang>/
    # So ../index.html = /<lang>/index.html (which exists), ../blog.html = /<lang>/blog.html (may not exist)
    # Keep the ../ structure as-is, it's correct.

    # CSS and JS paths: original ../css/, ../js/ — still valid from /<lang>/blog/
    # Actually from /<lang>/blog/*.html we need ../../css/ and ../../js/
    html = re.sub(r'href="\.\./css/', 'href="../../css/', html)
    html = re.sub(r'src="\.\./js/', 'src="../../js/', html)
    html = re.sub(r'href="\.\./favicon\.svg"', 'href="../../favicon.svg"', html)

    return html


def inject_hreflang(html, article_slug):
    block = (
        f'<link rel="alternate" hreflang="fr" href="https://agents-ia.pro/blog/{article_slug}">\n'
        f'    <link rel="alternate" hreflang="en" href="https://agents-ia.pro/en/blog/{article_slug}">\n'
        f'    <link rel="alternate" hreflang="de" href="https://agents-ia.pro/de/blog/{article_slug}">\n'
        f'    <link rel="alternate" hreflang="nl" href="https://agents-ia.pro/nl/blog/{article_slug}">\n'
        f'    <link rel="alternate" hreflang="x-default" href="https://agents-ia.pro/blog/{article_slug}">'
    )
    pat = re.compile(r'(<link[^>]*rel="canonical"[^>]*>)', re.IGNORECASE)
    return pat.sub(r'\1\n    ' + block, html, count=1)


def translate_article(src_path, lang_code, lang_cfg):
    slug = src_path.name
    dst_dir = ROOT / lang_code / "blog"
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / slug

    if dst_path.exists():
        print(f"  SKIP {lang_code}/blog/{slug}")
        return

    print(f"\n=== {slug} → {lang_code} ===")
    html = src_path.read_text(encoding="utf-8", errors="ignore")
    print(f"  size: {len(html)} chars")

    system = lang_cfg["system"] + "\n" + SYSTEM_BASE
    chunks = split_chunks(html)
    print(f"  chunks: {len(chunks)}")

    translated = []
    for i, ch in enumerate(chunks, 1):
        print(f"  chunk {i}/{len(chunks)}")
        t = call_api(system, ch)
        translated.append(t)

    result = "".join(translated)
    result = fix_metadata(result, lang_code, lang_cfg, slug)
    result = inject_hreflang(result, slug)
    dst_path.write_text(result, encoding="utf-8")
    print(f"  OK {dst_path} ({len(result)} bytes)")


def main():
    for art in ARTICLES:
        src = BLOG_SRC / art
        if not src.exists():
            print(f"MISSING {src}")
            continue
        for lang_code, cfg in LANGS.items():
            try:
                translate_article(src, lang_code, cfg)
                time.sleep(1)
            except Exception as e:
                print(f"  FAIL {art} {lang_code}: {e}")

    # Inject hreflang into FR originals
    print("\n=== Injecting hreflang into FR blog originals ===")
    for art in ARTICLES:
        src = BLOG_SRC / art
        if not src.exists():
            continue
        html = src.read_text(encoding="utf-8", errors="ignore")
        if 'hreflang="en"' in html:
            print(f"  SKIP {art}")
            continue
        html = inject_hreflang(html, art)
        src.write_text(html, encoding="utf-8")
        print(f"  OK {art}")


if __name__ == "__main__":
    main()
