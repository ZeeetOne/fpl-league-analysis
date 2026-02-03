"""Player Ownership Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_picks
from features.ownership import render_player_ownership
from fpl_api import GameUpdatingError

st.header("Player Ownership")
st.caption("*Players owned by managers in the league*")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    current_gw = context["current_gw"]

    # Gameweek selector
    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
    )

    # Load picks for all managers
    picks_data = load_manager_picks(entry_ids, selected_gw)

    render_player_ownership(context, picks_data, selected_gw)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
