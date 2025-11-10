import pygame
import sys

# 화면과 런
class Screen:
    def __init__(self):
        # 초기
        pygame.init()
        # 스크린 해상도
        self.width, self.height = 800, 1200
        # 배경 색
        self.back_ground_color = (0, 0, 0)
        # 스크린 세팅
        self.screen = pygame.display.set_mode((self.width, self.height))
        # 타이틀
        pygame.display.set_caption("SHOT!")
        # 프레임 일정도 유지
        self.clock = pygame.time.Clock()
        
        # run
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        # player
        self.player = Player(self.width // 2, self.height - 200)
        self.all_sprites.add(self.player)

    # 사건 중 x창 입력시 게임 종료
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    # 수정된 좌표 업데이트
    def update(self):
        self.all_sprites.update()

    # 화면에 나타내기
    def draw(self):
        self.screen.fill(self.back_ground_color)
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)

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
        
    def fire_bullet(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shot_down:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            self.bullets.add(bullet)
            self.last_shot = now
            
# 총알        
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

# 게임 실행
if __name__ == "__main__":
    game = Screen()
    game.run()