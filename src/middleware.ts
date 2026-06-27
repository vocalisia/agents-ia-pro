import { NextResponse, type NextRequest } from 'next/server'

const languages = new Set(['en', 'de', 'nl', 'es', 'it', 'pt'])

const agentTargets: Record<string, string> = {
  vocalis: '/vocalis-pro',
  'design-ai': '/agent-design',
  'chatbot-pro': '/agent-chatbot',
  'seo-master': '/agent-seo',
  'recruteur-ia': '/agent-rh',
  'email-genius': '/agent-email',
  'compta-bot': '/agent-finance',
}

const categoryTargets: Record<string, string> = {
  vocal: '/vocalis-pro',
  vente: '/agent-commercial',
  support: '/agent-support',
  marketing: '/agent-marketing',
  email: '/agent-email',
  seo: '/agent-seo',
  rh: '/agent-rh',
  finance: '/agent-finance',
  dev: '/agent-dev',
  design: '/agent-design',
  juridique: '/agent-juridique',
  custom: '/contact',
}

const canonicalPaths = new Set([
  '/agent-chatbot',
  '/agent-commercial',
  '/agent-design',
  '/agent-dev',
  '/agent-email',
  '/agent-finance',
  '/agent-juridique',
  '/agent-marketing',
  '/agent-rh',
  '/agent-seo',
  '/agent-support',
  '/vocalis-pro',
  '/contact',
])

function redirectWithoutQuery(request: NextRequest, pathname: string) {
  return NextResponse.redirect(new URL(pathname, request.url), 301)
}

function stripLanguage(pathname: string) {
  const parts = pathname.split('/').filter(Boolean)
  if (parts.length > 1 && languages.has(parts[0])) {
    return `/${parts.slice(1).join('/')}`
  }
  return pathname
}

export function middleware(request: NextRequest) {
  const url = request.nextUrl
  const pathname = stripLanguage(url.pathname)

  if (canonicalPaths.has(pathname) && (url.searchParams.has('id') || url.searchParams.has('cat'))) {
    return redirectWithoutQuery(request, pathname)
  }

  if (pathname === '/agent' || pathname === '/agent.html') {
    const target = agentTargets[url.searchParams.get('id') || ''] || '/agent-chatbot'
    return redirectWithoutQuery(request, target)
  }

  if (pathname === '/categories' || pathname === '/categories.html') {
    const target = categoryTargets[url.searchParams.get('cat') || '']
    if (target) return redirectWithoutQuery(request, target)
  }

  return NextResponse.next()
}

export const config = {
  matcher: [
    '/agent',
    '/agent.html',
    '/categories',
    '/categories.html',
    '/:lang(en|de|nl|es|it|pt)/agent',
    '/:lang(en|de|nl|es|it|pt)/agent.html',
    '/:lang(en|de|nl|es|it|pt)/categories',
    '/:lang(en|de|nl|es|it|pt)/categories.html',
    '/agent-:path*',
    '/vocalis-pro',
    '/contact',
  ],
}
