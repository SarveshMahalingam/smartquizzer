import React from "react";

function WeakTopics() {

  return (

    <div style={{
      padding:"40px",
      textAlign:"center",
      fontFamily:"Arial"
    }}>

      <h1>⚠ Weak Topics</h1>

      <p>
        This section will show topics where your quiz performance is low.
      </p>

      <div style={{
        marginTop:"40px",
        display:"grid",
        gridTemplateColumns:"repeat(3,1fr)",
        gap:"20px"
      }}>

        <div style={card}>Mathematics</div>
        <div style={card}>Computer Science</div>
        <div style={card}>History</div>

      </div>

    </div>

  );

}

const card = {
  background:"white",
  padding:"30px",
  borderRadius:"10px",
  boxShadow:"0 5px 15px rgba(0,0,0,0.1)"
};

export default WeakTopics;