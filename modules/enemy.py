import pygame
import random
from .enemy_bullet import EnemyBullet

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, all_enemy_bullets):
        super().__init__()
        self.origin_image = pygame.image.load("modules/images/enemy1.png")
        self.origin_image = pygame.transform.scale(self.origin_image, (120, 120))
        self.image = self.origin_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = random.uniform(0.7, 1.5)
        self.start_x = x
        self.start_y = y
        self.is_hit = False
        self.flash_duration = 100 # ms
        self.hits_time = 0
        self.hits = 0

        # bullet timing
        self.last_shot = pygame.time.get_ticks()
        self.shot_down = random.randint(1000, 3000)  # ms
        # bullet group
        self.enemy_bullets = pygame.sprite.Group()
        self.all_enemy_bullets = all_enemy_bullets
        
    def update(self):
        if self.is_hit:
            now = pygame.time.get_ticks()
            if now - self.hits_time > self.flash_duration:
                self.image = self.origin_image.copy()
                self.is_hit = False

        self.rect.y += self.speed
        if self.rect.top > 1000:  # Assuming screen height is 1000
            self.rect.x = random.randint(50, 550)
            self.rect.y = self.start_y

        # 총알 추가
        self.enemy_fire_bullet()
        self.enemy_bullets.update()

    def enemy_fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_down:
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            self.enemy_bullets.add(enemy_bullet)
            self.all_enemy_bullets.add(enemy_bullet)
            self.last_shot = now

    def get_hit(self):
        self.is_hit = True
        self.hits_time = pygame.time.get_ticks()
        # Change image to indicate hit (e.g., tint red)
        self.darken_image()

    def darken_image(self):
        dark_image = self.origin_image.copy()
        dark_image.fill((70, 70, 70), special_flags=pygame.BLEND_RGB_MULT)
        self.image = dark_image