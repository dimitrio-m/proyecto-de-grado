// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:5000'
    }
  },
  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' }
  },
  modules: [
    '@nuxtjs/tailwindcss',
    'nuxt-icon'
  ],
  build: {
    transpile: ['chart.js']
  }
})
