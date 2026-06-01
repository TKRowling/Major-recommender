import React from "react";
import { useNavigate } from "react-router-dom";
import chatbotIcon from "../assets/chatbot.png"; 
import "../styles/app.css";

const ChatbotWidget = () => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate("/chatbot");
  };

  return (
    <div className="chatbot-widget" onClick={handleClick}>
      <img src={chatbotIcon} alt="Chatbot" />
    </div>
  );
};

export default ChatbotWidget;