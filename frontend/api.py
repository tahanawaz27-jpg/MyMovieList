# frontend/api.py

import os
import requests
import streamlit as st

BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
REQUEST_TIMEOUT = 15


class MovieAPI:

    def __init__(self):
        if "token" not in st.session_state:
            st.session_state.token = None

    # ---------------- AUTH ---------------- #

    def set_token(self, token: str):
        st.session_state.token = token

    def clear_token(self):
        st.session_state.token = None

    @property
    def token(self):
        return st.session_state.get("token", None)

    @property
    def headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ---------------- REQUEST HELPER ---------------- #

    def _request(self, method: str, endpoint: str, **kwargs):
        """Centralized helper for handling API requests and network exceptions."""
        url = f"{BASE_URL}{endpoint}"
        headers = kwargs.pop("headers", {})
        merged_headers = {**self.headers, **headers}

        try:
            return requests.request(
                method=method,
                url=url,
                headers=merged_headers,
                timeout=REQUEST_TIMEOUT,
                **kwargs,
            )
        except requests.exceptions.RequestException as e:
            st.error(f"API Connection Error: {e}")
            return None

    # ---------------- USERS ---------------- #

    def register(self, data: dict):
        return self._request("POST", "/users/register", json=data)

    def login(self, username, password):
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "username": username,
            "password": password,
            "scope": "",
            "client_id": "",
            "client_secret": "",
        }
        return self._request("POST", "/users/login", headers=headers, data=data)

    # ---------------- MOVIES ---------------- #

    def get_movies(self, search: str = None):
        """Fetch movies with optional title search query."""
        params = {}
        if search:
            params["search"] = search
        return self._request("GET", "/movies/", params=params)

    def get_movie(self, movie_id):
        return self._request("GET", f"/movies/{movie_id}")

    def create_movie(self, movie: dict):
        return self._request("POST", "/movies/", json=movie)

    def update_movie(self, movie_id, movie: dict):
        return self._request("PATCH", f"/movies/{movie_id}", json=movie)

    def delete_movie(self, movie_id):
        return self._request("DELETE", f"/movies/{movie_id}")

    # ---------------- AI ---------------- #

    def recommend_movie(self, title: str):
        return self._request("GET", "/movies/recommend", params={"title": title})