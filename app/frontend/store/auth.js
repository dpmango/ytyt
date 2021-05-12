import {
  loginService,
  signupService,
  refreshTokenService,
  verifyGetService,
  verifyPostService,
  recoverService,
  recoverConfirmationService,
  passwordChangeService,
  logoutService,
  userService,
  updateUserService,
} from '~/api/auth';

export const state = () => ({
  token: null,
  user: {
    email: null,
    first_name: null,
    last_name: null,
    github_url: null,
    avatar: null,
    thumbnail_avatar: null,
    email_notifications: undefined,
    email_confirmed: undefined,
    dialog: null,
  },
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
    console.log('logout mutation called');
    state.token = null;
    state.user = {
      email: null,
      first_name: null,
      last_name: null,
      github_url: null,
      avatar: null,
      thumbnail_avatar: null,
      email_notifications: undefined,
      email_confirmed: undefined,
      dialog: null,
    };

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
    // const keys = Object.keys(user);
    // keys.forEach((key) => {
    //   state.user[key] = user[key];
    // });
  },
  verifyUserEmail(state) {
    state.user.email_confirmed = true;
  },
  // updateUserPhoto(state, user) {
  //   state.user.avatar = user.avatar;
  // },
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
  async refreshToken({ commit }, request) {
    const [err, result] = await refreshTokenService(this.$api, request);

    if (err);

    const { token } = result;

    commit('updateToken', token);

    return result;
  },
  async verifyGet({ commit }, request) {
    const [err, result] = await verifyGetService(this.$api, request);

    if (err) throw err;

    commit('verifyUserEmail');

    return result;
  },
  async verifyPost({ commit }, request) {
    const [err, result] = await verifyPostService(this.$api, request);

    if (err) throw err;

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
  async passwordChange({ commit, _dispatch }, request) {
    const [err, result] = await passwordChangeService(this.$api, request);

    if (err) throw err;

    const { detail } = result;

    return result;
  },
  async logout({ commit, dispatch }) {
    const [err, result] = await logoutService(this.$api);

    if (err) throw err;

    commit('logOut');

    dispatch('chat/disconnect', null, { root: true });

    this.$router.push('/auth/login');

    return result;
  },
  async update({ commit }, request) {
    const [err, result] = await updateUserService(this.$api, request);

    if (err) throw err;

    commit('updateUser', result);

    return result;
  },
};
