import { defineConfig } from "vite";

export default defineConfig({
  build: {
    outDir: "./ui/static/ui/",
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: "ui/vite_src/js/main.js",
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
  },
});
