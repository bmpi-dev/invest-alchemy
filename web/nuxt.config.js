module.exports = {
  mode: 'universal',

  head: {
    title: 'Invest Alchemy',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'Nuxt.js project' },
    ],
  },

  srcDir: 'client/',

  modules: [
    '@nuxt/http',
    '@nuxtjs/style-resources',
  ],

  plugins: [
    { src: '~plugins/iview', ssr: true }
  ],

  css: ['~assets/styles/global.less'],

  styleResources: {
    less: './assets/vars/*.less'
  },

  http: {
    baseURL: 'https://fey17sm0g7.execute-api.us-east-1.amazonaws.com/dev/',
  },

  render: {
    compressor: false,
  },

  telemetry: false,

};
