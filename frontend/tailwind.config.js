/** Tokens tomados de «PizzaSmart - T1-03 Tipografía y colores» (D02). */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        page: "#0A0A0C",
        surface: "#131315",
        raised: "#19191C",
        card: "#151517",
        input: "#101012",
        brand: { DEFAULT: "#FF5A24", hover: "#FF6A38", pressed: "#D93E0D" },
        ink: { DEFAULT: "#F3EEE7", secondary: "#AAA7A4", muted: "#9B9997", dim: "#777477", faint: "#656366" },
        ok: "#56C987",
        warn: "#F0AD3F",
        danger: "#EE4B45",
      },
      borderColor: { DEFAULT: "rgba(255,255,255,0.1)", strong: "rgba(255,255,255,0.2)" },
      fontFamily: {
        titulo: ["Manrope", "system-ui", "sans-serif"],
        cuerpo: ['"DM Sans"', "system-ui", "sans-serif"],
        serif: ['"Playfair Display"', "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};
