export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: 'ytyt',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { name: 'robots', content: 'noindex' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/png', href: '/favicon.png' }],
  },

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: [{ src: '~/assets/styles/index.scss', lang: 'sass' }],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    '~/plugins/axios',
    '~/plugins/refresh',
    '~/plugins/filters',
    '~/plugins/event-bus',
    '~/plugins/global-mixins',
    '~plugins/modal',
    '~plugins/lightbox',
    { src: '~plugins/legacy', mode: 'client' },
    { src: '~/plugins/markdown', mode: 'client' },
    { src: '~/plugins/toast', mode: 'client' },
    { src: '~plugins/mask', mode: 'client' },
    { src: '~/plugins/socket', mode: 'client' },
    { src: '~/plugins/vee-validate', mode: 'client' },
    { src: '~/plugins/swiper', mode: 'client', ssr: false },
  ],

  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [
    // https://go.nuxtjs.dev/typescript
    '@nuxt/typescript-build',
    // https://go.nuxtjs.dev/stylelint
    '@nuxtjs/stylelint-module',
    '@nuxtjs/style-resources',
    // https://github.com/nuxt-community/svg-module
    '@nuxtjs/svg',
  ],

  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    '@nuxtjs/axios',
    // https://github.com/nuxt-community/community-modules/tree/master/packages/toast
    '@nuxtjs/toast',
    // https://github.com/microcipcip/cookie-universal/tree/master/packages/cookie-universal-nuxt
    'cookie-universal-nuxt',
  ],

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {},

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {
    transpile: ['vue-final-modal'],
  },

  // https://github.com/nuxt-community/style-resources-module/
  styleResources: {
    sass: ['./assets/styles/utilities/_index.scss'],
    scss: ['./assets/styles/utilities/_index.scss'],
  },

  // https://nuxtjs.org/blog/moving-from-nuxtjs-dotenv-to-runtime-config
  publicRuntimeConfig: {
    baseURL: process.env.BASE_URL,
    socketURL: process.env.SOCKET_URL,
  },

  loading: {
    color: '#1E88E5',
    height: '3px',
    throttle: 800,
    continuous: true,
  },

  toast: {
    position: 'top-right',
  },

  router: {
    middleware: 'global',
  },

  // target: 'static',
  // ssr: false,
};
