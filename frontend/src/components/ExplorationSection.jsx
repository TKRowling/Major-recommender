import React from "react";
import { Link } from "react-router-dom";
import systemIcon from "../assets/icons8-system.png";
import chatbotIcon from "../assets/icons8-chatbot.png";
import aboutIcon from "../assets/icons8-about-me.png";
import "../styles/app.css";

const features = [
  {
    title: "Recommendation System",
    description:
      "Get personalized major recommendations based on your interests, strengths, hobbies, and academic profile. Explore the majors that best match your potential.",
    buttonText: "START NOW",
    buttonClass: "exploration-btn blue",
    link: "/recommendation",
    icon: systemIcon,
    alt: "Recommendation System",
  },
  {
    title: "AI Chatbot",
    description:
      "Ask questions about majors, careers, universities, and study paths. Get quick support and guidance through our intelligent chatbot assistant.",
    buttonText: "CHAT NOW",
    buttonClass: "exploration-btn red",
    link: "/chatbot",
    icon: chatbotIcon,
    alt: "AI Chatbot",
  },
  {
    title: "About Us",
    description:
      "Learn more about ChomNeanh AI, our mission, and how this platform helps students discover suitable majors and make confident academic decisions.",
    buttonText: "LEARN MORE",
    buttonClass: "exploration-btn green",
    link: "/about",
    icon: aboutIcon,
    alt: "About Us",
  },
];

function ExplorationSection() {
  return (
    <section className="exploration-section">
      <div className="exploration-header">
        <h2>Explore ChomNeanh AI</h2>
        <p>Discover the key features of our platform.</p>
      </div>

      <div className="exploration-grid">
        {features.map((item, index) => (
          <div className="exploration-card" key={index}>
            <div className="exploration-icon-box">
              <img src={item.icon} alt={item.alt} className="exploration-icon-img" />
            </div>

            <h3>{item.title}</h3>
            <p>{item.description}</p>

            <Link to={item.link} className={item.buttonClass}>
              {item.buttonText}
            </Link>
          </div>
        ))}
      </div>
    </section>
  );
}

export default ExplorationSection;