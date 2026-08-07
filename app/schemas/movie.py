# app/schemas/movie.py
from typing import Optional
from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    title: str
    director: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    watched: Optional[bool] = False
    is_watched: Optional[bool] = False


class MovieCreate(MovieBase):
    pass


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    director: Optional[str] = None
    genre: Optional[str] = None
    release_year: Optional[int] = None
    rating: Optional[float] = None
    watched: Optional[bool] = False
    is_watched: Optional[bool] = False


class MovieResponse(MovieBase):
    id: int
    user_id: Optional[int] = None
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)