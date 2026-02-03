"""Transfers by manager display."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_transfers_by_manager(context: dict, histories: dict, transfers: dict) -> None:
    """Display transfer statistics per manager.

    Args:
        context: League context containing standings data.
        histories: Dictionary of manager histories keyed by entry ID.
        transfers: Dictionary of manager transfers keyed by entry ID.
    """
    standings = context["standings"]
    current_gw = context.get("current_gw", 0)

    data = []

    for s in standings:
        entry_id = s["entry"]
        history = histories.get(entry_id, {})
        transfer_list = transfers.get(entry_id, [])

        total_transfers = len(transfer_list)
        transfer_cost = sum(gw.get("event_transfers_cost", 0) for gw in history.get("current", []))

        # Count transfers made in current gameweek
        current_gw_transfers = sum(1 for t in transfer_list if t.get("event", 0) == current_gw)

        data.append({
            "Team": s["entry_name"],
            "Total Transfers": total_transfers,
            "Total Hits (pts)": transfer_cost,
            "This GW Transfers": current_gw_transfers,
        })

    df = pd.DataFrame(data)
    df = df.sort_values("Total Transfers", ascending=False)

    st.subheader("Transfers by Manager")
    st.caption("*Total Hits = Points deducted for making extra transfers (4 points per additional transfer)*")
    st.dataframe(df, width='stretch', hide_index=True)

    fig = px.bar(
        df, x="Team", y="Total Transfers",
        title="Total Transfers Made",
        color="Total Hits (pts)",
        color_continuous_scale="Reds"
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, width='stretch')
