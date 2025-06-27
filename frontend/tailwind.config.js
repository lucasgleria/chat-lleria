/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Tailwind will read those files
  ],
  theme: {
    extend: {
      keyframes: {
        bounceY: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-25px)' },
        },
        bounceYZ: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        }
      },
      animation: {
        bounceY: 'bounceY 2s infinite',
        bounceYZ: 'bounceYZ 2s infinite'
      },
    },
  },
  plugins: [],
}