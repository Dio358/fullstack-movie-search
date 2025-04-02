import Layout from "../components/Layout";
import {useEffect, useState} from "react";
import LoginBox from "../components/LoginBox";
import createChartUrl from "../utils/chart";
import {SideBar} from "../components/sideBar";
import {DiscoverTab} from "../components/DiscoverTab";
import {FavoritesTab} from "../components/FavoritesTab";
import { Movie } from "../interfaces";

const IndexPage = () => {
  const [message, setMessage] = useState("");
  const [loggedIn, setLoggedIn] = useState(false);
  const [state, setState] = useState(0);
  const [token, setToken] = useState("");

  const movies : Movie[]= [
    { id: 0, title: "Harry Potter", vote_average: "8.0", release_date: "2023" },
    { id: 1, title: "Harry Potter 2", vote_average: "7.0", release_date: "2024" }
  ];

  const [chart, setChart] = useState("");
  

  const logIn = async (userName: string, password: string) => {
    try {
      const res = await fetch("/api/backend-proxy/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userName, password: password }),
      });

      const data = await res.json();
      console.log("Data from backend:", data);
      
      if (res.ok){
        setState(1)
        setMessage("")
        setToken(data.token)
      } else {
        setMessage("Login failed")
        console.log("Response:", data, res.status);
      }
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      setMessage("Failed to connect to backend.");
    }
  };

  const createAccount = async (userName: string, password: string) => {
    try {
      const res = await fetch("/api/backend-proxy/createUser", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: userName, password: password }),
      }); 
      
      const data = await res.json();

      if (res.ok){
        setState(1);
        setMessage("")
      }
      else if (res.status == 409){
        setMessage("UserName exists already")
      }
      else{
        setMessage("An unexpected error occured")
        console.log("Response:", data, res.status);
      }
      
    } catch (err) {
      console.error("Failed to fetch from backend:", err);
      setMessage("Failed to connect to backend.");
    }
  };

  const logOff = () => {
    setLoggedIn(false);
  };

  useEffect(() => {
    setChart(createChartUrl(movies));
  }, []);

  return (
    <Layout title="Home | Next.js + TypeScript Example">
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        {state === 0 && <LoginBox logIn={logIn} createAccount={createAccount} message={message}/>}

        {state !== 0 && (
          <div style={{
            padding: "20px",
            width: "70vh",
            height: "65vh",
            background: "rgba(255, 255, 255, 0.26)",
            borderRadius: "15px",
            display: "flex",
            flexDirection: "row",
            alignItems: "center"
          }}>
            <SideBar onClick={() => state !== 1 ? setState(1) : undefined} state={state}
                     onClick1={() => state !== 2 ? setState(2) : undefined} onClick2={() => setState(0)}/>

            {state === 1 && (
                <DiscoverTab token={token}/>
            )}

            {state === 2 && (
                <FavoritesTab items={movies} src={chart}/>
            )}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default IndexPage;
