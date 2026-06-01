import { useState } from "react";
import { fetchRecommendations } from "../api/recommendationApi";

const RESULT_STORAGE_KEY = "recommendation_results";

export default function useRecommendation() {
  const [recommendations, setRecommendations] = useState(() => {
    const saved = sessionStorage.getItem(RESULT_STORAGE_KEY);
    return saved ? JSON.parse(saved) : [];
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getRecommendations = async (payload) => {
    try {
      setLoading(true);
      setError("");

      const result = await fetchRecommendations(payload);
      const newRecommendations = result?.data?.recommendations || [];

      setRecommendations(newRecommendations);
      sessionStorage.setItem(
        RESULT_STORAGE_KEY,
        JSON.stringify(newRecommendations)
      );
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to load recommendations");
      setRecommendations([]);
      sessionStorage.removeItem(RESULT_STORAGE_KEY);
    } finally {
      setLoading(false);
    }
  };

  return {
    recommendations,
    setRecommendations,
    loading,
    error,
    getRecommendations,
  };
}