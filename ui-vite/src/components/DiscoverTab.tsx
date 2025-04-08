import { useState, useEffect, useContext } from "react";
import List from "./List";
import { Movie } from "../interfaces";
import { Title } from "./Title";
import { Token } from "./Token";
import { fetchMostPopularMovies } from "../api/movieApi";

export const DiscoverTab = () => {
  const [selectedLength, setSelectedLength] = useState(1);
  const [movies, setMovies] = useState<Movie[] | null>(null);
  const token = useContext(Token);

  const getMovies = async () => {
    const data = await fetchMostPopularMovies(token, 20);
    if (data) {
      setMovies(data);
    }
  };

  useEffect(() => {
    if (token) getMovies();
  }, [token]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "10%",
      }}
    >
      <Title>Popular Movies</Title>
      <select
        style={{ marginBottom: "15px" }}
        value={selectedLength}
        onChange={(e) => setSelectedLength(Number(e.target.value))}
      >
        {Array.from({ length: 20 }, (_, i) => (
          <option key={i + 1} value={i + 1}>
            {i + 1}
          </option>
        ))}
      </select>
      <List items={movies} action="add to" />
    </div>
  );
};
