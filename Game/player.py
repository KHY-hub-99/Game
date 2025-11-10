import pygame
import sys

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.player_image = pygame.image.load("images/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))
        self.rect = self.player_image.get_rect(center=(x, y))
    
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        if keys[pygame.K_UP]:
            self.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.y += self.speed