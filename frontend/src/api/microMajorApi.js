import api from "./axios";

export const fetchMicroMajors = async (payload) => {
  const response = await api.post("/micro-majors", payload);
  return response.data;
};