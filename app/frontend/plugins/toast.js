/* eslint-disable no-console */

export default function ({ $toast }, inject) {
  // options to the toast
  const options = {
    duration: 3000,
    containerClass: 'toast',
  };

  // register the toast with the custom message
  $toast.register(
    'default',
    (payload) => {
      if (!payload.message) {
        return 'Успешно';
      }

      return payload.message;
    },
    {
      ...options,
      ...{
        type: 'default',
      },
    }
  );

  $toast.register(
    'success',
    (payload) => {
      if (!payload.message) {
        return 'Успешно';
      }

      return payload.message;
    },
    {
      ...options,
      ...{
        type: 'success',
      },
    }
  );

  $toast.register(
    'error',
    (payload) => {
      if (!payload.message) {
        return 'Ошбика';
      }

      return payload.message;
    },
    {
      ...options,
      ...{
        type: 'error',
      },
    }
  );
}
