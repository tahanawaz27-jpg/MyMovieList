import streamlit as st


def dashboard_page(api):
    st.header("🎬 My Movies")

    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("🔄 Refresh Movies", use_container_width=True):
            st.rerun()

    # ---------------- SEARCH BAR ---------------- #
    search_query = st.text_input(
        "🔍 Search Movies",
        placeholder="Search by title, director, or genre...",
        key="movie_search_query",
    )

    # Fetch movies from API (passing search_query if API supports backend filtering)
    response = api.get_movies(search=search_query)

    if response is None or response.status_code != 200:
        st.error("Unable to fetch movies from server.")
        return

    movies = response.json()

    # Client-side fallback filtering to guarantee instant search
    if search_query and movies:
        query_lower = search_query.lower()
        movies = [
            m for m in movies
            if query_lower in str(m.get("title", "")).lower()
            or query_lower in str(m.get("director", "")).lower()
            or query_lower in str(m.get("genre", "")).lower()
        ]

    if not movies:
        if search_query:
            st.info(f"No movies found matching '{search_query}'.")
        else:
            st.info("No movies added yet.")
        return

    st.write(f"Showing **{len(movies)}** movie(s):")

    # ---------------- MOVIE LIST ---------------- #
    for movie in movies:
        movie_id = movie["id"]

        with st.expander(f"🎬 {movie.get('title', 'Untitled')}"):

            # ---------------- READ-ONLY MODE ---------------- #
            if not st.session_state.get(f"editing_{movie_id}", False):

                st.write(f"**Director:** {movie.get('director', 'N/A')}")
                st.write(f"**Genre:** {movie.get('genre', 'N/A')}")
                st.write(f"**Release Year:** {movie.get('release_year', 'N/A')}")
                st.write(f"**Rating:** ⭐ {movie.get('rating', 'N/A')}")
                st.write(
                    f"**Watched:** {'✅ Yes' if movie.get('watched') else '❌ No'}"
                )

                btn_col1, btn_col2 = st.columns(2)

                with btn_col1:
                    if st.button("✏ Edit", key=f"edit_{movie_id}"):
                        st.session_state[f"editing_{movie_id}"] = True
                        st.rerun()

                with btn_col2:
                    if st.button("🗑 Delete", key=f"delete_{movie_id}"):
                        delete_response = api.delete_movie(movie_id)

                        if delete_response and delete_response.status_code in (200, 204):
                            st.success("Movie deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Unable to delete movie.")

            # ---------------- EDIT MODE ---------------- #
            else:

                title = st.text_input(
                    "Title",
                    value=movie.get("title", ""),
                    key=f"title_{movie_id}",
                )

                director = st.text_input(
                    "Director",
                    value=movie.get("director", ""),
                    key=f"director_{movie_id}",
                )

                genre = st.text_input(
                    "Genre",
                    value=movie.get("genre", ""),
                    key=f"genre_{movie_id}",
                )

                release_year = st.number_input(
                    "Release Year",
                    min_value=1888,
                    max_value=2026,
                    value=int(movie.get("release_year", 2024)),
                    key=f"year_{movie_id}",
                )

                rating = st.slider(
                    "Rating",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(movie.get("rating", 0.0)),
                    step=0.1,
                    key=f"rating_{movie_id}",
                )

                watched = st.checkbox(
                    "Watched",
                    value=bool(movie.get("watched", False)),
                    key=f"watched_{movie_id}",
                )

                save_col1, save_col2 = st.columns(2)

                with save_col1:
                    if st.button("💾 Save", key=f"save_{movie_id}"):
                        update_response = api.update_movie(
                            movie_id,
                            {
                                "title": title,
                                "director": director,
                                "genre": genre,
                                "release_year": release_year,
                                "rating": rating,
                                "watched": watched,
                            },
                        )

                        if update_response and update_response.status_code == 200:
                            st.session_state[f"editing_{movie_id}"] = False
                            st.success("Movie updated!")
                            st.rerun()
                        else:
                            st.error("Unable to update movie.")

                with save_col2:
                    if st.button("❌ Cancel", key=f"cancel_{movie_id}"):
                        st.session_state[f"editing_{movie_id}"] = False
                        st.rerun()