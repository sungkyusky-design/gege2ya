"""
스트라이크 존: 산타모니카 - 1인칭 총게임 (레이캐스팅 FPS)

노을 지는 산타모니카 해변. 바다, 모래사장, 야자수, 대관람차가 있는 부두,
파스텔색 건물이 늘어선 시내 곳곳에 숨어 있는 적을 모두 쓰러뜨리세요.

규칙:
    - 적을 모두 쓰러뜨리면 라운드 승리. 라운드가 올라갈수록 적이 많아져요.
    - 체력이 0이 되면 게임 오버.

조작:
    W A S D          : 이동
    마우스           : 시점 (좌우 + 위아래)
    ← → / ↑ ↓        : 키보드로 시점 돌리기 (좌우 / 위아래)
    마우스 왼쪽      : 사격
    마우스 오른쪽    : 저격총 조준경
    1 2 3 4 / 휠     : 무기 바꾸기 (소총 / 권총 / 저격총 / 산탄총)
    Q                : 방금 쓰던 무기로
    R                : 재장전
    ESC              : 종료 (메뉴로)

팁:
    - 머리를 맞히면 한 방(HEADSHOT)! 적의 머리는 내 눈높이보다 조금 위에 있어요.
    - 쏘면 반동으로 시점이 위로 튀어요. 마우스를 살짝 내리면서 쏘면 잘 맞아요.
    - 저격총은 조준경(오른쪽 클릭) 없이 쏘면 잘 안 맞아요.

실행 방법:
    pip install pygame
    python shooter.py

원리 (레이캐스팅):
    화면을 세로 줄 여러 개로 나누고, 줄마다 플레이어 눈에서 광선(ray)을 쏴서
    바닥과 벽까지의 거리를 재요. 가까운 것은 크게, 먼 것은 작게 그리면 3D처럼 보여요.
"""

import asyncio
import math
import random
import sys

import pygame

from browser import fit_canvas

# ---------------------------------------------------------------
# 화면 / 게임 설정값
# ---------------------------------------------------------------
WIDTH, HEIGHT = 960, 600
FPS = 60
IN_BROWSER = sys.platform == "emscripten"
COL_W = 6 if IN_BROWSER else 4    # 세로 줄 하나의 폭(px). 브라우저는 느려서 조금 넓게
NUM_RAYS = WIDTH // COL_W
NORMAL_FOV = math.radians(66)     # 시야각
SCOPE_FOV = math.radians(18)      # 조준경을 들여다볼 때 시야각 (좁을수록 확대)
MAX_DEPTH = 40                    # 이보다 먼 곳은 안 그려요
EYE = 0.5                         # 눈높이 (1 = 건물 한 층 높이)
FOG_DIST = 26                     # 이 거리쯤 가면 노을 빛 안개에 묻혀요

MOVE_SPEED = 3.2                  # 1초에 몇 칸 움직이는지
TURN_SPEED = 2.6                  # ←/→ 키로 돌 때 속도
LOOK_SPEED = 420                  # ↑/↓ 키로 위아래 볼 때 속도
MOUSE_SENS = 0.0025               # 마우스 좌우 감도
MOUSE_SENS_Y = 1.0                # 마우스 위아래 감도
MAX_PITCH = 260                   # 위아래로 볼 수 있는 한계(px)

ENEMY_HP = 100
ENEMY_SPEED = 1.4
ENEMY_SIGHT = 14                  # 적이 플레이어를 알아보는 거리
ENEMY_REACTION = 0.7              # 적이 처음 발견하고 쏘기까지 걸리는 시간
SAFE_SPAWN = 8                    # 시작할 때 이 거리 안에는 적이 안 나와요
ENEMY_HEIGHT = 0.9                # 적 키 (눈높이 0.5보다 머리가 위에 있어요)

# 무기 목록
#   auto   : 꾹 누르면 연사되는지
#   delay  : 다음 발까지 걸리는 시간(초)
#   body / head : 몸통 / 머리 데미지 (적 체력 100)
#   spread : 총알이 퍼지는 정도(px)
#   kick   : 한 발 쏠 때 시점이 위로 튀는 정도(px)
#   pellets: 한 번에 나가는 총알 수 (산탄총)
WEAPONS = [
    dict(name="RIFLE", auto=True, delay=0.1, mag=30, reserve=120, body=34, head=100,
         spread=4, kick=9, reload=1.8, pellets=1, scope=False),
    dict(name="PISTOL", auto=False, delay=0.15, mag=12, reserve=60, body=40, head=100,
         spread=2, kick=16, reload=1.2, pellets=1, scope=False),
    dict(name="SNIPER", auto=False, delay=1.2, mag=5, reserve=25, body=100, head=100,
         spread=45, kick=50, reload=2.5, pellets=1, scope=True),
    dict(name="SHOTGUN", auto=False, delay=0.8, mag=8, reserve=32, body=20, head=40,
         spread=50, kick=40, reload=2.2, pellets=8, scope=False),
]

# ---------------------------------------------------------------
# 맵: 산타모니카 해변 (왼쪽이 바다, 오른쪽이 시내)
# ---------------------------------------------------------------
#   바닥   '~' 바다(못 들어가요)  '.' 모래사장  '_' 보드워크  '=' 도로
#          'p' 부두(나무 데크)    'g' 잔디 공원
#   건물   'A' 분홍  'B' 민트  'C' 노란 가게  'R' 붉은 호텔  'K' 나무 상자(엄폐물)
#   장식   'T' 야자수  'W' 대관람차
#   위치   'P' 플레이어 시작  'E' 적이 나타날 수 있는 곳
GAME_MAP = [
    "~~~~~~....._==RRRRR=AAAA==CCC=BB",
    "~~~~~~.T..._==RRRRR=AAAA==CCC=BB",
    "~~~~~~....._==RRRRR=gggggg=CCC=B",
    "~~~~~~..T.._=========gggTgg=====",
    "~~~~~~....._==AAAA===gggggg==KK=",
    "~~~~~~.E..._==AAAA=E=gggggg==KK=",
    "~~~~~~....._==AAAA===BBBBBB=E===",
    "~~~~~~..T.._========BBBBBB======",
    "~~~~~~....._==K=========E==RRRRR",
    "~pppppp....__==CCCC==AAAA==RRRRR",
    "~pWpppp.P..__==CCCC==AAAA==RRRRR",
    "~pppppp....__==CCCC==AAAA==RRRRR",
    "~~~~~~....._=====E======K=======",
    "~~~~~~..T.._==BBBB==gggg==AAAAAA",
    "~~~~~~....._==BBBB==gTgg==AAAAAA",
    "~~~~~~.E..._==BBBB==gggE==AAAAAA",
    "~~~~~~....._=====K============E=",
    "~~~~~~..T.._==RRRR==CCCCC=BBBBBB",
    "~~~~~~....._==RRRR==CCCCC=BBBBBB",
    "~~~~~~.E..._==RRRR=E=====K====E=",
    "~~~~~~....._==RRRR==AAAA==CCCCCC",
    "~~~~~~.T..._==RRRR==AAAA==CCCCCC",
]
MAP_W, MAP_H = len(GAME_MAP[0]), len(GAME_MAP)

# 건물 종류: 글자 -> (색, 높이, 창문이 있는지)
WALLS = {
    "A": ((235, 150, 170), 2.0, True),
    "B": ((100, 195, 185), 1.6, True),
    "C": ((240, 205, 110), 1.2, True),
    "R": ((190, 95, 75), 2.5, True),
    "K": ((150, 110, 70), 1.0, False),
}
MAX_WALL = max(height for _, height, _ in WALLS.values())

# 바닥 종류: 글자 -> 색
FLOORS = {
    "~": (40, 110, 170),
    ".": (225, 200, 150),
    "_": (150, 105, 70),
    "=": (70, 70, 80),
    "p": (125, 90, 60),
    "g": (95, 160, 80),
}

WHITE = (240, 240, 240)
RED = (230, 50, 50)
YELLOW = (255, 220, 90)
GREEN = (90, 220, 120)
BLACK = (0, 0, 0)
HAZE = (250, 170, 140)            # 노을 빛 안개 색
SUN_ANGLE = math.pi               # 해는 서쪽(바다 쪽)에 있어요


# ---------------------------------------------------------------
# 맵 관련 도우미 함수
# ---------------------------------------------------------------
def floor_of(col, row):
    """그 칸의 바닥 종류. 'P', 'E', 'T' 같은 칸은 왼쪽 칸의 바닥을 따라가요."""
    while col >= 0:
        ch = GAME_MAP[row][col]
        if ch in FLOORS:
            return ch
        if ch == "W":
            return "p"
        col -= 1
    return "."


# 매번 계산하지 않도록 칸마다 바닥/건물 정보를 미리 만들어 둬요
FLOOR_GRID = [[floor_of(col, row) for col in range(MAP_W)] for row in range(MAP_H)]
WALL_GRID = [[WALLS.get(ch) for ch in line] for line in GAME_MAP]


def in_map(col, row):
    return 0 <= col < MAP_W and 0 <= row < MAP_H


def is_blocked(x, y):
    """그 위치로 걸어갈 수 없으면 True (건물, 바다, 야자수, 대관람차, 맵 바깥)"""
    col, row = int(x), int(y)
    if not in_map(col, row):
        return True
    ch = GAME_MAP[row][col]
    return ch in WALLS or ch in "~TW"


def is_opaque(x, y):
    """그 위치가 시야를 가리면 True (건물만 가려요)"""
    col, row = int(x), int(y)
    return in_map(col, row) and WALL_GRID[row][col] is not None


def find_cells(letter):
    """맵에서 특정 글자가 있는 칸들의 '가운데 좌표' 목록"""
    return [(col + 0.5, row + 0.5)
            for row, line in enumerate(GAME_MAP)
            for col, ch in enumerate(line) if ch == letter]


def can_see(a, b):
    """a에서 b까지 건물에 가리지 않고 직선으로 보이면 True"""
    dist = a.distance_to(b)
    steps = int(dist / 0.1) + 1
    for i in range(1, steps):
        p = a.lerp(b, i / steps)
        if is_opaque(p.x, p.y):
            return False
    return True


def move_with_collision(pos, delta, radius=0.2):
    """막힌 곳을 뚫지 않게 움직이기. x와 y를 따로 검사해서 벽을 따라 미끄러지게 해요."""
    new_x = pos.x + delta.x
    side_x = new_x + math.copysign(radius, delta.x) if delta.x else new_x
    if not is_blocked(side_x, pos.y):
        pos.x = new_x
    new_y = pos.y + delta.y
    side_y = new_y + math.copysign(radius, delta.y) if delta.y else new_y
    if not is_blocked(pos.x, side_y):
        pos.y = new_y


def cast_ray(px, py, angle):
    """한 방향으로 광선을 쏴서 지나가는 바닥과 건물을 기록해요 (DDA 알고리즘).

    돌려주는 값:
        floors: [(시작 거리, 끝 거리, 바닥 글자), ...]  첫 건물 앞까지의 바닥 구간들
        walls : [(거리, 세로벽인지, 벽에 맞은 위치 0~1, 건물 정보), ...]  가까운 순서
                앞 건물보다 높은 건물만 기록해요 (뒤에 있는 낮은 건물은 어차피 안 보이니까)
    """
    dx, dy = math.cos(angle), math.sin(angle)
    map_x, map_y = int(px), int(py)
    delta_x = abs(1 / dx) if dx != 0 else 1e30
    delta_y = abs(1 / dy) if dy != 0 else 1e30
    if dx < 0:
        step_x, side_x = -1, (px - map_x) * delta_x
    else:
        step_x, side_x = 1, (map_x + 1 - px) * delta_x
    if dy < 0:
        step_y, side_y = -1, (py - map_y) * delta_y
    else:
        step_y, side_y = 1, (map_y + 1 - py) * delta_y

    floors, walls = [], []
    seg_start = 0.0
    cur_floor = FLOOR_GRID[map_y][map_x]
    tallest = 0.0
    while True:
        # 가까운 격자선을 하나 넘어가기
        if side_x < side_y:
            dist = side_x
            side_x += delta_x
            map_x += step_x
            vertical = True
        else:
            dist = side_y
            side_y += delta_y
            map_y += step_y
            vertical = False

        if dist > MAX_DEPTH or not in_map(map_x, map_y):
            if not walls:                      # 건물이 없으면 바닥이 지평선까지 이어져요
                floors.append((seg_start, math.inf, cur_floor))
            break

        spec = WALL_GRID[map_y][map_x]
        if spec:
            if not walls:
                floors.append((seg_start, dist, cur_floor))
            if spec[1] > tallest:
                hit = py + dy * dist if vertical else px + dx * dist
                walls.append((dist, vertical, hit - math.floor(hit), spec))
                tallest = spec[1]
                if tallest >= MAX_WALL:
                    break
        elif not walls:
            f = FLOOR_GRID[map_y][map_x]
            if f != cur_floor:
                floors.append((seg_start, dist, cur_floor))
                seg_start, cur_floor = dist, f
    return floors, walls


def angle_diff(a, b):
    """두 각도의 차이를 -π ~ π 범위로"""
    return (a - b + math.pi) % (2 * math.pi) - math.pi


def fog(color, dist):
    """멀수록 노을 빛 안개 색에 가까워지게"""
    t = min(1.0, dist / FOG_DIST) * 0.8
    return tuple(int(c + (h - c) * t) for c, h in zip(color, HAZE))


def shade(color, amount):
    return tuple(int(c * amount) for c in color)


# ---------------------------------------------------------------
# 그림 만들기 (이미지 파일 없이 도형으로 그려요)
# ---------------------------------------------------------------
def make_soldier_image(flash=False, hurt=False):
    img = pygame.Surface((60, 120), pygame.SRCALPHA)
    uniform = (200, 200, 200) if hurt else (70, 85, 60)
    vest = (200, 200, 200) if hurt else (45, 50, 40)
    skin = (230, 200, 170)
    pygame.draw.rect(img, (40, 40, 45), (18, 80, 10, 40))      # 왼다리
    pygame.draw.rect(img, (40, 40, 45), (32, 80, 10, 40))      # 오른다리
    pygame.draw.rect(img, uniform, (12, 32, 36, 52), border_radius=6)   # 몸통
    pygame.draw.rect(img, vest, (16, 38, 28, 30), border_radius=4)      # 조끼
    pygame.draw.circle(img, skin, (30, 20), 12)                # 얼굴
    pygame.draw.rect(img, (50, 60, 45), (17, 4, 26, 12), border_radius=6)  # 헬멧
    pygame.draw.rect(img, BLACK, (24, 18, 12, 4))              # 고글
    pygame.draw.rect(img, (25, 25, 25), (26, 52, 30, 7))       # 총
    if flash:
        pygame.draw.circle(img, YELLOW, (56, 55), 8)           # 총구 불꽃
    return img


def make_palm_image():
    img = pygame.Surface((120, 240), pygame.SRCALPHA)
    # 살짝 휘어진 줄기
    for i in range(20):
        y = 236 - i * 10
        x = 60 + int(math.sin(i / 7) * 10)
        pygame.draw.rect(img, (120, 85, 50) if i % 2 else (100, 70, 40), (x - 6, y - 10, 12, 11))
    # 잎사귀: 꼭대기에서 사방으로 늘어진 선
    top = (60 + int(math.sin(19 / 7) * 10), 42)
    for angle in range(0, 360, 40):
        rad = math.radians(angle)
        end = (top[0] + math.cos(rad) * 55, top[1] + math.sin(rad) * 25 + 22)
        mid = (top[0] + math.cos(rad) * 30, top[1] + math.sin(rad) * 12 - 6)
        pygame.draw.line(img, (40, 120, 50), top, mid, 9)
        pygame.draw.line(img, (50, 140, 60), mid, end, 7)
    return img


def make_ferris_wheel_image():
    img = pygame.Surface((240, 280), pygame.SRCALPHA)
    center, radius = (120, 115), 105
    pygame.draw.line(img, (230, 230, 230), center, (40, 278), 6)    # 받침대
    pygame.draw.line(img, (230, 230, 230), center, (200, 278), 6)
    pygame.draw.circle(img, (240, 240, 240), center, radius, 5)
    pygame.draw.circle(img, (240, 240, 240), center, radius - 20, 2)
    colors = [(230, 60, 60), (250, 200, 60), (60, 180, 230), (120, 220, 120)]
    for i in range(12):
        rad = math.radians(i * 30)
        rim = (center[0] + math.cos(rad) * radius, center[1] + math.sin(rad) * radius)
        pygame.draw.line(img, (220, 220, 220), center, rim, 2)
        pygame.draw.rect(img, colors[i % 4], (rim[0] - 9, rim[1], 18, 14), border_radius=4)
    pygame.draw.circle(img, (250, 220, 120), center, 10)
    return img


def make_sky():
    """노을 하늘. 아래쪽 끝이 지평선에 오도록 그려요."""
    h = HEIGHT + MAX_PITCH * 2 + 200
    sky = pygame.Surface((WIDTH, h))
    stops = [(0.0, (40, 30, 90)), (0.55, (150, 70, 140)), (0.85, (245, 120, 120)), (1.0, HAZE)]
    for y in range(h):
        t = y / (h - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                color = tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
                pygame.draw.line(sky, color, (0, y), (WIDTH, y))
                break
    return sky


def make_scope_overlay():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 255))
    pygame.draw.circle(overlay, (0, 0, 0, 0), (WIDTH // 2, HEIGHT // 2), 270)
    pygame.draw.circle(overlay, (0, 0, 0, 255), (WIDTH // 2, HEIGHT // 2), 272, 4)
    pygame.draw.line(overlay, (0, 0, 0, 255), (WIDTH // 2 - 270, HEIGHT // 2), (WIDTH // 2 + 270, HEIGHT // 2), 2)
    pygame.draw.line(overlay, (0, 0, 0, 255), (WIDTH // 2, HEIGHT // 2 - 270), (WIDTH // 2, HEIGHT // 2 + 270), 2)
    return overlay


# ---------------------------------------------------------------
# 등장인물
# ---------------------------------------------------------------
class Enemy:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.hp = ENEMY_HP
        self.dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        self.spotted = 0.0        # 플레이어를 보고 있던 시간
        self.shoot_timer = 0.0
        self.flash_timer = 0.0    # 총구 불꽃 표시 시간
        self.hurt_timer = 0.0     # 맞았을 때 하얗게 번쩍이는 시간

    def update(self, dt, player):
        """적 행동. 플레이어에게 준 피해량을 돌려줘요."""
        self.flash_timer -= dt
        self.hurt_timer -= dt
        dist = self.pos.distance_to(player.pos)
        sees = dist < ENEMY_SIGHT and can_see(self.pos, player.pos)

        if not sees:
            # 못 봤을 때: 어슬렁거리다가 막히면 방향 바꾸기
            self.spotted = 0.0
            before = pygame.Vector2(self.pos)
            move_with_collision(self.pos, self.dir * ENEMY_SPEED * 0.6 * dt)
            if self.pos == before or random.random() < 0.005:
                self.dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            return 0

        # 봤을 때: 너무 멀면 다가오고, 반응 시간이 지나면 쏘기
        self.spotted += dt
        if dist > 4:
            move_with_collision(self.pos, (player.pos - self.pos).normalize() * ENEMY_SPEED * dt)
        if self.spotted < ENEMY_REACTION:
            return 0

        self.shoot_timer -= dt
        if self.shoot_timer > 0:
            return 0
        self.shoot_timer = random.uniform(0.35, 0.9)
        self.flash_timer = 0.08
        # 멀수록, 플레이어가 움직일수록 잘 안 맞아요
        chance = max(0.12, 0.65 - dist * 0.045 - (0.15 if player.moving else 0))
        if random.random() < chance:
            return random.randint(7, 13)
        return 0


class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        self.pitch = 0.0          # 위아래 시점 (+면 위를 봐요)
        self.hp = 100
        self.moving = False

    def update(self, dt, keys, mouse_dx, mouse_dy, scoped):
        slow = 0.35 if scoped else 1.0              # 조준경을 보면 감도를 낮춰요
        self.angle += mouse_dx * MOUSE_SENS * slow
        self.pitch -= mouse_dy * MOUSE_SENS_Y * slow
        if keys[pygame.K_LEFT]:
            self.angle -= TURN_SPEED * slow * dt
        if keys[pygame.K_RIGHT]:
            self.angle += TURN_SPEED * slow * dt
        if keys[pygame.K_UP]:
            self.pitch += LOOK_SPEED * slow * dt
        if keys[pygame.K_DOWN]:
            self.pitch -= LOOK_SPEED * slow * dt
        self.pitch = max(-MAX_PITCH, min(MAX_PITCH, self.pitch))

        forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
        right = pygame.Vector2(-forward.y, forward.x)
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w]:
            move += forward
        if keys[pygame.K_s]:
            move -= forward
        if keys[pygame.K_d]:
            move += right
        if keys[pygame.K_a]:
            move -= right
        self.moving = move.length() > 0
        if self.moving:
            move_with_collision(self.pos, move.normalize() * MOVE_SPEED * dt)


class Weapon:
    """무기 하나의 총알 수"""

    def __init__(self, spec):
        self.spec = spec
        self.mag = spec["mag"]
        self.reserve = spec["reserve"]


class Arsenal:
    """가지고 있는 무기들과 사격/재장전/반동/무기 교체를 관리"""

    SWITCH_TIME = 0.4

    def __init__(self):
        self.weapons = [Weapon(spec) for spec in WEAPONS]
        self.index = 0
        self.last_index = 1
        self.cooldown = 0.0
        self.reload_left = 0.0
        self.switch_left = 0.0
        self.recoil = 0.0          # 반동으로 시점이 위로 튄 정도(px)
        self.since_shot = 1.0
        self.kick = 0.0            # 화면 아래 총이 뒤로 밀리는 효과

    @property
    def current(self):
        return self.weapons[self.index]

    @property
    def busy(self):
        return self.reload_left > 0 or self.switch_left > 0

    def switch(self, index):
        index %= len(self.weapons)
        if index != self.index:
            self.last_index, self.index = self.index, index
            self.reload_left = 0.0             # 바꾸면 재장전은 취소
            self.switch_left = self.SWITCH_TIME

    def reload(self):
        w = self.current
        if not self.busy and w.mag < w.spec["mag"] and w.reserve > 0:
            self.reload_left = w.spec["reload"]

    def update(self, dt):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.switch_left = max(0.0, self.switch_left - dt)
        self.since_shot += dt
        self.kick = max(0.0, self.kick - dt * 6)
        if self.since_shot > 0.12:                     # 안 쏘면 반동이 서서히 돌아와요
            self.recoil = max(0.0, self.recoil - 220 * dt)
        if self.reload_left > 0:
            self.reload_left -= dt
            if self.reload_left <= 0:
                self.reload_left = 0.0
                w = self.current
                taken = min(w.spec["mag"] - w.mag, w.reserve)
                w.mag += taken
                w.reserve -= taken

    def try_fire(self):
        """쏠 수 있으면 총알 하나를 쓰고 True"""
        w = self.current
        if self.cooldown > 0 or self.busy:
            return False
        if w.mag == 0:
            self.reload()
            return False
        w.mag -= 1
        self.cooldown = w.spec["delay"]
        self.since_shot = 0.0
        return True

    def add_recoil(self):
        """총알이 나간 '뒤에' 시점을 위로 튀게 해요 (그래서 첫 발은 정확해요)"""
        self.recoil = min(140.0, self.recoil + self.current.spec["kick"])
        self.kick = 1.0


class Decor:
    """야자수, 대관람차 같은 장식물"""

    def __init__(self, x, y, image, height, width):
        self.pos = pygame.Vector2(x, y)
        self.image = image
        self.height = height
        self.width = width


# ---------------------------------------------------------------
# 게임 전체
# ---------------------------------------------------------------
class Game:
    def __init__(self):
        self.soldier = make_soldier_image()
        self.soldier_flash = make_soldier_image(flash=True)
        self.soldier_hurt = make_soldier_image(hurt=True)
        self.sky = make_sky()
        self.scope_overlay = make_scope_overlay()
        self.small_font = pygame.font.Font(None, 24)
        palm, wheel = make_palm_image(), make_ferris_wheel_image()
        self.decor = [Decor(x, y, palm, 2.4, 1.2) for x, y in find_cells("T")]
        self.decor += [Decor(x, y, wheel, 4.0, 3.4) for x, y in find_cells("W")]
        self.spawn_points = find_cells("E")
        self.zbuffer = [math.inf] * NUM_RAYS
        self.mouse_was_down = False
        self.reset()

    def reset(self):
        self.round = 1
        self.kills = 0
        self.game_over = False
        self.start_round()

    def start_round(self):
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.arsenal = Arsenal()
        far = [p for p in self.spawn_points if self.player.pos.distance_to(p) > SAFE_SPAWN]
        count = min(len(far), 2 + self.round)
        self.enemies = [Enemy(*p) for p in random.sample(far, count)]
        self.banner = f"ROUND {self.round}"
        self.banner_timer = 2.0
        self.round_clear_timer = 0.0
        self.damage_flash = 0.0
        self.hitmarker = 0.0
        self.hitmarker_kill = False
        self.scoped = False
        self.feed = []             # 킬 로그: [글자, 남은 시간]

    # ----- 시점 계산 -----
    @property
    def fov(self):
        return SCOPE_FOV if self.scoped else NORMAL_FOV

    @property
    def proj(self):
        """거리 1에 있는 높이 1짜리 물체가 화면에서 몇 px인지"""
        return (WIDTH / 2) / math.tan(self.fov / 2)

    @property
    def horizon(self):
        """지평선의 화면 y좌표. 위를 보거나 반동이 생기면 아래로 내려가요."""
        zoom = NORMAL_FOV / self.fov
        return HEIGHT / 2 + (self.player.pitch + self.arsenal.recoil) * zoom

    # ----- 입력 -----
    def handle_event(self, event):
        if self.game_over:
            return
        if event.type == pygame.MOUSEWHEEL:
            self.arsenal.switch(self.arsenal.index - event.y)
        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_4:
                self.arsenal.switch(event.key - pygame.K_1)
            elif event.key == pygame.K_q:
                self.arsenal.switch(self.arsenal.last_index)
            elif event.key == pygame.K_r:
                self.arsenal.reload()

    # ----- 게임 진행 -----
    def update(self, dt, keys, mouse_dx, mouse_dy, buttons):
        self.banner_timer -= dt
        self.damage_flash = max(0.0, self.damage_flash - dt * 2)
        self.hitmarker = max(0.0, self.hitmarker - dt)
        self.feed = [[text, t - dt] for text, t in self.feed if t - dt > 0]
        if self.game_over:
            return

        if self.round_clear_timer > 0:
            self.round_clear_timer -= dt
            if self.round_clear_timer <= 0:
                self.round += 1
                self.start_round()
            return

        arsenal = self.arsenal
        spec = arsenal.current.spec
        self.scoped = buttons[2] and spec["scope"] and not arsenal.busy
        self.player.update(dt, keys, mouse_dx, mouse_dy, self.scoped)
        arsenal.update(dt)

        # 자동 무기는 누르고 있으면 계속, 나머지는 누를 때마다 한 발
        clicked = buttons[0] and not self.mouse_was_down
        self.mouse_was_down = buttons[0]
        if (buttons[0] if spec["auto"] else clicked) and arsenal.try_fire():
            self.shoot(spec)
            arsenal.add_recoil()

        for enemy in self.enemies:
            damage = enemy.update(dt, self.player)
            if damage:
                self.player.hp -= damage
                self.damage_flash = 0.6
        if self.player.hp <= 0:
            self.player.hp = 0
            self.game_over = True

        if not self.enemies:
            self.round_clear_timer = 2.5
            self.banner = "ROUND CLEAR"
            self.banner_timer = 2.5

    def current_spread(self, spec):
        if spec["scope"]:
            spread = 1 if self.scoped else spec["spread"]
        else:
            spread = spec["spread"] + (self.arsenal.recoil * 0.1 if spec["auto"] else 0)
        if self.player.moving:
            spread += 40 if spec["scope"] else 16
        return spread

    def shoot(self, spec):
        """조준점(화면 가운데) 근처로 총알을 쏴서 맞은 적에게 피해를 줘요."""
        spread = self.current_spread(spec)
        damage = {}               # 적마다 받은 피해 (산탄총은 여러 발이 한 적에게 맞을 수 있어요)
        headshots = set()
        for _ in range(spec["pellets"]):
            ax = WIDTH / 2 + random.uniform(-spread, spread)
            ay = HEIGHT / 2 + random.uniform(-spread, spread) * 0.6
            target, target_dist, head = None, math.inf, False
            for enemy in self.enemies:
                box = self.project(enemy.pos, ENEMY_HEIGHT, 0.45)
                if not box:
                    continue
                sx, top, bottom, w, perp = box
                if not (sx - w / 2 <= ax <= sx + w / 2 and top <= ay <= bottom):
                    continue
                col = int(ax // COL_W)
                if 0 <= col < NUM_RAYS and perp > self.zbuffer[col]:
                    continue                      # 건물 뒤에 숨어 있음
                if perp < target_dist:
                    target, target_dist = enemy, perp
                    head = ay < top + (bottom - top) * 0.2   # 위쪽 20% = 머리
            if target:
                damage[target] = damage.get(target, 0) + (spec["head"] if head else spec["body"])
                if head:
                    headshots.add(target)

        for enemy, amount in damage.items():
            enemy.hp -= amount
            enemy.hurt_timer = 0.08
            enemy.spotted = max(enemy.spotted, ENEMY_REACTION)   # 맞으면 바로 반격
            self.hitmarker = 0.15
            self.hitmarker_kill = enemy.hp <= 0
            if enemy.hp <= 0:
                self.enemies.remove(enemy)
                self.kills += 1
                self.feed.append(["HEADSHOT!" if enemy in headshots else "ENEMY DOWN", 2.5])

    def project(self, pos, height, width):
        """월드 위치 → 화면 위치/크기. 시야 밖이면 None

        돌려주는 값: (가운데 x, 위 y, 아래 y, 폭, 거리)
        """
        offset = pos - self.player.pos
        dist = offset.length()
        rel = angle_diff(math.atan2(offset.y, offset.x), self.player.angle)
        if dist < 0.1 or abs(rel) > self.fov / 2 + 0.4:
            return None
        perp = max(0.2, dist * math.cos(rel))
        size = self.proj / perp               # 이 거리에서 높이 1이 몇 px인지
        sx = (rel + self.fov / 2) / self.fov * WIDTH
        bottom = self.horizon + EYE * size
        return sx, bottom - size * height, bottom, size * width, perp

    # ----- 화면 그리기 -----
    def draw(self, screen, font, big_font):
        self.draw_sky(screen)
        self.draw_world(screen)
        self.draw_sprites(screen)
        if self.scoped:
            screen.blit(self.scope_overlay, (0, 0))
        else:
            self.draw_gun(screen)
        self.draw_hud(screen, font, big_font)

    def draw_sky(self, screen):
        horizon = self.horizon
        screen.blit(self.sky, (0, horizon - self.sky.get_height()))
        # 서쪽 바다 위로 지는 해
        rel = angle_diff(SUN_ANGLE, self.player.angle)
        if abs(rel) < self.fov / 2 + 0.3:
            zoom = NORMAL_FOV / self.fov
            x = (rel + self.fov / 2) / self.fov * WIDTH
            y = horizon - 45 * zoom
            pygame.draw.circle(screen, (255, 200, 140), (x, y), 70 * zoom)
            pygame.draw.circle(screen, (255, 225, 160), (x, y), 48 * zoom)
            pygame.draw.circle(screen, (255, 245, 210), (x, y), 34 * zoom)
        pygame.draw.rect(screen, FLOORS["."], (0, horizon, WIDTH, max(0, HEIGHT - horizon)))

    def draw_world(self, screen):
        p = self.player
        horizon, proj, fov = self.horizon, self.proj, self.fov
        for i in range(NUM_RAYS):
            ray_angle = p.angle - fov / 2 + fov * (i + 0.5) / NUM_RAYS
            floors, walls = cast_ray(p.pos.x, p.pos.y, ray_angle)
            fix = math.cos(ray_angle - p.angle)     # 물고기 눈 왜곡 보정
            x = i * COL_W

            # 1) 바닥: 구간마다 색을 칠해요 (멀수록 지평선 가까이)
            for d0, d1, kind in floors:
                y_near = HEIGHT if d0 < 0.05 else horizon + EYE * proj / (d0 * fix)
                y_far = horizon if d1 == math.inf else horizon + EYE * proj / (d1 * fix)
                if y_near > y_far:
                    # 바닥은 벽보다 안개를 약하게 (바다가 회색으로 안 보이게)
                    color = fog(FLOORS[kind], (min(d1, FOG_DIST) + d0) * 0.3)
                    pygame.draw.rect(screen, color, (x, y_far, COL_W, min(HEIGHT, y_near) - y_far + 1))

            # 2) 건물: 먼 것부터 그려야 가까운 것이 앞에 보여요
            self.zbuffer[i] = walls[0][0] * fix if walls else math.inf
            for dist, vertical, wall_x, (color, height, windows) in reversed(walls):
                perp = max(0.05, dist * fix)
                size = proj / perp
                bottom = horizon + EYE * size
                top = bottom - height * size
                base = shade(color, 0.82 if vertical else 1.0)
                if wall_x < 0.03 or wall_x > 0.97:      # 건물 모서리 선
                    base = shade(base, 0.6)
                pygame.draw.rect(screen, fog(base, perp), (x, top, COL_W, bottom - top + 1))
                # 창문: 층마다 두 칸씩
                if windows and (0.18 < wall_x < 0.42 or 0.58 < wall_x < 0.82):
                    glass = fog((60, 80, 120) if vertical else (90, 110, 150), perp)
                    floor_count = int(height / 0.5)
                    for k in range(floor_count):
                        y0 = bottom - (k * 0.5 + 0.42) * size
                        y1 = bottom - (k * 0.5 + 0.17) * size
                        if y1 > 0 and y0 < HEIGHT:
                            pygame.draw.rect(screen, glass, (x, y0, COL_W, y1 - y0))

    def draw_sprites(self, screen):
        items = []
        for enemy in self.enemies:
            box = self.project(enemy.pos, ENEMY_HEIGHT, 0.45)
            if box:
                if enemy.hurt_timer > 0:
                    img = self.soldier_hurt
                elif enemy.flash_timer > 0:
                    img = self.soldier_flash
                else:
                    img = self.soldier
                items.append((box, img))
        for d in self.decor:
            box = self.project(d.pos, d.height, d.width)
            if box:
                items.append((box, d.image))
        # 먼 것부터 그려야 가까운 것이 앞에 보여요
        items.sort(key=lambda item: -item[0][4])
        for box, img in items:
            self.draw_sprite_columns(screen, img, *box)

    def draw_sprite_columns(self, screen, img, sx, top, bottom, w, perp):
        """그림을 세로 줄 단위로 잘라 그려요. 건물보다 뒤에 있는 줄은 건너뛰어요.

        화면에 보이는 부분만 잘라서 늘리기 때문에, 아주 가까이 있어도 느려지지 않아요.
        """
        h = bottom - top
        vis_top, vis_bottom = max(0.0, top), min(float(HEIGHT), bottom)
        if vis_bottom <= vis_top or w < 1:
            return
        img_w, img_h = img.get_size()
        v0 = int((vis_top - top) / h * img_h)
        v1 = min(img_h, max(v0 + 1, math.ceil((vis_bottom - top) / h * img_h)))
        x0 = sx - w / 2
        first = max(0, int(x0 // COL_W))
        last = min(NUM_RAYS - 1, int((x0 + w) // COL_W))
        out_h = int(vis_bottom - vis_top) + 1
        for col in range(first, last + 1):
            if perp >= self.zbuffer[col]:
                continue
            u = int((col * COL_W + COL_W / 2 - x0) / w * img_w)
            if not 0 <= u < img_w:
                continue
            strip = img.subsurface((u, v0, 1, v1 - v0))
            screen.blit(pygame.transform.scale(strip, (COL_W, out_h)), (col * COL_W, vis_top))

    def draw_gun(self, screen):
        # 걸을 때 흔들리고, 쏠 때 뒤로 밀리고, 재장전/교체할 때 내려가요
        a = self.arsenal
        t = pygame.time.get_ticks() / 1000
        bob = math.sin(t * 10) * 6 if self.player.moving else 0
        down = 0
        if a.reload_left > 0:
            down = 120
        elif a.switch_left > 0:
            down = 200 * a.switch_left / a.SWITCH_TIME
        x = WIDTH / 2 + 110 + bob
        y = HEIGHT - 150 + abs(bob) + a.kick * 18 + down
        name = a.current.spec["name"]
        dark, mid, wood = (35, 35, 38), (60, 60, 66), (120, 80, 45)

        if name == "RIFLE":
            pygame.draw.polygon(screen, dark, [(x, y + 40), (x + 40, y), (x + 120, y + 70),
                                               (x + 120, y + 160), (x + 30, y + 160)])
            pygame.draw.polygon(screen, mid, [(x + 10, y + 30), (x + 40, y + 5),
                                              (x + 60, y + 20), (x + 30, y + 50)])
            muzzle = (x + 22, y + 18)
        elif name == "PISTOL":
            pygame.draw.polygon(screen, dark, [(x + 20, y + 70), (x + 50, y + 40), (x + 100, y + 80),
                                               (x + 90, y + 160), (x + 45, y + 160)])
            pygame.draw.polygon(screen, mid, [(x + 25, y + 68), (x + 50, y + 45),
                                              (x + 70, y + 60), (x + 45, y + 82)])
            muzzle = (x + 35, y + 58)
        elif name == "SNIPER":
            pygame.draw.polygon(screen, (50, 55, 45), [(x - 30, y + 10), (x - 10, y - 15), (x + 130, y + 90),
                                                       (x + 130, y + 160), (x + 40, y + 160)])
            pygame.draw.polygon(screen, BLACK, [(x + 10, y + 5), (x + 30, y - 15),
                                                (x + 90, y + 30), (x + 70, y + 50)])   # 조준경
            muzzle = (x - 22, y + 0)
        else:  # SHOTGUN
            pygame.draw.polygon(screen, dark, [(x - 10, y + 40), (x + 30, y), (x + 70, y + 30),
                                               (x + 30, y + 70)])
            pygame.draw.polygon(screen, wood, [(x + 30, y + 70), (x + 70, y + 30), (x + 130, y + 90),
                                               (x + 130, y + 160), (x + 60, y + 160)])
            muzzle = (x + 8, y + 28)

        if a.kick > 0.6:
            pygame.draw.circle(screen, YELLOW, muzzle, 18)
            pygame.draw.circle(screen, WHITE, muzzle, 8)

    def draw_hud(self, screen, font, big_font):
        # 맞았을 때 화면이 붉게
        if self.damage_flash > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((200, 0, 0, int(110 * self.damage_flash)))
            screen.blit(overlay, (0, 0))

        # 조준선 (화면 가운데). 총알이 퍼지는 만큼 벌어져요
        cx, cy = WIDTH / 2, HEIGHT / 2
        spec = self.arsenal.current.spec
        if not self.scoped:
            gap = 5 + self.current_spread(spec) * 0.6
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                start = (cx + dx * gap, cy + dy * gap)
                end = (cx + dx * (gap + 10), cy + dy * (gap + 10))
                pygame.draw.line(screen, GREEN, start, end, 2)
        if self.hitmarker > 0:
            color = RED if self.hitmarker_kill else WHITE
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                pygame.draw.line(screen, color, (cx + dx * 5, cy + dy * 5), (cx + dx * 12, cy + dy * 12), 2)

        # 왼쪽 아래 체력, 오른쪽 아래 총알
        hp_color = GREEN if self.player.hp > 40 else RED
        screen.blit(big_font.render(f"+ {self.player.hp}", True, hp_color), (24, HEIGHT - 70))
        w = self.arsenal.current
        ammo = "RELOADING..." if self.arsenal.reload_left > 0 else f"{w.mag} / {w.reserve}"
        image = big_font.render(ammo, True, WHITE)
        screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, HEIGHT - 20)))

        # 아래 가운데 무기 칸
        slot_w = 110
        left = WIDTH / 2 - slot_w * len(WEAPONS) / 2
        for i, weapon in enumerate(self.arsenal.weapons):
            rect = pygame.Rect(left + i * slot_w + 4, HEIGHT - 44, slot_w - 8, 30)
            selected = i == self.arsenal.index
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 220, 90, 200) if selected else (0, 0, 0, 120))
            screen.blit(panel, rect)
            label = self.small_font.render(f"{i + 1} {weapon.spec['name']}", True, BLACK if selected else WHITE)
            screen.blit(label, label.get_rect(center=rect.center))

        # 위쪽 정보
        info = f"ROUND {self.round}   ENEMIES {len(self.enemies)}   KILLS {self.kills}"
        screen.blit(font.render(info, True, WHITE), (16, 12))
        map_bottom = self.draw_minimap(screen)
        for i, (text, _) in enumerate(self.feed[-4:]):
            image = font.render(text, True, YELLOW)
            screen.blit(image, image.get_rect(topright=(WIDTH - 12, map_bottom + 8 + i * 26)))

        if self.banner_timer > 0:
            self.center_text(screen, big_font, self.banner, YELLOW, HEIGHT / 3)
        if self.game_over:
            self.center_text(screen, big_font, "YOU DIED", RED, HEIGHT / 2 - 40)
            self.center_text(screen, font, f"Round {self.round}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10)
            self.center_text(screen, font, "R: retry   ESC: quit", WHITE, HEIGHT / 2 + 40)

    def draw_minimap(self, screen):
        """오른쪽 위 작은 지도. 지도 아래쪽 y좌표를 돌려줘요."""
        cell = 5
        ox, oy = WIDTH - MAP_W * cell - 12, 12
        mini = pygame.Surface((MAP_W * cell, MAP_H * cell), pygame.SRCALPHA)
        for row in range(MAP_H):
            for col in range(MAP_W):
                spec = WALL_GRID[row][col]
                color = spec[0] if spec else FLOORS[FLOOR_GRID[row][col]]
                pygame.draw.rect(mini, (*color, 190), (col * cell, row * cell, cell, cell))
        screen.blit(mini, (ox, oy))
        p = self.player.pos * cell + (ox, oy)
        look = p + pygame.Vector2(math.cos(self.player.angle), math.sin(self.player.angle)) * 10
        pygame.draw.line(screen, BLACK, p, look, 2)
        pygame.draw.circle(screen, BLACK, p, 3)
        return oy + MAP_H * cell

    @staticmethod
    def center_text(screen, font, text, color, y):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, y)))


async def run():
    """게임 한 판 실행. ESC를 누르면 끝나요.

    창을 닫으면 False, ESC로 끝내면 True를 돌려줘요 (메뉴로 돌아갈지 판단용).
    """
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Strike Zone: Santa Monica")
    fit_canvas()
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 56)

    # 마우스를 창 안에 가두고 커서 숨기기 (FPS 게임처럼)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()

    game = Game()
    running = True
    closed = False             # 창을 닫았는지 여부
    while running:
        dt = min(0.05, clock.tick(FPS) / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running, closed = False, True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and game.game_over:
                game.reset()
            else:
                game.handle_event(event)
        if not running:
            break

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        game.update(dt, pygame.key.get_pressed(), mouse_dx, mouse_dy, pygame.mouse.get_pressed())
        game.draw(screen, font, big_font)
        pygame.display.flip()
        # 웹 브라우저에서 화면이 멈추지 않도록 잠깐 차례를 넘겨줘요
        await asyncio.sleep(0)

    # 마우스 원래대로
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    return not closed


if __name__ == "__main__":
    pygame.init()
    asyncio.run(run())
    pygame.quit()
