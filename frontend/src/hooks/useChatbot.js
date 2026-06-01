import { useState } from "react";
import { fetchChatbotReply } from "../api/chatbotApi";

export default function useChatbot() {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hello! I am your AI major advisor. Ask me about majors, universities, or careers."
    }
  ]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async (text) => {
    if (!text.trim()) return;

    const userMessage = { sender: "user", text };
    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);
      const result = await fetchChatbotReply(text);

      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: result?.data?.answer || "I could not answer that."
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "There was an error connecting to the chatbot service."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return {
    messages,
    loading,
    sendMessage,
  };
}