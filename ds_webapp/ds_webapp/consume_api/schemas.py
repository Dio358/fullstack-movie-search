"""
A file containing pydantic type schemas
"""

from typing import Optional, List
from pydantic import BaseModel


class Movie(BaseModel):
    """
    A class reprenting movies and the fields + types they contain
    """

    adult: bool
    backdrop_path: Optional[str] = None
    genre_ids: Optional[List[int]] = None
    id: int
    original_language: str
    original_title: str
    overview: Optional[str] = None
    popularity: Optional[float] = None
    poster_path: Optional[str] = None
    release_date: Optional[str] = None
    title: str
    video: Optional[bool] = None
    vote_average: Optional[float] = None
    vote_count: Optional[int] = None
