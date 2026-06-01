function RecommendationCard({ major, score, onSelect }) {
  return (
    <div className="recommend-card" onClick={() => onSelect(major)}>
      <h3>{major.name}</h3>
      <p>{major.description}</p>
      <span className="score">Match Score: {score}</span>
    </div>
  );
}

export default RecommendationCard;