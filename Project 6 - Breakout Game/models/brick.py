import pygame, random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class Brick:
    def __init__(self, x, y, width, height, color, health=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.health = health
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True
        
    def hit(self):
        "Reduce health when hit and check if the brick is destroyed"
        self.health -= 1
        if self.health <= 0:
            self.alive = False
            return True  # Brick destroyed
        return False  # Brick still alive    
    
    def draw(self, screen):
        "Draw the brick if it's alive"
        if self.alive:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, (50, 50, 50), self.rect, 2)  # Draw border