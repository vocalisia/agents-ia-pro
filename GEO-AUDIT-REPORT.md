# GEO Audit Report: Agents-IA.pro

**Audit Date:** 25 mars 2026
**URL:** https://agents-ia-pro.vercel.app
**Business Type:** Marketplace / Agency (SaaS hybrid)
**Pages Analyzed:** 20

---

## Executive Summary

**Overall GEO Score: 40/100 (Poor)**

Agents-IA.pro a une base technique solide (HTML statique, tous crawlers IA autorises, bonne structure de contenu) mais souffre de lacunes critiques en structured data (0 schema), presence de marque quasi-inexistante, et contenu date. Le site est pratiquement invisible pour les moteurs de recherche IA.

### Score Breakdown

| Categorie | Score | Poids | Score Pondere |
|-----------|-------|-------|---------------|
| AI Citability | 52/100 | 25% | 13.0 |
| Brand Authority | 8/100 | 20% | 1.6 |
| Content E-E-A-T | 52/100 | 20% | 10.4 |
| Technical GEO | 74/100 | 15% | 11.1 |
| Schema & Structured Data | 5/100 | 10% | 0.5 |
| Platform Optimization | 34/100 | 10% | 3.4 |
| **GEO Score Global** | | | **40/100** |

---

## Issues Critiques (Fix Immediat)

1. **Zero structured data** - Aucun JSON-LD, Microdata ou RDFa sur aucune page. Les moteurs IA ne peuvent pas comprendre la semantique du contenu.
   - **Fix:** Ajouter Organization + WebSite sur homepage, Service + FAQPage sur pages agents, Article sur blog posts.
   - **Status:** PARTIELLEMENT CORRIGE (homepage + agent-commercial)

2. **Compteurs affichent "0"** - Les stats hero (0 Agents, 0 Users, 0% Satisfaits) signalent une plateforme vide aux crawlers IA.
   - **Fix:** Afficher les vraies valeurs dans le HTML source.
   - **Status:** CORRIGE

3. **Placeholders partout** - GA4 `G-XXXXXXXXXX`, Meta Pixel `XXXXXXXXXX`, WhatsApp `41XXXXXXXXX`, email `votre@email.com`. Signale un site template non-fini.
   - **Fix:** Remplacer par les vrais identifiants.
   - **Status:** EN ATTENTE (besoin des vrais IDs)

4. **Pages legales inexistantes** - Mentions legales, CGU, Politique de confidentialite = liens `#` morts. Ironie pour un site publiant des guides RGPD.
   - **Fix:** Creer les vraies pages legales avec nom societe, adresse, CHE, etc.

5. **Aucune presence de marque externe** - 0 mentions Reddit, 0 YouTube, 0 LinkedIn, 0 Wikipedia, 0 Wikidata. La marque est invisible pour les modeles IA.
   - **Fix:** Creer profils LinkedIn, YouTube, Product Hunt, Trustpilot, Wikidata.

---

## Issues Haute Priorite

6. **Pas de llms.txt** - Fichier standard pour guider les IA sur le contenu du site.
   - **Status:** CORRIGE

7. **ClaudeBot mal nomme dans robots.txt** - `Claude-Web` au lieu de `ClaudeBot`.
   - **Status:** CORRIGE

8. **Pas d'auteurs nommes sur les articles** - "Redaction Agents-IA.pro" = zero signal d'expertise.
   - **Fix:** Ajouter de vrais auteurs avec bios, credentials, liens LinkedIn.

9. **Zero citations externes** - Aucun article ne cite de source externe (EUR-Lex, CNIL, Gartner...).
   - **Fix:** Ajouter 3-5 citations par article.

10. **Claims ROI non sourcees** - "+520% ROI", "+340% ROI", "+800% ROI" sans methodologie.
    - **Fix:** Ajouter sample size, periode, lien vers case study.

11. **Canonical tags manquants** - Pages agents n'ont pas de canonical (sauf agent-commercial).
    - **Fix:** Ajouter `<link rel="canonical">` a toutes les pages.

12. **OG/Twitter tags absents sur pages internes** - Seule la homepage a les meta OG.
    - **Fix:** Ajouter og:title, og:description, og:image a chaque page.

---

## Issues Moyenne Priorite

13. **Contenu date "2025"** - Titres et copyright referent 2025, on est en 2026.
14. **Security headers manquants** - CSP, X-Frame-Options, X-Content-Type-Options absents.
    - **Status:** CORRIGE via vercel.json
15. **Pas de preconnect** pour fonts/CDN externes.
    - **Status:** CORRIGE
16. **Testimonials non-verifiables** - "Marc B.", "Sophie L." = pattern de faux avis.
17. **Extensions .html visibles** dans les URLs.
    - **Status:** CORRIGE via vercel.json cleanUrls
18. **Pas de hreflang** - Site FR en Suisse multilingue.
19. **Bing Webmaster Tools non configure** - Pas d'IndexNow.

---

## Issues Basse Priorite

20. **Pas de version anglaise** - Limite la visibilite IA a 5-8% des requetes mondiales.
21. **Liens sociaux footer = `#`** - LinkedIn, Twitter, YouTube, Instagram non connectes.
22. **Pas de screenshots produit** - Marketplace sans images des agents.
23. **Pas de contenu video** - YouTube vide.

---

## Quick Wins Implementes

| Fix | Impact | Status |
|-----|--------|--------|
| llms.txt cree | +7-10 pts | FAIT |
| robots.txt corrige (ClaudeBot + 8 crawlers) | +5 pts | FAIT |
| Compteurs HTML pre-remplis (pas 0) | +10-15 pts citability | FAIT |
| vercel.json security headers | +5 pts technique | FAIT |
| vercel.json cleanUrls | +2 pts URL | FAIT |
| Preconnect fonts/CDN | +3 pts performance | FAIT |
| Schema Organization + WebSite (homepage) | +10 pts schema | FAIT |
| Schema Service + FAQ (agent-commercial) | +5 pts schema | FAIT |

**Score estime apres fixes : ~55-60/100** (vs 40 avant)

---

## Plan d'Action 30 Jours

### Semaine 1 : Fondations
- [ ] Remplacer TOUS les placeholders (GA4, Pixel, WhatsApp, email)
- [ ] Creer les pages legales (mentions, CGU, confidentialite)
- [ ] Ajouter canonical + OG tags a toutes les pages agents
- [ ] Ajouter Schema Service a tous les 9 agents restants
- [ ] Ajouter Schema Article a tous les 6 articles blog
- [ ] Creer page LinkedIn entreprise complete

### Semaine 2 : Contenu
- [ ] Ajouter auteurs nommes avec bios sur tous les articles
- [ ] Ajouter 3-5 citations externes par article
- [ ] Mettre a jour dates "2025" -> "2026"
- [ ] Creer 3 nouveaux case studies (industries differentes)
- [ ] Sourcer toutes les claims ROI avec methodologie

### Semaine 3 : Presence Externe
- [ ] Creer chaine YouTube + 3 videos demos
- [ ] Creer profil Trustpilot + solliciter avis
- [ ] Soumettre sur Product Hunt
- [ ] Poster contenu valeur sur Reddit (r/artificial, r/SaaS)
- [ ] Creer entree Wikidata

### Semaine 4 : Optimisation
- [ ] Configurer Google Search Console
- [ ] Configurer Bing Webmaster Tools + IndexNow
- [ ] Creer Google Business Profile
- [ ] Ajouter hreflang tags
- [ ] Publier rapport "Etat du marche agents IA francophones"
- [ ] Re-audit GEO pour mesurer progression

---

## Score Cible a 30 Jours : 70-75/100
