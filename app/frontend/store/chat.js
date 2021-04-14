// import { loginService } from '~/api/auth';
import { DIALOGS_TEST_DATA, HEAD_TEST_DATA, MESSAGES_TEST_DATA } from '~/api/mockData';

export const state = () => ({
  dialogs: DIALOGS_TEST_DATA,
  head: HEAD_TEST_DATA,
  messages: MESSAGES_TEST_DATA,
});

export const getters = {
  dialogs: (state) => {
    return state.dialogs;
  },
  head: (state) => {
    return state.head;
  },
  messages: (state) => {
    return state.messages;
  },
};

export const mutations = {
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
  changeRoom({ commit }, request) {},
  // async getMessages({ commit }, request) {
  //   const [err, result] = await loginService(this.$api, request);

  //   if (err) throw err;

  //   const { token, user } = result;

  //   commit('updateToken', token);
  //   commit('updateUser', user);

  //   return result;
  // },
};
