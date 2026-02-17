import { resolve } from "node:path";
import { defineConfig } from "vite";
import tailwindcss from "@tailwindcss/vite";
import solidPlugin from "vite-plugin-solid";
import { viteSingleFile } from "vite-plugin-singlefile";

export default defineConfig({
  plugins: [tailwindcss(), solidPlugin(), viteSingleFile()],
  resolve: {
    alias: {
      "@turbo": resolve(__dirname, "../assets"),
    },
  },
  build: {
    target: "esnext",
    outDir: "dist",
    minify: "esbuild",
  },
});
