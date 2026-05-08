# DNS Records à ajouter pour agents-ia.pro

## 📧 Resend (emails transactionnels — envoyer depuis hello@agents-ia.pro)

Le domaine `agents-ia.pro` a été ajouté dans Resend mais n'est pas encore vérifié.
En attendant la vérification DNS, le webhook envoie depuis `hello@trust.vocalis.pro` (déjà vérifié).

**Pour activer `hello@agents-ia.pro` comme sender :** ajouter ces 3 records DNS chez ton registrar (Vercel DNS / Cloudflare / registrar agents-ia.pro).

### 1. DKIM (TXT record)
| Type | Name | Value |
|------|------|-------|
| TXT | `resend._domainkey.agents-ia.pro` | `p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDPFc3pxsREA6b+6Yy0oGBfK7qCL1+WP1dLVoEBV6SQPR28pukN/m1ygHl6S62gSL6ZxGYMyABCu/u6NmI18izuWyx4fR7rgE3bEJS4MXI9qwaVe8CMYjE3gRvinNu/xTFqy4+wpPfeZ/EkrwdKIq3S0N31nLjgubFI1g556ux+PQIDAQAB` |

### 2. MX (SPF routing)
| Type | Name | Priority | Value |
|------|------|----------|-------|
| MX | `send.agents-ia.pro` | 10 | `feedback-smtp.eu-west-1.amazonses.com` |

### 3. SPF (TXT record)
| Type | Name | Value |
|------|------|-------|
| TXT | `send.agents-ia.pro` | `v=spf1 include:amazonses.com ~all` |

## Une fois les DNS ajoutés

1. Attendre 10-60 min propagation
2. Vérifier dans Resend Dashboard → https://resend.com/domains
3. Cliquer "Verify DNS"
4. Une fois "verified", changer dans `api/stripe-webhook.js` :
   ```js
   from: 'Agents-IA.pro <hello@agents-ia.pro>',
   ```
5. Redéployer : `vercel --prod`

---

## 🌐 Infos domaine actuelles

- **Registrar** : à vérifier (vérifier `whois agents-ia.pro`)
- **DNS gérés par** : probablement Vercel (domaine connecté au projet)
- **Check** : `vercel domains inspect agents-ia.pro`

Si DNS gérés par Vercel → ajouter dans Vercel Dashboard → Project Settings → Domains → DNS Records.

---

*Généré le 2026-04-24 · agents-ia.pro · VAULT 369 LTD*
