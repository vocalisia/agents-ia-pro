#!/usr/bin/env python3
"""
Tâche 1: Ajoute hreflang es/it/pt sur toutes les pages racine qui ont déjà des hreflang.
Idempotent: skip si déjà présent.
"""

import re
import glob
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

NEW_HREFLANG = [
    '    <link rel="alternate" hreflang="es" href="https://agents-ia.pro/es/">',
    '    <link rel="alternate" hreflang="it" href="https://agents-ia.pro/it/">',
    '    <link rel="alternate" hreflang="pt" href="https://agents-ia.pro/pt/">',
]

DETECT_PATTERN = re.compile(r'<link\s+rel="alternate"\s+hreflang=')
# Trouve le dernier hreflang de la séquence
LAST_HREFLANG_PATTERN = re.compile(
    r'(<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>)',
    re.IGNORECASE
)

def already_has_new_langs(content: str) -> bool:
    return (
        'hreflang="es"' in content and
        'hreflang="it"' in content and
        'hreflang="pt"' in content
    )

def process_file(filepath: str) -> str:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if not DETECT_PATTERN.search(content):
        return 'skip-no-hreflang'

    if already_has_new_langs(content):
        return 'skip-already-present'

    # Trouve toutes les occurrences de hreflang
    matches = list(LAST_HREFLANG_PATTERN.finditer(content))
    if not matches:
        return 'skip-no-match'

    last_match = matches[-1]
    insert_pos = last_match.end()

    injection = '\n' + '\n'.join(NEW_HREFLANG)
    new_content = content[:insert_pos] + injection + content[insert_pos:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return 'updated'

def main():
    html_files = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    results = {'updated': [], 'skip-no-hreflang': [], 'skip-already-present': [], 'skip-no-match': []}

    for filepath in html_files:
        filename = os.path.basename(filepath)
        status = process_file(filepath)
        results[status].append(filename)
        print(f'[{status}] {filename}')

    print('\n=== RÉSUMÉ ===')
    print(f"Updated:              {len(results['updated'])} fichiers")
    if results['updated']:
        for f in results['updated']:
            print(f"  - {f}")
    print(f"Skip (no hreflang):   {len(results['skip-no-hreflang'])} fichiers")
    print(f"Skip (already done):  {len(results['skip-already-present'])} fichiers")
    print(f"Skip (no match):      {len(results['skip-no-match'])} fichiers")

if __name__ == '__main__':
    main()
