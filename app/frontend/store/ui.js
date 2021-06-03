export const state = () => ({
  modalPaymentStart: false,
  modalPaymentModal: false,
});

export const getters = {
  modal: (state) => {
    return state.modal;
  },
};

export const mutations = {
  setModalPaymentStart(state, val) {
    state.modalPaymentStart = val;
  },
  setModalPaymentModal(state, val) {
    state.modalPaymentModal = val;
  },
};
