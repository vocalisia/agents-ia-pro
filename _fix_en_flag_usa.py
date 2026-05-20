"""Replace UK/Union-Jack CSS flag with USA flag on EN language option.
Applies to all HTML files that contain the lang selector.
Idempotent.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent
SKIP_DIRS = {"node_modules", ".next", ".vercel", ".git", "rapports-pdf"}

# The UK flag pattern (blue background + diagonal white lines)
UK_FLAG = (
    r'<span style="display:inline-block;width:28px;height:18px;background:#012169;'
    r'border-radius:3px;flex-shrink:0;position:relative;">'
    r'<span style="position:absolute;inset:0;background:linear-gradient'
    r'\(45deg,transparent 45%,#fff 45%,#fff 55%,transparent 55%\),'
    r'linear-gradient\(135deg,transparent 45%,#fff 45%,#fff 55%,transparent 55%\);">'
    r'</span></span>'
)

# USA flag: red/white stripes + blue canton
USA_FLAG = (
    '<span style="display:inline-block;width:28px;height:18px;'
    'background:repeating-linear-gradient(180deg,#B22234 0,#B22234 14.3%,'
    '#fff 14.3%,#fff 28.6%,#B22234 28.6%,#B22234 42.9%,'
    '#fff 42.9%,#fff 57.2%,#B22234 57.2%,#B22234 71.5%,'
    '#fff 71.5%,#fff 85.8%,#B22234 85.8%,#B22234 100%);'
    'border-radius:3px;flex-shrink:0;position:relative;">'
    '<span style="position:absolute;top:0;left:0;width:40%;height:54%;'
    'background:#3C3B6E;border-radius:2px 0 0 0;"></span></span>'
)

modified = []
skipped = []

for path in ROOT.rglob("*.html"):
    if any(p in SKIP_DIRS for p in path.parts):
        continue
    text = path.read_text(encoding="utf-8")
    new_text = re.sub(UK_FLAG, USA_FLAG, text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        modified.append(str(path.relative_to(ROOT)))
    else:
        skipped.append(str(path.relative_to(ROOT)))

print(f"Modified: {len(modified)}")
for m in modified:
    print(f"  M {m}")
print(f"Skipped (no UK flag found): {len(skipped)}")
