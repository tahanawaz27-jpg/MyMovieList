import requests

# Change this when deploying
import os

BASE_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


class MovieAPI:

    def __init__(self):
        self.token = None

    def set_token(self, token: str):
        self.token = token

    @property
    def headers(self):
        if self.token:
            return {
                "Authorization": f"Bearer {self.token}"
            }
        return {}

    # ---------------- USERS ---------------- #

    def register(self, data):
        return requests.post(
            f"{BASE_URL}/users/register",
            json=data,
        )

    def login(self, username, password):
        return requests.post(
            f"{BASE_URL}/users/login",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "username": username,
                "password": password,
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )

    # ---------------- MOVIES ---------------- #

    def get_movies(self):
        return requests.get(
            f"{BASE_URL}/movies",
            headers=self.headers,
        )

    def get_movie(self, movie_id):
        return requests.get(
            f"{BASE_URL}/movies/{movie_id}",
            headers=self.headers,
        )

    def create_movie(self, movie):
        return requests.post(
            f"{BASE_URL}/movies",
            json=movie,
            headers=self.headers,
        )

    def update_movie(self, movie_id, movie):
        return requests.patch(
            f"{BASE_URL}/movies/{movie_id}",
            json=movie,
            headers=self.headers,
        )

    def delete_movie(self, movie_id):
        return requests.delete(
            f"{BASE_URL}/movies/{movie_id}",
            headers=self.headers,
        )

    # ---------------- AI ---------------- #

    def recommend_movie(self, title):
        return requests.get(
            f"{BASE_URL}/movies/recommend",
            params={
                "title": title,
            },
            headers=self.headers,
        )