from typing import Optional, Tuple
from models import (
    Symbol, Position, Player, Move, GameState, GameStatus,
    GameMode, AIDifficulty, GameStats
)
from board import Board
from ai import BaseAI

class Game:
    """Main Game controller"""
    
    def __init__(self, mode: GameMode = GameMode.PVP, 
    difficulty: AIDifficulty = AIDifficulty.MEDIUM):    
        """Initialize game with mode and difficulty."""
        
        self.mode = mode
        self.difficulty = difficulty
        self.board = Board()
        self.stats = GameStats()
        self.ai = None
        self.ai1 = None
        self.ai2 = None
        self.game_state = None
        self.move_count = 0
        
        self._setup_players()
        
    def _setup_players(self) -> None:
        """Setup players depending on game mode."""
        
        if self.mode == GameMode.PVP:
            players = [
                Player(name="Player 1", symbol=Symbol.X),
                Player(name="Player 2", symbol=Symbol.O)
            ]
        elif self.mode == GameMode.PVE:
            players = [
                Player(name="Player", symbol=Symbol.X),
                Player(name="AI", symbol=Symbol.O, is_ai=True)
            ]
            self.ai = BaseAI(Symbol.O, self.difficulty)
            
        else: #EVE
            players = [
                Player(name="AI 1", symbol=Symbol.X, is_ai=True),
                Player(name="AI 2", symbol=Symbol.O, is_ai=True)
            ]
            self.ai = BaseAI(Symbol.X, self.difficulty)  # AI 1
            self.ai2 = BaseAI(Symbol.O, self.difficulty)  # AI 2
            
        self.game_state = GameState(
            board=self.board,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
    def make_move(self, position: Position) -> bool:
        """Make a move for the current player."""
        
        if self.game_state.is_game_over:
            return False
        
        current_player = self.game_state.current_player
        
        #check if valid mode
        if not self.board.is_empty(position):
            return False
        
        #make the move
        self.board.set_cell(position, current_player.symbol)
        
        #record move
        move = Move(position, current_player.symbol, current_player.name)
        self.game_state.add_move(move)
        self.move_count += 1
        
        # Check for winner
        winner = self.board.check_winner()
        if winner:
            self._handle_winner(winner)
            return True
        
        # Check for draw
        if self.board.is_full():
            self.game_state.end_game(GameStatus.DRAW)
            # Update stats for draw
            self.stats.add_game_result(None)
            # Add draw to both players
            for player in self.game_state.players:
                player.add_draw()
            return True
        
        #switch player
        self.game_state.switch_player()
        return True

    def _handle_winner(self, winner: Symbol) -> None:
        """Handle the end of the game when there's a winner."""
        for player in self.game_state.players:
            if player.symbol == winner:
                player.add_win()
            else:
                player.add_loss()
            
        #update game state
        if winner == Symbol.X:
            self.game_state.end_game(GameStatus.X_WINS)
        else:
            self.game_state.end_game(GameStatus.O_WINS)
            
        #update stats
        self.stats.add_game_result(winner)
        
        #store players in stats for tracking
        self.stats.players = self.game_state.players    
        
    def get_ai_move(self) -> Optional[Position]:
        """Get AI move if it's the AI's turn."""
        if self.game_state.is_game_over:
            return None
        
        current = self.game_state.current_player
        
        if not current.is_ai:
            return None
        
        if self.mode == GameMode.PVE:
            return self.ai.get_move(self.board)
        else: # EVE
            if current.symbol == Symbol.X:
                return self.ai.get_move(self.board)
            else:
                return self.ai2.get_move(self.board)
            
    def reset(self) -> None:
        """Reset the game to initial state."""
        self.board.reset()
        self.move_count = 0
       
        # Keep player names and symbols, but reset wins/losses
        players = self.game_state.players
        self.game_state = GameState(
            board=self.board,
            players=players,
            status=GameStatus.IN_PROGRESS
        )
        
    def get_stats(self) -> dict:
        """Get game statistics."""
        return {
            "players": self.game_state.players,
            "moves": len(self.game_state.moves),
            "duration": self.game_state.duration,
            "status": self.game_state.status.value
            }
        
    def get_player_stats(self) -> dict:
        """Get overall player statistics"""
        
        stats = {}
        for player in self.game_state.players:
            stats[player.name] = {
                "wins": player.wins,
                "losses": player.losses,
                "draws": player.draws,   
                "win_rate": player.win_rate
            }
            
        return stats
    
    def get_overall_stats(self) -> dict:
        """get overall stats"""
        return {
            "total_games": self.stats.total_games,
            "x_wins": self.stats.x_wins,
            "o_wins": self.stats.o_wins,
            "draws": self.stats.draws,
            "x_win_rate": self.stats.x_win_rate,
            "o_win_rate": self.stats.o_win_rate,
            "draw_rate": self.stats.draw_rate
        }
        