import { useEffect, useState } from "react";
import { fetchHistory } from "../api/recommendationApi";

function HistoryPage() {
  const [rows, setRows] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const result = await fetchHistory();
        setRows(result?.data || []);
      } catch (err) {
        setError(err?.response?.data?.message || "Failed to load history");
      }
    };
    load();
  }, []);

  return (
    <div className="page-container">
      <div className="card">
        <h2>Recommendation History</h2>

        {error && <p className="error-text">{error}</p>}

        {!rows.length && !error ? (
          <p>No history found.</p>
        ) : (
          <div className="history-list">
            {rows.map((row) => (
              <div key={row.id} className="history-card">
                <h3>History #{row.id}</h3>
                <p><strong>Favorite Subjects:</strong> {(row.favorite_subjects || []).join(", ")}</p>
                <p><strong>Good At Subjects:</strong> {(row.good_at_subjects || []).join(", ")}</p>
                <p><strong>Interests:</strong> {(row.interests || []).join(", ")}</p>
                <p><strong>Hobbies:</strong> {(row.hobbies || []).join(", ")}</p>

                <div className="history-result">
                  <p><strong>#1:</strong> {row.top1_major} ({Number(row.top1_score || 0).toFixed(2)}%)</p>
                  <p><strong>#2:</strong> {row.top2_major} ({Number(row.top2_score || 0).toFixed(2)}%)</p>
                  <p><strong>#3:</strong> {row.top3_major} ({Number(row.top3_score || 0).toFixed(2)}%)</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default HistoryPage;