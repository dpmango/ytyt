/* eslint-disable no-console */

// https://axios.nuxtjs.org/helpers
export default function ({ $axios, store, $config, redirect }, inject) {
  const api = $axios.create({
    baseURL: $config.baseURL,
    headers: {
      common: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        'X-Requested-With': 'XMLHttpRequest',
      },
    },
  });

  // Inject to context as $api
  inject('api', api);

  // Interceptors
  api.onRequest((x) => {
    console.log(`${x.method.toUpperCase()} | ${x.url}`, x.params, x.data);

    const token = store.state.auth.token;
    const isOpenEndpoint = ['constants'].find((v) => x.url.includes(v));

    if (!isOpenEndpoint && token) x.headers.common.Authorization = `JWT ${token}`;

    return x;
  });

  api.onResponse((x) => {
    console.log(`${x.status} | ${x.config.url}`, x.data);

    return x;
  });

  api.onError(async (error) => {
    if (parseInt(error.response && error.response.status) === 401) {
      console.log('unauthorized, logging out ...');
      await store.dispatch('auth/logOut');
    }

    return Promise.reject(error.response);
  });
}
