import type { Metadata } from 'next'
import Navbar from '@/components/Navbar'
import Link from 'next/link'
import { getAllPosts, formatDate } from '@/lib/mdx'
import dynamic from 'next/dynamic'

const NetworkGraph = dynamic(() => import('@/components/NetworkGraph'), { ssr: false })

export const metadata: Metadata = {
  title: "Agents-IA.pro | La Marketplace #1 d'Agents IA Francophones",
  description:
    "La marketplace #1 d'agents IA francophones. Trouvez, comparez et déployez +500 agents IA vérifiés pour automatiser votre entreprise. 98% de satisfaction, 12 840+ utilisateurs.",
  alternates: { canonical: 'https://agents-ia.pro/' },
  openGraph: {
    title: "Agents-IA.pro | La Marketplace #1 d'Agents IA Francophones",
    description:
      'Trouvez, comparez et déployez les meilleurs agents IA pour votre business.',
    url: 'https://agents-ia.pro/',
    type: 'website',
  },
}

// Website schema
const websiteSchema = {
  '@context': 'https://schema.org',
  '@type': 'WebSite',
  name: 'Agents IA Pro',
  url: 'https://agents-ia.pro',
  potentialAction: {
    '@type': 'SearchAction',
    target: 'https://agents-ia.pro/?s={search_term_string}',
    'query-input': 'required name=search_term_string',
  },
}

const featuredAgents = [
  {
    id: 1,
    badge: '#1 Vocal',
    name: 'Vocalis AI',
    creator: 'par Vocalis.pro',
    desc: 'Agent vocal IA qui gère vos appels téléphoniques 24/7. Prise de RDV, qualification de leads, support client automatisé.',
    tags: ['Vocal', 'Téléphone', 'Autonome'],
    rating: 4.9,
    users: '2.4K',
    price: 'Essai gratuit',
    priceClass: 'free',
    upvotes: 847,
    href: 'https://vocalis.pro',
    gradient: 'linear-gradient(135deg,#667eea,#764ba2)',
    icon: 'fa-phone-volume',
  },
  {
    id: 2,
    badge: '#1 Vente',
    name: 'Master Seller AI',
    creator: 'par Master-Seller.fr',
    desc: "Agent IA de vente qui analyse vos prospects, génère des scripts de vente personnalisés et automatise votre closing.",
    tags: ['Vente', 'Analytics', 'Closing'],
    rating: 4.8,
    users: '1.8K',
    price: 'Dès 49 CHF/mois',
    priceClass: 'paid',
    upvotes: 623,
    href: 'https://master-seller.fr',
    gradient: 'linear-gradient(135deg,#f093fb,#f5576c)',
    icon: 'fa-hand-holding-dollar',
  },
  {
    id: 3,
    badge: '#1 Confiance',
    name: 'Trust Vault AI',
    creator: 'par Trust-Vault.com',
    desc: "Agent IA qui vérifie la fiabilité des entreprises, collecte des avis vérifiés et génère des rapports de confiance.",
    tags: ['Sécurité', 'Avis', 'Rapports'],
    rating: 4.9,
    users: '1.2K',
    price: 'Gratuit',
    priceClass: 'free',
    upvotes: 512,
    href: 'https://trust-vault.com',
    gradient: 'linear-gradient(135deg,#4facfe,#00f2fe)',
    icon: 'fa-shield-halved',
  },
]

export default function HomePage() {
  const recentPosts = getAllPosts().slice(0, 3)

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
      />
      <Navbar />

      {/* ===== HERO ===== */}
      <section
        style={{
          position: 'relative',
          padding: '140px 0 80px',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            position: 'absolute',
            inset: 0,
            background:
              'radial-gradient(800px 400px at 20% 30%,rgba(99,102,241,0.18),transparent 60%),radial-gradient(600px 400px at 85% 60%,rgba(236,72,153,0.15),transparent 60%),radial-gradient(500px 300px at 50% 100%,rgba(168,85,247,0.12),transparent 60%)',
            zIndex: -1,
          }}
        />
        <div
          style={{
            position: 'absolute',
            inset: 0,
            backgroundImage:
              'linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px)',
            backgroundSize: '48px 48px',
            zIndex: -1,
            opacity: 0.6,
          }}
        />

        <div
          className="mx-auto px-6"
          style={{ maxWidth: 1200, display: 'grid', gridTemplateColumns: '1.1fr 1fr', gap: 60, alignItems: 'center' }}
        >
          <div>
            <div
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 8,
                padding: '7px 14px',
                background: 'rgba(255,255,255,0.06)',
                border: '1px solid rgba(255,255,255,0.1)',
                borderRadius: 999,
                fontSize: 13,
                color: '#e0e7ff',
                marginBottom: 24,
              }}
            >
              <span
                style={{
                  width: 8,
                  height: 8,
                  borderRadius: '50%',
                  background: '#10b981',
                  boxShadow: '0 0 0 4px rgba(16,185,129,0.2)',
                  flexShrink: 0,
                }}
              />
              +500 agents IA vérifiés · 12 840+ utilisateurs
            </div>

            <h1
              style={{
                fontSize: 'clamp(36px,5vw,64px)',
                fontWeight: 900,
                lineHeight: 1.05,
                letterSpacing: '-1.5px',
                margin: '0 0 24px',
                color: 'white',
              }}
            >
              Déployez un{' '}
              <em
                style={{
                  fontStyle: 'normal',
                  background: 'linear-gradient(90deg,#818cf8,#c084fc,#f472b6)',
                  WebkitBackgroundClip: 'text',
                  backgroundClip: 'text',
                  color: 'transparent',
                }}
              >
                agent IA
              </em>
              <br />
              qui bosse pour votre PME
              <br />
              en moins de 30 jours.
            </h1>

            <p
              style={{
                fontSize: 18,
                color: '#cbd5e1',
                lineHeight: 1.6,
                marginBottom: 32,
                maxWidth: 560,
              }}
            >
              Comparez, testez et activez les meilleurs agents IA francophones.
              Sans commission, sans engagement, avec le support d&apos;une équipe basée en Suisse.
            </p>

            <div style={{ display: 'flex', gap: 12, flexWrap: 'wrap', marginBottom: 32 }}>
              <a
                href="#explorer"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '15px 28px',
                  background: 'linear-gradient(90deg,#6366f1,#a855f7)',
                  color: 'white',
                  fontWeight: 600,
                  borderRadius: 12,
                  textDecoration: 'none',
                  fontSize: 15,
                  boxShadow: '0 10px 30px rgba(99,102,241,0.3)',
                }}
              >
                Explorer les 500+ agents <i className="fas fa-arrow-right" />
              </a>
              <Link
                href="/agence.html"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '15px 24px',
                  background: 'rgba(255,255,255,0.05)',
                  border: '1px solid rgba(255,255,255,0.15)',
                  color: 'white',
                  fontWeight: 600,
                  borderRadius: 12,
                  textDecoration: 'none',
                  fontSize: 15,
                }}
              >
                <i className="fas fa-calendar-check" /> Audit gratuit 30 min
              </Link>
            </div>

            <div
              style={{
                display: 'flex',
                gap: 28,
                flexWrap: 'wrap',
                paddingTop: 24,
                borderTop: '1px solid rgba(255,255,255,0.08)',
              }}
            >
              {[
                { big: '500+', label: 'agents' },
                { big: '4', label: 'langues' },
                { big: '🇨🇭', label: 'Basé en Suisse' },
                { big: '0%', label: 'commission' },
              ].map((s) => (
                <div key={s.label} style={{ display: 'flex', alignItems: 'center', gap: 8, color: '#cbd5e1', fontSize: 13 }}>
                  <span style={{ fontSize: 22, fontWeight: 800, color: 'white' }}>{s.big}</span> {s.label}
                </div>
              ))}
            </div>
          </div>

          {/* Hero visual — animated GSAP network */}
          <div style={{ position: 'relative', aspectRatio: '1/1', maxWidth: 520, marginLeft: 'auto' }}>
            <NetworkGraph />
          </div>
        </div>
      </section>

      {/* ===== FEATURED AGENTS ===== */}
      <section
        id="explorer"
        style={{
          padding: '100px 0',
          background: 'rgba(255,255,255,0.02)',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 1280 }}>
          <div style={{ textAlign: 'center', marginBottom: 56 }}>
            <h2 style={{ fontSize: 36, fontWeight: 800, color: 'white', marginBottom: 12 }}>
              <i className="fas fa-star" style={{ color: '#f59e0b', marginRight: 10 }} />
              Agents IA Featured
            </h2>
            <p style={{ color: '#94a3b8', fontSize: 16 }}>Sélectionnés et vérifiés par notre équipe</p>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill,minmax(320px,1fr))',
              gap: 24,
            }}
          >
            {featuredAgents.map((agent) => (
              <div
                key={agent.id}
                style={{
                  background: 'rgba(255,255,255,0.04)',
                  border: '1px solid rgba(255,255,255,0.1)',
                  borderRadius: 20,
                  padding: 28,
                  display: 'flex',
                  flexDirection: 'column',
                  gap: 16,
                  position: 'relative',
                }}
              >
                <span
                  style={{
                    position: 'absolute',
                    top: 16,
                    right: 16,
                    background: 'linear-gradient(90deg,#f59e0b,#f97316)',
                    color: 'white',
                    fontSize: 11,
                    fontWeight: 700,
                    padding: '4px 10px',
                    borderRadius: 999,
                    letterSpacing: '0.5px',
                  }}
                >
                  <i className="fas fa-trophy" style={{ marginRight: 4 }} />
                  {agent.badge}
                </span>

                <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
                  <div
                    style={{
                      width: 52,
                      height: 52,
                      borderRadius: 14,
                      background: agent.gradient,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontSize: 22,
                      flexShrink: 0,
                    }}
                  >
                    <i className={`fas ${agent.icon}`} style={{ color: 'white' }} />
                  </div>
                  <div>
                    <div style={{ fontWeight: 700, fontSize: 17, color: 'white' }}>{agent.name}</div>
                    <div style={{ fontSize: 12, color: '#94a3b8' }}>{agent.creator}</div>
                  </div>
                  <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: 4, color: '#10b981', fontSize: 12, fontWeight: 600 }}>
                    <i className="fas fa-check-circle" /> Vérifié
                  </div>
                </div>

                <p style={{ fontSize: 14, color: '#94a3b8', lineHeight: 1.6, margin: 0 }}>{agent.desc}</p>

                <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
                  {agent.tags.map((t) => (
                    <span
                      key={t}
                      style={{
                        padding: '4px 12px',
                        background: 'rgba(99,102,241,0.12)',
                        border: '1px solid rgba(99,102,241,0.3)',
                        borderRadius: 999,
                        fontSize: 12,
                        color: '#818cf8',
                        fontWeight: 500,
                      }}
                    >
                      {t}
                    </span>
                  ))}
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: 16, fontSize: 13, color: '#94a3b8' }}>
                  <span><i className="fas fa-star" style={{ color: '#f59e0b', marginRight: 4 }} />{agent.rating}</span>
                  <span><i className="fas fa-users" style={{ marginRight: 4 }} />{agent.users}</span>
                  <span
                    style={{
                      marginLeft: 'auto',
                      padding: '4px 12px',
                      borderRadius: 999,
                      fontSize: 12,
                      fontWeight: 700,
                      background: agent.priceClass === 'free' ? 'rgba(16,185,129,0.15)' : 'rgba(99,102,241,0.15)',
                      color: agent.priceClass === 'free' ? '#10b981' : '#818cf8',
                    }}
                  >
                    {agent.price}
                  </span>
                </div>

                <div style={{ display: 'flex', gap: 10, marginTop: 4 }}>
                  <button
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 6,
                      padding: '8px 16px',
                      background: 'rgba(255,255,255,0.05)',
                      border: '1px solid rgba(255,255,255,0.1)',
                      borderRadius: 10,
                      color: 'white',
                      fontSize: 13,
                      fontWeight: 600,
                      cursor: 'pointer',
                    }}
                  >
                    <i className="fas fa-arrow-up" /> {agent.upvotes}
                  </button>
                  <a
                    href={agent.href}
                    target="_blank"
                    rel="nofollow noopener"
                    style={{
                      flex: 1,
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: 8,
                      padding: '8px 16px',
                      background: 'linear-gradient(90deg,#6366f1,#a855f7)',
                      borderRadius: 10,
                      color: 'white',
                      textDecoration: 'none',
                      fontSize: 14,
                      fontWeight: 600,
                    }}
                  >
                    Essayer <i className="fas fa-arrow-right" />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ===== BLOG PREVIEW ===== */}
      {recentPosts.length > 0 && (
        <section style={{ padding: '100px 0' }}>
          <div className="mx-auto px-6" style={{ maxWidth: 1280 }}>
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: 48,
                flexWrap: 'wrap',
                gap: 16,
              }}
            >
              <div>
                <h2 style={{ fontSize: 32, fontWeight: 800, color: 'white', marginBottom: 8 }}>
                  Derniers articles
                </h2>
                <p style={{ color: '#94a3b8' }}>Guides, tendances et analyses IA</p>
              </div>
              <Link
                href="/blog"
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: 8,
                  padding: '10px 22px',
                  background: 'rgba(99,102,241,0.15)',
                  border: '1px solid rgba(99,102,241,0.3)',
                  borderRadius: 12,
                  color: '#818cf8',
                  textDecoration: 'none',
                  fontSize: 14,
                  fontWeight: 600,
                }}
              >
                Voir tous les articles <i className="fas fa-arrow-right" />
              </Link>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fill,minmax(300px,1fr))',
                gap: 24,
              }}
            >
              {recentPosts.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  style={{
                    display: 'flex',
                    flexDirection: 'column',
                    background: 'rgba(255,255,255,0.03)',
                    border: '1px solid rgba(255,255,255,0.08)',
                    borderRadius: 16,
                    overflow: 'hidden',
                    textDecoration: 'none',
                    transition: 'border-color 0.2s',
                  }}
                >
                  <div
                    style={{
                      padding: '24px 24px 20px',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: 12,
                      flex: 1,
                    }}
                  >
                    <span
                      style={{
                        display: 'inline-block',
                        padding: '3px 10px',
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
                    <h3
                      style={{
                        fontSize: 16,
                        fontWeight: 700,
                        color: 'white',
                        lineHeight: 1.4,
                        margin: 0,
                      }}
                    >
                      {post.title}
                    </h3>
                    <p style={{ fontSize: 14, color: '#94a3b8', lineHeight: 1.5, margin: 0 }}>
                      {post.description}
                    </p>
                  </div>
                  <div
                    style={{
                      padding: '12px 24px',
                      borderTop: '1px solid rgba(255,255,255,0.06)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontSize: 12,
                      color: '#64748b',
                    }}
                  >
                    <span>{formatDate(post.date)}</span>
                    <span>{post.readTime}</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ===== CTA CONTACT ===== */}
      <section
        id="contact"
        style={{
          padding: '100px 0',
          background:
            'linear-gradient(135deg,rgba(99,102,241,0.1),rgba(168,85,247,0.06))',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}
      >
        <div className="mx-auto px-6 text-center" style={{ maxWidth: 720 }}>
          <h2
            style={{
              fontSize: 'clamp(28px,4vw,48px)',
              fontWeight: 900,
              color: 'white',
              marginBottom: 20,
              letterSpacing: '-1px',
            }}
          >
            Prêt à déployer votre{' '}
            <span
              style={{
                background: 'linear-gradient(90deg,#6366f1,#ec4899)',
                WebkitBackgroundClip: 'text',
                backgroundClip: 'text',
                color: 'transparent',
              }}
            >
              premier agent IA
            </span>{' '}
            ?
          </h2>
          <p style={{ color: '#94a3b8', fontSize: 18, marginBottom: 36 }}>
            Audit gratuit 30 min avec un expert basé en Suisse. Aucun engagement.
          </p>
          <Link
            href="/agence.html"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 10,
              padding: '16px 36px',
              background: 'linear-gradient(90deg,#6366f1,#a855f7)',
              color: 'white',
              textDecoration: 'none',
              borderRadius: 14,
              fontSize: 16,
              fontWeight: 700,
              boxShadow: '0 14px 40px rgba(99,102,241,0.35)',
            }}
          >
            <i className="fas fa-calendar-check" /> Réserver mon audit gratuit
          </Link>
        </div>
      </section>

      {/* ===== FOOTER ===== */}
      <footer
        style={{
          padding: '60px 0 32px',
          borderTop: '1px solid rgba(255,255,255,0.08)',
        }}
      >
        <div className="mx-auto px-6" style={{ maxWidth: 1280 }}>
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill,minmax(200px,1fr))',
              gap: 40,
              marginBottom: 48,
            }}
          >
            <div>
              <div
                style={{
                  fontWeight: 800,
                  fontSize: 18,
                  color: 'white',
                  marginBottom: 12,
                }}
              >
                agents-ia
                <span
                  style={{
                    background: 'linear-gradient(90deg,#6366f1,#ec4899)',
                    WebkitBackgroundClip: 'text',
                    backgroundClip: 'text',
                    color: 'transparent',
                  }}
                >
                  .pro
                </span>
              </div>
              <p style={{ color: '#64748b', fontSize: 13, lineHeight: 1.6 }}>
                La marketplace #1 d&apos;agents IA francophones. Basée en Suisse.
              </p>
            </div>
            <div>
              <div style={{ fontWeight: 700, color: 'white', marginBottom: 16, fontSize: 13, letterSpacing: '0.5px' }}>
                RESSOURCES
              </div>
              {[
                { href: '/blog', label: 'Blog IA' },
                { href: '/categories.html', label: 'Catégories' },
                { href: '/rapports.html', label: 'Rapports' },
                { href: '/newsletter.html', label: 'Newsletter' },
              ].map((l) => (
                <Link
                  key={l.href}
                  href={l.href}
                  style={{ display: 'block', color: '#64748b', fontSize: 13, marginBottom: 8, textDecoration: 'none' }}
                >
                  {l.label}
                </Link>
              ))}
            </div>
            <div>
              <div style={{ fontWeight: 700, color: 'white', marginBottom: 16, fontSize: 13, letterSpacing: '0.5px' }}>
                ENTREPRISE
              </div>
              {[
                { href: '/a-propos.html', label: 'À propos' },
                { href: '/agence.html', label: 'Agence IA' },
                { href: '/editeurs.html', label: 'Éditeurs' },
                { href: '/contact.html', label: 'Contact' },
              ].map((l) => (
                <Link
                  key={l.href}
                  href={l.href}
                  style={{ display: 'block', color: '#64748b', fontSize: 13, marginBottom: 8, textDecoration: 'none' }}
                >
                  {l.label}
                </Link>
              ))}
            </div>
            <div>
              <div style={{ fontWeight: 700, color: 'white', marginBottom: 16, fontSize: 13, letterSpacing: '0.5px' }}>
                LÉGAL
              </div>
              {[
                { href: '/mentions-legales.html', label: 'Mentions légales' },
                { href: '/confidentialite.html', label: 'Confidentialité' },
                { href: '/cgu.html', label: 'CGU' },
              ].map((l) => (
                <Link
                  key={l.href}
                  href={l.href}
                  style={{ display: 'block', color: '#64748b', fontSize: 13, marginBottom: 8, textDecoration: 'none' }}
                >
                  {l.label}
                </Link>
              ))}
            </div>
          </div>

          <div
            style={{
              borderTop: '1px solid rgba(255,255,255,0.06)',
              paddingTop: 24,
              display: 'flex',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: 12,
              fontSize: 13,
              color: '#64748b',
            }}
          >
            <span>© {new Date().getFullYear()} agents-ia.pro — Tous droits réservés</span>
            <span>Directeur de publication : Laurent Duplat</span>
          </div>
        </div>
      </footer>
    </>
  )
}
