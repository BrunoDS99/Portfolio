import pygame, random
from config import *
from models.ball import Ball
from models.paddle import Paddle
from models.brick import Brick

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Initialize game objects
        self.paddle = Paddle(SCREEN_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.ball = Ball(BALL_START_X, BALL_START_Y, BALL_SIZE, BALL_SPEED)
        self.bricks = self.create_bricks()
        self.score = 0
        self.lives = 3
        
        self.paddle_direction = 0  # -1 for left, 1 for right, 0 for no movement
        
    def create_bricks(self):
        "Create a grid of bricks"
        bricks = []
        colors = [RED, GREEN, BLUE, ORANGE, YELLOW]
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_TOP_OFFSET
                color = colors[row % len(colors)]
                brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, color)
                bricks.append(brick)
        return bricks
    
    def handle_input(self):
        "User input handling"
        keys = pygame.key.get_pressed()
        self.paddle_direction = 0
        if keys[pygame.K_LEFT]:
            self.paddle_direction = -1
        if keys[pygame.K_RIGHT]:
            self.paddle_direction = 1
        if keys[pygame.K_SPACE] and self.ball.stuck_to_paddle:
            self.ball.launch()
            
    def update(self, dt):
        "Update game state"
        self.paddle.update(dt, self.paddle_direction) #Update paddle
        self.ball.update(dt) #Update Ball
        
        if self.ball.stuck_to_paddle:
            self.ball.x = self.paddle.x + self.paddle.width // 2 - self.ball.size // 2
            self.ball.rect.x = self.ball.x
        
    def draw(self):
        "Draw the screen"
        self.screen.fill(BLACK)
        
        #Draw game objects
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
            
        #Draw Score and Lives (temp)
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_tex = font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_tex, (SCREEN_WIDTH - 150, 10))
        
        pygame.display.flip()
        
    def run(self):
        "Main loop"
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # Delta time in seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.handle_input()
            self.update(dt)
            self.draw()
        
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()