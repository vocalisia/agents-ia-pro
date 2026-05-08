#!/usr/bin/env python3
"""Inject an affiliate 'Stack IA recommandée' block in blog articles.
Only injects if not already present.

Affiliate programs (replace REF codes once accounts created):
- ElevenLabs: ?ref=duplat  (20% lifetime commission)
- Make.com: ?pc=duplat    (30% first year)
- OpenAI: (no affiliate, use API credits via Azure or RevenueCat)
- Perplexity: ?referral=DUPLAT (credits back)
- n8n (self-host), Cal.com, Beehiiv (25% lifetime)
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
BLOG = ROOT / "blog"

AFFILIATE_HTML = """
<!-- ====== STACK IA RECOMMANDÉE (affiliate) ====== -->
<div style="margin:48px 0; padding:32px; background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.08); border-radius:16px;">
    <span style="display:inline-block; padding:4px 12px; background:rgba(251,146,60,0.2); color:#fdba74; border-radius:999px; font-size:11px; font-weight:700; letter-spacing:1px; margin-bottom:12px;">💡 STACK RECOMMANDÉE</span>
    <h3 style="margin:0 0 8px;">Les outils IA qu'on utilise réellement chez Agents-IA.pro</h3>
    <p style="color:var(--text-secondary); font-size:14px; margin:0 0 20px;">Sélection personnelle, testée en production. <em>Liens partenaires</em> — le prix pour vous est identique, on touche une commission si vous vous abonnez.</p>
    <div style="display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px;">
        <a href="https://elevenlabs.io/?from=partnerduplat" target="_blank" rel="noopener sponsored" onclick="gtag('event','affiliate_click',{partner:'elevenlabs'});" style="padding:14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">🎙️ ElevenLabs</div>
            <div style="font-size:12px; color:var(--text-secondary);">Voix IA multilingues premium</div>
        </a>
        <a href="https://www.make.com/en/register?pc=duplat" target="_blank" rel="noopener sponsored" onclick="gtag('event','affiliate_click',{partner:'make'});" style="padding:14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">⚙️ Make.com</div>
            <div style="font-size:12px; color:var(--text-secondary);">Automatisation no-code</div>
        </a>
        <a href="https://www.apify.com/sign-up?fpr=duplat" target="_blank" rel="noopener sponsored" onclick="gtag('event','affiliate_click',{partner:'apify'});" style="padding:14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">🕷️ Apify</div>
            <div style="font-size:12px; color:var(--text-secondary);">Web scraping + data IA</div>
        </a>
        <a href="https://www.perplexity.ai/?referral=DUPLAT" target="_blank" rel="noopener sponsored" onclick="gtag('event','affiliate_click',{partner:'perplexity'});" style="padding:14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">🔍 Perplexity Pro</div>
            <div style="font-size:12px; color:var(--text-secondary);">Recherche IA sourcée</div>
        </a>
        <a href="https://www.beehiiv.com/?via=duplat" target="_blank" rel="noopener sponsored" onclick="gtag('event','affiliate_click',{partner:'beehiiv'});" style="padding:14px; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.1); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">📬 Beehiiv</div>
            <div style="font-size:12px; color:var(--text-secondary);">Newsletter SaaS pro</div>
        </a>
        <a href="https://vocalis.pro/?ref=agents-ia" target="_blank" rel="noopener" onclick="gtag('event','affiliate_click',{partner:'vocalis'});" style="padding:14px; background:linear-gradient(135deg, rgba(99,102,241,0.2), rgba(168,85,247,0.15)); border:1px solid rgba(99,102,241,0.4); border-radius:10px; text-decoration:none; color:white; display:block;">
            <div style="font-weight:700; margin-bottom:4px;">🤖 Vocalis.pro</div>
            <div style="font-size:12px; color:var(--text-secondary);">Notre agent vocal IA (interne)</div>
        </a>
    </div>
</div>
<!-- ====== /STACK IA RECOMMANDÉE ====== -->
"""


def process(path: Path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False
    if "STACK IA RECOMMANDÉE" in content:
        return False

    # Insert before the final CTA box (pattern: "Besoin d'un agent IA" or "Un projet d'agent IA")
    patterns = [
        r'<div\s+style="margin-top:48px; padding:32px; background:linear-gradient\(135deg, rgba\(99,102,241,0\.1\), rgba\(168,85,247,0\.1\)\);',
    ]
    for pat in patterns:
        m = re.search(pat, content)
        if m:
            insert_at = m.start()
            new = content[:insert_at] + AFFILIATE_HTML + "\n\n            " + content[insert_at:]
            path.write_text(new, encoding="utf-8")
            return True
    return False


def main():
    files = list(BLOG.glob("*.html"))
    updated = 0
    for f in files:
        if process(f):
            updated += 1
            print(f"  OK {f.name}")
    print(f"\n{updated}/{len(files)} blog articles updated")


if __name__ == "__main__":
    main()
