import streamlit as st
import requests

API = "http://localhost:8000"

# -------------------------------------------------
# PAGE CONFIG + HIDE SIDEBAR
# -------------------------------------------------
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
st.title("🔐 Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    response = requests.post(
        f"{API}/login",
        params={"username": username, "password": password}
    ).json()

    if "role" in response:
        # Save user in session
        st.session_state.user = response

        # ✅ FIX: ROLE-BASED REDIRECT
        if response["role"] == "admin":
            st.switch_page("pages/admin.py")
        else:
            st.switch_page("pages/student.py")
    else:
        st.error("Invalid username or password")

# -------------------------------------------------
# REGISTER LINK
# -------------------------------------------------
st.page_link("pages/register.py", label="Register")
