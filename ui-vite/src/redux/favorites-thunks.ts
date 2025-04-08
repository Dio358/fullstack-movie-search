import { createAsyncThunk } from '@reduxjs/toolkit';
import { fetchFavoriteMovies } from '../api/movieApi';
import { Movie } from '../interfaces';

export const fetchFavorites = createAsyncThunk<Movie[], string>(
  'favorites/fetch',
  async (token: string) => {
    const data = await fetchFavoriteMovies(token);
    return data;
  }
);
