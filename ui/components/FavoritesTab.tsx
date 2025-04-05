import { useEffect, useContext, useState } from "react"
import List from "./List";
import { Movie } from "../interfaces";
import { Title } from "./Title";
import createChartUrl from "../utils/chart";
import { Token } from "./Token";



export const FavoritesTab = () => {
    const [movies, setMovies] = useState([])
    const [chartUrl, setChartUrl] = useState("")
    const token = useContext(Token)
  

    useEffect(() => {
        setChartUrl(createChartUrl(movies));
      }, [movies]);

    useEffect(() => {

        const getFavorites = async () => {
            try {
              const res = await fetch("/api/backend-proxy/movies/favorite/", {
                method: "GET",
                headers: {
                  "Content-Type": "application/json",
                  "Authorization": "Bearer " + token,
                },
              });
        
              const data = await res.json();
    
              if (res.ok) setMovies(data.results)
    
            } catch (err) {
              console.error("Failed to fetch from backend:", err);
            }
          };
        
        getFavorites()

    }, []);    

    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "13%"
    }}>
        <Title>Favorites</Title>
        <List items={movies} action="remove from"/>

        <Title>Average Score</Title>
        {chartUrl && <img src={chartUrl} alt="Chart of average scores"/>}
    </div>;
}