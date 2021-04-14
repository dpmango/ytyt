export const convertIdsToArray = (arr) => {
  if (typeof arr === 'number') {
    return [arr];
  } else if (typeof arr === 'string') {
    return [parseInt(arr)];
  }

  return arr;
};

export const addOrRemoveFromArray = (arr, action, active_arr) => {
  // add / remove (transform request array)
  // based on action
  if (action === 'add') {
    return [...new Set(arr.concat(...active_arr))];
  } else if (action === 'remove') {
    return active_arr.filter((x) => !arr.includes(x));
  }

  return arr;
};
