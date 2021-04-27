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

  $store.dispatch('chat/connect');
};
