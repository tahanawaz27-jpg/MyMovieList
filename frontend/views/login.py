import streamlit as st


def login_page(api):

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Register",
        ]
    )

    # ---------------- LOGIN ---------------- #

    with tab1:

        st.subheader("Login")

        username = st.text_input(
            "Email or Username",
            key="login_username",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password",
        )

        if st.button("Login"):

            response = api.login(
                username,
                password,
            )

            if response.status_code == 200:

                token = response.json()["access_token"]

                st.session_state.token = token

                st.success(
                    "Logged in successfully!"
                )

                st.rerun()

            else:

                try:
                    st.error(
                        response.json()["detail"]
                    )
                except Exception:
                    st.error("Login failed.")

    # ---------------- REGISTER ---------------- #

    with tab2:

        st.subheader("Register")

        username = st.text_input(
            "Username",
            key="register_username",
        )

        email = st.text_input(
            "Email",
            key="register_email",
        )

        password = st.text_input(
            "Password",
            type="password",
            key="register_password",
        )

        if st.button("Register"):

            response = api.register(
                {
                    "username": username,
                    "email": email,
                    "password": password,
                }
            )

            if response.status_code == 201:

                st.success(
                    "Registration successful!"
                )

            else:

                try:
                    st.error(
                        response.json()["detail"]
                    )
                except Exception:
                    st.error("Registration failed.")