# Audit E-E-A-T agents-ia.pro
Date: 2026-05-20 — Auditeur: research agent — Cible: Laurent Duplat (lead)

## Score global: 16,5 / 40 (FAIL — sous la barre passable de 24/40)

| Dimension | Score | Verdict |
|---|---|---|
| Experience | 5/10 | Cas clients OK mais sans noms réels, sans logos, sans screenshots, sans dates précises |
| Expertise | 5/10 | Bio fondateur faible (340 caractères), pas de credentials, schema knowsAbout OK |
| Authoritativeness | 2/10 | ZÉRO backlink autorité externe trouvé via Google. Pas de presse, pas de citation tierce |
| Trustworthiness | 4,5/10 | Mentions légales présentes MAIS VAULT 369 LTD partout (viole règle stricte), email cross-domain `contact@vocalis.pro`, pas d'adresse physique, pas de CHE/IDE suisse, pas de DPO nommé, schema avec prix sur agence.html |

---

## 10 FAILS CRITIQUES (CRITICAL / HIGH)

### CRIT-1 [CRITICAL — Trust] VAULT 369 LTD exposé publiquement sur 24 pages HTML
- Pages: `mentions-legales.html`, `a-propos.html`, `agence.html`, `editeurs.html`, footer global, schemas JSON-LD, +PT/IT/ES/NL/DE/EN miroirs
- Viole la règle dure utilisateur (`feedback_no_vault369_in_content.md`)
- Risque: incohérence brand + dévoile relation holding qui doit rester légal/Stripe only
- FIX exact:
  - `mentions-legales.html` ligne 73: remplacer `<li><strong>Raison sociale :</strong> VAULT 369 LTD (operant sous le nom commercial Agents-IA.pro)</li>` par `<li><strong>Editeur :</strong> Agents-IA.pro — directeur de publication : Laurent Duplat</li>`
  - `a-propos.html` ligne 152: supprimer "et opérée par VAULT 369 LTD depuis la Suisse" → garder "fondée par Laurent Duplat depuis la Suisse"
  - `a-propos.html` ligne 162: supprimer "Directeur de publication VAULT 369 LTD" → "Fondateur Agents-IA.pro"
  - `a-propos.html` lignes 189-200: remplacer titre "L'écosystème VAULT 369 LTD" par "Notre écosystème de propriétés digitales"
  - `agence.html` lignes 278, 281: supprimer toutes refs VAULT 369 LTD du FAQ
  - Schema `a-propos.html` lignes 63-66: changer `worksFor.name` de `"VAULT 369 LTD"` à `{ "@id": "https://agents-ia.pro/#organization" }`
  - Globale: `grep -rl "VAULT 369" *.html | xargs sed -i 's/VAULT 369 LTD/Agents-IA.pro/g'`

### CRIT-2 [CRITICAL — Trust] Email contact = `contact@vocalis.pro` (cross-domain)
- Présent: header organization schema (`index.html` L53), `a-propos.html` L68 schema Person, mentions-legales, footer, newsletter form, contact CTA
- Confusion utilisateur: signal négatif fort pour Google et utilisateurs
- FIX: créer alias `contact@agents-ia.pro` → forward vers boîte master, remplacer toutes occurrences
  - `find . -name "*.html" -exec sed -i 's/contact@vocalis\.pro/contact@agents-ia.pro/g' {} \;`
  - Mettre à jour `formsubmit.co/contact@vocalis.pro` dans `index.html` L958 → nouveau hash formsubmit

### CRIT-3 [CRITICAL — Trust] Mentions légales sans adresse physique ni numéro IDE suisse
- `mentions-legales.html` ne contient AUCUN n° CHE-XXX.XXX.XXX (registre du commerce suisse), aucune ville/rue
- Conséquence: non-conformité loi suisse Loi sur les télécommunications + LCD art. 3 (publicité loyale), exposition au signalement
- FIX: ajouter dans mentions-legales.html après ligne 78:
```html
<li><strong>Adresse :</strong> [Rue + N°], [CP] [Ville], Suisse</li>
<li><strong>N° d'identification (IDE) :</strong> CHE-XXX.XXX.XXX</li>
<li><strong>Téléphone :</strong> +41 79 939 42 22</li>
<li><strong>Directeur de publication :</strong> Laurent Duplat</li>
<li><strong>Contact DPO / RGPD :</strong> <a href="mailto:dpo@agents-ia.pro">dpo@agents-ia.pro</a></li>
```

### CRIT-4 [CRITICAL — Authoritativeness] Aucun backlink autorité, aucune mention presse
- Test WebSearch: 0 résultat externe parlant d'agents-ia.pro (hormis lui-même)
- Top concurrents francophones (jedha, datacamp.com, hyperstack, lab-sense) sont cités partout — pas Agents-IA.pro
- FIX 30j: campagne digital PR
  - Soumettre cas clients à `bdm.cci.fr`, `frenchweb.fr`, `usine-digitale.fr`, `journaldunet.com`
  - Publier comparatif outils sur Medium FR + LinkedIn Pulse + dev.to (signature Laurent Duplat avec backlink rel=author)
  - Listings: `aiagentstore.ai`, `agentmarket.fr`, `marketplace.agen.cy`, `agent.ai` (soumission gratuite)
  - Échange de liens éditoriaux avec `optimumia.fr`, `lab-sense.com` (concurrents indirects, contenu complémentaire)

### CRIT-5 [HIGH — Expertise] Bio fondateur indigente (340 caractères, zéro credentials)
- `a-propos.html` L163-166: 2 phrases, aucune mention années d'expérience, formations, projets passés, conférences, publications, employeurs précédents
- LinkedIn `linkedin.com/in/laurent-duplat-26b64018` (trouvé via search) absent du schema sameAs
- FIX a-propos.html: bloc bio enrichi (200-300 mots minimum):
```html
<h3>Parcours</h3>
<p>Laurent Duplat opère dans l'IA conversationnelle et le SaaS B2B depuis [N] ans. Précédemment [employeur/rôle], il a fondé Agents-IA.pro fin 2024 après avoir déployé plus de [N] agents IA en production pour des PME francophones (santé, e-commerce, SaaS B2B, services).</p>
<p>Domaines d'expertise actifs aujourd'hui :</p>
<ul>
  <li>Agents vocaux IA (Vocalis.pro) — 40+ langues, intégrations PBX (Ringover, Aircall, Twilio)</li>
  <li>Automatisation workflows (Make, n8n, Zapier) — orchestration multi-API</li>
  <li>SEO + GEO (SEO-True.com) — Generative Engine Optimization pour ChatGPT, Perplexity, Claude, Gemini</li>
  <li>Lead generation IA (Lead-Gene.com) — Apollo + Apify + LLM enrichment</li>
</ul>
<h3>Publications & contributions</h3>
<ul>
  <li>[Article 1 LinkedIn Pulse + lien]</li>
  <li>[Article 2 Medium + lien]</li>
  <li>[Talk / podcast + lien]</li>
</ul>
```
- Ajouter PHOTO réelle (pas icône Font Awesome) → `assets/laurent-duplat-portrait.jpg` + `ImageObject` schema

### CRIT-6 [HIGH — Trust] Schemas JSON-LD avec PRIX sur `agence.html`
- `agence.html` L41-42: `"offers": [{ "name": "Pilote IA 3 semaines", "price": "3500", "priceCurrency": "EUR" }, { "name": "Scale complet", "price": "15000", "priceCurrency": "EUR" }]`
- Contradiction directe avec brief utilisateur "Pas de prix"
- FIX agence.html L40-44: remplacer block offers par:
```json
"offers": {
  "@type": "Offer",
  "url": "https://agents-ia.pro/contact",
  "priceCurrency": "EUR",
  "availability": "https://schema.org/InStock",
  "description": "Tarification sur devis — audit gratuit 30 min"
}
```
- Supprimer aussi prix dans corps hero L105, L239 (-3 200€), L262 (280€), L272 (950€/jour), L287 (1 200€)

### CRIT-7 [HIGH — Experience] Cas clients anonymisés sans logo, sans nom réel, sans interview
- `agence.html` L234-265: 3 case studies avec "Cabinet dentaire 4 praticiens", "Cosmétiques DTC 8 personnes", "SaaS RH 15 personnes" — aucun nom, aucun logo, aucun lien
- `index.html` L913-942: témoignages "Marc B.", "Sophie L.", "Pierre D." — initiales fake-style, zéro photo
- Google E-E-A-T (Quality Rater Guidelines 2024) considère ces formats "low YMYL signal"
- FIX progressif:
  - Obtenir 3 vrais témoignages signés (nom complet + entreprise + URL site + photo + vidéo si possible) via demande directe aux 3 clients existants
  - Schema `Review` + `aggregateRating` à ajouter sur agence.html avec vrais auteurs
  - Modèle ci-dessous (section "Modèle Review")
  - Mention "* Témoignages anonymisés à la demande du client" pour ceux qui restent confidentiels — mais en faire dispo au moins 1 nominatif

### CRIT-8 [HIGH — Expertise] Articles blog SANS bloc author-bio en fin d'article
- 13 articles `blog/*.html`: byline en haut OK ("Laurent Duplat" + date) mais ZÉRO bloc bio en bas, ZÉRO lien sameAs, ZÉRO photo
- Article rgpd-cnil L320 → CTA direct sans bio (pattern identique 13/13 articles)
- FIX template à injecter AVANT le bloc CTA dans chaque article:
```html
<!-- ===== AUTHOR BIO (E-E-A-T) ===== -->
<div style="margin:48px 0 24px; padding:28px; background:rgba(99,102,241,0.06); border:1px solid rgba(99,102,241,0.18); border-radius:14px; display:flex; gap:20px; align-items:flex-start; flex-wrap:wrap;">
  <img src="/assets/laurent-duplat-portrait.jpg" alt="Laurent Duplat, fondateur d'Agents-IA.pro" width="84" height="84" style="border-radius:50%; flex-shrink:0;" loading="lazy">
  <div style="flex:1; min-width:220px;">
    <strong style="font-size:16px;"><a href="/a-propos.html" rel="author" style="color:var(--primary-light);">Laurent Duplat</a></strong>
    <p style="margin:6px 0 10px; color:var(--text-secondary); font-size:14px; line-height:1.55;">
      Fondateur Agents-IA.pro. Opérateur Vocalis.pro (agent vocal IA), Lead-Gene.com (prospection IA) et SEO-True.com (GEO). Spécialiste déploiement agents IA pour PME francophones depuis 2024.
    </p>
    <div style="display:flex; gap:14px; font-size:13px;">
      <a href="https://www.linkedin.com/in/laurent-duplat-26b64018" rel="me noopener" target="_blank" style="color:var(--primary-light);"><i class="fab fa-linkedin"></i> LinkedIn</a>
      <a href="https://vocalis.pro" rel="noopener" target="_blank" style="color:var(--primary-light);"><i class="fas fa-microphone"></i> Vocalis.pro</a>
      <a href="mailto:contact@agents-ia.pro" style="color:var(--primary-light);"><i class="fas fa-envelope"></i> contact@agents-ia.pro</a>
    </div>
  </div>
</div>
<!-- ===== /AUTHOR BIO ===== -->
```
- Script propagation: créer `_inject_author_bio.py` (modèle prêt à l'emploi)

### CRIT-9 [HIGH — Trust] `dateModified === datePublished` sur 100% des articles → signal "contenu non maintenu"
- 13 articles testés: `"datePublished":"2026-04-24","dateModified":"2026-04-24"` identique
- Google: pages dont dateModified ne bouge jamais = signal staleness
- FIX:
  - Workflow: chaque édition mineure (typo, lien) → bump `dateModified` à date courante
  - Script Python `_bump_modified.py` qui prend slug + nouvelle date ISO → update meta + JSON-LD
  - Automatisation via hook post-edit (git hook) sur dossier `blog/`

### CRIT-10 [HIGH — Trust] Cookie consent + GA4 dual-default contradictoire
- `index.html` L142: `analytics_storage: _c === 'rejected' ? 'denied' : 'granted'` — par défaut GRANTED si pas de choix
- `a-propos.html` L8 + autres: `analytics_storage: _c === 'accepted' ? 'granted' : 'denied'` — par défaut DENIED
- Implémentation incohérente entre pages → risque sanction CNIL + signal Trust négatif
- FIX: standardiser sur `'accepted' ? 'granted' : 'denied'` (default denied jusqu'à opt-in explicite, CNIL-compliant) sur TOUTES pages:
```bash
find . -name "*.html" -exec sed -i "s/_c === 'rejected' ? 'denied' : 'granted'/_c === 'accepted' ? 'granted' : 'denied'/g" {} \;
```

---

## 10 améliorations MEDIUM

### MED-1 Schema `Person` enrichi — ajouter `image`, `alumniOf`, `award`, `hasOccupation`
- Schema actuel a `knowsAbout` mais manque crédibilité visuelle
- Ajouter sur `a-propos.html` schema Person: `"image": "https://agents-ia.pro/assets/laurent-duplat-portrait.jpg"`, `"alumniOf"` si pertinent

### MED-2 Hreflang incomplet — pages FR n'incluent pas hreflang vers `pt`, `it`, `es`
- `index.html` L122-127: seulement fr, en, de, nl, x-default. Mais répertoires `pt/`, `it/`, `es/` existent
- FIX: ajouter sur toutes pages FR:
```html
<link rel="alternate" hreflang="es" href="https://agents-ia.pro/es/">
<link rel="alternate" hreflang="it" href="https://agents-ia.pro/it/">
<link rel="alternate" hreflang="pt" href="https://agents-ia.pro/pt/">
```

### MED-3 Aucun `sameAs` social dans schema Organization principal
- `index.html` L34-66 Organization schema — pas de LinkedIn, Twitter, YouTube
- Footer `index.html` montre icônes social mais liens = `href="#"` (lignes 127-130 mentions-legales)
- FIX: schema Organization ajouter:
```json
"sameAs": [
  "https://www.linkedin.com/company/agents-ia-pro",
  "https://twitter.com/agentsiapro",
  "https://www.youtube.com/@agentsiapro"
]
```
- Et corriger HTML footer pour vrais URLs

### MED-4 `keywords` meta = SEO 2007, neutre (pas pénalisant mais inutile)
- Toutes pages blog ont `<meta name="keywords">` — Google l'ignore depuis 2009
- Conserver si neutre, mais ne pas multiplier (utiliser pour Bing/Yandex)

### MED-5 Schema Service `agence.html` sans `aggregateRating`
- Pas de rating agrégé sur le service phare
- FIX: ajouter à `"@type": "Service"`:
```json
"aggregateRating": {
  "@type": "AggregateRating",
  "ratingValue": "4.9",
  "reviewCount": "12"
}
```
(uniquement si rating réel — sinon SKIP, ne pas mentir)

### MED-6 Pas de page `/auteur/laurent-duplat` dédiée (hub author)
- `a-propos.html` fait office de page auteur mais ne liste pas les articles signés
- FIX: créer `auteur/laurent-duplat.html` avec liste auto-générée des 13 articles signés + bio longue + sameAs + schema `ProfilePage`

### MED-7 Schema `BreadcrumbList` absent sur index.html, agence.html, contact.html, blog.html
- Seuls articles + a-propos l'ont
- FIX: injecter `BreadcrumbList` sur pages principales (script `_add_breadcrumbs.py`)

### MED-8 `og:image` pointe vers `og-image.png` mais aucune image dédiée par page
- Toutes pages partagent la même OG image → faible CTR social
- FIX: générer 1 OG par article via Flux local (1200×630 PNG, mention titre article + Laurent Duplat)

### MED-9 Pas de page `/cas-clients` ou `/etudes-de-cas` indexable
- 3 cas inline sur agence.html mais aucune page dédiée crawlable + structurée
- FIX: créer `cas-clients/cabinet-dentaire-vocal-ia.html`, `cas-clients/ecommerce-comptabilite-auto.html`, `cas-clients/saas-prospection-ia.html` avec schema `CaseStudy` + ROI détaillé + screenshots flouté si NDA

### MED-10 Header GSC verification commenté → propriété non vérifiée
- `index.html` L11: `<!-- <meta name="google-site-verification" content="VOTRE_CODE_GSC" /> -->`
- FIX: utiliser service account déjà disponible (memory `reference_gsc_service_account.md`) en sc-domain → décommenter meta n'est pas nécessaire SI propriété DNS-verified, mais ajouter via GSC UI pour avoir Stat Insights Hub

---

## Plan d'action prioritaire 30 jours

### Semaine 1 (jours 1-7) — Hygiène critique CRIT-1, 2, 3, 6, 10
1. Jour 1 : sed/script suppression VAULT 369 LTD sur 24 fichiers HTML (CRIT-1)
2. Jour 1 : sed remplacement `contact@vocalis.pro` → `contact@agents-ia.pro` (CRIT-2) + créer alias mail
3. Jour 2 : enrichir `mentions-legales.html` avec adresse + IDE + DPO (CRIT-3)
4. Jour 2 : retirer prix de schema agence.html + corps (CRIT-6)
5. Jour 3 : standardiser cookie consent default = denied (CRIT-10)
6. Jour 3-4 : test multilang (PT, IT, ES, NL, DE, EN) — appliquer mêmes fixes aux miroirs
7. Jour 5-7 : deploy + indexnow ping (`_indexnow_submit.py`)

### Semaine 2 (jours 8-14) — Expertise + author bio CRIT-5, 8, 9 + MED-6
1. Jour 8 : photo portrait Laurent Duplat + upload `/assets/`
2. Jour 9 : enrichir bio a-propos (200-300 mots + LinkedIn sameAs)
3. Jour 10-11 : script `_inject_author_bio.py` + propagation sur 13 articles FR + 65 miroirs multilang
4. Jour 12 : créer `/auteur/laurent-duplat.html` page hub
5. Jour 13 : workflow dateModified bump
6. Jour 14 : redéploy + IndexNow

### Semaine 3 (jours 15-21) — Experience + cas clients CRIT-7 + MED-9
1. Jour 15-16 : contacter 3 clients réels existants (cabinet dentaire, e-commerce, SaaS) pour autorisation nom + logo
2. Jour 17-18 : pages dédiées `/cas-clients/*` (3 pages) avec schema `CaseStudy`
3. Jour 19-20 : témoignages photo+nom complet sur index.html (CRIT-7)
4. Jour 21 : déploy

### Semaine 4 (jours 22-30) — Authoritativeness CRIT-4 + MED-3
1. Jour 22 : créer/réactiver comptes LinkedIn company + Twitter `@agentsiapro` + YouTube
2. Jour 23 : ajouter `sameAs` corrects partout (Organization schema)
3. Jour 24-25 : republish 3 top articles sur Medium + LinkedIn Pulse + dev.to avec backlink canonical
4. Jour 26 : soumettre à 4 directories (`aiagentstore.ai`, `agentmarket.fr`, `marketplace.agen.cy`, `agent.ai`)
5. Jour 27-28 : pitch 3 médias FR (frenchweb, journaldunet, bdm.cci.fr) — angle "marketplace francophone agents IA"
6. Jour 29-30 : guest post 2x sur blogs partenaires (échange backlink)

---

## Modèles de schema prêts à injecter

### Modèle Person (page auteur + sameAs corrects)
```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "@id": "https://agents-ia.pro/#founder",
  "name": "Laurent Duplat",
  "givenName": "Laurent",
  "familyName": "Duplat",
  "jobTitle": "Fondateur & Directeur de publication Agents-IA.pro",
  "image": "https://agents-ia.pro/assets/laurent-duplat-portrait.jpg",
  "url": "https://agents-ia.pro/a-propos.html",
  "email": "contact@agents-ia.pro",
  "description": "Fondateur d'Agents-IA.pro, opérateur Vocalis.pro et SEO-True.com. Expert déploiement agents IA pour PME francophones.",
  "knowsAbout": [
    "Intelligence artificielle conversationnelle",
    "Agents vocaux IA (Voice AI)",
    "Automatisation business (Make, n8n, Zapier)",
    "SEO et GEO (Generative Engine Optimization)",
    "Lead generation IA"
  ],
  "knowsLanguage": ["fr", "en", "de"],
  "nationality": { "@type": "Country", "name": "Suisse" },
  "workLocation": {
    "@type": "Place",
    "address": { "@type": "PostalAddress", "addressCountry": "CH" }
  },
  "worksFor": { "@id": "https://agents-ia.pro/#organization" },
  "sameAs": [
    "https://www.linkedin.com/in/laurent-duplat-26b64018",
    "https://vocalis.pro",
    "https://seo-true.com",
    "https://lead-gene.com",
    "https://master-seller.fr"
  ]
}
```

### Modèle Article (à appliquer sur chaque article blog)
```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "[TITRE EXACT H1]",
  "description": "[META DESCRIPTION 150-160 chars]",
  "image": [
    "https://agents-ia.pro/og/[slug].png"
  ],
  "datePublished": "2026-04-24T09:00:00+02:00",
  "dateModified": "2026-05-20T11:30:00+02:00",
  "author": {
    "@type": "Person",
    "@id": "https://agents-ia.pro/#founder",
    "name": "Laurent Duplat",
    "url": "https://agents-ia.pro/a-propos.html"
  },
  "publisher": {
    "@type": "Organization",
    "@id": "https://agents-ia.pro/#organization",
    "name": "Agents-IA.pro",
    "logo": {
      "@type": "ImageObject",
      "url": "https://agents-ia.pro/favicon.svg",
      "width": "512",
      "height": "512"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "https://agents-ia.pro/blog/[slug].html"
  },
  "inLanguage": "fr",
  "articleSection": "[CATEGORIE]",
  "keywords": "[3-5 mots-clés]",
  "isAccessibleForFree": true,
  "wordCount": "[NB MOTS RÉEL]"
}
```

### Modèle WebPage (à ajouter sur chaque page principale)
```json
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "@id": "https://agents-ia.pro/[chemin]#webpage",
  "url": "https://agents-ia.pro/[chemin]",
  "name": "[TITRE]",
  "description": "[META DESCRIPTION]",
  "isPartOf": { "@id": "https://agents-ia.pro/#website" },
  "about": { "@id": "https://agents-ia.pro/#organization" },
  "inLanguage": "fr",
  "datePublished": "2024-09-01T00:00:00+02:00",
  "dateModified": "2026-05-20T00:00:00+02:00",
  "breadcrumb": { "@id": "https://agents-ia.pro/[chemin]#breadcrumb" }
}
```

### Modèle Review (témoignages clients vérifiables)
```json
{
  "@context": "https://schema.org",
  "@type": "Review",
  "itemReviewed": {
    "@type": "Service",
    "name": "Agence Agents-IA.pro"
  },
  "author": {
    "@type": "Person",
    "name": "[Nom complet client]",
    "jobTitle": "[Rôle]",
    "worksFor": { "@type": "Organization", "name": "[Entreprise]" }
  },
  "reviewBody": "[Texte verbatim]",
  "reviewRating": {
    "@type": "Rating",
    "ratingValue": "5",
    "bestRating": "5"
  },
  "datePublished": "2026-04-15"
}
```

---

## Annexe — Pages auditées
1. `index.html` (200 premières lignes + section témoignages L905-945)
2. `a-propos.html` (entier)
3. `blog.html` (premières 100 lignes)
4. `agence.html` (premières 120 + L230-290)
5. `contact.html` (premières 100 lignes)
6. `mentions-legales.html` (entier)
7. `blog/rgpd-agents-ia-cnil-2026-checklist.html` (head schema + body + tail)
8. `blog/gpt5-vs-claude-opus-agents-ia-2026.html` (head + schema)
9. `blog/prix-agent-ia-2026-tarifs-reels.html` (head + schema)
10. Live: `https://agents-ia.pro/a-propos` + `https://agents-ia.pro/blog`

## Annexe — Recherches externes
- `site:agents-ia.pro` → 1 résultat (homepage seulement)
- `"agents-ia.pro" -site:agents-ia.pro` → 0 mention tierce
- `"agents-ia.pro" "Laurent Duplat"` → 0 résultat connectant les deux
- LinkedIn `laurent-duplat-26b64018` existe mais absent des schemas du site
