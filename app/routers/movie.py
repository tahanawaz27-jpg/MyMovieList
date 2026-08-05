# API endpoints
from app.utils.logger import logger
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.movie import MovieCreate, MovieResponse
from app.services import movie_service
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse,
)

from app.services.ai_service import recommend_movie
router = APIRouter(prefix="/movies", tags=["Movies"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED
)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):

    logger.info(f"Creating movie: {movie.title}")

    created_movie = movie_service.create_movie(db, movie)

    logger.info(
        f"Movie created successfully with id: {created_movie.id}"
    )

    return created_movie


@router.get("/", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):

    logger.info("Fetching all movies")

    movies = movie_service.get_movies(db)

    logger.info(f"Total movies found: {len(movies)}")

    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):

    logger.info(f"Fetching movie with id: {movie_id}")

    movie = movie_service.get_movie(db, movie_id)

    if movie is None:
        logger.warning(
            f"Movie with id {movie_id} not found"
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie: MovieCreate,
    db: Session = Depends(get_db)
):

    logger.info(f"Updating movie id: {movie_id}")

    updated_movie = movie_service.update_movie(
        db,
        movie_id,
        movie
    )

    if updated_movie is None:
        logger.warning(
            f"Movie id {movie_id} not found for update"
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    logger.info(
        f"Movie id {movie_id} updated successfully"
    )

    return updated_movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):

    logger.info(f"Deleting movie id: {movie_id}")

    movie = movie_service.delete_movie(db, movie_id)

    if movie is None:

        logger.warning(
            f"Movie id {movie_id} not found for deletion"
        )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )

    logger.info(
        f"Movie id {movie_id} deleted successfully"
    )

    return {"message": "Movie deleted successfully"}

@router.post(
    "/recommend",
    response_model=RecommendationResponse
)
def ai_recommend(movie: RecommendationRequest):

    logger.info(
        f"AI recommendation requested for: {movie.title}"
    )

    recommendation = recommend_movie(
        movie.title,
        movie.genre,
        movie.rating,
    )

    logger.info(
        "AI recommendation generated successfully"
    )

    return {
        "recommendation": recommendation
    }