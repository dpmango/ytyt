import Vue from 'vue';
import VueNativeSock from 'vue-native-websocket';
import { mutations } from '~/plugins/socket';

// Hack for sockets token update
export const rebuildSocket = async ({ $config, $store }) => {
  await $store.dispatch('chat/disconnect');

  const index = Vue._installedPlugins.indexOf(VueNativeSock);

  if (index > -1) {
    Vue._installedPlugins.splice(index, 1);
  }
  console.log('rebuilding socket', $store.state.auth.token);

  const socketWithToken = `${$config.socketURL}?token=${$store.state.auth.token}`;

  Vue.use(VueNativeSock, socketWithToken, {
    store: $store,
    mutations,
    connectManually: true,
    format: 'json',
    reconnection: true,
    reconnectionAttempts: 2,
    reconnectionDelay: 3000,
  });

  console.log('rebuilding - is connected', !$store.getters['chat/isConnected']);
  if (!$store.getters['chat/isConnected']) {
    console.log('will connect');
    $store.dispatch('chat/connect');
  }

  // setTimeout(() => {
  //   $store.dispatch('chat/getDialogs');
  //   $store.dispatch('chat/getNotificationCount');
  // }, 500);
};
