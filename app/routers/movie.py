from fastapi import APIRouter, HTTPException, status

from app.schemas.movie import (
    MovieCreate,
    MovieUpdate,
    MovieResponse,
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
def create_movie(movie: MovieCreate):
    try:
        logger.info(
            f"Creating movie: {movie.title}"
        )

        created_movie = movie_service.create_movie(movie)

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


# ---------------- GET ALL ---------------- #

@router.get(
    "/",
    response_model=list[MovieResponse],
)
def get_movies():
    try:
        logger.info(
            "Fetching all movies"
        )

        movies = movie_service.get_movies()

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
# Must come BEFORE /{movie_id}

@router.get(
    "/recommend",
    response_model=RecommendationResponse,
)
def ai_recommend(title: str):
    try:
        logger.info(
            f"AI recommendation requested for '{title}'"
        )

        recommendation = recommend_movie(title)

        logger.info(
            "Recommendation generated successfully"
        )

        return {
            "recommendation": recommendation
        }

    except HTTPException:
        raise

    except Exception as e:
        logger.exception(
            f"Recommendation error: {e}"
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to generate recommendation.",
        )


# ---------------- GET ONE ---------------- #

@router.get(
    "/{movie_id}",
    response_model=MovieResponse,
)
def get_movie(movie_id: int):
    try:
        logger.info(
            f"Fetching movie {movie_id}"
        )

        movie = movie_service.get_movie(movie_id)

        if movie is None:
            logger.warning(
                f"Movie {movie_id} not found"
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
):
    try:
        logger.info(
            f"Updating movie {movie_id}"
        )

        updated_movie = movie_service.update_movie(
            movie_id,
            movie,
        )

        if updated_movie is None:
            logger.warning(
                f"Movie {movie_id} not found"
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
def delete_movie(movie_id: int):
    try:
        logger.info(
            f"Deleting movie {movie_id}"
        )

        movie = movie_service.delete_movie(movie_id)

        if movie is None:
            logger.warning(
                f"Movie {movie_id} not found"
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