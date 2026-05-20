"""Remove VAULT 369 LTD mentions from SEO/marketing/content HTML.

KEEP legal pages (cgu, confidentialite, mentions-legales) — legally required.
Replace everywhere else: VAULT 369 LTD -> Agents-IA.pro

Idempotent. Safe to re-run.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
LEGAL_KEEP = {"cgu.html", "confidentialite.html", "mentions-legales.html"}

# Order matters: longest match first
REPLACEMENTS = [
    (re.compile(r"VAULT\s*369\s*LTD", re.IGNORECASE), "Agents-IA.pro"),
    (re.compile(r"VAULT\s*369", re.IGNORECASE), "Agents-IA.pro"),
]

# Skip dirs
SKIP_DIRS = {"node_modules", ".next", ".vercel", ".git"}

modified = []
skipped_legal = []
skipped_nomatch = []
errors = []

for path in ROOT.rglob("*.html"):
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    if path.name in LEGAL_KEEP:
        skipped_legal.append(str(path.relative_to(ROOT)))
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        errors.append(f"{path}: {e}")
        continue
    original = text
    for pattern, repl in REPLACEMENTS:
        text = pattern.sub(repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        modified.append(str(path.relative_to(ROOT)))
    else:
        skipped_nomatch.append(str(path.relative_to(ROOT)))

print(f"Modified: {len(modified)}")
for m in modified:
    print(f"  M {m}")
print(f"\nSkipped (legal pages, kept VAULT 369): {len(skipped_legal)}")
for s in skipped_legal:
    print(f"  L {s}")
print(f"\nNo match (already clean or never had): {len(skipped_nomatch)} files")
print(f"Errors: {len(errors)}")
for e in errors:
    print(f"  E {e}")
