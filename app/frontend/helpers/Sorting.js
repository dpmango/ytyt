const getMeta = (a, b, property) => {
  if (!a.meta || !b.meta) {
    return null;
  }

  const meta = [JSON.parse(a.meta), JSON.parse(b.meta)];

  return [meta[0][property], meta[1][property]];
};

export const sortNumber = (a, b, property, direction, isMeta) => {
  if (isMeta) {
    const meta = getMeta(a, b, property);
    if (meta === null) return 0;

    const [aVal, bVal] = meta;

    if (aVal === null || aVal === undefined) {
      aVal = 0;
    }
    if (bVal === null || bVal === undefined) {
      bVal = 0;
    }

    if (direction === 1) {
      return aVal - bVal;
    } else if (direction === 2) {
      return bVal - aVal;
    }
  }

  if (direction === 1) {
    return a[property] - b[property];
  } else if (direction === 2) {
    return b[property] - a[property];
  }
};

export const sortString = (a, b, property, direction, isMeta) => {
  if (isMeta) {
    const meta = getMeta(a, b, property);
    if (meta === null) return 0;

    const [aVal, bVal] = meta;

    if (aVal === null || aVal === undefined) {
      aVal = '';
    }
    if (bVal === null || bVal === undefined) {
      bVal = '';
    }

    if (direction === 1) {
      return aVal < bVal ? -1 : 1;
    } else if (direction === 2) {
      return aVal < bVal ? 1 : -1;
    }
  }

  if (direction === 1) {
    return a[property] < b[property] ? -1 : 1;
  } else if (direction === 2) {
    return a[property] < b[property] ? 1 : -1;
  }
};

export const sortDiscountCustom = (a, b, direction) => {
  const meta = [JSON.parse(a.meta), JSON.parse(b.meta)];

  let aCost = meta[0].cost;
  const bCost = meta[1].cost;
  const aCostWDiscount = meta[0].cost_with_discount;
  const bCostWDiscount = meta[1].cost_with_discount;

  if (aCost === null || aCost === undefined) {
    aCost = 0;
  }
  if (bCost === null || bCost === undefined) {
    aCost = 0;
  }
  if (aCostWDiscount === null || aCostWDiscount === undefined) {
    aCost = 0;
  }
  if (bCostWDiscount === null || bCostWDiscount === undefined) {
    aCost = 0;
  }

  const aVal = Math.round(((aCost - aCostWDiscount) / aCost) * 100);
  const bVal = Math.round(((bCost - bCostWDiscount) / bCost) * 100);

  if (direction === 1) {
    return aVal < bVal ? -1 : 1;
  } else if (direction === 2) {
    return aVal < bVal ? 1 : -1;
  }
};
