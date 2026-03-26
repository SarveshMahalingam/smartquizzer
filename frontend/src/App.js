import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";
import Quiz from "./pages/Quiz";
import Result from "./pages/Result";
import Leaderboard from "./pages/Leaderboard";
import Statistics from "./pages/Statistics";
import Profile from "./pages/Profile";
import QuizSetup from "./pages/QuizSetup";
import WeakTopics from "./pages/WeakTopics";


function App() {
  return (
    <Router>
      <Routes>

        <Route path="/" element={<Login />} />

        <Route path="/login" element={<Login />} />

        <Route path="/register" element={<Register />} />

        <Route path="/dashboard" element={<Dashboard />} />

        {/* Quiz Setup Page */}
        <Route path="/quizsetup" element={<QuizSetup />} />

        {/* Quiz Page */}
        <Route path="/quiz" element={<Quiz />} />

        <Route path="/result" element={<Result />} />

        <Route path="/leaderboard" element={<Leaderboard />} />

        <Route path="/stats" element={<Statistics />} />

        <Route path="/profile" element={<Profile />} />

        <Route path="/weaktopics" element={<WeakTopics />} />

      </Routes>
    </Router>
  );
}

export default App;