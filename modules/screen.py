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
        positions = [(random.randint(60, 540), 0) for _ in range(5)]
        for pos in positions:
            enemy = Enemy(pos[0], pos[1], self.enemies_bullets)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # font
        self.font = pygame.font.SysFont("pixel_font.ttf", 32)
        self.score = 0
        
        # HP바
        self.max_hp = 100
        self.current_hp = 100
        self.hit_damage = 20
        
        # 게임오버 판단
        self.game_over = False

    # 사건 중 x창 입력시 게임 종료
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    # 수정된 좌표 업데이트
    def update(self):
        if not self.game_over:
            self.all_sprites.update()
            self.enemies_bullets.update()
            self.player.bullets.update()
            self.check_collisions()


    # 화면에 나타내기
    def draw(self):
        # 배경 이미지 출력
        self.screen.blit(self.background, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player.bullets.draw(self.screen)
        self.draw_score()
        self.enemies_bullets.draw(self.screen)
        self.draw_hp_bar()
        
        if self.game_over:
            self.draw_game_over()
        
        pygame.display.flip()
        

    # 점수 도면 설정
    def draw_score(self):
        # 1. 폰트와 색상 설정 (self.score_font 사용)
        self.score_font = pygame.font.SysFont("pixel_font.ttf", 32)
        score_surf = self.score_font.render(f"SCORE: {self.score}", True, (255, 255, 0)) # 노란색 텍스트
        
        # 2. 위치 및 패딩 설정
        padding = 10
        score_box_width = score_surf.get_width() + padding * 2
        score_box_height = score_surf.get_height() + padding * 2
        score_box_x = self.width - score_box_width -10
        score_box_y = 10
        
        # 3. 배경 박스 그리기
        outer_rect = pygame.Rect(score_box_x, score_box_y, score_box_width, score_box_height)
        pygame.draw.rect(self.screen, (20, 20, 20), outer_rect) # 어두운 배경색
        pygame.draw.rect(self.screen, (255, 255, 255), outer_rect, 2) # 흰색 테두리 (굵기 2)
        
        # 4. 텍스트 위치 계산 및 출력 (박스 중앙에 오도록)
        text_x = score_box_x + padding
        text_y = score_box_y + padding
        
        self.screen.blit(score_surf, (text_x, text_y))
        
        
    # HP 도면 설정
    def draw_hp_bar(self):
        # HP 바 자체의 크기
        hp_bar_inner_width = 150 
        hp_bar_inner_height = 15
        
        # HP 텍스트 렌더링
        hp_text_content = f"HP: {int(self.current_hp)}/{self.max_hp}"
        hp_text_surf = self.font.render(hp_text_content, True, (255, 255, 255))
        
        # 외부 박스의 패딩
        padding = 10 
        
        # 외부 박스 크기 계산 (HP 바 + 텍스트 + 패딩)
        outer_box_width = max(hp_bar_inner_width, hp_text_surf.get_width()) + padding * 2
        outer_box_height = hp_bar_inner_height + hp_text_surf.get_height() + padding * 3 # 텍스트와 바 사이 간격 포함
        
        # 외부 박스 위치 (화면 왼쪽 아래)
        outer_box_x = 10
        outer_box_y = self.height - outer_box_height - 10
        
        # 1. 외부 박스 그리기 (배경 및 테두리)
        outer_rect = pygame.Rect(outer_box_x, outer_box_y, outer_box_width, outer_box_height)
        pygame.draw.rect(self.screen, (50, 50, 50), outer_rect) # 어두운 회색 배경
        pygame.draw.rect(self.screen, (200, 200, 200), outer_rect, 2) # 밝은 회색 테두리
        
        # 2. HP 텍스트 위치 계산 및 그리기 (외부 박스 상단 중앙)
        text_x = outer_box_x + (outer_box_width // 2) - (hp_text_surf.get_width() // 2)
        text_y = outer_box_y + padding
        self.screen.blit(hp_text_surf, (text_x, text_y))
        
        # 3. HP 바 위치 계산 (외부 박스 하단 중앙)
        hp_bar_x = outer_box_x + (outer_box_width // 2) - (hp_bar_inner_width // 2)
        hp_bar_y = outer_box_y + hp_text_surf.get_height() + padding * 2
        
        # HP 바 배경 (빈 HP 부분)
        pygame.draw.rect(self.screen, (100, 0, 0), (hp_bar_x, hp_bar_y, hp_bar_inner_width, hp_bar_inner_height)) # 어두운 빨간색
        
        # 현재 HP에 따른 바의 길이 계산
        fill_width = (self.current_hp / self.max_hp) * hp_bar_inner_width
        fill_rect = pygame.Rect(hp_bar_x, hp_bar_y, fill_width, hp_bar_inner_height)
        
        # HP 채움 색상 설정 (예: 녹색)
        fill_color = (0, 180, 0)
        
        # 현재 HP 바 채우기
        pygame.draw.rect(self.screen, fill_color, fill_rect)
        
        
    # 게임 오버 텍스트 그리기
    def draw_game_over(self):
        game_over_font = pygame.font.SysFont("pixel_font.ttf", 64)
        text_surf = game_over_font.render("GAME OVER", False, (255, 0, 0))
        text_rect = text_surf.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(text_surf, text_rect)
        
        restart_font = pygame.font.SysFont("pixel_font.ttf", 32)
        restart_surf = restart_font.render('Press "R" for restart', False, (255, 255, 255))
        restart_rect = restart_surf.get_rect(center=(self.width//2, self.height//2 + 50))
        self.screen.blit(restart_surf, restart_rect)
        
    # 게임 재시작
    def reset_game(self):
        # 1. 게임 상태 변수 초기화
        self.score = 0
        self.player_hits = 0
        self.current_hp = self.max_hp
        self.game_over = False
        
        # 2. 모든 스프라이트 그룹 비우기
        self.all_sprites.empty()
        self.enemies_bullets.empty()
        self.enemies.empty()
        
        # 3. 플레이어 재초기화 및 그룹에 추가
        self.player = Player(self.width // 2, self.height - 200) # 플레이어 객체 새로 생성
        self.all_sprites.add(self.player)
        
        # 4. 적군 재초기화 및 그룹에 추가
        positions = [(random.randint(50, 550), 0) for _ in range(3)]
        for pos in positions:
            enemy = Enemy(pos[0], pos[1], self.enemies_bullets)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)
        
        print("Game Restarted!")

    # 충돌 검사
    def check_collisions(self):
        hits = pygame.sprite.groupcollide(self.enemies, self.player.bullets, False, True)
        for enemy in hits:
            enemy.hits += 1
            enemy.get_hit()
            print(f"Enemy hit! Total hits: {enemy.hits}")
            if enemy.hits >= 3:
                enemy.kill()
                self.score += 100

                # 적을 제거한 후, 새로운 적을 다시 생성하여 추가
                new_enemy = Enemy(random.randint(50, 550), 0, self.enemies_bullets)
                self.all_sprites.add(new_enemy)
                self.enemies.add(new_enemy)

        hits_player_bullet = pygame.sprite.spritecollide(self.player, self.enemies_bullets, True)
        if hits_player_bullet:
            self.current_hp -= self.hit_damage
            if self.current_hp < 0:
                self.current_hp = 0
            
            print(f"Player hit by bullet! Remaining HP: {self.current_hp}")
            self.player.get_hit()
            
            # 플레이어 HP가 0 이하일 때 게임 종료
            if self.current_hp <= 0:
                self.game_over = True
                print("Game Over!")

    # 실행
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            
            if self.game_over:
                pygame.display.flip()
                self.clock.tick(10)
            else:
                self.clock.tick(60)
        pygame.quit()
        sys.exit()