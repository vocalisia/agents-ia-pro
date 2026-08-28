const canonicalOrigin = 'https://agents-ia.pro';

const agentTargets = new Map([
  ['vocalis', '/vocalis-pro'],
  ['design-ai', '/agent-design'],
  ['chatbot-pro', '/agent-chatbot'],
  ['seo-master', '/agent-seo'],
  ['recruteur-ia', '/agent-rh'],
  ['email-genius', '/agent-email'],
  ['compta-bot', '/agent-finance'],
]);

const categoryTargets = new Map([
  ['vocal', '/vocalis-pro'],
  ['vente', '/agent-commercial'],
  ['support', '/agent-support'],
  ['marketing', '/agent-marketing'],
  ['email', '/agent-email'],
  ['seo', '/agent-seo'],
  ['rh', '/agent-rh'],
  ['finance', '/agent-finance'],
  ['dev', '/agent-dev'],
  ['design', '/agent-design'],
  ['juridique', '/agent-juridique'],
  ['custom', '/contact'],
]);

const directTargets = new Set([
  '/vocalis-pro',
  '/agent-design',
  '/agent-chatbot',
  '/agent-seo',
  '/agent-rh',
  '/agent-email',
  '/agent-finance',
  '/agent-commercial',
  '/agent-support',
  '/agent-marketing',
  '/agent-dev',
  '/agent-juridique',
  '/contact',
]);

export default function handler(req, res) {
  const requestUrl = new URL(req.url || '/', canonicalOrigin);
  const source = requestUrl.searchParams.get('source');
  let target = '/';

  if (source === 'agent') {
    target = agentTargets.get(requestUrl.searchParams.get('id')) || '/agent-chatbot';
  } else if (source === 'categories') {
    target = categoryTargets.get(requestUrl.searchParams.get('cat')) || '/categories';
  } else if (source === 'target') {
    const candidate = `/${requestUrl.searchParams.get('target') || ''}`;
    target = directTargets.has(candidate) ? candidate : '/';
  }

  res.statusCode = 301;
  res.setHeader('Location', `${canonicalOrigin}${target}`);
  res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
  res.end();
}
