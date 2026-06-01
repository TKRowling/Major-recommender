import { formatPercent } from "../utils/formatters";

function MacroMajorCard({ item, onViewDetail, rank }) {
  const rankLabelMap = {
    1: "Best Match",
    2: "Alternative Path",
    3: "Explore Option",
  };

  return (
    <div className="macro-card">
      <div className="macro-card-rank">
        #{rank} {rankLabelMap[rank]}
      </div>

      <div className="macro-card-header">
        <h3>{item.macro_major}</h3>
      </div>

      <p className="score-text">
        Match Score: {formatPercent(item.score)}
      </p>

      <button className="secondary-btn" onClick={() => onViewDetail(item)}>
        View Detail
      </button>
    </div>
  );
}

export default MacroMajorCard;