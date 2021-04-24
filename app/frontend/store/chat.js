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
  ONLINE: 'users.status.online',
};

// const ERRORS = {
//   NOT_CONNECTED: 'Not connected to server',
//   NOT_CONNECTED_TO_CHAT: 'Chat not started',
//   ALREADY_CONNECTED: 'Already connected to server',
//   ALREADY_CONNECTED_TO_CHAT: 'Chat already started',
//   MISSING_ARGUMENT: 'Required argument is missing',
//   INVALID_ARGUMENT: 'Required argument has invalid type or value',
// };

export const state = () => ({
  activeDialog: null,
  notificationCount: 0,
  dialogs: [],
  messages: [],
  messagesMeta: {},
  dialogsMeta: {},
  socket: {
    isConnected: false,
    reconnectError: false,
  },
});

export const getters = {
  activeDialog: (state) => state.activeDialog,
  notificationCount: (state) => state.notificationCount,
  dialogs: (state) => state.dialogs,
  messages: (state) => state.messages,
  dialogsMeta: (state) => state.dialogsMeta,
  messagesMeta: (state) => state.messagesMeta,
  socket: (state) => state.socket,
  isConnected: (state) => state.socket.isConnected,
  head: (state) => {
    if (state.activeDialog) {
      const dialog = state.dialogs.find((x) => x.id === state.activeDialog);

      if (dialog) {
        const { first_name, last_name, thumbnail_avatar, status_online, email } = dialog.user;

        return { first_name, last_name, thumbnail_avatar, status_online, email };
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
    const { event, data, meta } = message;

    switch (event) {
      case EVENTS.DIALOGS:
        if (meta.offset === 0) {
          state.dialogs = data;
        } else {
          state.dialogs = [...data, ...state.dialogs];
        }

        state.dialogsMeta = meta;
        break;

      case EVENTS.MESSAGES:
        if (data.length) {
          state.activeDialog = data[0].dialog;
        }

        if (meta.offset === 0) {
          state.messages = data;
        } else {
          state.messages = [...data, ...state.messages];
        }

        state.messagesMeta = meta;
        break;

      case EVENTS.SEND_MESSAGE:
        state.messages.push(data);

        break;

      case EVENTS.READ_MESSAGE:
        // state.dialogs = data;
        break;

      case EVENTS.NOTIFICATION_COUNT:
        state.notificationCount = data;
        break;

      case EVENTS.ONLINE:
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
  setActiveDialog(state, id) {
    state.activeDialog = id;
  },
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
            dispatch('getNotificationCount');
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
    return new Promise((resolve) => {
      this.$socket.sendObj({
        event: EVENTS.DIALOGS,
        limit: (request && request.limit) || 20,
        offset: (request && request.offset) || 0,
      });

      this.watch(
        (state) => {
          return state.chat.dialogs;
        },
        (dialogs) => {
          resolve(dialogs);
        }
      );
    });
  },
  getMessages({ commit }, request) {
    return new Promise((resolve) => {
      this.$socket.sendObj({
        event: EVENTS.MESSAGES,
        dialog_id: request.id,
        limit: (request && request.limit) || 20,
        offset: (request && request.offset) || 0,
      });

      this.watch(
        (state) => {
          return state.chat.messages;
        },
        (messages) => {
          resolve(messages);
        }
      );
    });
  },
  getNotificationCount({ commit }, request) {
    this.$socket.sendObj({
      event: EVENTS.NOTIFICATION_COUNT,
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
