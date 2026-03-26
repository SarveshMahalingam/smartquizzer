import React, { useEffect, useState } from "react";
import axios from "axios";

function Leaderboard() {

  const [leaders,setLeaders] = useState([]);

  useEffect(()=>{

    axios.get("http://127.0.0.1:5000/quiz/leaderboard")
    .then(res=>{
      setLeaders(res.data);
    })
    .catch(err=>console.log(err));

  },[]);

  return(

    <div style={{padding:"40px"}}>

      <h1>Leaderboard</h1>

      <table style={{width:"400px",marginTop:"20px"}}>

        <thead>
          <tr>
            <th>Rank</th>
            <th>User</th>
            <th>Score</th>
          </tr>
        </thead>

        <tbody>

          {leaders.map((player,index)=>(

            <tr key={index}>

              <td>{index+1}</td>
              <td>User {player.user_id}</td>
              <td>{player.score}</td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>

  );

}

export default Leaderboard;