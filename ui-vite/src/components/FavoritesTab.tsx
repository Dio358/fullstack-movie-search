import { useEffect, useState } from "react";
import List from "./List";
import { Title } from "./Title";
import createChartUrl from "../utils/chart";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

export const FavoritesTab = () => {
  const [chartUrl, setChartUrl] = useState("");
  const favorites = useSelector((state: RootState) => state.favorites.movies);

  useEffect(() => {
    setChartUrl(createChartUrl(favorites));
  }, [favorites]);

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
      <List items={favorites} action="remove from" />

      <Title>Average Score</Title>
      {chartUrl && <img src={chartUrl} alt="Chart of average scores" />}
    </div>
  );
};
