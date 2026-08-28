import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const sourceDir = path.join(root, 'content', 'portfolio-articles')
const blogDir = path.join(root, 'blog')
const imageDir = path.join(root, 'images', 'article-covers')
const baseUrl = 'https://agents-ia.pro'
const siteShell = fs.readFileSync(path.join(root, 'index.html'), 'utf8')

function extractShell(pattern, label) {
  const match = siteShell.match(pattern)
  if (!match) throw new Error(`Fragment introuvable dans index.html : ${label}`)
  return match[0]
}

const navbar = extractShell(/<nav class="navbar"[\s\S]*?<\/nav>/, 'navbar')
  .replaceAll('href="#', 'href="/#')
const footer = extractShell(/<footer class="footer">[\s\S]*?<\/footer>/, 'footer')
const whatsappWidget = extractShell(/<a href="https:\/\/wa\.me\/[^"]+" class="whatsapp-widget"[\s\S]*?<\/a>/, 'widget WhatsApp')
const brandPatch = extractShell(/<style id="brand-logo-patch">[\s\S]*?<\/style>/, 'brand logo patch')
const perfPatch = extractShell(/<style id="data-perf-sprint5-cls">[\s\S]*?<\/style>/, 'performance patch')

function parseFrontmatter(raw) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) throw new Error('Frontmatter absent ou mal formé')
  const data = {}
  for (const line of match[1].split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z][A-Za-z0-9_]*)\s*:\s*(.*)$/)
    if (!m) continue
    let value = m[2].trim()
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) value = value.slice(1, -1)
    data[m[1]] = value
  }
  return { data, body: match[2].trim() }
}

function esc(value) {
  return String(value).replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;')
}

function inline(value) {
  let result = esc(value)
  result = result.replace(/\[([^\]]+)\]\((https?:\/\/[^\s)]+|\/[^\s)]+)\)/g, '<a href="$2">$1</a>')
  result = result.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
  result = result.replace(/`([^`]+)`/g, '<code>$1</code>')
  return result
}

function markdownToHtml(markdown) {
  const lines = markdown.split(/\r?\n/)
  const out = []
  let firstH1 = true
  let paragraph = []
  let list = null
  const flushParagraph = () => {
    if (paragraph.length) { out.push(`<p>${inline(paragraph.join(' '))}</p>`); paragraph = [] }
  }
  const closeList = () => {
    if (list) { out.push(`</${list}>`); list = null }
  }
  for (const line of lines) {
    if (!line.trim()) { flushParagraph(); closeList(); continue }
    const heading = line.match(/^(#{1,3})\s+(.+)$/)
    if (heading) { flushParagraph(); closeList(); const level = heading[1].length; if (!(level === 1 && firstH1)) out.push(`<h${level}>${inline(heading[2])}</h${level}>`); if (level === 1) firstH1 = false; continue }
    const bullet = line.match(/^[-*]\s+(.+)$/)
    if (bullet) { flushParagraph(); if (list !== 'ul') { closeList(); out.push('<ul>'); list = 'ul' } out.push(`<li>${inline(bullet[1])}</li>`); continue }
    const ordered = line.match(/^\d+\.\s+(.+)$/)
    if (ordered) { flushParagraph(); if (list !== 'ol') { closeList(); out.push('<ol>'); list = 'ol' } out.push(`<li>${inline(ordered[1])}</li>`); continue }
    closeList(); paragraph.push(line.trim())
  }
  flushParagraph(); closeList()
  return out.join('\n')
}

function textWordCount(markdown) {
  return (markdown.match(/[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9’'-]*/g) || []).length
}

function faqSchema(markdown, articleUrl) {
  const faqHeading = markdown.match(/^## (?:FAQ|Questions fréquentes)\s*$/mi)
  const faqStart = faqHeading ? faqHeading.index : -1
  if (faqStart < 0) return null
  const section = markdown.slice(faqStart).split(/\r?\n## /m)[0]
  const blocks = [...section.matchAll(/###\s+([^\n]+)\n+([\s\S]*?)(?=\n###\s+|\n##\s+|$)/g)]
  if (!blocks.length) return null
  return {
    '@context': 'https://schema.org', '@type': 'FAQPage', '@id': `${articleUrl}#faq`,
    mainEntity: blocks.map(([, question, answer]) => ({ '@type': 'Question', name: question.trim(), acceptedAnswer: { '@type': 'Answer', text: answer.replace(/\[([^\]]+)\]\([^)]*\)/g, '$1').replace(/\s+/g, ' ').trim() } }))
  }
}

function render(data, body) {
  const articleUrl = `${baseUrl}/blog/${data.slug}`
  const imageUrl = `${baseUrl}${data.image}`
  const articleSchema = {
    '@context': 'https://schema.org', '@type': 'Article', '@id': `${articleUrl}#article`,
    headline: data.title, description: data.description, url: articleUrl, mainEntityOfPage: { '@type': 'WebPage', '@id': articleUrl },
    datePublished: data.date, dateModified: data.dateModified || data.date, inLanguage: 'fr', image: imageUrl,
    author: { '@type': 'Person', '@id': `${baseUrl}/#founder`, name: data.author || 'Laurent Duplat', url: `${baseUrl}/a-propos` },
    publisher: { '@type': 'Organization', '@id': `${baseUrl}/#organization`, name: 'Agents-IA.pro', url: baseUrl, logo: `${baseUrl}/favicon.svg` },
    articleSection: data.category, wordCount: textWordCount(body), isAccessibleForFree: true,
  }
  const breadcrumbSchema = { '@context': 'https://schema.org', '@type': 'BreadcrumbList', itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Accueil', item: `${baseUrl}/` },
    { '@type': 'ListItem', position: 2, name: 'Blog', item: `${baseUrl}/blog` },
    { '@type': 'ListItem', position: 3, name: data.title, item: articleUrl },
  ] }
  const schemas = [articleSchema, breadcrumbSchema, faqSchema(body, articleUrl)].filter(Boolean).map((schema) => `<script type="application/ld+json">${JSON.stringify(schema).replaceAll('<', '\\u003c')}</script>`).join('\n')
  const articleHtml = markdownToHtml(body)
  return `<!doctype html>
<html lang="fr"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="/css/style.css">
<title>${esc(data.title)} | Agents-IA.pro</title><meta name="description" content="${esc(data.description)}">
<meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="${articleUrl}">
<meta property="og:type" content="article"><meta property="og:title" content="${esc(data.title)}"><meta property="og:description" content="${esc(data.description)}"><meta property="og:url" content="${articleUrl}"><meta property="og:image" content="${imageUrl}"><meta property="og:locale" content="fr_FR">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="${esc(data.title)}"><meta name="twitter:description" content="${esc(data.description)}"><meta name="twitter:image" content="${imageUrl}">
<link rel="icon" type="image/svg+xml" href="/favicon.svg"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" onload="this.onload=null;this.rel='stylesheet'"><noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"></noscript>
<link rel="preload" as="style" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css" onload="this.onload=null;this.rel='stylesheet'"><noscript><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"></noscript>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}window.gtag=gtag;var _c=(typeof localStorage!=='undefined')?localStorage.getItem('ai_cookies'):null;gtag('consent','default',{analytics_storage:_c==='rejected'?'denied':'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-B5627RD3TF"></script><script>gtag('js',new Date());gtag('config','G-B5627RD3TF');</script>
${schemas}
${brandPatch}
${perfPatch}
<style>.portfolio-article-cover{display:block;max-width:100%;height:auto;margin:0 auto 32px;border-radius:var(--radius)}.article-content{overflow-wrap:anywhere}.article-content pre,.article-content code{overflow-wrap:anywhere}</style>
</head><body>${navbar}
<main data-article-slug="${esc(data.slug)}"><section class="section article-hero"><div class="container"><p class="blog-tag">${esc(data.category)}</p><h1>${esc(data.title)}</h1><p class="section-sub">${esc(data.description)}</p><div class="article-meta"><span>Par ${esc(data.author || 'Laurent Duplat')}</span><span>${esc(data.date)}</span><span>${esc(data.readTime || 'Lecture pratique')}</span></div></div></section>
<article class="article-content"><p><a href="/blog">Retour au blog</a></p><img class="portfolio-article-cover" src="${esc(data.image)}" alt="Illustration originale : ${esc(data.title)}" width="1200" height="630" loading="eager" decoding="async">${articleHtml}
<section class="article-cta" aria-label="Contact"><h3>Besoin d’un cadrage sur votre cas ?</h3><p>Le formulaire de contact permet de décrire le processus, les données, les permissions et la reprise humaine à relire.</p><a class="btn btn-primary" href="/contact">Contacter l’équipe</a></section></article></main>
${footer}${whatsappWidget}<script src="/js/app.js" defer></script></body></html>`
}

fs.mkdirSync(blogDir, { recursive: true })
const files = fs.readdirSync(sourceDir).filter((name) => name.endsWith('.md')).sort()
const urls = []
for (const file of files) {
  const { data, body } = parseFrontmatter(fs.readFileSync(path.join(sourceDir, file), 'utf8'))
  if (!data.slug || !data.title || !data.image) throw new Error(`${file}: métadonnées obligatoires manquantes`)
  const target = path.join(blogDir, `${data.slug}.html`)
  fs.writeFileSync(target, render(data, body), 'utf8')
  urls.push(`  <url><loc>${baseUrl}/blog/${data.slug}</loc><lastmod>${data.dateModified || data.date}</lastmod></url>`)
  console.log(`${data.slug}\t${textWordCount(body)} words\t${target}`)
}
fs.writeFileSync(path.join(root, 'sitemap-portfolio-articles.xml'), `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls.join('\n')}\n</urlset>\n`, 'utf8')
