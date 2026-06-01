import RecommendationCard from './RecommendationCard';

function RecommendationList({ recommendations, onSelect }) {
  return (
    <div className="card">
      <h2>Top 3 Recommended Majors</h2>
      <div className="recommend-grid">
        {recommendations.length > 0 ? (
          recommendations.map((item, index) => (
            <RecommendationCard
              key={index}
              major={item.major}
              score={item.score}
              onSelect={onSelect}
            />
          ))
        ) : (
          <p>No recommendations yet. Submit the form first.</p>
        )}
      </div>
    </div>
  );
}

export default RecommendationList;