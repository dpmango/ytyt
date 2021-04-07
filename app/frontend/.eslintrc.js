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
    'vue/require-default-prop': 'off',
    'vue/no-unused-vars': 'off',
    '@typescript-eslint/no-unused-vars': 'off',
  },
};
