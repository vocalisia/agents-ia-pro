"""
Create Stripe CHF payment links for agents-ia.pro
Mirrors the EUR products in CHF for Swiss visitors (CH/LI).
"""
import stripe
import json
import os

from pathlib import Path as _Path
_vault = _Path(r"C:\Users\cohen.000\.secrets\vault.enc")
stripe.api_key = None
for _line in _vault.read_text(encoding="utf-8", errors="ignore").splitlines():
    _line = _line.strip()
    if _line.startswith("stripekey:"):
        stripe.api_key = _line.split(":", 1)[1].strip()
        break
if not stripe.api_key:
    raise RuntimeError("stripekey not found in vault")

REDIRECT_URL = "https://agents-ia.pro/merci.html"
METADATA_SITE = "agents-ia.pro"

PRODUCTS = [
    {
        "key": "bronze",
        "name": "Featured Listing Bronze CHF",
        "amount": 9900,   # CHF 99.00
        "currency": "chf",
        "recurring": {"interval": "month"},
        "metadata": {"product": "bronze_chf"},
    },
    {
        "key": "silver",
        "name": "Featured Listing Silver CHF",
        "amount": 29900,  # CHF 299.00
        "currency": "chf",
        "recurring": {"interval": "month"},
        "metadata": {"product": "silver_chf"},
    },
    {
        "key": "gold",
        "name": "Featured Listing Gold CHF",
        "amount": 79900,  # CHF 799.00
        "currency": "chf",
        "recurring": {"interval": "month"},
        "metadata": {"product": "gold_chf"},
    },
    {
        "key": "submit_fasttrack",
        "name": "Submit Fast-Track CHF",
        "amount": 14900,  # CHF 149.00
        "currency": "chf",
        "recurring": None,
        "metadata": {"product": "submit_fasttrack_chf"},
    },
    {
        "key": "rapport_assurance",
        "name": "Rapport Assurance IA CHF",
        "amount": 49900,  # CHF 499.00
        "currency": "chf",
        "recurring": None,
        "metadata": {"product": "rapport_assurance_chf"},
    },
    {
        "key": "rapport_voice",
        "name": "Rapport Voice AI Benchmark CHF",
        "amount": 29900,  # CHF 299.00
        "currency": "chf",
        "recurring": None,
        "metadata": {"product": "rapport_voice_chf"},
    },
    {
        "key": "rapport_rgpd",
        "name": "Rapport RGPD + AI Act CHF",
        "amount": 19900,  # CHF 199.00
        "currency": "chf",
        "recurring": None,
        "metadata": {"product": "rapport_rgpd_chf"},
    },
    {
        "key": "rapport_bundle",
        "name": "Rapport Bundle 5 rapports CHF",
        "amount": 69700,  # CHF 697.00
        "currency": "chf",
        "recurring": None,
        "metadata": {"product": "rapport_bundle_chf"},
    },
]

results = {}

for p in PRODUCTS:
    print(f"\n--- Creating: {p['name']} ---")

    # 1. Create Product
    product = stripe.Product.create(
        name=p["name"],
        metadata={"currency": p["currency"], "site": METADATA_SITE},
    )
    print(f"  Product ID: {product.id}")

    # 2. Create Price
    price_params = {
        "product": product.id,
        "unit_amount": p["amount"],
        "currency": p["currency"],
    }
    if p["recurring"]:
        price_params["recurring"] = p["recurring"]

    price = stripe.Price.create(**price_params)
    print(f"  Price ID: {price.id}")

    # 3. Create Payment Link
    link = stripe.PaymentLink.create(
        line_items=[{"price": price.id, "quantity": 1}],
        after_completion={
            "type": "redirect",
            "redirect": {"url": REDIRECT_URL},
        },
        metadata={"product": p["key"] + "_chf", "site": METADATA_SITE},
    )
    print(f"  Payment Link: {link.url}")
    results[p["key"]] = link.url

print("\n\n=== ALL CHF PAYMENT LINKS ===")
for k, v in results.items():
    print(f"{k}: {v}")

# Save to JSON
out_path = os.path.join(os.path.dirname(__file__), "stripe-payment-links-chf.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\nSaved to: {out_path}")
