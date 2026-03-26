import React, { useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Profile() {

const [profile,setProfile] = useState({});
const [achievements,setAchievements] = useState([]);
const [stats,setStats] = useState({});
const [loading,setLoading] = useState(true);

const navigate = useNavigate();
const token = localStorage.getItem("token");

useEffect(()=>{

if(!token){
navigate("/login");
return;
}

const headers = {
Authorization: "Bearer ${token}"
};

Promise.all([
axios.get("http://127.0.0.1:5000/quiz/profile",{headers}),
axios.get("http://127.0.0.1:5000/quiz/achievements",{headers}),
axios.get("http://127.0.0.1:5000/quiz/stats",{headers})
])
.then(([profileRes,achievementsRes,statsRes])=>{

setProfile(profileRes.data);
setAchievements(achievementsRes.data);
setStats(statsRes.data);
setLoading(false);

})
.catch(err=>{

console.error("Profile error:",err);

if(err.response && err.response.status === 401){
localStorage.removeItem("token");
navigate("/login");
}

setLoading(false);

});

},[token,navigate]);

if(loading){
return <h2 style={{textAlign:"center",marginTop:"100px"}}>Loading Profile...</h2>
}

return(

<div style={{
maxWidth:"900px",
margin:"auto",
padding:"40px",
fontFamily:"Arial"
}}><h1 style={{textAlign:"center"}}>User Profile</h1>{/* PROFILE CARD */}

<div style={{
background:"#ffffff",
padding:"30px",
borderRadius:"10px",
boxShadow:"0 5px 15px rgba(0,0,0,0.1)",
marginTop:"30px"
}}><h2>Level: {profile.level || 0}</h2><p>XP: {profile.xp || 0}</p>{/* XP BAR */}

<div style={{
height:"10px",
background:"#ddd",
borderRadius:"10px"
}}><div style={{
width:`${profile.xp ? profile.xp % 100 : 0}%`,
height:"10px",
background:"#4CAF50",
borderRadius:"10px"
}}></div></div></div>{/* STATISTICS */}

<div style={{
marginTop:"40px",
background:"#fff",
padding:"30px",
borderRadius:"10px",
boxShadow:"0 5px 15px rgba(0,0,0,0.1)"
}}><h2>Statistics</h2><p>Total Quizzes: {stats.total_quizzes || 0}</p>
<p>Best Score: {stats.best_score || 0}</p>
<p>Average Score: {stats.average_score || 0}</p>
<p>Accuracy: {stats.accuracy || 0}%</p></div>{/* ACHIEVEMENTS */}

<div style={{
marginTop:"40px",
background:"#fff",
padding:"30px",
borderRadius:"10px",
boxShadow:"0 5px 15px rgba(0,0,0,0.1)"
}}><h2>Achievements</h2>{achievements.length === 0 && <p>No achievements yet</p>}

{achievements.map((a,index)=>(

<div
key={index}
style={{
padding:"10px",
borderBottom:"1px solid #eee"
}}
><h4>{a.title}</h4>
<p>{a.description}</p></div>))}

</div></div>);

}

export default Profile;