module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', 'https://agents-ia.pro');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const body = parseBody(req.body);
  const email = String(body.email || '').trim();
  const name = String(body.name || [body.prenom, body.nom].filter(Boolean).join(' ') || email).trim();
  const company = String(body.company || body.entreprise || '').trim();
  const subject = String(body.subject || body._subject || body.sujet || '').trim();
  const message = String(body.message || body.besoin || body.projet || '').trim();
  const formType = message ? 'contact' : 'newsletter';

  if (!isValidEmail(email)) {
    return res.status(400).json({ error: 'Email invalide' });
  }

  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    return res.status(500).json({ error: 'Configuration email manquante' });
  }

  const html = `
    <div style="font-family:Arial,sans-serif;max-width:640px;color:#222">
      <h2>Nouveau ${escapeHtml(formType)} agents-ia.pro</h2>
      <table style="border-collapse:collapse;width:100%">
        ${row('Nom', name)}
        ${row('Email', email)}
        ${row('Entreprise', company || '-')}
        ${row('Sujet', subject || '-')}
        ${row('Message', message || '-')}
        ${row('Page', req.headers.referer || '-')}
      </table>
    </div>
  `;

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: process.env.LEADS_EMAIL_FROM || 'Agents-IA.pro <onboarding@resend.dev>',
        to: [process.env.CONTACT_EMAIL || 'contact@vocalis.pro'],
        reply_to: email,
        subject: `[agents-ia.pro] ${formType} - ${subject || name}`,
        html,
      }),
    });

    const text = await response.text();
    if (!response.ok) {
      return res.status(502).json({ error: 'Erreur envoi email', details: text });
    }

    let data = {};
    try {
      data = JSON.parse(text);
    } catch {}

    if (wantsHtml(req)) {
      res.writeHead(303, { Location: req.headers.referer || '/merci.html' });
      return res.end();
    }

    return res.status(200).json({ success: true, id: data.id || null });
  } catch (err) {
    return res.status(500).json({ error: 'Erreur serveur', details: err.message });
  }
};

function parseBody(rawBody) {
  if (!rawBody) return {};
  if (typeof rawBody === 'object') return rawBody;
  try {
    return JSON.parse(String(rawBody));
  } catch {
    const params = new URLSearchParams(String(rawBody));
    return Object.fromEntries(params.entries());
  }
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function wantsHtml(req) {
  const accept = String(req.headers.accept || '');
  const contentType = String(req.headers['content-type'] || '');
  return accept.includes('text/html') && !contentType.includes('application/json');
}

function row(label, value) {
  return `<tr><td style="padding:8px;border:1px solid #ddd;font-weight:700;background:#f7f7f7">${escapeHtml(label)}</td><td style="padding:8px;border:1px solid #ddd">${escapeHtml(value)}</td></tr>`;
}

function escapeHtml(value) {
  return String(value == null ? '' : value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
