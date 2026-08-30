/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        mono: [
          'JetBrains Mono',
          'Fira Code',
          'ui-monospace',
          'SFMono-Regular',
          'Menlo',
          'Monaco',
          'Consolas',
          'monospace',
        ],
      },
      colors: {
        ink: {
          900: '#0b0f1a',
          800: '#11172a',
          700: '#1a2240',
          600: '#252e54',
          500: '#3a4470',
          400: '#5b6592',
        },
        accent: {
          500: '#7c5cff',
          400: '#9b85ff',
          300: '#c1b3ff',
        },
        success: '#4ade80',
        error: '#f87171',
        warn: '#fbbf24',
      },
      boxShadow: {
        glow: '0 0 30px -10px rgba(124, 92, 255, 0.5)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.2s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(4px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
};
