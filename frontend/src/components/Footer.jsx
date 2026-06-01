import React from "react";
import { Link } from "react-router-dom";
import "../styles/app.css";

function Footer() {
  return (
    <footer className="footer">
      <div className="footer-container">
        
        {/* LEFT - BRAND */}
        <div className="footer-brand">
          <h3>ChomNeanh AI</h3>
          <p>
            AI-powered platform to help students discover suitable majors
            based on their interests, strengths, and academic profile.
          </p>
        </div>

        {/* CENTER - NAVIGATION */}
        <div className="footer-links">
          <h4>Navigation</h4>
          <Link to="/">Home</Link>
          <Link to="/recommendation">Recommendation</Link>
          <Link to="/chatbot">Chatbot</Link>
          <Link to="/about">About us</Link>
        </div>

        {/* RIGHT - FEATURES */}
        <div className="footer-links">
          <h4>Features</h4>
          <Link to="/recommendation">Major Recommendation</Link>
          <Link to="/chatbot">AI Chatbot</Link>
          <Link to="/history">History</Link>
        </div>
      </div>

      {/* BOTTOM */}
      <div className="footer-bottom">
        <p>© 2026 ChomNeanh AI | AI-Based Major Recommendation System</p>
      </div>
    </footer>
  );
}

export default Footer;