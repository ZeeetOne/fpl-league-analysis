"""Season points trajectory display."""

import plotly.graph_objects as go
import streamlit as st


def render_season_trajectory(team1_name: str, team2_name: str, history1: list, history2: list) -> None:
    """Display season points trajectory chart.

    Args:
        team1_name: Name of first team.
        team2_name: Name of second team.
        history1: History data for first team.
        history2: History data for second team.
    """
    st.subheader("Season Points Trajectory")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[gw["event"] for gw in history1],
        y=[gw["total_points"] for gw in history1],
        mode="lines+markers",
        name=team1_name,
        line=dict(width=2),
    ))
    fig.add_trace(go.Scatter(
        x=[gw["event"] for gw in history2],
        y=[gw["total_points"] for gw in history2],
        mode="lines+markers",
        name=team2_name,
        line=dict(width=2),
    ))
    fig.update_layout(
        xaxis_title="Gameweek",
        yaxis_title="Total Points",
        height=400,
    )
    st.plotly_chart(fig, width='stretch')
