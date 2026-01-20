/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'lab-white': '#F7F9FC',
        'charcoal': '#2D3436',
        'muted-gold': '#D4AF37',
      },
    },
  },
  plugins: [],
}
