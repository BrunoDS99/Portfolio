"""
All dataclass models for Tic Tac Toe.
Using dataclasses for clean, immutable data structures.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, List, Tuple
from datetime import datetime


class Symbol(Enum):
    """Enum for Tic Tac Toe symbols."""
    EMPTY = " "
    X = "X"
    O = "O"
    
    def __str__(self):
        return self.value

class GameMode(Enum):
    """Enum for game states."""
    PVP = 'Player vs Player'
    PVE = 'Player vs Environment'
    EVE = 'Environment vs Environment'

class AIDifficulty(Enum):
    """Enum for AI difficulty levels."""
    EASY = 'Easy'
    MEDIUM = 'Medium'
    HARD = 'Hard'
    
class GameStatus(Enum):
    """Enum for game status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"
    ABANDONED = "abandoned"
    
@dataclass
class Position:
    """Class for a position on the Tic Tac Toe board."""
    row: int
    col: int
    
    def __post_init__(self):
        """Validate position is within bounds."""
        if not (0 <= self.row < 3 and 0 <= self.col < 3):
            raise ValueError(f"Invalid position: ({self.row}, {self.col})")
    
    def to_index(self) -> int:
        """Convert position to a single index (0-8)."""
        return self.row * 3 + self.col
    
    @classmethod
    def from_index(cls, index: int) -> 'Position':
        """Create a Position from a single index (0-8)."""
        if not (0 <= index < 9):
            raise ValueError(f"Invalid index: {index}")
        return cls(index // 3, index % 3)
    
@dataclass
class Player:
    """Class for a player in Tic Tac Toe."""
    name: str
    symbol: Symbol
    is_ai: bool = False
    wins: int = 0
    losses: int = 0
    draws: int = 0
    
    def add_win(self) -> None:
        """Increment win count."""
        self.wins += 1
    
    def add_loss(self) -> None:
        """Increment loss count."""
        self.losses += 1
    
    def add_draw(self) -> None:
        """Increment draw count."""
        self.draws += 1
        
    @property
    def total_games(self) -> int:
        """Return total games played."""
        return self.wins + self.losses + self.draws
    
    @property
    def win_rate(self) -> float:
        """Return win rate as a percentage."""
        total = self.total_games
        return (self.wins / total) * 100 if total > 0 else 0.0

@dataclass 
class Move:
    """Represents a move in the game."""
    position: Position
    symbol: Symbol
    player_name: str
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self):
        return f"{self.player_name} ({self.symbol}) → ({self.position.row}, {self.position.col})"

@dataclass
class GameStats:
    """Overall game statistics."""
    total_games: int = 0
    x_wins: int = 0
    o_wins: int = 0
    draws: int = 0
    players: List[Player] = field(default_factory=list)
    move_history: List[Move] = field(default_factory=list)
    
    def add_game_result(self, winner: Optional[Symbol]) -> None:
        """Update game statistics based on the result."""
        self.total_games += 1
        if winner == Symbol.X:
            self.x_wins += 1
        elif winner == Symbol.O:
            self.o_wins += 1
        else:
            self.draws += 1
            
    
    @property
    def x_win_rate(self) -> float:
        """X win rate."""
        if self.total_games == 0:
            return 0.0
        return (self.x_wins / self.total_games) * 100
    
    @property
    def o_win_rate(self) -> float:
        """O win rate."""
        if self.total_games == 0:
            return 0.0
        return (self.o_wins / self.total_games) * 100
    
    @property
    def draw_rate(self) -> float:
        """Draw rate."""
        if self.total_games == 0:
            return 0.0
        return (self.draws / self.total_games) * 100
        
@dataclass
class GameConfig:
    """Game configuration settings."""
    mode: GameMode = GameMode.PVP
    ai_difficulty: AIDifficulty = AIDifficulty.MEDIUM
    player1_name: str = "Player 1"
    player2_name: str = "Player 2"
    sound_enabled: bool = True
    animations_enabled: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "mode": self.mode.value,
            "ai_difficulty": self.ai_difficulty.value,
            "player1_name": self.player1_name,
            "player2_name": self.player2_name,
            "sound_enabled": self.sound_enabled,
            "animations_enabled": self.animations_enabled
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'GameConfig':
        """Create from dictionary."""
        return cls(
            mode=GameMode(data.get("mode", "Player vs Player")),
            ai_difficulty=AIDifficulty(data.get("ai_difficulty", "medium")),
            player1_name=data.get("player1_name", "Player 1"),
            player2_name=data.get("player2_name", "Player 2"),
            sound_enabled=data.get("sound_enabled", True),
            animations_enabled=data.get("animations_enabled", True)
        )

@dataclass
class GameState:
    """Complete Game state"""
    board: any  # Forward reference to Board class
    players: List[Player]
    current_player_index: int = 0
    status: GameStatus = GameStatus.NOT_STARTED
    moves: List[Move] = field(default_factory=list)
    start_time: datetime = field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    
    @property
    def current_player(self) -> Player:
        """Get the current player."""
        return self.players[self.current_player_index]
    
    def switch_player(self) -> None:
        """Switch to the next player."""
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        
    def add_move(self, move: Move) -> None:
        """Add a move to the game state."""
        self.moves.append(move)
    
    def end_game(self, status: GameStatus) -> None:
        """End the game with a specific status."""
        self.status = status
        self.end_time = datetime.now()
        
    @property
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.status in {GameStatus.X_WINS, GameStatus.O_WINS, GameStatus.DRAW, GameStatus.ABANDONED}
    
    @property
    def duration(self) -> float:
        """Game duration in seconds."""
        if not self.end_time:
            return 0.0
        return (self.end_time - self.start_time).total_seconds()
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "players": [
                {"name": p.name, "symbol": p.symbol.value, "wins": p.wins}
                for p in self.players
            ],
            "status": self.status.value,
            "moves": [
                {
                    "player": m.player_name,
                    "symbol": m.symbol.value,
                    "row": m.position.row,
                    "col": m.position.col,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in self.moves
            ],
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration
        }
    
__all__ = [
    'Symbol',
    'GameMode', 
    'AIDifficulty',
    'GameStatus',
    'Position',
    'Player',
    'Move',
    'GameStats',
    'GameConfig',
    'GameState'
]