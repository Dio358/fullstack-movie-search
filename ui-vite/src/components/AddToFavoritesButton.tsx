import { memo, useContext, useState } from "react";
import ControlPointIcon from "@mui/icons-material/ControlPoint";
import { addMovieToFavorites } from "../api/movieApi";
import { Token } from "./Token";

export const AddToFavoritesButton = memo(
  ({
    index,
    hoveredIndex,
    movie_id,
  }: {
    index: number;
    hoveredIndex: number | null;
    movie_id: number;
  }) => {
    const [isFocusedHover, setIsFocusedHover] = useState(false);
    const token = useContext(Token);

    const handleAddToFavorites = async (movie_id: number) => {
      await addMovieToFavorites(token, movie_id);
    };

    const getColor = (): string => {
      if (isFocusedHover) return "rgba(0, 0, 0, 1)";
      if (index === hoveredIndex) return "rgba(0, 0, 0, 0.68)";
      return "rgba(0, 0, 0, 0.34)";
    };

    return (
      <ControlPointIcon
        style={{
          color: getColor(),
          transition: "color 150ms ease",
          cursor: "pointer",
        }}
        onMouseEnter={() => setIsFocusedHover(true)}
        onMouseLeave={() => setIsFocusedHover(false)}
        onClick={() => handleAddToFavorites(movie_id)}
      />
    );
  },
  (prevProps, nextProps) =>
    prevProps.index === nextProps.index &&
    prevProps.hoveredIndex === nextProps.hoveredIndex
);
