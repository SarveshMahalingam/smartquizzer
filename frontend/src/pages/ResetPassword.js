import React,{useState} from "react";
import axios from "axios";

function ResetPassword(){

const [token,setToken] = useState("");
const [password,setPassword] = useState("");

const reset = ()=>{

axios.post("http://127.0.0.1:5000/auth/reset-password",{
token:token,
password:password
})
.then(res=>alert("Password updated"))
.catch(err=>alert("Error"));

}

return(

<div style={{maxWidth:"400px",margin:"auto",marginTop:"100px"}}>

<h2>Reset Password</h2>

<input
placeholder="Token"
value={token}
onChange={(e)=>setToken(e.target.value)}
style={{width:"100%",padding:"10px",marginBottom:"10px"}}
/>

<input
type="password"
placeholder="New Password"
value={password}
onChange={(e)=>setPassword(e.target.value)}
style={{width:"100%",padding:"10px",marginBottom:"10px"}}
/>

<button
onClick={reset}
style={{width:"100%",padding:"10px"}}
>
Reset Password
</button>

</div>

)

}

export default ResetPassword;