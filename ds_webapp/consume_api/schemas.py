"""
A file containing pydantic type schemas
"""

from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class Movie(BaseModel):
    """
    A model representing a movie
    """

    adult: bool
    backdrop_path: Optional[str]
    genre_ids: List[int]
    id: int
    original_language: str
    original_title: str
    overview: str
    popularity: float
    poster_path: Optional[str]
    release_date: date
    title: str
    video: bool
    vote_average: float
    vote_count: int
