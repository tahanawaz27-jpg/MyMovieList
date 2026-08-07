import sys
import asyncio

# Fix WinError 10054 asyncio socket closure bug on Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.routers.movie import router
from app.routers.user import router as user_router
from fastapi import FastAPI

from app.database import Base, engine
from app.models.movie import Movie
from app.models.user import User
from app.utils.logger import logger


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(title="MyMovieList API")


@app.on_event("startup")
def startup_event():
    logger.info("MyMovieList API started successfully")


@app.on_event("shutdown")
def shutdown_event():
    logger.info("MyMovieList API shutting down")


@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to MyMovieList API"}


# Include movie routes
app.include_router(router)
app.include_router(user_router)