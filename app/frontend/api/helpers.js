export const mapApiError = (error) => {
  return {
    data: error.data,
    code: error.status,
  };
};

export const mapData = (data) => {
  return data;
};
