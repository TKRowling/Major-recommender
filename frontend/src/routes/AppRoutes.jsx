import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import RecommendationPage from "../pages/RecommendationPage";
import MacroMajorDetailPage from "../pages/MacroMajorDetailPage";
import ChatbotPage from "../pages/ChatbotPage";
import NotFound from "../pages/NotFound";

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/recommendation" element={<RecommendationPage />} />
      <Route path="/macro-major-detail" element={<MacroMajorDetailPage />} />
      <Route path="/chatbot" element={<ChatbotPage />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
}

export default AppRoutes;