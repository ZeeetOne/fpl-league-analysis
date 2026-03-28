"""Global Ownership page."""

import streamlit as st

from data_loader import get_global_context, show_error
from features.global_stats import render_global_ownership
from features.ui import page_header
from fpl_api import GameUpdatingError

page_header("Global Ownership", eyebrow="Global", subtitle="Most owned players worldwide and differential picks")

try:
    context = get_global_context()
    render_global_ownership(context)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    show_error(e)
