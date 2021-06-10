const formatBytes = (bytes, decimals = 2) => {
  if (bytes === 0) return '0 Bytes';

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['байт', 'Кб', 'Мб', 'Гб', 'Тб'];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
};

const bytesToMegaBytes = (bytes) => {
  if (bytes === 0) return null;

  const k = 1024;

  return Math.round((bytes / (k * k)) * 1e2) / 1e2;
};

export { formatBytes, bytesToMegaBytes };
