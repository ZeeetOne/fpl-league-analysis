"""League Insights page - Points analysis and trends."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories
from features.league_insights import (
    render_points_per_gameweek,
    render_rank_movement,
)
from fpl_api import GameUpdatingError

st.header("League Insights")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    histories = load_manager_histories(entry_ids)

    st.subheader("Points per Gameweek")
    st.caption("*Weekly performance across all managers (dashed line = league average)*")
    render_points_per_gameweek(context, histories)

    st.divider()

    st.subheader("Rank Movement")
    st.caption("*How positions have changed over recent gameweeks*")
    render_rank_movement(context, histories)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
