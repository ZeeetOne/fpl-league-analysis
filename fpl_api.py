"""FPL API client with caching."""

import requests
import streamlit as st

BASE_URL = "https://fantasy.premierleague.com/api"


class GameUpdatingError(Exception):
    """Raised when FPL API is updating before matches."""
    pass


def _make_request(url: str, timeout: int = 10) -> requests.Response:
    """Make a request and handle game updating state."""
    response = requests.get(url, timeout=timeout)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        if response.status_code == 503 and "updated" in response.text.lower():
            raise GameUpdatingError("The FPL game is currently being updated.")
        raise
    return response


@st.cache_data(ttl=300)
def get_league_standings(league_id: int) -> dict:
    """Fetch league standings."""
    url = f"{BASE_URL}/leagues-classic/{league_id}/standings/"
    response = _make_request(url)
    return response.json()


@st.cache_data(ttl=3600)
def get_bootstrap_data() -> dict:
    """Fetch bootstrap data (players, teams, gameweeks)."""
    url = f"{BASE_URL}/bootstrap-static/"
    response = _make_request(url)
    return response.json()


@st.cache_data(ttl=300)
def get_manager_entry(entry_id: int) -> dict:
    """Fetch manager's entry info (includes free transfers)."""
    url = f"{BASE_URL}/entry/{entry_id}/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_manager_history(entry_id: int) -> dict:
    """Fetch manager's gameweek history."""
    url = f"{BASE_URL}/entry/{entry_id}/history/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_manager_transfers(entry_id: int) -> list:
    """Fetch manager's transfer history."""
    url = f"{BASE_URL}/entry/{entry_id}/transfers/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(ttl=300)
def get_manager_picks(entry_id: int, gameweek: int) -> dict:
    """Fetch manager's picks for a specific gameweek."""
    url = f"{BASE_URL}/entry/{entry_id}/event/{gameweek}/picks/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def get_current_gameweek(bootstrap_data: dict) -> int:
    """Get the current gameweek number."""
    events = bootstrap_data.get("events", [])
    for event in events:
        if event.get("is_current"):
            return event["id"]
    # If no current GW, return the latest finished one
    for event in reversed(events):
        if event.get("finished"):
            return event["id"]
    return 1


def get_player_name(player_id: int, bootstrap_data: dict) -> str:
    """Get player name from ID."""
    elements = bootstrap_data.get("elements", [])
    for player in elements:
        if player["id"] == player_id:
            return player["web_name"]
    return "Unknown"


@st.cache_data(ttl=300)
def get_live_gameweek(gameweek: int) -> dict:
    """Fetch live data for a specific gameweek (player performance)."""
    url = f"{BASE_URL}/event/{gameweek}/live/"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()
