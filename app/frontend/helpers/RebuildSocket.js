import Vue from 'vue';
import VueNativeSock from 'vue-native-websocket';
import { mutations } from '~/plugins/socket';

// Hack for sockets token update
export const rebuildSocket = ({ $config, $store }) => {
  $store.dispatch('chat/disconnect');

  const index = Vue._installedPlugins.indexOf(VueNativeSock);

  if (index > -1) {
    Vue._installedPlugins.splice(index, 1);
  }

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

  if (!$store.getters['chat/isConnected']) {
    $store.dispatch('chat/connect');
  }

  setTimeout(() => {
    // just in case
    // TODO - should wather on layout default be working when redirecting from auth ?
    $store.dispatch('chat/getDialogs');
    $store.dispatch('chat/getNotificationCount');
  }, 500);
};
