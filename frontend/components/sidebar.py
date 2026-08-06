


import streamlit as st

def sidebar():
    with st.sidebar:
        page = st.radio(
            "Navigation",
            [
                "Dashboard",
                "Add Movie",
                "AI Recommendation",
            ]
        )

        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()

    return page