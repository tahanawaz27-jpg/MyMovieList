from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user, get_db
from app.models.user import User
from app.schemas.movie import (
    MovieCreate,
    MovieResponse,
    MovieUpdate,
)
from app.schemas.recommendation import RecommendationResponse
from app.services import movie_service
from app.services.ai_service import recommend_movie
from app.utils.logger import logger

router = APIRouter(
    prefix="/movies",
    tags=["Movies"],
)


# ---------------- CREATE ---------------- #

@router.post(
    "/",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_movie(
    movie: MovieCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Creating movie '{movie.title}' for user {current_user.id}"
        )

        created_movie = movie_service.create_movie(
            db,
            movie,
            current_user.id,
        )

        logger.info(
            f"Movie created successfully with id {created_movie.id}"
        )

        return created_movie

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Unexpected error while creating movie: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the movie.",
        )


# ---------------- GET ALL / SEARCH ---------------- #

@router.get(
    "/",
    response_model=list[MovieResponse],
)
def get_movies(
    search: Optional[str] = Query(None, description="Search query for filtering movies"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Fetching movies for user {current_user.id} with search='{search}'"
        )

        movies = movie_service.get_movies(
            db=db,
            user_id=current_user.id,
            search=search,
        )

        logger.info(
            f"Retrieved {len(movies)} movies"
        )

        return movies

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Unexpected error while fetching movies: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching movies.",
        )


# ---------------- AI RECOMMEND ---------------- #

@router.get(
    "/recommend",
    response_model=RecommendationResponse,
)
def ai_recommend(
    title: str,
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"AI recommendation requested by user {current_user.id} for '{title}'"
        )

        recommendations = recommend_movie(title)

        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to generate recommendations.",
            )

        logger.info("Recommendation generated successfully")

        return {"recommendations": recommendations}

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(f"Recommendation error: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate recommendation.",
        )

# ---------------- GET ONE ---------------- #

@router.get(
    "/{movie_id}",
    response_model=MovieResponse,
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Fetching movie {movie_id} for user {current_user.id}"
        )

        movie = movie_service.get_movie(
            db,
            movie_id,
            current_user.id,
        )

        if movie is None:
            logger.warning(
                f"Movie {movie_id} not found for user {current_user.id}"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found",
            )

        return movie

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Unexpected error while fetching movie {movie_id}: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while fetching the movie.",
        )


# ---------------- PATCH ---------------- #

@router.patch(
    "/{movie_id}",
    response_model=MovieResponse,
)
def update_movie(
    movie_id: int,
    movie: MovieUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Updating movie {movie_id} for user {current_user.id}"
        )

        updated_movie = movie_service.update_movie(
            db,
            movie_id,
            movie,
            current_user.id,
        )

        if updated_movie is None:
            logger.warning(
                f"Movie {movie_id} not found for user {current_user.id}"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found",
            )

        logger.info(
            f"Movie {movie_id} updated successfully"
        )

        return updated_movie

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Unexpected error while updating movie {movie_id}: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the movie.",
        )


# ---------------- DELETE ---------------- #

@router.delete(
    "/{movie_id}",
)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        logger.info(
            f"Deleting movie {movie_id} for user {current_user.id}"
        )

        movie = movie_service.delete_movie(
            db,
            movie_id,
            current_user.id,
        )

        if movie is None:
            logger.warning(
                f"Movie {movie_id} not found for user {current_user.id}"
            )

            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Movie not found",
            )

        logger.info(
            f"Movie {movie_id} deleted successfully"
        )

        return {
            "message": "Movie deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Unexpected error while deleting movie {movie_id}: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while deleting the movie.",
        )

@router.get("/recommend")
def ai_recommend(
    title: str,
    current_user: User = Depends(get_current_user),
):
    recommendations = recommend_movie(title)
    if not recommendations:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate recommendations at this time.",
        )

    return {"recommendations": recommendations}    