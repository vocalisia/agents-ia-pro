'use client'

import Link from 'next/link'

const LogoSVG = () => (
  <svg
    viewBox="0 0 40 40"
    xmlns="http://www.w3.org/2000/svg"
    style={{ width: 32, height: 32, verticalAlign: 'middle' }}
  >
    <defs>
      <linearGradient id="lg1nav" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stopColor="#6366f1" />
        <stop offset="0.5" stopColor="#8b5cf6" />
        <stop offset="1" stopColor="#ec4899" />
      </linearGradient>
    </defs>
    <path
      d="M20 3 L35 12 L35 28 L20 37 L5 28 L5 12 Z"
      fill="rgba(139,92,246,0.15)"
      stroke="url(#lg1nav)"
      strokeWidth="1.8"
    />
    <path
      d="M12 28 L20 12 L28 28 M15.5 22 L24.5 22"
      stroke="url(#lg1nav)"
      strokeWidth="2.4"
      strokeLinecap="round"
      strokeLinejoin="round"
      fill="none"
    />
    <circle cx="20" cy="12" r="2.2" fill="url(#lg1nav)" />
    <circle cx="12" cy="28" r="1.6" fill="#ec4899" />
    <circle cx="28" cy="28" r="1.6" fill="#6366f1" />
  </svg>
)

export default function Navbar() {
  return (
    <nav
      className="fixed top-0 left-0 right-0 z-50 py-4"
      style={{
        backdropFilter: 'blur(20px)',
        background: 'rgba(15,15,35,0.85)',
        borderBottom: '1px solid rgba(255,255,255,0.1)',
      }}
    >
      <div
        className="max-w-[1280px] mx-auto px-6 flex items-center justify-between"
      >
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 no-underline">
          <span className="flex items-center justify-center w-9 h-9">
            <LogoSVG />
          </span>
          <span
            className="font-extrabold text-white text-lg"
            style={{ letterSpacing: '-0.3px' }}
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
          </span>
        </Link>

        {/* Links */}
        <div className="hidden md:flex gap-8">
          {[
            { href: '/#explorer', label: 'Explorer' },
            { href: '/blog', label: 'Blog' },
            { href: '/agence.html', label: 'Agence' },
            { href: '/a-propos.html', label: 'À propos' },
          ].map((l) => (
            <Link
              key={l.href}
              href={l.href}
              className="text-[#8892b0] hover:text-white text-sm font-medium no-underline transition-colors"
            >
              {l.label}
            </Link>
          ))}
        </div>

        {/* CTA */}
        <div className="flex items-center gap-3">
          <Link
            href="/submit.html"
            className="hidden sm:flex items-center gap-2 px-5 py-2 rounded-full text-white text-sm font-semibold no-underline"
            style={{ background: '#6366f1' }}
          >
            + Soumettre
          </Link>
          <Link
            href="/agence.html"
            className="px-5 py-2 rounded-full text-white text-sm font-semibold no-underline border"
            style={{ borderColor: 'rgba(255,255,255,0.15)' }}
          >
            Audit gratuit
          </Link>
        </div>
      </div>
    </nav>
  )
}
