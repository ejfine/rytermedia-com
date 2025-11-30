// https://nuxt.com/docs/api/configuration/nuxt-config
import { defineNuxtConfig } from "nuxt/config";
export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  future: {
    compatibilityVersion: 4,
  },
  devtools: { enabled: process.env.NODE_ENV !== "test" },
  telemetry: process.env.NODE_ENV !== "test",
  // the conditional modules added in by the template make it complicated to format consistently...at least with only 3 'always included' modules
  // prettier-ignore
  modules: [
    "@nuxt/ui",
    ["@nuxt/eslint", { devOnly: true }],
    ["@nuxt/test-utils/module", { devOnly: true }],
  ],
  css: ["~/assets/css/main.css"],
  experimental: { appManifest: false }, // https://github.com/nuxt/nuxt/issues/30461#issuecomment-2572616714
  nitro: {
    prerender: {
      concurrency: 1, // lower the concurrency to not be such a memory hog
      interval: 200, // ms pause between batches – lets the Garbage Collector catch up
    },
  },
  vite: {
    server: {
      watch: {
        usePolling: true, // this seems to be explicitly needed when in a devcontainer in order for hot reloading to work
      },
    },
  },
});
