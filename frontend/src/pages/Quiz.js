import React, { useState, useEffect } from "react";
import axios from "axios";
import { useNavigate, useLocation } from "react-router-dom";
import he from "he";

function Quiz() {

  const navigate = useNavigate();
  const location = useLocation();

  const category = location.state?.category || "9";
  const amount = location.state?.amount || 5;

  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [marked, setMarked] = useState({});
  const [timeLeft, setTimeLeft] = useState(30);

  const token = localStorage.getItem("token");


  /* -------------------------
     FETCH QUESTIONS
  ------------------------- */

  useEffect(() => {

    axios.post(
      "http://127.0.0.1:5000/quiz/generate",
      {
        category,
        amount
      },
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    .then(res => {
      setQuestions(res.data.questions);
    })
    .catch(err => console.log(err));

  }, [category, amount, token]);


  /* -------------------------
     TIMER
  ------------------------- */

  useEffect(() => {

    if (questions.length === 0) return;

    const timer = setInterval(() => {

      setTimeLeft(prev => {

        if (prev === 1) {
          nextQuestion();
          return 30;
        }

        return prev - 1;

      });

    }, 1000);

    return () => clearInterval(timer);

  }, [currentQuestion, questions]);


  /* -------------------------
     SELECT ANSWER
  ------------------------- */

  const selectAnswer = (option) => {

    setAnswers(prev => ({
      ...prev,
      [currentQuestion]: option
    }));

  };


  /* -------------------------
     MARK FOR REVIEW
  ------------------------- */

  const markForReview = () => {

    setMarked(prev => ({
      ...prev,
      [currentQuestion]: true
    }));

  };


  /* -------------------------
     NAVIGATION
  ------------------------- */

  const nextQuestion = () => {

    if (currentQuestion < questions.length - 1) {

      setCurrentQuestion(currentQuestion + 1);
      setTimeLeft(30);

    } else {

      submitQuiz();

    }

  };

  const prevQuestion = () => {

    if (currentQuestion > 0) {

      setCurrentQuestion(currentQuestion - 1);
      setTimeLeft(30);

    }

  };


  /* -------------------------
     SUBMIT QUIZ (FIXED)
  ------------------------- */

  const submitQuiz = () => {

    let correct = 0;

    questions.forEach((q, index) => {

      if (
        he.decode(answers[index] || "") ===
        he.decode(q.answer)
      ) {
        correct++;
      }

    });

    navigate("/result", {
      state: {
        score: correct,
        total: questions.length,
        questions: questions,
        answers: answers
      }
    });

  };


  /* -------------------------
     LOADING
  ------------------------- */

  if (questions.length === 0) {

    return (
      <h2 style={{ textAlign: "center", marginTop: "100px" }}>
        Loading Questions...
      </h2>
    );

  }


  const q = questions[currentQuestion];

  const answered = Object.keys(answers).length;
  const remaining = questions.length - answered;


  /* -------------------------
     UI
  ------------------------- */

  return (

    <div style={{ display: "flex", height: "100vh", background: "#f5f6fa" }}>

      {/* LEFT SIDE */}

      <div style={{ flex: 3, padding: "30px" }}>

        {/* HEADER */}

        <div style={{
          display: "flex",
          justifyContent: "space-between",
          marginBottom: "20px"
        }}>

          <div>
            <h3>NeroQuiz Assessment</h3>
            <p>AI Generated Quiz</p>
          </div>

          <div style={{
            background: "#eee",
            padding: "10px 20px",
            borderRadius: "10px",
            fontSize: "18px"
          }}>
            ⏱ {timeLeft}s
          </div>

        </div>


        {/* QUESTION NAVIGATOR */}

        <div style={{
          display: "flex",
          gap: "10px",
          marginBottom: "20px",
          flexWrap: "wrap"
        }}>

          {questions.map((_, index) => (

            <button
              key={index}
              onClick={() => setCurrentQuestion(index)}
              style={{
                padding: "10px",
                borderRadius: "6px",
                border: "none",
                background: index === currentQuestion ? "#5c6bc0" : "#ddd",
                color: index === currentQuestion ? "white" : "black"
              }}
            >
              Q{index + 1}
            </button>

          ))}

        </div>


        {/* QUESTION CARD */}

        <div style={{
          background: "white",
          padding: "30px",
          borderRadius: "12px"
        }}>

          <h3 dangerouslySetInnerHTML={{ __html: q.question }} />

          <div style={{ marginTop: "20px" }}>

            {q.options.map((opt, index) => (

              <button
                key={index}
                onClick={() => selectAnswer(opt)}
                style={{
                  width: "100%",
                  padding: "12px",
                  marginBottom: "10px",
                  textAlign: "left",
                  background:
                    answers[currentQuestion] === opt
                      ? "#90ee90"
                      : "white",
                  border: "1px solid #ccc",
                  borderRadius: "6px"
                }}
              >

                {String.fromCharCode(65 + index)}.{" "}
                <span dangerouslySetInnerHTML={{ __html: opt }} />

              </button>

            ))}

          </div>

        </div>


        {/* NAVIGATION */}

        <div style={{
          display: "flex",
          justifyContent: "space-between",
          marginTop: "20px"
        }}>

          <button onClick={prevQuestion}>Previous</button>

          <button onClick={markForReview}>
            Mark For Review
          </button>

          <button onClick={nextQuestion}>
            {currentQuestion === questions.length - 1 ? "Submit" : "Next"}
          </button>

        </div>

      </div>


      {/* RIGHT PANEL */}

      <div style={{
        flex: 1,
        background: "white",
        padding: "20px"
      }}>

        <h3>Progress</h3>

        <p>Answered: {answered}</p>
        <p>Remaining: {remaining}</p>

        <button
          onClick={submitQuiz}
          style={{
            marginTop: "20px",
            width: "100%",
            padding: "12px",
            background: "#5c6bc0",
            color: "white",
            border: "none"
          }}
        >
          Submit Quiz
        </button>

      </div>

    </div>

  );

}

export default Quiz;