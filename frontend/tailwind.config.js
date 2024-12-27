/** @type {import('tailwindcss').Config} */
import typography from "@tailwindcss/typography";

export default {
  content: [
    "./index.html", // Include index.html
    "./src/**/*.{js,jsx}", // Include all JS and JSX files in src
  ],
  theme: {
    extend: {}, // Extend default theme here
  },
  plugins: [typography],
};
