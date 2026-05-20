#!/usr/bin/env python3
"""
Tâche 2: Ajoute FAQPage schema JSON-LD sur les pages cibles.
Extrait FAQ depuis le HTML (section <!-- FAQ --> ou h3+cat-count features).
Idempotent: skip si FAQPage déjà présent.
"""

import re
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

TARGET_PAGES = [
    'agent-commercial.html',
    'agent-support.html',
    'agent-chatbot.html',
    'agent-marketing.html',
    'agence.html',
    'categories.html',
    'blog.html',
]

# Fallback FAQ par page si pas de contenu FAQ extractable
FALLBACK_FAQ = {
    'agent-support.html': [
        {
            'name': "Comment l'agent de support IA répond-il aux tickets clients ?",
            'answer': "L'agent résout 80% des tickets en moins de 3 secondes grâce à sa base de connaissances IA entraînée sur vos documents, historique et procédures internes."
        },
        {
            'name': "Quels canaux de support l'agent IA prend-il en charge ?",
            'answer': "Chat widget, email, téléphone, WhatsApp et Messenger — tous centralisés dans un seul tableau de bord avec historique unifié."
        },
        {
            'name': "L'agent de support IA peut-il gérer plusieurs langues ?",
            'answer': "Oui, l'agent détecte et répond dans la langue du client : FR, EN, DE, IT, ES et plus de 20 langues supplémentaires."
        },
        {
            'name': "Que se passe-t-il pour les tickets complexes que l'IA ne peut pas résoudre ?",
            'answer': "L'agent transfère automatiquement les cas complexes au bon agent humain avec tout le contexte et l'historique de la conversation."
        },
    ],
    'agent-chatbot.html': [
        {
            'name': "Comment installer un chatbot IA sur mon site web ?",
            'answer': "L'installation prend moins de 5 minutes : copiez un simple snippet JavaScript sur votre site WordPress, Shopify ou site custom. Aucune compétence technique requise."
        },
        {
            'name': "Le chatbot IA peut-il prendre des rendez-vous automatiquement ?",
            'answer': "Oui, le chatbot s'intègre avec Calendly, Cal.com et Google Calendar pour permettre aux visiteurs de réserver directement dans votre agenda depuis la conversation."
        },
        {
            'name': "Comment le chatbot qualifie-t-il les leads ?",
            'answer': "Le chatbot pose les bonnes questions de qualification et score automatiquement chaque visiteur selon vos critères, puis envoie les leads qualifiés à votre CRM."
        },
        {
            'name': "Le chatbot IA supporte-t-il plusieurs langues ?",
            'answer': "Oui, le chatbot détecte automatiquement la langue du visiteur et répond dans sa langue pour maximiser le taux de conversion."
        },
    ],
    'agent-marketing.html': [
        {
            'name': "Comment un agent IA peut-il automatiser le marketing de mon entreprise ?",
            'answer': "L'agent IA gère votre calendrier éditorial, rédige vos posts et captions optimisés pour chaque plateforme, répond aux commentaires et DMs avec votre ton de marque."
        },
        {
            'name': "L'agent marketing IA peut-il créer du contenu sur plusieurs plateformes ?",
            'answer': "Oui, l'agent génère du contenu adapté pour LinkedIn, Instagram, Facebook, Twitter/X et TikTok avec les bons hashtags et formats spécifiques à chaque réseau."
        },
        {
            'name': "Combien de temps faut-il pour mettre en place un agent marketing IA ?",
            'answer': "La configuration initiale prend 24 à 48 heures. L'agent apprend votre ton de marque, vos produits et votre audience pour produire du contenu pertinent dès le départ."
        },
        {
            'name': "Comment mesurer le ROI d'un agent marketing IA ?",
            'answer': "L'agent fournit un tableau de bord avec les KPIs clés : engagement, portée, taux de conversion, leads générés — pour mesurer précisément le retour sur investissement."
        },
    ],
    'categories.html': None,  # skip - pas de contenu FAQ
    'blog.html': None,  # skip - pas de contenu FAQ
}


def clean_html(text: str) -> str:
    """Supprime les balises HTML et normalise les espaces."""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&amp;', '&', text)
    text = re.sub(r'&lt;', '<', text)
    text = re.sub(r'&gt;', '>', text)
    text = re.sub(r'&nbsp;', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def extract_explicit_faq(html: str) -> list:
    """Extrait Q+A depuis une section <!-- FAQ --> ou <h2>FAQ</h2>."""
    # Cherche <!-- FAQ -->
    idx = html.find('<!-- FAQ')
    if idx == -1:
        # Cherche h2 contenant "FAQ"
        h2_matches = list(re.finditer(r'<h2[^>]*>(.*?)</h2>', html, re.DOTALL))
        for m in h2_matches:
            if 'faq' in m.group(1).lower():
                idx = m.start()
                break

    if idx == -1:
        return []

    section = html[idx:idx + 5000]

    # Cherche paires h3 + p dans la section
    pairs = re.findall(
        r'<h3[^>]*>(.*?)</h3>\s*(?:<[^>]+>\s*)*<p[^>]*>(.*?)</p>',
        section,
        re.DOTALL
    )

    results = []
    for q_html, a_html in pairs[:5]:
        q = clean_html(q_html)
        a = clean_html(a_html)
        if len(q) > 10 and len(a) > 10:
            results.append({'name': q, 'answer': a})

    return results


def build_faqpage_schema(faq_items: list) -> str:
    """Génère le bloc script JSON-LD FAQPage."""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item['name'],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item['answer']
                }
            }
            for item in faq_items
        ]
    }
    json_str = json.dumps(schema, ensure_ascii=False, indent=2)
    return f'<script type="application/ld+json">\n{json_str}\n</script>'


def process_file(filepath: str, filename: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Idempotent check
    if 'FAQPage' in html:
        return 'skip-already-present'

    # Extrait FAQ
    faq_items = extract_explicit_faq(html)

    # Fallback si pas de FAQ explicite
    if not faq_items:
        fallback = FALLBACK_FAQ.get(filename)
        if fallback is None:
            return 'skip-no-faq-found'
        if fallback:
            faq_items = fallback

    if not faq_items:
        return 'skip-no-faq-found'

    # Génère et insère le schema avant </head>
    schema_block = build_faqpage_schema(faq_items)
    if '</head>' not in html:
        return 'skip-no-head-tag'

    new_html = html.replace('</head>', f'{schema_block}\n</head>', 1)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    return f'updated ({len(faq_items)} questions)'


def main():
    results = {}

    for filename in TARGET_PAGES:
        filepath = os.path.join(ROOT, filename)
        if not os.path.exists(filepath):
            status = 'skip-file-not-found'
        else:
            status = process_file(filepath, filename)

        results[filename] = status
        print(f'[{status}] {filename}')

    # Cherche aussi agent-vocal*.html
    import glob
    vocal_files = glob.glob(os.path.join(ROOT, 'agent-vocal*.html'))
    for filepath in vocal_files:
        filename = os.path.basename(filepath)
        status = process_file(filepath, filename)
        results[filename] = status
        print(f'[{status}] {filename}')

    print('\n=== RÉSUMÉ ===')
    updated = [k for k, v in results.items() if v.startswith('updated')]
    skipped = [k for k, v in results.items() if v.startswith('skip')]
    print(f'Updated: {len(updated)} -> {updated}')
    print(f'Skipped: {len(skipped)}')
    for k in skipped:
        print(f'  {k}: {results[k]}')


if __name__ == '__main__':
    main()
