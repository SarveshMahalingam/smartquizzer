import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";

function QuizSetup() {

const navigate = useNavigate();
const location = useLocation();

/* MODE FROM DASHBOARD */
const mode = location.state?.mode || "practice";

/* DEFAULT VALUES */
const [category,setCategory] = useState(
  mode === "daily" ? "9" : "9"
);

const [amount,setAmount] = useState(
  mode === "daily" ? "10" : "5"
);

/* START QUIZ */
const startQuiz = () => {

navigate("/quiz",{
state:{
category:category,
amount:amount,
mode:mode
}
});

};

return(

<div style={styles.page}>

<div style={styles.card}>

<h2>
{mode === "adaptive" && "Adaptive Quiz"}
{mode === "daily" && "Daily Challenge"}
{mode === "practice" && "Select Quiz Settings"}
</h2>

{/* TOPIC SELECTION (HIDDEN FOR ADAPTIVE) */}

{mode !== "adaptive" && (

<>
<label>Topic</label>

<select
value={category}
onChange={(e)=>setCategory(e.target.value)}
style={styles.select}
disabled={mode === "daily"}
>

<option value="9">General Knowledge</option>
<option value="18">Computer Science</option>
<option value="19">Mathematics</option>
<option value="21">Sports</option>
<option value="23">History</option>

</select>
</>

)}

{/* QUESTION AMOUNT */}

<label>Number of Questions</label>

<select
value={amount}
onChange={(e)=>setAmount(e.target.value)}
style={styles.select}
disabled={mode === "daily"}
>

<option value="5">5 Questions</option>
<option value="10">10 Questions</option>
<option value="15">15 Questions</option>

</select>

<button style={styles.button} onClick={startQuiz}>
Start Quiz
</button>

</div>

</div>

);

}

const styles={

page:{
height:"100vh",
display:"flex",
justifyContent:"center",
alignItems:"center",
background:"#f1f5f9",
fontFamily:"Arial"
},

card:{
background:"white",
padding:"40px",
borderRadius:"10px",
boxShadow:"0 5px 20px rgba(0,0,0,0.1)",
display:"flex",
flexDirection:"column",
gap:"15px",
width:"350px"
},

select:{
padding:"10px",
borderRadius:"6px",
border:"1px solid #ccc"
},

button:{
marginTop:"10px",
padding:"10px",
background:"#22c55e",
color:"white",
border:"none",
borderRadius:"6px",
cursor:"pointer",
fontWeight:"bold"
}

};

export default QuizSetup;
