"""Formation view rendering for best squad."""

import streamlit as st

from features.best_squad.squad_selector import merge_player_data, select_best_squad


def _get_points_color(points: int) -> str:
    """Get color based on points scored.

    Args:
        points: Total points scored.

    Returns:
        Hex color string.
    """
    if points >= 10:
        return "#00ff87"  # Bright green (FPL style)
    elif points >= 5:
        return "#ffffff"  # White
    else:
        return "#e90052"  # Red (FPL style)


def _render_player_card_html(player: dict) -> str:
    """Generate HTML for a player card with FPL-style shirt.

    Args:
        player: Player dict with web_name, team, team_code, total_points, price.

    Returns:
        HTML string for the player card.
    """
    points_color = _get_points_color(player["total_points"])
    shirt_url = f"https://fantasy.premierleague.com/dist/img/shirts/standard/shirt_{player['team_code']}-66.png"
    price = player.get("price", 0)
    price_str = f"£{price:.1f}m"

    html = f"""<div style='text-align: center; padding: 0.5rem; flex: 1; display: flex; flex-direction: column; align-items: center;'>
        <div style='background-color: rgba(0, 0, 0, 0.7); color: white; font-size: 0.75rem; font-weight: 600; padding: 0.2rem 0.5rem; border-radius: 4px; margin-bottom: 0.5rem;'>{price_str}</div>
        <div style='position: relative; display: inline-block;'>
            <img src="{shirt_url}" alt="{player['team']}" style='width: 80px; height: 80px; display: block;' onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
            <div style='display: none; width: 80px; height: 80px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; line-height: 80px; color: white; font-weight: bold; font-size: 1.5rem;'>{player['team'][:3]}</div>
        </div>
        <div style='background-color: {points_color}; color: #37003c; font-weight: bold; font-size: 0.9rem; width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.3);'>{player['total_points']}</div>
        <div style='font-size: 0.85rem; font-weight: 600; color: white; background-color: #37003c; padding: 0.25rem 0.5rem; border-radius: 2px; margin-top: 0.5rem;'>{player['web_name']}</div>
        <div style='font-size: 0.75rem; font-weight: 500; color: #37003c; background-color: white; padding: 0.15rem 0.4rem; border-radius: 2px; margin-top: 0.3rem;'>{player['team']}</div>
    </div>"""

    return html


def _render_forwards_row_html(forwards: list) -> str:
    """Generate HTML for forwards row (3 players centered).

    Args:
        forwards: List of forward player dicts.

    Returns:
        HTML string for forwards row.
    """
    if len(forwards) < 3:
        return ""

    cards = [_render_player_card_html(forwards[i]) for i in range(3)]
    cards_html = "".join(cards)

    return f"<div style='display: flex; justify-content: center; gap: 1rem; margin: 1rem 0;'>{cards_html}</div>"


def _render_midfielders_row_html(midfielders: list) -> str:
    """Generate HTML for midfielders row (5 players).

    Args:
        midfielders: List of midfielder player dicts.

    Returns:
        HTML string for midfielders row.
    """
    if len(midfielders) < 5:
        return ""

    cards = [_render_player_card_html(midfielders[i]) for i in range(5)]
    cards_html = "".join(cards)

    return f"<div style='display: flex; justify-content: center; gap: 0.5rem; margin: 1rem 0;'>{cards_html}</div>"


def _render_defenders_row_html(defenders: list) -> str:
    """Generate HTML for defenders row (5 players).

    Args:
        defenders: List of defender player dicts.

    Returns:
        HTML string for defenders row.
    """
    if len(defenders) < 5:
        return ""

    cards = [_render_player_card_html(defenders[i]) for i in range(5)]
    cards_html = "".join(cards)

    return f"<div style='display: flex; justify-content: center; gap: 0.5rem; margin: 1rem 0;'>{cards_html}</div>"


def _render_goalkeepers_row_html(goalkeepers: list) -> str:
    """Generate HTML for goalkeepers row (2 players centered).

    Args:
        goalkeepers: List of goalkeeper player dicts.

    Returns:
        HTML string for goalkeepers row.
    """
    if len(goalkeepers) < 2:
        return ""

    cards = [_render_player_card_html(goalkeepers[i]) for i in range(2)]
    cards_html = "".join(cards)

    return f"<div style='display: flex; justify-content: center; gap: 2rem; margin: 1rem 0;'>{cards_html}</div>"


def _render_summary_stats(squad: dict) -> None:
    """Display aggregate stats.

    Args:
        squad: Squad dict with all positions.
    """
    # Calculate totals
    all_players = []
    for position in squad.values():
        all_players.extend(position)

    if not all_players:
        return

    total_points = sum(p["total_points"] for p in all_players)
    highest = max(p["total_points"] for p in all_players)
    avg = round(total_points / len(all_players), 1)

    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Squad Points", total_points)
    with col2:
        st.metric("Highest Scorer", highest)
    with col3:
        st.metric("Average Points", avg)


def render_best_squad(bootstrap_data: dict, live_data: dict, selected_gw: int) -> None:
    """Render best squad in formation layout.

    Args:
        bootstrap_data: Bootstrap data containing player metadata.
        live_data: Live gameweek data containing player performance.
        selected_gw: Selected gameweek number.
    """
    with st.spinner("Building best squad..."):
        # Merge data
        all_players = merge_player_data(bootstrap_data, live_data)

        # Check if any players scored
        players_with_points = [p for p in all_players if p["total_points"] > 0]
        if not players_with_points:
            st.info("No player performance data available for this gameweek.")
            return

        # Select squad
        squad = select_best_squad(all_players)

    # Display summary stats
    _render_summary_stats(squad)

    st.divider()

    # Generate HTML for each formation row
    goalkeepers_html = _render_goalkeepers_row_html(squad.get("goalkeepers", []))
    defenders_html = _render_defenders_row_html(squad.get("defenders", []))
    midfielders_html = _render_midfielders_row_html(squad.get("midfielders", []))
    forwards_html = _render_forwards_row_html(squad.get("forwards", []))

    # Check if we have all formations
    if not all([goalkeepers_html, defenders_html, midfielders_html, forwards_html]):
        st.info("Not enough players with points in this gameweek to form a complete squad.")
        return

    # Render complete formation with pitch background in one HTML block
    formation_html = f"""<div style='background-image: url("https://fantasy.premierleague.com/assets/pitch-graphic-t77-OTdp.svg"); background-size: cover; background-position: center; background-repeat: no-repeat; border-radius: 10px; padding: 3rem 6rem; min-height: 850px; display: flex; flex-direction: column; justify-content: space-around;'>
        {goalkeepers_html}
        {defenders_html}
        {midfielders_html}
        {forwards_html}
    </div>"""

    st.markdown(formation_html, unsafe_allow_html=True)
