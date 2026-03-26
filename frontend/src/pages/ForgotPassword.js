import React,{useState} from "react";
import axios from "axios";

function ForgotPassword(){

const [email,setEmail] = useState("");

const submit = ()=>{

axios.post("http://127.0.0.1:5000/auth/forgot-password",{
email:email
})
.then(res=>{
alert("Reset token: "+res.data.token);
})
.catch(err=>alert("User not found"));

}

return(

<div style={{maxWidth:"400px",margin:"auto",marginTop:"100px"}}>

<h2>Forgot Password</h2>

<input
type="email"
placeholder="Enter Email"
value={email}
onChange={(e)=>setEmail(e.target.value)}
style={{width:"100%",padding:"10px",marginBottom:"10px"}}
/>

<button
onClick={submit}
style={{width:"100%",padding:"10px"}}
>
Send Reset Link
</button>

</div>

)

}

export default ForgotPassword;