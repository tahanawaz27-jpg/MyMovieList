from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas.movie import MovieCreate, MovieResponse
from app.services import movie_service

router = APIRouter(prefix="/movies", tags=["Movies"])


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MovieResponse)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db)):
    return movie_service.create_movie(db, movie)


@router.get("/", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):
    return movie_service.get_movies(db)


@router.get("/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = movie_service.get_movie(db, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieCreate, db: Session = Depends(get_db)):
    updated_movie = movie_service.update_movie(db, movie_id, movie)

    if not updated_movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return updated_movie


@router.delete("/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = movie_service.delete_movie(db, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return {"message": "Movie deleted successfully"}