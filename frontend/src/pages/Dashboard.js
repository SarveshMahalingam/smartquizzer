import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import quizLogo from "../assets/quiz-logo.png";

function Dashboard() {

  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [quizCompleted, setQuizCompleted] = useState(false);
  const [weakTopic, setWeakTopic] = useState("");

  useEffect(() => {
    if (!token) {
      navigate("/login");
    }
  }, [token, navigate]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div style={styles.page}>

      {/* HEADER */}
      <div style={styles.header}>

        <div style={styles.logoArea}>
          <img src={quizLogo} alt="logo" style={styles.logo}/>
          <h2>NeroQuiz</h2>
        </div>

        <div style={styles.nav}>

          <button style={styles.navBtn} onClick={() => navigate("/dashboard")}>
            Dashboard
          </button>

          <button style={styles.navBtn} onClick={() => navigate("/leaderboard")}>
            Leaderboard
          </button>

          <button style={styles.navBtn} onClick={() => navigate("/stats")}>
            Statistics
          </button>

          <button style={styles.navBtn} onClick={() => navigate("/profile")}>
            Profile
          </button>

          <button style={styles.logoutBtn} onClick={logout}>
            Logout
          </button>

        </div>

      </div>


      {/* MAIN */}
      <div style={styles.container}>

        {/* LEFT */}
        <div style={styles.left}>

          <h1 style={styles.title}>Rise & Study! 🚀</h1>

          <p style={styles.subtitle}>
            Practice quizzes and track your knowledge growth.
          </p>

          <div style={styles.actions}>

            <ActionCard
              title="Start Quiz"
              desc="Choose topic and begin a quiz"
              color="#22c55e"
              onClick={() => navigate("/quizsetup")}
            />

          </div>

          {/* WEAK TOPICS */}
          <div style={styles.weakTopics}>

            <h3>⚠ Weak Topics</h3>

            <div style={styles.topicRow}>
              <span>Mathematics</span>
              <span style={{color:"red"}}>40%</span>
            </div>

            <div style={styles.topicRow}>
              <span>History</span>
              <span style={{color:"red"}}>35%</span>
            </div>

            <div style={styles.topicRow}>
              <span>Sports</span>
              <span style={{color:"orange"}}>50%</span>
            </div>

          </div>

        </div>


        {/* RIGHT */}
        <div style={styles.right}>

          <h3>Your Progress</h3>

          <div style={styles.progressCard}>
            <p>Total Quizzes</p>
            <h2>12</h2>
          </div>

          <div style={styles.progressCard}>
            <p>Best Score</p>
            <h2>9 / 10</h2>
          </div>

          <div style={styles.progressCard}>
            <p>Accuracy</p>
            <h2>82%</h2>
          </div>

        </div>

      </div>

    </div>
  );
}


/* CARD COMPONENT */

function ActionCard({ title, desc, color, onClick }) {
  return (
    <div
      style={{ ...styles.card, borderLeft: `6px solid ${color}` }}
      onClick={onClick}
    >
      <h3>{title}</h3>
      <p>{desc}</p>
    </div>
  );
}


/* STYLES */

const styles = {

  page: {
    minHeight: "100vh",
    background: "linear-gradient(135deg,#e0f2fe,#f8fafc)",
    fontFamily: "Arial"
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "20px 40px",
    background: "white",
    boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
  },

  logoArea: {
    display: "flex",
    alignItems: "center",
    gap: "10px"
  },

  logo: {
    width: "35px"
  },

  nav: {
    display: "flex",
    gap: "20px",
    alignItems: "center"
  },

  navBtn: {
    background: "none",
    border: "none",
    cursor: "pointer",
    fontSize: "16px",
    fontWeight: "500"
  },

  logoutBtn: {
    background: "#ef4444",
    border: "none",
    color: "white",
    padding: "10px 18px",
    borderRadius: "30px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  container: {
    display: "flex",
    gap: "40px",
    padding: "40px"
  },

  left: {
    flex: 3
  },

  right: {
    flex: 1,
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
    height: "fit-content"
  },

  title: {
    fontSize: "36px"
  },

  subtitle: {
    marginBottom: "30px"
  },

  actions: {
    display: "grid",
    gridTemplateColumns: "1fr",
    maxWidth: "400px",
    gap: "20px"
  },

  card: {
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    cursor: "pointer",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)"
  },

  progressCard: {
    background: "#f8fafc",
    padding: "15px",
    borderRadius: "8px",
    marginTop: "15px"
  },

  weakTopics: {
    marginTop: "30px",
    background: "white",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
    maxWidth: "400px"
  },

  topicRow: {
    display: "flex",
    justifyContent: "space-between",
    padding: "10px 0",
    borderBottom: "1px solid #eee"
  }

};

export default Dashboard;