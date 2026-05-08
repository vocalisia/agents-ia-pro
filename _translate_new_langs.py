#!/usr/bin/env python3
"""Translate core monetization pages to ES/IT/PT via Mammouth.
Pages: index.html (home), editeurs, newsletter, rapports, agence, a-propos.
"""
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

LANGS = {
    "es": {
        "html_lang": "es-ES",
        "og_locale": "es_ES",
        "system": "You are a professional French→Spanish (es-ES) HTML translator for Agents-IA.pro. Natural business Spanish (Castellano), formal (usted), SEO-friendly.",
    },
    "it": {
        "html_lang": "it-IT",
        "og_locale": "it_IT",
        "system": "You are a professional French→Italian (it-IT) HTML translator for Agents-IA.pro. Natural business Italian, formal (Lei), SEO-friendly.",
    },
    "pt": {
        "html_lang": "pt-PT",
        "og_locale": "pt_PT",
        "system": "You are a professional French→Portuguese (pt-PT, European Portuguese) HTML translator for Agents-IA.pro. Natural business Portuguese, formal, SEO-friendly.",
    },
}

SYSTEM_BASE = """
STRICT RULES:
1. Output ONLY translated HTML. No markdown, no fences.
2. Preserve EXACTLY: all HTML tags, attributes, classes, ids, CSS inline styles, JavaScript, SVG, URLs, emails, phones, currency, hex colors, numeric values, JSON-LD structure.
3. Translate: visible text, meta (title, description, keywords, og:*), JSON-LD "name"/"description"/"headline"/"jobTitle"/"knowsAbout", alt/title/aria-label/placeholder.
4. Do NOT translate: brand names (Agents-IA.pro, Vocalis, VAULT 369 LTD, Stripe, Beehiiv, ElevenLabs, Make, Apify, Perplexity, OpenAI, Claude, GPT, Gemini, Mammouth, IndexNow, Laurent Duplat, WhatsApp Business, Vapi, Bland, Retell, Dext, Qonto, Brevo), technical acronyms (API, SaaS, CRM, PBN, SEO, GEO, DPA, DPIA, RGPD→GDPR in ES/IT/PT is optional, keep RGPD for FR-speakers familiarity).
5. RGPD → keep as "RGPD" in ES/IT/PT (international recognition).
6. CNIL → keep as "CNIL" (proper name).
7. JSON-LD "inLanguage": "fr" → target lang code.
8. Preserve <html lang="fr"> — patched post-processing.
9. Output clean UTF-8.
"""

# Pages to translate + base_slug (used for canonical)
PAGES = [
    ("index.html", "index.html"),
    ("editeurs.html", "editeurs.html"),
    ("newsletter.html", "newsletter.html"),
    ("rapports.html", "rapports.html"),
    ("agence.html", "agence.html"),
    ("a-propos.html", "a-propos.html"),
]


def call_api(system, user, retries=3):
    payload = {"model": MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0.3}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 agents-ia-translator/1.0"},
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
            last_err = f"HTTP {e.code}"
            time.sleep(2 ** attempt)
        except Exception as e:
            last_err = str(e)
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


def fix_metadata(html, lang_code, lang_cfg, slug):
    html = re.sub(r'(<html[^>]*\blang=")[^"]+(")', r'\1' + lang_cfg["html_lang"] + r'\2', html, count=1)
    # canonical: handle root / and slug
    if slug == "index.html":
        html = re.sub(r'(<link[^>]*rel="canonical"[^>]*href=")https://agents-ia\.pro/?(")', rf'\1https://agents-ia.pro/{lang_code}/\2', html)
        html = re.sub(r'(<meta[^>]*property="og:url"[^>]*content=")https://agents-ia\.pro/?(")', rf'\1https://agents-ia.pro/{lang_code}/\2', html)
    else:
        html = re.sub(
            r'(<link[^>]*rel="canonical"[^>]*href=")https://agents-ia\.pro/' + re.escape(slug) + r'(")',
            rf'\1https://agents-ia.pro/{lang_code}/{slug}\2',
            html,
        )
        html = re.sub(
            r'(<meta[^>]*property="og:url"[^>]*content=")https://agents-ia\.pro/' + re.escape(slug) + r'(")',
            rf'\1https://agents-ia.pro/{lang_code}/{slug}\2',
            html,
        )
    html = re.sub(r'(<meta[^>]*property="og:locale"[^>]*content=")[^"]+(")', r'\1' + lang_cfg["og_locale"] + r'\2', html, count=1)
    html = re.sub(r'"inLanguage":\s*"fr"', f'"inLanguage": "{lang_code}"', html)
    # Fix CSS/JS relative paths for /<lang>/ subdir
    html = re.sub(r'href="css/', 'href="../css/', html)
    html = re.sub(r'src="js/', 'src="../js/', html)
    html = re.sub(r'href="favicon\.svg"', 'href="../favicon.svg"', html)
    html = re.sub(r'href="logo\.svg"', 'href="../logo.svg"', html)
    return html


def translate_page(fname, slug, lang_code, lang_cfg):
    src = ROOT / fname
    dst_dir = ROOT / lang_code
    dst_dir.mkdir(exist_ok=True)
    dst = dst_dir / fname
    if dst.exists():
        print(f"  SKIP {lang_code}/{fname}")
        return
    print(f"\n=== {fname} → {lang_code} ===")
    html = src.read_text(encoding="utf-8", errors="ignore")
    print(f"  size: {len(html)} chars")

    chunks = split_chunks(html)
    print(f"  chunks: {len(chunks)}")

    translated = []
    for i, ch in enumerate(chunks, 1):
        print(f"  chunk {i}/{len(chunks)}")
        t = call_api(lang_cfg["system"] + "\n" + SYSTEM_BASE, ch)
        translated.append(t)

    result = "".join(translated)
    result = fix_metadata(result, lang_code, lang_cfg, slug)
    dst.write_text(result, encoding="utf-8")
    print(f"  OK {dst}")


def main():
    for fname, slug in PAGES:
        src = ROOT / fname
        if not src.exists():
            continue
        for lang_code, cfg in LANGS.items():
            try:
                translate_page(fname, slug, lang_code, cfg)
                time.sleep(1)
            except Exception as e:
                print(f"  FAIL {fname} {lang_code}: {e}")


if __name__ == "__main__":
    main()
