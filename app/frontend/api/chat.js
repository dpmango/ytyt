import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const filesService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.chat.files, request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
