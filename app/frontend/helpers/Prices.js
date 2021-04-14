// 1000.00 -> 1 000.00
export const formatPrice = (num) => {
  const spacesRegex = /\B(?=(\d{3})+(?!\d))/g;
  if (num === null || num === undefined) {
    return '0.00';
  }

  if (typeof num === 'number') {
    return num.toFixed(2).replace(spacesRegex, ' ');
  }

  if (typeof num === 'string') {
    return parseFloat(num).toFixed(2).replace(spacesRegex, ' ');
  }
};

export const priceShort = (num, digits) => {
  const si = [
    { value: 1, symbol: '' },
    { value: 1e3, symbol: 'т.' },
    { value: 1e6, symbol: 'М.' },
    { value: 1e9, symbol: 'Млр.' },
    { value: 1e12, symbol: 'Трл.' },
  ];
  const rx = /\.0+$|(\.[0-9]*[1-9])0+$/;
  let i;
  for (i = si.length - 1; i > 0; i--) {
    if (num >= si[i].value) {
      break;
    }
  }
  return (num / si[i].value).toFixed(digits).replace(rx, '$1') + si[i].symbol;
};

// use (9).pad(2) // output - 09
export const PricePad = (num, size) => {
  let s = String(num);
  while (s.length < (size || 2)) {
    s = '0' + s;
  }
  return s;
};

export const floatOnly = (val) => {
  const cleanLettersRegex = /[^\d.]|\.(?=.*\.)/g;

  if (val && typeof val === 'string') {
    if (val.match(cleanLettersRegex)) {
      val = val.replace(cleanLettersRegex, '');
    }

    return val;
  }

  return null;
};

export const getFloat = (val) => {
  const valCleared = floatOnly(val);

  if (valCleared) {
    val = parseFloat(valCleared.trim());
  }

  if (isNaN(val)) {
    return null;
  }

  return val;
};

window.getFloat = getFloat;
