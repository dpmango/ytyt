import Vue from 'vue';
import VueNativeSock from 'vue-native-websocket';

export const mutations = {
  SOCKET_ONOPEN: 'chat/SOCKET_ONOPEN',
  SOCKET_ONCLOSE: 'chat/SOCKET_ONCLOSE',
  SOCKET_ONERROR: 'chat/SOCKET_ONERROR',
  SOCKET_ONMESSAGE: 'chat/SOCKET_ONMESSAGE',
  SOCKET_RECONNECT: 'chat/SOCKET_RECONNECT',
  SOCKET_RECONNECT_ERROR: 'chat/SOCKET_RECONNECT_ERROR',
};

// https://github.com/nathantsoi/vue-native-websocket
export default function ({ store, $config }, inject) {
  // TODO - will not handle refresh updates?
  if (store.state.auth.token) {
    const socketWithToken = `${$config.socketURL}?token=${store.state.auth.token}`;
    Vue.use(VueNativeSock, socketWithToken, {
      store,
      mutations,
      connectManually: true,
      format: 'json',
      reconnection: true,
      reconnectionAttempts: 2,
      reconnectionDelay: 3000,
    });
  }
}
