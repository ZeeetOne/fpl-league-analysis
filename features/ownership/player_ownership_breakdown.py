"""Player ownership breakdown display."""

from collections import defaultdict

import pandas as pd
import plotly.express as px
import streamlit as st


POSITION_NAMES = {
    1: "Goalkeeper",
    2: "Defender",
    3: "Midfielder",
    4: "Forward"
}


def _calculate_ownership(picks_data: dict, bootstrap_data: dict) -> list:
    """Calculate player ownership across the league.

    Args:
        picks_data: {entry_id: picks_response, ...}
        bootstrap_data: Contains elements[] with player metadata

    Returns:
        List of dicts with player info and ownership stats
    """
    player_counts = defaultdict(int)
    total_managers = len([p for p in picks_data.values() if p])

    if total_managers == 0:
        return []

    # Count player occurrences
    for entry_id, picks_response in picks_data.items():
        if picks_response and picks_response.get("picks"):
            for pick in picks_response["picks"]:
                player_id = pick["element"]
                player_counts[player_id] += 1

    # Build player lookup from bootstrap
    player_info = {}
    for element in bootstrap_data.get("elements", []):
        player_info[element["id"]] = {
            "web_name": element["web_name"],
            "element_type": element["element_type"]
        }

    # Create ownership list (only owned players)
    ownership_list = []
    for player_id, count in player_counts.items():
        if count > 0:  # Filter to owned players only
            info = player_info.get(player_id, {})
            ownership_list.append({
                "player_id": player_id,
                "web_name": info.get("web_name", "Unknown"),
                "element_type": info.get("element_type", 0),
                "owned_by": count,
                "ownership_pct": round((count / total_managers * 100), 1)
            })

    return ownership_list


def _group_by_position(ownership_list: list) -> dict:
    """Group ownership data by position.

    Returns:
        {
            "Goalkeeper": [...],
            "Defender": [...],
            "Midfielder": [...],
            "Forward": [...]
        }
    """
    grouped = defaultdict(list)
    for player_data in ownership_list:
        position_type = player_data["element_type"]
        position_name = POSITION_NAMES.get(position_type, "Unknown")
        grouped[position_name].append(player_data)

    # Sort each position by ownership % descending
    for position in grouped:
        grouped[position].sort(key=lambda x: x["ownership_pct"], reverse=True)

    return dict(grouped)


def render_player_ownership(context: dict, picks_data: dict, selected_gw: int) -> None:
    """Display player ownership analysis.

    Args:
        context: League context containing bootstrap data.
        picks_data: Dictionary of manager picks keyed by entry ID.
        selected_gw: Selected gameweek number.
    """
    bootstrap_data = context["bootstrap_data"]

    # Check for empty picks data
    if not picks_data or all(p is None for p in picks_data.values()):
        st.info("No ownership data available for this gameweek.")
        return

    with st.spinner("Calculating ownership..."):
        # Calculate ownership
        ownership_list = _calculate_ownership(picks_data, bootstrap_data)

        if not ownership_list:
            st.info("No ownership data available for this gameweek.")
            return

        # Group by position
        ownership_by_position = _group_by_position(ownership_list)

    st.divider()

    # Summary metrics
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Unique Players Owned", len(ownership_list))

    with col2:
        most_owned = max(ownership_list, key=lambda x: x["ownership_pct"])
        st.metric(
            "Most Owned Player",
            most_owned["web_name"],
            f"{most_owned['ownership_pct']}%"
        )

    st.divider()

    # Position breakdown tabs
    tabs = st.tabs(["Goalkeepers", "Defenders", "Midfielders", "Forwards"])
    positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]

    for tab, position_name in zip(tabs, positions):
        with tab:
            position_data = ownership_by_position.get(position_name, [])

            if not position_data:
                st.info(f"No {position_name.lower()}s owned in this gameweek.")
                continue

            # Create DataFrame
            df = pd.DataFrame(position_data)

            # Bar chart
            fig = px.bar(
                df,
                x="ownership_pct",
                y="web_name",
                orientation="h",
                labels={"ownership_pct": "Ownership %", "web_name": "Player"},
                color="ownership_pct",
                color_continuous_scale="Blues",
            )
            fig.update_layout(
                height=max(400, len(position_data) * 25),
                showlegend=False,
                yaxis={'categoryorder': 'total ascending'},
            )
            st.plotly_chart(fig, key=f"ownership_chart_{position_name}")

            # Table
            st.subheader("Details")
            table_df = df[["web_name", "owned_by", "ownership_pct"]].copy()
            table_df.columns = ["Player", "Owned By", "Ownership %"]
            st.dataframe(table_df, hide_index=True, width='stretch')
