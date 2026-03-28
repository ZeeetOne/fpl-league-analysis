"""Global Player Rankings page."""

import streamlit as st

from data_loader import get_global_context
from features.global_stats import render_player_rankings
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("Player Rankings", eyebrow="Global", subtitle="All FPL players ranked by points, form, value and more")

try:
    context = get_global_context()
    render_player_rankings(context)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
