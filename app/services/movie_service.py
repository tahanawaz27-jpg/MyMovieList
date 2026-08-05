from app.utils.logger import logger
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.schemas.movie import MovieCreate


def create_movie(db: Session, movie: MovieCreate):

    logger.info(
        f"Saving movie to database: {movie.title}"
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
        f"Database save successful. Movie id: {new_movie.id}"
    )

    return new_movie


def get_movies(db: Session):
    return db.query(Movie).all()


def get_movie(db: Session, movie_id: int):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    return movie


def update_movie(db: Session, movie_id: int, movie: MovieCreate):
    existing_movie = db.query(Movie).filter(Movie.id == movie_id).first()

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

    return existing_movie


def delete_movie(db: Session, movie_id: int):

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