import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Statistics() {

const navigate = useNavigate();

const [stats,setStats] = useState(null);
const [loading,setLoading] = useState(true);
const [error,setError] = useState(null);

const token = localStorage.getItem("token");

useEffect(()=>{

if(!token){
navigate("/login");
return;
}

axios.get("http://127.0.0.1:5000/quiz/stats",{
headers:{
Authorization: `Bearer ${token}`
}
})
.then(res=>{
setStats(res.data);
setLoading(false);
})
.catch(err=>{

console.error("Statistics error:",err);

if(err.response && err.response.status === 401){
setError("Session expired. Please login again.");
localStorage.removeItem("token");
navigate("/login");
}
else{
setError("Failed to load statistics.");
}

setLoading(false);

});

},[token,navigate]);

if(loading){
return(

<h2 style={{textAlign:"center",marginTop:"120px"}}>
Loading Statistics...
</h2>
);
}if(error){
return(

<h2 style={{textAlign:"center",marginTop:"120px",color:"red"}}>
{error}
</h2>
);
}return(

<div style={{
maxWidth:"900px",
margin:"auto",
padding:"40px"
}}><h1 style={{textAlign:"center"}}>
📊 Your Quiz Statistics
</h1><div style={{
display:"grid",
gridTemplateColumns:"1fr 1fr",
gap:"25px",
marginTop:"50px"
}}><StatCard
title="Total Quizzes"
value={stats.total_quizzes}
color="#3498db"
/>

<StatCard
title="Best Score"
value={stats.best_score}
color="#27ae60"
/>

<StatCard
title="Average Score"
value={stats.average_score}
color="#e67e22"
/>

<StatCard
title="Accuracy %"
value={`${stats.accuracy}%`}
color="#9b59b6"
/>

</div></div>);

}

function StatCard({title,value,color}){

return(

<div style={{
background:color,
color:"white",
padding:"35px",
borderRadius:"12px",
textAlign:"center",
boxShadow:"0 8px 20px rgba(0,0,0,0.15)"
}}><h3 style={{marginBottom:"15px"}}>
{title}
</h3><h1 style={{fontSize:"40px"}}>
{value}
</h1></div>);

}

export default Statistics;