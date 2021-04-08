import endpoints from './endpoints';
import { mapApiError, mapData } from './helpers';

export const loginService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.login, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const signupService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.registration, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const recoverService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.passwordReset, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const logoutService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.logout);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const userService = async ($api) => {
  try {
    const { data } = await $api.get(endpoints.auth.user);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
