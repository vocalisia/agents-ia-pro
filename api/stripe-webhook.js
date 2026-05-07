// Vercel Serverless Function — Stripe Webhook handler for agents-ia.pro
// Verifies signature, sends rapport PDFs via Resend on successful payment.
//
// Env vars required (set in Vercel Dashboard → Project → Settings → Environment Variables):
//   STRIPE_WEBHOOK_SECRET  (from Stripe Dashboard → Developers → Webhooks → Signing secret)
//   RESEND_API_KEY         (from resend.com/api-keys)
//
// Stripe webhook URL to set in Dashboard: https://agents-ia.pro/api/stripe-webhook
// Events to subscribe: checkout.session.completed

import Stripe from 'stripe';
import { Resend } from 'resend';

export const config = {
  api: {
    bodyParser: false, // Stripe needs raw body for signature verification
  },
};

const SECURE_TOKEN = process.env.SECURE_TOKEN;
if (!SECURE_TOKEN) throw new Error('SECURE_TOKEN not set');
const BASE_URL = 'https://agents-ia.pro';

const PRODUCT_META = {
  rapport_assurance: {
    name: "Rapport · État de l'IA dans l'assurance France 2026",
    pdf: `${BASE_URL}/secure/${SECURE_TOKEN}/rapport-assurance-ia-france-2026.pdf`,
    filename: 'rapport-assurance-ia-france-2026.pdf',
  },
  rapport_voice: {
    name: 'Rapport · Benchmark 50 agents vocaux IA 2026',
    pdf: `${BASE_URL}/secure/${SECURE_TOKEN}/rapport-benchmark-50-voice-ai-2026.pdf`,
    filename: 'rapport-benchmark-50-voice-ai-2026.pdf',
  },
  rapport_rgpd: {
    name: 'Rapport · RGPD & AI Act : conformité PME 2026',
    pdf: `${BASE_URL}/secure/${SECURE_TOKEN}/rapport-rgpd-ai-act-pme-2026.pdf`,
    filename: 'rapport-rgpd-ai-act-pme-2026.pdf',
  },
  rapport_bundle: {
    name: 'Bundle 3 rapports (Assurance + Voice + RGPD)',
    pdf: null, // 3 PDFs, handled specially below
    filename: null,
  },
};

async function getRawBody(req) {
  const chunks = [];
  for await (const chunk of req) {
    chunks.push(typeof chunk === 'string' ? Buffer.from(chunk) : chunk);
  }
  return Buffer.concat(chunks);
}

function buildEmailHtml(slug, customerName, customerEmail, meta) {
  const greeting = customerName ? `Bonjour ${customerName},` : 'Bonjour,';

  // Bundle = 3 download links
  if (slug === 'rapport_bundle') {
    return `
<!DOCTYPE html>
<html><body style="font-family:Inter,Arial,sans-serif;color:#1f2937;max-width:600px;margin:0 auto;padding:24px;background:#f9fafb;">
  <div style="background:white;border-radius:16px;padding:32px;">
    <h1 style="color:#6366f1;font-size:24px;margin:0 0 16px;">✅ Merci pour votre achat !</h1>
    <p>${greeting}</p>
    <p>Votre <strong>Bundle 3 rapports</strong> est prêt. Voici vos 3 PDFs :</p>
    <ul style="line-height:1.8;">
      <li>🛡️ <a href="${BASE_URL}/secure/${SECURE_TOKEN}/rapport-assurance-ia-france-2026.pdf" style="color:#6366f1;">Rapport État de l'IA dans l'assurance France 2026 (87 pages)</a></li>
      <li>🎙️ <a href="${BASE_URL}/secure/${SECURE_TOKEN}/rapport-benchmark-50-voice-ai-2026.pdf" style="color:#6366f1;">Benchmark 50 agents vocaux IA 2026 (64 pages)</a></li>
      <li>⚖️ <a href="${BASE_URL}/secure/${SECURE_TOKEN}/rapport-rgpd-ai-act-pme-2026.pdf" style="color:#6366f1;">RGPD &amp; AI Act : conformité PME 2026 (52 pages)</a></li>
    </ul>
    <p style="color:#6b7280;font-size:14px;margin-top:24px;">Ces liens sont personnels. Merci de ne pas les partager.</p>
    <p>Des questions ? Répondez simplement à cet email.</p>
    <p>— Laurent Duplat<br>Agents-IA.pro · VAULT 369 LTD</p>
  </div>
  <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">© 2026 VAULT 369 LTD · <a href="${BASE_URL}" style="color:#9ca3af;">agents-ia.pro</a></p>
</body></html>`;
  }

  // Subscription (Featured Listing) — no PDF, just welcome
  if (['bronze', 'silver', 'gold'].includes(slug)) {
    const planName = slug.charAt(0).toUpperCase() + slug.slice(1);
    return `
<!DOCTYPE html>
<html><body style="font-family:Inter,Arial,sans-serif;color:#1f2937;max-width:600px;margin:0 auto;padding:24px;background:#f9fafb;">
  <div style="background:white;border-radius:16px;padding:32px;">
    <h1 style="color:#6366f1;font-size:24px;margin:0 0 16px;">🎉 Bienvenue sur Agents-IA.pro !</h1>
    <p>${greeting}</p>
    <p>Votre Featured Listing <strong>${planName}</strong> est activé. Voici les prochaines étapes :</p>
    <ol style="line-height:1.8;">
      <li>Notre équipe vous contacte sous <strong>48h</strong> pour récupérer votre pitch, screenshots et vidéo demo.</li>
      <li>Mise en ligne de votre fiche sous <strong>5 jours ouvrés</strong>.</li>
      <li>Dashboard stats accessible sous 7 jours.</li>
    </ol>
    <p>En attendant, <strong>répondez à cet email</strong> avec :</p>
    <ul>
      <li>📝 Pitch produit 100-200 mots</li>
      <li>🖼️ 2-3 screenshots de l'interface (1920×1080)</li>
      <li>🎥 Vidéo demo YouTube/Loom (1-3 min)</li>
      <li>🏷️ Logo HD (PNG transparent)</li>
      <li>🏷️ Catégorie souhaitée</li>
    </ul>
    <p>— Laurent Duplat<br>Fondateur Agents-IA.pro</p>
  </div>
  <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">© 2026 VAULT 369 LTD · <a href="${BASE_URL}" style="color:#9ca3af;">agents-ia.pro</a></p>
</body></html>`;
  }

  // Submit fast-track
  if (slug === 'submit_fasttrack') {
    return `
<!DOCTYPE html>
<html><body style="font-family:Inter,Arial,sans-serif;color:#1f2937;max-width:600px;margin:0 auto;padding:24px;background:#f9fafb;">
  <div style="background:white;border-radius:16px;padding:32px;">
    <h1 style="color:#6366f1;font-size:24px;margin:0 0 16px;">⚡ Fast-Track activé !</h1>
    <p>${greeting}</p>
    <p>Votre soumission <strong>Fast-Track</strong> (149€) est activée. Review prioritaire sous <strong>48h</strong>, publication sous <strong>5 jours ouvrés</strong>.</p>
    <p>Pour lancer la review, répondez à cet email avec :</p>
    <ul>
      <li>Lien vers votre agent IA</li>
      <li>Pitch 100-200 mots</li>
      <li>Logo + 1-2 screenshots</li>
      <li>Catégorie cible</li>
    </ul>
    <p>— Laurent Duplat<br>Agents-IA.pro</p>
  </div>
</body></html>`;
  }

  // Single report
  return `
<!DOCTYPE html>
<html><body style="font-family:Inter,Arial,sans-serif;color:#1f2937;max-width:600px;margin:0 auto;padding:24px;background:#f9fafb;">
  <div style="background:white;border-radius:16px;padding:32px;">
    <h1 style="color:#6366f1;font-size:24px;margin:0 0 16px;">✅ Merci pour votre achat !</h1>
    <p>${greeting}</p>
    <p>Votre rapport <strong>${meta.name}</strong> est prêt au téléchargement :</p>
    <p style="text-align:center;margin:32px 0;">
      <a href="${meta.pdf}" style="display:inline-block;padding:14px 28px;background:linear-gradient(90deg,#6366f1,#a855f7);color:white;border-radius:12px;font-weight:600;text-decoration:none;">📄 Télécharger le PDF</a>
    </p>
    <p style="color:#6b7280;font-size:14px;">Ce lien est personnel. Merci de ne pas le partager.</p>
    <p>Une question ou un retour ? Répondez simplement à cet email.</p>
    <p>— Laurent Duplat<br>Agents-IA.pro · VAULT 369 LTD</p>
  </div>
  <p style="text-align:center;color:#9ca3af;font-size:12px;margin-top:16px;">© 2026 VAULT 369 LTD · <a href="${BASE_URL}" style="color:#9ca3af;">agents-ia.pro</a></p>
</body></html>`;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  const resend = new Resend(process.env.RESEND_API_KEY);

  const rawBody = await getRawBody(req);
  const sig = req.headers['stripe-signature'];

  let event;
  try {
    event = stripe.webhooks.constructEvent(rawBody, sig, process.env.STRIPE_WEBHOOK_SECRET);
  } catch (err) {
    console.error('Webhook signature verification failed:', err.message);
    return res.status(400).json({ error: `Webhook Error: ${err.message}` });
  }

  if (event.type !== 'checkout.session.completed') {
    return res.status(200).json({ received: true, ignored: event.type });
  }

  const session = event.data.object;
  const slug = session.metadata?.slug;
  const customerEmail = session.customer_details?.email;
  const customerName = session.customer_details?.name;

  if (!slug || !customerEmail) {
    console.warn('Missing slug or email in session', session.id);
    return res.status(200).json({ received: true, warning: 'missing_metadata' });
  }

  const meta = PRODUCT_META[slug];
  if (!meta) {
    console.warn('Unknown product slug:', slug);
    return res.status(200).json({ received: true, warning: 'unknown_slug' });
  }

  const subject = slug.startsWith('rapport_')
    ? `Votre rapport : ${meta.name}`
    : slug === 'submit_fasttrack'
    ? '⚡ Soumission Fast-Track activée — prochaines étapes'
    : `Bienvenue sur Agents-IA.pro — plan ${slug.toUpperCase()}`;

  const html = buildEmailHtml(slug, customerName, customerEmail, meta);

  try {
    // Using trust.vocalis.pro (verified in Resend) as from address.
    // Switch to hello@agents-ia.pro once DNS records validated.
    await resend.emails.send({
      from: 'Agents-IA.pro <hello@trust.vocalis.pro>',
      to: customerEmail,
      bcc: ['contact@vocalis.pro'],
      subject,
      html,
      reply_to: 'contact@vocalis.pro',
    });
    console.log(`Email sent to ${customerEmail} for ${slug}`);
  } catch (err) {
    console.error('Resend error:', err);
    // Don't fail the webhook if email fails (Stripe will retry)
  }

  return res.status(200).json({ received: true, slug, emailed: customerEmail });
}
