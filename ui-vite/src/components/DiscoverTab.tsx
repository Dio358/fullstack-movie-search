import { useState, useEffect, useContext } from "react";
import List from "./List";
import { Movie } from "../interfaces";
import { Title } from "./Title";
import { Token } from "./Token";

export const DiscoverTab = () => {
    const [selectedLength, setSelectedLength] = useState(1);
    const [movies, setMovies] = useState< Movie[] | null>(null);
    const token = useContext(Token)
    
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

      useEffect(() => {
        getMovies()
      }, [token])

      const addTofavorites = async ({movie_id} : {movie_id : number}) => {
        console.log("adding movie with id:", movie_id)
        try {
          await fetch( import.meta.env.BASE_URL + "/movies/favorite/" + encodeURIComponent(movie_id), {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "Authorization": "Bearer " + token,
            },
          });
    
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
        <select style={{marginBottom: "15px"}} value={selectedLength} onChange={(e) => setSelectedLength(Number(e.target.value))}>
            {Array.from({length: 20}, (_, i) => (
                <option key={i + 1} value={i + 1}>
                    {i + 1}
                </option>
            ))}
        </select>
        <List items={movies} onClick={(movie: Movie) => addTofavorites({ movie_id: movie.id })} action="add to"/>
    </div>;
}