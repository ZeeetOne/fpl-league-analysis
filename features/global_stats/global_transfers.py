"""Global transfer trends — most transferred in/out this GW and season-wide."""

import pandas as pd
import plotly.express as px
import streamlit as st

from features.ui import metric_card, section_header

_POSITION_MAP = {1: "GKP", 2: "DEF", 3: "MID", 4: "FWD"}


def _build_transfer_df(bootstrap_data: dict) -> pd.DataFrame:
    teams = {t["id"]: t["short_name"] for t in bootstrap_data.get("teams", [])}
    rows = []
    for el in bootstrap_data.get("elements", []):
        in_gw = el.get("transfers_in_event", 0) or 0
        out_gw = el.get("transfers_out_event", 0) or 0
        in_season = el.get("transfers_in", 0) or 0
        out_season = el.get("transfers_out", 0) or 0
        rows.append({
            "Player": el["web_name"],
            "Team": teams.get(el["team"], ""),
            "Pos": _POSITION_MAP.get(el["element_type"], ""),
            "Price": round(el["now_cost"] / 10, 1),
            "In (GW)": in_gw,
            "Out (GW)": out_gw,
            "Net (GW)": in_gw - out_gw,
            "In (Season)": in_season,
            "Out (Season)": out_season,
            "Net (Season)": in_season - out_season,
            "Owned %": float(el.get("selected_by_percent", 0) or 0),
            "GW Pts": el.get("event_points", 0),
            "Total Pts": el.get("total_points", 0),
        })
    return pd.DataFrame(rows)


def _horizontal_bar(df: pd.DataFrame, x_col: str, color: str, title: str) -> None:
    fig = px.bar(
        df, x=x_col, y="Player", orientation="h",
        color_discrete_sequence=[color],
        text=x_col,
    )
    fig.update_traces(textposition="outside", texttemplate="%{text:,}")
    fig.update_layout(
        template="plotly_white",
        height=380,
        title=title,
        title_font=dict(size=14),
        xaxis_title="",
        yaxis_title="",
        yaxis=dict(categoryorder="total ascending"),
        showlegend=False,
        margin=dict(t=40, b=20, l=10, r=60),
    )
    st.plotly_chart(fig, use_container_width=True)


def render_global_transfers(context: dict) -> None:
    """Display global transfer trends."""
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]
    df = _build_transfer_df(bootstrap_data)

    tab_gw, tab_season = st.tabs([f"GW {current_gw} Transfers", "Season Transfers"])

    # ── This GW ───────────────────────────────────────────────────────────────
    with tab_gw:
        total_in = int(df["In (GW)"].sum())
        total_out = int(df["Out (GW)"].sum())
        top_net = df.loc[df["Net (GW)"].idxmax()]
        top_sold = df.loc[df["Out (GW)"].idxmax()]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Total Transfers In", f"{total_in:,}", f"GW {current_gw}")
        with col2:
            metric_card("Total Transfers Out", f"{total_out:,}", f"GW {current_gw}")
        with col3:
            metric_card("Biggest Net Gain", top_net["Player"], f"+{int(top_net['Net (GW)']):,}", "positive")
        with col4:
            metric_card("Most Sold", top_sold["Player"], f"{int(top_sold['Out (GW)']):,} outs", "negative")

        section_header("Most Transferred In / Out", f"Top 10 players by transfer activity — GW {current_gw}")

        col_in, col_out = st.columns(2)
        with col_in:
            top_in = df.nlargest(10, "In (GW)")[["Player", "Team", "Pos", "Price", "In (GW)", "GW Pts", "Owned %"]].copy()
            _horizontal_bar(top_in, "In (GW)", "#16a34a", "Top Transfers In")

        with col_out:
            top_out = df.nlargest(10, "Out (GW)")[["Player", "Team", "Pos", "Price", "Out (GW)", "GW Pts", "Owned %"]].copy()
            _horizontal_bar(top_out, "Out (GW)", "#dc2626", "Top Transfers Out")

        section_header("Net Transfer Table", "Biggest movers this gameweek")
        net_df = df[df["Net (GW)"] != 0].nlargest(30, "Net (GW)")[
            ["Player", "Team", "Pos", "Price", "In (GW)", "Out (GW)", "Net (GW)", "GW Pts", "Owned %"]
        ]
        max_gw_tf = int(df["In (GW)"].max()) if not df.empty else 1
        st.dataframe(
            net_df, hide_index=True, use_container_width=True,
            column_config={
                "In (GW)": st.column_config.ProgressColumn("In (GW)", min_value=0, max_value=max_gw_tf, format="%d"),
                "Out (GW)": st.column_config.ProgressColumn("Out (GW)", min_value=0, max_value=max_gw_tf, format="%d"),
                "Price": st.column_config.NumberColumn("Price", format="£%.1f"),
                "Owned %": st.column_config.NumberColumn("Owned %", format="%.1f%%"),
            },
        )

    # ── Season ────────────────────────────────────────────────────────────────
    with tab_season:
        season_in = int(df["In (Season)"].sum())
        season_out = int(df["Out (Season)"].sum())
        top_season_net = df.loc[df["Net (Season)"].idxmax()]
        top_season_sold = df.loc[df["Out (Season)"].idxmax()]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            metric_card("Season Transfers In", f"{season_in:,}")
        with col2:
            metric_card("Season Transfers Out", f"{season_out:,}")
        with col3:
            metric_card("Biggest Season Gain", top_season_net["Player"], f"+{int(top_season_net['Net (Season)']):,}", "positive")
        with col4:
            metric_card("Most Sold (Season)", top_season_sold["Player"], f"{int(top_season_sold['Out (Season)']):,} outs", "negative")

        section_header("Most Transferred In / Out", "Top 10 players by season transfer activity")

        col_in, col_out = st.columns(2)
        with col_in:
            top_in_s = df.nlargest(10, "In (Season)")[["Player", "Team", "Pos", "Price", "In (Season)", "Total Pts"]].copy()
            _horizontal_bar(top_in_s, "In (Season)", "#16a34a", "Top Transfers In (Season)")
        with col_out:
            top_out_s = df.nlargest(10, "Out (Season)")[["Player", "Team", "Pos", "Price", "Out (Season)", "Total Pts"]].copy()
            _horizontal_bar(top_out_s, "Out (Season)", "#dc2626", "Top Transfers Out (Season)")
