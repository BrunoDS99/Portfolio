import pygame, random, math
from config import SCREEN_WIDTH

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed
        self.x = x - width // 2  # Center the paddle on the x position
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.direction = 0
        self.old_x = self.x

        
    def update(self, dt, direction):
        "Update paddle position based on direction (-1 for left, 1 for right)"
        self.old_x = self.x
        self.x += direction * self.speed * dt
        self.direction = direction
        
        # Keep within screen bounds
        if self.x < 0:
            self.x = 0
            self.direction = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
            self.direction = 0
        
        self.rect.x = self.x
      
    def paddle_hit(self, ball):
        hit_pos = (ball.rect.centerx - self.rect.left) / self.rect.width #where on the paddle
        hit_pos = max(0, min(1,hit_pos))
        
        angle = (hit_pos - 0.5) * 140 #Base angle from position
        angle += self.direction * 25
        angle = max(-85, min(85, angle))
        
        speed_multiplier = 1.0 + abs(self.direction) * 0.3
        speed = ball.base_speed * speed_multiplier
        
        ball.vx = speed * math.sin(math.radians(angle))
        ball.vy = -speed *math.cos(math.radians(angle))
        
    def draw(self, screen):
        "Draw the paddle"
        pygame.draw.rect(screen, (100, 200, 255), self.rect)
        
    