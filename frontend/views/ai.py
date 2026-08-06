import streamlit as st


def ai_page(api):

    st.header("🤖 AI Recommendation")

    title = st.text_input(
        "Enter a movie title"
    )

    if st.button("Recommend"):

        response = api.recommend_movie(title)

        if response.status_code == 200:

            st.success(
                response.json()["recommendation"]
            )

        else:

            st.error(
                "Unable to generate recommendation."
            )