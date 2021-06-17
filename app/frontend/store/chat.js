/* eslint-disable no-console */
// import { loginService } from '~/api/auth';
import Vue from 'vue';
import { filesService } from '~/api/chat';
import { rebuildSocket } from '~/helpers/RebuildSocket';

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
  notificationDialogsCount: 0,
  notificationMessageCount: 0,
  dialogs: [],
  messages: [],
  messagesMeta: {},
  dialogsMeta: {},
  reply: {
    id: null,
    text: null,
  },
  socket: {
    error: null,
    isConnected: false,
    reconnectError: false,
  },
});

export const getters = {
  activeDialog: (state) => state.activeDialog,
  notificationDialogsCount: (state) => state.notificationDialogsCount,
  notificationMessageCount: (state) => state.notificationMessageCount,
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
  reply: (state) => state.reply,
};

export const mutations = {
  SOCKET_ONOPEN(state, event) {
    console.log('SOCKET_ONOPEN', event);
    this.$socket = event.currentTarget;
    state.socket.isConnected = true;
    state.socket.error = null;
    state.socket.reconnectError = false;

    state.activeDialog = null;
    state.messages = [];
    state.messagesMeta = {};
  },
  SOCKET_ONCLOSE(state, event) {
    console.log('SOCKET_ONCLOSE', event);
    try {
      rebuildSocket({
        $config: this.$config,
        $store: this,
      });
    } catch (e) {
      console.log('rebuild err', e);
    }
    state.socket.isConnected = false;
  },
  SOCKET_ONERROR(state, event) {
    console.error('SOCKET_ONERROR', event);
  },
  SOCKET_ONMESSAGE(state, message) {
    // console.log('SOCKET_ONMESSAGE', message);
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
        if (state.activeDialog && data.dialog === state.activeDialog) {
          state.messages.push(data);
        }

        state.dialogs = [
          ...state.dialogs.map((x) =>
            x.id !== data.dialog
              ? x
              : {
                  ...x,
                  ...{
                    last_message: {
                      body: data.body,
                      file: data.file,
                    },
                  },
                }
          ),
        ];

        state.dialogs = [
          ...state.dialogs.filter((x) => x.id === data.dialog),
          ...state.dialogs.filter((x) => x.id !== data.dialog),
        ];

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
        state.notificationDialogsCount = data;
        break;

      case EVENTS.MESSAGES_COUNT: {
        const { count, dialog_id } = data;

        state.notificationMessageCount = count;
        state.dialogs = [
          ...state.dialogs.map((x) =>
            x.id !== dialog_id
              ? x
              : {
                  ...x,
                  ...{
                    unread_messages_count: count,
                  },
                }
          ),
        ];

        break;
      }

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
  setReply(state, req) {
    state.reply.id = req.id;
    state.reply.text = req.text;
  },
  pushGhostMessage(state, message) {
    state.messages.push(message);
  },
  clearGhostMessage(state) {
    state.messages = state.messages.filter((x) => x.id !== 9999999);
  },
};

export const actions = {
  async connect({ commit, dispatch }, request) {
    if (Vue.prototype.$connect) {
      Vue.prototype.$disconnect();
      await Vue.prototype.$connect();
    }
  },
  async disconnect({ commit }, request) {
    if (Vue.prototype.$disconnect) {
      console.log('$disconnect method called');
      await Vue.prototype.$disconnect();
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
  async createMessageGhost({ commit, rootGetters }, { file, ...request }) {
    await commit('pushGhostMessage', {
      isGhost: true,
      id: 9999999,
      user: rootGetters['auth/user'],
      file: {
        url: null,
        size: file.size,
        // type: file.type.split('/')[0] === 'image' ? 2 : 1,
        type: 1,
        file_name: file.name,
      },
      lesson: null,
      body: null,
      text_body: null,
      markdown_body: null,
      reply: null,
      date_created: new Date(),
    });
  },
  async uploadFile({ commit }, file) {
    const formData = new FormData();
    formData.append('content', file);

    const [err, result] = await filesService(this.$api, formData);

    if (err) throw err;

    await commit('clearGhostMessage');

    return result;
  },
};
