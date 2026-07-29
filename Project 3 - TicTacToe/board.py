"""
Board class using dataclass models.
"""

from typing import Optional, List, Tuple
from models import Symbol, Position

class Board:
    """Tic Tac Toe board."""
    
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """Reset board to empty."""
        self.grid = [[Symbol.EMPTY for _ in range(3)] for _ in range(3)]
    
    def get_cell(self, position: Position) -> Symbol:
        """Get cell at position."""
        return self.grid[position.row][position.col]
    
    def set_cell(self, position: Position, symbol: Symbol) -> bool:
        """
        Set cell to symbol.
        
        Returns:
            bool: True if successful, False if cell was occupied
        """
        if self.grid[position.row][position.col] != Symbol.EMPTY:
            return False
        
        self.grid[position.row][position.col] = symbol
        return True
    
    def is_empty(self, position: Position) -> bool:
        """Check if cell is empty."""
        return self.grid[position.row][position.col] == Symbol.EMPTY
    
    def is_full(self) -> bool:
        """Check if board is full."""
        for row in self.grid:
            if Symbol.EMPTY in row:
                return False
        return True
    
    def get_empty_positions(self) -> List[Position]:
        """Get all empty positions."""
        empty = []
        for row in range(3):
            for col in range(3):
                pos = Position(row, col)
                if self.is_empty(pos):
                    empty.append(pos)
        return empty
    
    def check_winner(self) -> Optional[Symbol]:
        """
        Check if there's a winner.
        
        Returns:
            Symbol.X, Symbol.O, or None
        """
        # Check rows
        for row in range(3):
            if self.grid[row][0] != Symbol.EMPTY:
                if self.grid[row][0] == self.grid[row][1] == self.grid[row][2]:
                    return self.grid[row][0]
        
        # Check columns
        for col in range(3):
            if self.grid[0][col] != Symbol.EMPTY:
                if self.grid[0][col] == self.grid[1][col] == self.grid[2][col]:
                    return self.grid[0][col]
        
        # Check diagonals
        if self.grid[0][0] != Symbol.EMPTY:
            if self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
                return self.grid[0][0]
        
        if self.grid[0][2] != Symbol.EMPTY:
            if self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
                return self.grid[0][2]
        
        return None
    
    def __str__(self) -> str:
        """String representation of board."""
        result = []
        for row in self.grid:
            row_str = " | ".join(str(cell) for cell in row)
            result.append(row_str)
        return "\n---+---+---\n".join(result)
    
    def to_list(self) -> List[List[str]]:
        """Convert to list of strings."""
        return [[str(cell) for cell in row] for row in self.grid]