import Vue from 'vue';
import VueNativeSock from 'vue-native-websocket';

export const rebuildSocket = () => {
  // console.log(Vue.prototype.$socket.url);
  // // Hack for sockets with vue (token update)
  // const index = Vue._installedPlugins.indexOf(VueNativeSock);
  // if (index > -1) {
  //   Vue._installedPlugins.splice(index, 1);
  // }
  // Vue.use(VueNativeSock, socketWithToken, {
  //   store,
  //   mutations,
  //   connectManually: true,
  //   format: 'json',
  //   reconnection: true,
  //   reconnectionAttempts: 2,
  //   reconnectionDelay: 3000,
  // });
};
