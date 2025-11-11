import pygame
import random

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("modules/images/enemy.png")
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(0.7, 2.2)
        self.start_x = x
        self.start_y = y
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 1000:  # Assuming screen height is 1000
            self.rect.x = self.start_x
            self.rect.y = self.start_y