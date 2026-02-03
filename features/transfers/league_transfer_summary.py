"""League transfer summary display."""

import streamlit as st


def render_league_transfer_summary(context: dict, histories: dict, transfers: dict) -> None:
    """Display league-wide transfer summary metrics.

    Args:
        context: League context containing standings data.
        histories: Dictionary of manager histories keyed by entry ID.
        transfers: Dictionary of manager transfers keyed by entry ID.
    """
    standings = context["standings"]

    all_transfers_by_gw = {}

    for s in standings:
        entry_id = s["entry"]
        transfer_list = transfers.get(entry_id, [])

        # Track transfers by GW for activity chart
        for t in transfer_list:
            gw = t.get("event", 0)
            all_transfers_by_gw[gw] = all_transfers_by_gw.get(gw, 0) + 1

    st.subheader("League Transfer Summary")

    most_active_gw = max(all_transfers_by_gw, key=all_transfers_by_gw.get) if all_transfers_by_gw else 0
    most_active_count = all_transfers_by_gw.get(most_active_gw, 0)

    # Get current/latest gameweek transfers
    current_gw = context.get("current_gw", 0)
    current_gw_transfers = all_transfers_by_gw.get(current_gw, 0)

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Gameweek with Most Transfers", f"GW{most_active_gw} ({most_active_count} transfers)")
    with col2:
        st.metric("This GW Transfers", f"GW{current_gw} ({current_gw_transfers} transfers)")
