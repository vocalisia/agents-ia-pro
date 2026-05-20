"""Second pass after _fix_vault369.py: remove redundant Agents-IA.pro duplicates
created by the replace.

Patterns to fix:
  "d'Agents-IA.pro et de Agents-IA.pro"      -> "d'Agents-IA.pro"
  "Agents-IA.pro et Agents-IA.pro"            -> "Agents-IA.pro"
  "directeur de publication Agents-IA.pro"    -> "directeur de publication"
  "operant sous le nom commercial Agents-IA.pro" -> "" (irrelevant outside legal)
  "L'ecosysteme Agents-IA.pro" + "Agents-IA.pro opère" duplicates -> dedupe sentences

Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
LEGAL_KEEP = {"cgu.html", "confidentialite.html", "mentions-legales.html"}
SKIP_DIRS = {"node_modules", ".next", ".vercel", ".git"}

PATTERNS = [
    # "fondateur d'Agents-IA.pro et de Agents-IA.pro" -> "fondateur d'Agents-IA.pro"
    (re.compile(r"d'Agents-IA\.pro et de Agents-IA\.pro"), "d'Agents-IA.pro"),
    (re.compile(r"d'Agents-IA\.pro, Vocalis\.pro et directeur de publication Agents-IA\.pro"),
     "d'Agents-IA.pro et Vocalis.pro"),
    (re.compile(r"Fondateur d'Agents-IA\.pro et directeur de publication Agents-IA\.pro"),
     "Fondateur d'Agents-IA.pro"),
    (re.compile(r"Fondateur · Directeur de publication Agents-IA\.pro"),
     "Fondateur · Agents-IA.pro"),
    # Spanish/Italian/Portuguese mirrors of the same patterns
    (re.compile(r"de Agents-IA\.pro y de Agents-IA\.pro"), "de Agents-IA.pro"),
    (re.compile(r"di Agents-IA\.pro e di Agents-IA\.pro"), "di Agents-IA.pro"),
    (re.compile(r"da Agents-IA\.pro e da Agents-IA\.pro"), "da Agents-IA.pro"),
    # Section heading + paragraph duplicate
    (re.compile(r"L'écosystème Agents-IA\.pro"), "L'écosystème"),
    (re.compile(r"Agents-IA\.pro opère une constellation"),
     "Notre écosystème opère une constellation"),
    # Generic safety net: collapse triple+ "Agents-IA.pro Agents-IA.pro"
    (re.compile(r"(Agents-IA\.pro)(\s+\1){1,}"), r"\1"),
]

modified = []
for path in ROOT.rglob("*.html"):
    if any(part in SKIP_DIRS for part in path.parts):
        continue
    if path.name in LEGAL_KEEP:
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        continue
    original = text
    for pattern, repl in PATTERNS:
        text = pattern.sub(repl, text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        modified.append(str(path.relative_to(ROOT)))

print(f"Dedup pass — modified: {len(modified)}")
for m in modified:
    print(f"  M {m}")
