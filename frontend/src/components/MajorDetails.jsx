import UniversityList from './UniversityList';

function MajorDetails({ selectedMajor }) {
  if (!selectedMajor) {
    return (
      <div className="card">
        <h2>Major Details</h2>
        <p>Select a recommended major to view more details.</p>
      </div>
    );
  }

  return (
    <div className="card">
      <h2>{selectedMajor.name}</h2>
      <p>{selectedMajor.description}</p>

      <h3>Related Skills</h3>
      <ul>
        {selectedMajor.skills.map((skill, index) => (
          <li key={index}>{skill}</li>
        ))}
      </ul>

      <h3>Career Paths</h3>
      <ul>
        {selectedMajor.careerPaths.map((career, index) => (
          <li key={index}>{career}</li>
        ))}
      </ul>

      <UniversityList universities={selectedMajor.universities} />
    </div>
  );
}

export default MajorDetails;