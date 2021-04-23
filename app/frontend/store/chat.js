/* eslint-disable no-console */
// import { loginService } from '~/api/auth';
import Vue from 'vue';
import { createChatService, filesService } from '~/api/chat';

const EVENTS = {
  DIALOGS: 'dialogs.load',
  MESSAGES: 'dialogs.messages.load',
  SEND_MESSAGE: 'dialogs.messages.create',
  READ_MESSAGE: 'dialogs.messages.seen',
  NOTIFICATION_COUNT: 'notifications.dialogs.count',
};

const ERRORS = {
  NOT_CONNECTED: 'Not connected to server',
  NOT_CONNECTED_TO_CHAT: 'Chat not started',
  ALREADY_CONNECTED: 'Already connected to server',
  ALREADY_CONNECTED_TO_CHAT: 'Chat already started',
  MISSING_ARGUMENT: 'Required argument is missing',
  INVALID_ARGUMENT: 'Required argument has invalid type or value',
};

export const state = () => ({
  activeDialog: null,
  dialogs: [],
  messages: [],
  socket: {
    isConnected: false,
    reconnectError: false,
  },
});

export const getters = {
  activeDialog: (state) => state.activeDialog,
  dialogs: (state) => state.dialogs,
  messages: (state) => state.messages,
  socket: (state) => state.socket,
  isConnected: (state) => state.socket.isConnected,
  head: (state) => {
    if (state.activeDialog) {
      const dialog = state.dialogs.find((x) => x.id === state.activeDialog);

      if (dialog) {
        const { first_name, last_name, thumbnail_avatar } = dialog.last_message.user;

        return { first_name, last_name, thumbnail_avatar };
      }
    }
    return false;
  },
};

export const mutations = {
  SOCKET_ONOPEN(state, event) {
    console.log('SOCKET_ONOPEN', event);
    this.$socket = event.currentTarget;
    state.socket.isConnected = true;
  },
  SOCKET_ONCLOSE(state, event) {
    console.log('SOCKET_ONCLOSE', event);
    state.socket.isConnected = false;
  },
  SOCKET_ONERROR(state, event) {
    console.error('SOCKET_ONERROR', event);
  },
  SOCKET_ONMESSAGE(state, message) {
    console.log('SOCKET_ONMESSAGE', message);
    const { event, data } = message;

    // TODO - sorting better to be done on backend
    switch (event) {
      case EVENTS.DIALOGS:
        state.dialogs = data.sort((a, b) => a.id - b.id);
        break;

      case EVENTS.MESSAGES:
        if (data.length) {
          state.activeDialog = data[0].dialog;
        }
        state.messages = data.sort((a, b) => a.id - b.id);
        break;

      case EVENTS.SEND_MESSAGE:
        // TODO - tmp
        if (data !== 1) {
          state.messages.push(data);
        }
        break;

      case EVENTS.READ_MESSAGE:
        // state.dialogs = data;
        break;

      case EVENTS.NOTIFICATION_COUNT:
        // state.dialogs = data;
        break;

      default:
        break;
    }
  },
  SOCKET_RECONNECT(state, count) {
    console.info(state, count);
  },
  SOCKET_RECONNECT_ERROR(state) {
    state.socket.reconnectError = true;
  },

  // Static (inner) mutations
  setActiveDialog(state, id) {},
};

export const actions = {
  connect({ commit, dispatch }, request) {
    return new Promise((resolve) => {
      Vue.prototype.$connect();

      this.watch(
        (state) => {
          return state.chat.socket.isConnected;
        },
        (connect) => {
          if (connect) {
            dispatch('getDialogs');
            resolve(connect);
          }
        }
      );
    });
  },
  disconnect({ commit }, request) {
    Vue.prototype.$disconnect();
  },
  getDialogs({ commit }, request) {
    // if (this.$socket) return;
    this.$socket.sendObj({
      event: EVENTS.DIALOGS,
    });
  },
  getMessages({ commit }, request) {
    this.$socket.sendObj({
      event: EVENTS.MESSAGES,
      dialog_id: request.id,
    });
  },
  sendMessage({ commit }, request) {
    this.$socket.sendObj({
      event: EVENTS.SEND_MESSAGE,
      ...request,
    });
  },
  async createChat({ commit }, request) {
    const [err, result] = await createChatService(this.$api, request);

    if (err) throw err;

    // commit('verifyUserEmail');

    return result;
  },
  async uploadFile({ commit }, request) {
    const [err, result] = await filesService(this.$api, request);

    if (err) throw err;

    // commit('verifyUserEmail');

    return result;
  },
};
