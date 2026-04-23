# GEO Audit Report: Agents-IA.pro

**Audit Date:** 2026-04-17
**URL:** https://agents-ia.pro
**Business Type:** Marketplace / Agency (SaaS hybrid) — Agents IA francophones
**Pages Analyzed:** 42 fichiers HTML (28 dans sitemap)

---

## Executive Summary

**Overall GEO Score: 37/100 (Poor)**

Agents-ia.pro est un site statique HTML bien structuré visuellement mais **invisible pour Google et les IA**. Zéro page indexée sur Google, zéro mention tierce, des conflits techniques critiques (www vs non-www, hreflang bloqué par robots.txt), et un E-E-A-T quasi inexistant (pas d'auteur nommé, pas d'adresse, contact@vocalis.pro au lieu de @agents-ia.pro). Le contenu est orienté conversion humaine, pas extraction IA. Les stats ROI sont invérifiables. La marque n'existe pas comme entité pour les systèmes IA.

### Score Breakdown

| Category | Score | Weight | Weighted Score |
|---|---|---|---|
| AI Citability | 55/100 | 25% | 13.75 |
| Brand Authority | 8/100 | 20% | 1.60 |
| Content E-E-A-T | 26/100 | 20% | 5.20 |
| Technical GEO | 77/100 | 15% | 11.55 |
| Schema & Structured Data | 42/100 | 10% | 4.20 |
| Platform Optimization | 5/100 | 10% | 0.50 |
| **Overall GEO Score** | | | **36.80 ≈ 37/100** |

---

## 🔴 CRITICAL Issues (Fix Immediately)

### C1. Site NON INDEXÉ sur Google — 0 pages
- `site:agents-ia.pro` retourne 0 résultats
- Google Search Console PAS vérifié (commenté dans le code, ligne 11 de index.html)
- **Fix:** Activer GSC, soumettre sitemap, vérifier via meta tag ou DNS

### C2. Conflit www vs non-www sur TOUTES les pages
- **Canonical:** `https://www.agents-ia.pro/...` (avec www)
- **OG:URL:** `https://agents-ia.pro/...` (sans www)
- **Sitemap:** `https://agents-ia.pro/...` (sans www)
- **Hreflang:** `https://agents-ia.pro/...` (sans www)
- **Schema:** `https://agents-ia.pro` (sans www)
- Google ne sait pas quelle version est la bonne → dilution de l'autorité
- **Fix:** Choisir UNE version (sans www recommandé) et l'appliquer partout (canonicals, sitemap, schema, og:url). Ajouter redirect 301 www → non-www dans vercel.json

### C3. Hreflang pointe vers pages bloquées par robots.txt
- `hreflang="en"` → `/en/` qui est `Disallow: /en/` dans robots.txt
- `hreflang="de"` → `/de/` qui est `Disallow: /de/` dans robots.txt
- `hreflang="nl"` → `/nl/` qui est `Disallow: /nl/` dans robots.txt
- Contradictoire : Google voit un signal "indexe cette page" (hreflang) ET "n'indexe pas" (Disallow)
- **Fix:** Soit autoriser /en/, /de/, /nl/ dans robots.txt, soit retirer les hreflang

### C4. Double canonical sur index.html
- Ligne 8 ET ligne 102 contiennent `<link rel="canonical">`
- Confus pour les crawlers
- **Fix:** Supprimer le doublon (garder celui dans le `<head>` initial)

### C5. Consent Mode GA4 incohérent
- **index.html:** `rejected?denied:granted` (default = granted = tracking actif)
- **Toutes les autres pages:** `accepted?granted:denied` (default = denied = PAS de tracking)
- Résultat : GA4 ne track que la homepage correctement
- **Fix:** Unifier sur `_c === 'rejected' ? 'denied' : 'granted'` sur toutes les pages

---

## 🟠 HIGH Priority Issues

### H1. Mentions légales incomplètes (violation loi suisse)
- Pas d'adresse physique (juste "Basé en Suisse")
- Pas de numéro IDE/UID (obligatoire pour activité commerciale CH)
- Pas de nom du représentant légal (juste "Le représentant légal")
- Email contact@vocalis.pro au lieu de contact@agents-ia.pro
- **Impact:** Google YMYL signal négatif, confiance utilisateur brisée

### H2. Aucun auteur identifié sur le contenu
- Tous les articles : "Rédaction Agents-IA.pro"
- Pas de bio, pas de photo, pas de credentials
- Pas de profils LinkedIn liés
- **Impact:** E-E-A-T expertise/experience signal = 0

### H3. Témoignages invérifiables
- 3 témoignages : "Marc B.", "Sophie L.", "Pierre D." — initiale seule
- "2,400+ reviews" pour Vocalis AI — aucun lien vers plateforme de reviews
- "12,840+ professionnels newsletter" — non vérifiable
- **Impact:** Trust signal négatif, potentiellement pénalisant

### H4. llms.txt non conforme au standard
- Fichier existe mais = simple navigation/sitemap
- Manque : politiques d'accès, droits d'utilisation, format metadata, version
- URLs avec `.html` alors que Vercel utilise `cleanUrls: true`
- **Impact:** Crawlers IA ne comprennent pas la structure du site

### H5. Zéro images `<img>` dans le HTML
- Tout le visuel est en CSS/Font Awesome/SVG inline
- Aucune image indexable par Google Images
- Pas d'attributs `alt` possibles
- **Impact:** Zéro visibilité Google Images, pas de rich snippets visuels

### H6. Incohérence extensions dans canonicals
- `cgu.html`, `confidentialite.html`, `mentions-legales.html` gardent `.html`
- Toutes les autres pages : canonical sans extension
- **Fix:** Retirer `.html` des canonicals de cgu, confidentialite, mentions-legales

---

## 🟡 MEDIUM Priority Issues

### M1. Hreflang uniquement sur homepage
- 42 fichiers HTML, seul index.html (+ en/de/nl/index.html) a des hreflang
- Les 30+ autres pages n'ont pas de hreflang
- **Fix:** Si les pages multilingues n'existent pas, c'est normal. Sinon ajouter hreflang partout

### M2. Contenu orienté conversion, pas extraction IA
- Pages d'agents ouvrent avec des taglines marketing, pas des définitions
- Manque de blocs "En bref" auto-suffisants en haut de page
- FAQ avec réponses collapsées (invisibles pour crawlers)
- **Fix:** Ajouter un bloc définition 50-60 mots en haut de chaque page d'agent

### M3. Stats ROI non sourcées
- "+340%", "+520%", "+280%" sans méthodologie ni source
- Les IA dé-priorisent les claims non sourcées
- **Fix:** Ajouter une phrase de méthodologie pour chaque stat ROI

### M4. Schema Service areaServed incohérent
- Homepage : `"areaServed": "FR"` (France)
- agent-commercial : `"areaServed": {"@type": "Country", "name": "CH"}` (Suisse)
- **Fix:** Choisir CH (siège social en Suisse) et l'appliquer partout

### M5. Schema Offers avec prix à 0
- agent-commercial schema : `"price":"0"` pour Starter, Business, Enterprise
- Prix réels existent dans le HTML mais pas dans le schema
- **Fix:** Mettre les vrais prix dans les Offers ou utiliser `"priceRange"` pour Organization

### M6. Pas de BreadcrumbList schema
- Navigation hiérarchique visible mais pas de schema BreadcrumbList
- **Fix:** Ajouter sur toutes les pages internes

### M7. Pages sans aucun JSON-LD (10 pages)
- 404.html, agent.html, blog.html, categories.html, cgu.html, confidentialite.html, contact.html, mentions-legales.html, merci.html, submit.html
- **Fix:** Ajouter au minimum WebPage schema sur chacune

### M8. Pas de FAQPage schema
- Plusieurs pages ont du contenu FAQ mais pas de FAQPage structured data
- **Fix:** Ajouter FAQPage JSON-LD sur les pages avec FAQ (agent-commercial, agent-seo, etc.)

---

## 🔵 LOW Priority Issues

### L1. Pas de schema Article sur les blog posts
- Blog posts ont du JSON-LD mais pas d'Article schema (manque datePublished, author, etc.)
- **Fix:** Ajouter Article schema avec author Person, datePublished, dateModified

### L2. og:image identique sur toutes les pages
- Toutes les pages utilisent `/og-image.png`
- **Fix:** Créer des images OG spécifiques par page d'agent pour meilleur CTR social

### L3. Pas de schema AggregateRating
- Notes "4.8★", "4.9★" affichées mais pas dans le schema
- **Fix:** Ajouter AggregateRating dans le schema Service/Product

### L4. sitemap.xml manque des pages
- 28 URLs dans sitemap vs 42 fichiers HTML
- Pages manquantes : agent.html, blog-agent-ia-comptable.html, blog-agent-ia-recrutement.html, blog-agents-commerciaux-ia.html, contact.html, merci.html, submit.html, 404.html
- **Fix:** Ajouter les pages manquantes (sauf 404 et merci)

### L5. Pas de schema SearchAction fonctionnel
- Schema WebSite avec SearchAction pointe vers `?s={search_term_string}` mais le site n'a pas de vraie recherche
- **Fix:** Retirer le SearchAction ou implémenter une vraie recherche

---

## Category Deep Dives

### AI Citability (55/100)
**Points forts :**
- Tableaux comparatifs "Agent IA vs Employé" — extractables par les IA
- Blog post /blog/choisir-agent-ia avec calcul ROI détaillé (meilleur bloc du site, 82/100)
- Densité statistique correcte (prix, ROI, délais)

**Points faibles :**
- Pages d'agents ouvrent avec des slogans, pas des définitions
- FAQ collapsées = invisibles pour les crawlers
- Stats ROI sans source ni méthodologie
- Aucune donnée propriétaire ou recherche originale

**Fix prioritaire :** Ajouter un bloc "En bref" (50-60 mots, définition + prix + ROI + délai) en haut de chaque page.

---

### Brand Authority (8/100)
**Constat brutal :**
- 0 pages indexées Google
- 0 mentions tierces (YouTube, Reddit, LinkedIn, Wikipedia, presse)
- 0 backlinks détectables
- Nom de marque "agents IA" = terme générique → collision
- Concurrents (Agent.ai, AgentMarket.fr, Salesforce AgentExchange) dominent

**Fix prioritaire :** GSC → indexation → 20 mentions tierces en 90 jours (Product Hunt, Sortlist, FrenchWeb, Maddyness, G2).

---

### Content E-E-A-T (26/100)
| Dimension | Score |
|-----------|-------|
| Experience | 25/100 — Témoignages invérifiables, pas de case studies réels |
| Expertise | 35/100 — Contenu correct mais générique, pas d'expert nommé |
| Authoritativeness | 15/100 — Zéro validation externe, écosystème auto-référencé |
| Trustworthiness | 30/100 — Mentions légales incomplètes, email cross-domaine |

**Fix prioritaire :** Corriger mentions légales (adresse, IDE, nom dirigeant), ajouter des auteurs avec bio/LinkedIn, remplacer témoignages par case studies vérifiables.

---

### Technical GEO (77/100)
**Points forts (score élevé) :**
- 13 crawlers IA explicitement autorisés (GPTBot, ClaudeBot, PerplexityBot, etc.) — 92/100
- Site statique HTML = rendu parfait, pas de JS blocking — 95/100
- Meta tags complets (OG, Twitter Card, description) — 82/100
- Sitemap XML bien structuré avec lastmod/priority — 88/100
- Security headers corrects (HSTS, X-Frame-Options, etc.) — 85/100

**Points faibles :**
- Conflit www vs non-www dans canonicals (CRITIQUE) — 55/100
- Hreflang uniquement sur homepage, absent des 22 pages internes — 68/100
- llms.txt non conforme au standard, pas de llms-full.txt — 45/100
- Double canonical sur homepage
- GSC non vérifié
- Consent mode GA4 incohérent (homepage vs reste)
- Pas de meta robots sur pages internes
- Manque CSP et Permissions-Policy headers

---

### Schema & Structured Data (42/100)
**Points forts :**
- 58 blocs JSON-LD sur 32 fichiers — bonne couverture de base
- Organization schema complet (knowsAbout, sameAs, contactPoint)
- WebSite + SearchAction sur homepage
- FAQPage schema sur 2 pages d'agents (commercial, seo)
- BreadcrumbList sur 11 pages d'agents + blog posts

**Points faibles :**
- **CRITIQUE : prix = 0** dans tous les Offers (297/497/997 CHF dans le HTML mais "0" dans schema) → Google affiche "Gratuit"
- 10 pages sans aucun schema (categories, blog index, contact, legal, etc.)
- 3 tiers de qualité : 2 pages complètes, 9 partielles, 7 minimales
- 16/18 pages agents sans FAQPage schema malgré contenu FAQ
- 7 pages agents sans BreadcrumbList
- Blog : author = Organization au lieu de Person (Google préfère Person pour E-E-A-T)
- Blog : pas d'image dans Article schema (requis pour rich results)
- AggregateRating sur 2 pages seulement, 5/5 avec 3 notes = suspicieux
- areaServed incohérent (FR homepage vs CH agent-commercial)

---

### Platform Optimization (5/100)
- YouTube : absent
- LinkedIn : absent
- Reddit : absent
- Trustpilot : absent
- Product Hunt : absent
- G2 : absent
- Wikipedia/Wikidata : absent
- Presse francophone : absent

---

## Quick Wins (Implement This Week)

1. **Vérifier Google Search Console** → activer meta tag ou DNS TXT → soumettre sitemap → demander indexation. **Impact: CRITIQUE, Effort: 15 min**

2. **Unifier canonical URLs** → remplacer `www.agents-ia.pro` par `agents-ia.pro` sur les 42 fichiers. **Impact: HIGH, Effort: 30 min (find & replace)**

3. **Corriger consent mode GA4** → copier la logique de index.html (`rejected?denied:granted`) sur toutes les pages. **Impact: HIGH, Effort: 20 min**

4. **Corriger mentions légales** → ajouter adresse, IDE/UID, nom dirigeant, email @agents-ia.pro. **Impact: HIGH, Effort: 15 min**

5. **Retirer Disallow /en/ /de/ /nl/ de robots.txt** OU retirer les hreflang de index.html. **Impact: HIGH, Effort: 5 min**

---

## 30-Day Action Plan

### Week 1: Fondations Techniques (URGENT)
- [ ] Vérifier et activer Google Search Console
- [ ] Soumettre sitemap.xml dans GSC
- [ ] Unifier canonical URLs (retirer www partout)
- [ ] Ajouter redirect 301 www → non-www dans vercel.json
- [ ] Supprimer double canonical sur index.html (ligne 102)
- [ ] Corriger consent mode GA4 sur toutes les pages
- [ ] Résoudre conflit hreflang vs robots.txt
- [ ] Corriger extensions .html dans canonicals de cgu/confidentialite/mentions-legales
- [ ] Corriger areaServed incohérent (CH partout)
- [ ] Corriger prix schema Offers (vrais prix ou priceRange)

### Week 2: E-E-A-T & Trust
- [ ] Compléter mentions légales (adresse, IDE, nom, email)
- [ ] Créer des profils auteurs avec nom, photo, bio, LinkedIn
- [ ] Remplacer témoignages initiales par case studies vérifiables
- [ ] Ajouter sources/liens vers les stats ROI
- [ ] Ajouter liens vers sources officielles dans article RGPD (CNIL, PFPDT)

### Week 3: Schema & AI Citability
- [ ] Ajouter FAQPage schema sur pages avec FAQ
- [ ] Ajouter Article schema sur blog posts
- [ ] Ajouter BreadcrumbList schema sur toutes les pages internes
- [ ] Ajouter JSON-LD sur les 10 pages qui n'en ont pas
- [ ] Réécrire llms.txt conforme au standard (accès, droits, metadata)
- [ ] Ajouter blocs "En bref" définitionnels sur chaque page d'agent
- [ ] Déplier les FAQ (réponses visibles, pas collapsées)

### Week 4: Brand Authority & Platform
- [ ] Créer page LinkedIn entreprise
- [ ] Soumettre sur Product Hunt
- [ ] S'inscrire sur Sortlist.ch, G2, Trustpilot
- [ ] Publier 2 articles invités (FrenchWeb, Maddyness, ICTjournal.ch)
- [ ] Ajouter des images `<img>` avec alt text pour Google Images
- [ ] Créer og:image spécifiques par page d'agent
- [ ] Ajouter AggregateRating dans schema

---

## Appendix: Pages Analyzed

| URL | Title | Issues |
|---|---|---|
| / | Marketplace #1 d'Agents IA | Double canonical, consent mode unique, schema areaServed=FR |
| /agent-commercial | Agent Commercial IA | Schema prix=0, areaServed=CH |
| /agent-support | Agent Support IA | 1 seul JSON-LD |
| /agent-email | Agent Email IA | Standard |
| /agent-chatbot | Agent Chatbot IA | Standard |
| /agent-marketing | Agent Marketing IA | Standard |
| /agent-seo | Agent SEO IA | Page la moins citable (44/100) |
| /agent-rh | Agent RH IA | Standard |
| /agent-finance | Agent Finance IA | Standard |
| /agent-design | Agent Design IA | Standard |
| /agent-juridique | Agent Juridique IA | Standard |
| /agent-dev | Agent Dev IA | Standard |
| /agent-assurance | Agent Assurance | 1 JSON-LD seulement |
| /agent-ecommerce | Agent E-commerce | 1 JSON-LD seulement |
| /agent-formation | Agent Formation | 1 JSON-LD seulement |
| /agent-immobilier | Agent Immobilier | 1 JSON-LD seulement |
| /agent-logistique | Agent Logistique | 1 JSON-LD seulement |
| /agent-recouvrement | Agent Recouvrement | 1 JSON-LD seulement |
| /agent-restauration | Agent Restauration | 1 JSON-LD seulement |
| /agent-sante | Agent Santé | 1 JSON-LD seulement |
| /agent | Page agent générique | PAS de JSON-LD |
| /blog | Blog index | PAS de JSON-LD |
| /blog/choisir-agent-ia | Guide choix agent IA | Meilleure page citabilité (62/100) |
| /blog/agent-vocal-cabinet-dentaire | Case study dentaire | Standard |
| /blog/top-10-agents-ia-mars-2025 | Top 10 agents mars 2025 | Date "mars 2025" → possiblement périmé |
| /blog/agent-ia-vs-employe | Agent IA vs Employé | Standard |
| /blog/rgpd-agents-ia | RGPD et agents IA | Pas de liens sources officielles |
| /blog/deployer-agent-ia-30-minutes | Tutoriel déploiement | Standard |
| /categories | Catégories | PAS de JSON-LD |
| /cgu | CGU | PAS de JSON-LD, canonical avec .html |
| /confidentialite | Confidentialité | PAS de JSON-LD, canonical avec .html |
| /mentions-legales | Mentions légales | PAS de JSON-LD, canonical avec .html, INCOMPLÈTES |
| /contact | Contact | PAS de JSON-LD |
| /submit | Soumettre agent | PAS de JSON-LD |
| /merci | Page merci | PAS de JSON-LD |
| /en/ | English version | Bloqué par robots.txt mais a canonical + hreflang |
| /de/ | German version | Bloqué par robots.txt mais a canonical + hreflang |
| /nl/ | Dutch version | Bloqué par robots.txt mais a canonical + hreflang |

---

*Rapport généré par Claude Opus 4.6 — GEO Audit System*
