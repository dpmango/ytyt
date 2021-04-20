const UPDATE_INTERVAL = 12 * 60 * 60 * 1000;

async function refreshToken(token, store, $toast) {
  try {
    await store.dispatch('auth/refreshToken', { token });
  } catch (error) {
    store.commit('auth/logOut');
    $toast.global.error({ message: 'Ошибка обновления токена' });
    // throw new Error('Ошибка обновления токена');
  }
}

export default async function ({ $axios, store, $toast, $config }, inject) {
  const token = store.state.auth.token;
  if (token) {
    await refreshToken(token, store, $toast);

    setInterval(async function () {
      await refreshToken(token, store, $toast);
    }, UPDATE_INTERVAL);
  }
}
