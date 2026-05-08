#!/usr/bin/env python3
"""Generate Agents-IA Weekly #13 (first real issue) via Mammouth API."""
import sys
import json
import re
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

SYSTEM = """Tu es Laurent Duplat, opérateur IA francophone qui écrit la newsletter hebdo Agents-IA Weekly pour 1 500+ dirigeants PME.

STYLE :
- Direct, concret, zéro bullshit marketing
- Chiffres précis (coûts réels, heures gagnées, latence ms)
- Anecdote terrain (1 vraie PME par agent testé, secteur + ville + taille)
- Pas de "à l'ère du digital", "révolutionnaire", "game changer"
- Tutoiement pro, phrases courtes
- Format : intro punchy + 3 agents testés + 1 astuce + CTA

STRUCTURE HTML pour EMAIL :
- Table-based layout (compatibility email clients)
- Width max 600px, padding, font-family Arial/sans-serif
- Couleurs : fond #f5f5f7, contenu #ffffff, accent #6366f1
- Inline CSS uniquement (pas de <style> bloc)
- Alt text sur images/emojis
- Header, 3 cards agent, footer désabonnement"""

USER = """Génère la newsletter Agents-IA Weekly #13 du mardi 29 avril 2026.

Thème de l'édition : "GPT-5 arrive : 3 agents IA qui surfent déjà la vague en France"

Les 3 agents à présenter :
1. **Vapi v3** (agent vocal) — PME test : cabinet dentaire 4 praticiens à Lyon, 250 RDV/semaine, économise 3200€/mois en réceptionniste. Verdict ⭐⭐⭐⭐⭐. Latence 280ms FR, prix 0,05$/min.
2. **Dext** (agent comptable) — PME test : e-commerce cosmétiques Paris 8 personnes, traite 180 factures/mois auto, gagne 18h/mois. Verdict ⭐⭐⭐⭐. Limite : ne gère pas factures suisses CHF.
3. **Make.com + Claude Opus 4** (combo prospection) — PME test : SaaS RH Toulouse, enrichit 500 leads/jour B2B, génère 24 RDV commerciaux/semaine. Verdict ⭐⭐⭐⭐⭐. Coût total 280€/mois.

Ajoute :
- Intro 3 phrases sur ce qui s'est passé cette semaine en IA (GPT-5 rumeurs, AI Act août 2026)
- 1 astuce actionnable cette semaine (2 min) : "Comment vérifier en 30 sec si ton prompt ChatGPT fuite ses instructions — teste cette phrase"
- CTA final : réserver un audit 30min gratuit https://agents-ia.pro/#contact
- Lien désabonnement placeholder + lien gérer préférences
- Signature Laurent Duplat + liens écosystème (Vocalis.pro, Agents-IA.pro)

Format HTML email complet (<html><head><body>...) avec inline CSS uniquement, largeur 600px."""


def call(system, user):
    payload = {"model": MODEL, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}], "temperature": 0.6, "max_tokens": 4000}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json", "User-Agent": "Mozilla/5.0 agents-ia-newsletter/1.0"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=180) as resp:
        obj = json.loads(resp.read().decode("utf-8"))
        content = obj["choices"][0]["message"]["content"]
        content = re.sub(r"^```(?:html)?\s*", "", content.strip())
        content = re.sub(r"\s*```$", "", content)
        return content


def main():
    print("Generating Newsletter Issue #13...")
    html = call(SYSTEM, USER)
    out = ROOT / "newsletter-issue-13-2026-04-29.html"
    out.write_text(html, encoding="utf-8")
    print(f"OK {out} ({len(html)} bytes)")
    print("\nAperçu : ouvre le .html dans ton navigateur pour preview.")
    print("À envoyer via Beehiiv (importer HTML) ou Brevo (template).")


if __name__ == "__main__":
    main()
