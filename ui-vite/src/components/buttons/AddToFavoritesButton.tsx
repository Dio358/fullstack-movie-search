import { memo, useContext, useEffect, useState } from "react";
import ControlPointIcon from "@mui/icons-material/ControlPoint";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import {
  addMovieToFavorites,
  deleteMovieFromFavorites,
} from "../../api/movieApi";
import { Token } from "../login/Token";
import { AppDispatch, RootState } from "../../redux/store";
import { useAppDispatch } from "../../redux/hooks";
import { addMovie, deleteMovie } from "../../redux/favorites-slice";
import { useSelector } from "react-redux";
import { Movie } from "../../interfaces";
import { Tooltip } from "@mui/material";

export const AddToFavoritesButton = memo(
  ({
    index,
    hoveredIndex,
    movie,
  }: {
    index: number;
    hoveredIndex: number | null;
    movie: Movie;
  }) => {
    const [isFocusedHover, setIsFocusedHover] = useState(false);
    const token = useContext(Token);
    const favorites = useSelector((state: RootState) => state.favorites.movies);
    const dispatch: AppDispatch = useAppDispatch();
    const [inFavorites, setInFavorites] = useState(false);

    useEffect(() => {
      setInFavorites(favorites.some((m: Movie) => m.id === movie.id));
    }, [favorites, dispatch]);

    const handleAddToFavorites = async (movie: Movie) => {
      await addMovieToFavorites(token, movie.id);
      dispatch(addMovie(movie));
    };

    const handleRemoveFromFavorites = async (movie_id: number) => {
      await deleteMovieFromFavorites(token, movie_id);
      dispatch(deleteMovie(movie_id));
    };

    const getPlusColor = (): string => {
      if (isFocusedHover) return "rgba(0, 0, 0, 1)";
      if (index === hoveredIndex) return "rgba(0, 0, 0, 0.68)";
      return "rgba(0, 0, 0, 0.34)";
    };

    const getCheckCircleColor = (): string => {
      if (isFocusedHover) return "rgb(2, 250, 23)";
      if (index === hoveredIndex) return "rgba(2, 250, 23, 0.68)";
      return "rgba(0, 0, 0, 0.34)";
    };

    return inFavorites ? (
      <Tooltip title="Remove from favorites">
        <CheckCircleIcon
          style={{
            color: getCheckCircleColor(),
            transition: "color 150ms ease",
            cursor: "pointer",
          }}
          onMouseEnter={() => setIsFocusedHover(true)}
          onMouseLeave={() => setIsFocusedHover(false)}
          onClick={() => handleRemoveFromFavorites(movie.id)}
        />
      </Tooltip>
    ) : (
      <Tooltip title="Add to favorites">
        <ControlPointIcon
          style={{
            color: getPlusColor(),
            transition: "color 150ms ease",
            cursor: "pointer",
          }}
          onMouseEnter={() => setIsFocusedHover(true)}
          onMouseLeave={() => setIsFocusedHover(false)}
          onClick={() => handleAddToFavorites(movie)}
        />
      </Tooltip>
    );
  },
  (prevProps, nextProps) =>
    prevProps.index === nextProps.index &&
    prevProps.hoveredIndex === nextProps.hoveredIndex
);
