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

const tmpFixFrom = (str) => {
  return str === '24:00' ? '00:00' : str;
};
const tmpFixTo = (str) => {
  return str === '0:00' ? '24:00' : str;
};

export const timeInRangeHHMM = (range, curTime) => {
  const from = HHMMtoSeconds(tmpFixFrom(range.from));
  const to = HHMMtoSeconds(tmpFixTo(range.to));
  const cur = HHMMtoSeconds(curTime);

  return cur >= from && cur <= to;
};

window.djs = djs;
