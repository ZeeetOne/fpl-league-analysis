"""Shared data loading utilities for FPL League Analysis."""

import streamlit as st

import fpl_api
from config import LEAGUE_ID


@st.cache_data(ttl=300)
def load_all_data():
    """Load all required data."""
    standings = fpl_api.get_league_standings(LEAGUE_ID)
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


def get_league_context():
    """Helper to get common data needed by most pages."""
    standings_data, bootstrap_data = load_all_data()
    league_info = standings_data.get("league", {})
    standings = standings_data.get("standings", {}).get("results", [])
    current_gw = fpl_api.get_current_gameweek(bootstrap_data)
    entry_ids = tuple(s["entry"] for s in standings)
    return {
        "league_info": league_info,
        "standings": standings,
        "bootstrap_data": bootstrap_data,
        "current_gw": current_gw,
        "entry_ids": entry_ids,
    }
