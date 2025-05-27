/** @type {import('tailwindcss').Config} */
// tailwind.config.js
// tailwind.config.js
export default {
  darkMode: 'class',
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        montserrat: ['Hamlet', 'Montserrat', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
