import type { Metadata } from 'next'
import { SpeedInsights } from '@vercel/speed-insights/next'
import './globals.css'
import CookieBanner from '@/components/CookieBanner'

export const metadata: Metadata = {
  metadataBase: new URL('https://agents-ia.pro'),
  title: {
    default: 'Agents-IA.pro | La Marketplace #1 d\'Agents IA Francophones',
    template: '%s | Agents-IA.pro',
  },
  description:
    'La marketplace #1 d\'agents IA francophones. Trouvez, comparez et déployez +500 agents IA vérifiés pour automatiser votre entreprise.',
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
    url: 'https://agents-ia.pro/a-propos.html',
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
    <html lang="fr">
      <head>
        {/* Google Fonts */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap"
          rel="stylesheet"
        />
        <link
          rel="stylesheet"
          href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css"
        />

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
      <body>
        {children}
        <CookieBanner />
        <SpeedInsights />
      </body>
    </html>
  )
}
