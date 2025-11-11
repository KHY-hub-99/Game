import pygame
from .bullet import Bullet

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.image = pygame.image.load("modules/images/player.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.start_y = y
        
        # 총알 그룹
        self.bullets = pygame.sprite.Group()
        self.last_shot = 0
        self.shot_down = 150
    
    def update(self):
        # 이동키 조정
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # 총알키 조정
        if keys[pygame.K_SPACE]:
            self.fire_bullet()
        
        # 총알 이동 좌표 업데이트    
        self.bullets.update()

        if self.rect.top > 1000:  # Assuming screen height is 1000
            self.rect.x = self.start_x
            self.rect.y = self.start_y
        if self.rect.left < 0:
            self.rect.x = self.start_x
            self.rect.y = self.start_y
        if self.rect.right > 600:  # Assuming screen width is 600
            self.rect.x = self.start_x
            self.rect.y = self.start_y
        
    def fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_down:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = now