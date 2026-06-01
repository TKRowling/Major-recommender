import axios from "./axios";

export const fetchRecommendations = async (payload) => {
  const response = await axios.post("/recommend", payload);
  return response.data;
};

export const fetchHistory = async () => {
  const response = await axios.get("/history");
  return response.data;
};