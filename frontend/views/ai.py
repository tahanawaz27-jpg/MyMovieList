# frontend/views/ai.py
import streamlit as st


def ai_page(api):
    st.header("🤖 AI Movie Recommendations")
    st.write("Enter a movie you love, and get 3 tailored recommendations!")

    # ---------------- SEARCH INPUT & BUTTONS ---------------- #
    col_input, col_btn1, col_btn2 = st.columns([3, 1.2, 1.2])

    with col_input:
        movie_title = st.text_input(
            "Enter a movie title",
            placeholder="e.g. Inception, The Godfather, Interstellar...",
            label_visibility="collapsed",
        )

    with col_btn1:
        get_recs = st.button("✨ Recommend", use_container_width=True)

    with col_btn2:
        refresh_recs = st.button("🔄 Refresh", use_container_width=True)

    # Re-fetch when user clicks Recommend or Refresh
    should_fetch = (get_recs or refresh_recs) and movie_title.strip()

    if should_fetch:
        with st.spinner("Finding great recommendations for you..."):
            response = api.recommend_movie(movie_title.strip())

            if response and response.status_code == 200:
                data = response.json()
                recs = data.get("recommendations", [])
                st.session_state["recommendations"] = recs
                st.session_state["searched_title"] = movie_title.strip()
            else:
                st.error("Unable to generate recommendations. Please try again.")

    # ---------------- DISPLAY RECOMMENDATIONS ---------------- #
    if "recommendations" in st.session_state and st.session_state["recommendations"]:
        searched = st.session_state.get("searched_title", movie_title)
        st.subheader(f"3 Movies similar to *{searched}*:")

        recs = st.session_state["recommendations"]

        # 3-Column Responsive Card Grid
        cols = st.columns(len(recs))

        for idx, (col, rec) in enumerate(zip(cols, recs), start=1):
            with col:
                with st.container(border=True):
                    st.markdown(f"### #{idx} {rec.get('title', 'Unknown Title')}")
                    
                    genre = rec.get("genre", "N/A")
                    st.caption(f"🏷️ **Genre:** {genre}")

                    st.markdown("---")
                    st.write(rec.get("reason", "No detailed explanation available."))