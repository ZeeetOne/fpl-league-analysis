"""Head-to-Head Comparison page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories, show_error
from features.head_to_head import (
    render_team_comparison,
    render_season_trajectory,
    render_gameweek_breakdown,
)
from features.ui import page_header, section_header
from fpl_api import GameUpdatingError

page_header("Head-to-Head", eyebrow="League", subtitle="Compare any two managers across the season")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    histories = load_manager_histories(entry_ids)

    team1_name, team2_name, history1, history2 = render_team_comparison(context, histories)

    if team1_name and team2_name and history1 and history2:
        section_header("Season Trajectory", "Cumulative points over the season")
        render_season_trajectory(team1_name, team2_name, history1, history2)

        section_header("Gameweek Breakdown", "Points scored each gameweek")
        render_gameweek_breakdown(team1_name, team2_name, history1, history2)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
