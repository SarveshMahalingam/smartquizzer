import React from "react";
import he from "he";
import { useLocation, useNavigate } from "react-router-dom";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend
} from "recharts";

function Result() {

  const location = useLocation();
  const navigate = useNavigate();

  const score = location.state?.score || 0;
  const total = location.state?.total || 0;
  const questions = location.state?.questions || [];
  const answers = location.state?.answers || {};

  const wrong = total - score;
  const accuracy = total === 0 ? 0 : Math.round((score / total) * 100);

  const data = [
    { name: "Correct", value: score },
    { name: "Wrong", value: wrong }
  ];

  const COLORS = ["#4caf50", "#f44336"];


  return (

    <div style={{ padding: "40px", background: "#f5f6fa", minHeight: "100vh" }}>

      <h1 style={{ textAlign: "center" }}>Quiz Result</h1>


      {/* TOP CARD */}

      <div style={{
        background: "white",
        padding: "30px",
        borderRadius: "12px",
        maxWidth: "700px",
        margin: "30px auto",
        textAlign: "center",
        boxShadow: "0 0 10px rgba(0,0,0,0.1)"
      }}>

        <h2>Score: {score} / {total}</h2>
        <p>Accuracy: {accuracy}%</p>


        {/* PIE CHART */}

        <div style={{ display: "flex", justifyContent: "center" }}>

          <PieChart width={300} height={300}>
            <Pie
              data={data}
              cx="50%"
              cy="50%"
              outerRadius={100}
              dataKey="value"
              label
            >
              {data.map((entry, index) => (
                <Cell key={index} fill={COLORS[index]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>

        </div>


        <button
          onClick={() => navigate("/dashboard")}
          style={{
            marginTop: "20px",
            padding: "12px 25px",
            background: "#1f3c88",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer"
          }}
        >
          Back to Dashboard
        </button>

      </div>


      {/* ANSWER REVIEW */}

      <div style={{ maxWidth: "800px", margin: "auto" }}>

        <h2>Review Answers</h2>

        {questions.map((q, index) => (

          <div
            key={index}
            style={{
              background: "white",
              padding: "20px",
              borderRadius: "10px",
              marginTop: "15px",
              boxShadow: "0 0 8px rgba(0,0,0,0.1)"
            }}
          >

            <h4 dangerouslySetInnerHTML={{ __html: q.question }} />

            <p>
              Your Answer:{" "}
              <span
  style={{
    color: answers[index] === q.answer ? "green" : "red"
  }}
  dangerouslySetInnerHTML={{
    __html: answers[index] || "Not Answered"
  }}
/>
            </p>

           <p>
  Correct Answer:{" "}
  <span
    style={{ color: "green" }}
    dangerouslySetInnerHTML={{ __html: q.answer }}
  />
</p>
          </div>

        ))}

      </div>

    </div>

  );

}

export default Result;