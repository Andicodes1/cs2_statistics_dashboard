import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API = "http://localhost:8000"

# =========================================================
# AUTH GUARD
# =========================================================
if "user" not in st.session_state or st.session_state.user is None:
    st.switch_page("pages/login.py")

# =========================================================
# PAGE CONFIG + HIDE SIDEBAR
# =========================================================
st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.markdown("""
<style>
[data-testid="stSidebar"] { display: none; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA FROM API
# =========================================================
teams = requests.get(f"{API}/teams").json()
matches = requests.get(f"{API}/matches").json()

TEAM_LOGOS = {t["name"]: t["logo"] for t in teams}

df = pd.DataFrame(
    matches,
    columns=["id", "date", "team", "opponent", "map", "result", "event"]
)

df = df.drop(columns=["id"])

# =========================================================
# DATA CLEANING
# =========================================================
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["team"] = df["team"].astype(str).str.upper().str.strip()
df["result"] = df["result"].astype(str).str.strip().str.upper()

# =========================================================
# DERIVE WIN / LOSS (ROBUST FIX)
# =========================================================

# Case 1: result like "16-12"
if df["result"].str.contains("-", na=False).any():
    scores = df["result"].str.split("-", expand=True)
    df["team_score"] = pd.to_numeric(scores[0], errors="coerce")
    df["opponent_score"] = pd.to_numeric(scores[1], errors="coerce")

    df["result"] = df.apply(
        lambda r: "Win" if r["team_score"] > r["opponent_score"] else "Loss",
        axis=1
    )

# Case 2: numeric result (1 / 0 / -1)
elif df["result"].str.isnumeric().any():
    df["result"] = df["result"].astype(int).apply(
        lambda x: "Win" if x > 0 else "Loss"
    )

# Case 3: text normalization
else:
    df["result"] = df["result"].replace({
        "W": "Win",
        "L": "Loss",
        "WIN": "Win",
        "LOSS": "Loss"
    })

# =========================================================
# TEAM COLORS
# =========================================================
TEAM_COLORS = {
    "NAVI": "#FFD700",
    "G2": "#000000",
    "FAZE": "#E10600",
    "VITALITY": "#FFD200",
    "SPIRIT": "#00BFFF",
    "HEROIC": "#C8102E",
    "ENCE": "#1E90FF",
    "MOUZ": "#D50000",
    "ASTRALIS": "#C8102E",
    "FURIA": "#000000",
    "CLOUD9": "#00AEEF",
    "OG": "#000000",
    "BIG": "#D50000",
    "FNATIC": "#FF6A00",
    "APEKS": "#1E90FF",
    "MOVISTAR RIDERS": "#0057B8",
    "9INE": "#00FFAA",
    "COMPLEXITY": "#000000",
    "SAW": "#00A859",
    "BAD NEWS EAGLES": "#D50000",
}

# =========================================================
# HEADER
# =========================================================
st.title("🎮 CS2 Statistics Dashboard")
st.markdown("---")

# =========================================================
# FILTERS
# =========================================================
c1, c2, c3 = st.columns(3)

with c1:
    team_filter = st.selectbox(
        "Team",
        ["All"] + sorted(df["team"].unique())
    )

with c2:
    map_filter = st.selectbox(
        "Map",
        ["All"] + sorted(df["map"].unique())
    )

with c3:
    event_filter = st.selectbox(
        "Event",
        ["All"] + sorted(df["event"].unique())
    )

filtered_df = df.copy()

if team_filter != "All":
    filtered_df = filtered_df[filtered_df["team"] == team_filter]

if map_filter != "All":
    filtered_df = filtered_df[filtered_df["map"] == map_filter]

if event_filter != "All":
    filtered_df = filtered_df[filtered_df["event"] == event_filter]

# =========================================================
# TEAM LOGOS
# =========================================================
st.markdown("---")
st.subheader("Teams")

if team_filter == "All":
    cols = st.columns(6)
    for i, team in enumerate(TEAM_LOGOS):
        col = cols[i % 6]
        col.image(TEAM_LOGOS[team], width=70)
        col.caption(team)
else:
    if team_filter in TEAM_LOGOS:
        st.image(TEAM_LOGOS[team_filter], width=140)
        st.caption(team_filter)

# =========================================================
# METRICS (NOW WORKING)
# =========================================================
total_matches = len(filtered_df)
wins = len(filtered_df[filtered_df["result"] == "Win"])
losses = len(filtered_df[filtered_df["result"] == "Loss"])
win_rate = round((wins / total_matches) * 100, 1) if total_matches > 0 else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Matches", total_matches)
m2.metric("Wins", wins)
m3.metric("Losses", losses)
m4.metric("Win Rate", f"{win_rate}%")

# =========================================================
# MAP WIN PERCENTAGE
# =========================================================
st.markdown("---")
st.subheader("Map Win Percentage")

map_stats = (
    filtered_df.groupby("map")["result"]
    .value_counts(normalize=True)
    .rename("percentage")
    .reset_index()
)

map_stats = map_stats[map_stats["result"] == "Win"]
map_stats["percentage"] = (map_stats["percentage"] * 100).round(1)

color = TEAM_COLORS.get(team_filter, "#1f77b4")

fig_map = px.bar(
    map_stats,
    x="map",
    y="percentage",
    title="Win Percentage per Map",
    labels={"percentage": "Win %"}
)

fig_map.update_traces(
    marker_color=color,
    text=map_stats["percentage"].astype(str) + "%",
    textposition="outside",
    width=0.45
)

fig_map.update_layout(
    yaxis_range=[0, 100],
    bargap=0.6
)

st.plotly_chart(fig_map, use_container_width=True)

# =========================================================
# TEAM WINS
# =========================================================
st.markdown("---")
st.subheader("Team Wins")

team_wins = (
    filtered_df[filtered_df["result"] == "Win"]
    .groupby("team")
    .size()
    .reset_index(name="wins")
    .sort_values("wins", ascending=False)
)

fig_team = px.bar(
    team_wins,
    x="team",
    y="wins",
    title="Total Wins per Team",
    color="team",
    color_discrete_map=TEAM_COLORS
)

fig_team.update_traces(
    text=team_wins["wins"],
    textposition="outside",
    width=0.45
)

st.plotly_chart(fig_team, use_container_width=True)

# =========================================================
# MATCH TABLE
# =========================================================
st.markdown("---")
st.subheader("Match History")

st.dataframe(
    filtered_df.sort_values("date", ascending=False),
    use_container_width=True,
    hide_index=True
)

# =========================================================
# LOGOUT
# =========================================================
st.markdown("---")
if st.button("Logout"):
    st.session_state.user = None
    st.switch_page("pages/login.py")
