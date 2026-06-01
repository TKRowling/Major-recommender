import React from "react";
import { Link } from "react-router-dom";
import recommendationIcon from "../assets/icons8-system.png";
import chatbotIcon from "../assets/icons8-chatbot.png";
import aboutIcon from "../assets/icons8-about-me.png";
import "../styles/app.css";

function AboutPage() {
  const features = [
    {
      title: "Recommendation System",
      text: "Analyzes student interests, strengths, and preferences to suggest suitable majors.",
      icon: recommendationIcon,
    },
    {
      title: "AI Chatbot",
      text: "Provides quick answers about majors, careers, universities, and academic pathways.",
      icon: chatbotIcon,
    },
    {
      title: "Student Guidance",
      text: "Supports students in making more confident academic and future career decisions.",
      icon: aboutIcon,
    },
  ];

  return (
    <div className="about-page">
      <section className="about-hero">
        <div className="about-hero__container">
          <div className="about-hero__text">
            <span className="about-badge">About ChomNeanh AI</span>
            <h1>Helping students discover the right major with confidence</h1>
            <p>
              ChomNeanh AI is an intelligent major recommendation platform built
              to help students explore suitable academic pathways based on their
              interests, strengths, and personal preferences.
            </p>

            <div className="about-hero__actions">
              <Link to="/recommendation" className="about-primary-btn">
                Try Recommendation
              </Link>
              <Link to="/chatbot" className="about-secondary-btn">
                Ask AI Chatbot
              </Link>
            </div>
          </div>

          <div className="about-hero__card">
            <h3>What ChomNeanh AI does</h3>
            <ul>
              <li>Suggests suitable majors from student profile data</li>
              <li>Provides AI support for questions and exploration</li>
              <li>Helps students understand options before deciding</li>
              <li>Encourages better academic and career planning</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="about-story">
        <div className="about-section__container">
          <div className="about-section__header">
            <h2>Our Mission</h2>
            <p>
              We aim to make major exploration easier, more personalized, and
              more accessible for students.
            </p>
          </div>

          <div className="about-story__content">
            <div className="about-story__card">
              <h3>Why we built it</h3>
              <p>
                Many students are unsure which major best fits their interests
                and abilities. ChomNeang AI was created to reduce that
                uncertainty and provide a more guided, data-driven experience.
              </p>
            </div>

            <div className="about-story__card">
              <h3>What makes it useful</h3>
              <p>
                The platform combines recommendation logic, chatbot assistance,
                and structured exploration tools into one system, giving
                students both guidance and flexibility.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="about-features">
        <div className="about-section__container">
          <div className="about-section__header">
            <h2>Core Features</h2>
            <p>
              The platform is designed around practical tools that support real
              student decision-making.
            </p>
          </div>

          <div className="about-features__grid">
            {features.map((item, index) => (
              <div className="about-feature-card" key={index}>
                <div className="about-feature-card__icon">
                  <img src={item.icon} alt={item.title} />
                </div>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="about-impact">
        <div className="about-section__container">
          <div className="about-impact__box">
            <h2>Why it matters</h2>
            <p>
              Choosing the right major can shape academic success, confidence,
              and long-term career direction. ChomNeang AI helps students make
              that choice with more clarity and support.
            </p>
            <Link to="/recommendation" className="about-primary-btn">
              Start Exploring
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}

export default AboutPage;