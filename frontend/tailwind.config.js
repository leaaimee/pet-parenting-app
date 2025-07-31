/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/app/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        base: "#F5F2F0",
        text: "#2C2C2C",
        plum: "#7B6D8D",
        dark: "#41354F",
        highlight: "#C3B7D7",
      },
    },
  },
  plugins: [],
};
