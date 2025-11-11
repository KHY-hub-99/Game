import pygame
import sys
from .player import Player
from .enemy import Enemy
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
        
        # run
        self.running = True
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        
        # player
        self.player = Player(self.width // 2, self.height - 200)
        self.all_sprites.add(self.player)
        
        # enemy
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