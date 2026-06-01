function UniversityList({ universities }) {
  return (
    <div>
      <h3>Universities in Cambodia</h3>
      <ul>
        {universities.map((uni, index) => (
          <li key={index}>{uni}</li>
        ))}
      </ul>
    </div>
  );
}

export default UniversityList;