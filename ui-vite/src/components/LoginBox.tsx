import React from "react";

const LoginBox = ({
  logIn,
  createAccount,
  message,
}: {
  logIn: (email: string, password: string) => void;
  createAccount: (email: string, password: string) => void;
  message: string;
}) => {
    const [userName, setUsername] = React.useState<string>("")
    const [password, setPassword] = React.useState<string>("")

    return <div style={{ 
        padding: "20px", 
        width: "30vh", 
        height: "30vh",
        background: "rgb(18,18,18)", 
        borderRadius: "5px", 
        display: "flex", 
        flexDirection: "column", 
        alignItems: "center" 
      }}>
        <h1 style={{ fontFamily: "Arial", textAlign: "center", paddingBottom: "5px", color: "white" }}>Log in</h1>
        <input 
          type="text" 
          value={userName}
          style={{ fontFamily: "Arial", borderRadius: "5px", padding: "10px", width: "70%", marginBottom: "10px", background: "transparent", color: "whitesmoke" }}
          onChange={(e) => setUsername(e.target.value)} 
          placeholder="Enter username"
        />
        <input 
          type="password" 
          value={password}
          style={{ fontFamily: "Arial", borderRadius: "5px", padding: "10px", width: "70%", background: "transparent", color: "whitesmoke"}}
          onChange={(e) => setPassword(e.target.value)} 
          placeholder="Enter password"
        />
        {message != "" && <span>{message}</span>}
        <button onClick={() => logIn(userName, password)}
            style={{
              marginTop: "20px",
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
          <button onClick={() => createAccount(userName, password)}
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