"""Best Squad page - Top performing FPL players in formation."""

import streamlit as st

from fpl_api import get_bootstrap_data, get_live_gameweek, get_current_gameweek, GameUpdatingError
from features.best_squad import render_best_squad

st.header("Best Squad")
st.caption("*Top performing FPL players in football formation*")

try:
    # Load bootstrap data (no league context needed)
    with st.spinner("Loading FPL data..."):
        bootstrap_data = get_bootstrap_data()
        current_gw = get_current_gameweek(bootstrap_data)

    # Gameweek selector
    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
    )

    # Load live gameweek data
    with st.spinner("Loading player performances..."):
        live_data = get_live_gameweek(selected_gw)

    # Render formation
    render_best_squad(bootstrap_data, live_data, selected_gw)

except GameUpdatingError:
    st.warning("The FPL game is currently being updated. Please try again later.")
except Exception as e:
    st.error(f"Failed to load data: {e}")
