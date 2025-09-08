import react from "@vitejs/plugin-react";
import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vitest/config";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["src/test/setup.ts"],
    coverage: {
      reporter: ["text", "json", "html"],
      reportsDirectory: "coverage",
      include: ["src/**/*.{ts,tsx}"],
      exclude: ["src/api/generated/**", "src/**/__tests__/**", "src/test/**", "**/*.d.ts"],
    },
    globals: true,
    alias: [
      { find: "@", replacement: fileURLToPath(new URL("./src", import.meta.url)) },
      {
        find: "@components",
        replacement: fileURLToPath(new URL("./src/components", import.meta.url)),
      },
      { find: "@hooks", replacement: fileURLToPath(new URL("./src/hooks", import.meta.url)) },
      { find: "@services", replacement: fileURLToPath(new URL("./src/services", import.meta.url)) },
      { find: "@utils", replacement: fileURLToPath(new URL("./src/utils", import.meta.url)) },
    ],
  },
});
