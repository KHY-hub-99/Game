import pygame
import sys
from modules.player import Player

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