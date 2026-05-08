# 💳 Stripe Setup Guide — agents-ia.pro monétisation multi-langue

Guide complet pour activer les 9 Stripe Payment Links avec support multi-devise et multi-langue.

---

## 1. Créer les 9 Payment Links

Connecte-toi sur https://dashboard.stripe.com → **Produits** → **Payment Links** → Create.

### Abonnements récurrents (3 produits)

| Produit | Prix | Billing | URL à coller dans HTML |
|---------|------|---------|------------------------|
| **Featured Listing Bronze** | 99€ | Monthly | remplace `AGENTS-IA-BRONZE-LINK` |
| **Featured Listing Silver** | 299€ | Monthly | remplace `AGENTS-IA-SILVER-LINK` |
| **Featured Listing Gold** | 799€ | Monthly | remplace `AGENTS-IA-GOLD-LINK` |

### One-shot (6 produits)

| Produit | Prix | URL à coller |
|---------|------|--------------|
| **Submit Fast-Track** | 149€ | `SUBMIT-FASTTRACK-LINK` |
| **Rapport Assurance** | 499€ | `RAPPORT-ASSURANCE-LINK` |
| **Rapport Voice AI** | 299€ | `RAPPORT-VOICE-LINK` |
| **Rapport RGPD** | 199€ | `RAPPORT-RGPD-LINK` |
| **Rapport Bundle** | 697€ | `RAPPORT-BUNDLE-LINK` |

---

## 2. Activer les langues sur Stripe Checkout

Dans chaque Payment Link → **Advanced options** → **Customer detection**.

Stripe détecte automatiquement la langue du navigateur du client parmi les 40 langues supportées (fr, en, de, nl inclus).

**Fallback langue** à configurer :
- **Default language** : English (pour les marchés internationaux)
- **Allowed languages** : French, English, German, Dutch

**Options checkout à activer pour ces produits :**

- ✅ Collect phone number (upsell futur)
- ✅ Collect billing address (facturation VAULT 369 LTD)
- ✅ Allow promo codes
- ✅ Enable Link (Stripe Link = 1-click checkout)
- ✅ Apple Pay + Google Pay

---

## 3. Multi-devise (EUR, CHF, USD, GBP)

### Pour les abonnements récurrents (Featured Listing)

Stripe permet **pricing par devise** sur un même Product. Pour chaque plan :

1. Aller dans le Product (ex: "Featured Listing Silver")
2. **Add another price** → Currency : CHF
3. Prix CHF suggéré (au taux du jour) :
   - Bronze : 99€ → **99 CHF**
   - Silver : 299€ → **299 CHF**
   - Gold : 799€ → **799 CHF**
4. Répéter pour USD (ajouter ~10% pour marges) :
   - Bronze : **$119** | Silver : **$349** | Gold : **$949**
5. Répéter pour GBP :
   - Bronze : **£89** | Silver : **£259** | Gold : **£699**

Le Payment Link **sélectionne automatiquement la devise** selon la localisation IP du client.

### Pour les one-shot (Rapports, Submit Fast-track)

Idem : Add another price par devise. Stripe auto-détecte.

---

## 4. Factures multilingues VAULT 369 LTD

**Dans Stripe Dashboard → Settings → Tax & Invoicing :**

- **Business name** : VAULT 369 LTD
- **Address** : (ton adresse Suisse)
- **Email** : contact@vocalis.pro
- **IBAN** : (IBAN VAULT 369 LTD — celui du template TF9QONBY-0022)
- **Tax status** : Franchise art. 293B CGI (pas de TVA française) + exonéré TVA Suisse si applicable

**Invoice template multilingue** :
Settings → Branding → **Upload logo** (utilise `../vocalis-pro-backup/media/downloads/logo-VOCALIS-long.png`).
Settings → Emails → Activer "Customer locale" pour que l'email de confirmation soit dans la langue du client.

**Facture type** : Stripe envoie automatiquement la facture PDF dans la langue du client (fr/en/de/nl).

---

## 5. Webhook pour CRM / automatisation

Configure un webhook Stripe → ton stack d'automatisation (Make.com recommandé) :

**URL webhook** : https://hook.eu1.make.com/XXXXX (à créer dans Make)

**Events à écouter** :
- `checkout.session.completed` (paiement OK)
- `customer.subscription.created` (nouveau Featured Listing)
- `customer.subscription.deleted` (résiliation)
- `payment_intent.succeeded` (paiement one-shot)

**Dans Make scenario** :
1. Trigger : Stripe Webhook
2. Router :
   - Si `metadata.product = featured_listing` → envoyer email de bienvenue éditeur + créer tâche Trello "Onboard new editor"
   - Si `metadata.product = rapport_*` → envoyer le PDF correspondant via email (attachment depuis Google Drive)
   - Si `metadata.product = submit_fasttrack` → notifier équipe ("Review Fast-track in 48h")
3. Toujours : ajouter contact dans CRM (HubSpot free / Airtable) + ajouter à newsletter Beehiiv

---

## 6. PDF des rapports — livraison automatique

**Chaque rapport doit être livré automatiquement après paiement.**

### Option A (recommandée) : Google Drive + Make

1. Uploader les 3 PDFs dans Google Drive (Agents-IA.pro > Reports)
2. Dans Make webhook handler, match `metadata.report = assurance|voice|rgpd|bundle`
3. Attacher le PDF correspondant au email de confirmation via Gmail/Brevo module

### Option B (plus simple) : Stripe post-payment URL

1. Dans chaque Payment Link → **After payment** → Custom URL
2. Rediriger vers une page `agents-ia.pro/download/{report_slug}?session_id={CHECKOUT_SESSION_ID}`
3. Cette page vérifie le `session_id` via Stripe API et sert le PDF

**Le plus rapide** = Option A avec Brevo transactionnel + attachment direct.

---

## 7. Coupons et codes promo

**Actions à créer** :
- `LAUNCH50` : -50% premier mois sur Featured Listing (limite: 20 utilisations)
- `BUNDLE30` : -30% rapports individuels (limite: illimitée, période: 30j)
- `AFFILIATE-XXXX` : codes uniques pour partenaires affiliés

Stripe Dashboard → Coupons → New.

---

## 8. Remplacements automatiques à faire (quick script)

Une fois tu as récupéré tes vrais Stripe Payment Link URLs, remplace-les dans tous les fichiers :

```bash
cd C:/Users/cohen.000/agents-ia-pro

# Remplacer tous les placeholders
sed -i 's|buy.stripe.com/AGENTS-IA-BRONZE-LINK|buy.stripe.com/VRAI-LIEN-BRONZE|g' editeurs.html en/editeurs.html de/editeurs.html nl/editeurs.html
sed -i 's|buy.stripe.com/AGENTS-IA-SILVER-LINK|buy.stripe.com/VRAI-LIEN-SILVER|g' editeurs.html en/editeurs.html de/editeurs.html nl/editeurs.html
sed -i 's|buy.stripe.com/AGENTS-IA-GOLD-LINK|buy.stripe.com/VRAI-LIEN-GOLD|g' editeurs.html en/editeurs.html de/editeurs.html nl/editeurs.html

sed -i 's|buy.stripe.com/SUBMIT-FASTTRACK-LINK|buy.stripe.com/VRAI-LIEN-SUBMIT|g' submit.html

sed -i 's|buy.stripe.com/RAPPORT-ASSURANCE-LINK|buy.stripe.com/VRAI-LIEN-ASSURANCE|g' rapports.html en/rapports.html de/rapports.html nl/rapports.html
sed -i 's|buy.stripe.com/RAPPORT-VOICE-LINK|buy.stripe.com/VRAI-LIEN-VOICE|g' rapports.html en/rapports.html de/rapports.html nl/rapports.html
sed -i 's|buy.stripe.com/RAPPORT-RGPD-LINK|buy.stripe.com/VRAI-LIEN-RGPD|g' rapports.html en/rapports.html de/rapports.html nl/rapports.html
sed -i 's|buy.stripe.com/RAPPORT-BUNDLE-LINK|buy.stripe.com/VRAI-LIEN-BUNDLE|g' rapports.html en/rapports.html de/rapports.html nl/rapports.html

# Deploy
vercel --prod --yes
```

---

## 9. Tests à faire après activation

- [ ] Test paiement Bronze en mode test (carte `4242 4242 4242 4242`)
- [ ] Vérifier email de confirmation reçu dans la bonne langue
- [ ] Vérifier webhook Make reçu et traité
- [ ] Test résiliation (cancel subscription) → email de confirmation
- [ ] Test coupon `LAUNCH50`
- [ ] Test passer depuis `/en/editeurs.html` → checkout doit être en anglais
- [ ] Vérifier facture PDF = VAULT 369 LTD + IBAN correct + pas de TVA
- [ ] Vérifier détection auto devise (VPN CH → CHF, VPN US → USD)

---

## 10. Monitoring revenus

**Dashboard Stripe** : Analytics → Revenue.

**Metrics à tracker hebdomadairement** :
- MRR Featured Listing (Bronze + Silver + Gold)
- Rapports vendus par type
- Taux de conversion page → checkout → paid
- Churn mensuel (résiliations)
- Source traffic (via UTM parameters sur les Payment Links)

**UTM à ajouter sur chaque Payment Link** :
```
?utm_source=agents-ia.pro&utm_medium=editeurs_page&utm_campaign=silver_launch
```

---

*Dernière mise à jour : 2026-04-24 · VAULT 369 LTD · Laurent Duplat*
