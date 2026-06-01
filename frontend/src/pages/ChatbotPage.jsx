import React, { useMemo, useRef, useState, useEffect } from "react";
import { Link } from "react-router-dom";
import "../styles/app.css";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000/api";

const SUGGESTIONS = [
  "What majors fit someone who likes math and technology?",
  "Recommend majors for business and leadership interests",
  "What universities in Cambodia offer Computer Science?",
  "What careers match Finance or Accounting?",
];

async function askChatbot(question) {
  const response = await fetch(`${API_BASE_URL}/chatbot`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.details || data.error || "Failed to get chatbot response");
  }

  return data;
}

function ChatbotPage() {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: "bot",
      text: "Hi! I’m your AI major advisor. Ask me about majors, universities, skills, or career paths.",
      time: "Now",
      sources: [],
    },
  ]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const formattedDate = useMemo(() => {
    return new Date().toLocaleDateString(undefined, {
      weekday: "long",
      month: "short",
      day: "numeric",
    });
  }, []);

  const sendMessage = async (textValue = input) => {
    const trimmed = textValue.trim();

    if (!trimmed || loading) return;

    const userMessage = {
      id: Date.now(),
      sender: "user",
      text: trimmed,
      time: "Just now",
      sources: [],
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const result = await askChatbot(trimmed);

      const botReply = {
        id: Date.now() + 1,
        sender: "bot",
        text: result.answer || "I could not generate an answer.",
        time: "Just now",
        sources: result.sources || [],
      };

      setMessages((prev) => [...prev, botReply]);
    } catch (error) {
      const errorReply = {
        id: Date.now() + 1,
        sender: "bot",
        text: `Sorry, I could not connect to the chatbot API.\n\nError: ${error.message}`,
        time: "Just now",
        sources: [],
      };

      setMessages((prev) => [...prev, errorReply]);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    sendMessage();
  };

  return (
    <div className="chatbot-page">
      <div className="chatbot-shell">
        <aside className="chatbot-sidebar">
          <Link to="/" className="chatbot-back-btn">
            ← Back to Home
          </Link>

          <div className="chatbot-brand-card">
            <div className="chatbot-brand-icon">AI</div>
            <div>
              <h2>AI Chatbot</h2>
              <p>Your major and career guidance assistant</p>
            </div>
          </div>

          <div className="chatbot-side-section">
            <h4>What you can ask</h4>
            <ul>
              <li>Best-fit majors</li>
              <li>University suggestions</li>
              <li>Career options</li>
              <li>Skill-based advice</li>
            </ul>
          </div>
        </aside>

        <main className="chatbot-main">
          <div className="chatbot-header">
            <div>
              <h1>AI Major Advisor</h1>
              <p>Ask about majors, universities, and career paths</p>
            </div>
            <span className="chatbot-date">{formattedDate}</span>
          </div>

          <div className="chatbot-suggestions">
            {SUGGESTIONS.map((item, index) => (
              <button
                key={index}
                type="button"
                className="chatbot-chip"
                onClick={() => sendMessage(item)}
                disabled={loading}
              >
                {item}
              </button>
            ))}
          </div>

          <div className="chatbot-messages">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`chatbot-message-row ${
                  message.sender === "user" ? "user" : "bot"
                }`}
              >
                <div
                  className={`chatbot-avatar ${
                    message.sender === "user" ? "user" : "bot"
                  }`}
                >
                  {message.sender === "user" ? "U" : "AI"}
                </div>

                <div
                  className={`chatbot-bubble ${
                    message.sender === "user" ? "user" : "bot"
                  }`}
                >
                  <p>{message.text}</p>



                  <span>{message.time}</span>
                </div>
              </div>
            ))}

            {loading && (
              <div className="chatbot-message-row bot">
                <div className="chatbot-avatar bot">AI</div>
                <div className="chatbot-bubble bot">
                  <p>Generating answer...</p>
                  <span>Just now</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <form className="chatbot-input-bar" onSubmit={handleSubmit}>
            <input
              type="text"
              placeholder="Ask about majors, universities, or careers..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={loading}
            />
            <button type="submit" disabled={loading}>
              {loading ? "Sending..." : "Send"}
            </button>
          </form>
        </main>
      </div>
    </div>
  );
}

export default ChatbotPage;