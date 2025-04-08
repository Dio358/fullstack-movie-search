import { useEffect, useContext, useState } from "react";
import List from "./List";
import { Title } from "./Title";
import createChartUrl from "../utils/chart";
import { Token } from "./Token";
import { fetchFavoriteMovies } from "../api/movieApi";

export const FavoritesTab = () => {
  const [movies, setMovies] = useState([]);
  const [chartUrl, setChartUrl] = useState("");
  const token = useContext(Token);

  useEffect(() => {
    setChartUrl(createChartUrl(movies));
  }, [movies]);

  useEffect(() => {
    const getFavorites = async () => {
      if (!token) return;
      const favorites = await fetchFavoriteMovies(token);
      if (favorites) {
        setMovies(favorites);
      }
    };

    getFavorites();
  }, [token]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        marginLeft: "20px",
        paddingLeft: "13%",
      }}
    >
      <Title>Favorites</Title>
      <List items={movies} action="remove from" />

      <Title>Average Score</Title>
      {chartUrl && <img src={chartUrl} alt="Chart of average scores" />}
    </div>
  );
};
