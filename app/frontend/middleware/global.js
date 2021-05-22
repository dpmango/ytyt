/* eslint-disable no-console */

// https://axios.nuxtjs.org/helpers
export default async function ({ $axios, store, $config, redirect, ...context }) {
  if (context.isStatic) {
    const token = context.$cookies.get('ytyt_token');

    if (token) {
      try {
        await store.commit('auth/updateToken', token);
        await store.dispatch('auth/getUserInfo');
      } catch (e) {
        await store.commit('auth/logOut');
      }
    }

    await store.dispatch('constants/get');
  }
}
