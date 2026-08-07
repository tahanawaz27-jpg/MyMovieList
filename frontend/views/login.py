import streamlit as st


def login_page(api):
    tab1, tab2 = st.tabs(["Login", "Register"])

    # ---------------- LOGIN ---------------- #
    with tab1:
        st.subheader("Login")

        with st.form("login_form"):
            username = st.text_input("Email or Username", key="login_username")
            password = st.text_input("Password", type="password", key="login_password")
            login_submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

        if login_submitted:
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                response = api.login(username, password)

                if response is not None:
                    if response.status_code == 200:
                        token = response.json().get("access_token")

                        if token:
                            # Save in session state & API handler
                            st.session_state.token = token
                            api.set_token(token)

                            # Persist token in URL parameters to prevent logout on browser refresh
                            st.query_params["token"] = token

                            st.success("Logged in successfully!")
                            st.rerun()
                        else:
                            st.error("Token not received from server.")
                    else:
                        try:
                            detail = response.json().get("detail", "Login failed.")
                            if isinstance(detail, list):
                                detail = ", ".join([err.get("msg", "") for err in detail])
                            st.error(detail)
                        except Exception:
                            st.error("Login failed.")

    # ---------------- REGISTER ---------------- #
    with tab2:
        st.subheader("Register")

        with st.form("register_form"):
            username = st.text_input("Username", key="register_username")
            email = st.text_input("Email", key="register_email")
            password = st.text_input("Password", type="password", key="register_password")
            register_submitted = st.form_submit_button("Register", type="primary", use_container_width=True)

        if register_submitted:
            if not username or not email or not password:
                st.warning("Please fill in all registration fields.")
            else:
                response = api.register(
                    {
                        "username": username,
                        "email": email,
                        "password": password,
                    }
                )

                if response is not None:
                    if response.status_code == 201:
                        st.success("Registration successful! Please log in.")
                    else:
                        try:
                            detail = response.json().get("detail", "Registration failed.")
                            if isinstance(detail, list):
                                detail = ", ".join([err.get("msg", "") for err in detail])
                            st.error(detail)
                        except Exception:
                            st.error("Registration failed.")