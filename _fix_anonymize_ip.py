#!/usr/bin/env python3
import re
from pathlib import Path

BASE = Path(__file__).parent
count = 0

for ext in ['*.html', '*.tsx', '*.ts', '*.js']:
    for f in BASE.rglob(ext):
        if '.next' in str(f) or 'node_modules' in str(f):
            continue
        content = f.read_text(encoding='utf-8', errors='ignore')
        # Pattern: gtag('config', 'G-B5627RD3TF', { anonymize_ip: true });
        new = re.sub(
            r"gtag\('config',\s*'G-B5627RD3TF',\s*\{\s*anonymize_ip:\s*true\s*\}\)",
            "gtag('config', 'G-B5627RD3TF')",
            content
        )
        # Template literal version in layout.tsx: ${GA_ID}', { anonymize_ip: true })
        new = re.sub(
            r"gtag\('config',\s*'\$\{GA_ID\}',\s*\{\s*anonymize_ip:\s*true\s*\}\)",
            "gtag('config', '${GA_ID}')",
            new
        )
        if new != content:
            f.write_text(new, encoding='utf-8', errors='ignore')
            count += 1
            print(f'Fixed: {f.relative_to(BASE)}')

print(f'Total: {count} files fixed')
