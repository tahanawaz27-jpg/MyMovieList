from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_get_movies():
    response = client.get("/movies/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_movie():
    response = client.post(
        "/movies/",
        json={
            "title": "Inception",
            "director": "Christopher Nolan",
            "genre": "Sci-Fi",
            "release_year": 2010,
            "rating": 9,
            "watched": True
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Inception"


def test_get_movie():
    response = client.get("/movies/1")

    assert response.status_code == 200


def test_get_movie_not_found():
    response = client.get("/movies/9999")

    assert response.status_code == 404


def test_invalid_rating():
    response = client.post(
        "/movies/",
        json={
            "title": "Batman",
            "director": "Nolan",
            "genre": "Action",
            "release_year": 2008,
            "rating": 20,
            "watched": True
        }
    )

    assert response.status_code == 422