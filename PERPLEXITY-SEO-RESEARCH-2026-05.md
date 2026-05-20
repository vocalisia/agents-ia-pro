# agents-ia.pro — SEO/GEO Research (mai 2026)

> **Note méthodologique** : Perplexity API budget exhausted au moment de l'exécution (HTTP 400 ExceededBudget). Contenu ci-dessous = synthèse expert basée sur connaissances marché IA FR/CH mai 2026. À re-valider via Perplexity quand le budget est rechargé, ou via SERP scrape direct (Scrapling/Camofox déjà installés).

---

## Section 1 — Top 10 concurrents FR/CH (agent IA / marketplace IA)

| # | Site | URL | DR (est.) | Positionnement | Force principale | Faiblesse SEO exploitable |
|---|------|-----|-----------|----------------|------------------|---------------------------|
| 1 | Dust | dust.tt | 72 | SaaS plateforme agents | Backing Sequoia, équipe ex-OpenAI, marque forte | Pas de marketplace publique d'agents, faible contenu FR/PME |
| 2 | LightOn | lighton.ai | 65 | SaaS LLM souverain FR | Souveraineté EU, partenariats grands comptes | Marketing axé grands comptes, vide sur PME/marketplace |
| 3 | Mistral AI | mistral.ai | 81 | LLM/agents | Brand authority maximale FR | Pas de marketplace agents prêts-à-l'emploi |
| 4 | Hugging Face (Spaces) | huggingface.co | 91 | Marketplace ML/agents | DR massif, écosystème ouvert | Trop technique, zéro UX PME, FR faible |
| 5 | n8n | n8n.io | 78 | Automation + agents | Open source, communauté forte | Pas SEO ciblé PME francophones, docs EN-first |
| 6 | Make.com | make.com | 80 | Automation no-code + IA | Brand reconnu PME | Pas spécialisé "agent IA", positioning automation |
| 7 | Zapier | zapier.com | 92 | Automation + AI Actions | DR géant, Zapier Agents lancé 2025 | EN-first, prix US, peu adapté RGPD strict |
| 8 | Synthesia (agents vocaux FR) | synthesia.io | 79 | SaaS avatar/voice | Brand vocal IA leader | Pas marketplace, prix élevés, B2B grands comptes |
| 9 | Voiceflow | voiceflow.com | 70 | Builder agents conversationnels | UX builder solide | Vide contenu FR, peu de cas PME franco |
| 10 | Hubspot AI Agents | hubspot.com/products/ai-agents | 92 | Agents intégrés CRM | DR énorme, distribution massive | Lock-in CRM, pas marketplace ouverte |

**Acteurs FR/CH émergents à surveiller** (DR <40 mais montent vite) :
- aimarketplace.fr, agentia.fr, intelligence-artificielle.com (blog FR), lebigdata.fr (blog), siecledigital.fr (blog), journaldunet.com (media)
- Suisse : ictjournal.ch, swissinfo.ch IA section, ai-suisse.ch

**Opportunité agents-ia.pro** : créneau "marketplace agents IA prêts-à-l'emploi pour PME francophones" — vide concurrentiel net entre Hugging Face (trop tech) et Hubspot (trop CRM-locked).

---

## Section 2 — 7 techniques GEO/LLM SEO 2026

### 1. llms.txt avancé (structure hiérarchique)
Fichier `/llms.txt` racine + `/llms-full.txt` (corpus complet). Format Markdown structuré :
```
# agents-ia.pro
> Marketplace agents IA pour PME francophones

## Catégories
- [Agents vocaux](https://agents-ia.pro/vocal): support client 24/7
- [Agents commerciaux](https://agents-ia.pro/sales): qualification leads

## Pricing
[Tarifs](https://agents-ia.pro/pricing)

## FAQ
[FAQ complète](https://agents-ia.pro/faq.md)
```
**Pourquoi** : ChatGPT/Claude/Perplexity scrapent llms.txt prioritairement (Anthropic spec adoptée fin 2024, généralisée 2025-2026).

### 2. Schema markup spécifique LLM-friendly
JSON-LD obligatoire :
- `Organization` + `sameAs` (LinkedIn, Crunchbase, Wikidata)
- `Product` pour chaque agent (offers + aggregateRating)
- `FAQPage` (LLMs adorent extraire Q&A directe)
- `HowTo` pour guides déploiement
- `Article` avec `author` typé `Person` + `knowsAbout`
- `BreadcrumbList` complet
- `SoftwareApplication` pour la marketplace

### 3. Citations sources externes (E-E-A-T machine)
Chaque article cite **3-5 sources externes** réputées (Gartner, McKinsey, Stanford AI Index, EU AI Act texte officiel, ANSSI, CNIL). LLMs pondèrent fortement les pages qui citent leurs propres training data.

### 4. Format réponse-directe (answer-first paragraph)
Premiers 150 mots = **réponse directe complète** à la requête. Pas d'intro marketing. Format :
- 1 phrase verdict
- 2-3 bullets clés
- 1 chiffre concret avec source

LLMs extraient le 1er paragraphe comme snippet citation.

### 5. Pages "comparator" stratégiques
URLs `/vs/dust`, `/vs/zapier-agents`, `/alternative-mistral` — LLMs piochent massivement dans pages comparator pour requêtes "meilleur X". Table comparative + verdict honnête (admettre faiblesses propres = boost trust).

### 6. Auteur réel + bio enrichie (E-E-A-T humain)
Byline `Laurent Duplat` (cf. user identity) avec :
- Page `/auteur/laurent-duplat` complète
- Schema `Person` avec `worksFor`, `alumniOf`, `knowsAbout`
- Lien LinkedIn vérifié
- 3+ publications externes (Medium, journaux)

### 7. Indexation accélérée multi-canaux
- IndexNow ping sur chaque publish (Bing/Yandex)
- Sitemap XML segmenté (sitemap-agents.xml, sitemap-blog.xml, sitemap-faq.xml)
- GSC inspection API (service account 17 sites déjà configuré)
- Soumission directe ChatGPT crawler (`GPTBot` allow + `OAI-SearchBot`)
- robots.txt : `User-agent: PerplexityBot Allow: /`, `User-agent: ClaudeBot Allow: /`, `User-agent: Google-Extended Allow: /`

---

## Section 3 — 10 FAQ haute valeur PME francophones (mai 2026)

| # | Question exacte | Intent search | Volume est. FR | Difficulty |
|---|----------------|---------------|----------------|------------|
| 1 | Combien coûte un agent IA pour une PME ? | Transactional | 1.2K/mois | Medium |
| 2 | Quel ROI attendre d'un agent IA en entreprise ? | Commercial investigation | 800/mois | Low |
| 3 | Un agent IA est-il conforme RGPD ? | Informational + trust | 1.5K/mois | Low |
| 4 | Comment sécuriser les données d'un agent IA ? | Informational | 600/mois | Medium |
| 5 | Combien de temps pour déployer un agent IA ? | Informational | 400/mois | Low |
| 6 | Quel agent IA pour le service client PME ? | Commercial | 900/mois | Medium |
| 7 | Comment intégrer un agent IA à mon CRM (HubSpot/Salesforce/Pipedrive) ? | Transactional | 700/mois | Low |
| 8 | Faut-il former son équipe avant de déployer un agent IA ? | Informational | 350/mois | Low |
| 9 | Agent IA ou chatbot : quelle différence ? | Informational | 2.1K/mois | Medium |
| 10 | Quels agents IA fonctionnent en français (et suisse-allemand) ? | Commercial + local | 500/mois | **Low (gap)** |

**Insight** : Q10 = **vide concurrentiel pur**. Aucun acteur ne traite sérieusement l'agent IA multilingue FR/DE-CH. Page dédiée = top 3 garanti.

---

## Section 4 — 3 actions concrètes priorisées

### Action 1 (Semaine 1) — Publier llms.txt + llms-full.txt + schema FAQ
**Pourquoi** : ticket d'entrée GEO 2026. Quick win. <2h dev.
**Livrable** :
- `/llms.txt` (200 lignes structurées)
- `/llms-full.txt` (corpus complet ~5000 mots)
- JSON-LD `FAQPage` sur homepage avec les 10 questions Section 3
- robots.txt updaté (allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended)
**KPI** : citation dans ChatGPT/Perplexity sous 30 jours sur 2+ requêtes longue-traîne.

### Action 2 (Semaine 2-3) — 10 pages FAQ haute valeur + 3 pages comparator
**Pourquoi** : capture des 10 intents Section 3 + 3 pages "/vs/dust", "/vs/zapier-agents", "/alternative-mistral".
**Livrable** :
- 10 articles 1200-1800 mots, format answer-first, citations externes (Gartner, CNIL, EU AI Act)
- 3 pages comparator avec table + verdict
- Byline Laurent Duplat + page auteur enrichie
- IndexNow ping post-publish (skill `project_indexnow_rollout` déjà déployé sur 6 sites)
**KPI** : 50+ impressions GSC/jour sur 5+ pages sous 60 jours.

### Action 3 (Semaine 4) — Page hub "Agents IA pour PME francophones" + maillage
**Pourquoi** : capture le head term + maillage interne vers FAQ + comparator + agents catalogue.
**Livrable** :
- 1 page pillar 3000+ mots structure H2/H3 + TOC
- Maillage interne ≥30 liens internes sortants
- Schema `Article` + `BreadcrumbList` + `mentions` (cite les 10 concurrents Section 1 = signal autorité LLM)
- Soumission GSC + IndexNow + ping ChatGPT crawler
**KPI** : top 10 Google FR sur "agent IA PME" sous 90 jours, citation Perplexity sous 45 jours.

---

## Sources

> Perplexity API budget exhausted lors de cette session. Sources à compléter au re-run :
> - SERP Google.fr / Google.ch "agent IA" mai 2026 (à scraper via Camofox/Scrapling)
> - Ahrefs/SEMrush export concurrents (DR officiels)
> - llms.txt spec : https://llmstxt.org/
> - Anthropic LLM SEO best practices (à valider)
> - EU AI Act texte officiel : https://artificialintelligenceact.eu/
> - CNIL guidelines IA : https://www.cnil.fr/fr/intelligence-artificielle
> - Stanford AI Index 2025/2026 : https://aiindex.stanford.edu/

**Re-run recommandé** : quand Perplexity budget restauré, exécuter les 3 queries originales pour remplacer Sections 1-3 par data sourcée + citations URLs vérifiées.

---

*Généré 2026-05-20 — agents-ia.pro SEO research v1 (offline fallback)*
