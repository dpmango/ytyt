export const actions = {
  async nuxtServerInit({ dispatch, commit }) {
    const token = this.$cookies.get('ytyt_token');

    console.log('nuxt server init', token);

    if (token) {
      // https://github.com/nuxt-community/axios-module/issues/298
      // this.$api.setToken(token, 'JWT');
      try {
        await commit('auth/updateToken', token);
        await dispatch('auth/getUserInfo');
        // await dispatch('constants/get');
      } catch (e) {
        await commit('auth/logOut');
      }
    }

    await dispatch('constants/get');
  },
};
