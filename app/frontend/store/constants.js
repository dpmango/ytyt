import { getService } from '~/api/constants';

export const state = () => ({
  constants: [],
});

export const getters = {
  constants: (state) => {
    return state.constants;
  },
  getConstantById: (state) => (id) => {
    return state.constants.find((x) => x.id === id);
  },
};

export const mutations = {
  clear(state) {
    state.constants = [];
  },
  setConstants(state, constants) {
    state.constants = constants;
  },
};

export const actions = {
  async get({ commit }) {
    const [err, result] = await getService(this.$api);

    if (err) throw err;

    commit('setConstants', result);

    return result;
  },
};
