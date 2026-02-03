"""Squad selection logic for best performers."""

POSITION_NAMES = {
    1: "goalkeeper",
    2: "defender",
    3: "midfielder",
    4: "forward"
}

SQUAD_COMPOSITION = {
    "goalkeeper": 2,
    "defender": 5,
    "midfielder": 5,
    "forward": 3
}


def merge_player_data(bootstrap_data: dict, live_data: dict) -> list:
    """Merge bootstrap metadata with live performance data.

    Args:
        bootstrap_data: Bootstrap data containing player metadata and teams.
        live_data: Live gameweek data containing player performance stats.

    Returns:
        List of dicts with {id, web_name, element_type, team, team_code, total_points, price}
    """
    # Get all players from bootstrap
    players = bootstrap_data.get("elements", [])

    # Build team lookup with both short_name and team_code
    teams = {}
    for t in bootstrap_data.get("teams", []):
        teams[t["id"]] = {
            "short_name": t["short_name"],
            "code": t["code"]
        }

    # Build points lookup from live data
    points_lookup = {}
    for element in live_data.get("elements", []):
        points_lookup[element["id"]] = element.get("stats", {}).get("total_points", 0)

    # Merge
    merged = []
    for player in players:
        team_info = teams.get(player["team"], {"short_name": "Unknown", "code": 0})
        # Convert price from tenths to actual price (e.g., 48 -> £4.8m)
        price = player.get("now_cost", 0) / 10
        merged.append({
            "id": player["id"],
            "web_name": player["web_name"],
            "element_type": player["element_type"],
            "team": team_info["short_name"],
            "team_code": team_info["code"],
            "total_points": points_lookup.get(player["id"], 0),
            "price": price
        })

    return merged


def select_best_squad(all_players: list) -> dict:
    """Select top N players by position based on total_points.

    Args:
        all_players: List of player dicts with element_type and total_points.

    Returns:
        Dict with keys: goalkeepers, defenders, midfielders, forwards
    """
    # Group by position
    by_position = {
        "goalkeeper": [],
        "defender": [],
        "midfielder": [],
        "forward": []
    }

    for player in all_players:
        position = POSITION_NAMES.get(player["element_type"])
        if position and player["total_points"] > 0:  # Only include players who scored
            by_position[position].append(player)

    # Sort by points and take top N
    squad = {}
    for position, players in by_position.items():
        # Sort descending by total_points
        sorted_players = sorted(players, key=lambda x: x["total_points"], reverse=True)
        # Take top N for this position
        n = SQUAD_COMPOSITION[position]
        squad[f"{position}s"] = sorted_players[:n]  # 'goalkeepers', 'defenders', etc.

    return squad
