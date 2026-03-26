import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Login({ setToken }) {

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const submit = async () => {

    try {

      const res = await axios.post(
        "http://127.0.0.1:5000/auth/login",
        {
          email: email,
          password: password
        }
      );

      console.log("Login response:", res.data);

      const token = res.data.access_token || res.data.token;

      if (!token) {
        alert("Login failed: token not received");
        return;
      }

      localStorage.setItem("token", token);

      if (setToken) {
        setToken(token);
      }

      navigate("/dashboard");

    } catch (err) {

      console.log("Login error:", err);

      if (err.response) {
        alert(err.response.data.error || "Login failed");
      } else if (err.request) {
        alert("Backend server not reachable");
      } else {
        alert("Unexpected error occurred");
      }

    }

  };

  return (

    <div style={styles.page}>
      <div style={styles.card}>

        <h2 style={styles.title}>Welcome Back 👋</h2>

        <p style={styles.subtitle}>
          Sign in to continue learning
        </p>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />

        <button style={styles.button} onClick={submit}>
          🚀 Sign In
        </button>

        <p style={styles.text}>
          Don't have an account?
          <span style={styles.link} onClick={() => navigate("/register")}>
            {" "}Sign Up
          </span>
        </p>

      </div>
    </div>

  );

}

const styles = {

  page: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#f4f6fb",
    fontFamily: "Arial"
  },

  card: {
    width: "360px",
    background: "white",
    padding: "40px",
    borderRadius: "12px",
    boxShadow: "0 10px 25px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column",
    gap: "15px"
  },

  title: {
    textAlign: "center",
    marginBottom: "5px"
  },

  subtitle: {
    textAlign: "center",
    color: "#666",
    marginBottom: "10px"
  },

  input: {
    padding: "12px",
    border: "1px solid #ddd",
    borderRadius: "8px",
    fontSize: "14px"
  },

  button: {
    marginTop: "10px",
    padding: "12px",
    border: "none",
    borderRadius: "8px",
    background: "#06b6d4",
    color: "white",
    fontSize: "16px",
    cursor: "pointer",
    fontWeight: "bold"
  },

  text: {
    textAlign: "center",
    fontSize: "14px",
    marginTop: "10px"
  },

  link: {
    color: "#6366f1",
    cursor: "pointer",
    fontWeight: "bold"
  }

};

export default Login;