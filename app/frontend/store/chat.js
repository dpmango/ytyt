/* eslint-disable no-console */
// import { loginService } from '~/api/auth';
import Vue from 'vue';
import { filesService } from '~/api/chat';

const EVENTS = {
  DIALOGS: 'dialogs.load',
  MESSAGES: 'dialogs.messages.load',
  SEND_MESSAGE: 'dialogs.messages.create',
  READ_MESSAGE: 'dialogs.messages.seen',
  NOTIFICATION_COUNT: 'notifications.dialogs.count',
  MESSAGES_COUNT: 'notifications.dialogs.messages.count',
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
    error: null,
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
    const { event, data, meta, exception } = message;

    if (exception) {
      state.socket.error = data;
      this.$toast.global.error({ message: data });
    } else {
      state.socket.error = null;
    }

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
        // if (data.length) {
        //   state.activeDialog = data[0].dialog;
        // }

        if (meta.offset === 0) {
          state.messages = data;
        } else {
          state.messages = [...data, ...state.messages];
        }

        state.messagesMeta = meta;
        break;

      case EVENTS.SEND_MESSAGE: {
        if (state.activeDialog) {
          state.messages.push(data);
        }

        break;
      }
      case EVENTS.READ_MESSAGE: {
        const { id, date_read } = data;
        const message = state.messages.find((x) => x.id === id);
        if (message) {
          message.date_read = date_read;

          state.messages = [...state.messages.map((x) => (x.id !== id ? x : { ...x, ...message }))];
        }
        break;
      }
      case EVENTS.NOTIFICATION_COUNT:
        state.notificationCount = data;
        break;

      case EVENTS.MESSAGES_COUNT:
        break;

      case EVENTS.ONLINE: {
        const { user_id, status_online } = data;
        state.dialogs = [
          ...state.dialogs.map((x) =>
            x.user.id !== user_id
              ? x
              : {
                  ...x,
                  ...{
                    user: {
                      ...x.user,
                      ...{ status_online },
                    },
                  },
                }
          ),
        ];
        break;
      }

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
  resetMessages(state) {
    state.activeDialog = null;
    state.messages = [];
    state.messagesMeta = {};
  },
};

export const actions = {
  connect({ commit, dispatch }, request) {
    if (Vue.prototype.$connect) {
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
    }
  },
  disconnect({ commit }, request) {
    if (Vue.prototype.$disconnect) {
      Vue.prototype.$disconnect();
    }
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
  readMessage({ commit }, request) {
    this.$socket.sendObj({
      event: EVENTS.READ_MESSAGE,
      dialog_id: request.dialog_id,
      message_id: request.message_id,
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
  async uploadFile({ commit }, request) {
    const [err, result] = await filesService(this.$api, request);

    if (err) throw err;

    // commit('verifyUserEmail');

    return result;
  },
};
