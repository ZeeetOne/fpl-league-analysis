"""Team comparison summary display."""

import streamlit as st

from features.ui import metric_card


def render_team_comparison(context: dict, histories: dict) -> tuple:
    """Display team comparison with stats.

    Args:
        context: League context containing standings data.
        histories: Dictionary of manager histories keyed by entry ID.

    Returns:
        Tuple of (team1_name, team2_name, history1, history2) for use in other sections.
    """
    standings = context["standings"]

    team_options = {s["entry_name"]: s for s in standings}

    col1, col2 = st.columns(2)
    with col1:
        team1_name = st.selectbox("Select Team 1", list(team_options.keys()), key="h2h_team1")
    with col2:
        team2_name = st.selectbox(
            "Select Team 2",
            [t for t in team_options.keys() if t != team1_name],
            key="h2h_team2"
        )

    team1 = team_options[team1_name]
    team2 = team_options[team2_name]

    history1 = histories.get(team1["entry"], {}).get("current", [])
    history2 = histories.get(team2["entry"], {}).get("current", [])

    if not history1 or not history2:
        st.warning("Could not load history for one or both teams")
        return None, None, None, None

    def calc_stats(history):
        points = [gw["points"] for gw in history]
        return {
            "Total Points": sum(points),
            "Average Points": round(sum(points) / len(points), 1) if points else 0,
            "Best GW Points": max(points) if points else 0,
            "Worst GW Points": min(points) if points else 0,
            "Gameweeks Played": len(points),
        }

    stats1 = calc_stats(history1)
    stats2 = calc_stats(history2)

    stat_keys = list(stats1.keys())

    # Display as a grid: label | team1 value | team2 value
    for key in stat_keys:
        v1 = stats1[key]
        v2 = stats2[key]
        delta = v2 - v1 if isinstance(v2, (int, float)) else None

        cols = st.columns([2, 1, 1])
        cols[0].markdown(f"**{key}**")

        delta_type1 = "neutral"
        delta_type2 = "neutral"
        if delta is not None and delta != 0:
            if key == "Worst GW Points":
                delta_type1 = "positive" if delta < 0 else "neutral"
                delta_type2 = "positive" if delta > 0 else "neutral"
            else:
                delta_type1 = "positive" if delta < 0 else "neutral"
                delta_type2 = "positive" if delta > 0 else "neutral"

        with cols[1]:
            metric_card(team1_name, str(v1), delta_type=delta_type1)
        with cols[2]:
            delta_label = f"+{delta}" if delta and delta > 0 else (f"{delta}" if delta else None)
            metric_card(team2_name, str(v2), delta_label, delta_type=delta_type2)

    return team1_name, team2_name, history1, history2
