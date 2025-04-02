import {useState} from "react";
import List from "./List";
import * as React from "react";
import { Movie } from "../interfaces";

export const DiscoverTab = ({
    token,
  }: {
    token: string;
  }) => {
    const [selectedLength, setSelectedLength] = useState(1);
    const [selectedMovie, setSelectedMovie] = useState(-1);
    const [hoveredIndex, setHoveredIndex] = React.useState<number | null>(null);
    const [movies, setMovies] = React.useState< Movie[] | null>(null);

    const getMovies = async () => {
        try {
          const res = await fetch("/api/backend-proxy/most_popular/20", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token,
            },
          });
    
          const data = await res.json();
          console.log("Data from backend:", data);
          
          if (res.ok){
            setMovies(data)
          } 
        } catch (err) {
          console.error("Failed to fetch from backend:", err);
        }
      };

      React.useEffect(() => {
        getMovies()
      }, [token])

    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "10%"
    }}>
        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Popular Movies</h1>
        <select value={selectedLength} onChange={(e) => setSelectedLength(Number(e.target.value))}>
            {Array.from({length: 20}, (_, i) => (
                <option key={i + 1} value={i + 1}>
                    {i + 1}
                </option>
            ))}
        </select>
        <List items={movies} length={selectedLength} action="add to"/>
    

        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies in the Same
            Genres</h1>
        {/* <List items={movies} action="remove from"/> */}

        <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies with Similar
            Runtimes</h1>
        {/* <List items={movies} action="remove from"/> */}
    </div>;
}