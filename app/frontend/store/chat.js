/* eslint-disable no-console */
// import { loginService } from '~/api/auth';
import Vue from 'vue';
import { DIALOGS_TEST_DATA, HEAD_TEST_DATA, MESSAGES_TEST_DATA } from '~/api/mockData';

const EVENTS = {
  DIALOGS: 'dialogs.load',
  MESSAGES: 'dialogs.messages.load',
  SEND_MESSAGE: 'dialogs.messages.create',
  READ_MESSAGE: 'dialogs.messages.seen',
  NOTIFICATION_COUNT: 'notifications.dialogs.count',
};

export const state = () => ({
  dialogs: DIALOGS_TEST_DATA,
  head: HEAD_TEST_DATA,
  messages: MESSAGES_TEST_DATA,
  socket: {
    isConnected: false,
    message: '',
    reconnectError: false,
  },
});

export const getters = {
  dialogs: (state) => state.dialogs,
  head: (state) => state.head,
  messages: (state) => state.messages,
  socket: (state) => state.socket,
};

export const mutations = {
  SOCKET_ONOPEN(state, event) {
    console.log('open', event);
    this.$socket = event.currentTarget;
    state.socket.isConnected = true;
  },
  SOCKET_ONCLOSE(state, event) {
    console.log('close', event);
    state.socket.isConnected = false;
  },
  SOCKET_ONERROR(state, event) {
    console.error(state, event);
  },
  // default handler called for all methods
  SOCKET_ONMESSAGE(state, message) {
    console.log('onmessage', message);
    state.socket.message = message;
  },
  // mutations for reconnect methods
  SOCKET_RECONNECT(state, count) {
    console.info(state, count);
  },
  SOCKET_RECONNECT_ERROR(state) {
    state.socket.reconnectError = true;
  },
  // logOut(state) {
  //   state.sign_token = '';
  //   state.user = {};
  //   this.$cookies.remove('ytyt_token');
  //   this.$api.setToken(false);
  // },
  // updateToken(state, token) {
  //   if (token) {
  //     state.token = token;
  //     this.$cookies.set('ytyt_token', token);
  //     // TODO - token not set on client - transformed request instaed
  //     // this.$api.setToken(token, 'JWT');
  //   }
  // },
  // updateUser(state, user) {
  //   state.user = { ...state.user, ...user };
  // },
  // updateUserPhoto(state, picture) {
  //   state.user.picture.url = picture.url;
  // },
};

export const actions = {
  connect({ commit }, request) {
    Vue.prototype.$connect();
  },
  disconnect({ commit }, request) {
    Vue.prototype.$disconnect();
  },
  sendMessage(context, message) {
    this.$socket.send(message);
  },
  // changeRoom({ commit }, request) {},
  // async getMessages({ commit }, request) {
  //   const [err, result] = await loginService(this.$api, request);

  //   if (err) throw err;

  //   const { token, user } = result;

  //   commit('updateToken', token);
  //   commit('updateUser', user);

  //   return result;
  // },
};
