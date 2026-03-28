"""Global FPL feature modules."""

from .season_stats import render_season_stats
from .player_rankings import render_player_rankings
from .global_transfers import render_global_transfers
from .global_ownership import render_global_ownership

__all__ = [
    "render_season_stats",
    "render_player_rankings",
    "render_global_transfers",
    "render_global_ownership",
]
