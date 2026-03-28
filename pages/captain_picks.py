"""Captain Picks Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories, show_error
from features.captain import render_captain_picks
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("Captain Picks", eyebrow="League", subtitle="Who the league captained and how it paid off")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    histories = load_manager_histories(entry_ids)

    render_captain_picks(context, histories)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
