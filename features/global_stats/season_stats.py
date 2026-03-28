"""Global season statistics — GW averages, highest scores, chip usage."""

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from features.ui import metric_card, section_header

_CHIP_LABELS = {
    "wildcard": "Wildcard",
    "freehit": "Free Hit",
    "bboost": "Bench Boost",
    "3xc": "Triple Captain",
}

_CHIP_COLORS = {
    "Wildcard": "#37003c",
    "Free Hit": "#7b2d8b",
    "Bench Boost": "#16a34a",
    "Triple Captain": "#d97706",
}


def render_season_stats(context: dict) -> None:
    """Display global season statistics."""
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    events = bootstrap_data.get("events", [])
    played = [e for e in events if e.get("finished") or e.get("is_current")]

    if not played:
        st.info("No gameweek data available yet.")
        return

    # ── Summary metrics ───────────────────────────────────────────────────────
    avgs = [e["average_entry_score"] for e in played if e.get("average_entry_score")]
    highs = [e["highest_score"] for e in played if e.get("highest_score")]

    season_avg = round(sum(avgs) / len(avgs), 1) if avgs else 0
    best_avg_gw = max(played, key=lambda e: e.get("average_entry_score") or 0)
    all_time_high = max(highs) if highs else 0
    all_time_high_gw = next((e["id"] for e in played if e.get("highest_score") == all_time_high), "—")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Season Avg Score", f"{season_avg} pts")
    with col2:
        metric_card("Best GW Avg", f"GW {best_avg_gw['id']}", f"{best_avg_gw.get('average_entry_score', 0)} pts avg", "positive")
    with col3:
        metric_card("All-Time High Score", f"{all_time_high} pts", f"GW {all_time_high_gw}", "positive")
    with col4:
        metric_card("Gameweeks Played", str(len(played)), f"of 38 total")

    # ── GW avg + highest score chart ─────────────────────────────────────────
    section_header("Score Trends", "Global average and highest score per gameweek")

    gw_df = pd.DataFrame([
        {
            "Gameweek": e["id"],
            "Global Avg": e.get("average_entry_score", 0),
            "Highest Score": e.get("highest_score", 0),
        }
        for e in played
    ])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=gw_df["Gameweek"], y=gw_df["Highest Score"],
        name="Highest Score",
        mode="lines+markers",
        line=dict(color="#37003c", width=2),
        marker=dict(size=5),
        fill="tozeroy",
        fillcolor="rgba(55,0,60,0.06)",
    ))
    fig.add_trace(go.Scatter(
        x=gw_df["Gameweek"], y=gw_df["Global Avg"],
        name="Global Avg",
        mode="lines+markers",
        line=dict(color="#16a34a", width=3),
        marker=dict(size=6),
    ))
    fig.update_layout(
        template="plotly_white",
        height=400,
        xaxis_title="Gameweek",
        yaxis_title="Points",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        margin=dict(t=20, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    # ── Chip usage ────────────────────────────────────────────────────────────
    section_header("Chip Usage", "How many managers played each chip per gameweek")

    chip_rows = []
    for e in played:
        for chip in e.get("chip_plays", []):
            label = _CHIP_LABELS.get(chip["chip_name"], chip["chip_name"])
            chip_rows.append({
                "Gameweek": e["id"],
                "Chip": label,
                "Managers": chip["num_played"],
            })

    if chip_rows:
        chip_df = pd.DataFrame(chip_rows)
        chip_totals = chip_df.groupby("Chip")["Managers"].sum().reset_index()
        chip_totals.columns = ["Chip", "Total Uses"]

        col_chart, col_table = st.columns([2, 1])

        with col_chart:
            fig2 = go.Figure()
            for chip_name, color in _CHIP_COLORS.items():
                subset = chip_df[chip_df["Chip"] == chip_name]
                if not subset.empty:
                    fig2.add_trace(go.Bar(
                        x=subset["Gameweek"],
                        y=subset["Managers"],
                        name=chip_name,
                        marker_color=color,
                    ))
            fig2.update_layout(
                template="plotly_white",
                barmode="stack",
                height=350,
                xaxis_title="Gameweek",
                yaxis_title="Managers",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=20, b=40),
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col_table:
            st.dataframe(
                chip_totals.sort_values("Total Uses", ascending=False),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Total Uses": st.column_config.ProgressColumn(
                        "Total Uses",
                        min_value=0,
                        max_value=int(chip_totals["Total Uses"].max() * 1.1),
                        format="%d",
                    )
                },
            )
    else:
        st.info("No chip data available yet.")
