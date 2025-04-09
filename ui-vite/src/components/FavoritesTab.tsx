import { JSX, useEffect, useState } from "react";
import List from "./List";
import { Title } from "./Title";
import { createBarChart } from "../utils/chart";
import { useSelector } from "react-redux";
import { RootState } from "../redux/store";

export const FavoritesTab = () => {
  const favorites = useSelector((state: RootState) => state.favorites.movies);
  const [BarChart, setBarChart] = useState<JSX.Element | null>(null);

  useEffect(() => {
    setBarChart(createBarChart(favorites));
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
      {BarChart}
    </div>
  );
};
