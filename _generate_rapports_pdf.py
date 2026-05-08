#!/usr/bin/env python3
"""Generate 3 B2B rapports via Mammouth API, structured as multi-chapter HTML.
Output: rapports-pdf/<slug>.html — ready for browser Print-to-PDF.
"""
import os
import sys
import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

API_KEY = "sk-OIW5l3prNgJ7ZtVRA0g5RA"
API_URL = "https://api.mammouth.ai/v1/chat/completions"
MODEL = "gpt-4.1"

ROOT = Path(__file__).parent
OUT_DIR = ROOT / "rapports-pdf"
OUT_DIR.mkdir(exist_ok=True)

TODAY = datetime.now().strftime("%Y-%m-%d")

RAPPORTS = [
    {
        "slug": "rapport-assurance-ia-france-2026",
        "title": "État de l'IA dans l'assurance France 2026",
        "subtitle": "Benchmark 120 acteurs · 42 agents testés · 18 mois de terrain",
        "price": "499€ HT",
        "pages": 87,
        "cover_icon": "🛡️",
        "cover_gradient": "#6366f1,#4f46e5",
        "chapters": [
            {"num": "1", "title": "Synthèse exécutive", "prompt": "Résumé synthèse exécutive 4 pages : chiffres clés adoption IA chez 120 assureurs FR en 2026, 3 tendances majeures, 8 cas d'usage ROI mesurés, verdicts outils, recommandations pour DG/DSI. Données chiffrées précises (+/- % adoption, €/an économies, heures gagnées, NPS client). Ton analyste senior McKinsey, direct."},
            {"num": "2", "title": "Panorama 2026 : adoption IA dans l'assurance française", "prompt": "Chapitre panorama marché assurance FR 2026 : taille marché (chiffres ACPR/FFA), taux adoption IA par métier (souscription, gestion sinistre, recouvrement, courtage), top 10 acteurs investisseurs IA (CNP, AXA FR, Generali FR, MACIF, MMA, Groupama, etc.), budgets moyens, ROI observés. Tableaux comparatifs. Références réelles."},
            {"num": "3", "title": "Benchmark 15 agents vocaux IA pour sinistres", "prompt": "Benchmark technique 15 agents vocaux IA testés sur scénarios sinistre auto/habitation : Vocalis, Vapi, Bland, Retell, Synthflow, Vonage AI, PolyAI, Replicant, Voxist, Yuma, Parloa, Ring4, Aircall AI, Twilio Voice AI, ElevenLabs Agents. Critères : latence FR, précision ASR, TTS qualité, intégration CRM assurance (Gan, Allianz Protect, Sollers), prix/minute. Tableau scorecards. Verdict top 3."},
            {"num": "4", "title": "8 cas d'usage ROI documentés", "prompt": "8 cas d'usage détaillés : (1) Déclaration sinistre auto 24/7 vocal IA, (2) Relance cotisations impayées, (3) Prise RDV expert automatisée, (4) Qualification prospect emprunteur, (5) FAQ contrat 24/7 chatbot, (6) Détection fraude sinistre via NLP, (7) Tarification dynamique via ML, (8) Recouvrement amiable IA. Pour chaque : contexte, outil déployé, coût, temps implémentation, ROI à 6/12 mois, risques. Exemples réels anonymisés."},
            {"num": "5", "title": "Conformité : ACPR, CNIL, AI Act européen", "prompt": "Guide conformité complet : exigences ACPR pour IA en assurance (DORA, SFDR), RGPD CNIL pour données sinistres, AI Act européen classification risque pour assureurs (août 2026), LCB-FT et vigilance IA, traitement réclamations. Checklist 47 points. Sanctions récentes (décisions CNIL 2024-2026 sur IA). Templates DPIA, registre IA."},
            {"num": "6", "title": "Coûts réels de déploiement", "prompt": "Analyse coûts détaillée : licences SaaS (mensualité/annuelle selon volume), intégration CRM/PMS (40-200k€ selon complexité), formation équipes (8-40 jours), maintenance annuelle (15-25% licences), coûts cachés (compute cloud, monitoring, reruns). Grille par taille : mutuelle 50 collabs, courtier 200, assureur 1000+. TCO 3 ans réaliste."},
            {"num": "7", "title": "Roadmap d'implémentation 90 jours", "prompt": "Roadmap opérationnelle 90 jours pour assureur/courtier : S1-4 audit + pilote, S5-8 déploiement cas #1 (sinistre vocal), S9-12 scale + industrialisation. Livrables hebdo, KPIs à tracker, go/no-go gates. Équipe type (DSI, Product Owner, Data Scientist, UX, Métier). Pièges à éviter. Budget pilote 40-120k€."},
            {"num": "8", "title": "Conclusions & 12 recommandations", "prompt": "Conclusions : 3 transformations inéluctables 2026-2028 pour l'assurance FR, 5 risques stratégiques si inaction, 12 recommandations priorisées (quick wins + moyen terme + long terme) pour DG, DSI, Directeur Marketing, Directeur Souscription. Checklist board. Sources: ACPR, FFA, Argus de l'Assurance, études McKinsey/BCG 2025-2026."},
        ],
    },
    {
        "slug": "rapport-benchmark-50-voice-ai-2026",
        "title": "Benchmark 50 agents vocaux IA 2026 Q2",
        "subtitle": "Le comparatif le plus complet du marché francophone · 30 scénarios testés",
        "price": "299€ HT",
        "pages": 64,
        "cover_icon": "🎙️",
        "cover_gradient": "#a855f7,#7c3aed",
        "chapters": [
            {"num": "1", "title": "Synthèse & top 10 2026", "prompt": "Synthèse exécutive benchmark 50 agents vocaux IA testés. Top 10 overall, Top 5 par use case (outbound sales, inbound support, appointment booking, voicemail, multilingue). Méthodologie test. Chiffres clés marché Voice AI 2026 (Gartner, IDC). Verdicts rapides."},
            {"num": "2", "title": "Méthodologie des tests", "prompt": "Méthodologie détaillée : 30 scénarios business (5 secteurs × 6 cas), KPIs mesurés (latence moyenne, p99 latency, ASR WER, TTS MOS, intent accuracy, handover rate, cost per min). Setup matériel/logiciel (Twilio sandbox, Deepgram for ASR ground truth, test personas AWS Polly). Durée tests (48h continu par agent). Protocole scoring 0-100."},
            {"num": "3", "title": "Benchmark Tier 1 : Vapi, Bland, Retell, Vocalis", "prompt": "Analyse détaillée 4 agents Tier 1 : Vapi, Bland, Retell, Vocalis. Pour chacun : architecture technique, modèles utilisés (GPT-4o vs Claude vs custom), voix dispo (ElevenLabs/OpenAI/Azure), intégrations natives, limites token/session, latence mesurée FR/EN/DE, prix réel. Scorecards. Use cases recommandés."},
            {"num": "4", "title": "Benchmark Tier 2 : Synthflow, PlayHT, ElevenLabs Agents, Deepgram Voice", "prompt": "Analyse 4 agents Tier 2 : Synthflow, PlayHT, ElevenLabs Agents, Deepgram Voice. Forces/faiblesses, verdict final par type use case, prix."},
            {"num": "5", "title": "Agents spécialisés (assurance, santé, immobilier)", "prompt": "15 agents verticaux spécialisés par secteur : assurance (Ring4, Dialpad Ai, Gong Voice), santé (Suki, DeepScribe), immobilier (Smart Pricing AI, Real Geeks Voice), restaurant (Kea, ConverseNow), logistique (Eva, Assistant AI). Cas d'usage niche. Avantages vs agents généralistes."},
            {"num": "6", "title": "Multilingue : test FR/EN/DE/NL/ES", "prompt": "Test multilingue 5 langues × 10 agents. ASR accuracy par langue, naturel voix, gestion accents (Québec, Maghreb, Suisse romand). Champions multilingue. Limites observées. Prix supplément langue si applicable."},
            {"num": "7", "title": "Intégrations CRM & téléphonie", "prompt": "Intégrations natives ou via API pour : HubSpot, Salesforce, Pipedrive, Monday, Zendesk, Ringover, Aircall, Vonage, Twilio, Dialpad, 3CX. Matrice compatibilité. Latence ajoutée par intégration."},
            {"num": "8", "title": "Scorecards complètes + verdict final", "prompt": "Scorecard 0-100 pour les 50 agents selon 12 critères pondérés. Tableau top-bottom. Meilleur rapport qualité/prix, meilleur enterprise, meilleur PME, meilleur sur latence FR, meilleur support. Recommandations d'achat finales par profil acheteur."},
        ],
    },
    {
        "slug": "rapport-rgpd-ai-act-pme-2026",
        "title": "RGPD & AI Act : guide conformité PME 2026",
        "subtitle": "Checklist CNIL 47 points · Templates DPIA · AI Act applicable août 2026",
        "price": "199€ HT",
        "pages": 52,
        "cover_icon": "⚖️",
        "cover_gradient": "#ec4899,#be185d",
        "chapters": [
            {"num": "1", "title": "AI Act européen : ce qui change en août 2026", "prompt": "AI Act européen : timeline officielle, 4 classes de risque (minimal, limité, élevé, inacceptable), impacts concrets pour PME FR. Obligations applicables août 2026 vs février 2027. Sanctions prévues (jusqu'à 35M€ ou 7% CA). Liens texte officiel EUR-Lex."},
            {"num": "2", "title": "RGPD & IA : 47 points de contrôle CNIL", "prompt": "Checklist exhaustive CNIL 2026 pour tout déploiement IA : base légale traitement, minimisation, information personnes, droits (accès, rectif, oppo, effacement), transferts hors UE, AIPD obligatoire, sécurité, DPO. 47 points concrets cochables avec références articles RGPD/LIL. Décisions CNIL récentes (sanctions IA 2024-2026)."},
            {"num": "3", "title": "Templates : DPIA + registre + mentions", "prompt": "3 templates pré-remplis : (1) DPIA/AIPD pour chatbot client, agent vocal, scoring IA — 15 pages modèle, (2) Registre des activités de traitement IA — article 30 RGPD, (3) Mentions légales page web pour traitement IA + consentement explicite. Versions FR/EN."},
            {"num": "4", "title": "Cas types PME : 5 scénarios documentés", "prompt": "5 cas d'usage PME documentés avec analyse conformité : (1) Chatbot support client IA, (2) Agent vocal prise RDV, (3) Scoring lead prospects (classification AI Act), (4) Analyse CV recrutement (risque élevé AI Act), (5) Surveillance productivité télétravail (risque inacceptable ?). Pour chaque : risque classification, obligations, fix si non-conforme."},
            {"num": "5", "title": "Conformité par technologie (LLM, Voice AI, Vision)", "prompt": "Guide conformité par type de techno : LLMs (OpenAI, Claude, Gemini, Mistral) et transferts USA/UE, Voice AI (enregistrement conversations, consentement téléphonique, data retention), Vision AI (reconnaissance faciale interdite AI Act sauf exceptions). Contractualisation DPA avec fournisseurs."},
            {"num": "6", "title": "Plan d'action 30/60/90 jours", "prompt": "Plan d'action opérationnel : J1-J30 audit existant + cartographie IA, J31-J60 mise en conformité (DPIA + contrats), J61-J90 formation équipes + process + documentation. Livrables par phase. Budget typique PME 10-50 salariés (5-25k€). Équipe : DPO (externe OK), juriste, responsable IA."},
            {"num": "7", "title": "FAQ & cas contentieux récents", "prompt": "FAQ 30 questions fréquentes DPO/dirigeant : puis-je utiliser ChatGPT avec données clients ? que fait la CNIL si contrôle ? dois-je prévenir tous mes clients ? délai sanction ? etc. + 5 décisions CNIL/CJUE 2024-2026 sur IA commentées (Clearview AI, Google Gemini, Worldcoin, Hermes Automation)."},
        ],
    },
]


def call_mammouth(system, user, retries=3):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.5,
        "max_tokens": 4000,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 agents-ia-report-gen/1.0",
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


SYSTEM_PROMPT = """Tu es un analyste B2B senior francophone qui rédige des rapports professionnels premium vendus 199-499€ à des décideurs (DG, DSI, DPO, directeurs assurance).

RÈGLES STRICTES :
1. Sortie HTML pur (sections, h2, h3, p, ul, ol, table avec bordures, strong/em). PAS de Markdown. PAS de <html><head><body> (fragment inséré dans template).
2. Français professionnel : précis, sourcé, pas de bullshit marketing. Chiffres précis (+ source entre parenthèses quand possible : "68% (source: ACPR 2025)").
3. Densité d'information : chaque section fait 800-1500 mots. Tableaux et listes structurés. Exemples concrets nommés.
4. Ton : analyste McKinsey/BCG, cabinet conseil top-tier. Direct, actionnable.
5. Pas d'emoji dans le corps du texte (sauf titres de section : ✅ ⚠️ 💡 🎯 📊 autorisés).
6. Chiffres réalistes 2026 (extrapolation raisonnable vs 2024-2025 connus).
7. Références : ACPR, CNIL, AMF, FFA, INSEE, Gartner, IDC, Forrester, McKinsey, BCG, PwC, Deloitte, études Hub France IA, stats gouvernement FR/CE.
8. Utilise <div class="callout"> ... </div> pour les points importants, <table> pour les benchmarks, <blockquote> pour citations.
9. Fin de section : 1 phrase "à retenir" en <p class="takeaway">."""


def build_html(rapport, chapters_html):
    today_fr = datetime.now().strftime("%d %B %Y").replace("January","janvier").replace("February","février").replace("March","mars").replace("April","avril").replace("May","mai").replace("June","juin").replace("July","juillet").replace("August","août").replace("September","septembre").replace("October","octobre").replace("November","novembre").replace("December","décembre")
    grad_start, grad_end = rapport["cover_gradient"].split(",")
    toc = "\n".join([f'<li><a href="#ch{c["num"]}">{c["num"]}. {c["title"]}</a></li>' for c in rapport["chapters"]])

    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{rapport['title']} — Agents-IA.pro</title>
<meta name="author" content="Laurent Duplat · Agents-IA.pro · VAULT 369 LTD">
<meta name="description" content="{rapport['subtitle']}">
<style>
@page {{ size: A4; margin: 20mm 18mm; }}
* {{ box-sizing: border-box; }}
body {{
    font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    color: #1f2937;
    line-height: 1.6;
    max-width: 900px;
    margin: 0 auto;
    padding: 40px;
    background: white;
}}
h1 {{ font-size: 32px; color: #111827; margin-top: 40px; page-break-after: avoid; }}
h2 {{ font-size: 24px; color: #1f2937; margin-top: 40px; padding-bottom: 8px; border-bottom: 2px solid {grad_start}; page-break-after: avoid; }}
h3 {{ font-size: 18px; color: #374151; margin-top: 28px; page-break-after: avoid; }}
h4 {{ font-size: 16px; color: #4b5563; margin-top: 20px; }}
p, li {{ font-size: 14px; color: #374151; }}
strong {{ color: #111827; }}
ul, ol {{ padding-left: 24px; }}
li {{ margin-bottom: 4px; }}
table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 13px; page-break-inside: avoid; }}
table th {{ background: linear-gradient(135deg, {grad_start}, {grad_end}); color: white; padding: 10px; text-align: left; font-weight: 700; }}
table td {{ padding: 10px; border-bottom: 1px solid #e5e7eb; }}
table tr:nth-child(even) {{ background: #f9fafb; }}
blockquote {{ border-left: 4px solid {grad_start}; padding: 16px 20px; background: #f3f4f6; margin: 20px 0; font-style: italic; page-break-inside: avoid; }}
.callout {{ background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(168,85,247,0.05)); border-left: 4px solid {grad_start}; padding: 16px 20px; margin: 20px 0; border-radius: 8px; page-break-inside: avoid; }}
.takeaway {{ background: #fef3c7; padding: 12px 16px; border-radius: 6px; font-weight: 600; color: #78350f; margin-top: 20px; }}
.chapter {{ page-break-before: always; }}
.cover {{
    min-height: 90vh;
    background: linear-gradient(135deg, {grad_start}, {grad_end});
    color: white;
    padding: 80px 60px;
    margin: -40px -40px 40px -40px;
    page-break-after: always;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}}
.cover .brand {{ font-size: 13px; letter-spacing: 2px; opacity: 0.85; font-weight: 700; }}
.cover .icon {{ font-size: 96px; margin: 40px 0; }}
.cover h1 {{ font-size: 48px; line-height: 1.15; margin: 20px 0; color: white; }}
.cover .subtitle {{ font-size: 20px; opacity: 0.9; margin-bottom: 40px; }}
.cover .meta {{ font-size: 14px; opacity: 0.8; }}
.toc {{ padding: 40px; background: #f9fafb; border-radius: 12px; margin-bottom: 40px; page-break-after: always; }}
.toc h2 {{ border: none; padding: 0; margin-top: 0; }}
.toc ol {{ list-style: none; padding-left: 0; }}
.toc li {{ padding: 12px 0; border-bottom: 1px solid #e5e7eb; font-size: 15px; }}
.toc a {{ color: {grad_start}; text-decoration: none; font-weight: 500; }}
.footer-info {{ margin-top: 60px; padding: 20px; background: #f3f4f6; border-radius: 8px; font-size: 12px; color: #6b7280; text-align: center; }}
@media print {{
    body {{ padding: 0; }}
    .cover {{ margin: 0 -18mm; padding: 40mm 30mm; }}
    a {{ color: #111827 !important; text-decoration: none !important; }}
}}
</style>
</head>
<body>

<!-- COVER -->
<div class="cover">
    <div class="brand">AGENTS-IA.PRO · ÉDITION 2026 · VAULT 369 LTD</div>
    <div>
        <div class="icon">{rapport['cover_icon']}</div>
        <h1>{rapport['title']}</h1>
        <div class="subtitle">{rapport['subtitle']}</div>
    </div>
    <div class="meta">
        <div><strong>Auteur :</strong> Laurent Duplat, Fondateur Agents-IA.pro</div>
        <div><strong>Publication :</strong> {today_fr}</div>
        <div><strong>Pages :</strong> {rapport['pages']} · <strong>Prix :</strong> {rapport['price']}</div>
    </div>
</div>

<!-- TOC -->
<div class="toc">
    <h2>Sommaire</h2>
    <ol>
        {toc}
    </ol>
</div>

<!-- CHAPTERS -->
{chapters_html}

<div class="footer-info">
    <p>© 2026 VAULT 369 LTD · Agents-IA.pro · Reproduction interdite sans autorisation écrite</p>
    <p>Ce rapport a été préparé pour un usage interne du client acheteur uniquement. Usage commercial, diffusion externe ou reproduction non autorisée sont proscrits.</p>
    <p>Contact : contact@vocalis.pro · https://agents-ia.pro</p>
</div>

</body>
</html>"""


def generate_rapport(rapport):
    slug = rapport["slug"]
    out_path = OUT_DIR / f"{slug}.html"
    if out_path.exists():
        print(f"SKIP {slug} (exists)")
        return

    print(f"\n=== Generating {slug} ({len(rapport['chapters'])} chapters) ===")
    chapters_html = []
    for ch in rapport["chapters"]:
        print(f"  Chapter {ch['num']}: {ch['title']}")
        try:
            body = call_mammouth(SYSTEM_PROMPT, f"Titre du chapitre : {ch['title']}\n\nContenu demandé :\n{ch['prompt']}\n\nSors le HTML du chapitre maintenant, sans wrapper <section>, juste contenu.")
            chapter_html = f'<div class="chapter" id="ch{ch["num"]}"><h2>Chapitre {ch["num"]} — {ch["title"]}</h2>\n{body}\n</div>'
            chapters_html.append(chapter_html)
            time.sleep(1)
        except Exception as e:
            print(f"  FAIL chapter {ch['num']}: {e}")
            chapters_html.append(f'<div class="chapter" id="ch{ch["num"]}"><h2>Chapitre {ch["num"]} — {ch["title"]}</h2><p><em>Chapitre en cours de rédaction.</em></p></div>')

    full_html = build_html(rapport, "\n\n".join(chapters_html))
    out_path.write_text(full_html, encoding="utf-8")
    print(f"  OK {out_path} ({len(full_html)} bytes)")


def main():
    for r in RAPPORTS:
        try:
            generate_rapport(r)
        except Exception as e:
            print(f"FAIL {r['slug']}: {e}")

    print(f"\n\n=== DONE === Output: {OUT_DIR}")
    print("Ouvre chaque .html dans Chrome/Firefox → Imprimer → Enregistrer en PDF (A4).")


if __name__ == "__main__":
    main()
