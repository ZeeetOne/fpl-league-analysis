"""Transfer activity by gameweek display."""

import pandas as pd
import plotly.express as px
import streamlit as st


def render_transfer_activity_by_gw(context: dict, histories: dict, transfers: dict) -> None:
    """Display transfer activity chart by gameweek.

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

    st.subheader("Transfer Activity by Gameweek")

    if all_transfers_by_gw:
        gw_data = pd.DataFrame([
            {"Gameweek": f"GW{gw}", "GW_num": gw, "Transfers": count}
            for gw, count in sorted(all_transfers_by_gw.items())
        ])
        gw_data = gw_data.sort_values("GW_num")

        fig_activity = px.bar(
            gw_data, x="Gameweek", y="Transfers",
            title="League Transfer Activity per Gameweek",
            color="Transfers",
            color_continuous_scale="Blues"
        )
        fig_activity.update_layout(height=350)
        st.plotly_chart(fig_activity, width='stretch')
