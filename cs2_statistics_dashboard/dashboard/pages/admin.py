import streamlit as st
import requests
import pandas as pd

API = "http://localhost:8000"

# =========================================================
# AUTH GUARD (ADMIN ONLY)
# =========================================================
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

if st.session_state.user["role"] != "admin":
    st.switch_page("pages/student.py")

# =========================================================
# PAGE CONFIG (KEEP SIDEBAR FOR ADMIN)
# =========================================================
st.set_page_config(
    page_title="Admin Panel",
    page_icon="🛠",
    layout="wide"
)

# =========================================================
# SIDEBAR – ADMIN TOOLS
# =========================================================
st.sidebar.title("🛠 Admin Tools")

action = st.sidebar.radio(
    "Choose Action",
    ["View Teams", "Add Team", "Update Team", "Delete Team"]
)

st.sidebar.markdown("---")
if st.sidebar.button("Go to Dashboard"):
    st.switch_page("pages/student.py")

if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")

# =========================================================
# LOAD TEAMS
# =========================================================
teams = requests.get(f"{API}/teams").json()
teams_df = pd.DataFrame(teams)

# =========================================================
# MAIN CONTENT
# =========================================================
st.title("🛠 Admin – Team Management")
st.markdown("---")

# -------------------------
# VIEW TEAMS (READ)
# -------------------------
if action == "View Teams":
    st.subheader("All Teams")

    if teams_df.empty:
        st.info("No teams found.")
    else:
        cols = st.columns(6)
        for i, row in teams_df.iterrows():
            col = cols[i % 6]
            col.image(row["logo"], width=70)
            col.caption(row["name"])

        st.markdown("### Teams Table")
        st.dataframe(teams_df, use_container_width=True)

# -------------------------
# ADD TEAM (CREATE)
# -------------------------
elif action == "Add Team":
    st.subheader("Add New Team")

    name = st.text_input("Team Name")
    logo = st.text_input("Team Logo URL (HLTV)")

    if st.button("Add Team"):
        if name and logo:
            requests.post(
                f"{API}/teams",
                params={"name": name.upper(), "logo_url": logo}
            )
            st.success("Team added successfully.")
            st.rerun()
        else:
            st.error("Please fill in all fields.")

# -------------------------
# UPDATE TEAM (UPDATE)
# -------------------------
elif action == "Update Team":
    st.subheader("Update Team Logo")

    if teams_df.empty:
        st.info("No teams available.")
    else:
        team_to_update = st.selectbox(
            "Select Team",
            teams_df["name"].tolist()
        )

        new_logo = st.text_input("New Logo URL")

        if st.button("Update Team"):
            if new_logo:
                # Delete then re-add (simple & explainable)
                requests.delete(
                    f"{API}/teams",
                    params={"name": team_to_update}
                )
                requests.post(
                    f"{API}/teams",
                    params={"name": team_to_update, "logo_url": new_logo}
                )
                st.success("Team updated successfully.")
                st.rerun()
            else:
                st.error("Please provide a new logo URL.")

# -------------------------
# DELETE TEAM (DELETE)
# -------------------------
elif action == "Delete Team":
    st.subheader("Delete Team")

    if teams_df.empty:
        st.info("No teams available.")
    else:
        team_to_delete = st.selectbox(
            "Select Team to Delete",
            teams_df["name"].tolist()
        )

        if st.button("Delete Team"):
            requests.delete(
                f"{API}/teams",
                params={"name": team_to_delete}
            )
            st.success("Team deleted successfully.")
            st.rerun()
