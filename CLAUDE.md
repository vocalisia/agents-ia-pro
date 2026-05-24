# Agents-IA.pro

## Rôle
Site agence agents IA — agents-ia.pro.

## Stack
- HTML statique + scripts Python pour génération/publication
- Vercel (Standard, JAMAIS Turbo)

## Scripts clés
- `_generate_articles.py` — génération articles
- `_translate_blog.py` — traduction multilang
- `_inject_affiliate_block.py` — blocs monétisation
- `_indexnow_submit.py` — soumission IndexNow
- `_generate_rapports_pdf.py` — rapports PDF
- `publish.mjs` / `_update_sitemap_new_langs.py` — mise à jour sitemap

## Règles
- JAMAIS OpenAI direct → Mammouth API
- JAMAIS push Vercel sans test localhost HTTP 200 réel
- JAMAIS VAULT 369 LTD dans contenu public

## GA4 CONSENT — VERROUILLÉ (HARD RULE, zéro tolérance)

`src/app/layout.tsx` bloc GA4 = **INTOUCHABLE**. Pattern exact obligatoire :

```js
var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;
gtag('consent', 'default', { analytics_storage: _c === 'rejected' ? 'denied' : 'granted', ... });
```

- OPT-OUT uniquement : `rejected → denied`, tout le reste → `granted`
- INTERDICTION de changer `'granted'` en `'denied'` comme valeur par défaut
- INTERDICTION d'ajouter `if (_c === 'accepted')` ou toute logique opt-in
- INTERDICTION de toucher ce bloc sans confirmation explicite de l'utilisateur

Violation = rollback immédiat. Ce bug a causé 0 connexions GA4 pendant 1 semaine (2026-05-16 → 2026-05-23).
