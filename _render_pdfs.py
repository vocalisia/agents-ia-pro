#!/usr/bin/env python3
"""Convert the 3 rapport HTML files to PDF using Playwright (Chromium headless)."""
import sys
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).parent
PDF_DIR = ROOT / "rapports-pdf"

RAPPORTS = [
    "rapport-assurance-ia-france-2026",
    "rapport-benchmark-50-voice-ai-2026",
    "rapport-rgpd-ai-act-pme-2026",
]


def render():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context()
        for slug in RAPPORTS:
            src = PDF_DIR / f"{slug}.html"
            dst = PDF_DIR / f"{slug}.pdf"
            if not src.exists():
                print(f"SKIP {slug} (no HTML)")
                continue
            print(f"Rendering {slug}...")
            page = context.new_page()
            page.goto(f"file:///{src.as_posix()}")
            page.wait_for_load_state("networkidle")
            page.pdf(
                path=str(dst),
                format="A4",
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
                print_background=True,
            )
            page.close()
            print(f"  OK {dst} ({dst.stat().st_size // 1024} KB)")
        browser.close()


if __name__ == "__main__":
    render()
