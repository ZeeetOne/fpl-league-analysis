"""League Insights page - Points analysis and trends."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories
from features.league_insights import (
    render_points_per_gameweek,
    render_rank_movement,
)
from features.ui import page_header, section_header
from fpl_api import GameUpdatingError

page_header("League Insights", eyebrow="League", subtitle="Points trends and rank movement over recent gameweeks")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    histories = load_manager_histories(entry_ids)

    section_header("Points per Gameweek", "Weekly performance (dashed line = league average)")
    render_points_per_gameweek(context, histories)

    section_header("Rank Movement", "How league positions have changed over recent gameweeks")
    render_rank_movement(context, histories)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
