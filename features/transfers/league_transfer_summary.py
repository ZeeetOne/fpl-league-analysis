"""League transfer summary display."""

import streamlit as st

from features.ui import metric_card


def render_league_transfer_summary(context: dict, histories: dict, transfers: dict) -> None:
    """Display league-wide transfer summary metrics.

    Args:
        context: League context containing standings data.
        histories: Dictionary of manager histories keyed by entry ID.
        transfers: Dictionary of manager transfers keyed by entry ID.
    """
    standings = context["standings"]
    current_gw = context.get("current_gw", 0)

    all_transfers_by_gw = {}
    transfers_per_manager = {}
    total_hit_cost = 0

    for s in standings:
        entry_id = s["entry"]
        transfer_list = transfers.get(entry_id, [])
        transfers_per_manager[s["entry_name"]] = len(transfer_list)

        for t in transfer_list:
            gw = t.get("event", 0)
            all_transfers_by_gw[gw] = all_transfers_by_gw.get(gw, 0) + 1

    # Calculate total hit costs from histories
    for s in standings:
        entry_id = s["entry"]
        history = histories.get(entry_id, {})
        for gw in history.get("current", []):
            total_hit_cost += gw.get("event_transfers_cost", 0)

    total_transfers = sum(all_transfers_by_gw.values())
    most_active_gw = max(all_transfers_by_gw, key=all_transfers_by_gw.get) if all_transfers_by_gw else 0
    most_active_count = all_transfers_by_gw.get(most_active_gw, 0)
    most_active_manager = max(transfers_per_manager, key=transfers_per_manager.get) if transfers_per_manager else "—"
    most_active_manager_count = transfers_per_manager.get(most_active_manager, 0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Total Transfers", str(total_transfers), "season total")
    with col2:
        metric_card("Busiest GW", f"GW{most_active_gw}", f"{most_active_count} transfers")
    with col3:
        metric_card("Most Active Manager", most_active_manager, f"{most_active_manager_count} transfers")
    with col4:
        metric_card("Total Hit Cost", f"-{total_hit_cost} pts", "points deducted", "negative" if total_hit_cost > 0 else "neutral")
