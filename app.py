"""FPL League Analysis Dashboard."""

import streamlit as st

from config import APP_ICON, APP_TITLE

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

# Define pages
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/home:", default=True)
standings_page = st.Page("pages/standings.py", title="Standings", icon=":material/leaderboard:")
league_insights_page = st.Page("pages/league_insights.py", title="League Insights", icon=":material/insights:")
head_to_head_page = st.Page("pages/head_to_head.py", title="Head-to-Head", icon=":material/compare:")
point_sources_page = st.Page("pages/point_sources.py", title="Point Sources", icon=":material/pie_chart:")
transfer_analysis_page = st.Page("pages/transfer_analysis.py", title="Transfer Analysis", icon=":material/swap_horiz:")
captain_picks_page = st.Page("pages/captain_picks.py", title="Captain Picks", icon=":material/star:")
player_ownership_page = st.Page("pages/player_ownership.py", title="Player Ownership", icon=":material/group:")
best_squad_page = st.Page("pages/best_squad.py", title="Best Squad", icon=":material/trophy:")

# Group pages with st.navigation
pg = st.navigation({
    "": [dashboard],
    "League Overview": [standings_page, league_insights_page],
    "Managers": [head_to_head_page, point_sources_page],
    "Analysis": [transfer_analysis_page, captain_picks_page, player_ownership_page],
    "Global": [best_squad_page],
    "About": [],
})

pg.run()
