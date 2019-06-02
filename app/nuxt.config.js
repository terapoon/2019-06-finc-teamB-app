module.exports = {
  mode: 'spa',
  head: {
    title: 'finc GYM',
    bodyAttrs: {
      ontouchstart: '',
    },
    meta: [
      { charset: 'utf-8' },
    ],
    link: [
      { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
      { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css?family=Noto+Sans+JP' },
    ],
  },
  loading: { color: '#fff' },
  loadingIndicator: {
    name: 'circle',
    color: '#3B8070',
    background: 'white',
  },
  css: [
    '~/assets/main.css',
  ],
  plugins: [
    { src: '~plugins/persiststate.js', ssr: false },
  ],
  pageTransition: 'fade',
  modules: [
    '@nuxtjs/axios',
    'bootstrap-vue/nuxt',
    ['@nuxtjs/moment', ['ja']],
    '@nuxtjs/proxy',
  ],
  proxy: {
    '/api/': {
      target: process.env.API_URL || 'http://localhost:4000',
      pathRewrite: { '^/api/': '' },
    },
  },
  axios: {
    baseURL: '/api',
  },
  build: {
    extend(config, ctx) {
      if (ctx.isDev && ctx.isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/,
        });
      }
    },
  },
};
