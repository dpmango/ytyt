export const state = () => ({
  modalPaymentStart: false,
  modalPaymentStart2: false,
  modalPaymentModal: false,
});

export const mutations = {
  setModalPaymentStart(state, val) {
    state.modalPaymentStart = val;
    if (val) {
      state.modalPaymentStart2 = false;
      state.modalPaymentModal = false;
    }
  },
  setModalPaymentStart2(state, val) {
    state.modalPaymentStart2 = val;
    if (val) {
      state.modalPaymentStart = false;
      state.modalPaymentModal = false;
    }
  },
  setModalPaymentModal(state, val) {
    state.modalPaymentModal = val;
    if (val) {
      state.modalPaymentStart = false;
      state.modalPaymentStart2 = false;
    }
  },
};
