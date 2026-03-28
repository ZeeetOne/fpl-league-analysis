"""Most transferred players display."""

from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st

import fpl_api


def render_most_transferred_players(context: dict, transfers: dict) -> None:
    """Display most transferred players in/out.

    Args:
        context: League context containing bootstrap data.
        transfers: Dictionary of manager transfers keyed by entry ID.
    """
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    selected_gw = st.selectbox(
        "Select Gameweek",
        options=list(range(1, current_gw + 1)),
        index=current_gw - 1,
        key="transfers_gw_select",
    )

    all_transfers_in = []
    all_transfers_out = []

    for entry_id, transfer_list in transfers.items():
        for t in transfer_list:
            if t.get("event") == selected_gw:
                all_transfers_in.append(t.get("element_in"))
                all_transfers_out.append(t.get("element_out"))

    in_counts = Counter(all_transfers_in)
    out_counts = Counter(all_transfers_out)

    col1, col2 = st.columns(2)

    with col1:
        top_in = in_counts.most_common(10)
        in_data = [{"Player": fpl_api.get_player_name(pid, bootstrap_data), "Count": count}
                   for pid, count in top_in if pid]
        if in_data:
            df_in = pd.DataFrame(in_data)
            fig_in = px.bar(
                df_in.sort_values("Count"),
                x="Count", y="Player",
                orientation="h",
                title="Most Transferred In",
                template="plotly_white",
                color_discrete_sequence=["#16a34a"],
            )
            fig_in.update_layout(
                height=380,
                margin=dict(t=40, b=20, l=10, r=20),
                yaxis_title="",
                xaxis_title="Times Transferred In",
            )
            st.plotly_chart(fig_in, use_container_width=True)
        else:
            st.info("No transfers in for this gameweek")

    with col2:
        top_out = out_counts.most_common(10)
        out_data = [{"Player": fpl_api.get_player_name(pid, bootstrap_data), "Count": count}
                    for pid, count in top_out if pid]
        if out_data:
            df_out = pd.DataFrame(out_data)
            fig_out = px.bar(
                df_out.sort_values("Count"),
                x="Count", y="Player",
                orientation="h",
                title="Most Transferred Out",
                template="plotly_white",
                color_discrete_sequence=["#dc2626"],
            )
            fig_out.update_layout(
                height=380,
                margin=dict(t=40, b=20, l=10, r=20),
                yaxis_title="",
                xaxis_title="Times Transferred Out",
            )
            st.plotly_chart(fig_out, use_container_width=True)
        else:
            st.info("No transfers out for this gameweek")
