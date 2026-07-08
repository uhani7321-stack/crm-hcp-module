/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
      colors: {
        primary: '#2563EB', // Blue-600
        secondary: '#F3F4F6', // Gray-100
        border: '#E5E7EB', // Gray-200
        background: '#F9FAFB', // Gray-50
      }
    },
  },
  plugins: [],
}
