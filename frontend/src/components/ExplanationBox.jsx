function ExplanationBox({ explanation }) {
  return (
    <div className="card">
      <h3>Why this major was recommended</h3>

      <ul className="explanation-list">
        {explanation?.map((item, index) => (
          <li key={index}>
            <strong>{item.feature}:</strong> {item.message} ({item.detail})
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ExplanationBox;