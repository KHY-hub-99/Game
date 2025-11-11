import pygame
from .bullet import Bullet

# Player
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.speed = 5
        self.origin_image = pygame.image.load("modules/images/player.png")
        self.origin_image = pygame.transform.scale(self.origin_image, (60, 60))
        self.image = self.origin_image.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x = x
        self.start_y = y

        # 플레이어 피격 상태
        self.is_hit = False
        self.flash_duration = 100 # ms
        self.hits_time = 0
        
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

        # Flash effect when hit
        if self.is_hit:
            now = pygame.time.get_ticks()
            if now - self.hits_time > self.flash_duration:
                self.image = self.origin_image.copy()
                self.is_hit = False
        
        # 총알 이동 좌표 업데이트    
        self.bullets.update()
        
        # 이탈 시
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 600:
            self.rect.right = 600
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 1000:
            self.rect.bottom = 1000

    # 플레이어 피격 시 호출할 메서드
    def get_hit(self):
        self.is_hit = True
        self.hits_time = pygame.time.get_ticks()
        self.darken_image()

    # 플레이어 이미지 어둡게 만드는 메서드
    def darken_image(self):
        dark_image = self.origin_image.copy()
        dark_image.fill((100, 100, 100), special_flags=pygame.BLEND_RGB_MULT) # 적보다 살짝 덜 어둡게
        self.image = dark_image
        
    def fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_down:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = now

