import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime
import numpy as np

st.set_page_config(
    page_title="Secure Dashboard",
    layout="wide"
)

# Simple hash function for passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# User database (in production, use a real database)
USERS = {
    "admin": {
        "password": hash_password("admin123"),
        "role": "admin",
        "name": "Administrator"
    },
    "user": {
        "password": hash_password("user123"),
        "role": "user",
        "name": "Regular User"
    },
    "viewer": {
        "password": hash_password("viewer123"),
        "role": "viewer",
        "name": "View Only User"
    }
}

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "username" not in st.session_state:
    st.session_state.username = None
if "role" not in st.session_state:
    st.session_state.role = None

# Login function
def login(username, password):
    if username in USERS:
        if USERS[username]["password"] == hash_password(password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = USERS[username]["role"]
            st.session_state.name = USERS[username]["name"]
            return True
    return False

# Logout function
def logout():
    st.session_state.authenticated = False
    st.session_state.username = None
    st.session_state.role = None
    st.session_state.name = None

# Login page
if not st.session_state.authenticated:
    st.title("Login")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.form("login_form"):
            st.markdown("### Enter your credentials")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.form_submit_button("Login", type="primary", use_container_width=True):
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        # Demo credentials
        with st.expander("Demo Credentials"):
            st.markdown("""
            **Admin User:**
            - Username: admin
            - Password: admin123

            **Regular User:**
            - Username: user
            - Password: user123

            **Viewer:**
            - Username: viewer
            - Password: viewer123
            """)

else:
    # Main dashboard (only visible after login)
    st.title("Secure Dashboard")

    # User info and logout
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        st.markdown(f"**Welcome, {st.session_state.name}!**")
    with col2:
        st.markdown(f"**Role:** {st.session_state.role.title()}")
    with col3:
        if st.button("Logout", type="secondary"):
            logout()
            st.rerun()

    st.markdown("---")

    # Role-based content
    if st.session_state.role == "admin":
        st.subheader("Admin Dashboard")

        # Admin metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Users", "1,234")
        with col2:
            st.metric("Active Sessions", "42")
        with col3:
            st.metric("Revenue", "$125,430")
        with col4:
            st.metric("System Health", "98%")

        # Sample chart
        chart_data = pd.DataFrame(
            np.random.randn(20, 3),
            columns=["Sales", "Revenue", "Growth"]
        )
        st.line_chart(chart_data)

    elif st.session_state.role == "user":
        st.subheader("User Dashboard")

        # Limited functionality for regular users
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Your Tasks", "12")
            st.metric("Completed", "8")

        with col2:
            st.metric("Pending", "4")
            st.metric("Performance", "85%")

    else:  # viewer role
        st.subheader("Viewer Dashboard")
        st.info("You have read-only access. Contact an administrator for additional permissions.")

        # Read-only view
        st.markdown("### Public Reports")
        st.metric("Total Reports", "25")