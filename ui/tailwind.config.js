// tailwind.config.js

/** @type {import('tailwindcss').Config} */
module.exports = {
  plugins: [
    require('daisyui'),
    require('@tailwindcss/typography')
  ],
  content: [
    './pages/**/*.{vue,js}',
    './components/**/*.{vue,js}',
    './layouts/**/*.{vue,js}'
  ],
  daisyui: { }
}
