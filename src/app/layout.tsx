import type { Metadata } from 'next'
import { SpeedInsights } from '@vercel/speed-insights/next'
import { Inter } from 'next/font/google'
import dynamic from 'next/dynamic'
import './globals.css'

// Self-hosted Inter via next/font/google — eliminates Google Fonts render-blocking (~825ms)
// display:swap + automatic preload + zero layout shift
const inter = Inter({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700', '800', '900'],
  display: 'swap',
  preload: true,
  variable: '--font-inter',
})

// Cookie banner is not above-fold — deferred to reduce initial JS
const CookieBanner = dynamic(() => import('@/components/CookieBanner'), {
  ssr: false,
  loading: () => null,
})

export const metadata: Metadata = {
  metadataBase: new URL('https://agents-ia.pro'),
  title: {
    default: 'Agents IA Pro — Agent Chatbot, Code & Automation | Marketplace #1',
    template: '%s | Agents-IA.pro',
  },
  description:
    'Agents-IA.pro : marketplace +500 agents IA vérifiés — agent chatbot, agent code, agent pro, agent support. Trouvez et déployez l\'agent IA parfait pour votre entreprise.',
  robots: { index: true, follow: true },
  alternates: {
    canonical: 'https://agents-ia.pro/',
    languages: {
      fr: 'https://agents-ia.pro/',
      en: 'https://agents-ia.pro/en/',
      de: 'https://agents-ia.pro/de/',
      nl: 'https://agents-ia.pro/nl/',
    },
  },
  openGraph: {
    type: 'website',
    siteName: 'Agents-IA.pro',
    locale: 'fr_FR',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    images: ['/og-image.png'],
  },
  icons: { icon: '/favicon.svg' },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const GA_ID = 'G-B5627RD3TF'

  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    '@id': 'https://agents-ia.pro/#organization',
    name: 'Agents-IA.pro',
    url: 'https://agents-ia.pro',
    logo: 'https://agents-ia.pro/favicon.svg',
    description:
      'La marketplace #1 d\'agents IA francophones pour automatiser votre entreprise.',
    foundingDate: '2024',
    founder: { '@id': 'https://agents-ia.pro/#founder' },
    address: { '@type': 'PostalAddress', addressCountry: 'CH' },
    contactPoint: {
      '@type': 'ContactPoint',
      contactType: 'sales',
      email: 'contact@vocalis.pro',
      url: 'https://agents-ia.pro/#contact',
      availableLanguage: ['fr', 'en', 'de', 'nl'],
    },
  }

  const founderSchema = {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': 'https://agents-ia.pro/#founder',
    name: 'Laurent Duplat',
    jobTitle: 'Fondateur & Directeur de publication',
    worksFor: { '@id': 'https://agents-ia.pro/#organization' },
    url: 'https://agents-ia.pro/a-propos',
    email: 'contact@vocalis.pro',
    knowsAbout: [
      'Intelligence artificielle',
      'Agents vocaux IA',
      'Automatisation business',
      'SEO et GEO',
      'Marketing IA',
    ],
    knowsLanguage: ['fr', 'en', 'de'],
    nationality: { '@type': 'Country', name: 'Suisse' },
    sameAs: ['https://vocalis.pro', 'https://master-seller.fr'],
  }

  return (
    <html lang="fr" className={inter.variable}>
      <head>
        {/* Preconnect for tiers tiers used post-paint (GA, FA CDN) */}
        <link rel="preconnect" href="https://www.googletagmanager.com" />
        <link rel="dns-prefetch" href="https://cdnjs.cloudflare.com" />

        {/* Font Awesome — async via media-print trick (no longer render-blocking)
            Saves ~947ms render-blocking time. Icons appear progressively after first paint.
            We inject raw HTML so the onload handler is in the SSR markup (React strips string handlers). */}
        <link
          rel="preload"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
          as="style"
        />
        <script
          dangerouslySetInnerHTML={{
            __html: `(function(){var l=document.createElement('link');l.rel='stylesheet';l.href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css';l.media='print';l.onload=function(){this.media='all'};document.head.appendChild(l);})();`,
          }}
        />
        <noscript>
          <link
            rel="stylesheet"
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
          />
        </noscript>

        {/* ⚠️ GA4 CONSENT — VERROUILLÉ — NE PAS MODIFIER
             OPT-OUT pattern: rejected→denied, sinon granted.
             INTERDIT de passer analytics_storage à 'denied' par défaut.
             Bug historique 2026-05-16/23 : opt-in = 0 connexions GA4 pendant 1 semaine. */}
        <script
          dangerouslySetInnerHTML={{
            __html: `
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
window.gtag = gtag;
var _c = (typeof localStorage !== 'undefined') ? localStorage.getItem('ai_cookies') : null;
gtag('consent', 'default', { analytics_storage: _c === 'rejected' ? 'denied' : 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied', wait_for_update: 500 });
(function(){var s=document.createElement('script');s.async=true;s.src='https://www.googletagmanager.com/gtag/js?id=${GA_ID}';document.head.appendChild(s);})();
gtag('js', new Date());
gtag('config', '${GA_ID}');`,
          }}
        />

        {/* Organization + Founder schema */}
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
        />
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(founderSchema) }}
        />
      </head>
      <body className={inter.className}>
        {children}
        <CookieBanner />
        <SpeedInsights />
      </body>
    </html>
  )
}
