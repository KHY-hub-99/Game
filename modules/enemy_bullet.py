import pygame
import random

# Enemy Bullet      
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("modules/images/enemy_bullet.png")
        self.image = pygame.transform.scale(self.image, (30, 60))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 4)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 1000:
            self.kill()