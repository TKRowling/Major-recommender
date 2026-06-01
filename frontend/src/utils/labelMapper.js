export const confidenceColor = (label) => {
  if (label === "High Match") return "high";
  if (label === "Moderate Match") return "moderate";
  return "low";
};