import { useState, useContext, useEffect } from "react";
import List from "../list/List";
import { Movie } from "../../interfaces";
import AsyncSelect from "react-select/async";
import { Title } from "../elements/Title";
import { Token } from "../login/Token";
import {
  searchMovies,
  fetchSameGenreMovies,
  fetchSimilarRuntimeMovies,
} from "../../api/movieApi";

export const SearchTab = () => {
  const [selectedMovie, setSelectedMovie] = useState<string | null>(null);
  const [sameGenreMovies, setSameGenreMovies] = useState<Movie[]>([]);
  const [similarRuntimeMovies, setSimilarRuntimeMovies] = useState<Movie[]>([]);
  const token = useContext(Token);

  const loadOptions = (inputValue: string) => {
    return searchMovies(token, inputValue);
  };

  useEffect(() => {
    const fetchRelatedMovies = async () => {
      if (!selectedMovie) {
        setSameGenreMovies([]);
        setSimilarRuntimeMovies([]);
        return;
      }

      try {
        const [sameGenre, similarRuntime] = await Promise.all([
          fetchSameGenreMovies(token, selectedMovie),
          fetchSimilarRuntimeMovies(token, selectedMovie),
        ]);

        setSameGenreMovies(sameGenre);
        setSimilarRuntimeMovies(similarRuntime);
      } catch (err) {
        console.error("Failed to fetch related movies:", err);
        setSameGenreMovies([]);
        setSimilarRuntimeMovies([]);
      }
    };

    fetchRelatedMovies();
  }, [selectedMovie]);

  const handleSelect = (option: any) => {
    setSelectedMovie(option?.label ?? null);
  };

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
      <div
        style={{
          display: "flex",
          flexDirection: "row",
          alignItems: "center",
          gap: "10px",
          minWidth: "400px",
        }}
      >
        <AsyncSelect
          cacheOptions
          loadOptions={loadOptions}
          onChange={handleSelect}
          placeholder="Search for a movie..."
          defaultOptions
          styles={{
            container: (base) => ({
              ...base,
              flex: 1,
            }),
          }}
        />
      </div>

      <Title>Movies in the Same Genres</Title>
      <List items={sameGenreMovies} maxHeight="200px" action="remove from" />

      <Title>Movies with Similar Runtimes</Title>
      <List
        items={similarRuntimeMovies}
        maxHeight="200px"
        action="remove from"
      />
    </div>
  );
};
