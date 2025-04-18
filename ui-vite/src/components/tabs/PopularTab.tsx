import { useState, useEffect, useContext } from "react";
import List from "../list/List";
import { Movie } from "../../interfaces";
import { Title } from "../elements/Title";
import { Token } from "../login/Token";
import { fetchMostPopularMovies } from "../../api/movieApi";

export const PopularTab = () => {
  const [selectedLength, setSelectedLength] = useState(1);
  const [movies, setMovies] = useState<Movie[] | null>(null);
  const token = useContext(Token);

  const getMovies = async () => {
    const data = await fetchMostPopularMovies(token, 20);
    if (data) {
      setMovies(data);
    }
  };

  console.log("token: ", token);
  useEffect(() => {
    console.log("token: ", token);

    if (token) getMovies();
  }, [token]);

  useEffect(() => {
    if (movies) console.log("movies: ", movies);
  }, [movies]);

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
      <List items={movies} length={selectedLength} action="add to" />
    </div>
  );
};
