"""Shared data loading utilities for FPL League Analysis."""

import streamlit as st

import fpl_api


@st.cache_data(ttl=300)
def load_all_data(league_id: int):
    """Load all required data for a given league."""
    standings = fpl_api.get_league_standings(league_id)
    bootstrap = fpl_api.get_bootstrap_data()
    return standings, bootstrap


@st.cache_data(ttl=300)
def load_manager_entries(entry_ids: tuple):
    """Load entry info for all managers (includes free transfers)."""
    entries = {}
    for entry_id in entry_ids:
        try:
            entries[entry_id] = fpl_api.get_manager_entry(entry_id)
        except Exception:
            entries[entry_id] = None
    return entries


@st.cache_data(ttl=300)
def load_manager_histories(entry_ids: tuple):
    """Load history for all managers."""
    histories = {}
    for entry_id in entry_ids:
        try:
            histories[entry_id] = fpl_api.get_manager_history(entry_id)
        except Exception:
            histories[entry_id] = None
    return histories


@st.cache_data(ttl=300)
def load_manager_transfers(entry_ids: tuple):
    """Load transfers for all managers."""
    transfers = {}
    for entry_id in entry_ids:
        try:
            transfers[entry_id] = fpl_api.get_manager_transfers(entry_id)
        except Exception:
            transfers[entry_id] = []
    return transfers


@st.cache_data(ttl=300)
def load_manager_picks(entry_ids: tuple, gameweek: int):
    """Load picks for all managers for a specific gameweek."""
    picks = {}
    for entry_id in entry_ids:
        try:
            picks[entry_id] = fpl_api.get_manager_picks(entry_id, gameweek)
        except Exception:
            picks[entry_id] = None
    return picks


def get_rank_change_indicator(current: int, previous: int) -> str:
    """Return arrow indicator for rank change."""
    if previous == 0:
        return "-"
    diff = previous - current
    if diff > 0:
        return f"↑{diff}"
    elif diff < 0:
        return f"↓{abs(diff)}"
    return "-"


def _get_manager_range(total: int):
    """Resolve the current manager display range from session state."""
    display = st.session_state.get("manager_display", "Top 10")
    if display == "Top 10":
        return 0, min(10, total)
    if display == "Top 20":
        return 0, min(20, total)
    if display == "All":
        return 0, total
    # Custom
    start = max(1, int(st.session_state.get("custom_start", 1)))
    end = max(start, int(st.session_state.get("custom_end", 20)))
    return start - 1, min(end, total)


def get_league_context():
    """Helper to get common data needed by most pages."""
    league_id = int(st.session_state.get("league_id") or 0)
    if not league_id:
        from features.ui import welcome_screen
        welcome_screen()
    standings_data, bootstrap_data = load_all_data(league_id)
    league_info = standings_data.get("league", {})
    all_standings = standings_data.get("standings", {}).get("results", [])
    current_gw = fpl_api.get_current_gameweek(bootstrap_data)

    start, end = _get_manager_range(len(all_standings))
    standings = all_standings[start:end]
    entry_ids = tuple(s["entry"] for s in standings)

    return {
        "league_info": league_info,
        "standings": standings,
        "bootstrap_data": bootstrap_data,
        "current_gw": current_gw,
        "entry_ids": entry_ids,
    }


def get_global_context():
    """Return bootstrap data and current GW — no league ID required."""
    bootstrap_data = fpl_api.get_bootstrap_data()
    current_gw = fpl_api.get_current_gameweek(bootstrap_data)
    return {
        "bootstrap_data": bootstrap_data,
        "current_gw": current_gw,
    }
