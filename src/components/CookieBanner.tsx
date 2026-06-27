'use client'

import { useState, useEffect } from 'react'

const COOKIE_KEY = 'ai_cookies'

export default function CookieBanner() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const id = window.setTimeout(() => {
      const consent = localStorage.getItem(COOKIE_KEY)
      if (consent !== 'accepted' && consent !== 'rejected') {
        setVisible(true)
      }
    }, 800)
    return () => window.clearTimeout(id)
  }, [])

  function updateConsent(granted: boolean) {
    if (typeof window !== 'undefined' && typeof (window as unknown as { gtag?: (...a: unknown[]) => void }).gtag === 'function') {
      ;(window as unknown as { gtag: (...a: unknown[]) => void }).gtag('consent', 'update', {
        analytics_storage: granted ? 'granted' : 'denied',
        ad_storage: 'denied',
        ad_user_data: 'denied',
        ad_personalization: 'denied',
      })
    }
  }

  function handleAccept() {
    localStorage.setItem(COOKIE_KEY, 'accepted')
    updateConsent(true)
    setVisible(false)
  }

  function handleRefuse() {
    localStorage.setItem(COOKIE_KEY, 'rejected')
    updateConsent(false)
    setVisible(false)
  }

  if (!visible) return null

  return (
    <div
      style={{
        position: 'fixed',
        bottom: 0,
        left: 0,
        right: 0,
        zIndex: 9999,
        background: 'rgba(10,12,26,0.97)',
        borderTop: '1px solid rgba(255,255,255,0.08)',
        padding: '16px 24px',
        backdropFilter: 'blur(12px)',
      }}
    >
      <div
        style={{
          maxWidth: 1200,
          margin: '0 auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: 20,
          flexWrap: 'wrap',
        }}
      >
        <p style={{ margin: 0, fontSize: 14, color: '#94a3b8', flex: '1 1 300px', lineHeight: 1.5 }}>
          Nous utilisons des cookies pour analyser le trafic et améliorer votre expérience.{' '}
          <a href="/confidentialite" style={{ color: '#818cf8', textDecoration: 'underline' }}>
            En savoir plus
          </a>
        </p>
        <div style={{ display: 'flex', gap: 10, flexShrink: 0 }}>
          <button
            onClick={handleRefuse}
            style={{
              padding: '9px 18px',
              fontSize: 13,
              fontWeight: 500,
              borderRadius: 8,
              border: '1px solid rgba(255,255,255,0.12)',
              background: 'transparent',
              color: '#94a3b8',
              cursor: 'pointer',
            }}
          >
            Refuser
          </button>
          <button
            onClick={handleAccept}
            style={{
              padding: '9px 18px',
              fontSize: 13,
              fontWeight: 600,
              borderRadius: 8,
              border: 'none',
              background: 'linear-gradient(90deg,#6366f1,#a855f7)',
              color: 'white',
              cursor: 'pointer',
            }}
          >
            Accepter
          </button>
        </div>
      </div>
    </div>
  )
}
