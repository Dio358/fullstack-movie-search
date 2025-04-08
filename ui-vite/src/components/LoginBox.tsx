import React from "react";
import { createAccount, logIn } from "../api/authApi";
import { useAppDispatch } from "../redux/hooks";
import {} from "../redux/favorites-slice";
import { AppDispatch } from "../redux/store";
import { fetchFavorites } from "../redux/favorites-thunks";

const LoginBox = ({
  setToken,
  setState,
}: {
  setToken: (token: string) => void;
  setState: (state: number) => void;
}) => {
  const [userName, setUsername] = React.useState<string>("");
  const [password, setPassword] = React.useState<string>("");
  const [message, setMessage] = React.useState<string>("");
  const dispatch: AppDispatch = useAppDispatch();

  const loadFavorites = (token: string) => async () => {
    dispatch(fetchFavorites(token));
  };

  const handleLogIn = async (userName: string, password: string) => {
    try {
      const result = await logIn(userName, password);
      if (result) {
        await loadFavorites(result.token)();
        setToken(result.token);
        setState(1);
        setMessage("");
      } else {
        setMessage("Login failed");
      }
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      setMessage("Failed to connect to backend.");
    }
  };

  const handleCreateAccount = async (userName: string, password: string) => {
    const result = await createAccount(userName, password);
    if (result.success) {
      setState(1);
      setMessage("");
    } else {
      setMessage(result.message || "Account creation failed");
    }
  };

  return (
    <div
      style={{
        padding: "20px",
        paddingBottom: "60px",
        width: "30vh",
        height: "30vh",
        background: "rgb(18,18,18)",
        borderRadius: "5px",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
      }}
    >
      <h1
        style={{
          fontFamily: "Arial",
          textAlign: "center",
          paddingBottom: "5px",
          color: "white",
        }}
      >
        Log in
      </h1>
      <input
        type="text"
        value={userName}
        style={{
          fontFamily: "Arial",
          borderRadius: "5px",
          padding: "10px",
          width: "70%",
          marginBottom: "10px",
          background: "transparent",
          color: "whitesmoke",
        }}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Enter username"
      />
      <input
        type="password"
        value={password}
        style={{
          fontFamily: "Arial",
          borderRadius: "5px",
          padding: "10px",
          width: "70%",
          background: "transparent",
          color: "whitesmoke",
        }}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Enter password"
      />
      {message != "" && <span>{message}</span>}
      <button
        onClick={() => handleLogIn(userName, password)}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          backgroundColor: "rgba(17, 124, 231, 0.9)",
          color: "white",
          border: "none",
          borderRadius: "5px",
          fontFamily: "Arial",
          cursor: "pointer",
        }}
      >
        Log in
      </button>
      <button
        onClick={() => handleCreateAccount(userName, password)}
        style={{
          marginTop: "15px",
          padding: "10px 20px",
          backgroundColor: "rgba(17, 124, 231, 0.9)",
          color: "white",
          border: "none",
          borderRadius: "5px",
          fontFamily: "Arial",
          cursor: "pointer",
        }}
      >
        Create Account
      </button>
    </div>
  );
};

export default LoginBox;
