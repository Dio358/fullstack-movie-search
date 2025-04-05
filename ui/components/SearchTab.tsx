import { useState, useContext, useEffect } from "react";
import List from "./List";
import { Movie } from "../interfaces";
import AsyncSelect from "react-select/async";
import { Title } from "./Title";
import { Token } from "./Token";

export const SearchTab = () => {
    const [selectedMovie, setSelectedMovie] = useState<string | null>(null);
    const [searchResult, setSearchResult] = useState<Movie[]>([]);
    const [sameGenreMovies, setSameGenreMovies] = useState<Movie[]>([])
    const [similarRuntimeMovies, setSimilarRuntimeMovies] = useState<Movie[]>([])
    const token = useContext(Token)
    

    const loadOptions = async (inputValue: string): Promise<{ value: number; label: string }[]> => {
        if (!inputValue.trim()) {
            return [];
        }
    
        try {
            const res = await fetch("/api/backend-proxy/movies/" + encodeURIComponent(inputValue), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                },
            });
    
            const data = await res.json();
    
            if (res.ok) {
                const results = Array.isArray(data?.results) ? data.results : [];
    
                setSearchResult(results);
    
                return results.map((movie: Movie) => ({
                    value: movie.id,
                    label: movie.title,
                }));
            } else {
                return [];
            }
        } catch (err) {
            console.error("Failed to fetch from backend:", err);
            return [];
        }
    };
    const getSameGenreMovies = async (title: string): Promise<Movie[]> => {
        try {
            const res = await fetch("/api/backend-proxy/movies/same_genres/" + encodeURIComponent(title), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                },
            });
    
            const data = await res.json();
            return res.ok && Array.isArray(data) ? data : [];
        } catch (err) {
            console.error("Failed to fetch same genre movies:", err);
            return [];
        }
    };
    
    const getSimilarRuntimeMovies = async (title: string): Promise<Movie[]> => {
        try {
            const res = await fetch("/api/backend-proxy/movies/similar_runtime/" + encodeURIComponent(title), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                },
            });
    
            const data = await res.json();
            console.log("data: ", data)
            return res.ok && Array.isArray(data) ? data : [];
        } catch (err) {
            console.error("Failed to fetch similar runtime movies:", err);
            return [];
        }
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
                    getSameGenreMovies(selectedMovie),
                    getSimilarRuntimeMovies(selectedMovie)
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
        <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginLeft: "20px",
            paddingLeft: "10%"
        }}>
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center", gap: "10px", minWidth: "400px" }}>
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
            <List items={sameGenreMovies} onClick={(item) => console.log(item)} maxHeight="200px" action="remove from" />

            <Title>Movies with Similar Runtimes</Title>
            <List items={similarRuntimeMovies} maxHeight="200px" action="remove from" />
        </div>
    );
};
