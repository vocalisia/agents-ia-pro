#!/usr/bin/env python3
"""Propagate the NEW hero v2 + new language selector from FR index.html
into all 6 language versions (EN/DE/NL/ES/IT/PT).

Strategy:
1. Translate the hero v2 strings table into each target language
2. Replace the OLD hero section in each /<lang>/index.html with the new one
3. Replace the OLD lang switcher (or any variant) with the new globe-based one
   (with current lang's flag/code shown as active button)
"""
import sys
import re
import json
import time
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
    "en": ("English", "EN", "en-US"),
    "de": ("Deutsch", "DE", "de-DE"),
    "nl": ("Nederlands", "NL", "nl-NL"),
    "es": ("Español", "ES", "es-ES"),
    "it": ("Italiano", "IT", "it-IT"),
    "pt": ("Português", "PT", "pt-PT"),
}


def call_api(system, user, retries=3):
    payload = {"model": MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0.3}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL, data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 hero-translator/1.0"},
        method="POST",
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                obj = json.loads(resp.read().decode("utf-8"))
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
    raise RuntimeError(last_err)


# ============================================================================
# Extract the hero v2 block + lang selector from FR index.html
# ============================================================================
FR_INDEX = (ROOT / "index.html").read_text(encoding="utf-8", errors="ignore")

# 1. Extract <style id="hero-v2-style">...</style>
hero_style_match = re.search(r'<style id="hero-v2-style">.*?</style>', FR_INDEX, re.DOTALL)
HERO_STYLE = hero_style_match.group(0) if hero_style_match else ""

# 2. Extract <section class="hero-v2">...</section>
hero_section_match = re.search(r'<section class="hero-v2">.*?</section>', FR_INDEX, re.DOTALL)
HERO_SECTION_FR = hero_section_match.group(0) if hero_section_match else ""

# 3. Extract NEW lang selector wrapper (the entire .lang-selector div + its <script>)
lang_match = re.search(r'<!-- Language selector dropdown -->.*?</script>', FR_INDEX, re.DOTALL)
LANG_BLOCK_FR = lang_match.group(0) if lang_match else ""

print(f"Hero style: {len(HERO_STYLE)} chars")
print(f"Hero section: {len(HERO_SECTION_FR)} chars")
print(f"Lang block: {len(LANG_BLOCK_FR)} chars")


# ============================================================================
# Language-specific lang selector button (current lang shown)
# ============================================================================
def build_lang_block(active_code):
    """Returns the lang selector HTML with the active code displayed in the button."""
    return LANG_BLOCK_FR.replace(
        "<i class=\"fas fa-globe\" style=\"opacity:0.85;\"></i> FR <i class=\"fas fa-chevron-down\"",
        f"<i class=\"fas fa-globe\" style=\"opacity:0.85;\"></i> {active_code} <i class=\"fas fa-chevron-down\"",
        1,
    )


# ============================================================================
# Translate the hero section into each language via Mammouth
# ============================================================================
def translate_hero(target_name, target_locale):
    sys_prompt = f"""You are a professional French→{target_name} ({target_locale}) HTML translator for Agents-IA.pro.

STRICT RULES:
1. Output ONLY the translated HTML <section>...</section>. No commentary, no markdown, no fences.
2. Preserve EXACTLY: all HTML tags, attributes, classes, ids, CSS, JavaScript, SVG markup, URLs, hex colors, numeric values.
3. Translate ONLY: visible text, alt/title/aria-label/placeholder, text inside SVG <text>.
4. Do NOT translate: brand names (Agents-IA.pro, Vocalis, VAULT 369 LTD), URLs, technical acronyms (PME → SME in EN/DE only, otherwise keep PME).
5. Adjust currency/spelling to target locale standards.
6. Keep "🇨🇭" emoji as-is (Swiss flag).
7. The button labels "Explorer les 500+ agents" and "Audit gratuit 30 min" must be translated naturally.
8. The placeholder "Un agent IA qui peut..." must be translated naturally.
9. Output clean UTF-8.

Natural business {target_name}, formal register, SEO-friendly tone, direct/operational (not corporate jargon).
"""
    return call_api(sys_prompt, HERO_SECTION_FR)


# ============================================================================
# Replace OLD hero + OLD lang selector in each <lang>/index.html
# ============================================================================
def patch_lang_index(lang_code, hero_html, lang_label_code):
    path = ROOT / lang_code / "index.html"
    if not path.exists():
        print(f"  SKIP {lang_code}: no index.html")
        return False

    content = path.read_text(encoding="utf-8", errors="ignore")
    original = content

    # 1. Replace OLD hero section: looking for <section class="hero">...</section>
    old_hero_pat = re.compile(r'<section class="hero">.*?</section>', re.DOTALL)
    if old_hero_pat.search(content):
        # Inject hero style in <head> if not already done
        if "hero-v2-style" not in content:
            content = re.sub(r'(</head>)', HERO_STYLE + "\n" + r'\1', content, count=1)
        content = old_hero_pat.sub(hero_html, content, count=1)
        print(f"  [{lang_code}] Old hero replaced.")
    else:
        # Maybe the hero is already v2 (e.g., FR was source and new translation already incorporates it)
        print(f"  [{lang_code}] No <section class=\"hero\"> found — checking for hero-v2.")

    # 2. Replace OLD lang switcher (any variant: <div class="lang-switch">, etc.)
    # Old patterns to handle:
    #   <div class="lang-switch" style="...">...</div>
    #   <!-- Language selector dropdown --><div class="lang-selector">...</div>...<script>...</script>  (already new)
    new_lang_block = build_lang_block(lang_label_code)

    # Pattern A: old "FR EN DE NL" simple links
    old_simple_pat = re.compile(r'<div class="lang-switch"[^>]*>.*?</div>', re.DOTALL)
    if old_simple_pat.search(content):
        content = old_simple_pat.sub(new_lang_block, content, count=1)
        print(f"  [{lang_code}] Old simple lang-switch replaced.")
    # Pattern B: existing lang-selector with bug (FR FR or emoji issues) — replace it too
    elif "<!-- Language selector dropdown -->" in content:
        # Replace the entire block from comment to its </script>
        bug_pat = re.compile(r'<!-- Language selector dropdown -->.*?</script>', re.DOTALL)
        if bug_pat.search(content):
            content = bug_pat.sub(new_lang_block, content, count=1)
            print(f"  [{lang_code}] Existing lang-selector replaced.")

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    if not HERO_SECTION_FR or not LANG_BLOCK_FR:
        print("FAIL: could not extract hero or lang block from FR index.html")
        return

    # Translate hero for each language
    translations = {}
    for lang_code, (name, label_code, locale) in LANGS.items():
        print(f"\n=== Translating hero → {lang_code} ({name}) ===")
        try:
            html = translate_hero(name, locale)
            translations[lang_code] = html
            time.sleep(1)
        except Exception as e:
            print(f"  FAIL: {e}")

    # Patch each lang's index.html
    print("\n=== Patching index.html files ===")
    for lang_code, (_, label_code, _) in LANGS.items():
        if lang_code not in translations:
            continue
        try:
            patch_lang_index(lang_code, translations[lang_code], label_code)
        except Exception as e:
            print(f"  FAIL {lang_code}: {e}")


if __name__ == "__main__":
    main()
