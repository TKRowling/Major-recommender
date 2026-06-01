// import { useLocation, useNavigate } from "react-router-dom";
// import { useState } from "react";
// import FeatureImportanceChart from "../components/FeatureImportanceChart";

// function MacroMajorDetailPage() {
//   const location = useLocation();
//   const navigate = useNavigate();
//   const [openOriginalClass, setOpenOriginalClass] = useState(null);

//   const selectedMacroMajor = location.state?.selectedMacroMajor;

//   const toggleOriginalClass = (originalClass) => {
//     setOpenOriginalClass((prev) =>
//       prev === originalClass ? null : originalClass
//     );
//   };

//   if (!selectedMacroMajor) {
//     return (
//       <div className="page-container">
//         <div className="macro-card">
//           <h2>No detail data found.</h2>
//           <button
//             className="secondary-btn"
//             onClick={() => navigate("/recommendation")}
//           >
//             Back to Recommendation
//           </button>
//         </div>
//       </div>
//     );
//   }

//   return (
//     <div className="page-container">
//       <button
//         className="secondary-btn back-btn"
//         onClick={() => navigate("/recommendation")}
//       >
//         ← Back
//       </button>

//       <div className="macro-card macro-card-detail">
//         <div className="macro-card-header">
//           <h2>{selectedMacroMajor.macro_major}</h2>
//         </div>

//         <p className="score-text">
//           <strong>Match Score:</strong> {(selectedMacroMajor.score ?? 0).toFixed(2)}%
//         </p>

//         <p className="score-text">
//           <strong>Confidence:</strong> {(selectedMacroMajor.confidence ?? 0).toFixed(2)}%
//         </p>

//         <div className="detail-section">
//           <h3>Why this major was recommended</h3>
//           <p>{selectedMacroMajor.why_recommended || "No explanation available."}</p>
//         </div>

//         <div className="detail-section">
//           <h3>Feature Importance</h3>
//           <FeatureImportanceChart
//             items={selectedMacroMajor.feature_importance || []}
//           />
//         </div>

//         <div className="detail-section">
//           <h3>Original class options</h3>

//           {!selectedMacroMajor.original_class_suggestions?.length ? (
//             <p>No original class suggestions available.</p>
//           ) : (
//             <div className="original-class-list">
//               {selectedMacroMajor.original_class_suggestions.map((item, index) => {
//                 const isOpen = openOriginalClass === item.original_class;

//                 return (
//                   <div
//                     key={`${item.original_class}-${index}`}
//                     className="original-class-card"
//                   >
//                     <button
//                       type="button"
//                       className="original-class-toggle"
//                       onClick={() => toggleOriginalClass(item.original_class)}
//                     >
//                       <div>
//                         <strong>{item.original_class}</strong>
//                         <div className="fit-score-text">
//                           Fit Score: {item.fit_score}
//                         </div>
//                       </div>
//                       <span>{isOpen ? "−" : "+"}</span>
//                     </button>

//                     {isOpen && (
//                       <div className="micro-major-panel">
//                         <h4>Top 3 Micro Majors</h4>

//                         {item.top_micro_majors?.length ? (
//                           <ul className="micro-major-list">
//                             {item.top_micro_majors.map((micro, microIndex) => (
//                               <li key={`${micro}-${microIndex}`}>{micro}</li>
//                             ))}
//                           </ul>
//                         ) : (
//                           <p>No micro majors available.</p>
//                         )}
//                       </div>
//                     )}
//                   </div>
//                 );
//               })}
//             </div>
//           )}
//         </div>
//       </div>
//     </div>
//   );
// }

// export default MacroMajorDetailPage;
import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";
import FeatureImportanceChart from "../components/FeatureImportanceChart";

function MacroMajorDetailPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const [openOriginalClass, setOpenOriginalClass] = useState(null);

  const selectedMacroMajor = location.state?.selectedMacroMajor;

  const toggleOriginalClass = (originalClass) => {
    setOpenOriginalClass((prev) =>
      prev === originalClass ? null : originalClass
    );
  };

  if (!selectedMacroMajor) {
    return (
      <div className="page-container">
        <div className="detail-empty-card">
          <h2>No detail data found</h2>
          <p>Please go back and generate recommendations first.</p>
          <button
            className="secondary-btn"
            onClick={() => navigate("/recommendation")}
          >
            Back to Recommendation
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container detail-page">
      <div className="detail-topbar">
        <button
          className="secondary-btn back-btn"
          onClick={() => navigate("/recommendation")}
        >
          ← Back
        </button>
      </div>

      <div className="detail-hero-card">
        <div className="detail-hero-header">
          <div>
            <span className="detail-badge">Major Detail</span>
            <h1>{selectedMacroMajor.macro_major}</h1>
          </div>
        </div>

        <div className="detail-metric-grid">
          <div className="detail-metric-card">
            <span className="metric-label">Match Score</span>
            <span className="metric-value">
              {(selectedMacroMajor.score ?? 0).toFixed(2)}%
            </span>
          </div>

          <div className="detail-metric-card">
            <span className="metric-label">Confidence</span>
            <span className="metric-value">
              {(selectedMacroMajor.confidence ?? 0).toFixed(2)}%
            </span>
          </div>
        </div>
      </div>

      <div className="detail-section-card">
        <div className="detail-section-header">
          <h2>Why this major was recommended</h2>
        </div>
        <p className="detail-paragraph">
          {selectedMacroMajor.why_recommended || "No explanation available."}
        </p>
      </div>

      <div className="detail-section-card">
        <div className="detail-section-header">
          <h2>Feature Importance</h2>
          <p>Most influential inputs for this recommendation.</p>
        </div>

        <FeatureImportanceChart
          items={selectedMacroMajor.feature_importance || []}
        />
      </div>

      <div className="detail-section-card">
        <div className="detail-section-header">
          <h2>Original class options</h2>
          <p>
            Expand each original class to explore the most relevant micro majors.
          </p>
        </div>

        {!selectedMacroMajor.original_class_suggestions?.length ? (
          <p className="detail-muted-text">
            No original class suggestions available.
          </p>
        ) : (
          <div className="original-class-list">
            {selectedMacroMajor.original_class_suggestions.map((item, index) => {
              const isOpen = openOriginalClass === item.original_class;

              return (
                <div
                  key={`${item.original_class}-${index}`}
                  className={`original-class-card ${isOpen ? "open" : ""}`}
                >
                  <button
                    type="button"
                    className="original-class-toggle"
                    onClick={() => toggleOriginalClass(item.original_class)}
                  >
                    <div className="original-class-info">
                      <div className="original-class-title-row">
                        <strong>{item.original_class}</strong>
                        <span className="fit-score-pill">
                          Fit Score: {item.fit_score}
                        </span>
                      </div>
                    </div>

                    <span className="accordion-icon">{isOpen ? "−" : "+"}</span>
                  </button>

                  {isOpen && (
                    <div className="micro-major-panel">
                      <h3>Top 3 Micro Majors</h3>

                      {item.top_micro_majors?.length ? (
                        <div className="micro-major-chip-list">
                          {item.top_micro_majors.map((micro, microIndex) => (
                            <span
                              key={`${micro}-${microIndex}`}
                              className="micro-major-chip"
                            >
                              {micro}
                            </span>
                          ))}
                        </div>
                      ) : (
                        <p className="detail-muted-text">
                          No micro majors available.
                        </p>
                      )}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

export default MacroMajorDetailPage;