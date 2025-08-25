/** @type {import('tailwindcss').Config} */
import plugin from 'tailwindcss/plugin'
import typography from '@tailwindcss/typography'

export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],

  theme: {
    extend: {
      // Custom color palette inspired by Roman Events logo
      colors: {

        brand: {
          gold: '#d4af37',     // Main metallic gold
          goldLight: '#f5d879', // Highlighted gold (balloons shine)
          goldDark: '#b8860b',  // Deep antique gold
          black: '#0a0a0a',     // Background black
          gray: '#1a1a1a',      // Subtle gray for borders
        },

        // Primary color should be the cream background from logo
        primary: {
          50: '#fefdfb',
          100: '#fef7e7',     // Main cream background from logo
          200: '#fdefd0',
          300: '#fbe3a8',
          400: '#f8d280',
          500: '#f4c354',     // Primary cream color
          600: '#eab308',
          700: '#ca8a04',
          800: '#a16207',
          900: '#854d0e',
          950: '#422006',
        },

        // Orange as secondary (for accents like the Roman helmet)
        secondary: {
          50: '#fff7ed',
          100: '#ffedd5',
          200: '#fed7aa',
          300: '#fdba74',
          400: '#fb923c',
          500: '#f97316',     // Orange from Roman helmet
          600: '#ea580c',
          700: '#c2410c',
          800: '#9a3412',
          900: '#7c2d12',
          950: '#431407',
        },

        // Accent color based on the blue balloons
        accent: {
          red: '#e63946',
          blue: '#457b9d',
          teal: '#2a9d8f',
          cream: '#fefae0',
        },

        // Individual balloon colors for variety
        balloons: {
          red: '#ef4444',      // Red balloon
          orange: '#f97316',   // Orange balloon
          yellow: '#eab308',   // Yellow balloon
          green: '#22c55e',    // Green balloon
          blue: '#3b82f6',     // Blue balloon
          purple: '#8b5cf6',   // Purple balloon
          pink: '#ec4899',     // Pink balloon
          teal: '#14b8a6',     // Teal option
        },

        // Main cream background colors (matching logo exactly)
        cream: {
          50: '#fefdfb',
          100: '#fef7e7',     // Main cream background from logo
          200: '#fdefd0',
          300: '#fbe3a8',
          400: '#f8d280',
          500: '#f4c354',
          600: '#eab308',
          700: '#ca8a04',
          800: '#a16207',
          900: '#854d0e',
          950: '#422006',
        },

        // Updated neutral grays
        neutral: {
          50: '#fafafa',
          100: '#f5f5f5',
          200: '#e5e5e5',
          300: '#d4d4d4',
          400: '#a3a3a3',
          500: '#737373',
          600: '#525252',
          700: '#404040',
          800: '#262626',
          900: '#171717',      // Dark text like logo
          950: '#0a0a0a',
        },
      },

      // Custom fonts
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
        mono: ['JetBrains Mono', 'monospace'],
        display: ['Trajan Pro', 'Playfair Display', 'serif']
      },

      // Custom spacing
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },

      // Custom shadows with cream/orange glows
      boxShadow: {
        soft: '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
        medium: '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 30px -5px rgba(0, 0, 0, 0.05)',
        strong: '0 10px 40px -10px rgba(0, 0, 0, 0.15), 0 20px 50px -10px rgba(0, 0, 0, 0.1)',
        glow: '0 0 20px rgba(244, 195, 84, 0.4)',          // Cream glow
        'glow-orange': '0 0 20px rgba(249, 115, 22, 0.4)', // Orange glow
        'glow-blue': '0 0 20px rgba(59, 130, 246, 0.4)',   // Blue glow
        'glow-purple': '0 0 20px rgba(217, 70, 239, 0.4)', // Purple glow
        'gold-glow': '0 0 15px rgba(212, 175, 55, 0.6)',   // Gold glow
        'gold-strong': '0 0 25px rgba(212, 175, 55, 0.8)', // Stronger gold glow
        balloon: '0 4px 20px rgba(244, 195, 84, 0.2)',     // Balloon-like shadow with cream
      },

      // Custom border radius
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },

      // Custom animations
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'fade-in-up': 'fadeInUp 0.6s ease-out',
        'fade-in-down': 'fadeInDown 0.6s ease-out',
        'slide-in-left': 'slideInLeft 0.5s ease-out',
        'slide-in-right': 'slideInRight 0.5s ease-out',
        'bounce-soft': 'bounceSoft 2s infinite',
        'pulse-soft': 'pulseSoft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        float: 'float 3s ease-in-out infinite',
        'balloon-float': 'balloonFloat 4s ease-in-out infinite',
        wiggle: 'wiggle 1s ease-in-out infinite',
      },

      // Keyframes
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        fadeInUp: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        fadeInDown: {
          '0%': { opacity: '0', transform: 'translateY(-20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideInLeft: {
          '0%': { opacity: '0', transform: 'translateX(-20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        slideInRight: {
          '0%': { opacity: '0', transform: 'translateX(20px)' },
          '100%': { opacity: '1', transform: 'translateX(0)' },
        },
        bounceSoft: {
          '0%, 20%, 53%, 80%, 100%': { transform: 'translate3d(0,0,0)' },
          '40%, 43%': { transform: 'translate3d(0, -8px, 0)' },
          '70%': { transform: 'translate3d(0, -4px, 0)' },
          '90%': { transform: 'translate3d(0, -2px, 0)' },
        },
        pulseSoft: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        balloonFloat: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '25%': { transform: 'translateY(-8px) rotate(1deg)' },
          '50%': { transform: 'translateY(-15px) rotate(0deg)' },
          '75%': { transform: 'translateY(-8px) rotate(-1deg)' },
        },
        wiggle: {
          '0%, 100%': { transform: 'rotate(-3deg)' },
          '50%': { transform: 'rotate(3deg)' },
        },
      },

      // Backgrounds
      backgroundImage: {
        'gold-gradient': 'linear-gradient(135deg, #B8860B 0%, #D4AF37 40%, #F5D879 60%, #B8860B 100%)',
        'black-gradient': 'linear-gradient(180deg, #0a0a0a 0%, #141414 100%)',
        'hero-pattern': "url('/images/hero-pattern.svg')",
        'balloon-pattern':
          'radial-gradient(circle at 20% 20%, rgba(212,175,55,0.10) 0%, transparent 50%), radial-gradient(circle at 80% 40%, rgba(212,175,55,0.06) 0%, transparent 50%)',
      },

      // Typography (requires @tailwindcss/typography)
      typography: {
        DEFAULT: {
          css: {
            maxWidth: '65ch',
            color: 'inherit',
            a: {
              color: 'inherit',
              textDecoration: 'underline',
              fontWeight: '500',
            },
            '[class~="lead"]': { color: 'inherit' },
            strong: { color: 'inherit', fontWeight: '600' },
          },
        },
      },
    },
  },

  plugins: [
    typography,
    plugin(function ({ addUtilities }) {
      const newUtilities = {
        '.text-shadow': {
          textShadow: '0 2px 4px rgba(0,0,0,0.10)',
        },
        '.text-shadow-md': {
          textShadow: '0 4px 8px rgba(0,0,0,0.12), 0 2px 4px rgba(0,0,0,0.08)',
        },
        '.text-shadow-lg': {
          textShadow: '0 15px 35px rgba(0,0,0,0.1), 0 5px 15px rgba(0,0,0,0.07)',
        },
        '.text-shadow-none': {
          textShadow: 'none',
        },
        '.backdrop-blur-xs': {
          backdropFilter: 'blur(2px)',
        },
        // Balloon-inspired effects with cream base
        '.balloon-bounce': {
          transform: 'translateY(-5px)',
          transition: 'transform 0.3s ease',
        },
        '.balloon-hover': {
          '&:hover': {
            transform: 'translateY(-8px) scale(1.05)',
            boxShadow: '0 8px 25px rgba(212, 175, 55, 0.35)',
          },
        },
      }
      addUtilities(newUtilities)
    }),
  ],

  // Safelist for dynamic classes including new balloon colors
  safelist: [
    'animate-fade-in',
    'animate-fade-in-up',
    'animate-slide-in-left',
    'animate-slide-in-right',
    'animate-balloon-float',

    // Brand combos
    'bg-brand-black', 'bg-brand-charcoal', 'bg-brand-ivory',
    'text-brand-gold', 'text-brand-gold-dark', 'text-brand-gold-light',
    'border-brand-gold', 'shadow-gold-glow', 'shadow-gold-strong',
    'bg-gold-gradient', 'bg-black-gradient',

    // Balloon variants
    'bg-balloons-gold', 'bg-balloons-red', 'bg-balloons-blue',
    'bg-balloons-teal', 'bg-balloons-purple', 'bg-balloons-pink',
    'text-balloons-gold', 'text-balloons-red', 'text-balloons-blue',
    'text-balloons-teal', 'text-balloons-purple', 'text-balloons-pink',
  ],
}
