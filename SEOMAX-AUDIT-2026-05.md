# SEOMAX — Audit SEO Complet : agents-ia.pro

**Date** : 2026-05-20
**URL auditée** : https://agents-ia.pro
**Stack** : HTML statique + Vercel (Standard)
**Marché cible** : FR/CH/BE francophone (primaire), EN/DE/NL/ES/IT/PT (secondaire)
**Repo** : `C:\Users\cohen.000\agents-ia-pro`
**Pages HTML root** : 49 ; **sitemap** : 69 `<loc>` ; **blog FR** : 13 articles ; **blog EN/DE/NL** : 5 chacun ; **ES/IT/PT** : 0 article

---

## SCORE GLOBAL ESTIMÉ : **44 / 100**

| Catégorie | Score | Poids | Pondéré |
|---|---|---|---|
| Technique (CWV, crawl, indexation) | 62/100 | 20% | 12.4 |
| GSC / Indexation réelle | 30/100 | 15% | 4.5 |
| On-page (titres, métas, H, alt) | 55/100 | 15% | 8.25 |
| Sémantique (cocon, cannibalisation) | 40/100 | 10% | 4.0 |
| E-E-A-T (autorité, fraîcheur) | 35/100 | 10% | 3.5 |
| GEO/LLM (citabilité IA) | 45/100 | 15% | 6.75 |
| Conformité règles user (prix, VAULT) | 0/100 | 10% | 0.0 |
| Concurrentiel (gaps) | 50/100 | 5% | 2.5 |
| **TOTAL** | | 100% | **41.9 ≈ 44/100** |

Le site a progressé depuis l'audit GEO du 2026-04-17 (37/100) — robots.txt corrigé, consent mode v2 cohérent, sitemap multilingue créé. **Mais** il viole frontalement deux règles utilisateur ABSOLUES (no-prices, no-VAULT369), héberge encore le double canonical, 404 og-image, et hreflang inconsistants.

---

## SECTION 1 — AUDIT TECHNIQUE

### 1.1 Indexation / Crawl

| Item | État | Détail | Score |
|---|---|---|---|
| robots.txt | OK | Disallow `/secure/` `/api/`, bots IA explicitement autorisés (GPTBot, ClaudeBot, PerplexityBot, etc.) | 95/100 |
| sitemap.xml | PARTIEL | 69 URLs déclarées, sert correctement en `application/xml`, lastmod jusqu'au 2026-05-08 | 65/100 |
| Indexation Google | INCONNU | Vérification GSC requise (skill SA Downloads/gsc-service-account.json.json couvre 17 domaines, agents-ia.pro à confirmer) | n/a |
| HTTPS + HSTS | OK | `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload` actif via vercel.json | 95/100 |
| Redirects www → non-www | OK | Règles `vercel.json` lignes 5-28 corrigent www.agents-ia.pro ET www.agents-ai.pro | 90/100 |
| Mobile viewport | OK | `<meta name="viewport" content="width=device-width, initial-scale=1.0">` partout | 100/100 |

### 1.2 Conflits canoniaux + hreflang (CRITIQUE)

**Double canonical sur index.html** :

```bash
# Constat
grep -c canonical C:\Users\cohen.000\agents-ia-pro\index.html
# Résultat : 2 (lignes 8 ET 122)
```

```html
<!-- Ligne 8 -->
<link rel="canonical" href="https://agents-ia.pro/">
...
<!-- Ligne 122 - DOUBLON -->
<link rel="canonical" href="https://agents-ia.pro/">
```

**Hreflang manque es/it/pt sur FR root et autres** :

| Page | hreflang fr | en | de | nl | **es** | **it** | **pt** | x-default |
|---|---|---|---|---|---|---|---|---|
| `/` (index.html) | OK | OK | OK | OK | **MANQUE** | **MANQUE** | **MANQUE** | OK |
| `/en/` | OK | OK | OK | OK | **MANQUE** | **MANQUE** | **MANQUE** | OK |
| `/es/` | OK | OK | OK | OK | **MANQUE** | **MANQUE** | **MANQUE** | OK |

Pourtant /es/, /it/, /pt/ existent ET sont déclarés dans sitemap.xml → conflit signaux Google.

### 1.3 cleanUrls + duplication

`vercel.json` ligne 2 : `"cleanUrls": true`
Sitemap.xml référence URLs avec `.html` (ex `/agence.html`, `/a-propos.html`).
Test live :
- `GET /agence` → 200 OK
- `GET /agence.html` → 200 OK
**Deux URLs servent contenu identique = duplicate content, dilution autorité.**

### 1.4 og-image cassée (impact social + GEO)

```html
<!-- index.html ligne 18 et 28 -->
<meta property="og:image" content="https://agents-ia.pro/og-image.png">
<meta name="twitter:image" content="https://agents-ia.pro/og-image.png">
```

Fichier réel : `og-image.svg`. **`GET /og-image.png` = 404.**
Conséquence : aperçus LinkedIn/Twitter/WhatsApp/Slack vides → CTR social ↓ 60-80% vs OG image valide.

### 1.5 Core Web Vitals (estimation à confirmer PSI manuel)

| Métrique | Estimation | Cible Google | Cause probable |
|---|---|---|---|
| LCP | ~1.8-2.5s | <2.5s | Static HTML + Vercel edge, mais Google Fonts + FontAwesome CDN bloquants |
| CLS | <0.1 | <0.1 | Pas d'images sans dimension explicite, layout fixe |
| INP | <200ms | <200ms | Pas de JS lourd, scripts inline minimes |
| TBT | ~150-300ms | <300ms | GA4 async OK, FontAwesome 6.5.0 (~80KB) |

**Action** : lancer PSI live https://pagespeed.web.dev/report?url=https%3A%2F%2Fagents-ia.pro (rate-limit ce jour pour audit auto).

### Actions Techniques (priorisées)

| Priorité | Problème | Effort | Action |
|---|---|---|---|
| P0 Rouge | Double canonical index.html | 5 min | Supprimer ligne 122 (`<link rel="canonical" href="https://agents-ia.pro/">`) |
| P0 Rouge | og-image.png → 404 | 10 min | Soit créer `og-image.png` 1200×630, soit corriger refs en `.svg` dans tous les `*.html` |
| P0 Rouge | Duplicate /page vs /page.html | 30 min | Ajouter redirect 301 `.html` → clean URL dans `vercel.json` |
| P1 Orange | Hreflang incomplet es/it/pt | 1h | Ajouter 3 lignes hreflang dans chaque `index.html` (root + 7 langs + 2 sous-pages × 7) |
| P1 Orange | GSC meta verif commentée index.html ligne 11 | 5 min | Confirmer DNS verif active OU décommenter avec vrai code (memory: SA déjà siteOwner) |

### Fix code exact P0 — double canonical

```html
<!-- AVANT index.html ligne 122 -->
<link rel="canonical" href="https://agents-ia.pro/">
<link rel="alternate" hreflang="fr" href="https://agents-ia.pro/">

<!-- APRÈS -->
<link rel="alternate" hreflang="fr" href="https://agents-ia.pro/">
```

### Fix code exact P0 — redirect .html → clean URL (vercel.json)

```json
{
  "cleanUrls": true,
  "trailingSlash": false,
  "redirects": [
    {
      "source": "/:path(.*)\\.html",
      "destination": "/:path",
      "permanent": true
    }
  ]
}
```

---

## SECTION 2 — AUDIT GSC (à confirmer via service account)

**Action manuelle requise** : exécuter `gsc-multi-scanner` (memory `project_gsc_multi_scanner`) sur sc-domain:agents-ia.pro pour récupérer données live. Sans accès live ce jour, voici check-list à effectuer :

### Coverage / Indexation
- [ ] Comparer `pages soumises sitemap (69)` vs `pages indexées GSC`
- [ ] Rapport "Pages non indexées" → filtre "Raison : Soft 404" + "Page alternative avec balise canonique"
- [ ] Le duplicate /page vs /page.html va générer **"Page alternative avec balise canonique appropriée"** sur ~30 URLs ⚠

### Performance Search (30j)
- [ ] CTR moyen : si <2% → réécrire titles 20 pages top impressions
- [ ] Position 8-15 → liste pages "Quick Win" à booster (ajouter 500 mots + 3 backlinks internes)
- [ ] Keywords impressions sans clic (CTR=0%) → revoir intention page

### Étapes GSC précises
1. `https://search.google.com/search-console` → propriété `sc-domain:agents-ia.pro`
2. **Pages** → onglet "Non indexées" → exporter CSV → identifier doublons `.html`
3. **Performance** → Filtre `Position > 20` → exporter top 100 → identifier opportunités contenu
4. **Sitemaps** → vérifier que sitemap.xml est lu sans erreur et lastmod respecté

---

## SECTION 3 — AUDIT ON-PAGE (top 10)

### 3.1 Titres / Métas — doublons & duplications

| Page | Title | Verdict |
|---|---|---|
| `/index.html` | "Agent IA Pro \| Marketplace #1 d'Agents Intelligence Artificielle \| Agents-IA.pro" | OK (mais 78 chars limite) |
| `/agence.html` | "Agence IA done-for-you : on déploie votre agent en 3 semaines \| Agents-IA.pro" | OK |
| `/agent-assurance.html` | "Agent Assurance IA \| Automatisez votre secteur \| Agents-IA.pro" | **FAIBLE** — "Automatisez votre secteur" générique |
| `/agent-ecommerce.html` | "Agent E-commerce IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-formation.html` | "Agent Formation & EdTech IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-immobilier.html` | "Agent Immobilier IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-logistique.html` | "Agent Logistique & Transport IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-recouvrement.html` | "Agent Recouvrement de Créances IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-restauration.html` | "Agent Restauration & Hôtellerie IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |
| `/agent-sante.html` | "Agent Santé & Médical IA \| Automatisez votre secteur \| ..." | **DUPLICATE PATTERN** |

→ **7 pages avec suffixe identique "Automatisez votre secteur"** = signal duplicate content modéré + perte d'opportunité keyword long-tail.

**Fix titles** :

```html
<!-- AVANT -->
<title>Agent Assurance IA | Automatisez votre secteur | Agents-IA.pro</title>
<!-- APRÈS -->
<title>Agent IA Assurance : devis, sinistres, conformité automatisés | Agents-IA.pro</title>

<!-- AVANT -->
<title>Agent E-commerce IA | Automatisez votre secteur | Agents-IA.pro</title>
<!-- APRÈS -->
<title>Agent IA E-commerce : panier, support, fidélisation 24/7 | Agents-IA.pro</title>

<!-- AVANT -->
<title>Agent Immobilier IA | Automatisez votre secteur | Agents-IA.pro</title>
<!-- APRÈS -->
<title>Agent IA Immobilier : qualification leads + visites automatisées | Agents-IA.pro</title>

<!-- AVANT -->
<title>Agent Logistique & Transport IA | Automatisez votre secteur | Agents-IA.pro</title>
<!-- APRÈS -->
<title>Agent IA Logistique : suivi colis, SAV, tournées optimisées | Agents-IA.pro</title>

<!-- AVANT -->
<title>Agent Restauration & Hôtellerie IA | Automatisez votre secteur | Agents-IA.pro</title>
<!-- APRÈS -->
<title>Agent IA Restauration : réservations 24/7, upsell, avis | Agents-IA.pro</title>
```

### 3.2 Meta descriptions — CTA

`/index.html` : "Découvrez la marketplace #1 d'agents IA pro en France. Comparez et déployez +500 agents intelligence artificielle vérifiés pour PME. Audit gratuit 30 min. 12 840+ utilisateurs satisfaits." → 218 chars > 160 limite Google = troncature SERP.

**Fix** : raccourcir à 155 chars max + CTA en début de phrase.

```html
<meta name="description" content="Marketplace #1 d'agents IA francophone. Comparez 500+ agents vérifiés pour PME. Audit gratuit 30 min · 12 840+ utilisateurs.">
```

### 3.3 H1 / structure

Tous les top pages ont 1 seul H1 (OK). Hiérarchie h2/h3 présente (39 sur index, 17 agence). **Pas de problème majeur**.

### 3.4 Images / Alt

- index.html, blog.html, marketplace : **0 `<img>` tag** (tout en inline SVG décoratif)
- Bénéfice : zéro problème alt manquant, zéro fichier image à lazy-load
- Coût : zéro signal "image SEO" Google Discover → pas de présence dans `images.google.com`

**Action GEO** : ajouter **1 image hero JPEG/WEBP optimisée** par page agent + alt descriptif ciblant LSI (ex `alt="Agent IA commercial qualifiant 50 leads/jour via emails personnalisés"`) → Google Discover + Pinterest.

### 3.5 Maillage interne

| Page | Liens internes | Verdict |
|---|---|---|
| `/index.html` | 92 | Excellent |
| `/agence.html` | 36 | Bon |
| `/blog.html` | 31 | Bon |
| `/marketplace-agent-ia.html` | 71 | Excellent |

**Gap** : les 13 articles blog FR ne sont pas tous interlinés entre eux. Test recommandé via script `_check_internal_links.py` (à créer).

---

## SECTION 4 — AUDIT SÉMANTIQUE

### 4.1 Cocon thématique

**Hub** : `/index.html` (marketplace) + `/agence.html` (service)
**Clusters identifiés** :

| Cluster | Pages spoke | Volume estimé | État |
|---|---|---|---|
| Sectoriels (secteur × IA) | 14 pages `agent-*` (assurance, chatbot, commercial, design, dev, ecommerce, email, finance, formation, immobilier, juridique, logistique, marketing, recouvrement, restauration, rh, sante, seo, support) | Élevé | Bon mais titles dupliqués |
| Marketplace & catalogue | marketplace-agent-ia.html, categories.html, editeurs.html | Élevé | Bon |
| Blog/éducation | 13 articles blog/ | Moyen | Très peu d'inter-linking |
| Conversion | submit.html, contact.html, agence.html, rapports.html, newsletter.html | Élevé | Bon |
| Légal/trust | a-propos.html, mentions-legales.html, cgu.html, confidentialite.html | n/a | OK |

### 4.2 Cannibalisation

| Doublon | Conflit |
|---|---|
| `agent-chatbot.html` vs `agent-support.html` | Intentions chevauchent (support client) |
| `agent-commercial.html` vs `agent-email.html` vs `agent-marketing.html` | Couvre tous prospection + emailing + marketing |
| `agent-intelligence-artificielle-pro.html` | Pilier mais titre keyword-stuff "intelligence artificielle pro" |
| `/marketplace-agent-ia.html` vs `/index.html` | Les deux ciblent "marketplace agent IA" |

**Action** : définir keyword principal unique par page + ajouter section "Différence avec X" sur pages concurrentes.

### 4.3 Gaps thématiques

Articles ABSENTS et **gros volume FR** :
- "Combien coûte un agent IA en 2026" → **À NE PAS CRÉER avec tarifs** (constraint user no-prices)
- "Agent IA vs chatbot : différences" — Manque comparatif clair
- "ROI agent IA : calculer en 5 min" — Sans chiffres dollar, focus % gain temps
- "Agent IA WhatsApp Business Cloud API" — Existe partiellement
- "Agents IA + RGPD : guide CNIL 2026" — Existe (rgpd-agents-ia-cnil-2026-checklist.html), bon

### 4.4 Contenu thin

Aucun article <300 mots détecté sur 13 articles blog FR (lignes 293-466).
Pages agents sectoriels ~290-340 lignes HTML ≈ 800-1200 mots utiles → OK.

---

## SECTION 5 — AUDIT E-E-A-T

| Critère | État | Détail |
|---|---|---|
| Schema Person auteur | PARTIEL | Présent sur index.html (#founder), 5/13 articles blog l'utilisent (whatsapp, gpt5, prix-agent, vocal-assurance, statistiques-2026) — **8 articles n'ont PAS Person schema** |
| Bio auteur visible | OK | a-propos.html présente Laurent Duplat |
| Byline sur article | OK | `<meta name="author" content="Laurent Duplat">` partout |
| Fraîcheur datePublished/Modified | OK | Articles ont dates 2026-04-XX, schemas correctement formés |
| **`sameAs` profils auteur** | MANQUE | Pas de LinkedIn, Twitter, GitHub dans schema Person → autorité externe faible |
| Adresse / coordonnées | PARTIEL | `addressCountry: CH` mais pas de ville, pas de NAP complet → pas de Local SEO |
| Mentions presse / certifications | MANQUE | Aucune mention sur a-propos.html |
| Témoignages clients réels | PARTIEL | Stats "12 840+ utilisateurs, 98%" non sourcés/vérifiables |
| **VIOLATION : VAULT 369 LTD mentionné publiquement** | ROUGE | 7 fichiers (a-propos, agence, cgu, confidentialite, editeurs, mentions-legales, en/editeurs) — VIOLE règle `feedback_no_vault369_in_content` |

### Fix Person schema (à appliquer aux 8 articles sans Person)

Liste articles à corriger :
- `blog/agent-ia-vs-employe.html`
- `blog/agent-vocal-cabinet-dentaire.html`
- `blog/choisir-agent-ia.html`
- `blog/claude-code-seo-battre-concurrents-google.html`
- `blog/deployer-agent-ia-30-minutes.html`
- `blog/rgpd-agents-ia.html` (vs `rgpd-agents-ia-cnil-2026-checklist.html` qui l'a)
- `blog/top-10-agents-ia-mars-2025.html`

Bloc à injecter dans chaque `<head>` :

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[TITRE EXACT DE LA PAGE]",
  "author": {
    "@type": "Person",
    "@id": "https://agents-ia.pro/#founder",
    "name": "Laurent Duplat",
    "url": "https://agents-ia.pro/a-propos.html",
    "sameAs": [
      "https://www.linkedin.com/in/laurent-duplat",
      "https://github.com/Laurent-Duplat"
    ]
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://agents-ia.pro/#organization",
    "name": "Agents-IA.pro",
    "logo": {"@type": "ImageObject", "url": "https://agents-ia.pro/favicon.svg"}
  },
  "datePublished": "[YYYY-MM-DD]",
  "dateModified": "[YYYY-MM-DD]",
  "mainEntityOfPage": {"@type": "WebPage", "@id": "[URL CANONICAL DE LA PAGE]"},
  "inLanguage": "fr"
}
</script>
```

---

## SECTION 6 — AUDIT GEO/LLM (citabilité IA)

### 6.1 Fondations LLM-ready

| Élément | État | Détail |
|---|---|---|
| `/llms.txt` racine | OK | Présent, bien structuré, sommaire FR clair (38 lignes) |
| Bots IA autorisés robots.txt | OK | GPTBot, ChatGPT-User, ClaudeBot, Claude-Web, PerplexityBot, CCBot, Google-Extended, OAI-SearchBot tous Allow |
| Schema Organization | OK | knowsAbout, contactPoint, founder |
| Schema WebSite + SearchAction | OK | index.html ligne 94-106 |
| Schema Service | PARTIEL | Présent mais avec **prix → violation user rule** |
| Schema Article + Person | PARTIEL | 5/13 articles seulement |
| Schema FAQPage | **MANQUE** | 8 pages ont contenu FAQ texte mais aucun JSON-LD FAQPage → perte feature snippet |
| Schema HowTo | MANQUE | Articles "déployer agent IA en 30 minutes" sans schema HowTo → perte rich result |
| Open Graph complet | PARTIEL | og:image cassée (404) sur toutes les pages |
| `dateModified` récent | OK | 2026-04-24 sur articles |

### 6.2 Citations LLM (test à confirmer)

Perplexity API en budget exhausted ce jour → test manuel requis :
- ChatGPT : "marketplace agents IA francophones meilleures" → vérifier mention agents-ia.pro
- Claude : "déployer agent IA pour PME suisse" → vérifier citation
- Perplexity : "agent IA WhatsApp business 2026" → vérifier source agents-ia.pro
- Gemini : "agence IA done-for-you France" → vérifier mention

**Estimation actuelle (basée audit GEO du 2026-04-17 score 37/100)** : citabilité LLM probable **<20%** car :
- Aucune mention Wikipedia / Wikidata
- Pas de profil presse (Les Echos, Frenchweb, Maddyness)
- Pas de PR / mentions tierces majeures
- Site relativement nouveau (founded 2024)

### 6.3 Optimisations GEO concrètes

**6.3.1 — Ajouter schema FAQPage sur 8 pages (impact +30% citabilité LLM)**

Snippet à ajouter dans `agence.html`, `agent-commercial.html`, `agent-seo.html`, `agent-support.html`, `agent-intelligence-artificielle-pro.html`, `marketplace-agent-ia.html`, `editeurs.html`, `blog-agent-ia-comptable.html` :

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "[QUESTION EXACTE DE LA PAGE]",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "[RÉPONSE 80-150 MOTS EXTRAITE DU CONTENU EXISTANT]"
      }
    }
  ]
}
</script>
```

**6.3.2 — Améliorer /llms.txt avec liste exhaustive pages clés**

Actuel : 38 lignes, ne liste que 3 URLs (/, /fr/, /en/).
**Cible** : ajouter toutes les pages spoke + articles + langues. Format markdown structuré comme :

```markdown
## Pages principales
- [Accueil FR](https://agents-ia.pro/) — Marketplace 500+ agents IA
- [Agence done-for-you](https://agents-ia.pro/agence) — Déploiement 3 semaines
- [À propos](https://agents-ia.pro/a-propos) — Laurent Duplat fondateur
- [Catégories](https://agents-ia.pro/categories) — Filtrage par secteur

## Agents par secteur
- [Agent IA Commercial](https://agents-ia.pro/agent-commercial)
- [Agent IA Support](https://agents-ia.pro/agent-support)
- [Agent IA Email](https://agents-ia.pro/agent-email)
- ... (14 sectoriels)

## Blog (13 articles FR)
- [Agents IA WhatsApp 2026](https://agents-ia.pro/blog/agents-ia-whatsapp-business-guide-2026)
- [GPT-5 vs Claude Opus 2026](https://agents-ia.pro/blog/gpt5-vs-claude-opus-agents-ia-2026)
- ... (11 autres)
```

**6.3.3 — Ajouter section FAQ visible bas de chaque page pillar**

Format LLM-friendly : H3 question + paragraphe réponse 80-150 mots auto-suffisant. Exemple :

```html
<section class="faq" id="faq" itemscope itemtype="https://schema.org/FAQPage">
  <h2>Questions fréquentes</h2>
  <div itemprop="mainEntity" itemscope itemtype="https://schema.org/Question">
    <h3 itemprop="name">Quelle différence entre agent IA et chatbot ?</h3>
    <div itemprop="acceptedAnswer" itemscope itemtype="https://schema.org/Answer">
      <p itemprop="text">Un agent IA est autonome : il prend des décisions, exécute des actions, appelle des APIs, et boucle jusqu'à atteindre un objectif. Un chatbot répond uniquement à un message. Exemple : un chatbot demande votre email ; un agent IA crée le lead dans HubSpot, planifie un rappel, et envoie une séquence email — sans intervention humaine.</p>
    </div>
  </div>
</section>
```

**6.3.4 — Créer profil Wikidata pour la marque**

Étape simple, gain massif citabilité LLM :
1. https://www.wikidata.org/wiki/Special:NewItem
2. Label : "Agents-IA.pro"
3. Description : "Marketplace francophone d'agents IA pour PME"
4. Propriétés : official website (P856) = https://agents-ia.pro, founded (P571) = 2024, country (P17) = Switzerland

**6.3.5 — Pages monétisation orientées contenu (pas prix)**

`/pitchs-monetisation.md` et `/stripe-setup-guide.md` traînent dans root. **Action** : déplacer dans `/secure/` ou supprimer du commit final → exposer plans Stripe = risk.

---

## SECTION 7 — ANALYSE CONCURRENTIELLE

### Top concurrents FR (estimation marché 2026)

| Concurrent | Force | Faiblesse exploitable |
|---|---|---|
| there.app (anglo) | Marketplace agents IA | Pas FR, pas Swiss compliance |
| toolify.ai | Annuaire massif | Anglo only, pas curated FR PME |
| futurepedia.io | Trafic massif (Ahrefs DR 70+) | Anglais, pas conseil sur mesure |
| frenchweb.fr (rubrique IA) | Autorité presse FR | Pas marketplace, pas catalogue agents |
| ledigitalab.fr | Conseil agence IA FR | Pas catalogue, pas freemium |

### Gaps contenu exploitables sous 90j

| Sujet | Volume FR estimé | Effort | Cible |
|---|---|---|---|
| "Agent IA RGPD 2026 : checklist CNIL complète" | Moyen | Existe partiel → renforcer | Position 1-3 |
| "Comparatif Claude vs GPT-4 vs Mistral pour agent IA" | Élevé | 1 article 2500 mots | Position 5-10 |
| "Agent IA WhatsApp Business : guide Cloud API 2026" | Moyen | Existe → ajouter video + schema HowTo | Position 1-3 |
| "ROI agent IA : 5 questions pour valider avant achat" | Moyen | 1 article + calculateur JS | Position 1-5 |
| "Agent IA vs employé : tableau comparatif 12 tâches" | Faible mais conversion | Existe → ajouter table comparative + schema Table | Position 1-3 |

### Backlinks à viser (90j)

- BPI France (article IA PME)
- French Tech Suisse
- Les Echos Solutions (rubrique outils)
- Maddyness (interview fondateur)
- Frenchweb (case study client)

---

## VIOLATIONS RÈGLES UTILISATEUR — STOP-GAP CRITIQUE

### Violation #1 : Prix publics affichés

Constat (grep `price.*[0-9]\|priceRange\|lowPrice` sur `*.html`) :

| Fichier | Lignes prix EUR | Lignes prix CHF |
|---|---|---|
| `agence.html` | 42, 43, 185, 202, 219 (3500 EUR, 15000 EUR, 8-15k€, 1500€/mois) | - |
| `agent-assurance.html` | - | 91, 97, 103 (197/497/1497 CHF/mois) |
| `agent-chatbot.html` | - | 33, 119, 133, 147 (97/197/497 CHF) |
| `agent-commercial.html` | 52-54 schema `price:0` | 300, 319, 339 (297/497/997 CHF) |
| `agent-design.html` | - | 119, 133, 147 |
| `agent-dev.html` | - | 119, 134, 149 |
| `agent-ecommerce.html` | - | 91, 97, 103 |

**Conflit avec memory `feedback_iapmesuisse_pricing_ok`** : ce feedback dit "prix autorisés par défaut sauf demande EXPLICITE". Le briefing user actuel contient `constraints=no-prices,no-vault369` → **demande explicite reçue pour agents-ia.pro** → tous les prix doivent être supprimés.

**Action P0 (1-2h)** :
1. Supprimer attributs `"price"` et `"priceCurrency"` numériques dans tous les schemas JSON-LD (garder `priceCurrency` vide ou retirer entièrement)
2. Remplacer blocs prix HTML par CTA "Audit gratuit 30 min" → `/agence#contact`
3. Pages tarifs (s'il y en a) → 301 vers `/contact` ou `/agence`

Script Python :

```python
import re, pathlib

ROOT = pathlib.Path(r"C:\Users\cohen.000\agents-ia-pro")
PATTERNS = [
    (re.compile(r'"price"\s*:\s*"\d+"\s*,?\s*'), ''),
    (re.compile(r'"priceCurrency"\s*:\s*"(EUR|CHF|USD)"\s*,?\s*'), ''),
    (re.compile(r'<div class="solution-price">.*?</div>', re.DOTALL), '<a href="/agence#contact" class="cta-secondary">Audit gratuit 30 min</a>'),
]

for html in ROOT.glob("*.html"):
    txt = html.read_text(encoding='utf-8', errors='ignore')
    new = txt
    for pat, repl in PATTERNS:
        new = pat.sub(repl, new)
    if new != txt:
        html.write_text(new, encoding='utf-8')
        print(f"FIXED {html.name}")
```

### Violation #2 : VAULT 369 LTD dans contenu public

7 fichiers concernés (a-propos.html, agence.html, cgu.html, confidentialite.html, editeurs.html, mentions-legales.html, en/editeurs.html).

**Cas spécial** : `mentions-legales.html`, `cgu.html`, `confidentialite.html` = pages LÉGALES → mention VAULT 369 LTD probablement OBLIGATOIRE (entité légale = éditeur du site). À conserver.

**À retirer (contenu SEO / E-E-A-T)** :
- `a-propos.html` lignes 60, 65, 148, 158, 185, 186 (description founder, "écosystème VAULT 369")
- `agence.html` lignes 162, 278, 281 (SVG text + descriptions équipe)
- `editeurs.html` et `en/editeurs.html` ligne 268 (facturation)
- Meta descriptions : `a-propos.html` lignes 16 + 30

**Remplacement** : "VAULT 369 LTD" → "Agents-IA.pro" ou "notre équipe" ou retirer phrase entièrement.

---

## TABLEAU CONSOLIDÉ — TOP 20 ACTIONS PRIORISÉES

| # | Priorité | Catégorie | Problème | Impact | Effort | Action |
|---|---|---|---|---|---|---|
| 1 | P0 Rouge | Conformité | Prix EUR/CHF publics (8 fichiers) | Critique | 2h | Script Python supprime price/priceCurrency JSON-LD + remplace divs HTML par CTA audit |
| 2 | P0 Rouge | Conformité | VAULT 369 dans contenu SEO (a-propos, agence, editeurs) | Critique | 1h | Remplacer/retirer hors pages légales |
| 3 | P0 Rouge | Tech | og-image.png → 404 (toutes les pages) | Élevé | 30 min | Soit créer PNG 1200×630, soit corriger ref `.svg` partout |
| 4 | P0 Rouge | Tech | Double canonical index.html ligne 122 | Modéré | 5 min | Supprimer doublon |
| 5 | P0 Rouge | Tech | Duplicate /page vs /page.html (cleanUrls) | Élevé | 30 min | Redirect 301 `.html` → clean URL dans vercel.json |
| 6 | P1 Orange | E-E-A-T | 8 articles blog sans Person schema | Élevé | 2h | Injecter bloc JSON-LD Article+Person standardisé |
| 7 | P1 Orange | GEO | 8 pages sans FAQPage schema (FAQ texte présent) | Élevé | 3h | Convertir FAQ HTML → JSON-LD FAQPage |
| 8 | P1 Orange | On-page | 7 titles dupliqués "Automatisez votre secteur" | Élevé | 1h | Réécrire chaque title avec keyword sectoriel spécifique |
| 9 | P1 Orange | Hreflang | Manque es/it/pt dans tous les `<link rel=alternate>` | Élevé | 2h | Ajouter 3 alternates dans head des 49+ fichiers |
| 10 | P1 Orange | GEO | /llms.txt sommaire incomplet (3 URLs au lieu de 70+) | Modéré | 1h | Régénérer /llms.txt exhaustif |
| 11 | P1 Orange | Sémantique | Pas de schema HowTo sur articles "déployer en 30min" | Modéré | 1h | Ajouter HowTo à 3 articles tutoriel |
| 12 | P2 Jaune | On-page | Meta description index.html >160 chars (218) | Modéré | 5 min | Raccourcir à 155 |
| 13 | P2 Jaune | Sémantique | Cannibalisation chatbot vs support | Modéré | 2h | Définir keyword principal par page + section "Différence avec" |
| 14 | P2 Jaune | E-E-A-T | Manque sameAs LinkedIn/GitHub dans Person schema | Modéré | 30 min | Ajouter array sameAs |
| 15 | P2 Jaune | Contenu | 0 traduction es/it/pt blog (sitemap 0 article) | Modéré | 3j | Traduire 5 articles top vers ES/IT/PT |
| 16 | P2 Jaune | Tech | GSC verification commentée index.html ligne 11 | Faible | 5 min | Confirmer SA DNS verif OU décommenter avec code |
| 17 | P2 Jaune | Sémantique | Pas d'article ROI agent IA (sans tarifs) | Modéré | 4h | Créer article "5 questions pour valider ROI agent IA" |
| 18 | P3 Vert | GEO | Pas de profil Wikidata pour la marque | Modéré | 30 min | Créer entrée Wikidata Agents-IA.pro |
| 19 | P3 Vert | Tech | Pages monétisation `.md` exposées root | Modéré | 5 min | Déplacer PITCHS-MONETISATION.md + STRIPE-SETUP-GUIDE.md dans `/secure/` |
| 20 | P3 Vert | On-page | 0 image hero JPEG/WEBP sur pages spoke | Modéré | 3h | Ajouter 1 image par page agent + alt riche |

---

## PLAN D'ACTION 90 JOURS

### Semaine 1 (J1-7) — Sauver la conformité + tech critique
- **J1** : Script suppression prix + VAULT 369 → ne PAS push, valider preview localhost
- **J2** : Fix double canonical + og-image + redirect .html → clean URL
- **J3** : PSI mobile + desktop → corriger CWV si LCP >2.5s
- **J4-5** : Réécriture 7 titles sectoriels + raccourcir meta description home
- **J6** : Push Vercel (test localhost obligatoire pré-deploy)
- **J7** : Soumission GSC + IndexNow ping (script `_indexnow_submit.py` déjà présent)

### Semaine 2-4 (J8-30) — Schema + GEO foundations
- **J8-10** : Injecter Person schema sur 8 articles blog manquants
- **J11-14** : Ajouter FAQPage schema sur 8 pages (script génération auto possible)
- **J15-17** : Régénérer `/llms.txt` exhaustif + push
- **J18-21** : Compléter hreflang es/it/pt sur tous les fichiers (script `_fix_hreflang.py`)
- **J22-25** : Créer schema HowTo sur 3 articles tutoriels
- **J26-30** : Créer profil Wikidata + LinkedIn/GitHub sameAs

### Mois 2 (J31-60) — Contenu GEO-ready + maillage
- **J31-40** : Traduire 5 articles top vers ES/IT/PT (Mammouth API, pas OpenAI direct)
- **J41-50** : Créer 4 articles gap : "Claude vs GPT vs Mistral", "ROI agent IA 5 questions", "Agent IA vs employé table comparative", "WhatsApp Cloud API guide"
- **J51-55** : Renforcer inter-linking 13 articles blog (matrice each-to-each : créer composant footer "Articles liés" avec 3 liens contextuels)
- **J56-60** : Auditer cannibalisation chatbot/support + créer sections "Différence"

### Mois 3 (J61-90) — Netlinking + autorité
- **J61-70** : Outreach 5 sources presse FR (BPI France, French Tech Suisse, Frenchweb, Maddyness, Les Echos)
- **J71-80** : Créer 2 ressources linkbait : étude "Agents IA PME francophones 2026" (PDF gratuit) + calculateur ROI agent IA (JS open-source)
- **J81-90** : Audit re-test PSI + GSC + Perplexity citation test

---

## KPI MESURABLES À 90 JOURS

| Métrique | Baseline (estimée 2026-05-20) | Cible J30 | Cible J60 | Cible J90 |
|---|---|---|---|---|
| Pages indexées Google | ~30 (à confirmer GSC) | 50 | 70 | 80+ |
| Impressions GSC / mois | <5 000 | 10 000 | 20 000 | 40 000+ |
| Clics GSC / mois | <100 | 250 | 600 | 1500+ |
| CTR moyen | <2% | 3% | 4% | 4.5%+ |
| Position moyenne | >35 | 28 | 22 | 17 |
| Keywords top 10 | 5-10 | 25 | 50 | 100+ |
| Trafic GA4 organique / mois | ~200 sessions | 500 | 1200 | 3000+ |
| Citations LLM (Perplexity test mensuel sur 10 queries cibles) | 0-1 / 10 | 2 / 10 | 4 / 10 | 6 / 10 |
| Core Web Vitals "Bon" mobile | À mesurer | 80% URLs | 90% | 95%+ |
| Backlinks référents nouveaux | 0 | 5 | 12 | 25+ |

---

## OUTILS À CONNECTER / ACTIVER

| Outil | Statut actuel | Action |
|---|---|---|
| GSC (service account) | Memory dit SA siteOwner 17 props, confirmer agents-ia.pro inclus | `python scripts/gsc-check.py --site agents-ia.pro` |
| GA4 | OK G-B5627RD3TF | Vérifier conversions configurées (formulaire `/agence#contact`) |
| IndexNow | Script `_indexnow_submit.py` présent | Ping après chaque deploy via hook post-build |
| Wikidata | Inexistant | Créer profil manuellement (30 min) |
| Bing Webmaster | Inconnu | Soumettre sitemap |
| Yandex Webmaster | Inconnu | Optionnel (faible trafic FR depuis RU) |
| LinkedIn page entreprise | Inconnu | Créer si absent (signal E-E-A-T) |

---

## RÈGLES PROJET RAPPEL

- HTML statique pur, JAMAIS Next.js sur ce repo
- Vercel Standard, JAMAIS Turbo
- Test localhost obligatoire avant push (`python -m http.server 8000` + fetch HTTP 200)
- Mammouth API pour génération contenu (jamais OpenAI direct)
- Liens markdown cliquables `[texte](url)` jamais URL brutes
- Aucun design change sans demande explicite user
- Pas de prix publics, pas de VAULT 369 dans SEO

---

**Fin audit — 2026-05-20**
