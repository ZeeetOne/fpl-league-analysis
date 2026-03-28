"""Dashboard home page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories, show_error
from features.dashboard import render_gw_highlights, render_league_summary, render_standings, BASIC_COLUMNS
from features.ui import page_header, section_header
from fpl_api import GameUpdatingError

page_header(
    "FPL League Analysis",
    eyebrow="Dashboard",
)

try:
    with st.spinner("Loading FPL data..."):
        context = get_league_context()
        histories = load_manager_histories(context["entry_ids"])

    league_info = context["league_info"]

    st.caption(f"League: **{league_info.get('name', 'Unknown')}**")

    section_header("League Summary", "Overview of league status")
    render_league_summary(context)

    section_header("This GW Highlights", "Notable changes and standout performances")
    render_gw_highlights(context)

    section_header("League Standings", "Current rankings and point totals")
    render_standings(context, histories=histories, columns=BASIC_COLUMNS, limit=10)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. This usually happens before matches begin. Please try again later.")
except Exception as e:
    show_error(e)
