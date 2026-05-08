#!/usr/bin/env python3
"""Create 9 Stripe Payment Links via API + auto-replace placeholders in HTML files.

Uses sk_live_* key from vault.enc. CREATES REAL LIVE PAYMENT LINKS.

Products:
- 3 recurring subscriptions: Bronze 99€/mo, Silver 299€/mo, Gold 799€/mo
- 6 one-shot: Submit 149€, Rapport Assurance 499€, Rapport Voice 299€,
  Rapport RGPD 199€, Bundle 697€
"""
import os
import sys
import re
import json
import urllib.request
import urllib.error
import urllib.parse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Load Stripe secret key from vault
VAULT_PATH = Path(r"C:\Users\cohen.000\.secrets\vault.enc")
STRIPE_SK = None
for line in VAULT_PATH.read_text(encoding="utf-8", errors="ignore").splitlines():
    line = line.strip()
    if line.startswith("stripekey:"):
        STRIPE_SK = line.split(":", 1)[1].strip()
        break
if not STRIPE_SK:
    print("FAIL: stripekey not found in vault")
    sys.exit(1)

STRIPE_API = "https://api.stripe.com/v1"
ROOT = Path(__file__).parent

PRODUCTS = [
    # slug -> (name, description, price_eur, recurring, placeholder)
    ("bronze", "Agents-IA.pro · Featured Listing Bronze",
     "Fiche agent dans la catégorie dédiée, badge Partenaire Vérifié, lien dofollow, statistiques mensuelles.",
     99, "month", "AGENTS-IA-BRONZE-LINK"),
    ("silver", "Agents-IA.pro · Featured Listing Silver",
     "Top 3 catégorie, badge Featured, article review 1500 mots, 1 post newsletter, support prioritaire.",
     299, "month", "AGENTS-IA-SILVER-LINK"),
    ("gold", "Agents-IA.pro · Featured Listing Gold",
     "Top 1 permanent, bannière homepage 1 sem/mois, case study 3000 mots, 2 newsletters, account manager dédié.",
     799, "month", "AGENTS-IA-GOLD-LINK"),
    ("submit_fasttrack", "Agents-IA.pro · Submit Fast-Track",
     "Review prioritaire sous 48h, publication sous 5 jours ouvrés, review SEO incluse.",
     149, None, "SUBMIT-FASTTRACK-LINK"),
    ("rapport_assurance", "Rapport · État de l'IA dans l'assurance France 2026",
     "Benchmark 120 assureurs, 15 agents vocaux testés, conformité ACPR/CNIL, roadmap 90j. PDF 87 pages.",
     499, None, "RAPPORT-ASSURANCE-LINK"),
    ("rapport_voice", "Rapport · Benchmark 50 agents vocaux IA 2026 Q2",
     "Comparatif 50 agents vocaux, 30 scénarios testés, scorecards détaillées. PDF 64 pages.",
     299, None, "RAPPORT-VOICE-LINK"),
    ("rapport_rgpd", "Rapport · RGPD & AI Act : conformité PME 2026",
     "Checklist CNIL 47 points, templates DPIA, guide AI Act. PDF 52 pages + 3 templates.",
     199, None, "RAPPORT-RGPD-LINK"),
    ("rapport_bundle", "Rapport · Bundle 3 rapports (Assurance + Voice + RGPD)",
     "Les 3 rapports complets : assurance (87p), benchmark voice (64p), RGPD (52p). -30% vs unitaire.",
     697, None, "RAPPORT-BUNDLE-LINK"),
]


def stripe_post(endpoint, data):
    body = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
    req = urllib.request.Request(
        f"{STRIPE_API}/{endpoint}",
        data=body,
        headers={
            "Authorization": f"Bearer {STRIPE_SK}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        print(f"  HTTP {e.code}: {err_body[:400]}")
        raise


def create_payment_link(slug, name, description, price_eur, recurring_interval):
    print(f"\n=== {slug} ({price_eur}€{'/' + recurring_interval if recurring_interval else ' one-shot'}) ===")

    # 1) Create Product
    product = stripe_post("products", {
        "name": name,
        "description": description,
        "metadata[slug]": slug,
        "metadata[source]": "agents-ia.pro",
    })
    product_id = product["id"]
    print(f"  Product created: {product_id}")

    # 2) Create Price
    price_data = {
        "product": product_id,
        "unit_amount": price_eur * 100,
        "currency": "eur",
        "metadata[slug]": slug,
    }
    if recurring_interval:
        price_data["recurring[interval]"] = recurring_interval
    price = stripe_post("prices", price_data)
    price_id = price["id"]
    print(f"  Price created: {price_id}")

    # 3) Create Payment Link
    payment_link_data = {
        "line_items[0][price]": price_id,
        "line_items[0][quantity]": 1,
        "allow_promotion_codes": "true",
        "billing_address_collection": "required",
        "metadata[slug]": slug,
        "metadata[source]": "agents-ia.pro",
        "after_completion[type]": "redirect",
        "after_completion[redirect][url]": f"https://agents-ia.pro/merci.html?product={slug}",
    }
    # Add phone number collection for agency/submit leads
    if slug in ("silver", "gold", "submit_fasttrack"):
        payment_link_data["phone_number_collection[enabled]"] = "true"
    pl = stripe_post("payment_links", payment_link_data)
    url = pl["url"]
    print(f"  Payment Link: {url}")
    return url


def replace_placeholder(placeholder, real_url):
    """Replace placeholder URL in all HTML files (FR + EN + DE + NL)."""
    files = []
    files.extend(ROOT.glob("*.html"))
    for sub in ["en", "de", "nl"]:
        d = ROOT / sub
        if d.exists():
            files.extend(d.glob("*.html"))
    # Blog articles too (affiliate CTAs might contain similar)
    for sub in ["blog", "en/blog", "de/blog", "nl/blog"]:
        d = ROOT / sub
        if d.exists():
            files.extend(d.glob("*.html"))

    count = 0
    placeholder_url = f"https://buy.stripe.com/{placeholder}"
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if placeholder_url in content:
                new = content.replace(placeholder_url, real_url)
                f.write_text(new, encoding="utf-8")
                count += 1
        except Exception:
            pass
    return count


def main():
    results = {}
    errors = []

    for slug, name, desc, price, recurring, placeholder in PRODUCTS:
        try:
            url = create_payment_link(slug, name, desc, price, recurring)
            results[slug] = (url, placeholder)
        except Exception as e:
            print(f"  FAIL {slug}: {e}")
            errors.append(slug)

    # Save mapping
    mapping_file = ROOT / "stripe-payment-links.json"
    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump({k: v[0] for k, v in results.items()}, f, indent=2)
    print(f"\nMapping saved: {mapping_file}")

    # Replace placeholders in HTML files
    print("\n=== Replacing placeholders in HTML files ===")
    for slug, (url, placeholder) in results.items():
        count = replace_placeholder(placeholder, url)
        print(f"  {placeholder} → {count} files updated")

    print("\n=== SUMMARY ===")
    for slug, (url, _) in results.items():
        print(f"{slug:25} {url}")
    if errors:
        print(f"\nErrors: {errors}")


if __name__ == "__main__":
    main()
