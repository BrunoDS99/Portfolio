import random
from typing import List, Tuple, Optional
from models import Symbol, Position, AIDifficulty
from board import Board

class BaseAI:
    """Base class for AI players."""
    
    def __init__(self, symbol: Symbol, difficulty: AIDifficulty):
        self.symbol = symbol
        self.difficulty = difficulty
        self.opponent = Symbol.O if symbol == Symbol.X else Symbol.X
    
    def get_move(self, board: Board) -> Optional[Position]:
        """Get AI Move."""
        empty = board.get_empty_positions()
        if not empty:
            return None
        
        if self.difficulty == AIDifficulty.EASY:
            return self._easy_move(empty)
        elif self.difficulty == AIDifficulty.MEDIUM:
            return self._medium_move(board, empty)
        else: #hard
            return self._hard_move(board, empty)
    
    def _easy_move(self, empty: List[Position]) -> Position:
        """Random move for easy difficulty."""
        return random.choice(empty)
    
    def _medium_move(self, board: Board, empty: List[Position]) -> Position:
        """Medium difficulty: block opponent or win if possible."""
        # Check for winning move
        for pos in empty:
            board.set_cell(pos, self.symbol)
            if board.check_winner() == self.symbol:
                board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
                return pos
            board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
            
        # Check for blocking opponent's winning move
        for pos in empty:
            board.set_cell(pos, self.opponent)
            if board.check_winner() == self.opponent:
                board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
                return pos
            board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo

        # take center if available
        center = Position(1, 1)
        if center in empty:
            return center
        
        # take a corner if available
        corners = [Position(0, 0), Position(0, 2), Position(2, 0), Position(2, 2)]
        available_corners = [c for c in corners if c in empty]
        if available_corners:
            return random.choice(available_corners)

        # fallback to random move
        return random.choice(empty)
    
    def _hard_move(self, board: Board, empty: List[Position]) -> Position:
        """Hard difficulty: minimax algorithm"""
        
        best_score = float('-inf')
        best_move = empty[0]
        
        for pos in empty:
            board.set_cell(pos, self.symbol)
            score = self._minimax(board, 0, False)
            board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
            
            if score > best_score:
                best_score = score
                best_move = pos
            
            return best_move
        
        def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> float:
            """Minimax algorithm for hard difficulty."""
            
            #check terminal state
            winner = board.check_winner()
            if winner == self.symbol:
                return 10 - depth
            elif winner == self.opponent:
                return depth - 10
            elif board.is_full():
                return 0
            
            if is_maximizing:
                max_eval = float('-inf')
                for pos in board.get_empty_positions():
                    board.set_cell(pos, self.symbol)
                    eval = self._minimax(board, depth + 1, False)
                    board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
                    max_eval = max(max_eval, eval)
                return max_eval
            else:
                min_eval = float('inf')
                for pos in board.get_empty_positions():
                    board.set_cell(pos, self.opponent)
                    eval = self._minimax(board, depth + 1, True)
                    board.grid[pos.row][pos.col] = Symbol.EMPTY  # Undo
                    min_eval = min(min_eval, eval)
                return min_eval