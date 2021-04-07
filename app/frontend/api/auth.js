import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

// SERVICES
export const loginService = async (request) => {
  try {
    const { data } = await loginRequest(request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const signupService = async (request) => {
  try {
    const { data } = await signupRequest(request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const recoverService = async (request) => {
  try {
    const { data } = await recoverRequest(request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

// REQUEST (API ROUTE MAPPERS)
const loginRequest = (request) => {
  // TODO - any other way to acces nuxt api ?
  return window.$nuxt.$api.post(endpoints.auth.login, {
    ...request,
  });
};

const signupRequest = (request) => {
  return window.$nuxt.$api.post(endpoints.auth.registration, {
    ...request,
  });
};

const recoverRequest = (request) => {
  return window.$nuxt.$api.post(endpoints.auth.passwordReset, {
    ...request,
  });
};
