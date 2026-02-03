"""Transfer Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories, load_manager_transfers
from features.transfers import (
    render_league_transfer_summary,
    render_transfer_activity_by_gw,
    render_transfers_by_manager,
    render_most_transferred_players,
)
from fpl_api import GameUpdatingError

st.header("Transfer Analysis")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]

    histories = load_manager_histories(entry_ids)
    transfers = load_manager_transfers(entry_ids)

    render_league_transfer_summary(context, histories, transfers)

    st.divider()

    render_transfer_activity_by_gw(context, histories, transfers)

    st.divider()

    render_transfers_by_manager(context, histories, transfers)

    st.divider()

    render_most_transferred_players(context, transfers)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
