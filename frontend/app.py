import streamlit as st

from api import MovieAPI

from components.sidebar import sidebar

from views.login import login_page
from views.dashboard import dashboard_page
from views.add_movie import add_movie_page
from views.ai import ai_page


st.set_page_config(
    page_title="MyMovieList",
    page_icon="🎬",
)


# ---------------- SESSION ---------------- #

if "token" not in st.session_state:
    st.session_state.token = None


# Create API object
api = MovieAPI()


# Restore token after every Streamlit rerun
if st.session_state.token:
    api.set_token(st.session_state.token)


# ---------------- UI ---------------- #

st.title("🎬 MyMovieList")


# ---------------- LOGIN ---------------- #

if not st.session_state.token:

    login_page(api)

    st.stop()


# ---------------- SIDEBAR ---------------- #

page = sidebar()


# ---------------- ROUTING ---------------- #

if page == "Dashboard":

    dashboard_page(api)


elif page == "Add Movie":

    add_movie_page(api)


elif page == "AI Recommendation":

    ai_page(api)