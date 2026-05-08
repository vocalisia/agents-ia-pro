#!/usr/bin/env python3
"""Generate 5 fresh blog articles for agents-ia.pro via Mammouth API.
Topics chosen for freshness signal (2026 Q1-Q2) + long-tail keywords.
"""
import os
import json
import re
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

API_KEY = "sk-OIW5l3prNgJ7ZtVRA0g5RA"
API_URL = "https://api.mammouth.ai/v1/chat/completions"
MODEL = "gpt-4.1"

ROOT = Path(__file__).parent
BLOG = ROOT / "blog"
BLOG.mkdir(exist_ok=True)

TOPICS = [
    {
        "slug": "gpt5-vs-claude-opus-agents-ia-2026",
        "title": "GPT-5 vs Claude Opus 4 : quel LLM pour vos agents IA en 2026 ?",
        "description": "Comparatif terrain 2026 : GPT-5, Claude Opus 4, Gemini 2.5. Coûts, latence, qualité pour agents IA business francophones.",
        "kw": "GPT-5 agents IA, Claude Opus 4 entreprise, comparatif LLM 2026",
        "cat": "Stratégie IA",
    },
    {
        "slug": "prix-agent-ia-2026-tarifs-reels",
        "title": "Combien coûte un agent IA en 2026 ? Tarifs réels déploiement PME",
        "description": "Coût réel d'un agent IA déployé en PME en 2026 : licences, intégration, maintenance. Grilles tarifaires Vocalis, OpenAI, Claude.",
        "kw": "prix agent IA 2026, tarif chatbot IA PME, coût déploiement IA",
        "cat": "Coûts & ROI",
    },
    {
        "slug": "agent-ia-vocal-assurance-cas-usage",
        "title": "Agent IA vocal en assurance : 7 cas d'usage rentables en 2026",
        "description": "Comment les assureurs utilisent les agents vocaux IA en 2026 : déclaration sinistre, relance, prise RDV. ROI et conformité LCB-FT.",
        "kw": "agent IA assurance, agent vocal sinistre, IA courtier assurance",
        "cat": "Secteur Assurance",
    },
    {
        "slug": "agents-ia-whatsapp-business-guide-2026",
        "title": "Agents IA WhatsApp Business : guide complet 2026",
        "description": "Déployer un agent IA sur WhatsApp Business en 2026 : API Cloud, coûts, intégration CRM, meilleurs outils francophones.",
        "kw": "agent IA WhatsApp, chatbot WhatsApp Business 2026, automatisation WhatsApp",
        "cat": "Messaging IA",
    },
    {
        "slug": "rgpd-agents-ia-cnil-2026-checklist",
        "title": "Agents IA & RGPD : checklist conformité CNIL mise à jour 2026",
        "description": "Guide CNIL 2026 : déployer un agent IA conforme RGPD. Mentions obligatoires, DPA, consentement, AI Act européen.",
        "kw": "RGPD agent IA 2026, CNIL chatbot conformité, AI Act PME",
        "cat": "Conformité & RGPD",
    },
]


def call_mammouth(prompt):
    req_body = json.dumps({
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "Tu es Laurent Duplat, opérateur IA francophone depuis 2024, "
                    "fondateur d'Agents-IA.pro. Tu écris des articles techniques "
                    "précis, sans bullshit marketing, avec chiffres et exemples concrets. "
                    "Format HTML pur (sans <html>, <head>, <body>). Utilise <h2>, <h3>, "
                    "<p>, <ul>, <li>, <strong>. Pas de Markdown. "
                    "Ton : direct, opérationnel, francophone suisse/français. "
                    "Ajoute des liens internes vers vocalis.pro, seo-true.com, "
                    "master-seller.fr quand pertinent (rel=nofollow)."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.7,
        "max_tokens": 3500,
    }).encode("utf-8")

    req = urllib.request.Request(
        API_URL,
        data=req_body,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 agents-ia-generator/1.0",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8", errors="ignore")
        print(f"  HTTP {e.code}: {err[:200]}")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


def build_article_html(topic, body_html, today_iso):
    slug = topic["slug"]
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;
  gtag('consent', 'default', {{ analytics_storage: _c === 'accepted' ? 'granted' : 'denied', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 }});
</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-B5627RD3TF"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', 'G-B5627RD3TF');
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} | Agents-IA.pro</title>
    <meta name="description" content="{topic['description']}">
    <meta name="keywords" content="{topic['kw']}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
    <meta name="author" content="Laurent Duplat">
    <link rel="icon" type="image/svg+xml" href="../favicon.svg">
    <link rel="stylesheet" href="../css/style.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="canonical" href="https://agents-ia.pro/blog/{slug}.html">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:title" content="{topic['title']}">
    <meta property="og:description" content="{topic['description']}">
    <meta property="og:url" content="https://agents-ia.pro/blog/{slug}.html">
    <meta property="og:locale" content="fr_FR">
    <meta property="article:author" content="Laurent Duplat">
    <meta property="article:published_time" content="{today_iso}">
    <meta property="article:section" content="{topic['cat']}">

    <!-- Schema Article + Person -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "{topic['title']}",
      "description": "{topic['description']}",
      "datePublished": "{today_iso}",
      "dateModified": "{today_iso}",
      "author": {{
        "@type": "Person",
        "@id": "https://agents-ia.pro/#founder",
        "name": "Laurent Duplat",
        "url": "https://agents-ia.pro/a-propos.html"
      }},
      "publisher": {{
        "@type": "Organization",
        "@id": "https://agents-ia.pro/#organization",
        "name": "Agents-IA.pro",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://agents-ia.pro/favicon.svg"
        }}
      }},
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "https://agents-ia.pro/blog/{slug}.html"
      }},
      "inLanguage": "fr",
      "articleSection": "{topic['cat']}",
      "keywords": "{topic['kw']}"
    }}
    </script>
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{ "@type": "ListItem", "position": 1, "name": "Accueil", "item": "https://agents-ia.pro/" }},
        {{ "@type": "ListItem", "position": 2, "name": "Blog", "item": "https://agents-ia.pro/blog.html" }},
        {{ "@type": "ListItem", "position": 3, "name": "{topic['title']}", "item": "https://agents-ia.pro/blog/{slug}.html" }}
      ]
    }}
    </script>
</head>
<body>

<!-- NAVBAR -->
<nav class="navbar" id="navbar">
    <div class="nav-container">
        <a href="../index.html" class="nav-logo">
            <span class="logo-icon">🤖</span>
            <span class="logo-text">agents-ia<span class="logo-accent">.pro</span></span>
        </a>
        <div class="nav-links" id="navLinks">
            <a href="../index.html#explorer" class="nav-link">Explorer</a>
            <a href="../categories.html" class="nav-link">Catégories</a>
            <a href="../index.html#solutions" class="nav-link">Solutions IA</a>
            <a href="../blog.html" class="nav-link">Blog</a>
            <a href="../a-propos.html" class="nav-link">À propos</a>
        </div>
        <div class="nav-actions">
            <a href="../submit.html" class="btn-submit"><i class="fas fa-plus"></i> Soumettre un Agent</a>
            <a href="../index.html#contact" class="btn-login">Démo gratuite</a>
            <button class="mobile-toggle" id="mobileToggle"><i class="fas fa-bars"></i></button>
        </div>
    </div>
</nav>

<!-- ARTICLE -->
<section class="section" style="padding-top:120px;">
    <div class="container">
        <div class="article-content" style="max-width:820px; margin:0 auto;">
            <nav aria-label="Fil d'Ariane" style="margin-bottom:24px; font-size:14px; color:var(--text-secondary);">
                <a href="../index.html" style="color:var(--primary-light);">Accueil</a> &rsaquo;
                <a href="../blog.html" style="color:var(--primary-light);">Blog</a> &rsaquo;
                {topic['cat']}
            </nav>

            <span style="display:inline-block; padding:6px 14px; background:rgba(99,102,241,0.15); color:var(--primary-light); border-radius:999px; font-size:12px; font-weight:600; margin-bottom:16px;">{topic['cat']}</span>
            <h1 class="section-title" style="text-align:left; margin-bottom:16px;">{topic['title']}</h1>

            <div style="display:flex; gap:16px; align-items:center; margin-bottom:40px; color:var(--text-secondary); font-size:14px;">
                <div style="display:flex; align-items:center; gap:8px;">
                    <div style="width:32px; height:32px; border-radius:50%; background:linear-gradient(135deg,#6366f1,#a855f7); display:flex; align-items:center; justify-content:center; color:white;"><i class="fas fa-user-tie"></i></div>
                    <a href="../a-propos.html" style="color:var(--primary-light); font-weight:600;">Laurent Duplat</a>
                </div>
                <span>&bull;</span>
                <time datetime="{today_iso}">{today_iso}</time>
                <span>&bull;</span>
                <span><i class="fas fa-clock"></i> 8 min de lecture</span>
            </div>

            {body_html}

            <div style="margin-top:48px; padding:32px; background:linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.1)); border-radius:16px; text-align:center;">
                <h3 style="margin-bottom:12px;">Besoin d'un agent IA pour votre business ?</h3>
                <p style="color:var(--text-secondary); margin-bottom:24px;">Audit gratuit 30 minutes — on regarde votre cas, sans slides marketing.</p>
                <a href="../index.html#contact" class="btn-login" style="padding:14px 32px; font-size:16px; display:inline-block;">Réserver mon audit <i class="fas fa-arrow-right"></i></a>
            </div>
        </div>
    </div>
</section>

<!-- FOOTER -->
<footer class="footer">
    <div class="container">
        <div class="footer-grid">
            <div class="footer-brand"><span class="logo-icon">🤖</span><span class="logo-text">agents-ia<span class="logo-accent">.pro</span></span><p>La marketplace #1 d'agents IA francophones.</p></div>
            <div class="footer-links"><h4>Écosystème</h4><a href="https://vocalis.pro" target="_blank" rel="noopener nofollow">Vocalis.pro</a><a href="https://vocalis.blog" target="_blank" rel="noopener nofollow">Vocalis.blog</a><a href="https://vocalis-ai.org" target="_blank" rel="noopener nofollow">Vocalis-AI.org</a><a href="https://ai-due.com" target="_blank" rel="noopener nofollow">AI-DUE.com</a><a href="https://tesla-mag.ch" target="_blank" rel="noopener nofollow">Tesla-Mag.ch</a><a href="https://master-seller.fr" target="_blank" rel="noopener nofollow">Master-Seller.fr</a><a href="https://iapmesuisse.ch" target="_blank" rel="noopener nofollow">IAPMESuisse.ch</a></div>
            <div class="footer-links"><h4>Services IA</h4><a href="https://seo-true.com" target="_blank" rel="noopener nofollow">SEO-True.com</a><a href="https://trustly-ai.com" target="_blank" rel="noopener nofollow">Trustly-AI.com</a><a href="https://trust-vault.com" target="_blank" rel="noopener nofollow">Trust-Vault.com</a><a href="https://agentic-whatsup.com" target="_blank" rel="noopener nofollow">Agentic-WhatsUp.com</a><a href="https://lead-gene.com" target="_blank" rel="noopener nofollow">Lead-Gene.com</a><a href="https://xn--factureimpaye-6ya.fr" target="_blank" rel="noopener nofollow">Factureimpayée.fr</a></div>
            <div class="footer-links">
                <h4>Ressources</h4>
                <a href="../blog.html">Blog</a>
                <a href="../a-propos.html">À propos</a>
                <a href="../index.html#contact">Contact</a>
                <a href="../submit.html">Soumettre un agent</a>
            </div>
        </div>
        <div class="footer-bottom">
            <p>&copy; 2025-2026 Agents-IA.pro — Tous droits réservés | 🇨🇭 Basé en Suisse</p>
            <div class="footer-legal">
                <a href="../mentions-legales.html">Mentions légales</a>
                <a href="../cgu.html">CGU</a>
                <a href="../confidentialite.html">Politique de confidentialité</a>
            </div>
        </div>
    </div>
</footer>

<a href="https://wa.me/41799394222" class="whatsapp-widget" target="_blank" rel="noopener" aria-label="WhatsApp"><i class="fab fa-whatsapp"></i></a>
<div class="cookie-banner" id="cookieBanner"><div class="cookie-content"><p>🍪 Ce site utilise des cookies. <a href="../confidentialite.html" style="color:var(--primary-light);">Politique de confidentialité</a>.</p><div class="cookie-actions"><button class="cookie-btn cookie-accept" id="cookieAccept">Accepter</button><button class="cookie-btn cookie-decline" id="cookieDecline">Refuser</button></div></div></div>
<script src="../js/app.js"></script>
</body>
</html>"""


def main():
    today_iso = datetime.utcnow().strftime("%Y-%m-%d")
    generated = []

    for topic in TOPICS:
        slug = topic["slug"]
        out_path = BLOG / f"{slug}.html"

        if out_path.exists():
            print(f"SKIP {slug} (already exists)")
            continue

        print(f"\n=== Generating {slug} ===")

        prompt = f"""Écris un article de blog en HTML (PAS de Markdown, PAS de <html>/<head>/<body>) sur :

**{topic['title']}**

Description SEO cible : {topic['description']}
Mots-clés : {topic['kw']}
Catégorie : {topic['cat']}

Structure obligatoire :
1. Paragraphe introduction (le contexte 2026, la problématique concrète)
2. 5-7 sections avec <h2> (titres orientés intention de recherche)
3. Des sous-sections <h3> dans certains H2
4. Listes <ul>/<li> pour les points clés
5. Tableaux <table> avec <thead>/<tbody>/<tr>/<th>/<td> pour comparaisons (bordures OK)
6. Quelques <strong> pour les chiffres et points critiques
7. Une FAQ finale (3-5 questions) avec <h2>FAQ</h2> + <h3> par question
8. Conclusion avec call to action

Contraintes :
- 1500-2000 mots
- Ton direct opérationnel, pas marketing
- Chiffres réalistes et sourcés dans le texte (CNIL, Stanford AI Index, etc.)
- 2-3 liens internes vers https://vocalis.pro, https://seo-true.com ou https://master-seller.fr (rel=nofollow)
- Pas de phrases de bullshit type "à l'ère digitale"
- Date de référence : 2026 Q2

Commence directement par le premier paragraphe, sans titre (le H1 est déjà placé)."""

        body = call_mammouth(prompt)
        if not body:
            print(f"  FAIL {slug}")
            continue

        # Clean: remove markdown code fences if any
        body = re.sub(r'^```(?:html)?\s*', '', body.strip())
        body = re.sub(r'\s*```$', '', body.strip())

        html = build_article_html(topic, body, today_iso)
        out_path.write_text(html, encoding="utf-8")
        print(f"  OK {out_path} ({len(html)} bytes)")
        generated.append(slug)

        time.sleep(2)

    print(f"\n\nGenerated {len(generated)} articles:")
    for s in generated:
        print(f"  - https://agents-ia.pro/blog/{s}.html")


if __name__ == "__main__":
    main()
