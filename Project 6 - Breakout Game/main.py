import pygame, random
from config import *
from models.ball import Ball
from models.paddle import Paddle
from models.brick import Brick
from views.scoreboard import Scoreboard

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        
        # Initialize game objects
        self.paddle = Paddle(SCREEN_WIDTH // 2, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.ball = Ball(BALL_START_X, BALL_START_Y, BALL_SIZE, BALL_SPEED)
        self.bricks = self.create_bricks()

        self.scoreboard = Scoreboard()
        
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
            
    def handle_collisions(self):
        "Handle colision"
        #Ball and wall
        if self.ball.x < 0 or self.ball.x + self.ball.size >= SCREEN_WIDTH:
            self.ball.vx *= -1
        
        if self.ball.y <= 0:
            self.ball.vy *= -1
            
        #ball and paddle
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.vy > 0:
            self.ball.vy *= -1
            self.ball.y = self.paddle.y - self.ball.size
            
        #ball and bricks
        for brick in self.bricks:
            if brick.alive and self.ball.rect.colliderect(brick.rect):
                if brick.hit():
                    self.scoreboard.add_points(10)
                self.ball.vy *= -1
                break
        
        #balls go off screen
        if self.ball.y > SCREEN_HEIGHT:
            self.scoreboard.lives -= 1
            if self.scoreboard.lives <= 0:
                self.game_over = True
            else:
                self.reset_ball()    
        
    def update(self, dt):
        "Update game state"
        self.paddle.update(dt, self.paddle_direction) #Update paddle
        self.ball.update(dt) #Update Ball
        
        if self.ball.stuck_to_paddle:
            self.ball.x = self.paddle.x + self.paddle.width // 2 - self.ball.size // 2
            self.ball.rect.x = self.ball.x
            
        self.handle_collisions()
        
    def draw(self):
        "Draw the screen"
        self.screen.fill(BLACK)
        
        #Draw game objects
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for brick in self.bricks:
            brick.draw(self.screen)
            
        #Draw Scoreboard
        self.scoreboard.draw(self.screen)
        
        #Draw game over screen
        if self.game_over:
            self.scoreboard.draw_game_over(self.screen)
        
        pygame.display.flip()
        
    def reset_ball(self):
        "Reset ball to paddle position"
        self.ball.x = self.paddle.x + self.paddle.width // 2 - self.ball.size // 2
        self.ball.y = PADDLE_Y - self.ball.size
        self.ball.stuck_to_paddle = True
        self.ball.vx = 0
        self.ball.vy = 0
        
    def reset_game(self):
        "Reset entire game"
        self.game_over = False
        
        # Reset paddle
        self.paddle.x = SCREEN_WIDTH // 2 - self.paddle.width // 2
        self.paddle.rect.x = self.paddle.x
        
        # Reset ball
        self.reset_ball()
        
        # Reset bricks
        self.bricks = self.create_bricks()
        
        # Reset scoreboard
        self.scoreboard.score = 0
        self.scoreboard.lives = 3
        self.scoreboard.level = 1
        
    def run(self):
        "Main loop"
        while self.running:
            dt = self.clock.tick(FPS) / 1000  # Delta time in seconds
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if self.game_over:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                        if event.key == pygame.K_ESCAPE:
                            self.running = False
            
            
            if not self.game_over:
                self.handle_input()
                self.update(dt)

            self.draw()
        pygame.quit()
        
if __name__ == "__main__":
    game = Game()
    game.run()