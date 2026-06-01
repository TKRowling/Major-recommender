import { useState } from "react";
import { useNavigate } from "react-router-dom";
import UserForm from "../components/UserForm";
import MacroMajorCard from "../components/MacroMajorCard";
import LoadingSpinner from "../components/LoadingSpinner";
import useRecommendation from "../hooks/useRecommendation";

const FORM_STORAGE_KEY = "recommendation_form_data";
const RESULT_STORAGE_KEY = "recommendation_results";

function RecommendationPage() {
  const navigate = useNavigate();
  const {
    recommendations,
    setRecommendations,
    loading,
    error,
    getRecommendations,
  } = useRecommendation();

  const [formData, setFormData] = useState(() => {
    const saved = sessionStorage.getItem(FORM_STORAGE_KEY);
    return saved
      ? JSON.parse(saved)
      : {
          favorite_subjects_sorted: [],
          good_at_subjects_sorted: [],
          interests_sorted: [],
          hobbies_sorted: [],
          work_style: [],
          future_workplace: [],
        };
  });

  const updateFormData = (updater) => {
    setFormData((prev) => {
      const next = typeof updater === "function" ? updater(prev) : updater;
      sessionStorage.setItem(FORM_STORAGE_KEY, JSON.stringify(next));
      return next;
    });
  };

  const handleViewDetail = (item) => {
    navigate("/macro-major-detail", {
      state: {
        selectedMacroMajor: item,
      },
    });
  };

  const handleReset = () => {
    const emptyForm = {
      favorite_subjects_sorted: [],
      good_at_subjects_sorted: [],
      interests_sorted: [],
      hobbies_sorted: [],
      work_style: [],
      future_workplace: [],
    };

    updateFormData(emptyForm);
    setRecommendations([]);
    sessionStorage.removeItem(FORM_STORAGE_KEY);
    sessionStorage.removeItem(RESULT_STORAGE_KEY);
  };

  return (
    <div className="page-container">
      <UserForm
        onSubmit={getRecommendations}
        loading={loading}
        formData={formData}
        setFormData={updateFormData}
      />

      <div className="page-actions">
        <button className="secondary-btn" onClick={handleReset}>
          Reset Form
        </button>
      </div>

      {loading && (
        <div className="loading-box">
          <LoadingSpinner />
          <p>Analyzing your profile and generating recommendations...</p>
        </div>
      )}

      {error && <p className="error-text">{error}</p>}

      {recommendations.length > 0 && (
        <div className="result-grid macro-card-grid">
          {recommendations.map((item, index) => (
            <MacroMajorCard
              key={`${item.macro_major}-${index}`}
              item={item}
              rank={index + 1}
              onViewDetail={handleViewDetail}
            />
          ))}
        </div>
      )}
    </div>
  );
}

export default RecommendationPage;