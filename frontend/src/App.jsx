import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import RecommendationPage from "./pages/RecommendationPage";
import MacroMajorDetailPage from "./pages/MacroMajorDetailPage";
import HistoryPage from "./pages/HistoryPage";
import ChatbotPage from "./pages/ChatbotPage";
import AboutPage from "./pages/AboutPage";
import Footer from "./components/Footer";
import LoginPage from "./pages/LoginPage";

function App() {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/recommendation" element={<RecommendationPage />} />
        <Route path="/macro-major-detail" element={<MacroMajorDetailPage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/chatbot" element={<ChatbotPage />} />
        <Route path="/about" element={<AboutPage />} />
        <Route path="/login" element={<LoginPage />} />
      </Routes>
      <Footer /> 
    </>
  );
}

export default App;