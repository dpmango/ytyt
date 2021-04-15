import {
  loginService,
  signupService,
  recoverService,
  recoverConfirmationService,
  logoutService,
  userService,
  updateUserService,
} from '~/api/auth';

export const state = () => ({
  token: null,
  user: {},
});

export const getters = {
  user: (state) => {
    return state.user;
  },
  token: (state) => {
    return state.token;
  },
  isAuthenticated: (state) => {
    return !!state.token;
  },
};

export const mutations = {
  logOut(state) {
    state.sign_token = '';
    state.user = {};

    this.$cookies.remove('ytyt_token');
    this.$api.setToken(false);
  },
  updateToken(state, token) {
    if (token) {
      state.token = token;

      this.$cookies.set('ytyt_token', token);
      // TODO - token not set on client - transformed request instaed
      // this.$api.setToken(token, 'JWT');
    }
  },
  updateUser(state, user) {
    state.user = { ...state.user, ...user };
  },
  updateUserPhoto(state, picture) {
    state.user.picture.url = picture.url;
  },
};

export const actions = {
  checkToken({ commit }) {
    const token = this.$cookies.get('ytyt_token');

    if (token) {
      // TODO - check if token is already there
      commit('updateToken', token);
    }
  },
  async getUserInfo({ commit }, request) {
    const [err, result] = await userService(this.$api);

    if (err) throw err;

    commit('updateUser', result);

    return result;
  },
  async login({ commit }, request) {
    const [err, result] = await loginService(this.$api, request);

    if (err) throw err;

    const { token, user } = result;

    commit('updateToken', token);
    commit('updateUser', user);

    return result;
  },
  async signup({ commit, _dispatch }, request) {
    const [err, result] = await signupService(this.$api, request);

    if (err) throw err;

    const { token, user } = result;

    commit('updateToken', token);
    commit('updateUser', user);

    return result;
  },
  async recover({ commit, _dispatch }, request) {
    const [err, result] = await recoverService(this.$api, request);

    if (err) throw err;

    const { detail } = result;

    return result;
  },
  async recoverConfirmation({ commit, _dispatch }, request) {
    const [err, result] = await recoverConfirmationService(this.$api, request);

    if (err) throw err;

    const { detail } = result;

    return result;
  },
  async logout({ commit }) {
    const [err, result] = await logoutService(this.$api);

    if (err) throw err;

    commit('logOut');

    return result;
  },
  async update({ commit }, request) {
    const [err, result] = await updateUserService(this.$api, request);

    if (err) throw err;

    commit('updateUser', result);

    return result;
  },
};
