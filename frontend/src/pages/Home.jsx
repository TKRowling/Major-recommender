import React from "react";
import Navbar from "../components/Navbar";
import HeroSection from "../components/HeroSection";
import "../styles/app.css";
import ChatbotWidget from "../components/ChatbotWidget";
import ExplorationSection from "../components/ExplorationSection";
import TestimonialSection from "../components/TestimonialSection";

function Home() {
  return (
    <div className="landing-page">
      <HeroSection />
      <TestimonialSection />
      <ExplorationSection />
      <ChatbotWidget />
    </div>
  );
}

export default Home;