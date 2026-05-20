#!/usr/bin/env python3
"""
Tâche 3: Déduplique les titres "Automatisez votre secteur" sur 7 pages.
Chaque page reçoit un title + meta description uniques.
Idempotent: skip si le title cible est déjà présent.
"""

import re
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Dict: fichier -> {title, description}
PAGES = {
    'agent-assurance.html': {
        'title': 'Agent IA Assurance | Automatisez votre assurance | Agents-IA.pro',
        'description': "Agent IA spécialisé assurance : gestion des sinistres, devis automatiques, suivi client 24/7. Réduisez votre coût de traitement de 60% et boostez la satisfaction assurés.",
    },
    'agent-ecommerce.html': {
        'title': 'Agent IA E-Commerce | Automatisez vos ventes en ligne | Agents-IA.pro',
        'description': "Agent IA e-commerce : service client automatique, relances abandon de panier, recommandations personnalisées. Boostez vos conversions de 40% sans effort supplémentaire.",
    },
    'agent-formation.html': {
        'title': 'Agent IA Formation | Automatisez votre centre de formation | Agents-IA.pro',
        'description': "Agent IA pour centres de formation : création de contenu, suivi des apprenants, coaching IA personnalisé. Multipliez votre chiffre d'affaires par 3 sans ressources supplémentaires.",
    },
    'agent-immobilier.html': {
        'title': 'Agent IA Immobilier | Automatisez votre agence immobilière | Agents-IA.pro',
        'description': "Agent IA immobilier : qualification automatique, planification des visites, gestion des dossiers. Vendez 3× plus vite et réduisez le temps de traitement de chaque prospect.",
    },
    'agent-logistique.html': {
        'title': 'Agent IA Logistique | Automatisez votre chaîne logistique | Agents-IA.pro',
        'description': "Agent IA logistique & transport : planification d'itinéraires, gestion des stocks, suivi des livraisons en temps réel. Réduisez vos coûts de transport de 30%.",
    },
    'agent-recouvrement.html': {
        'title': 'Agent IA Recouvrement | Automatisez votre recouvrement de créances | Agents-IA.pro',
        'description': "Agent IA recouvrement de créances : relances automatiques multi-canaux, négociation IA, suivi en temps réel. Récupérez jusqu'à 85% de vos créances impayées.",
    },
    'agent-restauration.html': {
        'title': 'Agent IA Restauration | Automatisez votre restaurant | Agents-IA.pro',
        'description': "Agent IA restauration & hôtellerie : réservations en ligne, commandes click & collect, gestion des avis clients. Augmentez vos couverts de 30% et fidélisez votre clientèle.",
    },
}


def update_title(html: str, new_title: str) -> tuple[str, bool]:
    """Remplace le <title> existant. Retourne (html, changed)."""
    pattern = re.compile(r'<title>.*?</title>', re.DOTALL)
    new_tag = f'<title>{new_title}</title>'
    new_html, count = pattern.subn(new_tag, html, count=1)
    return new_html, count > 0


def update_description(html: str, new_desc: str) -> tuple[str, bool]:
    """Remplace meta description existante. Retourne (html, changed)."""
    pattern = re.compile(
        r'<meta\s+name=["\']description["\']\s+content=["\'][^"\']*["\']\s*/?>',
        re.IGNORECASE
    )
    new_tag = f'<meta name="description" content="{new_desc}">'
    new_html, count = pattern.subn(new_tag, html, count=1)
    return new_html, count > 0


def process_file(filepath: str, config: dict) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    target_title = config['title']
    target_desc = config['description']

    # Idempotent: vérifie si title cible déjà présent
    if f'<title>{target_title}</title>' in html:
        return 'skip-already-updated'

    html, title_changed = update_title(html, target_title)
    html, desc_changed = update_description(html, target_desc)

    if not title_changed and not desc_changed:
        return 'skip-no-tags-found'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    parts = []
    if title_changed:
        parts.append('title')
    if desc_changed:
        parts.append('description')
    return f'updated ({", ".join(parts)})'


def main():
    results = {}

    for filename, config in PAGES.items():
        filepath = os.path.join(ROOT, filename)
        if not os.path.exists(filepath):
            status = 'skip-file-not-found'
        else:
            status = process_file(filepath, config)

        results[filename] = status
        print(f'[{status}] {filename}')
        if status.startswith('updated'):
            print(f'  title -> {config["title"]}')
            print(f'  desc  -> {config["description"][:80]}...')

    print('\n=== RÉSUMÉ ===')
    updated = [k for k, v in results.items() if v.startswith('updated')]
    skipped = [k for k, v in results.items() if v.startswith('skip')]
    print(f'Updated: {len(updated)}/7 fichiers -> {updated}')
    print(f'Skipped: {len(skipped)} -> {skipped}')


if __name__ == '__main__':
    main()
