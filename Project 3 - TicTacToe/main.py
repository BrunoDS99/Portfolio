from models import GameMode, AIDifficulty, GameStats, GameStatus, GameState, Player, Position
from game import Game
from view import ConsoleView
from utils import save_stats, load_stats


class TicTacToeApp:
    """Main app class"""
    
    def __init__(self):
        self.view = ConsoleView()
        self.stats = load_stats()
        if not self.stats:
            self.stats = GameStats()
        self.view.display_welcome()
        
    def run(self) -> None:
        """Main application loop."""
        while True:
            choice = self.view.get_menu_choice()
            
            if choice == '1':
                self._play_game(GameMode.PVP)
            elif choice == '2':
                self._play_game(GameMode.PVE, AIDifficulty.EASY)
            elif choice == '3':
                self._play_game(GameMode.PVE, AIDifficulty.MEDIUM)
            elif choice == '4':
                self._play_game(GameMode.PVE, AIDifficulty.HARD)
            elif choice == '5':
                self._play_game(GameMode.EVE, AIDifficulty.MEDIUM)
            elif choice == '6':
                self.view.display_game_stats(self.stats)
                input("\nPress Enter to continue...")
            elif choice == '7':
                print("\nThanks for playing!")
                save_stats(self.stats)
                break
            
    def _play_game(self, mode: GameMode, difficulty: AIDifficulty = None) -> None:
        """Play a game with the given mode and difficulty."""
        game = Game(mode, difficulty if difficulty else AIDifficulty.MEDIUM)
        
        while True:
            self.view._clear_screen()
            self.view.display_board(game.board)
            self.view.display_players(game.game_state.players)
            
            # Check if game is over
            if game.game_state.is_game_over:
                self.view.display_game_status(game.game_state.status)
                
                if game.game_state.status in [GameStatus.X_WINS, GameStatus.O_WINS]:
                    winner = game.board.check_winner()
                    self.view.display_winner(winner)
                else:
                    self.view.display_winner(None)
                
                # Show player stats
                stats = game.get_player_stats()
                self.view.display_player_stats(stats)
                
                # Save overall stats
                overall = game.get_overall_stats()
                self.stats.total_games = game.stats.total_games
                self.stats.x_wins = game.stats.x_wins
                self.stats.o_wins = game.stats.o_wins
                self.stats.draws = game.stats.draws
                save_stats(self.stats)
                
                # Save overall stats to persistent storage
                self.stats.total_games = overall['total_games']
                self.stats.x_wins = overall['x_wins']
                self.stats.o_wins = overall['o_wins']
                self.stats.draws = overall['draws']
                save_stats(self.stats)
                
                # Play again?
                if not self.view.get_play_again():
                    break
                
                game.reset()
                continue
            
            # Get current player
            current = game.game_state.current_player
            
            # AI's turn
            if current.is_ai:
                self.view.display_turn(current)
                self.view.display_ai_thinking(current)
                move = game.get_ai_move()
                if move:
                    game.make_move(move)
                    self.view.display_move(current, move)
                continue
            
            # Human's turn
            self.view.display_turn(current)
            position = self.view.get_position()
            
            if position is None:  # Player quit
                game.game_state.end_game(GameStatus.ABANDONED)
                break
            
            if not game.make_move(position):
                self.view.display_error("Invalid move! That position is taken.")
                continue
            
            self.view.display_move(current, position)

if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()