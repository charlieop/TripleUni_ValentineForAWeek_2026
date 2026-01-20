// https://nuxt.com/docs/api/configuration/nuxt-config
import { resolve } from "path";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: false },
  alias: {
    "@": resolve(__dirname, "."),
  },
  css: [
    "@/assets/css/resets.css",
    "@/assets/css/fonts.css",
    "@/assets/css/style.css",
  ],
  ssr: false,
  modules: ["@nuxt/ui", "@vueform/nuxt"],
  app: {
    baseURL: "/",

    head: {
      title: "一周CP 2026",
      viewport:
        "width=device-width, initial-scale=1, user-scalable=no, viewport-fit=cover",
      link: [
        {
          rel: "icon",
          type: "image/x-icon",
          href: "https://tripleuni.com/img/logo-512.461b29bd.png",
        },
      ],
    },
  },
});
