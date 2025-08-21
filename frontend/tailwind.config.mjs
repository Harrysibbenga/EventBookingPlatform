/** @type {import('tailwindcss').Config} */
export default {
    content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
    
    theme: {
      extend: {
        // Custom color palette for event booking platform
        colors: {
          primary: {
            50: '#fef7ee',
            100: '#fdedd3',
            200: '#fbd7a5',
            300: '#f8bc6d',
            400: '#f59932',
            500: '#f2800b',
            600: '#e36706',
            700: '#bc4f08',
            800: '#963f0e',
            900: '#79360f',
            950: '#411a05',
          },
          secondary: {
            50: '#f0f9ff',
            100: '#e0f2fe',
            200: '#bae6fd',
            300: '#7dd3fc',
            400: '#38bdf8',
            500: '#0ea5e9',
            600: '#0284c7',
            700: '#0369a1',
            800: '#075985',
            900: '#0c4a6e',
            950: '#082f49',
          },
          accent: {
            50: '#fdf4ff',
            100: '#fae8ff',
            200: '#f5d0fe',
            300: '#f0abfc',
            400: '#e879f9',
            500: '#d946ef',
            600: '#c026d3',
            700: '#a21caf',
            800: '#86198f',
            900: '#701a75',
            950: '#4a044e',
          },
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
            900: '#171717',
            950: '#0a0a0a',
          }
        },
        
        // Custom fonts
        fontFamily: {
          sans: ['Inter', 'system-ui', 'sans-serif'],
          serif: ['Playfair Display', 'Georgia', 'serif'],
          mono: ['JetBrains Mono', 'monospace'],
        },
        
        // Custom spacing
        spacing: {
          '18': '4.5rem',
          '88': '22rem',
          '128': '32rem',
        },
        
        // Custom shadows
        boxShadow: {
          'soft': '0 2px 15px -3px rgba(0, 0, 0, 0.07), 0 10px 20px -2px rgba(0, 0, 0, 0.04)',
          'medium': '0 4px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 30px -5px rgba(0, 0, 0, 0.05)',
          'strong': '0 10px 40px -10px rgba(0, 0, 0, 0.15), 0 20px 50px -10px rgba(0, 0, 0, 0.1)',
          'glow': '0 0 20px rgba(248, 188, 109, 0.4)',
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
          'float': 'float 3s ease-in-out infinite',
        },
        
        // Custom keyframes
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
        },
        
        // Custom backgrounds
        backgroundImage: {
          'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
          'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
          'hero-pattern': "url('/images/hero-pattern.svg')",
        },
        
        // Custom typography
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
              '[class~="lead"]': {
                color: 'inherit',
              },
              strong: {
                color: 'inherit',
                fontWeight: '600',
              },
              'ol[type="A"]': {
                '--list-counter-style': 'upper-alpha',
              },
              'ol[type="a"]': {
                '--list-counter-style': 'lower-alpha',
              },
              'ol[type="A" s]': {
                '--list-counter-style': 'upper-alpha',
              },
              'ol[type="a" s]': {
                '--list-counter-style': 'lower-alpha',
              },
              'ol[type="I"]': {
                '--list-counter-style': 'upper-roman',
              },
              'ol[type="i"]': {
                '--list-counter-style': 'lower-roman',
              },
              'ol[type="I" s]': {
                '--list-counter-style': 'upper-roman',
              },
              'ol[type="i" s]': {
                '--list-counter-style': 'lower-roman',
              },
              'ol[type="1"]': {
                '--list-counter-style': 'decimal',
              },
            },
          },
        },
      },
    },
    
    plugins: [
      // Add custom utilities
      function({ addUtilities, theme }) {
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
        }
        
        addUtilities(newUtilities)
      },
    ],
    
    // Safelist for dynamic classes
    safelist: [
      'animate-fade-in',
      'animate-fade-in-up',
      'animate-slide-in-left',
      'animate-slide-in-right',
    ],
  }