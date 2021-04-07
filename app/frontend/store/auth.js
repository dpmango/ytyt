import Cookies from 'js-cookie';
import { loginService, signupService, recoverService } from '~/api/auth';

export const state = () => ({
  token: null,
  user: {},
});

export const getters = {
  user: (state) => state.user,
  token: (state) => state.token,
  isAuthenticated: (state) => {
    return state.token;
  },
};

export const mutations = {
  logOut(state) {
    state.sign_token = '';
    state.user = {};
  },
  updateToken(state, token) {
    if (token) {
      state.token = token;
      Cookies.set('ytyt_token', token);
      this.$api.setToken(token, 'Bearer');
      // axios.defaults.headers.common.Authorization = 'Bearer ' + token;
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
    const token = Cookies.get('ytyt_token');

    if (token) {
      commit('updateToken', token);
    }
  },
  async login({ commit }, request) {
    const [err, result] = await loginService(request);

    if (err) throw err;

    const { token, user } = result;

    commit('updateToken', token);
    commit('updateUser', user);

    return result;
  },
  async signup({ commit, _dispatch }, request) {
    const [err, result] = await signupService(request);

    if (err) throw err;

    const { token, user } = result;

    commit('updateToken', token);
    commit('updateUser', user);

    return result;
  },
  async recover({ commit, _dispatch }, request) {
    const [err, result] = await recoverService(request);

    if (err) throw err;

    const { detail } = result;

    return result;
  },
};
