"""Gameweek by gameweek breakdown display."""

import pandas as pd
import streamlit as st


def render_gameweek_breakdown(team1_name: str, team2_name: str, history1: list, history2: list) -> None:
    """Display gameweek by gameweek breakdown.

    Args:
        team1_name: Name of first team.
        team2_name: Name of second team.
        history1: History data for first team.
        history2: History data for second team.
    """
    st.subheader("Gameweek by Gameweek")

    h2h_data = []
    wins1, wins2, draws = 0, 0, 0
    biggest_swing = {"gw": 0, "diff": 0, "winner": ""}

    for gw1, gw2 in zip(history1, history2):
        diff = abs(gw1["points"] - gw2["points"])

        if gw1["points"] > gw2["points"]:
            wins1 += 1
            winner = team1_name
        elif gw2["points"] > gw1["points"]:
            wins2 += 1
            winner = team2_name
        else:
            draws += 1
            winner = "Draw"

        # Track biggest swing
        if diff > biggest_swing["diff"]:
            biggest_swing = {"gw": gw1["event"], "diff": diff, "winner": winner}

        h2h_data.append({
            "GW": gw1["event"],
            team1_name: gw1["points"],
            team2_name: gw2["points"],
            "Diff": diff,
            "Winner": winner,
        })

    # Summary stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Record", f"{wins1} - {draws} - {wins2}")
    with col2:
        st.metric(
            "Biggest Swing",
            f"GW{biggest_swing['gw']} ({biggest_swing['diff']} pts)",
            delta=biggest_swing['winner']
        )

    st.write(f"**{team1_name}** wins: {wins1} | **{team2_name}** wins: {wins2} | Draws: {draws}")

    df = pd.DataFrame(h2h_data)
    st.dataframe(df, width='stretch', hide_index=True)
