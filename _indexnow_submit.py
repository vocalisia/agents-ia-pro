#!/usr/bin/env python3
"""Submit updated URLs to IndexNow (Bing, Yandex, etc.)."""
import json
import urllib.request
import urllib.error

INDEXNOW_ENDPOINTS = [
    "https://api.indexnow.org/indexnow",
    "https://www.bing.com/indexnow",
]

SUBMISSIONS = [
    {
        "host": "agents-ia.pro",
        "key": "254340f57d7a8f6d3a5a432252d0b44a",
        "keyLocation": "https://agents-ia.pro/254340f57d7a8f6d3a5a432252d0b44a.txt",
        "urls": [
            "https://agents-ia.pro/",
            "https://agents-ia.pro/a-propos.html",
            "https://agents-ia.pro/editeurs.html",
            "https://agents-ia.pro/newsletter.html",
            "https://agents-ia.pro/rapports.html",
            "https://agents-ia.pro/submit.html",
            "https://agents-ia.pro/blog.html",
            "https://agents-ia.pro/blog/gpt5-vs-claude-opus-agents-ia-2026.html",
            "https://agents-ia.pro/blog/prix-agent-ia-2026-tarifs-reels.html",
            "https://agents-ia.pro/blog/agent-ia-vocal-assurance-cas-usage.html",
            "https://agents-ia.pro/blog/agents-ia-whatsapp-business-guide-2026.html",
            "https://agents-ia.pro/blog/rgpd-agents-ia-cnil-2026-checklist.html",
            "https://agents-ia.pro/en/",
            "https://agents-ia.pro/en/editeurs.html",
            "https://agents-ia.pro/en/newsletter.html",
            "https://agents-ia.pro/en/rapports.html",
            "https://agents-ia.pro/de/",
            "https://agents-ia.pro/de/editeurs.html",
            "https://agents-ia.pro/de/newsletter.html",
            "https://agents-ia.pro/de/rapports.html",
            "https://agents-ia.pro/nl/",
            "https://agents-ia.pro/nl/editeurs.html",
            "https://agents-ia.pro/nl/newsletter.html",
            "https://agents-ia.pro/nl/rapports.html",
            "https://agents-ia.pro/sitemap.xml",
        ],
    },
    {
        "host": "vocalis.pro",
        "key": "5a6c5d8cb912b355d48513c662891634",
        "keyLocation": "https://vocalis.pro/5a6c5d8cb912b355d48513c662891634.txt",
        "urls": [
            "https://vocalis.pro/",
            "https://vocalis.pro/sitemap.xml",
            "https://vocalis.pro/blog/",
            "https://vocalis.pro/en/",
            "https://vocalis.pro/de/",
            "https://vocalis.pro/es/",
            "https://vocalis.pro/nl/",
            "https://vocalis.pro/it/",
        ],
    },
]


def submit(endpoint, payload):
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Mozilla/5.0 indexnow-submitter/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read().decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "ignore")[:400]
    except Exception as e:
        return 0, str(e)


def main():
    for sub in SUBMISSIONS:
        print(f"\n=== {sub['host']} ({len(sub['urls'])} urls) ===")
        payload = {
            "host": sub["host"],
            "key": sub["key"],
            "keyLocation": sub["keyLocation"],
            "urlList": sub["urls"],
        }
        for endpoint in INDEXNOW_ENDPOINTS:
            code, body = submit(endpoint, payload)
            label = "OK" if 200 <= code < 300 else ("WARN" if code == 202 else "FAIL")
            print(f"  {label} [{code}] {endpoint}")
            if body and code not in (200, 202):
                print(f"    body: {body[:200]}")


if __name__ == "__main__":
    main()
