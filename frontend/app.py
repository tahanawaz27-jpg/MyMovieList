import streamlit as st

from api import MovieAPI
from components.sidebar import sidebar
from views.add_movie import add_movie_page
from views.ai import ai_page
from views.dashboard import dashboard_page
from views.login import login_page

st.set_page_config(
    page_title="MyMovieList",
    page_icon="🎬",
)

# ---------------- PERSISTENT SESSION ---------------- #

# 1. Initialize token state from URL query params if present
if "token" not in st.session_state:
    st.session_state.token = st.query_params.get("token", None)

api = MovieAPI()

if st.session_state.token:
    api.set_token(st.session_state.token)

# ---------------- UI ---------------- #

st.title("🎬 MyMovieList")

# ---------------- AUTH GUARD ---------------- #

if not st.session_state.token:
    login_page(api)
    st.stop()

# ---------------- ROUTING ---------------- #

page = sidebar()

if page == "Dashboard":
    dashboard_page(api)

elif page == "Add Movie":
    add_movie_page(api)

elif page == "AI Recommendation":
    ai_page(api)