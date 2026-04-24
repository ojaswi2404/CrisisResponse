import streamlit as st


ADMIN_CREDENTIALS = {"username": "admin", "password": "admin123"}

STAFF_CREDENTIALS = {
    "fire1": {"password": "fire123", "group": "fire", "label": "Fire Staff"},
    "med1": {"password": "med123", "group": "medical", "label": "Medical Staff"},
    "security1": {"password": "security123", "group": "security", "label": "Security Staff"},
    "other1": {"password": "other123", "group": "other", "label": "Other Staff"},
}


def login_admin(username: str, password: str) -> bool:
    success = username == ADMIN_CREDENTIALS["username"] and password == ADMIN_CREDENTIALS["password"]
    st.session_state.admin_logged_in = success
    return success


def logout_admin() -> None:
    st.session_state.admin_logged_in = False


def login_staff(username: str, password: str):
    user = STAFF_CREDENTIALS.get(username)
    if user and user["password"] == password:
        st.session_state.staff_logged_in = True
        st.session_state.staff_user = {"username": username, **user}
        return st.session_state.staff_user
    st.session_state.staff_logged_in = False
    st.session_state.staff_user = None
    return None


def logout_staff() -> None:
    st.session_state.staff_logged_in = False
    st.session_state.staff_user = None
