import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Register() {

const [name,setName] = useState("");
const [email,setEmail] = useState("");
const [password,setPassword] = useState("");

const navigate = useNavigate();

/* PASSWORD VALIDATION */

const hasLength = password.length >= 8;
const hasUpper = /[A-Z]/.test(password);
const hasNumber = /[0-9]/.test(password);
const hasSpecial = /[!@#$%^&*]/.test(password);

const submit = () => {

axios.post("http://127.0.0.1:5000/register",{
name:name,
email:email,
password:password
})
.then(()=>{
alert("Account created successfully");
navigate("/login");
})
.catch(()=>alert("Registration failed"));

};

return(

<div style={styles.page}><div style={styles.card}><h2 style={styles.title}>Create Account ✨</h2><input
type="text"
placeholder="Full Name"
value={name}
onChange={(e)=>setName(e.target.value)}
style={styles.input}
/>

<input
type="email"
placeholder="Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
style={styles.input}
/>

<input
type="password"
placeholder="Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
style={styles.input}
/>

{/* PASSWORD RULES */}

<div style={styles.rules}><p style={{fontWeight:"bold"}}>Password requirements</p><p style={{color: hasLength ? "green" : "#888"}}>
{hasLength ? "✔" : "•"} Minimum 8 characters
</p><p style={{color: hasUpper ? "green" : "#888"}}>
{hasUpper ? "✔" : "•"} One uppercase letter
</p><p style={{color: hasNumber ? "green" : "#888"}}>
{hasNumber ? "✔" : "•"} One number
</p><p style={{color: hasSpecial ? "green" : "#888"}}>
{hasSpecial ? "✔" : "•"} One special character
</p></div><button style={styles.button} onClick={submit}>
🚀 Sign Up
</button><p style={styles.text}>
Already have an account?
<span style={styles.link} onClick={()=>navigate("/login")}>
 Sign In
</span>
</p></div></div>);

}

const styles={

page:{
height:"100vh",
display:"flex",
justifyContent:"center",
alignItems:"center",
background:"#f4f6fb",
fontFamily:"Arial"
},

card:{
width:"360px",
background:"white",
padding:"40px",
borderRadius:"12px",
boxShadow:"0 10px 25px rgba(0,0,0,0.1)",
display:"flex",
flexDirection:"column",
gap:"15px"
},

title:{
textAlign:"center"
},

input:{
padding:"12px",
border:"1px solid #ddd",
borderRadius:"8px",
fontSize:"14px"
},

rules:{
fontSize:"13px",
lineHeight:"1.6"
},

button:{
marginTop:"10px",
padding:"12px",
border:"none",
borderRadius:"8px",
background:"#06b6d4",
color:"white",
fontSize:"16px",
cursor:"pointer",
fontWeight:"bold"
},

text:{
textAlign:"center",
fontSize:"14px",
marginTop:"10px"
},

link:{
color:"#6366f1",
cursor:"pointer",
fontWeight:"bold"
}

};

export default Register;