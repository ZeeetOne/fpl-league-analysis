"""Player Ownership Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_picks, show_error
from features.ownership import render_player_ownership
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("Player Ownership", eyebrow="League", subtitle="Players owned by managers in the league")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    current_gw = context["current_gw"]

    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
    )

    picks_data = load_manager_picks(entry_ids, selected_gw)
    render_player_ownership(context, picks_data, selected_gw)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
