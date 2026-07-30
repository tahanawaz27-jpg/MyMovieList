#handles API requests
from fastapi import FastAPI

from app.database import Base, engine
from app.models.movie import Movie
from app.routers.movie import router

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="MyMovieList API")
@app.get("/")
def root():
    return {"message": "Welcome to MyMovieList API"}
# Include movie routes
app.include_router(router)  