"""Dashboard home page."""

import streamlit as st

from data_loader import get_league_context, load_manager_histories
from features.dashboard import render_gw_highlights, render_league_summary, render_standings, BASIC_COLUMNS
from fpl_api import GameUpdatingError

st.title("FPL League Analysis")

try:
    with st.spinner("Loading FPL data..."):
        context = get_league_context()
        histories = load_manager_histories(context["entry_ids"])

    league_info = context["league_info"]

    st.subheader(f"League: {league_info.get('name', 'Unknown')}")

    st.divider()

    st.header("League Summary")
    st.caption("*Overview of league status*")
    render_league_summary(context)

    st.divider()

    st.header("This GW Highlights")
    st.caption("*Notable changes and standout performances*")
    render_gw_highlights(context)

    st.divider()

    st.header("League Standings")
    st.caption("*Current rankings and point totals*")
    render_standings(context, histories=histories, columns=BASIC_COLUMNS, limit=10)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. This usually happens before matches begin. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
