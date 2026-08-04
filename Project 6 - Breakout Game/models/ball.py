import pygame, random

class Ball:
    def __init__(self, x, y, size, speed):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.vx = 0
        self.vy = 0
        self.stuck_to_paddle = True
        self.rect = pygame.Rect(x, y, size, size)
        
    def launch(self, direction=1):
        "Launch the ball from the paddle"
        self.stuck_to_paddle = False
        self.vx = random.uniform(-0.5, 0.5) * self.speed
        self.vy = -self.speed
        
    def update(self, dt):
        "Update ball position based on velocity"
        if self.stuck_to_paddle:
            return
        
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, screen):
        "Draw the ball"
        pygame.draw.rect(screen, (255, 255, 255), self.rect)