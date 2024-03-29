export const actions = {
  async nuxtServerInit({ dispatch, commit }, { $sentry }) {
    // wont be triggered with ssr: false in nuxt.config.js

    try {
      const token = this.$cookies.get('ytyt_token');

      if (token) {
        // https://github.com/nuxt-community/axios-module/issues/298
        // this.$api.setToken(token, 'JWT');
        try {
          await commit('auth/updateToken', token);
          await dispatch('auth/getUserInfo');
        } catch (e) {
          await commit('auth/logOut');
        }
      }
      await dispatch('constants/get');
    } catch (error) {
      $sentry.captureException(error);
    }
  },
};
