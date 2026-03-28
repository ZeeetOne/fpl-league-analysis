"""Points per gameweek chart display."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_points_per_gameweek(context: dict, histories: dict) -> None:
    """Display points per gameweek chart with league average line.

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
                    "Points": gw["points"],
                })

    if not chart_data:
        st.warning("No gameweek data available")
        return

    df = pd.DataFrame(chart_data)

    # Filter to last 6 gameweeks
    max_gw = df["Gameweek"].max()
    df_last6 = df[df["Gameweek"] > max_gw - 6]

    # Calculate league average per gameweek
    avg_by_gw = df_last6.groupby("Gameweek")["Points"].mean().reset_index()
    avg_by_gw.columns = ["Gameweek", "Avg Points"]

    fig = px.line(
        df_last6, x="Gameweek", y="Points", color="Team",
        markers=True,
        template="plotly_white",
    )

    # Add league average line
    fig.add_trace(go.Scatter(
        x=avg_by_gw["Gameweek"],
        y=avg_by_gw["Avg Points"],
        mode="lines",
        name="League Avg",
        line=dict(color="#37003c", width=3, dash="dash"),
    ))

    fig.update_layout(
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=40, b=40, l=40, r=40),
        xaxis_title="Gameweek",
        yaxis_title="Points",
    )
    st.plotly_chart(fig, use_container_width=True)
