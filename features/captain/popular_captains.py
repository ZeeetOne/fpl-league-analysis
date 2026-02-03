"""Popular captains analysis display."""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

import fpl_api


def render_captain_picks(context: dict, histories: dict = None) -> None:
    """Display captain picks analysis.

    Args:
        context: League context containing standings and bootstrap data.
        histories: Dictionary of manager histories keyed by entry ID.
    """
    standings = context["standings"]
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    # Build player points lookup
    player_points = {}
    for element in bootstrap_data.get("elements", []):
        player_points[element["id"]] = element.get("event_points", 0)

    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
    )

    with st.spinner("Loading captain data..."):
        all_captains = []
        captain_points_list = []

        for s in standings:
            entry_id = s["entry"]

            try:
                picks = fpl_api.get_manager_picks(entry_id, selected_gw)
                for pick in picks.get("picks", []):
                    if pick.get("is_captain"):
                        captain_id = pick["element"]
                        all_captains.append(captain_id)
                        # Get captain points (doubled for captain)
                        pts = player_points.get(captain_id, 0) * 2
                        captain_points_list.append({
                            "captain_id": captain_id,
                            "points": pts,
                        })
                        break
            except Exception:
                pass

    # Most popular captains with points
    st.subheader("Most Popular Captains")
    captain_counts = Counter(all_captains)
    top_captains = captain_counts.most_common(10)

    captain_df = pd.DataFrame([
        {
            "Captain": fpl_api.get_player_name(pid, bootstrap_data),
            "Picked by Managers": count,
            "Points (x2)": player_points.get(pid, 0) * 2,
        }
        for pid, count in top_captains if pid
    ])

    if not captain_df.empty:
        # Captain success metrics
        if captain_points_list:
            best_captain = max(captain_points_list, key=lambda x: x["points"])
            worst_captain = min(captain_points_list, key=lambda x: x["points"])

            col1, col2 = st.columns(2)
            with col1:
                best_name = fpl_api.get_player_name(best_captain["captain_id"], bootstrap_data)
                st.metric("Best Captain", f"{best_name} ({best_captain['points']} pts)")
            with col2:
                worst_name = fpl_api.get_player_name(worst_captain["captain_id"], bootstrap_data)
                st.metric("Worst Captain", f"{worst_name} ({worst_captain['points']} pts)")

        st.divider()

        fig = px.bar(
            captain_df, x="Captain", y="Picked by Managers",
            title="Most Popular Captain Picks",
            color="Points (x2)",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig, width="stretch")

        st.dataframe(captain_df, width="stretch", hide_index=True)
    else:
        st.warning("No captain data available for selected gameweek")
