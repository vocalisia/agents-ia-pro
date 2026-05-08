import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: '#6366f1',
        'primary-dark': '#4f46e5',
        'primary-light': '#818cf8',
        accent: '#a855f7',
        'accent-pink': '#ec4899',
        dark: '#0F0F23',
        'dark-2': '#1A1A3E',
        'dark-3': '#252550',
        'dark-card': 'rgba(255,255,255,0.03)',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      backgroundImage: {
        'gradient-brand': 'linear-gradient(90deg, #6366f1, #a855f7)',
        'gradient-brand-pink': 'linear-gradient(90deg, #818cf8, #c084fc, #f472b6)',
      },
    },
  },
  plugins: [],
}

export default config
