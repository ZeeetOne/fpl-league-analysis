"""FPL League Analysis Dashboard."""

import streamlit as st

from config import APP_ICON, APP_TITLE, DEFAULT_LEAGUE_ID
from features.ui import inject_css, sidebar_brand

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

inject_css()

# Initialize session state defaults
if "league_id" not in st.session_state:
    st.session_state.league_id = DEFAULT_LEAGUE_ID

_DISPLAY_OPTIONS = ["Top 10", "Top 20", "All", "Custom"]

# Sidebar settings (rendered on every page)
with st.sidebar:
    sidebar_brand()
    st.subheader("Settings")

    league_input = st.text_input(
        "League ID",
        value=str(st.session_state.league_id) if st.session_state.league_id else "",
        placeholder="Enter league ID...",
        key="league_id_input",
    )
    if st.button("Analyze", use_container_width=True, type="primary"):
        try:
            parsed_id = int(league_input)
        except (ValueError, TypeError):
            parsed_id = None
        if parsed_id and 1 <= parsed_id <= 99_999_999:
            st.session_state.league_id = parsed_id
        elif parsed_id is not None:
            st.error("Please enter a valid league ID (1 – 99,999,999).")

    st.divider()

    display_option = st.radio(
        "Show managers",
        _DISPLAY_OPTIONS,
        key="manager_display",
    )

    if display_option == "Custom":
        st.number_input("From rank", min_value=1, value=1, step=1, key="custom_start")
        st.number_input("To rank", min_value=1, value=20, step=1, key="custom_end")

# Define pages — League
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon=":material/home:", default=True)
standings_page = st.Page("pages/standings.py", title="Standings", icon=":material/leaderboard:")
league_insights_page = st.Page("pages/league_insights.py", title="League Insights", icon=":material/insights:")
head_to_head_page = st.Page("pages/head_to_head.py", title="Head-to-Head", icon=":material/compare:")
point_sources_page = st.Page("pages/point_sources.py", title="Point Sources", icon=":material/pie_chart:")
transfer_analysis_page = st.Page("pages/transfer_analysis.py", title="Transfer Analysis", icon=":material/swap_horiz:")
captain_picks_page = st.Page("pages/captain_picks.py", title="Captain Picks", icon=":material/star:")
player_ownership_page = st.Page("pages/player_ownership.py", title="Player Ownership", icon=":material/group:")

# Define pages — Global
season_stats_page = st.Page("pages/season_stats.py", title="Season Stats", icon=":material/bar_chart:")
player_rankings_page = st.Page("pages/player_rankings.py", title="Player Rankings", icon=":material/format_list_numbered:")
global_transfers_page = st.Page("pages/global_transfers.py", title="Global Transfers", icon=":material/trending_up:")
global_ownership_page = st.Page("pages/global_ownership.py", title="Global Ownership", icon=":material/public:")
best_squad_page = st.Page("pages/best_squad.py", title="Best Squad", icon=":material/trophy:")

# Define pages — Help
feedback_page = st.Page("pages/feedback.py", title="Feedback", icon=":material/rate_review:")

# Group pages with st.navigation
pg = st.navigation({
    "": [dashboard],
    "League": [
        standings_page,
        league_insights_page,
        head_to_head_page,
        point_sources_page,
        transfer_analysis_page,
        captain_picks_page,
        player_ownership_page,
    ],
    "Global": [
        season_stats_page,
        player_rankings_page,
        global_transfers_page,
        global_ownership_page,
        best_squad_page,
    ],
    "Help": [feedback_page],
})

pg.run()
