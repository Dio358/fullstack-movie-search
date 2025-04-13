import { BASE_URL } from "./backendURL";
import { Movie } from "../interfaces";

export const fetchMostPopularMovies = async (token: string, count: number = 20) => {
    try {
      const res = await fetch(`${BASE_URL}/movies/most_popular/${count}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: "Bearer " + token,
        },
      });
  
      const data = await res.json();
  
      if (res.ok) {
        return data;
      } else {
        return null;
      }
    } catch (err) {
      console.error("Failed to fetch most popular movies:", err);
      return null;
    }
  };
  
export const addMovieToFavorites = async (token: string, movie_id: number) => {
    try {
      await fetch(
        `${BASE_URL}/movies/favorite/` + encodeURIComponent(movie_id),
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log("Movie added to favorites successfully");
    } catch (err) {
      console.error("Failed to add movie to favorites:", err);
    }
  };

  
export const deleteMovieFromFavorites = async (token: string, movie_id: number) => {
    console.log("removing movie from favorites:", movie_id);
    console.log("Token:", token);
    try {
      await fetch(
        `${BASE_URL}/movies/favorite/` + encodeURIComponent(movie_id),
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log("Movie removed from favorites successfully");
    } catch (err) {
      console.error("Failed to add movie to favorites:", err);
    }
  };

export const fetchFavoriteMovies = async (token: string) => {
  try {
    const res = await fetch(`${BASE_URL}/movies/favorite`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    });

    const data = await res.json();
    console.log("results: ", data)

    if (res.ok) {
      return data.results;
    } else {
      return null;
    }
  } catch (err) {
    console.error("Failed to fetch favorite movies:", err);
    return null;
  }
};


export const searchMovies = async (token: string, query: string): Promise<{ value: number; label: string }[]> => {
  if (!query.trim()) return [];

  try {
    const res = await fetch(`${BASE_URL}/movies/${encodeURIComponent(query)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    });

    const data = await res.json();

    if (res.ok && Array.isArray(data?.results)) {
      return data.results.map((movie: Movie) => ({
        value: movie.id,
        label: movie.title,
      }));
    }

    return [];
  } catch (err) {
    console.error("Failed to search movies:", err);
    return [];
  }
};

export const fetchSameGenreMovies = async (token: string, title: string): Promise<Movie[]> => {
  try {
    const res = await fetch(`${BASE_URL}/movies/same_genres/${encodeURIComponent(title)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    });

    const data = await res.json();
    return res.ok && Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Failed to fetch same genre movies:", err);
    return [];
  }
};

export const fetchSimilarRuntimeMovies = async (token: string, title: string): Promise<Movie[]> => {
  try {
    const res = await fetch(`${BASE_URL}/movies/similar_runtime/${encodeURIComponent(title)}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: "Bearer " + token,
      },
    });

    const data = await res.json();
    return res.ok && Array.isArray(data) ? data : [];
  } catch (err) {
    console.error("Failed to fetch similar runtime movies:", err);
    return [];
  }
};
