import os
import requests
import streamlit as st


BASE_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


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

        return st.session_state.get(
            "token",
            None
        )



    @property
    def headers(self):

        if self.token:

            return {
                "Authorization": f"Bearer {self.token}"
            }

        return {}



    def request_error(self, error):

        st.error(
            f"API connection error: {error}"
        )



    # ---------------- USERS ---------------- #

    def register(self, data):

        try:

            return requests.post(
                f"{BASE_URL}/users/register",
                json=data,
                timeout=REQUEST_TIMEOUT,
            )

        except requests.exceptions.RequestException as e:

            self.request_error(e)

            return None



    def login(self, username, password):

        try:

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

                timeout=REQUEST_TIMEOUT,
            )


        except requests.exceptions.RequestException as e:

            self.request_error(e)

            return None



    # ---------------- MOVIES ---------------- #

    def get_movies(self):

        return requests.get(
            f"{BASE_URL}/movies/",
            headers=self.headers,
        )


    def get_movie(self, movie_id):

        return requests.get(
            f"{BASE_URL}/movies/{movie_id}",
            headers=self.headers,
        )


    def create_movie(self, movie):

        return requests.post(
            f"{BASE_URL}/movies/",
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

        try:

            return requests.get(
                f"{BASE_URL}/movies/recommend",

                params={
                    "title": title,
                },

                headers=self.headers,

                timeout=REQUEST_TIMEOUT,
            )


        except requests.exceptions.RequestException as e:

            self.request_error(e)

            return None