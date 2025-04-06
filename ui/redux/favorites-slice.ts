import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Movie } from "../interfaces";

interface favoritesState {
    movies: Movie[];

}

const initialState: favoritesState = {
    movies: []
};

const favoritesSlice = createSlice({
    name: "list",
    initialState,
    reducers: {
        // add Movie
        addMovie(state, action) {
            state.movies.push(action.payload)
        },
        // load Movies
        getMovies(state) {

        },
        // delete movie
        deleteMovie(state, action) {
            state.movies.filter(movie => movie.id !== action.payload.id)
        }
    }
})

export const { addMovie, getMovies, deleteMovie} = favoritesSlice.actions
export default favoritesSlice.reducer