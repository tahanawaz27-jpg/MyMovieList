from sqlalchemy.orm import Session
from app.models.movie import Movie
from app.schemas.movie import MovieCreate


def create_movie(db: Session, movie: MovieCreate):
    new_movie = Movie(
        title=movie.title,
        director=movie.director,
        genre=movie.genre,
        release_year=movie.release_year,
        rating=movie.rating,
        watched=movie.watched
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie


def get_movies(db: Session):
    return db.query(Movie).all()


def get_movie(db: Session, movie_id: int):
    return db.query(Movie).filter(Movie.id == movie_id).first()


def update_movie(db: Session, movie_id: int, movie: MovieCreate):
    existing_movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not existing_movie:
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
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        return None

    db.delete(movie)
    db.commit()

    return movie