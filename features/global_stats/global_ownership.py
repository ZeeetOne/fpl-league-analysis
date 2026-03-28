"""Global player ownership — most owned players worldwide with differential insights."""

import pandas as pd
import plotly.express as px
import streamlit as st

from features.ui import metric_card, section_header

_POSITION_MAP = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}
_POSITION_TABS = ["Goalkeepers", "Defenders", "Midfielders", "Forwards"]
_POSITION_KEYS = ["GKP", "DEF", "MID", "FWD"]


def _build_ownership_df(bootstrap_data: dict) -> pd.DataFrame:
    teams = {t["id"]: t["short_name"] for t in bootstrap_data.get("teams", [])}
    rows = []
    for el in bootstrap_data.get("elements", []):
        rows.append({
            "Player": el["web_name"],
            "Team": teams.get(el["team"], ""),
            "Pos": _POSITION_MAP.get(el["element_type"], ""),
            "Price": round(el["now_cost"] / 10, 1),
            "Owned %": float(el.get("selected_by_percent", 0) or 0),
            "Total Pts": el.get("total_points", 0),
            "GW Pts": el.get("event_points", 0),
            "Form": float(el.get("form", 0) or 0),
            "Pts / £m": round(el.get("total_points", 0) / max(el["now_cost"] / 10, 0.1), 1),
        })
    return pd.DataFrame(rows)


def _ownership_bar(pos_df: pd.DataFrame, n: int = 15) -> None:
    top = pos_df.nlargest(n, "Owned %")
    fig = px.bar(
        top, x="Owned %", y="Player", orientation="h",
        color="Owned %",
        color_continuous_scale=[[0, "#e9d5f5"], [1, "#37003c"]],
        text="Owned %",
        hover_data=["Team", "Price", "Total Pts", "GW Pts"],
    )
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig.update_layout(
        template="plotly_white",
        height=max(380, n * 26),
        xaxis_title="Ownership %",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        coloraxis_showscale=False,
        showlegend=False,
        margin=dict(t=10, b=20, l=10, r=60),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_global_ownership(context: dict) -> None:
    """Display global player ownership analysis."""
    bootstrap_data = context["bootstrap_data"]
    df = _build_ownership_df(bootstrap_data)

    # ── Summary metrics ───────────────────────────────────────────────────────
    top_owned = df.loc[df["Owned %"].idxmax()]
    avg_owned = df[df["Owned %"] > 0]["Owned %"].mean()
    above_50 = len(df[df["Owned %"] >= 50])
    must_haves = len(df[df["Owned %"] >= 70])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Most Owned", top_owned["Player"], f"{top_owned['Owned %']}%", "neutral")
    with col2:
        metric_card("Avg Ownership", f"{avg_owned:.1f}%", "of owned players")
    with col3:
        metric_card("Players >50% Owned", str(above_50), "widespread picks")
    with col4:
        metric_card("Must-Haves (>70%)", str(must_haves), "near-universal")

    # ── Position tabs ─────────────────────────────────────────────────────────
    section_header("Ownership by Position", "Top globally owned players per position")

    tabs = st.tabs(_POSITION_TABS)
    for tab, pos_key in zip(tabs, _POSITION_KEYS):
        with tab:
            pos_df = df[df["Pos"] == pos_key].copy()
            if pos_df.empty:
                st.info("No data available.")
                continue

            _ownership_bar(pos_df)

            detail_df = pos_df.nlargest(20, "Owned %")[
                ["Player", "Team", "Price", "Owned %", "Total Pts", "GW Pts", "Form", "Pts / £m"]
            ]
            st.dataframe(
                detail_df, hide_index=True, use_container_width=True,
                column_config={
                    "Price": st.column_config.NumberColumn("Price", format="£%.1f"),
                    "Owned %": st.column_config.ProgressColumn("Owned %", min_value=0, max_value=100, format="%.1f%%"),
                    "Total Pts": st.column_config.ProgressColumn("Total Pts", min_value=0, max_value=int(df["Total Pts"].max()), format="%d"),
                    "Form": st.column_config.NumberColumn("Form", format="%.1f"),
                    "Pts / £m": st.column_config.NumberColumn("Pts / £m", format="%.1f"),
                },
            )

    # ── Differentials ─────────────────────────────────────────────────────────
    section_header("Differentials", "Low ownership but strong form — potential edge picks")

    diff_df = df[
        (df["Owned %"] < 10) &
        (df["Form"] >= df["Form"].quantile(0.75))
    ].sort_values("Form", ascending=False).head(20)[
        ["Player", "Team", "Pos", "Price", "Owned %", "Form", "Total Pts", "GW Pts", "Pts / £m"]
    ]

    if diff_df.empty:
        st.info("No differential players found with current filters.")
    else:
        st.dataframe(
            diff_df, hide_index=True, use_container_width=True,
            column_config={
                "Price": st.column_config.NumberColumn("Price", format="£%.1f"),
                "Owned %": st.column_config.NumberColumn("Owned %", format="%.1f%%"),
                "Form": st.column_config.ProgressColumn("Form", min_value=0, max_value=float(df["Form"].max()), format="%.1f"),
                "Total Pts": st.column_config.NumberColumn("Total Pts", format="%d"),
                "Pts / £m": st.column_config.NumberColumn("Pts / £m", format="%.1f"),
            },
        )
