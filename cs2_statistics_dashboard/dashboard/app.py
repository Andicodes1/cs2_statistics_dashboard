import streamlit as st

# Hide sidebar
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.switch_page("pages/login.py")
elif st.session_state.user["role"] == "admin":
    st.switch_page("pages/admin.py")
else:
    st.switch_page("pages/student.py")
