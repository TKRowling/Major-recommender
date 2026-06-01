const FAVORITE_SUBJECT_OPTIONS = [
  "Accounting",
  "Art / Design",
  "Biology",
  "Business",
  "Chemistry",
  "Computer Science / ICT",
  "Economics",
  "English",
  "Geography",
  "History",
  "Khmer Literature",
  "Mathematics",
  "Physics",
];

const GOOD_AT_SUBJECT_OPTIONS = [
  "Accounting",
  "Art / Design",
  "Biology",
  "Business",
  "Chemistry",
  "Computer Science / ICT",
  "Economics",
  "English",
  "Geography",
  "History",
  "Khmer Literature",
  "Mathematics",
  "Physics",
];

const INTEREST_OPTIONS = [
  "Agriculture",
  "Business / Entrepreneurship",
  "Creative Arts",
  "Education / Teaching",
  "Engineering / Building things",
  "Environment / Sustainability",
  "Finance / Investment",
  "Healthcare / Medicine",
  "Law / Politics",
  "Media / Communication",
  "Psychology / Human behavior",
  "Research / Science",
  "Social Work",
  "Technology / AI",
  "Tourism / Hospitality",
];

const HOBBY_OPTIONS = [
  "Coding / Programming",
  "DIY / Building projects",
  "Debate / Public speaking",
  "Drawing / Design",
  "Gaming",
  "Listening Music",
  "Online Business",
  "Photography / Videography",
  "Reading",
  "Social Media Content Creation",
  "Sports",
  "Stock / Crypto trading",
  "Tutoring friends",
  "Volunteering",
  "Writing",
];

const WORK_STYLE_OPTIONS = [
  "Working with numbers",
  "Working with people",
  "Working with machines / technology",
  "Working in creative / art fields",
  "Working outdoors",
  "Business / Management roles"
];

const FUTURE_WORKPLACE_OPTIONS = [
  "Private Company",
  "Government",
  "Non-Governmental Organization (NGO)",
  "Start my own business"
];

function UserForm({ onSubmit, loading, formData, setFormData }) {
  const handleCheckboxChange = (field, value) => {
  setFormData((prev) => {
    const currentValues = prev[field] || [];
    const exists = currentValues.includes(value);

    return {
      ...prev,
      [field]: exists
        ? currentValues.filter((item) => item !== value)
        : [...currentValues, value],
    };
  });
};

  const renderCheckboxGroup = (title, field, options) => {
    const descriptions = {
      favorite_subjects_sorted:
        "Choose the school subjects you enjoy the most.",
      good_at_subjects_sorted:
        "Choose the subjects where you feel most confident.",
      interests_sorted:
        "Choose the fields or career areas that attract you.",
      hobbies_sorted:
        "Choose the activities you usually enjoy in your free time.",
      work_style: 
        "Choose the work style that matches how you prefer to work.",
      future_workplace: 
        "Choose the type of workplace you prefer in the future.",
    };

    return (
      <section className="form-section">
        <div className="section-header">
          <h3>{title}</h3>
          <p>{descriptions[field]}</p>
        </div>

        <div className="checkbox-grid">
          {options.map((option) => (
            <label key={option} className="checkbox-item">
              <input
                type="checkbox"
                checked={formData[field].includes(option)}
                onChange={() => handleCheckboxChange(field, option)}
              />
              <span>{option}</span>
            </label>
          ))}
        </div>
      </section>
    );
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="card form-card">
      <div className="form-header">
        <span className="form-badge">Step 1</span>
        <h2>Student Preference Profile</h2>
        <p>
          Select the subjects, interests, and activities that best describe
          you.
        </p>
      </div>

      <form className="student-form" onSubmit={handleSubmit}>
        <div className="form-group-block">
          <h3 className="group-block-title">Academic Profile</h3>

          {renderCheckboxGroup(
            "Subjects You Enjoy",
            "favorite_subjects_sorted",
            FAVORITE_SUBJECT_OPTIONS
          )}

          {renderCheckboxGroup(
            "Subjects You Are Strong In",
            "good_at_subjects_sorted",
            GOOD_AT_SUBJECT_OPTIONS
          )}
        </div>

        <div className="form-group-block">
          <h3 className="group-block-title">Personal Profile</h3>

          {renderCheckboxGroup(
            "Career Interests",
            "interests_sorted",
            INTEREST_OPTIONS
          )}

          {renderCheckboxGroup(
            "Activities and Hobbies",
            "hobbies_sorted",
            HOBBY_OPTIONS
          )}

          {renderCheckboxGroup(
            "Preferred Work Style",
            "work_style",
            WORK_STYLE_OPTIONS
          )}

          {renderCheckboxGroup(
            "Preferred Future Workplace",
            "future_workplace",
            FUTURE_WORKPLACE_OPTIONS
          )}
        </div>

        <button type="submit" className="primary-btn" disabled={loading}>
          {loading ? "Analyzing your profile..." : "Get Top 3 Recommendations"}
        </button>
      </form>
    </div>
  );
}

export default UserForm;