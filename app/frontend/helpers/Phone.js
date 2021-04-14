export const phoneMaskCleared = (phone) => {
  return phone.replace(/[^A-Z0-9]/gi, '');
};
