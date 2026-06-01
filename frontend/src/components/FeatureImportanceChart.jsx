function FeatureImportanceChart({ items = [] }) {
  if (!items.length) {
    return <p className="detail-muted-text">No feature importance available.</p>;
  }

  const maxValue = Math.max(...items.map((item) => item.importance || 0), 1);

  return (
    <div className="feature-chart">
      {items.map((item, index) => (
        <div key={index} className="feature-row">
          <div className="feature-label">{item.feature}</div>

          <div className="feature-bar-wrap">
            <div
              className="feature-bar"
              style={{
                width: `${((item.importance || 0) / maxValue) * 100}%`,
              }}
            />
          </div>

          <div className="feature-value">
            {(item.importance || 0).toFixed(2)}%
          </div>
        </div>
      ))}
    </div>
  );
}

export default FeatureImportanceChart;