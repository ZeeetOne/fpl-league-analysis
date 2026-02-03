"""Head-to-Head Comparison page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories
from features.head_to_head import (
    render_team_comparison,
    render_season_trajectory,
    render_gameweek_breakdown,
)
from fpl_api import GameUpdatingError

st.header("Head-to-Head Comparison")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]

    histories = load_manager_histories(entry_ids)

    # Team comparison returns the selected teams for use in other sections
    team1_name, team2_name, history1, history2 = render_team_comparison(context, histories)

    # Only render other sections if teams were successfully loaded
    if team1_name and team2_name and history1 and history2:
        st.divider()

        render_season_trajectory(team1_name, team2_name, history1, history2)

        st.divider()

        render_gameweek_breakdown(team1_name, team2_name, history1, history2)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
