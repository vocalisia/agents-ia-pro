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
