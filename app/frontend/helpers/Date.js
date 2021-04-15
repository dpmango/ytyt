import dayjs from 'dayjs';
import 'dayjs/locale/ru';
dayjs.locale('ru');

export const djs = (x) => {
  return dayjs(x);
};

export const timeToTimeStamp = (time) => {
  const djsTime = dayjs(time * 1000);
  let mask = 'DD MMM, HH:mm';

  if (djs().year() !== djsTime.year()) {
    mask = 'DD MMM YYYY, HH:mm';
  }

  return djsTime.format(mask);
};

export const timeToHHMM = (time) => {
  return dayjs(time * 1000).format('HH:mm');
};

export const HHMMtoSeconds = (str) => {
  const [h, m] = str.split(':');

  if (h && m) {
    return +h * 60 * 60 + +m * 60;
  }

  return 0;
};
