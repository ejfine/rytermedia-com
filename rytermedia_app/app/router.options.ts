import type { RouterConfig } from "@nuxt/schema";
import { createMemoryHistory, createWebHistory } from "vue-router";

export default {
  history: (base) => {
    console.log("router.options.ts is being used");
    console.log("Protocol:", import.meta.client ? window.location.protocol : "SSR");

    if (import.meta.client && window.location.protocol === "file:") {
      console.log("Using memory history for file:// protocol");
      return createMemoryHistory(base);
    }

    console.log("Using web history");
    return createWebHistory(base);
  },
} satisfies RouterConfig;
