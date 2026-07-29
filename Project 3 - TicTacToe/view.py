import os
from typing import Optional
from models import Position, Symbol, Player, GameStatus, GameMode, GameStats

class ConsoleView:
    """Console-based view"""
    
    def __init__(self):
        self._clear_screen()
        
    def _clear_screen(self) -> None:
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def display_welcome(self) -> None:
        """Display welcome message."""
        self._clear_screen()
        print("-" * 50)
        print("     TIC TAC TOE")
        print("-" * 50)
        print("\nA professional implementation with:")
        print("  • Multiple game modes")
        print("  • AI with 3 difficulty levels")
        print("  • Statistics tracking")
        print("  • Clean architecture")
        print("\nPress Enter to continue...")
        input()
        
    def display_board(self, board) -> None:
        """Display the board."""
        print("\n" + "=" * 30)
        print("    Current Board")
        print("=" * 30)
        print("\n    1   2   3")
        print("  ┌───┬───┬───┐")
        
        for row in range(3):
            symbols = []
            for col in range(3):
                cell = board.get_cell(Position(row, col))
                symbols.append(str(cell))
            
            print(f"{row+1} │ {symbols[0]} │ {symbols[1]} │ {symbols[2]} │")
            if row < 2:
                print("  ├───┼───┼───┤")
        
        print("  └───┴───┴───┘")
        print("\n" + "=" * 30)
        
    def display_players(self, players: list) -> None:
        """Display player information."""
        print("\n👥 Players:")
        for player in players:
            symbol_icon = "❌" if player.symbol == Symbol.X else "⭕"
            player_icon = "🤖" if player.is_ai else "👤"
            print(f"  {symbol_icon} {player.name} ({player_icon})")
    
    def display_player_stats(self, stats: dict) -> None:
        """Display player statistics."""
        print("\n📊 Player Statistics:")
        for name, data in stats.items():
            print(f"\n  {name}:")
            print(f"    Wins: {data['wins']}")
            print(f"    Losses: {data['losses']}")
            print(f"    Draws: {data['draws']}")
            print(f"    Win Rate: {data['win_rate']:.1f}%")
    
    def display_game_status(self, status: GameStatus) -> None:
        """Display game status."""
        status_messages = {
            GameStatus.NOT_STARTED: " Not started",
            GameStatus.IN_PROGRESS: " In progress",
            GameStatus.X_WINS: "❌ X Wins! ",
            GameStatus.O_WINS: "⭕ O Wins! ",
            GameStatus.DRAW: " It's a draw!",
            GameStatus.ABANDONED: " Abandoned"
        }
        print(f"\n📊 Status: {status_messages.get(status, 'Unknown')}")
    
    def display_winner(self, winner: Optional[Symbol]) -> None:
        """Display winner."""
        if winner:
            icon = "❌" if winner == Symbol.X else "⭕"
            print(f"\n {icon} {winner.value} WINS THE GAME! ")
        else:
            print("\n It's a draw!")
    
    def display_move(self, player: Player, position: Position) -> None:
        """Display a move being made."""
        icon = "❌" if player.symbol == Symbol.X else "⭕"
        print(f"\n {player.name} {icon} → ({position.row+1}, {position.col+1})")
    
    def display_turn(self, player: Player) -> None:
        """Display whose turn it is."""
        icon = "❌" if player.symbol == Symbol.X else "⭕"
        print(f"\n{player.name} {icon}, it's your turn!")
    
    def display_ai_thinking(self, player: Player) -> None:
        """Display AI thinking message."""
        print(f"\n {player.name} is thinking...")
    
    def get_position(self) -> Optional[Position]:
        """
        Get position from player.
        
        Returns:
            Position or None if player quits
        """
        while True:
            try:
                pos_input = input("\nEnter position (1-9) or 'quit': ").strip()
                
                if pos_input.lower() == 'quit':
                    return None
                
                pos = int(pos_input) - 1
                if 0 <= pos < 9:
                    return Position.from_index(pos)
                print("❌ Please enter a number between 1-9")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def get_menu_choice(self) -> str:
        """Get main menu choice."""
        print("\n" + "=" * 50)
        print("        📋 MAIN MENU")
        print("=" * 50)
        print("\n1.  Player vs Player")
        print("2.  Player vs AI (Easy)")
        print("3.  Player vs AI (Medium)")
        print("4.  Player vs AI (Hard)")
        print("5.  AI vs AI (Watch the show!)")
        print("6.  View Statistics")
        print("7. ❌ Exit")
        print("\n" + "=" * 50)
        
        while True:
            choice = input("\nChoose (1-7): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return choice
            print("❌ Invalid choice. Please enter 1-7")
    
    def get_play_again(self) -> bool:
        """Ask if player wants to play again."""
        while True:
            choice = input("\nPlay again? (y/n): ").strip().lower()
            if choice in ['y', 'yes']:
                return True
            if choice in ['n', 'no']:
                return False
            print("❌ Please enter 'y' or 'n'")
    
    def display_error(self, message: str) -> None:
        """Display error message."""
        print(f"\n❌ {message}")
    
    def display_info(self, message: str) -> None:
        """Display info message."""
        print(f"\nℹ️  {message}")
    
    def display_game_stats(self, stats: GameStats) -> None:
        """Display overall game statistics."""
        print("\n" + "=" * 50)
        print("        📊 OVERALL STATISTICS")
        print("=" * 50)
        print(f"\nTotal Games: {stats.total_games}")
        print(f"X Wins: {stats.x_wins} ({stats.x_win_rate:.1f}%)")
        print(f"O Wins: {stats.o_wins} ({stats.o_win_rate:.1f}%)")
        print(f"Draws: {stats.draws} ({stats.draw_rate:.1f}%)")