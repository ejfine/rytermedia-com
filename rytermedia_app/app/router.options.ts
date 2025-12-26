// app/router.options.ts
import type { RouterConfig } from "@nuxt/schema";
import { createWebHashHistory, createWebHistory } from "vue-router";

export default {
  history: (base) => {
    if (import.meta.client && window.location.protocol === "file:") {
      return createWebHashHistory("/");
    }
    return createWebHistory(base);
  },
} satisfies RouterConfig;
