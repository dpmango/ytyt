import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const initService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.payment.init, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const initInstallmentService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.payment.initInstallment, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
