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
        description="Release year"
    )

    rating: float = Field(
        ...,
        ge=0,
        le=10,
        description="Movie rating"
    )

    watched: bool


class MovieUpdate(BaseModel):
    title: str | None = Field(
        None,
        min_length=2,
        max_length=100,
    )

    director: str | None = Field(
        None,
        min_length=2,
        max_length=100,
    )

    genre: str | None = Field(
        None,
        min_length=2,
        max_length=50,
    )

    release_year: int | None = Field(
        None,
        ge=1888,
        le=2100,
    )

    rating: float | None = Field(
        None,
        ge=0,
        le=10,
    )

    watched: bool | None = None


class MovieResponse(MovieCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )