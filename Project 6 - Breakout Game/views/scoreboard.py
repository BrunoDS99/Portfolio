import pygame

from config import SCREEN_WIDTH, WHITE, BLACK, SCREEN_HEIGHT

class Scoreboard:
    def __init__(self):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.high_score = self.load_high_score()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def load_high_score(self):
        "Load the high score from a file"
        try:
            with open("saves/high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0
        
    def save_high_score(self):
        "Save the high score to a file"
        try:
            with open("saves/high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass 
        
    def update(self, score, lives, level):
        "update the scoreboard values"
        self.score = score
        self.lives = lives
        self.level = level
        
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
    def add_points(self, points):
        "Add points to the score"
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
            self.save_high_score()
            
    def draw(self, screen):
        "Draw the scoreboard on the screen"
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        level_rect = level_text.get_rect(center=(SCREEN_WIDTH // 2, 20))
        screen.blit(level_text, level_rect)
        
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 150, 20))
        
        high_score_text = self.small_font.render(f"Best: {self.high_score}", True, (150,150,150))
        high_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(high_score_text, high_rect)
        
    def draw_game_over(self, screen):
        "Draw game over on the screen"
        #Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0,0,0))
        screen.blit(overlay, (0,0))
        
        #Game over text
        big_font = pygame.font.Font(None, 72)
        game_over_text = big_font.render("GAME OVER", True, (255,0,0))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        
        #Final Score
        score_text = self.font.render(f"Final score: {self.score}", True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(score_text, score_rect)
        
        #High score
        high_text = self.font.render(f"High score: {self.high_score}", True, (255, 255, 0))
        high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(high_text, high_rect)
        
        #Restart
        small_font = pygame.font.Font(None, 28)
        restart_text = small_font.render("Press SPACE to restart or ESC to quit", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
        screen.blit(restart_text, restart_rect)
        