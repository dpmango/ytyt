module.exports = {
  root: true,
  env: {
    browser: true,
    node: true,
  },
  extends: ['@nuxtjs/eslint-config-typescript', 'plugin:prettier/recommended', 'plugin:nuxt/recommended'],
  plugins: [],
  // add your custom rules here
  rules: {
    quotes: ['error', 'single'],
    // 'prettier/prettier': 'error',
    camelcase: 'off',
    'vue/require-default-prop': 'off',
    'vue/no-unused-vars': 'off',
    'vue/no-v-html': 'off',
    '@typescript-eslint/no-unused-vars': 'off',
  },
};
