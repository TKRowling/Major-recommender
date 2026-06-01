export const normalizeChartValue = (value) => {
  const num = Number(value || 0);
  return Math.max(0, Math.min(100, (num / 5) * 100));
};