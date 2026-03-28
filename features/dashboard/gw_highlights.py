"""GW Highlights section for dashboard."""

from collections import Counter

import streamlit as st

import fpl_api
from features.ui import metric_card


def render_gw_highlights(context: dict) -> None:
    """Display GW highlights as styled metric cards."""
    standings = context["standings"]
    bootstrap_data = context["bootstrap_data"]
    current_gw = context["current_gw"]

    # Calculate biggest rise and drop
    biggest_rise = None
    biggest_drop = None
    max_rise = 0
    max_drop = 0

    for s in standings:
        if s["last_rank"] == 0:
            continue
        change = s["last_rank"] - s["rank"]
        if change > max_rise:
            max_rise = change
            biggest_rise = s
        if change < max_drop:
            max_drop = change
            biggest_drop = s

    highest_gw = max(standings, key=lambda s: s["event_total"]) if standings else None
    best_captain = _get_best_captain(standings, bootstrap_data, current_gw)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if biggest_rise:
            metric_card(
                "Biggest Rise",
                biggest_rise["entry_name"],
                f"▲ +{max_rise} places",
                "positive",
            )
        else:
            metric_card("Biggest Rise", "—", "No movement", "neutral")

    with col2:
        if biggest_drop:
            metric_card(
                "Biggest Drop",
                biggest_drop["entry_name"],
                f"▼ {abs(max_drop)} places",
                "negative",
            )
        else:
            metric_card("Biggest Drop", "—", "No movement", "neutral")

    with col3:
        if highest_gw:
            metric_card(
                "Highest GW Score",
                highest_gw["entry_name"],
                f"{highest_gw['event_total']} pts",
                "positive",
            )
        else:
            metric_card("Highest GW Score", "—", "No data", "neutral")

    with col4:
        if best_captain:
            captain_name, captain_pts, captain_count = best_captain
            metric_card(
                "Best Captain",
                captain_name,
                f"{captain_pts} pts · {captain_count} manager{'s' if captain_count > 1 else ''}",
                "positive",
            )
        else:
            metric_card("Best Captain", "—", "No data", "neutral")


def _get_best_captain(standings: list, bootstrap_data: dict, current_gw: int) -> tuple | None:
    """Find the captain with highest points this GW."""
    player_points = {}
    for element in bootstrap_data.get("elements", []):
        player_points[element["id"]] = element.get("event_points", 0)

    captain_picks = []
    for s in standings:
        try:
            picks = fpl_api.get_manager_picks(s["entry"], current_gw)
            for pick in picks.get("picks", []):
                if pick.get("is_captain"):
                    captain_id = pick["element"]
                    pts = player_points.get(captain_id, 0)
                    captain_picks.append((captain_id, pts))
                    break
        except Exception:
            pass

    if not captain_picks:
        return None

    best_id, best_pts = max(captain_picks, key=lambda x: x[1])
    captain_counts = Counter(c[0] for c in captain_picks)
    count = captain_counts[best_id]
    captain_name = fpl_api.get_player_name(best_id, bootstrap_data)

    return captain_name, best_pts, count
