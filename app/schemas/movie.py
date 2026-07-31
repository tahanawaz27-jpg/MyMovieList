# Checks input/output data

from pydantic import BaseModel, Field, ConfigDict


class MovieCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Movie title"
    )

    director: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Director name"
    )

    genre: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Movie genre"
    )

    release_year: int = Field(
        ...,
        ge=1888,
        le=2100,
        description="Year the movie was released"
    )

    rating: float = Field(
        ...,
        ge=0,
        le=10,
        description="Movie rating between 0 and 10"
    )

    watched: bool


class MovieResponse(MovieCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)