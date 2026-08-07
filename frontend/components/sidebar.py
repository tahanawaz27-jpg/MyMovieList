# frontend/components/sidebar.py
import streamlit as st


def sidebar():
    # ---------------- CUSTOM SIDEBAR STYLING ---------------- #
    st.markdown(
        """
        <style>
            /* Sidebar container padding & background */
            [data-testid="stSidebar"] {
                padding-top: 1.5rem;
            }

            /* Sidebar Title / Header */
            .sidebar-header {
                font-size: 1.25rem;
                font-weight: 800;
                color: #ffffff;
                margin-bottom: 0.2rem;
                letter-spacing: -0.3px;
            }

            .sidebar-tagline {
                color: rgba(255, 255, 255, 0.5);
                font-size: 0.8rem;
                margin-bottom: 1.2rem;
            }

            /* Active User Status Badge */
            .user-status-badge {
                background: rgba(76, 175, 80, 0.12);
                border: 1px solid rgba(76, 175, 80, 0.3);
                color: #4caf50;
                border-radius: 20px;
                padding: 4px 12px;
                font-size: 0.78rem;
                font-weight: 600;
                display: inline-flex;
                align-items: center;
                gap: 6px;
                margin-bottom: 1.5rem;
            }

            /* Turn radio options into clickable styled menu buttons */
            [data-testid="stSidebar"] div[role="radiogroup"] {
                gap: 8px;
            }

            [data-testid="stSidebar"] div[role="radiogroup"] label {
                background-color: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.07);
                border-radius: 10px;
                padding: 10px 14px;
                color: rgba(255, 255, 255, 0.85);
                font-weight: 500;
                transition: all 0.2s ease-in-out;
                cursor: pointer;
            }

            /* Hover state for navigation links */
            [data-testid="stSidebar"] div[role="radiogroup"] label:hover {
                background-color: rgba(255, 75, 75, 0.12);
                border-color: rgba(255, 75, 75, 0.4);
                color: #ffffff;
                transform: translateX(2px);
            }

            /* Logout Button Styling */
            [data-testid="stSidebar"] .stButton > button {
                border-color: rgba(255, 255, 255, 0.15);
                background-color: transparent;
                color: rgba(255, 255, 255, 0.75);
                margin-top: 1rem;
            }

            [data-testid="stSidebar"] .stButton > button:hover {
                border-color: #ff4b4b;
                color: #ff4b4b;
                background-color: rgba(255, 75, 75, 0.08);
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.markdown('<div class="sidebar-header">📍 Menu</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-tagline">Navigate your collection</div>', unsafe_allow_html=True)

        if st.session_state.get("token"):
            st.markdown(
                '<div class="user-status-badge">🟢 Connected</div>',
                unsafe_allow_html=True,
            )

        # Main navigation choices matching your routing in app.py
        selected_page = st.radio(
            "Navigation Menu",
            options=["Dashboard", "Add Movie", "AI Recommendation"],
            label_visibility="collapsed",
        )

        st.divider()

        # Logout Action
        if st.session_state.get("token"):
            if st.button("🚪 Log Out", use_container_width=True):
                st.session_state.clear()
                if "token" in st.query_params:
                    del st.query_params["token"]
                st.rerun()

        return selected_page