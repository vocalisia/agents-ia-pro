export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { name, email, company, subject, message } = req.body;

  if (!name || !email || !message) {
    return res.status(400).json({ error: 'Champs requis manquants' });
  }

  try {
    const response = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.RESEND_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        from: 'Agents-IA.pro <onboarding@resend.dev>',
        to: ['contact@vocalis.pro'],
        reply_to: email,
        subject: `[Contact agents-ia.pro] ${subject || 'Nouveau message'}`,
        html: `
          <div style="font-family: Inter, sans-serif; max-width: 600px; margin: 0 auto; padding: 32px; background: #f8f8f8;">
            <div style="background: linear-gradient(135deg, #6366f1, #ec4899); padding: 24px 32px; border-radius: 12px 12px 0 0;">
              <h1 style="color: white; margin: 0; font-size: 20px;">Nouveau message — Agents-IA.pro</h1>
            </div>
            <div style="background: white; padding: 32px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.08);">
              <table style="width: 100%; border-collapse: collapse;">
                <tr><td style="padding: 8px 0; color: #666; font-size: 14px; width: 120px;">Nom</td><td style="padding: 8px 0; font-weight: 600; color: #111;">${name}</td></tr>
                <tr><td style="padding: 8px 0; color: #666; font-size: 14px;">Email</td><td style="padding: 8px 0; font-weight: 600; color: #111;"><a href="mailto:${email}" style="color: #6366f1;">${email}</a></td></tr>
                ${company ? `<tr><td style="padding: 8px 0; color: #666; font-size: 14px;">Entreprise</td><td style="padding: 8px 0; font-weight: 600; color: #111;">${company}</td></tr>` : ''}
                ${subject ? `<tr><td style="padding: 8px 0; color: #666; font-size: 14px;">Sujet</td><td style="padding: 8px 0; font-weight: 600; color: #111;">${subject}</td></tr>` : ''}
              </table>
              <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
              <p style="color: #333; line-height: 1.7; white-space: pre-wrap;">${message}</p>
              <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">
              <p style="color: #999; font-size: 12px; margin: 0;">Envoyé depuis agents-ia.pro le ${new Date().toLocaleDateString('fr-FR', { day: '2-digit', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
            </div>
          </div>
        `,
      }),
    });

    if (!response.ok) {
      const err = await response.json();
      console.error('Resend error:', err);
      return res.status(500).json({ error: 'Erreur envoi email' });
    }

    return res.status(200).json({ success: true });
  } catch (err) {
    console.error('Handler error:', err);
    return res.status(500).json({ error: 'Erreur serveur' });
  }
}
