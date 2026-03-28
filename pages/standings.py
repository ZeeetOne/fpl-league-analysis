"""League Standings page."""

import streamlit as st

from data_loader import (
    get_league_context,
    load_manager_histories,
    load_manager_picks,
    load_manager_transfers,
    show_error,
)
from features.standings import render_standings
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("League Standings", eyebrow="League", subtitle="Full rankings with points, chips, transfers and captain stats")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    current_gw = context["current_gw"]

    histories = load_manager_histories(entry_ids)
    transfers = load_manager_transfers(entry_ids)
    picks = load_manager_picks(entry_ids, current_gw)

    render_standings(context, histories, transfers, picks)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
