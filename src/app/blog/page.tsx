import type { Metadata } from 'next'
import Link from 'next/link'
import Navbar from '@/components/Navbar'
import { getAllPosts, formatDate } from '@/lib/mdx'

export const metadata: Metadata = {
  title: 'Blog IA | Agents-IA.pro',
  description:
    'Actualités, guides et conseils sur les agents IA, l\'automatisation et l\'intelligence artificielle pour les entreprises.',
  alternates: { canonical: 'https://agents-ia.pro/blog' },
  openGraph: {
    title: 'Blog IA | Agents-IA.pro',
    description:
      'Guides, tendances et analyses sur les agents IA pour PME francophones.',
    url: 'https://agents-ia.pro/blog',
    type: 'website',
  },
}

const blogListSchema = {
  '@context': 'https://schema.org',
  '@type': 'Blog',
  name: 'Blog Agents-IA.pro',
  url: 'https://agents-ia.pro/blog',
  description: 'Guides et analyses sur les agents IA pour les entreprises.',
  publisher: {
    '@id': 'https://agents-ia.pro/#organization',
  },
  author: {
    '@id': 'https://agents-ia.pro/#founder',
  },
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
  ],
}

export default function BlogPage() {
  const posts = getAllPosts()

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(blogListSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      <Navbar />

      <main style={{ paddingTop: 100 }}>
        {/* Header */}
        <section
          style={{
            padding: '60px 0 80px',
            position: 'relative',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              position: 'absolute',
              inset: 0,
              background:
                'radial-gradient(600px 300px at 50% 0%,rgba(99,102,241,0.12),transparent 60%)',
              zIndex: -1,
            }}
          />
          <div className="mx-auto px-6 text-center" style={{ maxWidth: 800 }}>
            {/* Breadcrumb */}
            <nav
              aria-label="Fil d'Ariane"
              style={{
                display: 'flex',
                justifyContent: 'center',
                gap: 8,
                alignItems: 'center',
                marginBottom: 32,
                fontSize: 13,
                color: '#64748b',
              }}
            >
              <Link href="/" style={{ color: '#818cf8', textDecoration: 'none' }}>
                Accueil
              </Link>
              <i className="fas fa-chevron-right" style={{ fontSize: 10 }} />
              <span style={{ color: 'white' }}>Blog</span>
            </nav>

            <h1
              style={{
                fontSize: 'clamp(32px,5vw,56px)',
                fontWeight: 900,
                color: 'white',
                marginBottom: 16,
                letterSpacing: '-1px',
              }}
            >
              Blog{' '}
              <span
                style={{
                  background: 'linear-gradient(90deg,#818cf8,#c084fc,#f472b6)',
                  WebkitBackgroundClip: 'text',
                  backgroundClip: 'text',
                  color: 'transparent',
                }}
              >
                Agents IA
              </span>
            </h1>
            <p style={{ color: '#94a3b8', fontSize: 18, lineHeight: 1.6 }}>
              Guides, analyses et tendances sur les agents IA pour les entreprises francophones.
              <br />
              Par <strong style={{ color: 'white' }}>Laurent Duplat</strong>.
            </p>
          </div>
        </section>

        {/* Posts grid */}
        <section style={{ padding: '0 0 100px' }}>
          <div className="mx-auto px-6" style={{ maxWidth: 1280 }}>
            {posts.length === 0 ? (
              <div
                style={{
                  textAlign: 'center',
                  padding: '60px 0',
                  color: '#64748b',
                }}
              >
                <i
                  className="fas fa-pen-to-square"
                  style={{ fontSize: 48, marginBottom: 16, display: 'block' }}
                />
                <p>Aucun article pour l&apos;instant. Revenez bientôt.</p>
              </div>
            ) : (
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fill,minmax(320px,1fr))',
                  gap: 28,
                }}
              >
                {posts.map((post) => (
                  <Link
                    key={post.slug}
                    href={`/blog/${post.slug}`}
                    style={{
                      display: 'flex',
                      flexDirection: 'column',
                      background: 'rgba(255,255,255,0.03)',
                      border: '1px solid rgba(255,255,255,0.08)',
                      borderRadius: 20,
                      overflow: 'hidden',
                      textDecoration: 'none',
                    }}
                  >
                    {/* Top accent bar */}
                    <div
                      style={{
                        height: 3,
                        background: 'linear-gradient(90deg,#6366f1,#a855f7,#ec4899)',
                      }}
                    />

                    <div
                      style={{
                        padding: '28px 28px 20px',
                        display: 'flex',
                        flexDirection: 'column',
                        gap: 14,
                        flex: 1,
                      }}
                    >
                      <span
                        style={{
                          display: 'inline-block',
                          padding: '3px 12px',
                          background: 'rgba(99,102,241,0.15)',
                          color: '#818cf8',
                          borderRadius: 999,
                          fontSize: 11,
                          fontWeight: 700,
                          letterSpacing: '0.8px',
                          textTransform: 'uppercase',
                          width: 'fit-content',
                        }}
                      >
                        {post.category}
                      </span>

                      <h2
                        style={{
                          fontSize: 18,
                          fontWeight: 700,
                          color: 'white',
                          lineHeight: 1.35,
                          margin: 0,
                        }}
                      >
                        {post.title}
                      </h2>

                      <p
                        style={{
                          fontSize: 14,
                          color: '#94a3b8',
                          lineHeight: 1.6,
                          margin: 0,
                          flex: 1,
                        }}
                      >
                        {post.description}
                      </p>
                    </div>

                    <div
                      style={{
                        padding: '14px 28px',
                        borderTop: '1px solid rgba(255,255,255,0.06)',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        fontSize: 12,
                        color: '#64748b',
                      }}
                    >
                      <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <i className="fas fa-user-circle" />
                        {post.author}
                      </span>
                      <span style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                        <span>{formatDate(post.date)}</span>
                        <span
                          style={{
                            padding: '2px 8px',
                            background: 'rgba(255,255,255,0.05)',
                            borderRadius: 999,
                          }}
                        >
                          {post.readTime}
                        </span>
                      </span>
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer
        style={{
          padding: '40px 0 24px',
          borderTop: '1px solid rgba(255,255,255,0.08)',
          textAlign: 'center',
          fontSize: 13,
          color: '#64748b',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 1280 }}>
          <span>© {new Date().getFullYear()} agents-ia.pro · Directeur de publication : Laurent Duplat</span>
        </div>
      </footer>
    </>
  )
}
