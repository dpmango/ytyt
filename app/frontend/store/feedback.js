import { feedbackService } from '~/api/feedback';

export const actions = {
  async feedback({ commit }, request) {
    const [err, result] = await feedbackService(this.$api, request);

    if (err) throw err;

    return result;
  },
};
