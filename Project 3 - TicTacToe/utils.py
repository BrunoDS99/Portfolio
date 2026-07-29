import json
import os
from models import GameStats


def get_stats_filepath(filename: str = 'stats.json') -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, filename)


def save_stats(stats: GameStats, filename: str = 'stats.json') -> None:
    """Save statistics to file"""
    
    filepath = get_stats_filepath()
    
    data = {
        "total_games": stats.total_games,
        "x_wins": stats.x_wins,
        "o_wins": stats.o_wins,
        "draws": stats.draws
    }

    with open(filepath, 'w') as f:
        json.dump(data, f)
    print(f"Stats saved to: {filepath}")

def load_stats(filename: str = 'stats.json') -> GameStats:
    """Load statistics from file."""
    
    filepath = get_stats_filepath(filename)
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            stats = GameStats()
            stats.total_games = data.get("total_games", 0)
            stats.x_wins = data.get("x_wins", 0)
            stats.o_wins = data.get("o_wins", 0)
            stats.draws = data.get("draws", 0)
            print(f"Stats loaded from: {filepath}")
            return stats
    return GameStats()