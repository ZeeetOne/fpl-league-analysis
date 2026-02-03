"""League Standings page."""

import streamlit as st

from data_loader import (
    get_league_context,
    load_manager_histories,
    load_manager_picks,
    load_manager_transfers,
)
from features.standings import render_standings
from fpl_api import GameUpdatingError

st.header("League Standings")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    current_gw = context["current_gw"]

    # Load additional data for full standings
    histories = load_manager_histories(entry_ids)
    transfers = load_manager_transfers(entry_ids)
    picks = load_manager_picks(entry_ids, current_gw)

    render_standings(context, histories, transfers, picks)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
