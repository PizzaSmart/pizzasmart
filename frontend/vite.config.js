import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: { port: 5173 }, // el backend permite este origen por CORS (CORS_ORIGENES)
  test: { environment: "jsdom", setupFiles: "./src/setupTests.js", globals: true },
});
