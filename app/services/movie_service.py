from sqlalchemy.exc import SQLAlchemyError

from app.database import SessionLocal
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate
from app.utils.logger import logger


def create_movie(movie: MovieCreate):
    db = SessionLocal()

    try:
        logger.info(
            f"Saving movie '{movie.title}'"
        )

        new_movie = Movie(
            title=movie.title,
            director=movie.director,
            genre=movie.genre,
            release_year=movie.release_year,
            rating=movie.rating,
            watched=movie.watched,
        )

        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

        logger.info(
            f"Movie created with id {new_movie.id}"
        )

        return new_movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise

    finally:
        db.close()


def get_movies():
    db = SessionLocal()

    try:
        movies = db.query(Movie).all()

        logger.info(
            f"{len(movies)} movies retrieved"
        )

        return movies

    except SQLAlchemyError as e:
        logger.exception(e)
        raise

    finally:
        db.close()


def get_movie(movie_id: int):
    
    db = SessionLocal()

    try:
        movie = db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

        return movie

    except SQLAlchemyError as e:
        logger.exception(e)
        raise

    finally:
        db.close()


def update_movie(
    movie_id: int,
    movie: MovieUpdate,
):
    db = SessionLocal()

    try:
        existing_movie = db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

        if existing_movie is None:
            return None

        update_data = movie.model_dump(
            exclude_unset=True
        )

        for key, value in update_data.items():
            setattr(
                existing_movie,
                key,
                value
            )

        db.commit()
        db.refresh(existing_movie)

        logger.info(
            f"Movie {movie_id} updated"
        )

        return existing_movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise

    finally:
        db.close()


def delete_movie(movie_id: int):
    db = SessionLocal()

    try:
        movie = db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

        if movie is None:
            return None

        db.delete(movie)
        db.commit()

        logger.info(
            f"Movie {movie_id} deleted"
        )

        return movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise

    finally:
        db.close()