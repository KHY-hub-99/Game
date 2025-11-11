import pygame
import sys
import random

# 화면과 런
class Screen:
    def __init__(self):
        # 초기
        pygame.init()
        # 스크린 해상도
        self.width, self.height = 600, 1000
        # 배경 색
        self.back_ground_color = (0, 0, 0)
        self.background = pygame.image.load("modules/images/background.png")
        self.background = pygame.transform.scale(self.background, (self.width, self.height))
        # 스크린 세팅
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 타이틀
        pygame.display.set_caption("SHOT!")
        # 프레임 일정도 유지
        self.clock = pygame.time.Clock()
        
        # run과 모든 스프라이트 그룹 초기화
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        
        # player group
        self.player = Player(self.width // 2, self.height - 200)
        self.all_sprites.add(self.player)

        # enemy_bullets group
        self.enemies_bullets = pygame.sprite.Group()
        
        # enemy group
        self.enemies = pygame.sprite.Group()
        positions = [(random.randint(50, 550), 0) for _ in range(3)]
        for pos in positions:
            enemy = Enemy(pos[0], pos[1])
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # font
        self.font = pygame.font.SysFont(None, 36)
        self.score = 0

    # 사건 중 x창 입력시 게임 종료
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # 수정된 좌표 업데이트
    def update(self):
        self.all_sprites.update()
        self.check_collisions()


    # 화면에 나타내기
    def draw(self):
        # 배경 이미지 출력
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.draw_score()
        self.enemies_bullets.draw(self.screen)
        

    # 점수 그리기
    def draw_score(self):
        score_surf = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surf, (10, 10))

    # 충돌 검사
    def check_collisions(self):
        hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
        for enemy in hits:
            enemy.hits += 1
            enemy.get_hit()
            print(f"Enemy hit! Total hits: {enemy.hits}")
            if enemy.hits >= 3:
                enemy.kill()
                self.score += 1

                # 적을 제거한 후, 새로운 적을 다시 생성하여 추가
                new_enemy = Enemy(random.randint(50, 550), 0)
                self.all_sprites.add(new_enemy)
                self.enemies.add(new_enemy)
                self.enemies_bullets.add(new_enemy.enemy_bullets)

    # 실행
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

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

        # 이탈 시
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

# Bullet      
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=10):
        super().__init__()
        self.image = pygame.image.load("modules/images/bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
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
            enemy_bullet = EnemyBullet(self.rect.centerx, self.rect.top)
            self.enemy_bullets.add(enemy_bullet)
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

# Enemy Bullet      
class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("modules/images/enemy_bullet.png")
        self.image = pygame.transform.scale(self.image, (20, 40))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = random.randint(2, 4)
        
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 1000:
            self.kill()

# 게임 실행
if __name__ == "__main__":
    game = Screen()
    game.run()