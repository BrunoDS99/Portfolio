import json
import os
from models import GameStats

def save_stats(stats: GameStats, filename: str = 'stats.json') -> None:
    """Save statistics to file"""
    
    data = {
        "total_games": stats.total_games,
        "x_wins": stats.x_wins,
        "o_wins": stats.o_wins,
        "draws": stats.draws
    }

    with open(filename, 'w') as f:
        json.dump(data, f)

def load_stats(filename: str = 'stats.json') -> GameStats:
    """Load statistics from file."""
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
            stats = GameStats()
            stats.total_games = data.get("total_games", 0)
            stats.x_wins = data.get("x_wins", 0)
            stats.o_wins = data.get("o_wins", 0)
            stats.draws = data.get("draws", 0)
            return stats
    return GameStats()