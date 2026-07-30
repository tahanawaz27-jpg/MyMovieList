#Checks input/output data
from pydantic import BaseModel


class MovieCreate(BaseModel):
    title: str
    director: str
    genre: str
    release_year: int
    rating: float
    watched: bool


class MovieResponse(MovieCreate):
    id: int

    class Config:
        from_attributes = True