"""
쉿, 쳐다보지 마! - SCP-096 추격 게임

규칙:
    - 방향키(또는 WASD)로 움직여요. 손전등은 마지막으로 움직인 방향을 비춰요.
    - 손전등으로 096의 얼굴을 비추거나 096에게 부딪히면 096이 비명을 지른 뒤
      미친 듯이 쫓아와요.
    - 추격 시간이 끝날 때까지 잡히지 않으면 점수 +1. 대신 다음 추격은 더 빠르고 길어요.
    - Shift 키로 잠깐 대시할 수 있어요 (쿨타임 있음).
    - 잡히면 게임 오버. R 키로 다시 시작, ESC 키로 종료.

실행 방법:
    pip install pygame
    python game.py
"""

import math
import random

import pygame

# ---------------------------------------------------------------
# 게임 설정값 (숫자를 바꾸면 난이도가 바뀌어요)
# ---------------------------------------------------------------
WIDTH, HEIGHT = 800, 600
FPS = 60

PLAYER_RADIUS = 14
PLAYER_SPEED = 200          # 1초에 움직이는 픽셀 수
DASH_SPEED = 520
DASH_TIME = 0.2             # 대시가 지속되는 시간(초)
DASH_COOLDOWN = 2.0         # 대시를 다시 쓰기까지 기다리는 시간(초)

LIGHT_RANGE = 260           # 손전등이 닿는 거리
LIGHT_ANGLE = 30            # 손전등 폭 (가운데에서 좌우로 몇 도인지)

SHY_RADIUS = 18
SHY_WANDER_SPEED = 40       # 얌전할 때 속도
SHY_CHASE_SPEED = 215       # 첫 추격 속도 (플레이어보다 살짝 빠름)
SHY_CHASE_SPEED_UP = 15     # 점수가 오를 때마다 늘어나는 추격 속도
SHY_TURN = 3.0              # 방향을 트는 민첩함 (작을수록 급회전을 못 해요)
SCREAM_TIME = 1.8           # 비명 지르는 시간 = 도망칠 준비 시간
CHASE_TIME = 5.0            # 첫 추격 시간
CHASE_TIME_UP = 1.0         # 점수가 오를 때마다 늘어나는 추격 시간

# 색깔 (빨강, 초록, 파랑)
BLACK = (15, 15, 20)
FLOOR = (40, 42, 50)
WHITE = (235, 235, 235)
PALE = (215, 210, 200)
RED = (220, 40, 40)
YELLOW = (255, 240, 150)
BLUE = (80, 160, 255)
GRAY = (130, 130, 140)


class Player:
    """내가 조종하는 캐릭터"""

    def __init__(self):
        self.pos = pygame.Vector2(WIDTH / 2, HEIGHT - 80)
        self.facing = pygame.Vector2(0, -1)   # 바라보는 방향 (처음엔 위쪽)
        self.dash_left = 0.0                  # 남은 대시 시간
        self.dash_cooldown = 0.0              # 남은 쿨타임

    def update(self, dt, keys):
        # 1) 키보드 입력으로 움직일 방향 만들기
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move.y += 1

        # 2) 대시 처리
        self.dash_cooldown = max(0.0, self.dash_cooldown - dt)
        self.dash_left = max(0.0, self.dash_left - dt)
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.dash_cooldown == 0:
            self.dash_left = DASH_TIME
            self.dash_cooldown = DASH_COOLDOWN

        # 3) 실제로 이동 (대각선이 더 빠르지 않도록 길이를 1로 맞춤)
        if move.length() > 0:
            move = move.normalize()
            self.facing = move
            speed = DASH_SPEED if self.dash_left > 0 else PLAYER_SPEED
            self.pos += move * speed * dt

        # 4) 화면 밖으로 나가지 않게 막기
        self.pos.x = max(PLAYER_RADIUS, min(WIDTH - PLAYER_RADIUS, self.pos.x))
        self.pos.y = max(PLAYER_RADIUS, min(HEIGHT - PLAYER_RADIUS, self.pos.y))

    def can_see(self, target):
        """target 위치가 손전등 불빛 안에 있으면 True"""
        to_target = target - self.pos
        if to_target.length() == 0 or to_target.length() > LIGHT_RANGE:
            return False
        # 두 방향 사이의 각도를 -180 ~ 180도 범위로 맞춘 뒤 비교
        angle = (self.facing.angle_to(to_target) + 180) % 360 - 180
        return abs(angle) < LIGHT_ANGLE

    def draw(self, screen):
        # 손전등 불빛: 부채꼴 모양을 반투명하게 그리기
        light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        points = [self.pos]
        for step in range(-LIGHT_ANGLE, LIGHT_ANGLE + 1, 5):
            points.append(self.pos + self.facing.rotate(step) * LIGHT_RANGE)
        pygame.draw.polygon(light, (*YELLOW, 45), points)
        screen.blit(light, (0, 0))

        # 몸통 (대시 중엔 하얗게 번쩍)
        color = WHITE if self.dash_left > 0 else BLUE
        pygame.draw.circle(screen, color, self.pos, PLAYER_RADIUS)
        # 바라보는 방향에 작은 점
        pygame.draw.circle(screen, BLACK, self.pos + self.facing * 8, 4)


class Shy:
    """SCP-096. 상태(state)에 따라 행동이 달라져요.

    "wander" : 얌전히 어슬렁거림
    "scream" : 얼굴을 보여서 비명을 지르는 중 (제자리에서 덜덜 떨림)
    "chase"  : 미친 듯이 쫓아옴
    """

    def __init__(self):
        self.pos = pygame.Vector2(WIDTH / 2, 150)
        self.vel = pygame.Vector2(0, 0)
        self.state = "wander"
        self.timer = 0.0                       # 현재 상태가 끝날 때까지 남은 시간
        self.wander_dir = pygame.Vector2(1, 0)
        self.wander_change = 0.0               # 어슬렁 방향을 바꿀 때까지 남은 시간

    def trigger(self):
        """얼굴을 봤다! 비명 시작"""
        self.state = "scream"
        self.timer = SCREAM_TIME
        self.vel = pygame.Vector2(0, 0)

    def update(self, dt, player, score):
        """096 움직이기. 추격을 무사히 버텨내면 True를 돌려줘요."""
        self.timer -= dt

        if self.state == "wander":
            # 가끔 랜덤한 방향으로 바꾸며 천천히 걷기
            self.wander_change -= dt
            if self.wander_change <= 0:
                self.wander_dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
                self.wander_change = random.uniform(1.5, 3.5)
            self.vel = self.wander_dir * SHY_WANDER_SPEED

        elif self.state == "scream":
            if self.timer <= 0:
                self.state = "chase"
                self.timer = CHASE_TIME + CHASE_TIME_UP * score

        elif self.state == "chase":
            # 플레이어 쪽으로 방향을 틀되, 한 번에 확 꺾지는 못해요.
            # 그래서 마지막 순간에 옆으로 피하면 지나쳐 버릴 수 있어요.
            speed = SHY_CHASE_SPEED + SHY_CHASE_SPEED_UP * score
            to_player = player.pos - self.pos
            if to_player.length() > 0:
                desired = to_player.normalize() * speed
                self.vel += (desired - self.vel) * min(1.0, SHY_TURN * dt)
            if self.timer <= 0:
                self.state = "wander"     # 지쳐서 다시 얌전해짐
                return True

        self.pos += self.vel * dt

        # 벽에 부딪히면 튕겨 나오기
        if not SHY_RADIUS <= self.pos.x <= WIDTH - SHY_RADIUS:
            self.wander_dir.x *= -1
            self.vel.x *= -1
        if not SHY_RADIUS <= self.pos.y <= HEIGHT - SHY_RADIUS:
            self.wander_dir.y *= -1
            self.vel.y *= -1
        self.pos.x = max(SHY_RADIUS, min(WIDTH - SHY_RADIUS, self.pos.x))
        self.pos.y = max(SHY_RADIUS, min(HEIGHT - SHY_RADIUS, self.pos.y))
        return False

    def draw(self, screen):
        pos = pygame.Vector2(self.pos)
        if self.state == "scream":
            # 덜덜 떨리는 효과
            pos += (random.uniform(-4, 4), random.uniform(-4, 4))

        # 길쭉한 팔 두 개
        arm = 30 if self.state == "chase" else 22
        pygame.draw.line(screen, PALE, pos + (-12, 0), pos + (-20, arm), 4)
        pygame.draw.line(screen, PALE, pos + (12, 0), pos + (20, arm), 4)
        # 몸(머리)
        pygame.draw.circle(screen, PALE, pos, SHY_RADIUS)

        if self.state == "wander":
            # 얌전할 땐 두 손으로 얼굴을 가리고 있어요
            pygame.draw.circle(screen, GRAY, pos + (-6, 0), 7)
            pygame.draw.circle(screen, GRAY, pos + (6, 0), 7)
        else:
            # 화났을 땐 까만 눈과 쩍 벌린 입
            pygame.draw.circle(screen, BLACK, pos + (-6, -5), 3)
            pygame.draw.circle(screen, BLACK, pos + (6, -5), 3)
            mouth = pygame.Rect(0, 0, 12, 14 if self.state == "scream" else 9)
            mouth.center = (pos.x, pos.y + 6)
            pygame.draw.ellipse(screen, BLACK, mouth)
        if self.state == "chase":
            pygame.draw.circle(screen, RED, pos, SHY_RADIUS + 3, 2)


class Game:
    """게임 전체(점수, 상태, 화면 그리기)를 관리"""

    def __init__(self):
        self.best = 0
        self.reset()

    def reset(self):
        self.player = Player()
        self.shy = Shy()
        self.score = 0
        self.game_over = False

    def update(self, dt, keys):
        if self.game_over:
            return

        self.player.update(dt, keys)
        survived = self.shy.update(dt, self.player, self.score)
        if survived:
            self.score += 1
            self.best = max(self.best, self.score)

        touching = self.player.pos.distance_to(self.shy.pos) < PLAYER_RADIUS + SHY_RADIUS

        if self.shy.state == "wander":
            # 얌전한 096을 비추거나 건드리면 → 비명!
            if self.player.can_see(self.shy.pos) or touching:
                self.shy.trigger()
        elif self.shy.state == "chase" and touching:
            self.game_over = True

    def draw(self, screen, font, big_font):
        # 추격 중이면 바닥이 붉게 깜빡여요
        if self.shy.state == "chase" and int(self.shy.timer * 4) % 2 == 0:
            screen.fill((70, 30, 35))
        else:
            screen.fill(FLOOR)

        self.player.draw(screen)
        self.shy.draw(screen)

        # 윗부분 정보 표시
        info = f"SCORE {self.score}   BEST {self.best}"
        screen.blit(font.render(info, True, WHITE), (16, 12))
        if self.player.dash_cooldown == 0:
            screen.blit(font.render("DASH READY (Shift)", True, YELLOW), (16, 40))

        if self.shy.state == "scream":
            self.center_text(screen, big_font, "IT SAW YOU. RUN!", RED, HEIGHT / 2 - 120)
        elif self.shy.state == "chase":
            left = f"SURVIVE {self.shy.timer:.1f}"
            self.center_text(screen, font, left, WHITE, 24)

        if self.game_over:
            self.center_text(screen, big_font, "GAME OVER", RED, HEIGHT / 2 - 30)
            self.center_text(screen, font, "R: retry   ESC: quit", WHITE, HEIGHT / 2 + 20)

    @staticmethod
    def center_text(screen, font, text, color, y):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, y)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Don't Look - SCP-096")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 64)
    game = Game()

    running = True
    while running:
        # dt = 지난 프레임부터 흐른 시간(초). 컴퓨터 속도와 상관없이 똑같이 움직이게 해줘요.
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()

        game.update(dt, pygame.key.get_pressed())
        game.draw(screen, font, big_font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
