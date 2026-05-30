import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import Link from 'next/link'
import { MDXRemote } from 'next-mdx-remote/rsc'
import Navbar from '@/components/Navbar'
import { getAllPostSlugs, getPost, formatDate } from '@/lib/mdx'

interface Props {
  params: { slug: string }
}

export async function generateStaticParams() {
  return getAllPostSlugs().map((slug) => ({ slug }))
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = getPost(params.slug)
  if (!post) return {}

  return {
    title: post.title,
    description: post.description,
    authors: [{ name: post.author }],
    alternates: {
      canonical: `https://agents-ia.pro/blog/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.description,
      url: `https://agents-ia.pro/blog/${post.slug}`,
      type: 'article',
      publishedTime: post.date,
      authors: [post.author],
      images: post.image
        ? [{ url: post.image }]
        : [{ url: '/og-image.png', width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.description,
    },
  }
}

export default function BlogPostPage({ params }: Props) {
  const post = getPost(params.slug)
  if (!post) notFound()

  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': `https://agents-ia.pro/blog/${post.slug}`,
    headline: post.title,
    description: post.description,
    datePublished: post.date,
    dateModified: post.dateModified ?? post.date,
    url: `https://agents-ia.pro/blog/${post.slug}`,
    image: post.image ?? 'https://agents-ia.pro/og-image.png',
    inLanguage: 'fr',
    author: {
      '@type': 'Person',
      '@id': 'https://agents-ia.pro/#founder',
      name: post.author,
      url: 'https://agents-ia.pro/a-propos.html',
      sameAs: [
        'https://www.linkedin.com/in/vocalisia/',
        'https://x.com/VocalisAi',
      ],
    },
    publisher: {
      '@id': 'https://agents-ia.pro/#organization',
    },
    isPartOf: {
      '@type': 'Blog',
      name: 'Blog Agents-IA.pro',
      url: 'https://agents-ia.pro/blog',
    },
    mainEntityOfPage: {
      '@type': 'WebPage',
      '@id': `https://agents-ia.pro/blog/${post.slug}`,
    },
    keywords: post.category,
    articleSection: post.category,
    wordCount: post.content.split(/\s+/).length,
  }

  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Accueil',
        item: 'https://agents-ia.pro/',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Blog',
        item: 'https://agents-ia.pro/blog',
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: post.title,
        item: `https://agents-ia.pro/blog/${post.slug}`,
      },
    ],
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      <Navbar />

      <main style={{ paddingTop: 100 }}>
        {/* Article header */}
        <header
          style={{
            padding: '60px 0 48px',
            position: 'relative',
            overflow: 'hidden',
            borderBottom: '1px solid rgba(255,255,255,0.06)',
          }}
        >
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background:
                'radial-gradient(800px 400px at 50% 0%,rgba(99,102,241,0.1),transparent 60%)',
              zIndex: -1,
            }}
          />
          <div className="mx-auto px-6" style={{ maxWidth: 860 }}>
            {/* Breadcrumb */}
            <nav
              aria-label="Fil d'Ariane"
              style={{
                display: 'flex',
                gap: 8,
                alignItems: 'center',
                marginBottom: 28,
                fontSize: 13,
                color: '#64748b',
              }}
            >
              <Link href="/" style={{ color: '#818cf8', textDecoration: 'none' }}>
                Accueil
              </Link>
              <i className="fas fa-chevron-right" style={{ fontSize: 10 }} />
              <Link href="/blog" style={{ color: '#818cf8', textDecoration: 'none' }}>
                Blog
              </Link>
              <i className="fas fa-chevron-right" style={{ fontSize: 10 }} />
              <span
                style={{
                  color: '#94a3b8',
                  maxWidth: 300,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}
              >
                {post.title}
              </span>
            </nav>

            {/* Category pill */}
            <span
              style={{
                display: 'inline-block',
                padding: '4px 14px',
                background: 'rgba(99,102,241,0.15)',
                color: '#818cf8',
                borderRadius: 999,
                fontSize: 11,
                fontWeight: 700,
                letterSpacing: '0.8px',
                textTransform: 'uppercase',
                marginBottom: 20,
              }}
            >
              {post.category}
            </span>

            <h1
              style={{
                fontSize: 'clamp(28px,4.5vw,52px)',
                fontWeight: 900,
                color: 'white',
                lineHeight: 1.1,
                letterSpacing: '-1px',
                marginBottom: 24,
              }}
            >
              {post.title}
            </h1>

            <p
              style={{
                fontSize: 18,
                color: '#94a3b8',
                lineHeight: 1.6,
                marginBottom: 32,
                maxWidth: 720,
              }}
            >
              {post.description}
            </p>

            {/* Author / meta row */}
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: 20,
                alignItems: 'center',
                fontSize: 13,
                color: '#64748b',
              }}
            >
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 10,
                }}
              >
                <div
                  style={{
                    width: 40,
                    height: 40,
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg,#6366f1,#a855f7)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 18,
                    color: 'white',
                    fontWeight: 800,
                    flexShrink: 0,
                  }}
                >
                  L
                </div>
                <div>
                  <div style={{ color: 'white', fontWeight: 600, fontSize: 14 }}>
                    {post.author}
                  </div>
                  <div style={{ fontSize: 12, color: '#64748b' }}>
                    Fondateur & Directeur de publication
                  </div>
                </div>
              </div>

              <span style={{ color: 'rgba(255,255,255,0.15)' }}>|</span>

              <span>
                <i className="fas fa-calendar" style={{ marginRight: 6 }} />
                {formatDate(post.date)}
              </span>

              <span>
                <i className="fas fa-clock" style={{ marginRight: 6 }} />
                {post.readTime}
              </span>
            </div>
          </div>
        </header>

        {/* Article body */}
        <div
          style={{ padding: '60px 0 80px' }}
        >
          <div
            className="mx-auto px-6"
            style={{ maxWidth: 860, display: 'grid', gridTemplateColumns: '1fr minmax(0,220px)', gap: 48, alignItems: 'start' }}
          >
            {/* Main content */}
            <article className="prose-blog">
              <MDXRemote source={post.content} />
            </article>

            {/* Sidebar */}
            <aside style={{ position: 'sticky', top: 100 }}>
              <div
                style={{
                  background: 'rgba(255,255,255,0.03)',
                  border: '1px solid rgba(255,255,255,0.08)',
                  borderRadius: 16,
                  padding: 24,
                  marginBottom: 20,
                }}
              >
                <div
                  style={{
                    fontSize: 12,
                    fontWeight: 700,
                    color: '#818cf8',
                    letterSpacing: '0.8px',
                    marginBottom: 16,
                    textTransform: 'uppercase',
                  }}
                >
                  À PROPOS DE L&apos;AUTEUR
                </div>
                <div
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: 12,
                    marginBottom: 12,
                  }}
                >
                  <div
                    style={{
                      width: 44,
                      height: 44,
                      borderRadius: '50%',
                      background: 'linear-gradient(135deg,#6366f1,#a855f7)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: 20,
                      color: 'white',
                      fontWeight: 800,
                      flexShrink: 0,
                    }}
                  >
                    L
                  </div>
                  <div>
                    <div style={{ color: 'white', fontWeight: 700, fontSize: 14 }}>
                      Laurent Duplat
                    </div>
                    <div style={{ fontSize: 12, color: '#64748b' }}>Expert IA & Automatisation</div>
                  </div>
                </div>
                <p style={{ fontSize: 13, color: '#64748b', lineHeight: 1.6, margin: 0 }}>
                  Fondateur d&apos;agents-ia.pro. Spécialiste déploiement agents IA pour PME francophones depuis 2023.
                </p>
              </div>

              <Link
                href="/agence.html"
                style={{
                  display: 'block',
                  padding: '18px 20px',
                  background: 'linear-gradient(135deg,rgba(99,102,241,0.15),rgba(168,85,247,0.08))',
                  border: '1px solid rgba(99,102,241,0.3)',
                  borderRadius: 16,
                  textDecoration: 'none',
                  textAlign: 'center',
                }}
              >
                <div style={{ fontSize: 24, marginBottom: 8 }}>🚀</div>
                <div style={{ color: 'white', fontWeight: 700, fontSize: 14, marginBottom: 6 }}>
                  Déployez votre agent IA
                </div>
                <div style={{ color: '#94a3b8', fontSize: 12, lineHeight: 1.5, marginBottom: 14 }}>
                  Audit gratuit 30 min avec un expert basé en Suisse.
                </div>
                <span
                  style={{
                    display: 'inline-block',
                    padding: '8px 18px',
                    background: 'linear-gradient(90deg,#6366f1,#a855f7)',
                    color: 'white',
                    borderRadius: 999,
                    fontSize: 12,
                    fontWeight: 700,
                  }}
                >
                  Réserver l&apos;audit
                </span>
              </Link>
            </aside>
          </div>
        </div>

        {/* Back to blog */}
        <div
          style={{
            borderTop: '1px solid rgba(255,255,255,0.08)',
            padding: '40px 0',
          }}
        >
          <div className="mx-auto px-6" style={{ maxWidth: 860 }}>
            <Link
              href="/blog"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                color: '#818cf8',
                textDecoration: 'none',
                fontSize: 14,
                fontWeight: 600,
              }}
            >
              <i className="fas fa-arrow-left" /> Retour au blog
            </Link>
          </div>
        </div>
      </main>

      <footer
        style={{
          padding: '40px 0 24px',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          textAlign: 'center',
          fontSize: 13,
          color: '#64748b',
        }}
      >
        <span>© {new Date().getFullYear()} agents-ia.pro · Directeur de publication : Laurent Duplat</span>
      </footer>
    </>
  )
}
