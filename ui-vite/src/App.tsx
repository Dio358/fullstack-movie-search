import { useState } from "react";
import LoginBox from "./components/LoginBox";
import { SideBar } from "./components/sideBar";
import { DiscoverTab } from "./components/DiscoverTab";
import { FavoritesTab } from "./components/FavoritesTab";
import { SearchTab } from "./components/SearchTab";
import { Token } from "./components/Token";
import { Provider } from "react-redux";
import { store } from "./redux/store";

function App() {
  const [message, setMessage] = useState("");
  const [state, setState] = useState(0);
  const [token, setToken] = useState("");
  const BASE_URL = import.meta.env.VITE_BASE_URL;

  const logIn = async (userName: string, password: string) => {
    try {
      const res = await fetch(`${BASE_URL}/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userName, password: password }),
      });

      const data = await res.json();

      if (res.ok) {
        setState(1);
        setMessage("");
        setToken(data.token);
      } else {
        setMessage("Login failed");
        console.log("Response:", data, res.status);
      }
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      setMessage("Failed to connect to backend.");
    }
  };

  const createAccount = async (userName: string, password: string) => {
    try {
      const res = await fetch(`${BASE_URL}/createUser`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userName, password: password }),
      });

      const data = await res.json();

      if (res.ok) {
        setState(1);
        setMessage("");
      } else if (res.status == 409) {
        setMessage("UserName exists already");
      } else {
        setMessage("An unexpected error occured");
        console.log("Response:", data, res.status);
      }
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      setMessage("Failed to connect to backend.");
    }
  };

  return (
    <Provider store={store}>
      <div
        style={{
          minHeight: "100vh",
          minWidth: "100vw",
          background: "linear-gradient(135deg,rgb(10, 10, 10),rgb(42,42,42))",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          height: "100vh",
        }}
      >
        {state === 0 && (
          <LoginBox
            logIn={logIn}
            createAccount={createAccount}
            message={message}
          />
        )}

        {state !== 0 && (
          <div
            style={{
              padding: "50px",
              width: "100vh",
              height: "80vh",
              background: "rgb(18,18,18)",
              borderRadius: "5px",
              display: "flex",
              flexDirection: "row",
              alignItems: "center",
            }}
          >
            <SideBar
              onClick={() => (state !== 1 ? setState(1) : undefined)}
              onClick1={() => (state !== 2 ? setState(2) : undefined)}
              onClick2={() => (state !== 3 ? setState(3) : undefined)}
              onClick3={() => setState(0)}
              state={state}
            />

            <Token.Provider value={token}>
              {state === 1 && <DiscoverTab />}

              {state === 2 && <FavoritesTab />}

              {state === 3 && <SearchTab />}
            </Token.Provider>
          </div>
        )}
      </div>
    </Provider>
  );
}

export default App;
