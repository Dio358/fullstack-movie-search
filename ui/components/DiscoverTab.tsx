import {useState} from "react";
import List from "./List";
import * as React from "react";
import { Movie } from "../interfaces";
import { Title } from "./Title";

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
          const res = await fetch("/api/backend-proxy/movies/most_popular/20", {
            method: "GET",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token,
            },
          });
    
          const data = await res.json();
          
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

      const addTofavorites = async ({movie_id} : {movie_id : number}) => {
        console.log("adding movie with id:", movie_id)
        try {
          const res = await fetch("/api/backend-proxy/movies/favorite/" + encodeURIComponent(movie_id), {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token,
            },
          });
    
          const data = await res.json();
          console.log("response: ",res)
        } catch (err) {
          console.error("Failed to fetch from backend:", err);
        }
      };

    return <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "10%"
    }}>
        <Title>Popular Movies</Title>
        <select value={selectedLength} onChange={(e) => setSelectedLength(Number(e.target.value))}>
            {Array.from({length: 20}, (_, i) => (
                <option key={i + 1} value={i + 1}>
                    {i + 1}
                </option>
            ))}
        </select>
        <List items={movies} length={selectedLength} onClick={(movie: Movie) => addTofavorites({ movie_id: movie.id })} action="add to"/>
    </div>;
}