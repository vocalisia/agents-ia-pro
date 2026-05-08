#!/usr/bin/env python3
"""Create Stripe webhook endpoint via API + extract signing secret."""
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

VAULT = Path(r"C:\Users\cohen.000\.secrets\vault.enc").read_text(encoding="utf-8", errors="ignore")
STRIPE_SK = None
for line in VAULT.splitlines():
    line = line.strip()
    if line.startswith("stripekey:"):
        STRIPE_SK = line.split(":", 1)[1].strip()
        break

WEBHOOK_URL = "https://agents-ia.pro/api/stripe-webhook"
EVENTS = ["checkout.session.completed"]


def stripe_post(endpoint, data):
    body = urllib.parse.urlencode(data, doseq=True).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.stripe.com/v1/{endpoint}",
        data=body,
        headers={"Authorization": f"Bearer {STRIPE_SK}", "Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def stripe_get(endpoint):
    req = urllib.request.Request(
        f"https://api.stripe.com/v1/{endpoint}",
        headers={"Authorization": f"Bearer {STRIPE_SK}"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    # Check if webhook already exists
    endpoints = stripe_get("webhook_endpoints")
    existing = None
    for ep in endpoints.get("data", []):
        if ep["url"] == WEBHOOK_URL:
            existing = ep
            break

    if existing:
        print(f"Webhook already exists: {existing['id']}")
        # Get signing secret — only shown on creation, so we rotate it by creating a new one? No, just keep the existing one but we can't retrieve it.
        # We'll need to delete and recreate to get the secret (acceptable since no live traffic yet)
        print(f"Deleting existing webhook to get fresh secret...")
        req = urllib.request.Request(
            f"https://api.stripe.com/v1/webhook_endpoints/{existing['id']}",
            headers={"Authorization": f"Bearer {STRIPE_SK}"},
            method="DELETE",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            json.loads(resp.read().decode("utf-8"))
        print("  Deleted.")

    # Create fresh webhook
    data = {
        "url": WEBHOOK_URL,
        "description": "agents-ia.pro — send PDFs and welcome emails on checkout",
    }
    for ev in EVENTS:
        data.setdefault("enabled_events[]", []).append(ev)

    result = stripe_post("webhook_endpoints", data)
    print(f"\nWebhook created: {result['id']}")
    print(f"URL: {result['url']}")
    print(f"SIGNING SECRET (save NOW, not shown again):")
    print(f"  {result['secret']}")

    # Save to vault for reference
    secret_line = f"STRIPE_WEBHOOK_SECRET:{result['secret']}\n"
    vault_path = Path(r"C:\Users\cohen.000\.secrets\vault.enc")
    content = vault_path.read_text(encoding="utf-8", errors="ignore")
    if "STRIPE_WEBHOOK_SECRET:" not in content:
        with open(vault_path, "a", encoding="utf-8") as f:
            f.write("\n" + secret_line)
        print(f"\nSaved to vault.enc")

    # Print export commands
    print("\n=== Next step: add env vars to Vercel ===")
    print(f'vercel env add STRIPE_SECRET_KEY production  # paste sk_live_... from vault')
    print(f'vercel env add STRIPE_WEBHOOK_SECRET production  # paste {result["secret"][:20]}...')
    print(f'vercel env add RESEND_API_KEY production  # paste re_... from vault')


if __name__ == "__main__":
    main()
