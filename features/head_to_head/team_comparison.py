"""Team comparison summary display."""

import streamlit as st


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

    # Calculate stats
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

    # Display comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(team1_name)
        for key, value in stats1.items():
            st.metric(key, value)

    with col2:
        st.subheader(team2_name)
        for key, value in stats2.items():
            delta = value - stats1[key] if isinstance(value, (int, float)) else None
            st.metric(key, value, delta=delta if delta else None)

    return team1_name, team2_name, history1, history2
