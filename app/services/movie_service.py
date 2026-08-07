from typing import Optional
from sqlalchemy import or_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate
from app.utils.logger import logger


def create_movie(
    db: Session,
    movie: MovieCreate,
    user_id: int,
):
    try:
        new_movie = Movie(
            title=movie.title,
            director=movie.director,
            genre=movie.genre,
            release_year=movie.release_year,
            rating=movie.rating,
            watched=movie.watched,
            owner_id=user_id,
        )

        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

        logger.info(f"Movie created: {new_movie.title}")

        return new_movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise


def get_movies(
    db: Session,
    user_id: int,
    search: Optional[str] = None,
):
    try:
        query = db.query(Movie).filter(Movie.owner_id == user_id)

        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Movie.title.ilike(search_pattern),
                    Movie.director.ilike(search_pattern),
                    Movie.genre.ilike(search_pattern),
                )
            )

        return query.all()

    except SQLAlchemyError as e:
        logger.exception(e)
        raise


def get_movie(
    db: Session,
    movie_id: int,
    user_id: int,
):
    try:
        return (
            db.query(Movie)
            .filter(
                Movie.id == movie_id,
                Movie.owner_id == user_id,
            )
            .first()
        )

    except SQLAlchemyError as e:
        logger.exception(e)
        raise


def update_movie(
    db: Session,
    movie_id: int,
    movie: MovieUpdate,
    user_id: int,
):
    try:
        existing_movie = (
            db.query(Movie)
            .filter(
                Movie.id == movie_id,
                Movie.owner_id == user_id,
            )
            .first()
        )

        if existing_movie is None:
            return None

        update_data = movie.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(existing_movie, key, value)

        db.commit()
        db.refresh(existing_movie)

        return existing_movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise


def delete_movie(
    db: Session,
    movie_id: int,
    user_id: int,
):
    try:
        movie = (
            db.query(Movie)
            .filter(
                Movie.id == movie_id,
                Movie.owner_id == user_id,
            )
            .first()
        )

        if movie is None:
            return None

        db.delete(movie)
        db.commit()

        return movie

    except SQLAlchemyError as e:
        db.rollback()
        logger.exception(e)
        raise