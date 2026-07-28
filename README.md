# MyMovieList API

A simple REST API built with FastAPI to manage a list of movies.

## Requirements

- Python 3
- FastAPI
- SQLAlchemy
- Uvicorn

## How to Run

1. Clone the repository.
2. Open the project folder.
3. Create and activate a virtual environment.
4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Run the server:

```bash
uvicorn app.main:app --reload
```

6. Open your browser and go to:

```
http://127.0.0.1:8000/docs
```

## Available Endpoints

- POST `/movies`
- GET `/movies`
- GET `/movies/{movie_id}`
- PUT `/movies/{movie_id}`
- DELETE `/movies/{movie_id}`