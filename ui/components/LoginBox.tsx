import { useState } from "react";

const LoginBox = ({logIn}) => {
    const [userName, setUsername] = useState("");
    const [password, setPassword] = useState("");

    return <div style={{ 
        padding: "20px", 
        width: "30vh", 
        height: "25vh",
        background: "rgba(255, 255, 255, 0.9)", 
        borderRadius: "15px", 
        display: "flex", 
        flexDirection: "column", 
        alignItems: "center" 
      }}>
        <h1 style={{ fontFamily: "Arial", textAlign: "center", marginBottom: "20px" }}>Log in</h1>
        <input 
          type="text" 
          value={userName}
          style={{ fontFamily: "Arial", borderRadius: "5px", padding: "10px", width: "70%", marginBottom: "10px", background: "transparent" }}
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Enter username"
        />
        <input 
          type="password" 
          value={password}
          style={{ fontFamily: "Arial", borderRadius: "5px", padding: "10px", width: "70%", background: "transparent" }}
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Enter password"
        />
        <button onClick={logIn(userName, password)}
            style={{
              marginTop: "15px",
              padding: "10px 20px",
              backgroundColor: "rgba(17, 124, 231, 0.9)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              fontFamily: "Arial",
              cursor: "pointer"
            }}
          >
            Log in
          </button>
          <button onClick={() => console.log("Button clicked")}
            style={{
              marginTop: "15px",
              padding: "10px 20px",
              backgroundColor: "rgba(17, 124, 231, 0.9)",
              color: "white",
              border: "none",
              borderRadius: "5px",
              fontFamily: "Arial",
              cursor: "pointer"
            }}
          >
            Create Account
          </button>
      </div>

}

export default LoginBox;