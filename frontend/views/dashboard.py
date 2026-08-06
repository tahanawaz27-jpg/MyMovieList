import streamlit as st


def dashboard_page(api):

    st.header("🎬 My Movies")

    if st.button("🔄 Refresh Movies"):
        st.rerun()

    response = api.get_movies()

    if response.status_code != 200:
        st.error("Unable to fetch movies.")
        return

    movies = response.json()

    if not movies:
        st.info("No movies added yet.")
        return

    for movie in movies:

        movie_id = movie["id"]

        with st.expander(f"🎬 {movie['title']}"):

            # Read-only movie information
            if not st.session_state.get(f"editing_{movie_id}", False):

                st.write(f"**Director:** {movie['director']}")
                st.write(f"**Genre:** {movie['genre']}")
                st.write(f"**Release Year:** {movie['release_year']}")
                st.write(f"**Rating:** ⭐ {movie['rating']}")
                st.write(
                    f"**Watched:** {'✅ Yes' if movie['watched'] else '❌ No'}"
                )

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "✏ Edit",
                        key=f"edit_{movie_id}"
                    ):
                        st.session_state[f"editing_{movie_id}"] = True
                        st.rerun()

                with col2:
                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{movie_id}"
                    ):

                        delete_response = api.delete_movie(movie_id)

                        if delete_response.status_code == 200:
                            st.success("Movie deleted successfully!")
                            st.rerun()
                        else:
                            st.error("Unable to delete movie.")

            # Edit mode
            else:

                title = st.text_input(
                    "Title",
                    value=movie["title"],
                    key=f"title_{movie_id}",
                )

                director = st.text_input(
                    "Director",
                    value=movie["director"],
                    key=f"director_{movie_id}",
                )

                genre = st.text_input(
                    "Genre",
                    value=movie["genre"],
                    key=f"genre_{movie_id}",
                )

                release_year = st.number_input(
                    "Release Year",
                    min_value=1888,
                    max_value=2100,
                    value=movie["release_year"],
                    key=f"year_{movie_id}",
                )

                rating = st.slider(
                    "Rating",
                    min_value=0.0,
                    max_value=10.0,
                    value=float(movie["rating"]),
                    step=0.1,
                    key=f"rating_{movie_id}",
                )

                watched = st.checkbox(
                    "Watched",
                    value=movie["watched"],
                    key=f"watched_{movie_id}",
                )


                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "💾 Save",
                        key=f"save_{movie_id}",
                    ):

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

                        if update_response.status_code == 200:

                            st.session_state[f"editing_{movie_id}"] = False
                            st.success("Movie updated!")
                            st.rerun()

                        else:
                            st.error("Unable to update movie.")


                with col2:

                    if st.button(
                        "❌ Cancel",
                        key=f"cancel_{movie_id}",
                    ):

                        st.session_state[f"editing_{movie_id}"] = False
                        st.rerun()