"""Captain Picks Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories
from features.captain import render_captain_picks
from fpl_api import GameUpdatingError

st.header("Captain Picks Analysis")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]
    histories = load_manager_histories(entry_ids)

    render_captain_picks(context, histories)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
