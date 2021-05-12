import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const getService = async ($api) => {
  try {
    const { data } = await $api.get(endpoints.constants.get);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
