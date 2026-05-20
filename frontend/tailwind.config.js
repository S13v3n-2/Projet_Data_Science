/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
      },
      colors: {
        brand: {
          bg: '#F8FAFC',
          sidebar: '#0F172A',
          accent: '#6366F1',
          success: '#10B981',
          danger: '#EF4444',
          warning: '#F59E0B',
          border: '#E2E8F0',
        },
      },
      boxShadow: {
        card: '0 1px 2px 0 rgba(15, 23, 42, 0.04), 0 1px 3px 0 rgba(15, 23, 42, 0.06)',
      },
    },
  },
  plugins: [],
}
