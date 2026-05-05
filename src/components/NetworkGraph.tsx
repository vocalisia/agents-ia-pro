'use client'

import { useRef, useEffect } from 'react'
import gsap from 'gsap'
import { useGSAP } from '@gsap/react'

gsap.registerPlugin(useGSAP)

interface Node {
  x: number
  y: number
  emoji: string
  r: number
  delay: number
  orbitRadius: number
  orbitSpeed: number
  orbitOffset: number
}

const CENTER = { x: 300, y: 300 }

const NODES: Node[] = [
  { x: 300, y: 80,  emoji: '🎙️', r: 38, delay: 0,    orbitRadius: 0,   orbitSpeed: 0,    orbitOffset: 0 },
  { x: 490, y: 140, emoji: '💰', r: 34, delay: 0.15, orbitRadius: 6,   orbitSpeed: 4.2,  orbitOffset: 0 },
  { x: 520, y: 300, emoji: '📊', r: 36, delay: 0.3,  orbitRadius: 8,   orbitSpeed: 5.8,  orbitOffset: 1.2 },
  { x: 490, y: 460, emoji: '⚖️', r: 34, delay: 0.45, orbitRadius: 5,   orbitSpeed: 4.8,  orbitOffset: 2.4 },
  { x: 300, y: 520, emoji: '💬', r: 38, delay: 0.6,  orbitRadius: 0,   orbitSpeed: 0,    orbitOffset: 0 },
  { x: 110, y: 460, emoji: '👥', r: 34, delay: 0.75, orbitRadius: 7,   orbitSpeed: 6.1,  orbitOffset: 3.6 },
  { x: 80,  y: 300, emoji: '🛡️', r: 36, delay: 0.9,  orbitRadius: 6,   orbitSpeed: 4.5,  orbitOffset: 0.8 },
  { x: 110, y: 140, emoji: '📧', r: 34, delay: 1.05, orbitRadius: 5,   orbitSpeed: 5.2,  orbitOffset: 2.1 },
]

export default function NetworkGraph() {
  const svgRef = useRef<SVGSVGElement>(null)
  const nodeRefs = useRef<SVGGElement[]>([])
  const lineRefs = useRef<SVGLineElement[]>([])
  const coreRef = useRef<SVGCircleElement>(null)
  const glowRef = useRef<SVGCircleElement>(null)
  const orbit1Ref = useRef<SVGCircleElement>(null)
  const orbit2Ref = useRef<SVGCircleElement>(null)

  // Store base positions for floating animation
  const basePositions = useRef(NODES.map(n => ({ x: n.x, y: n.y })))

  useGSAP(() => {
    // Entrance: fade in SVG
    gsap.from(svgRef.current, { opacity: 0, duration: 1, ease: 'power2.out' })

    // Core pulse
    gsap.to(glowRef.current, {
      r: 82,
      opacity: 0.8,
      duration: 2.4,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    })

    gsap.to(coreRef.current, {
      r: 62,
      duration: 3.1,
      repeat: -1,
      yoyo: true,
      ease: 'sine.inOut',
    })

    // Orbit rings rotation
    gsap.to(orbit1Ref.current, {
      rotation: 360,
      svgOrigin: '300 300',
      duration: 28,
      repeat: -1,
      ease: 'none',
    })

    gsap.to(orbit2Ref.current, {
      rotation: -360,
      svgOrigin: '300 300',
      duration: 44,
      repeat: -1,
      ease: 'none',
    })

    // Node entrance + float
    nodeRefs.current.forEach((node, i) => {
      if (!node) return
      const n = NODES[i]

      // Entrance
      gsap.from(node, {
        opacity: 0,
        scale: 0,
        transformOrigin: `${n.x}px ${n.y}px`,
        duration: 0.6,
        delay: 0.3 + n.delay,
        ease: 'back.out(1.7)',
      })

      // Float animation per node (unique rhythm)
      gsap.to(node, {
        y: `+=${8 + i * 2}`,
        x: `+=${(i % 2 === 0 ? 1 : -1) * (4 + i)}`,
        duration: 3 + i * 0.4,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: n.delay,
      })
    })

    // Lines: pulse opacity
    lineRefs.current.forEach((line, i) => {
      if (!line) return
      gsap.fromTo(
        line,
        { opacity: 0 },
        {
          opacity: 0.35,
          duration: 0.5,
          delay: 0.6 + NODES[i].delay,
          ease: 'power2.out',
        }
      )
      gsap.to(line, {
        opacity: 0.15,
        duration: 2.2 + i * 0.3,
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        delay: 1 + NODES[i].delay,
      })
    })
  }, { scope: svgRef })

  return (
    <svg
      ref={svgRef}
      viewBox="0 0 600 600"
      xmlns="http://www.w3.org/2000/svg"
      style={{
        width: '100%',
        height: 'auto',
        filter: 'drop-shadow(0 30px 80px rgba(99,102,241,0.3))',
      }}
    >
      <defs>
        <linearGradient id="hg1" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#6366f1" />
          <stop offset="1" stopColor="#a855f7" />
        </linearGradient>
        <linearGradient id="hg2" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stopColor="#a855f7" />
          <stop offset="1" stopColor="#ec4899" />
        </linearGradient>
        <linearGradient id="hg3" x1="0" y1="0" x2="1" y2="0">
          <stop offset="0" stopColor="#6366f1" />
          <stop offset="1" stopColor="#ec4899" />
        </linearGradient>
        <radialGradient id="hcore" cx="0.5" cy="0.5">
          <stop offset="0" stopColor="#a78bfa" />
          <stop offset="1" stopColor="#4c1d95" />
        </radialGradient>
        <filter id="hglow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="12" />
        </filter>
        <filter id="nodeGlow" x="-50%" y="-50%" width="200%" height="200%">
          <feGaussianBlur stdDeviation="4" />
        </filter>
      </defs>

      {/* Connection lines */}
      {NODES.map((n, i) => (
        <line
          key={`line-${i}`}
          ref={el => { if (el) lineRefs.current[i] = el }}
          x1={CENTER.x}
          y1={CENTER.y}
          x2={n.x}
          y2={n.y}
          stroke="url(#hg3)"
          strokeWidth="1.5"
          opacity="0"
        />
      ))}

      {/* Orbit rings */}
      <circle
        ref={orbit1Ref}
        cx="300"
        cy="300"
        r="200"
        fill="none"
        stroke="url(#hg1)"
        strokeWidth="1"
        opacity="0.3"
        strokeDasharray="4 6"
      />
      <circle
        ref={orbit2Ref}
        cx="300"
        cy="300"
        r="260"
        fill="none"
        stroke="url(#hg1)"
        strokeWidth="0.6"
        opacity="0.18"
        strokeDasharray="2 8"
      />

      {/* Satellite nodes */}
      {NODES.map((n, i) => (
        <g
          key={`node-${i}`}
          ref={el => { if (el) nodeRefs.current[i] = el }}
        >
          {/* glow behind node */}
          <circle
            cx={n.x}
            cy={n.y}
            r={n.r + 10}
            fill={i % 2 === 0 ? '#6366f1' : '#a855f7'}
            opacity="0.15"
            filter="url(#nodeGlow)"
          />
          <circle
            cx={n.x}
            cy={n.y}
            r={n.r}
            fill="#0f0f1a"
            stroke={i % 2 === 0 ? 'url(#hg1)' : 'url(#hg2)'}
            strokeWidth="2"
          />
          <text
            x={n.x}
            y={n.y + 7}
            fontFamily="Inter,sans-serif"
            fontSize={n.r * 0.65}
            textAnchor="middle"
          >
            {n.emoji}
          </text>
        </g>
      ))}

      {/* Core glow */}
      <circle
        ref={glowRef}
        cx="300"
        cy="300"
        r="72"
        fill="url(#hcore)"
        filter="url(#hglow)"
        opacity="0.6"
      />

      {/* Core node */}
      <circle
        ref={coreRef}
        cx="300"
        cy="300"
        r="58"
        fill="#0f0f1a"
        stroke="url(#hg3)"
        strokeWidth="3"
      />

      {/* A icon inside core */}
      <path
        d="M300 258 L337 280 L337 320 L300 342 L263 320 L263 280 Z"
        fill="rgba(139,92,246,0.35)"
        stroke="url(#hg3)"
        strokeWidth="2"
      />
      <path
        d="M282 324 L300 280 L318 324 M290 310 L310 310"
        stroke="white"
        strokeWidth="2.6"
        strokeLinecap="round"
        strokeLinejoin="round"
        fill="none"
      />
      <circle cx="300" cy="278" r="3.5" fill="#ec4899" />
    </svg>
  )
}
