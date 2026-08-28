import fs from 'node:fs'
import path from 'node:path'

const root = process.cwd()
const sourceDir = path.join(root, 'content', 'portfolio-articles')
const blogDir = path.join(root, 'blog')
const basePages = new Set(['/', '/blog', '/contact', '/a-propos', '/categories', '/confidentialite', '/mentions-legales', '/cgu', '/agence'])
const files = fs.readdirSync(sourceDir).filter((name) => name.endsWith('.md')).sort()
const issues = []
const records = []

function parse(raw, file) {
  const match = raw.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n([\s\S]*)$/)
  if (!match) { issues.push(`${file}: frontmatter absent`); return { data: {}, body: '' } }
  const data = {}
  for (const line of match[1].split(/\r?\n/)) {
    const m = line.match(/^([A-Za-z][A-Za-z0-9_]*)\s*:\s*(?:"(.*)"|'(.*)'|(.*))$/)
    if (m) data[m[1]] = (m[2] ?? m[3] ?? m[4] ?? '').trim()
  }
  return { data, body: match[2] }
}

function words(text) { return (text.match(/[A-Za-zÀ-ÖØ-öø-ÿ0-9][A-Za-zÀ-ÖØ-öø-ÿ0-9’'-]*/g) || []).length }
function allLinks(text) { return [...text.matchAll(/href="([^"]+)"/g)].map((m) => m[1]) }
function editorialMarkdown(body) {
  return body
    .replace(/^#\s+.+$/m, '')
    .split(/^##\s+(?:FAQ|Questions fréquentes)\s*$/mi)[0]
    .replace(/\[[^\]]+\]\([^)]*\)/g, ' ')
}
function renderedArticle(html) {
  return (html.match(/<article class="article-content">([\s\S]*?)<\/article>/) || [])[1] || ''
}
function hasLocalRoute(clean) {
  const relative = clean.replace(/^\//, '')
  return fs.existsSync(path.join(root, relative)) || fs.existsSync(path.join(root, `${relative}.html`))
}

for (const file of files) {
  const { data, body } = parse(fs.readFileSync(path.join(sourceDir, file), 'utf8'), file)
  const htmlPath = path.join(blogDir, `${data.slug}.html`)
  const html = fs.existsSync(htmlPath) ? fs.readFileSync(htmlPath, 'utf8') : ''
  const articleHtml = renderedArticle(html)
  const wordCount = words(editorialMarkdown(body))
  const contextualLinks = allLinks(articleHtml).filter((link) => /^\/blog\/[^/?#]+$/.test(link))
  const record = { file, slug: data.slug, editorialWords: wordCount, htmlWords: words(articleHtml.replace(/<script[\s\S]*?<\/script>|<style[\s\S]*?<\/style>|<[^>]+>/g, ' ')), htmlBytes: Buffer.byteLength(html), h1: (html.match(/<h1>/g) || []).length, canonical: (html.match(/<link rel="canonical"/g) || []).length, articleSchema: html.includes('"@type":"Article"'), faqSchema: html.includes('"@type":"FAQPage"'), indexable: html.includes('<meta name="robots" content="index,follow,max-image-preview:large">'), contextualArticleLinks: contextualLinks.length, images: data.image }
  records.push(record)
  if (!data.slug || !data.title || !data.description || !data.image) issues.push(`${file}: métadonnée obligatoire manquante`)
  if (wordCount < 3000) issues.push(`${file}: ${wordCount} mots utiles, seuil SEO3000 non atteint`)
  if (/[ÃÂ�]|\uFFFD/.test(body + articleHtml)) issues.push(`${file}: encodage suspect`)
  if (/(priceRange|lowPrice|highPrice|priceCurrency|"price"|€|CHF|\$|£|\bprix\b|\btarif\b|\bmontant\b|\bdevis\b|\bco[uû]t\b)/i.test(body + articleHtml)) issues.push(`${file}: règle portefeuille prix potentiellement violée`)
  if (/preview-|\.html(?:\)|")/.test(body)) issues.push(`${file}: lien de prévisualisation ou extension publique dans le maillage`)
  if (!html || !articleHtml || record.h1 !== 1 || record.canonical !== 1 || !record.articleSchema || !record.faqSchema || !record.indexable) issues.push(`${file}: rendu HTML incomplet (fichier/H1/canonical/schema/robots indexables)`)
  if (data.image?.startsWith('http') || !fs.existsSync(path.join(root, data.image.replace(/^\//, '')))) issues.push(`${file}: image locale manquante ou hotlink`)
  if (!html.includes("_c==='rejected'?'denied':'granted'")) issues.push(`${file}: GA4 consent opt-out attendu absent`)
  if (!articleHtml.includes('class="article-cta"')) issues.push(`${file}: CTA de contact absent`)
  if (!articleHtml.includes('Sources de référence')) issues.push(`${file}: sources visibles absentes`)
  if (!articleHtml.match(/<h2>(?:FAQ|Questions fréquentes)<\/h2>/)) issues.push(`${file}: FAQ visible absente`)
  if (contextualLinks.length < 2) issues.push(`${file}: maillage contextuel insuffisant (${contextualLinks.length})`)
  for (const link of allLinks(articleHtml)) {
    if (!link.startsWith('/') || link.startsWith('//')) continue
    const clean = link.split('#')[0].split('?')[0]
    const targetSlug = clean.match(/^\/blog\/([^/]+)$/)?.[1]
    if (targetSlug && !fs.existsSync(path.join(blogDir, `${targetSlug}.html`))) issues.push(`${file}: lien interne cassé ${link}`)
    else if (!targetSlug && !basePages.has(clean) && !hasLocalRoute(clean)) issues.push(`${file}: destination locale non vérifiée ${link}`)
  }
}

const slugs = records.map((r) => r.slug)
if (new Set(slugs).size !== files.length) issues.push('slugs dupliqués')
const report = { date: new Date().toISOString(), articleCount: records.length, records, issueCount: issues.length, issues }
console.log(JSON.stringify(report, null, 2))
process.exitCode = issues.some((issue) => /manquante|hotlink|cassé|métadonnée|encodage|GA4|prévisualisation|règle portefeuille|slugs dupliqués|rendu HTML incomplet/.test(issue)) ? 1 : 0
