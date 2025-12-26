// app/router.options.ts
import type { RouterConfig } from "@nuxt/schema";
import { createMemoryHistory } from "vue-router";

const offline = process.env.NUXT_OFFLINE_SINGLE_HTML === "1";

export default {
  history: (base) => {
    // Keep normal behavior for your real deployed site.
    if (!offline) return null;

    // When building the single-file version, ignore the URL path entirely.
    return import.meta.client ? createMemoryHistory(base) : null;
  },
} satisfies RouterConfig;
