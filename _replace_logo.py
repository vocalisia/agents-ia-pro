#!/usr/bin/env python3
"""Replace emoji/fa-robot logo with professional SVG logo across all pages.
Logo is inlined as a compact SVG mark (just the hexagonal A) next to the text wordmark.
"""
import re
from pathlib import Path

ROOT = Path(__file__).parent

# Inline SVG MARK ONLY (logo text "agents-ia.pro" kept as original text wordmark)
SVG_MARK = '''<svg viewBox="0 0 40 40" xmlns="http://www.w3.org/2000/svg" style="width:32px;height:32px;vertical-align:middle;"><defs><linearGradient id="lg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6366f1"/><stop offset="0.5" stop-color="#8b5cf6"/><stop offset="1" stop-color="#ec4899"/></linearGradient></defs><path d="M20 3 L35 12 L35 28 L20 37 L5 28 L5 12 Z" fill="rgba(139,92,246,0.15)" stroke="url(#lg1)" stroke-width="1.8"/><path d="M12 28 L20 12 L28 28 M15.5 22 L24.5 22" stroke="url(#lg1)" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" fill="none"/><circle cx="20" cy="12" r="2.2" fill="url(#lg1)"/><circle cx="12" cy="28" r="1.6" fill="#ec4899"/><circle cx="28" cy="28" r="1.6" fill="#6366f1"/></svg>'''


# Patterns to replace
PATTERNS = [
    # Original: <span class="logo-icon"><i class="fas fa-robot"></i></span>
    (re.compile(r'<span class="logo-icon"><i class="fas fa-robot"></i></span>'),
     f'<span class="logo-icon">{SVG_MARK}</span>'),
    # With 🤖 emoji
    (re.compile(r'<span class="logo-icon">🤖</span>'),
     f'<span class="logo-icon">{SVG_MARK}</span>'),
    # Minified variants with different quote/spacing
    (re.compile(r'<span class="logo-icon">🤖\s*</span>'),
     f'<span class="logo-icon">{SVG_MARK}</span>'),
]

# Ensure the logo-icon style doesn't shrink/clip the SVG
STYLE_PATCH = """
<style id="brand-logo-patch">
.nav-logo { text-decoration: none; display: inline-flex; align-items: center; gap: 10px; }
.nav-logo .logo-icon { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; }
.nav-logo .logo-icon svg { width: 32px; height: 32px; }
.footer-brand .logo-icon { display: inline-flex; align-items: center; justify-content: center; width: 36px; height: 36px; }
.footer-brand .logo-icon svg { width: 32px; height: 32px; }
.logo-text { font-weight: 800; letter-spacing: -0.3px; font-size: 18px; }
.logo-accent { background: linear-gradient(90deg, #6366f1, #ec4899); -webkit-background-clip: text; background-clip: text; color: transparent; }
</style>
"""


def process(path: Path):
    try:
        content = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return False

    original = content
    changed = False

    for pat, repl in PATTERNS:
        new = pat.sub(repl, content)
        if new != content:
            content = new
            changed = True

    # Inject the style patch in <head> if not already done
    if "brand-logo-patch" not in content and changed:
        content = re.sub(r'(</head>)', STYLE_PATCH + r'\1', content, count=1)

    if changed and content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def main():
    files = []
    files.extend(ROOT.glob("*.html"))
    for sub in ["en", "de", "nl", "es", "it", "pt"]:
        d = ROOT / sub
        if d.exists():
            files.extend(d.glob("*.html"))
            sub_blog = d / "blog"
            if sub_blog.exists():
                files.extend(sub_blog.glob("*.html"))
    if (ROOT / "blog").exists():
        files.extend((ROOT / "blog").glob("*.html"))

    updated = 0
    for f in files:
        if process(f):
            updated += 1
    print(f"{updated}/{len(files)} files updated")


if __name__ == "__main__":
    main()
