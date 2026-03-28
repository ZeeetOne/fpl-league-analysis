"""Transfer Analysis page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories, load_manager_transfers, show_error
from features.transfers import (
    render_league_transfer_summary,
    render_transfer_activity_by_gw,
    render_transfers_by_manager,
    render_most_transferred_players,
)
from features.ui import page_header, section_header
from fpl_api import GameUpdatingError

page_header("Transfer Analysis", eyebrow="League", subtitle="Transfer activity and patterns across the mini-league")

try:
    context = get_league_context()
    entry_ids = context["entry_ids"]

    histories = load_manager_histories(entry_ids)
    transfers = load_manager_transfers(entry_ids)

    render_league_transfer_summary(context, histories, transfers)

    section_header("Activity by Gameweek", "Transfer volume across the season")
    render_transfer_activity_by_gw(context, histories, transfers)

    section_header("Transfers by Manager", "Individual manager transfer records")
    render_transfers_by_manager(context, histories, transfers)

    section_header("Most Transferred Players", "Popular ins and outs in the league")
    render_most_transferred_players(context, transfers)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
