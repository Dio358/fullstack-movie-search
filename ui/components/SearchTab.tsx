import {useState} from "react";
import List from "./List";
import * as React from "react";
import { Movie } from "../interfaces";

export const SearchTab = ({
    token,
  }: {
    token: string;
  }) => {
    const [selectedLength, setSelectedLength] = useState(1);
    const [selectedMovie, setSelectedMovie] = useState(-1);
    const [hoveredIndex, setHoveredIndex] = React.useState<number | null>(null);
    const [title, setTitle] = React.useState<string>("");
    const [searchResult, setSearchResult] = React.useState<Movie[]>([]);
    
    const handleInput = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTitle(e.target.value);
    };

    const searchMovie = async () => {
        if (!title.trim()) {
            setSearchResult([]);
            return;
        }
        
        try {
            const res = await fetch("/api/backend-proxy/movies/" + encodeURIComponent(title), {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + token,
                },
            });
    
            const data = await res.json();
            console.log("Data from backend:", data.results);
            console.log("res.ok:", res.ok);
          
            if (res.ok) {
                setSearchResult(Array.isArray(data?.results) ? data.results : []);
            } 
        } catch (err) {
            console.error("Failed to fetch from backend:", err);
            setSearchResult([]);
        }
    };

    React.useEffect(() => {
        searchMovie();
    }, [title]);

    return (
        <div style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            marginLeft: "20px",
            paddingLeft: "10%"
        }}>
            <div style={{display: "flex", flexDirection: "row", alignItems: "center", gap: "10px"}}>
                <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Search Movie</h1>
                <input
                    type="text"
                    placeholder="Search for a movie..."
                    value={title}
                    onChange={handleInput}
                    style={{
                        padding: "8px",
                        fontSize: "16px",
                        borderRadius: "4px",
                        border: "1px solid #ccc"
                    }}
                />        
            </div>
            
            {searchResult.length > 0 ? (
                <List items={searchResult} action="add to"/>
            ) : (
                <p>{title.trim() ? "No results found" : "Type to search for movies"}</p>
            )}
            
            <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies in the Same Genres</h1>
            {/* <List items={movies} action="remove from"/> */}

            <h1 style={{fontFamily: "Arial", textAlign: "center", marginBottom: "20px"}}>Movies with Similar Runtimes</h1>
            {/* <List items={movies} action="remove from"/> */}
        </div>
    );
}