import React from "react";
import { Link } from "react-router-dom";
import "../styles/app.css";

const Navbar = () => {
  return (
    <header className="landing-navbar">
      <div className="landing-navbar__container">
        <div className="landing-navbar__brand">
          <Link to="/" className="landing-navbar__logo">
            <img src="/ChomNeang AI logo.png" alt="ChomNeang AI" />
          </Link>
        </div>

        <nav className="landing-navbar__menu">
          <Link to="/">Home</Link>
          <Link to="/recommendation">Recommendation</Link>
          <Link to="/history">History</Link>

          {/* FIX HERE */}
          <Link to="/login" className="landing-navbar__login">
            Login
          </Link>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;