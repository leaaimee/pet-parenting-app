/** @type {import('tailwindcss').Config} */
export default {
  content: ["./src/app/**/*.{js,ts,jsx,tsx}"],
  safelist: [
    "bg-[#f9f2f2]", // very light pastel pink – airy, soft
    "bg-[#f3eeea]", // very light beige-pink – elegant, warm neutral
    "bg-[#f2e0e0]", // light dusty rose – friendly, muted
    "bg-[#262229]", // deep charcoal plum – moody, dramatic
  ],
  theme: {
    extend: {
      colors: {
        base: "#F5F2F0",       // soft ivory – clean, warm background
        text: "#2C2C2C",       // dark grey – primary readable text
        plum: "#7B6D8D",       // muted lavender-plum – cozy, calming
        dark: "#41354F",       // deep eggplant – contrast, structure
        highlight: "#C3B7D7",  // pastel lavender – soft accent, friendly
      },
    },
  },
  plugins: [],
};
