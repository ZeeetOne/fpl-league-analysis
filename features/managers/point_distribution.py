"""Point distribution by position display."""

from collections import defaultdict

import plotly.graph_objects as go
import streamlit as st

import fpl_api


def _get_position_name(element_type: int) -> str:
    """Get position name from element type.

    Args:
        element_type: Position type (1=GK, 2=DEF, 3=MID, 4=FWD).

    Returns:
        Position name.
    """
    positions = {
        1: "Goalkeeper",
        2: "Defense",
        3: "Midfield",
        4: "Attack"
    }
    return positions.get(element_type, "Unknown")


def _calculate_position_points(entry_id: int, gameweek: int, bootstrap_data: dict) -> dict:
    """Calculate points by position for a manager in a specific gameweek.

    Args:
        entry_id: Manager's entry ID.
        gameweek: Gameweek number to analyze.
        bootstrap_data: Bootstrap data containing player information.

    Returns:
        Dictionary with position names as keys and total points as values.
    """
    # Build player lookup with position info
    player_lookup = {}
    for element in bootstrap_data.get("elements", []):
        player_lookup[element["id"]] = {
            "element_type": element["element_type"],
        }

    position_points = defaultdict(int)

    try:
        # Get the manager's picks for this gameweek
        picks_data = fpl_api.get_manager_picks(entry_id, gameweek)
        picks = picks_data.get("picks", [])

        # Get live gameweek data to get player points
        live_data = fpl_api.get_live_gameweek(gameweek)

        # Build a lookup for player points in this gameweek
        player_gw_points = {}
        for element_data in live_data.get("elements", []):
            player_id = element_data["id"]
            stats = element_data.get("stats", {})
            player_gw_points[player_id] = stats.get("total_points", 0)

        # Calculate points by position
        for pick in picks:
            player_id = pick["element"]
            multiplier = pick.get("multiplier", 0)

            # Get points from live data
            player_points = player_gw_points.get(player_id, 0)
            total_points = multiplier * player_points

            # Get player position
            player_info = player_lookup.get(player_id)
            if player_info:
                element_type = player_info["element_type"]
                position_name = _get_position_name(element_type)
                position_points[position_name] += total_points

    except Exception as e:
        # Return empty dict if data is not available
        return {}

    return dict(position_points)


def render_point_distribution(context: dict) -> None:
    """Display point distribution by position analysis.

    Args:
        context: League context containing standings and bootstrap data.
    """
    standings = context["standings"]
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    team_options = {s["entry_name"]: s for s in standings}

    # Gameweek selection
    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
    )

    # Manager selection - same style as Head-to-Head
    col1, col2 = st.columns(2)
    with col1:
        team1_name = st.selectbox("Select Manager 1", list(team_options.keys()), key="ps_team1")
    with col2:
        team2_name = st.selectbox(
            "Select Manager 2",
            [t for t in team_options.keys() if t != team1_name],
            key="ps_team2"
        )

    team1 = team_options[team1_name]
    team2 = team_options[team2_name]

    # Calculate position points for both managers
    with st.spinner("Loading gameweek data..."):
        try:
            position_points_1 = _calculate_position_points(team1["entry"], selected_gw, bootstrap_data)
            position_points_2 = _calculate_position_points(team2["entry"], selected_gw, bootstrap_data)

        except Exception as e:
            st.error(f"Error calculating point distribution: {e}")
            return

    if not position_points_1 and not position_points_2:
        st.warning("No point data available for the selected managers. This could mean the gameweek hasn't started yet.")
        return

    st.divider()

    # Display pie charts side by side
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(team1_name)

        if position_points_1:
            total_points_1 = sum(position_points_1.values())
            st.markdown(f"**Total Points:** {total_points_1} pts")

            # Create pie chart
            fig1 = go.Figure(data=[go.Pie(
                labels=list(position_points_1.keys()),
                values=list(position_points_1.values()),
                hole=0.3,
                marker=dict(
                    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
                ),
            )])

            fig1.update_layout(
                height=400,
                showlegend=True,
                margin=dict(t=20, b=20, l=20, r=20),
            )

            st.plotly_chart(fig1, key="pie_chart_team1")

            # Show breakdown
            with st.expander("View Breakdown"):
                for position, points in sorted(
                    position_points_1.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    percentage = (points / total_points_1 * 100) if total_points_1 > 0 else 0
                    st.write(f"**{position}:** {points} pts ({percentage:.1f}%)")
        else:
            st.warning("No data available")

    with col2:
        st.subheader(team2_name)

        if position_points_2:
            total_points_2 = sum(position_points_2.values())
            total_points_1 = sum(position_points_1.values()) if position_points_1 else 0
            diff = total_points_2 - total_points_1

            # Format difference with + or - sign
            if diff > 0:
                diff_text = f"<span style='color: green;'>(+{diff})</span>"
            elif diff < 0:
                diff_text = f"<span style='color: red;'>({diff})</span>"
            else:
                diff_text = "(0)"

            st.markdown(f"**Total Points:** {total_points_2} pts {diff_text}", unsafe_allow_html=True)

            # Create pie chart
            fig2 = go.Figure(data=[go.Pie(
                labels=list(position_points_2.keys()),
                values=list(position_points_2.values()),
                hole=0.3,
                marker=dict(
                    colors=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
                ),
            )])

            fig2.update_layout(
                height=400,
                showlegend=True,
                margin=dict(t=20, b=20, l=20, r=20),
            )

            st.plotly_chart(fig2, key="pie_chart_team2")

            # Show breakdown
            with st.expander("View Breakdown"):
                for position, points in sorted(
                    position_points_2.items(),
                    key=lambda x: x[1],
                    reverse=True
                ):
                    percentage = (points / total_points_2 * 100) if total_points_2 > 0 else 0
                    st.write(f"**{position}:** {points} pts ({percentage:.1f}%)")
        else:
            st.warning("No data available")

    # Comparison bar chart
    st.divider()
    st.subheader("Position Comparison")

    if position_points_1 and position_points_2:
        positions = ["Goalkeeper", "Defense", "Midfield", "Attack"]

        fig = go.Figure()

        # Team 1 bars
        values_1 = [position_points_1.get(pos, 0) for pos in positions]
        fig.add_trace(go.Bar(
            name=team1_name,
            x=positions,
            y=values_1,
            marker_color='#4ECDC4',
            text=values_1,
            textposition='auto',
        ))

        # Team 2 bars
        values_2 = [position_points_2.get(pos, 0) for pos in positions]
        fig.add_trace(go.Bar(
            name=team2_name,
            x=positions,
            y=values_2,
            marker_color='#FF6B6B',
            text=values_2,
            textposition='auto',
        ))

        fig.update_layout(
            barmode='group',
            xaxis_title="Position",
            yaxis_title="Total Points",
            height=400,
            showlegend=True,
        )

        st.plotly_chart(fig, key="bar_chart_comparison")
