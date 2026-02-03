"""League summary metrics display."""

import streamlit as st


def render_league_summary(context: dict) -> None:
    """Display league summary metrics as cards.

    Args:
        context: League context containing standings and current gameweek.
    """
    standings = context["standings"]
    current_gw = context["current_gw"]

    total_managers = len(standings)
    avg_points = sum(s["total"] for s in standings) / total_managers if standings else 0
    leader = standings[0] if standings else None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Managers", total_managers)
    with col2:
        st.metric("Current Gameweek", f"GW {current_gw}")
    with col3:
        st.metric("League Avg Points", f"{avg_points:.0f}")
    with col4:
        if leader:
            st.metric("Leader", leader["entry_name"], f"Rank 1 w/ {leader['total']} pts")
