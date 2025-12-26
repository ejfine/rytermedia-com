import type { RouterConfig } from "@nuxt/schema";
import { createWebHashHistory, createWebHistory } from "vue-router";

export default {
  history: (base) => {
    if (import.meta.client && window.location.protocol === "file:") {
      // This is the key: make the base match the file URL pathname.
      // Example pathname: "/C:/Users/.../.output/public/index.html"
      const fileBase = window.location.pathname;
      return createWebHashHistory(fileBase);
    }

    return createWebHistory(base);
  },
} satisfies RouterConfig;
