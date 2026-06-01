import { useState } from "react";
import { fetchMicroMajors } from "../api/microMajorApi";

export default function useMicroMajor() {
  const [microMajors, setMicroMajors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const getMicroMajors = async (payload) => {
    try {
      setLoading(true);
      setError("");

      const result = await fetchMicroMajors(payload);
      setMicroMajors(result?.data?.micro_majors || []);
    } catch (err) {
      setError(err?.response?.data?.message || "Failed to load micro majors");
    } finally {
      setLoading(false);
    }
  };

  return {
    microMajors,
    loading,
    error,
    getMicroMajors,
  };
}