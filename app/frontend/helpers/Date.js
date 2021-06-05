import dayjs from 'dayjs';
import 'dayjs/locale/ru';
dayjs.locale('ru');

export const djs = (x) => {
  return dayjs(x);
};

export const isToday = (date) => djs().diff(date, 'days') === 0;

export const timeToTimeStamp = (time) => {
  const djsTime = djs(time);
  let mask = 'DD MMM, HH:mm';

  if (isToday(djsTime)) {
    mask = 'HH:mm';
  } else if (djs().year() !== djsTime.year()) {
    mask = 'DD MMM YYYY, HH:mm';
  }

  return djsTime.format(mask);
};

export const timeToHHMM = (time) => {
  return djs(time).format('HH:mm');
};

export const HHMMtoSeconds = (str) => {
  const [h, m] = str.split(':');

  if (h && m) {
    return +h * 60 * 60 + +m * 60;
  }

  return 0;
};
