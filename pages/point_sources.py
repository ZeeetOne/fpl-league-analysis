"""Point Sources Analysis page."""

import streamlit as st

from data_loader import get_league_context
from features.managers import render_point_distribution
from fpl_api import GameUpdatingError

st.header("Point Sources")
st.caption("*Breakdown of where managers' points come from by position*")

try:
    context = get_league_context()
    render_point_distribution(context)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
