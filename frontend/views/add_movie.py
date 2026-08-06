import streamlit as st


def add_movie_page(api):

    st.header("➕ Add Movie")

    title = st.text_input("Title")

    director = st.text_input("Director")

    genre = st.text_input("Genre")

    year = st.number_input(
        "Release Year",
        min_value=1888,
        max_value=2100,
        value=2025,
    )

    rating = st.slider(
        "Rating",
        0.0,
        10.0,
        5.0,
        0.1,
    )

    watched = st.checkbox("Watched")

    if st.button("Add Movie"):

        response = api.create_movie(
            {
                "title": title,
                "director": director,
                "genre": genre,
                "release_year": year,
                "rating": rating,
                "watched": watched,
            }
        )
        if response.status_code == 201:
             st.success("✅ Movie created successfully!")
      

        else:

            st.error(response.text)