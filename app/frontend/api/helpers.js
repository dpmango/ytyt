export const mapApiError = (error) => {
  let message = error.data;

  // TODO - refactor to case switch
  if (error.status === 500) {
    message = 'Ошибка сервера';
  }

  return {
    data: message,
    code: error.status,
  };
};

export const mapData = (data) => {
  return data;
};
