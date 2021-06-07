import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const feedbackService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.feedback.base, {
      ...request,
      ...{ phone: request.phone.replace(/[^A-Z0-9]/gi, '') },
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
