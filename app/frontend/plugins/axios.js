/* eslint-disable no-console */

// https://axios.nuxtjs.org/helpers
export default function ({ $axios, $config, redirect }, inject) {
  const api = $axios.create({
    baseURL: $config.baseURL,
    headers: {
      'Content-Type': 'application/json',
      Accept: 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  });

  // Inject to context as $api
  inject('api', api);

  // Interceptors
  api.onRequest((x) => {
    console.log(`${x.method.toUpperCase()} | ${x.url}`, x.params, x.data);

    return x;
  });

  api.onResponse((x) => {
    console.log(`${x.status} | ${x.config.url}`, x.data);

    return x;
  });

  api.onError((error) => {
    if (parseInt(error.response && error.response.status) === 401) {
      console.log('unauthorized, logging out ...');
      // auth.logout();
      redirect('/auth/login');
    }

    return Promise.reject(error.response);
  });
}
