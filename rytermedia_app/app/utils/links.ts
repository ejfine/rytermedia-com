import type { NavigationMenuItem } from "@nuxt/ui";

export const navLinks: NavigationMenuItem[] = [
  {
    label: "Home",
    icon: "i-lucide-home",
    to: "/",
  },
  {
    label: "Services",
    icon: "i-lucide-briefcase",
    to: "/services",
  },
  {
    label: "Gallery",
    icon: "i-lucide-book-image",
    to: "/gallery",
  },
  {
    label: "Blog",
    icon: "i-lucide-file-text",
    to: "/blog",
  },
  {
    label: "About",
    icon: "i-lucide-user",
    to: "/about",
  },
];
