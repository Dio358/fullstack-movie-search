import { createSlice } from '@reduxjs/toolkit';
import { fetchFavorites } from './favorites-thunks';
import { Movie } from '../interfaces';

interface favoritesState {
  movies: Movie[];
}

const initialState: favoritesState = {
  movies: [],
};

const favoritesSlice = createSlice({
  name: 'list',
  initialState,
  reducers: {
    addMovie(state, action) {
        if (!state.movies.some((m) => action.payload.id === m.id))
            state.movies.push(action.payload);
    },
    deleteMovie(state, action) {
      state.movies = state.movies.filter(movie => movie.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder.addCase(fetchFavorites.fulfilled, (state, action) => {
      state.movies = action.payload;
    });
  },
});

export const { addMovie, deleteMovie } = favoritesSlice.actions;
export default favoritesSlice.reducer;
