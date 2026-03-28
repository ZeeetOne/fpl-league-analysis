"""Rank movement chart — league position per gameweek derived from cumulative points."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_rank_movement(context: dict, histories: dict) -> None:
    """Display league rank movement chart (position within the mini-league per GW)."""
    standings = context["standings"]

    # Build {gw: {team_name: total_points}} from cumulative history
    gw_totals: dict[int, dict[str, int]] = {}
    for s in standings:
        entry_id = s["entry"]
        history = histories.get(entry_id)
        if not history or "current" not in history:
            continue
        for gw_data in history["current"]:
            gw = gw_data["event"]
            if gw not in gw_totals:
                gw_totals[gw] = {}
            gw_totals[gw][s["entry_name"]] = gw_data["total_points"]

    if not gw_totals:
        st.warning("No rank data available.")
        return

    # Derive league rank at each GW from cumulative points
    chart_data = []
    for gw in sorted(gw_totals):
        totals = gw_totals[gw]
        sorted_teams = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        for league_rank, (team_name, _) in enumerate(sorted_teams, 1):
            chart_data.append({
                "Team": team_name,
                "Gameweek": gw,
                "League Rank": league_rank,
            })

    df = pd.DataFrame(chart_data)

    # Filter to last 6 gameweeks
    max_gw = df["Gameweek"].max()
    df_last6 = df[df["Gameweek"] > max_gw - 6]

    n_teams = df["Team"].nunique()
    fig = px.line(
        df_last6, x="Gameweek", y="League Rank", color="Team",
        markers=True,
        color_discrete_sequence=px.colors.qualitative.Plotly,
    )
    fig.update_yaxes(
        autorange="reversed",
        tickmode="linear",
        tick0=1,
        dtick=1,
        range=[n_teams + 0.5, 0.5],
        title="League Position",
    )
    fig.update_xaxes(tickmode="linear", dtick=1, title="Gameweek")
    fig.update_layout(
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)
