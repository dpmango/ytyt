import { rebuildSocket } from '~/helpers/RebuildSocket';

const UPDATE_INTERVAL = 10 * 60 * 1000; // 10 mins

async function refreshToken(context) {
  const token = context.store.state.auth.token;

  // console.log('refreshing token', token);

  if (token) {
    try {
      await context.store.dispatch('auth/refreshToken', { token });
      rebuildSocket({
        $config: context.$config,
        $store: context.store,
      });
    } catch (error) {
      context.store.commit('auth/logOut');
      context.$toast.global.error({ message: 'Ошибка обновления токена' });
      // throw new Error('Ошибка обновления токена');
    }
  }
}

export default function (context, inject) {
  // if (token) {
  //   // await refreshToken(token, store, $toast);
  //   // rebuildSocket();
  // }

  // TODO - add cookies timestamps

  setInterval(() => {
    refreshToken(context);
  }, UPDATE_INTERVAL);
}
