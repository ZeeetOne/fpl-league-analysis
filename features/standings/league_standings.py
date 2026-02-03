"""League standings table with configurable columns."""

import pandas as pd
import streamlit as st

import fpl_api
from data_loader import get_rank_change_indicator


# Column presets
BASIC_COLUMNS = ["Rank", "Change", "Chip", "Team", "Manager", "GW Pts", "Total Pts"]
ALL_COLUMNS = [
    "Rank", "Change", "Team", "Manager", "GW Pts", "Total Pts",
    "Behind", "High", "Low", "Chips", "Chips Left",
    "TF Season", "TF GW", "Hits Season", "Hits GW",
    "Captain", "Capt Pts"
]

# All available chips in FPL (each can be used once per half-season)
ALL_CHIPS = {"wildcard", "freehit", "bboost", "3xc"}
FIRST_HALF_DEADLINE_GW = 19  # Chips must be used before GW20 for first half


def render_standings(
    context: dict,
    histories: dict = None,
    transfers: dict = None,
    picks: dict = None,
    columns: list = None,
    limit: int = None,
) -> None:
    """Display league standings table with configurable columns.

    Args:
        context: League context containing standings and bootstrap data.
        histories: Dictionary of manager histories keyed by entry ID.
        transfers: Dictionary of manager transfers keyed by entry ID.
        picks: Dictionary of manager picks for current GW keyed by entry ID.
        columns: List of column names to display. None for all columns.
        limit: Maximum number of rows to display. None for all rows.
    """
    all_standings = context["standings"]
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    standings = all_standings[:limit] if limit else all_standings

    # Determine which columns to show
    display_columns = columns if columns else ALL_COLUMNS

    # Build player points lookup (needed for captain info)
    player_points = {}
    if "Captain" in display_columns or "Capt Pts" in display_columns:
        for element in bootstrap_data.get("elements", []):
            player_points[element["id"]] = element.get("event_points", 0)

    # Get leader's total points for "Behind" column
    leader_total = all_standings[0]["total"] if all_standings else 0

    data = []
    for s in standings:
        entry_id = s["entry"]
        history = (histories or {}).get(entry_id, {}) or {}
        transfer_list = (transfers or {}).get(entry_id, [])
        manager_picks = (picks or {}).get(entry_id, {}) or {}

        row = {}

        # Always compute these base values
        row["Rank"] = s["rank"]
        row["Change"] = get_rank_change_indicator(s["rank"], s["last_rank"])
        row["Team"] = s["entry_name"]
        row["Manager"] = s["player_name"]
        row["GW Pts"] = s["event_total"]
        row["Total Pts"] = s["total"]

        # Chip (current GW only)
        if "Chip" in display_columns:
            row["Chip"] = _get_current_gw_chip(history.get("chips", []), current_gw)

        # Chips (all season)
        if "Chips" in display_columns:
            row["Chips"] = _format_all_chips(history.get("chips", []))

        # Points Behind Leader
        if "Behind" in display_columns:
            behind = leader_total - s["total"]
            row["Behind"] = f"-{behind}" if behind > 0 else "0"

        # High, Low - from history
        gw_points = [gw.get("points", 0) for gw in history.get("current", [])]

        if "High" in display_columns:
            row["High"] = max(gw_points) if gw_points else 0

        if "Low" in display_columns:
            row["Low"] = min(gw_points) if gw_points else 0

        # Chips Left
        if "Chips Left" in display_columns:
            row["Chips Left"] = _get_chips_remaining(history.get("chips", []))

        # Transfer columns
        if "TF Season" in display_columns:
            row["TF Season"] = len(transfer_list)

        if "TF GW" in display_columns:
            row["TF GW"] = sum(1 for t in transfer_list if t.get("event") == current_gw)

        # Hits columns
        gw_history_data = history.get("current", [])

        if "Hits Season" in display_columns:
            row["Hits Season"] = sum(gw.get("event_transfers_cost", 0) for gw in gw_history_data)

        if "Hits GW" in display_columns:
            gw_history = next(
                (gw for gw in gw_history_data if gw.get("event") == current_gw),
                {}
            )
            row["Hits GW"] = gw_history.get("event_transfers_cost", 0)

        # Captain info
        if "Captain" in display_columns or "Capt Pts" in display_columns:
            captain_name, captain_pts = _get_captain_info(
                manager_picks, bootstrap_data, player_points
            )
            if "Captain" in display_columns:
                row["Captain"] = captain_name
            if "Capt Pts" in display_columns:
                row["Capt Pts"] = captain_pts

        data.append(row)

    df = pd.DataFrame(data)

    # Reorder columns to match display_columns order
    ordered_cols = [col for col in display_columns if col in df.columns]
    df = df[ordered_cols]

    st.dataframe(df, width="stretch", hide_index=True)


def _get_current_gw_chip(chips: list, current_gw: int) -> str:
    """Get chip used in current gameweek only."""
    chip_abbrev = {
        "wildcard": "WC",
        "freehit": "FH",
        "bboost": "BB",
        "3xc": "TC",
    }

    for chip in chips:
        if chip.get("event") == current_gw:
            name = chip.get("name", "").lower()
            return chip_abbrev.get(name, name.upper())

    return "-"


def _format_all_chips(chips: list) -> str:
    """Format all chips used this season with GW numbers."""
    if not chips:
        return "-"

    chip_abbrev = {
        "wildcard": "WC",
        "freehit": "FH",
        "bboost": "BB",
        "3xc": "TC",
    }

    chip_entries = []
    for chip in chips:
        name = chip.get("name", "").lower()
        gw = chip.get("event", "?")
        abbrev = chip_abbrev.get(name, name.upper())
        chip_entries.append(f"{abbrev}({gw})")

    return ", ".join(chip_entries) if chip_entries else "-"


def _get_captain_info(
    picks_data: dict,
    bootstrap_data: dict,
    player_points: dict,
) -> tuple:
    """Get captain name and points from picks data."""
    if not picks_data:
        return "-", 0

    for pick in picks_data.get("picks", []):
        if pick.get("is_captain"):
            captain_id = pick["element"]
            captain_name = fpl_api.get_player_name(captain_id, bootstrap_data)
            captain_pts = player_points.get(captain_id, 0)
            return captain_name, captain_pts

    return "-", 0


def _get_chips_remaining(used_chips: list) -> str:
    """Get remaining chips by half (all chips can be used once per half)."""
    chip_abbrev = {
        "wildcard": "WC",
        "freehit": "FH",
        "bboost": "BB",
        "3xc": "TC",
    }
    all_chip_names = ["wildcard", "freehit", "bboost", "3xc"]

    # Track chips used in each half
    first_half_used = set()
    second_half_used = set()

    for chip in used_chips:
        name = chip.get("name", "").lower()
        gw = chip.get("event", 0)
        if gw <= FIRST_HALF_DEADLINE_GW:
            first_half_used.add(name)
        else:
            second_half_used.add(name)

    # Get remaining chips for each half
    first_half_remaining = [chip_abbrev[c] for c in all_chip_names if c not in first_half_used]
    second_half_remaining = [chip_abbrev[c] for c in all_chip_names if c not in second_half_used]

    # Format output
    first_str = ", ".join(first_half_remaining) if first_half_remaining else "-"
    second_str = ", ".join(second_half_remaining) if second_half_remaining else "-"

    if first_half_remaining == list(chip_abbrev.values()):
        first_str = "All"
    if second_half_remaining == list(chip_abbrev.values()):
        second_str = "All"

    return f"1st: {first_str} · 2nd: {second_str}"
