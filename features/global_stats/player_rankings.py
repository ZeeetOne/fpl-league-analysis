"""Global player rankings — sortable, filterable table of all FPL players."""

import pandas as pd
import streamlit as st

from features.ui import metric_card, section_header

_POSITION_MAP = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}
_ALL_POSITIONS = ["GKP", "DEF", "MID", "FWD"]


def _build_player_df(bootstrap_data: dict) -> pd.DataFrame:
    teams = {t["id"]: t["short_name"] for t in bootstrap_data.get("teams", [])}
    rows = []
    for el in bootstrap_data.get("elements", []):
        rows.append({
            "Player": el["web_name"],
            "Team": teams.get(el["team"], ""),
            "Pos": _POSITION_MAP.get(el["element_type"], ""),
            "Price": round(el["now_cost"] / 10, 1),
            "Total Pts": el.get("total_points", 0),
            "GW Pts": el.get("event_points", 0),
            "Form": float(el.get("form", 0) or 0),
            "Owned %": float(el.get("selected_by_percent", 0) or 0),
            "ICT": float(el.get("ict_index", 0) or 0),
            "Pts / £m": round(el.get("total_points", 0) / max(el["now_cost"] / 10, 0.1), 1),
        })
    return pd.DataFrame(rows)


def render_player_rankings(context: dict) -> None:
    """Display global player rankings with filters."""
    bootstrap_data = context["bootstrap_data"]
    df = _build_player_df(bootstrap_data)

    # ── Summary metrics ───────────────────────────────────────────────────────
    top_scorer = df.loc[df["Total Pts"].idxmax()]
    top_gw = df.loc[df["GW Pts"].idxmax()]
    top_owned = df.loc[df["Owned %"].idxmax()]
    top_value = df.loc[df["Pts / £m"].idxmax()]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        metric_card("Top Scorer (Season)", top_scorer["Player"], f"{int(top_scorer['Total Pts'])} pts", "positive")
    with col2:
        metric_card("Top Score (This GW)", top_gw["Player"], f"{int(top_gw['GW Pts'])} pts", "positive")
    with col3:
        metric_card("Most Owned", top_owned["Player"], f"{top_owned['Owned %']}%", "neutral")
    with col4:
        metric_card("Best Value", top_value["Player"], f"{top_value['Pts / £m']} pts/£m", "positive")

    # ── Filters ───────────────────────────────────────────────────────────────
    section_header("All Players", "Filter and sort all FPL players")

    col_a, col_b, col_c, col_d = st.columns([1, 1, 1, 1])
    with col_a:
        pos_filter = st.multiselect("Position", _ALL_POSITIONS, default=_ALL_POSITIONS, key="pr_pos")
    with col_b:
        min_p = float(df["Price"].min())
        max_p = float(df["Price"].max())
        price_range = st.slider("Price (£m)", min_p, max_p, (min_p, max_p), 0.1, key="pr_price")
    with col_c:
        sort_col = st.selectbox("Sort by", ["Total Pts", "GW Pts", "Form", "Owned %", "ICT", "Pts / £m", "Price"], key="pr_sort")
    with col_d:
        min_owned = st.number_input("Min Owned %", min_value=0.0, max_value=100.0, value=0.0, step=1.0, key="pr_min_owned")

    filtered = df[
        df["Pos"].isin(pos_filter) &
        df["Price"].between(price_range[0], price_range[1]) &
        (df["Owned %"] >= min_owned)
    ].sort_values(sort_col, ascending=False)

    st.caption(f"Showing {len(filtered):,} of {len(df):,} players")

    max_pts = int(df["Total Pts"].max()) if not df.empty else 300
    max_gw_pts = int(df["GW Pts"].max() * 1.2) if not df.empty else 30

    st.dataframe(
        filtered,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn("Price (£m)", format="£%.1f"),
            "Total Pts": st.column_config.ProgressColumn("Total Pts", min_value=0, max_value=max_pts, format="%d"),
            "GW Pts": st.column_config.ProgressColumn("GW Pts", min_value=0, max_value=max_gw_pts, format="%d"),
            "Owned %": st.column_config.ProgressColumn("Owned %", min_value=0, max_value=100, format="%.1f%%"),
            "Form": st.column_config.NumberColumn("Form", format="%.1f"),
            "ICT": st.column_config.NumberColumn("ICT", format="%.1f"),
            "Pts / £m": st.column_config.NumberColumn("Pts / £m", format="%.1f"),
        },
    )
