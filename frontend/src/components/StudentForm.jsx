import React, { useState } from "react";
import "../styles/app.css";

const StudentForm = ({ onStart }) => {
  const [firstName, setFirstName] = useState("");
  const [email, setEmail] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (onStart) {
      onStart({ firstName, email });
      return;
    }

    console.log("Assessment started:", { firstName, email });
  };

  return (
    <div className="hero-form-card">
      <h2 className="hero-form-card__title">Find Your Suitable Major</h2>
      <p className="hero-form-card__subtitle">ChomNeanh AI is free for students</p>

      <form onSubmit={handleSubmit} className="hero-form">
        <input
          type="text"
          placeholder="Your First Name"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
          className="hero-form__input"
        />

        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="hero-form__input"
        />

        <button type="submit" className="hero-form__button">
          START THE ASSESSMENT
        </button>
      </form>
    </div>
  );
};

export default StudentForm;