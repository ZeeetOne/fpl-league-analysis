"""Rank movement chart display."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_rank_movement(context: dict, histories: dict) -> None:
    """Display rank movement chart showing position changes over gameweeks.

    Args:
        context: League context containing standings data.
        histories: Dictionary of manager histories keyed by entry ID.
    """
    standings = context["standings"]

    chart_data = []
    for s in standings:
        entry_id = s["entry"]
        history = histories.get(entry_id)
        if history and "current" in history:
            for gw in history["current"]:
                chart_data.append({
                    "Team": s["entry_name"],
                    "Gameweek": gw["event"],
                    "Rank": gw.get("overall_rank", gw.get("rank", 0)),
                })

    if not chart_data:
        st.warning("No rank data available")
        return

    df = pd.DataFrame(chart_data)

    # Filter to last 6 gameweeks
    max_gw = df["Gameweek"].max()
    df_last6 = df[df["Gameweek"] > max_gw - 6]

    # Calculate league-relative rank (1 = top of league)
    # Group by gameweek and assign rank based on cumulative points at that GW
    rank_data = []
    for gw in df_last6["Gameweek"].unique():
        gw_df = df_last6[df_last6["Gameweek"] == gw].copy()
        # We need to get total_points to calculate proper league rank
        # For now, use the overall rank as proxy
        for _, row in gw_df.iterrows():
            rank_data.append(row.to_dict())

    if not rank_data:
        st.warning("No rank data available")
        return

    df_ranks = pd.DataFrame(rank_data)

    fig = px.line(
        df_ranks, x="Gameweek", y="Rank", color="Team",
        title="Rank Movement (Last 6 GWs)",
        markers=True
    )

    # Invert y-axis so rank 1 is at top
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    st.plotly_chart(fig, width="stretch")
