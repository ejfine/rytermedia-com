export default defineAppConfig({
  global: {
    picture: {
      dark: "/images/headshot.jpg",
      light: "/images/headshot.jpg",
      alt: "My profile picture",
    },
    meetingLink: "tel:+14044342430",
    email: "ethanryter3@gmail.com",
    available: true,
  },
  ui: {
    colors: {
      primary: "blue",
      neutral: "neutral",
    },
    pageHero: {
      slots: {
        container: "py-18 sm:py-24 lg:py-32",
        title: "mx-auto max-w-xl text-pretty text-3xl sm:text-4xl lg:text-5xl",
        description: "mt-2 text-md mx-auto max-w-2xl text-pretty sm:text-md text-muted",
      },
    },
  },
  footer: {
    credits: `© ${new Date().getFullYear()} Ryter Media`,
    colorMode: false,
    links: [
      {
        icon: "i-simple-icons-instagram",
        to: "https://www.instagram.com/rytermedia/",
        target: "_blank",
        "aria-label": "Ryter Media on Instagram",
      },
      {
        icon: "i-simple-icons-x",
        to: "https://x.com/RyterEthan",
        target: "_blank",
        "aria-label": "Ryter Media on X",
      },
      {
        icon: "i-mdi-gondola",
        to: "https://gondola.cc/RyterEthan",
        target: "_blank",
        "aria-label": "Ryter Media on Gondola",
      },
    ],
  },
});
