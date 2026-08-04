import pygame, random
from config import SCREEN_WIDTH

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.x = x - width // 2  # Center the paddle on the x position
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def update(self, dt, direction):
        "Update paddle position based on direction (-1 for left, 1 for right)"
        self.x += direction * self.speed * dt
        # Keep the paddle within the screen bounds
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        self.rect.x = self.x
        
    def draw(self, screen):
        "Draw the paddle"
        pygame.draw.rect(screen, (100, 200, 255), self.rect)