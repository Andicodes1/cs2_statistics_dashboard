import streamlit as st
import requests

API = "http://localhost:8000"

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>[data-testid="stSidebar"]{display:none;}</style>
""", unsafe_allow_html=True)

st.title("📝 Register")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Register"):
    requests.post(
        f"{API}/register",
        params={"username": username, "password": password}
    )
    st.success("Account created successfully")
    st.switch_page("pages/login.py")
