"""Global Season Stats page."""

import streamlit as st

from data_loader import get_global_context
from features.global_stats import render_season_stats
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("Season Stats", eyebrow="Global", subtitle="Worldwide FPL averages, highest scores and chip usage")

try:
    context = get_global_context()
    render_season_stats(context)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
