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

export const refreshTokenService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.refreshToken, request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const verifyGetService = async ($api, params) => {
  try {
    const { data } = await $api.patch(endpoints.auth.verifyEmail, params);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const verifyPostService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.verifyEmail, request);

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

export const recoverConfirmationService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.passwordResetConfirm, {
      ...request,
    });

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};

export const passwordChangeService = async ($api, request) => {
  try {
    const { data } = await $api.post(endpoints.auth.passwordChange, {
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

export const updateUserService = async ($api, request) => {
  try {
    const { data } = await $api.patch(endpoints.auth.user, request);

    return [null, mapData(data)];
  } catch (error) {
    return [mapApiError(error), null];
  }
};
