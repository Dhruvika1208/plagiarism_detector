# plagiarism_detector/backend/auth.py
import streamlit as st

# Hardcoded credentials (You can replace it with a database later)
user_credentials = {
    "student": {"username": "student", "password": "student123"},
    "teacher": {"username": "teacher", "password": "teacher123"},
}

def login():
    """Login page to authenticate users."""
    st.sidebar.title("Login")
    role = st.sidebar.selectbox("Login as:", ["Student", "Teacher"])
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login"):
        if (
            username == user_credentials[role]["username"]
            and password == user_credentials[role]["password"]
        ):
            st.session_state["authenticated"] = True
            st.session_state["role"] = role
            st.sidebar.success(f"Logged in as {role}!")
        else:
            st.sidebar.error("Invalid credentials!")

def logout():
    """Logout and clear session data."""
    st.session_state["authenticated"] = False
    st.session_state["role"] = None
    st.sidebar.success("Logged out successfully!")
