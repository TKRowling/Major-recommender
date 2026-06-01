import React from "react";
import { useNavigate } from "react-router-dom";
import StudentForm from "./StudentForm";
import "../styles/app.css";

const HeroSection = () => {
  const navigate = useNavigate();

  const handleStart = (formData) => {
    console.log("User clicked start:", formData);
    navigate("/recommendation");
  };

  return (
    <section className="hero-section">
      <div className="hero-overlay" />
      <div className="hero-content">
        <div className="hero-text">
          <h1>
            What&apos;s Your
            <br />
            Ideal Major?
          </h1>

          <h3>Finding the right major can be challenging.</h3>

          <p>
            ChomNeanh AI is a free AI-powered tool that helps students discover suitable
            majors based on their interests, strengths, and academic preferences.
            Start your journey toward the right future today.
          </p>
        </div>

        <div className="hero-form-wrapper">
          <StudentForm onStart={handleStart} />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;