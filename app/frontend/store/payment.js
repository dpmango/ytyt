import { initService, initInstallmentService } from '~/api/payment';

export const state = () => ({
  payment: {},
});

export const getters = {
  payment: (state) => {
    return state.payment;
  },
};

export const mutations = {
  setPayment(state, data) {
    state.payment = data;
  },
};

export const actions = {
  async init({ commit }) {
    const [err, result] = await initService(this.$api, {
      course_id: 1,
    });

    if (err) throw err;

    commit('setPayment', result);

    return result;
  },
  async initInstallment({ commit }, request) {
    let promo_code = '';

    // {
    //   id: 'installment_0_0_4_5',
    //   code: 'PROMO_CODE_0_0_4',
    //   title: '0-0-4'
    // },
    // {
    //   id: 'installment_0_0_6_6',
    //   code: 'PROMO_CODE_0_0_6',
    //   title: '0-0-6'
    // },
    // {
    //   id: 'installment_0_0_10_10',
    //   code: 'PROMO_CODE_0_0_10',
    //   title: '0-0-10'
    // },
    // {
    //   id: 'installment_0_0_12_11',
    //   code: 'PROMO_CODE_0_0_12',
    //   title: '0-0-12'
    // }

    if (request.id === 2) {
      promo_code = 'installment_0_0_4_5';
    } else if (request.id === 3) {
      promo_code = 'installment_0_0_6_6';
    } else if (request.id === 4) {
      promo_code = 'installment_0_0_12_11';
    }

    const [err, result] = await initInstallmentService(this.$api, {
      course_id: 1,
      promo_code,
    });

    if (err) throw err;

    commit('setPayment', result);

    return result;
  },
};
