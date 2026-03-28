"""League summary metrics display."""

import streamlit as st

from features.ui import metric_card


def render_league_summary(context: dict) -> None:
    """Display league summary metrics as styled cards."""
    standings = context["standings"]
    current_gw = context["current_gw"]

    total_managers = len(standings)
    avg_points = sum(s["total"] for s in standings) / total_managers if standings else 0
    leader = standings[0] if standings else None

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        metric_card("Total Managers", str(total_managers))
    with col2:
        metric_card("Current Gameweek", f"GW {current_gw}")
    with col3:
        metric_card("League Avg Points", f"{avg_points:.0f} pts")
    with col4:
        if leader:
            metric_card(
                "League Leader",
                leader["entry_name"],
                f"Rank 1 · {leader['total']} pts",
                "positive",
            )
        else:
            metric_card("League Leader", "—")
