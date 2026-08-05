from app.utils.logger import logger
from app.database import SessionLocal
from app.models.movie import Movie
from app.schemas.movie import MovieCreate


def create_movie(movie: MovieCreate):
    db = SessionLocal()

    try:
        logger.info(f"Saving movie to database: {movie.title}")

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
            f"Database save successful. Movie id: {new_movie.id}"
        )

        return new_movie

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating movie: {e}")
        raise

    finally:
        db.close()


def get_movies():
    db = SessionLocal()

    try:
        return db.query(Movie).all()

    finally:
        db.close()


def get_movie(movie_id: int):
    db = SessionLocal()

    try:
        return db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

    finally:
        db.close()


def update_movie(movie_id: int, movie: MovieCreate):
    db = SessionLocal()

    try:
        existing_movie = db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

        if existing_movie is None:
            return None

        existing_movie.title = movie.title
        existing_movie.director = movie.director
        existing_movie.genre = movie.genre
        existing_movie.release_year = movie.release_year
        existing_movie.rating = movie.rating
        existing_movie.watched = movie.watched

        db.commit()
        db.refresh(existing_movie)

        logger.info(
            f"Movie id {movie_id} updated successfully"
        )

        return existing_movie

    except Exception as e:
        db.rollback()
        logger.error(f"Error updating movie: {e}")
        raise

    finally:
        db.close()


def delete_movie(movie_id: int):
    db = SessionLocal()

    try:
        logger.info(
            f"Searching movie id {movie_id} for deletion"
        )

        movie = db.query(Movie).filter(
            Movie.id == movie_id
        ).first()

        if movie is None:
            logger.warning(
                f"Movie id {movie_id} does not exist"
            )
            return None

        db.delete(movie)
        db.commit()

        logger.info(
            f"Movie id {movie_id} deleted from database"
        )

        return movie

    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting movie: {e}")
        raise

    finally:
        db.close()