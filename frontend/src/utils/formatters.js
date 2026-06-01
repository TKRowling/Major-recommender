export const formatPercent = (value) => {
  const num = Number(value ?? 0);
  return `${num.toFixed(2)}%`;
};