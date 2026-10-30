"""
스트라이크 존: 산타모니카 - 1인칭 총게임 (레이캐스팅 FPS)

노을 지는 산타모니카 해변. 바다, 모래사장, 야자수, 대관람차가 있는 부두,
파스텔색 건물이 늘어선 시내 곳곳에 숨어 있는 적을 모두 쓰러뜨리세요.

규칙:
    - 적을 모두 쓰러뜨리면 라운드 승리. 라운드가 올라갈수록 적이 많아지고 종류도 늘어나요.
    - 체력이 0이 되면 게임 오버.

적 종류:
    일반병    : 평범한 적
    돌격병    : 빨간 모자. 빠르게 달려들어요. 체력은 낮지만 가까이서 아파요
    저격수    : 2라운드부터. 멀리서 쏴요. 쏘기 전에 빨간 불빛이 반짝여요
    중장갑병  : 3라운드부터. 체력 300. 느리지만 총알을 쉴 새 없이 쏴요

조작:
    W A S D          : 이동
    스페이스바       : 점프
    마우스           : 시점 (좌우 + 위아래)
    ← → / ↑ ↓        : 키보드로 시점 돌리기 (좌우 / 위아래)
    마우스 왼쪽      : 사격
    마우스 오른쪽    : 저격총 조준경 (조준경을 보면서 휠: 3배 / 6배 / 12배 확대)
    1 2 3 4 / 휠     : 무기 바꾸기 (소총 / 권총 / 저격총 / 산탄총)
    Q                : 방금 쓰던 무기로
    R                : 재장전
    ESC              : 종료 (메뉴로)

팁:
    - 머리를 맞히면 큰 피해(HEADSHOT)! 적의 머리는 내 눈높이보다 조금 위에 있어요.
    - 쏘면 반동으로 시점이 위로 튀어요. 마우스를 살짝 내리면서 쏘면 잘 맞아요.
    - 점프하면 적 총알이 덜 맞지만, 내 총알도 퍼져요.

실행 방법:
    pip install pygame
    python shooter.py

원리 (레이캐스팅):
    화면을 세로 줄 여러 개로 나누고, 줄마다 플레이어 눈에서 광선(ray)을 쏴서
    바닥과 벽까지의 거리를 재요. 가까운 것은 크게, 먼 것은 작게 그리면 3D처럼 보여요.
    세로 줄이 가늘수록 선명하지만 느려져요. 그래서 컴퓨터 속도에 맞춰 줄 폭을 자동으로 바꿔요.
"""

import asyncio
import math
import random
import sys
import time

import pygame

from browser import fit_canvas

# ---------------------------------------------------------------
# 화면 / 게임 설정값
# ---------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
UI = HEIGHT / 600                 # 화면 크기에 맞춰 글자/총 그림을 키우는 비율
FPS = 60
IN_BROWSER = sys.platform == "emscripten"
START_COL_W = 4 if IN_BROWSER else 2   # 세로 줄 하나의 폭(px). 작을수록 선명
MIN_COL_W, MAX_COL_W = 2, 8       # 자동 해상도 조절 범위
FRAME_BUDGET = 0.014              # 한 장면 계산에 이보다 오래 걸리면 줄 폭을 넓혀요(초)
NORMAL_FOV = math.radians(66)     # 시야각
SCOPE_ZOOMS = [3, 6, 12]          # 저격총 조준경 배율
MAX_DEPTH = 60                    # 이보다 먼 곳은 안 그려요
EYE = 0.5                         # 눈높이 (1 = 건물 한 층 높이)
FOG_DIST = 32                     # 이 거리쯤 가면 노을 빛 안개에 묻혀요

MOVE_SPEED = 3.2                  # 1초에 몇 칸 움직이는지
TURN_SPEED = 2.6                  # ←/→ 키로 돌 때 속도
LOOK_SPEED = 420 * UI             # ↑/↓ 키로 위아래 볼 때 속도
MOUSE_SENS = 0.0025               # 마우스 좌우 감도
MOUSE_SENS_Y = 1.0                # 마우스 위아래 감도
MAX_PITCH = 260 * UI              # 위아래로 볼 수 있는 한계(px)
JUMP_SPEED = 4.2                  # 점프 힘
GRAVITY = 13                      # 중력 (클수록 빨리 떨어져요)

SAFE_SPAWN = 8                    # 시작할 때 이 거리 안에는 적이 안 나와요

# 무기 목록
#   auto   : 꾹 누르면 연사되는지
#   delay  : 다음 발까지 걸리는 시간(초)
#   body / head : 몸통 / 머리 데미지
#   spread : 총알이 퍼지는 정도(px)
#   kick   : 한 발 쏠 때 시점이 위로 튀는 정도(px)
#   pellets: 한 번에 나가는 총알 수 (산탄총)
WEAPONS = [
    dict(name="RIFLE", auto=True, delay=0.1, mag=30, reserve=120, body=34, head=100,
         spread=4, kick=9, reload=1.8, pellets=1, scope=False),
    dict(name="PISTOL", auto=False, delay=0.15, mag=12, reserve=60, body=40, head=100,
         spread=2, kick=16, reload=1.2, pellets=1, scope=False),
    dict(name="SNIPER", auto=False, delay=1.2, mag=5, reserve=25, body=150, head=300,
         spread=45, kick=50, reload=2.5, pellets=1, scope=True),
    dict(name="SHOTGUN", auto=False, delay=0.8, mag=8, reserve=32, body=20, head=40,
         spread=50, kick=40, reload=2.2, pellets=8, scope=False),
]

# 적 종류
#   hp       : 체력            speed : 이동 속도        sight : 플레이어를 알아보는 거리
#   reaction : 발견 후 첫 사격까지 시간                 keep  : 이 거리까지만 다가와요
#   range    : 이보다 멀면 안 쏴요                      fire  : 사격 간격(초) 범위
#   damage   : 한 발 피해 범위  accuracy : 명중률       falloff : 거리 1칸마다 줄어드는 명중률
#   height / width : 크기 (눈높이 0.5 기준)
#   look     : 생김새 (옷 색, 머리 장비, 총 길이)
ENEMY_TYPES = {
    "GRUNT": dict(hp=100, speed=1.4, sight=14, reaction=0.7, keep=4, range=14,
                  fire=(0.35, 0.9), damage=(7, 13), accuracy=0.65, falloff=0.045,
                  height=0.9, width=0.45,
                  look=dict(uniform=(70, 85, 60), vest=(45, 50, 40), pants=(40, 40, 45),
                            head="helmet", gun=30)),
    "RUSHER": dict(hp=60, speed=3.0, sight=12, reaction=0.4, keep=1.2, range=6,
                   fire=(0.6, 1.0), damage=(12, 20), accuracy=0.8, falloff=0.05,
                   height=0.85, width=0.42,
                   look=dict(uniform=(240, 130, 60), vest=(250, 210, 90), pants=(60, 80, 140),
                             head="cap", gun=22)),
    "SNIPER": dict(hp=80, speed=0.6, sight=30, reaction=1.4, keep=99, range=30,
                   fire=(2.2, 3.0), damage=(30, 40), accuracy=0.6, falloff=0.008,
                   height=0.9, width=0.45,
                   look=dict(uniform=(175, 160, 110), vest=(140, 125, 85), pants=(120, 105, 75),
                             head="hood", gun=40)),
    "HEAVY": dict(hp=300, speed=0.9, sight=14, reaction=0.9, keep=5, range=14,
                  fire=(0.1, 0.18), damage=(3, 5), accuracy=0.35, falloff=0.03,
                  height=1.0, width=0.62,
                  look=dict(uniform=(50, 55, 75), vest=(30, 32, 45), pants=(35, 35, 45),
                            head="heavy", gun=34)),
}

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


def fog(color, dist, fog_dist):
    """멀수록 노을 빛 안개 색에 가까워지게"""
    t = min(1.0, dist / fog_dist) * 0.8
    return tuple(int(c + (h - c) * t) for c, h in zip(color, HAZE))


def shade(color, amount):
    return tuple(int(c * amount) for c in color)


# ---------------------------------------------------------------
# 그림 만들기 (이미지 파일 없이 도형으로 그려요)
# ---------------------------------------------------------------
def make_enemy_image(look, state="normal"):
    """적 그림. state: normal(평소) / flash(총구 불꽃) / hurt(맞음) / aim(저격 조준 불빛)"""
    img = pygame.Surface((60, 120), pygame.SRCALPHA)
    hurt = state == "hurt"
    pale = (210, 210, 210)
    uniform = pale if hurt else look["uniform"]
    vest = pale if hurt else look["vest"]
    pants = pale if hurt else look["pants"]
    skin = (230, 200, 170)
    heavy = look["head"] == "heavy"

    pygame.draw.rect(img, pants, (16 if heavy else 18, 80, 12, 40))       # 왼다리
    pygame.draw.rect(img, pants, (32, 80, 12, 40))                        # 오른다리
    if heavy:
        pygame.draw.rect(img, uniform, (4, 28, 52, 58), border_radius=8)  # 두꺼운 갑옷
        pygame.draw.rect(img, vest, (10, 34, 40, 36), border_radius=6)
    else:
        pygame.draw.rect(img, uniform, (12, 32, 36, 52), border_radius=6)  # 몸통
        pygame.draw.rect(img, vest, (16, 38, 28, 30), border_radius=4)     # 조끼

    head = look["head"]
    if head == "helmet":
        pygame.draw.circle(img, skin, (30, 20), 12)
        pygame.draw.rect(img, (50, 60, 45), (17, 4, 26, 12), border_radius=6)
        pygame.draw.rect(img, BLACK, (24, 18, 12, 4))                     # 고글
    elif head == "cap":
        pygame.draw.circle(img, skin, (30, 20), 12)
        pygame.draw.rect(img, (210, 40, 40), (18, 6, 24, 9), border_radius=5)   # 빨간 모자
        pygame.draw.rect(img, (210, 40, 40), (28, 12, 18, 4))                    # 챙
        pygame.draw.rect(img, BLACK, (23, 19, 14, 3))                            # 선글라스
    elif head == "hood":
        pygame.draw.circle(img, look["vest"] if not hurt else pale, (30, 19), 14)   # 위장 두건
        pygame.draw.rect(img, skin, (22, 16, 16, 9))
        pygame.draw.rect(img, BLACK, (24, 18, 12, 3))
    else:  # heavy
        pygame.draw.circle(img, (40, 42, 55) if not hurt else pale, (30, 17), 15)   # 통 헬멧
        pygame.draw.rect(img, (120, 200, 230), (20, 14, 20, 6))                     # 바이저

    gun = look["gun"]
    pygame.draw.rect(img, (25, 25, 25), (26, 52, gun, 8 if heavy else 7))         # 총
    if state == "flash":
        pygame.draw.circle(img, YELLOW, (min(59, 26 + gun), 55), 8)               # 총구 불꽃
    if state == "aim":
        pygame.draw.circle(img, (255, 40, 40), (34, 50), 6)                       # 조준경 반짝임
        pygame.draw.circle(img, WHITE, (34, 50), 2)
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
    h = int(HEIGHT + MAX_PITCH * 2 + 200)
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
    cx, cy, r = WIDTH // 2, HEIGHT // 2, int(HEIGHT * 0.46)
    pygame.draw.circle(overlay, (0, 0, 0, 0), (cx, cy), r)
    pygame.draw.circle(overlay, (0, 0, 0, 255), (cx, cy), r + 2, 4)
    pygame.draw.line(overlay, (0, 0, 0, 255), (cx - r, cy), (cx + r, cy), 2)
    pygame.draw.line(overlay, (0, 0, 0, 255), (cx, cy - r), (cx, cy + r), 2)
    # 거리 가늠용 눈금
    for i in range(1, 5):
        pygame.draw.line(overlay, (0, 0, 0, 255), (cx - 8, cy + i * r // 6), (cx + 8, cy + i * r // 6), 2)
    return overlay


# ---------------------------------------------------------------
# 등장인물
# ---------------------------------------------------------------
class Enemy:
    def __init__(self, x, y, kind):
        self.kind = kind
        self.t = ENEMY_TYPES[kind]           # 이 종류의 능력치
        self.pos = pygame.Vector2(x, y)
        self.hp = self.t["hp"]
        self.dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        self.sees = False
        self.los_timer = random.uniform(0, 0.2)   # 시야 검사는 0.2초마다 (계산 아끼기)
        self.spotted = 0.0        # 플레이어를 보고 있던 시간
        self.shoot_timer = 0.0
        self.flash_timer = 0.0    # 총구 불꽃 표시 시간
        self.hurt_timer = 0.0     # 맞았을 때 하얗게 번쩍이는 시간

    @property
    def aiming(self):
        """저격수가 곧 쏠 때 True (빨간 불빛으로 미리 알려줘요)"""
        return self.kind == "SNIPER" and self.sees and self.spotted > 0.4 and self.shoot_timer < 0.8

    def update(self, dt, player):
        """적 행동. 플레이어에게 준 피해량을 돌려줘요."""
        t = self.t
        self.flash_timer -= dt
        self.hurt_timer -= dt
        dist = self.pos.distance_to(player.pos)
        self.los_timer -= dt
        if self.los_timer <= 0:
            self.los_timer = 0.2
            self.sees = dist < t["sight"] and can_see(self.pos, player.pos)

        if not self.sees:
            # 못 봤을 때: 어슬렁거리다가 막히면 방향 바꾸기
            self.spotted = 0.0
            before = pygame.Vector2(self.pos)
            move_with_collision(self.pos, self.dir * t["speed"] * 0.6 * dt)
            if self.pos == before or random.random() < 0.005:
                self.dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
            return 0

        # 봤을 때: 너무 멀면 다가오고, 반응 시간이 지나면 쏘기
        self.spotted += dt
        if dist > t["keep"]:
            move_with_collision(self.pos, (player.pos - self.pos).normalize() * t["speed"] * dt)
        if self.spotted < t["reaction"] or dist > t["range"]:
            return 0

        self.shoot_timer -= dt
        if self.shoot_timer > 0:
            return 0
        self.shoot_timer = random.uniform(*t["fire"])
        self.flash_timer = 0.08
        # 멀수록, 플레이어가 움직이거나 점프 중일수록 잘 안 맞아요
        chance = t["accuracy"] - dist * t["falloff"]
        if player.moving:
            chance -= 0.15
        if player.z > 0:
            chance -= 0.15
        if random.random() < max(0.08, chance):
            return random.randint(*t["damage"])
        return 0


class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        self.pitch = 0.0          # 위아래 시점 (+면 위를 봐요)
        self.z = 0.0              # 점프 높이
        self.vz = 0.0             # 위아래 속도
        self.hp = 100
        self.moving = False

    def update(self, dt, keys, mouse_dx, mouse_dy, sens):
        """sens: 조준경으로 확대했을 때 감도를 낮추는 비율"""
        self.angle += mouse_dx * MOUSE_SENS * sens
        self.pitch -= mouse_dy * MOUSE_SENS_Y * sens
        if keys[pygame.K_LEFT]:
            self.angle -= TURN_SPEED * sens * dt
        if keys[pygame.K_RIGHT]:
            self.angle += TURN_SPEED * sens * dt
        if keys[pygame.K_UP]:
            self.pitch += LOOK_SPEED * sens * dt
        if keys[pygame.K_DOWN]:
            self.pitch -= LOOK_SPEED * sens * dt
        self.pitch = max(-MAX_PITCH, min(MAX_PITCH, self.pitch))

        # 점프: 땅에 있을 때만 뛸 수 있고, 중력 때문에 다시 떨어져요
        if keys[pygame.K_SPACE] and self.z == 0:
            self.vz = JUMP_SPEED
        self.vz -= GRAVITY * dt
        self.z = max(0.0, self.z + self.vz * dt)
        if self.z == 0:
            self.vz = 0.0

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
        self.zoom_index = 0        # 조준경 배율 (SCOPE_ZOOMS 중 몇 번째)

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
        # 적 그림: (종류, 상태)마다 하나씩 미리 만들어 둬요
        self.enemy_images = {
            (kind, state): make_enemy_image(t["look"], state)
            for kind, t in ENEMY_TYPES.items()
            for state in ("normal", "flash", "hurt", "aim")
        }
        self.sky = make_sky()
        self.scope_overlay = make_scope_overlay()
        self.font = pygame.font.Font(None, int(30 * UI))
        self.big_font = pygame.font.Font(None, int(56 * UI))
        self.small_font = pygame.font.Font(None, int(24 * UI))
        palm, wheel = make_palm_image(), make_ferris_wheel_image()
        self.decor = [Decor(x, y, palm, 2.4, 1.2) for x, y in find_cells("T")]
        self.decor += [Decor(x, y, wheel, 4.0, 3.4) for x, y in find_cells("W")]
        self.spawn_points = find_cells("E")
        self.set_col_w(START_COL_W)
        self.mouse_was_down = False
        self.reset()

    def set_col_w(self, col_w):
        """세로 줄 폭 바꾸기 (작을수록 선명, 클수록 빠름)"""
        self.col_w = col_w
        self.num_rays = math.ceil(WIDTH / col_w)
        self.zbuffer = [math.inf] * self.num_rays

    def adjust_quality(self, frame_time):
        """한 장면 계산 시간을 보고 선명도를 자동으로 조절해요."""
        if frame_time > FRAME_BUDGET and self.col_w < MAX_COL_W:
            self.set_col_w(self.col_w + 1)
        elif (self.col_w > MIN_COL_W
              and frame_time * self.col_w / (self.col_w - 1) < FRAME_BUDGET * 0.75):
            self.set_col_w(self.col_w - 1)

    def reset(self):
        self.round = 1
        self.kills = 0
        self.game_over = False
        self.start_round()

    def pick_enemy_kind(self):
        """라운드가 올라갈수록 새로운 적이 섞여 나와요"""
        pool = ["GRUNT"] * 3 + ["RUSHER"] * 2
        if self.round >= 2:
            pool += ["SNIPER"] * 2
        if self.round >= 3:
            pool += ["HEAVY"] * 2
        return random.choice(pool)

    def start_round(self):
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.arsenal = Arsenal()
        far = [p for p in self.spawn_points if self.player.pos.distance_to(p) > SAFE_SPAWN]
        count = min(len(far), 2 + self.round)
        self.enemies = [Enemy(*p, self.pick_enemy_kind()) for p in random.sample(far, count)]
        # 새로운 적이 처음 나오는 라운드에는 그 적이 꼭 한 명은 있게
        news = {2: "SNIPER", 3: "HEAVY"}
        new_kind = news.get(self.round)
        if new_kind:
            first = self.enemies[0]
            self.enemies[0] = Enemy(first.pos.x, first.pos.y, new_kind)
        self.banner = f"ROUND {self.round}"
        self.sub_banner = f"NEW ENEMY: {new_kind}" if new_kind else ""
        self.banner_timer = 2.5
        self.round_clear_timer = 0.0
        self.damage_flash = 0.0
        self.hitmarker = 0.0
        self.hitmarker_kill = False
        self.scoped = False
        self.feed = []             # 킬 로그: [글자, 남은 시간]

    # ----- 시점 계산 -----
    @property
    def zoom(self):
        return SCOPE_ZOOMS[self.arsenal.zoom_index] if self.scoped else 1

    @property
    def fov(self):
        # 배율만큼 시야를 좁혀요 (tan을 써야 정확히 '몇 배'가 돼요)
        return 2 * math.atan(math.tan(NORMAL_FOV / 2) / self.zoom)

    @property
    def proj(self):
        """거리 1에 있는 높이 1짜리 물체가 화면에서 몇 px인지"""
        return (WIDTH / 2) / math.tan(self.fov / 2)

    @property
    def horizon(self):
        """지평선의 화면 y좌표. 위를 보거나 반동이 생기면 아래로 내려가요."""
        return HEIGHT / 2 + (self.player.pitch + self.arsenal.recoil) * self.zoom

    @property
    def eye(self):
        """눈높이. 점프하면 높아져요."""
        return EYE + self.player.z

    @property
    def fog_dist(self):
        # 조준경으로 보면 안개가 걷혀서 멀리까지 선명해요
        return FOG_DIST * min(4, self.zoom)

    # ----- 입력 -----
    def handle_event(self, event):
        if self.game_over:
            return
        a = self.arsenal
        if event.type == pygame.MOUSEWHEEL:
            if self.scoped:      # 조준경을 보고 있으면 휠로 확대/축소
                a.zoom_index = max(0, min(len(SCOPE_ZOOMS) - 1, a.zoom_index + event.y))
            else:
                a.switch(a.index - event.y)
        elif event.type == pygame.KEYDOWN:
            if pygame.K_1 <= event.key <= pygame.K_4:
                a.switch(event.key - pygame.K_1)
            elif event.key == pygame.K_q:
                a.switch(a.last_index)
            elif event.key == pygame.K_r:
                a.reload()

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
        self.player.update(dt, keys, mouse_dx, mouse_dy, min(1.0, 1.5 / self.zoom))
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
                self.damage_flash = min(1.0, 0.4 + damage / 40)
        if self.player.hp <= 0:
            self.player.hp = 0
            self.game_over = True

        if not self.enemies:
            self.round_clear_timer = 2.5
            self.banner = "ROUND CLEAR"
            self.sub_banner = ""
            self.banner_timer = 2.5

    def current_spread(self, spec):
        if spec["scope"]:
            spread = 1 if self.scoped else spec["spread"]
        else:
            spread = spec["spread"] + (self.arsenal.recoil * 0.1 if spec["auto"] else 0)
        if self.player.moving:
            spread += 40 if spec["scope"] else 16
        if self.player.z > 0:
            spread += 25
        return spread * UI

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
                box = self.project(enemy.pos, enemy.t["height"], enemy.t["width"])
                if not box:
                    continue
                sx, top, bottom, w, perp = box
                if not (sx - w / 2 <= ax <= sx + w / 2 and top <= ay <= bottom):
                    continue
                col = int(ax // self.col_w)
                if 0 <= col < self.num_rays and perp > self.zbuffer[col]:
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
            enemy.spotted = max(enemy.spotted, enemy.t["reaction"])   # 맞으면 바로 반격
            enemy.sees = True
            self.hitmarker = 0.15
            self.hitmarker_kill = enemy.hp <= 0
            if enemy.hp <= 0:
                self.enemies.remove(enemy)
                self.kills += 1
                how = "HEADSHOT!" if enemy in headshots else "DOWN"
                self.feed.append([f"{enemy.kind} {how}", 2.5])

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
        sx = WIDTH / 2 + math.tan(rel) * self.proj if abs(rel) < 1.4 else (WIDTH * 2 if rel > 0 else -WIDTH)
        bottom = self.horizon + self.eye * size
        return sx, bottom - size * height, bottom, size * width, perp

    # ----- 화면 그리기 -----
    def draw(self, screen):
        self.draw_sky(screen)
        self.draw_world(screen)
        self.draw_sprites(screen)
        if self.scoped:
            screen.blit(self.scope_overlay, (0, 0))
            label = self.font.render(f"x{self.zoom}", True, WHITE)
            screen.blit(label, label.get_rect(center=(WIDTH / 2 + HEIGHT * 0.3, HEIGHT / 2 + HEIGHT * 0.3)))
        else:
            self.draw_gun(screen)
        self.draw_hud(screen)

    def ray_angle(self, i):
        """i번째 세로 줄이 바라보는 방향. 화면에 평평하게 펼쳐지도록 tan으로 계산해요."""
        x = (i + 0.5) * self.col_w - WIDTH / 2
        return self.player.angle + math.atan(x / self.proj)

    def draw_sky(self, screen):
        horizon = self.horizon
        screen.blit(self.sky, (0, horizon - self.sky.get_height()))
        # 서쪽 바다 위로 지는 해
        rel = angle_diff(SUN_ANGLE, self.player.angle)
        if abs(rel) < self.fov / 2 + 0.3:
            z = min(2, self.zoom)            # 조준경으로 봐도 해가 화면을 다 가리지 않게
            x = WIDTH / 2 + math.tan(rel) * self.proj
            y = horizon - 45 * UI * z
            pygame.draw.circle(screen, (255, 200, 140), (x, y), 70 * UI * z)
            pygame.draw.circle(screen, (255, 225, 160), (x, y), 48 * UI * z)
            pygame.draw.circle(screen, (255, 245, 210), (x, y), 34 * UI * z)
        pygame.draw.rect(screen, FLOORS["."], (0, horizon, WIDTH, max(0, HEIGHT - horizon)))

    def draw_world(self, screen):
        p = self.player
        horizon, proj, eye, fog_dist, col_w = self.horizon, self.proj, self.eye, self.fog_dist, self.col_w
        for i in range(self.num_rays):
            ray_angle = self.ray_angle(i)
            floors, walls = cast_ray(p.pos.x, p.pos.y, ray_angle)
            fix = math.cos(ray_angle - p.angle)     # 물고기 눈 왜곡 보정
            x = i * col_w

            # 1) 바닥: 구간마다 색을 칠해요 (멀수록 지평선 가까이)
            for d0, d1, kind in floors:
                y_near = HEIGHT if d0 < 0.05 else horizon + eye * proj / (d0 * fix)
                y_far = horizon if d1 == math.inf else horizon + eye * proj / (d1 * fix)
                if y_near > y_far and y_far < HEIGHT:
                    # 바닥은 벽보다 안개를 약하게 (바다가 회색으로 안 보이게)
                    color = fog(FLOORS[kind], (min(d1, fog_dist) + d0) * 0.3, fog_dist)
                    pygame.draw.rect(screen, color, (x, y_far, col_w, min(HEIGHT, y_near) - y_far + 1))

            # 2) 건물: 먼 것부터 그려야 가까운 것이 앞에 보여요
            self.zbuffer[i] = walls[0][0] * fix if walls else math.inf
            for dist, vertical, wall_x, (color, height, windows) in reversed(walls):
                perp = max(0.05, dist * fix)
                size = proj / perp
                bottom = horizon + eye * size
                top = bottom - height * size
                if top > HEIGHT or bottom < 0:
                    continue
                base = shade(color, 0.82 if vertical else 1.0)
                if wall_x < 0.03 or wall_x > 0.97:      # 건물 모서리 선
                    base = shade(base, 0.6)
                pygame.draw.rect(screen, fog(base, perp, fog_dist), (x, top, col_w, bottom - top + 1))
                # 창문: 층마다 두 칸씩
                if windows and (0.18 < wall_x < 0.42 or 0.58 < wall_x < 0.82):
                    glass = fog((60, 80, 120) if vertical else (90, 110, 150), perp, fog_dist)
                    for k in range(int(height / 0.5)):
                        y0 = bottom - (k * 0.5 + 0.42) * size
                        y1 = bottom - (k * 0.5 + 0.17) * size
                        if y1 > 0 and y0 < HEIGHT:
                            pygame.draw.rect(screen, glass, (x, y0, col_w, y1 - y0))

    def draw_sprites(self, screen):
        items = []
        for enemy in self.enemies:
            box = self.project(enemy.pos, enemy.t["height"], enemy.t["width"])
            if box:
                if enemy.hurt_timer > 0:
                    state = "hurt"
                elif enemy.flash_timer > 0:
                    state = "flash"
                elif enemy.aiming:
                    state = "aim"
                else:
                    state = "normal"
                items.append((box, self.enemy_images[(enemy.kind, state)], enemy))
        for d in self.decor:
            box = self.project(d.pos, d.height, d.width)
            if box:
                items.append((box, d.image, None))
        # 먼 것부터 그려야 가까운 것이 앞에 보여요
        items.sort(key=lambda item: -item[0][4])
        for box, img, enemy in items:
            self.draw_sprite_columns(screen, img, *box)
            if enemy and enemy.hp < enemy.t["hp"]:
                self.draw_hp_bar(screen, enemy, box)

    def draw_hp_bar(self, screen, enemy, box):
        """다친 적 머리 위에 체력 막대"""
        sx, top, bottom, w, perp = box
        col = int(sx // self.col_w)
        if not (0 <= col < self.num_rays) or perp >= self.zbuffer[col]:
            return
        bar_w = max(20, w * 0.9)
        rect = pygame.Rect(sx - bar_w / 2, top - 10 * UI, bar_w, max(3, 5 * UI))
        pygame.draw.rect(screen, BLACK, rect)
        rect.width = int(bar_w * max(0, enemy.hp) / enemy.t["hp"])
        pygame.draw.rect(screen, RED, rect)

    def draw_sprite_columns(self, screen, img, sx, top, bottom, w, perp):
        """그림을 세로 줄 단위로 잘라 그려요. 건물보다 뒤에 있는 줄은 건너뛰어요.

        화면에 보이는 부분만 잘라서 늘리기 때문에, 아주 가까이 있어도 느려지지 않아요.
        """
        h = bottom - top
        vis_top, vis_bottom = max(0.0, top), min(float(HEIGHT), bottom)
        if vis_bottom <= vis_top or w < 1:
            return
        col_w = self.col_w
        img_w, img_h = img.get_size()
        v0 = int((vis_top - top) / h * img_h)
        v1 = min(img_h, max(v0 + 1, math.ceil((vis_bottom - top) / h * img_h)))
        x0 = sx - w / 2
        first = max(0, int(x0 // col_w))
        last = min(self.num_rays - 1, int((x0 + w) // col_w))
        out_h = int(vis_bottom - vis_top) + 1
        for col in range(first, last + 1):
            if perp >= self.zbuffer[col]:
                continue
            u = int((col * col_w + col_w / 2 - x0) / w * img_w)
            if not 0 <= u < img_w:
                continue
            strip = img.subsurface((u, v0, 1, v1 - v0))
            screen.blit(pygame.transform.scale(strip, (col_w, out_h)), (col * col_w, vis_top))

    def draw_gun(self, screen):
        # 걸을 때 흔들리고, 쏠 때 뒤로 밀리고, 재장전/교체할 때 내려가요
        a = self.arsenal
        t = pygame.time.get_ticks() / 1000
        bob = math.sin(t * 10) * 6 if self.player.moving and self.player.z == 0 else 0
        down = 0
        if a.reload_left > 0:
            down = 120
        elif a.switch_left > 0:
            down = 200 * a.switch_left / a.SWITCH_TIME
        x = WIDTH / 2 + 110 * UI + bob
        y = HEIGHT - 150 * UI + abs(bob) + (a.kick * 18 + down) * UI

        def at(dx, dy):
            """총 그림 기준점에서 (dx, dy)만큼 떨어진 화면 좌표 (화면 크기에 맞춰 키워요)"""
            return (x + dx * UI, y + dy * UI)

        def poly(color, points):
            pygame.draw.polygon(screen, color, [at(px, py) for px, py in points])

        name = a.current.spec["name"]
        dark, mid, wood = (35, 35, 38), (60, 60, 66), (120, 80, 45)
        if name == "RIFLE":
            poly(dark, [(0, 40), (40, 0), (120, 70), (120, 160), (30, 160)])
            poly(mid, [(10, 30), (40, 5), (60, 20), (30, 50)])
            muzzle = at(22, 18)
        elif name == "PISTOL":
            poly(dark, [(20, 70), (50, 40), (100, 80), (90, 160), (45, 160)])
            poly(mid, [(25, 68), (50, 45), (70, 60), (45, 82)])
            muzzle = at(35, 58)
        elif name == "SNIPER":
            poly((50, 55, 45), [(-30, 10), (-10, -15), (130, 90), (130, 160), (40, 160)])
            poly(BLACK, [(10, 5), (30, -15), (90, 30), (70, 50)])         # 조준경
            muzzle = at(-22, 0)
        else:  # SHOTGUN
            poly(dark, [(-10, 40), (30, 0), (70, 30), (30, 70)])
            poly(wood, [(30, 70), (70, 30), (130, 90), (130, 160), (60, 160)])
            muzzle = at(8, 28)

        if a.kick > 0.6:
            pygame.draw.circle(screen, YELLOW, muzzle, 18 * UI)
            pygame.draw.circle(screen, WHITE, muzzle, 8 * UI)

    def draw_hud(self, screen):
        font, big_font = self.font, self.big_font
        # 맞았을 때 화면이 붉게
        if self.damage_flash > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((200, 0, 0, int(110 * self.damage_flash)))
            screen.blit(overlay, (0, 0))

        # 조준선 (화면 가운데). 총알이 퍼지는 만큼 벌어져요
        cx, cy = WIDTH / 2, HEIGHT / 2
        spec = self.arsenal.current.spec
        if not self.scoped:
            gap = 5 * UI + self.current_spread(spec) * 0.6
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                start = (cx + dx * gap, cy + dy * gap)
                end = (cx + dx * (gap + 10 * UI), cy + dy * (gap + 10 * UI))
                pygame.draw.line(screen, GREEN, start, end, 2)
        if self.hitmarker > 0:
            color = RED if self.hitmarker_kill else WHITE
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                pygame.draw.line(screen, color, (cx + dx * 5 * UI, cy + dy * 5 * UI),
                                 (cx + dx * 12 * UI, cy + dy * 12 * UI), 2)

        # 왼쪽 아래 체력, 오른쪽 아래 총알
        hp_color = GREEN if self.player.hp > 40 else RED
        screen.blit(big_font.render(f"+ {self.player.hp}", True, hp_color), (24, HEIGHT - 70 * UI))
        w = self.arsenal.current
        ammo = "RELOADING..." if self.arsenal.reload_left > 0 else f"{w.mag} / {w.reserve}"
        image = big_font.render(ammo, True, WHITE)
        screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, HEIGHT - 20 * UI)))

        # 아래 가운데 무기 칸
        slot_w = 110 * UI
        left = WIDTH / 2 - slot_w * len(WEAPONS) / 2
        for i, weapon in enumerate(self.arsenal.weapons):
            rect = pygame.Rect(left + i * slot_w + 4, HEIGHT - 44 * UI, slot_w - 8, 30 * UI)
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
            screen.blit(image, image.get_rect(topright=(WIDTH - 12, map_bottom + 8 + i * 30 * UI)))

        if self.banner_timer > 0:
            self.center_text(screen, big_font, self.banner, YELLOW, HEIGHT / 3)
            if self.sub_banner:
                self.center_text(screen, font, self.sub_banner, RED, HEIGHT / 3 + 45 * UI)
        if self.game_over:
            self.center_text(screen, big_font, "YOU DIED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"Round {self.round}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, "R: retry   ESC: quit", WHITE, HEIGHT / 2 + 40 * UI)

    def draw_minimap(self, screen):
        """오른쪽 위 작은 지도. 지도 아래쪽 y좌표를 돌려줘요."""
        cell = int(5 * UI)
        ox, oy = WIDTH - MAP_W * cell - 12, 12
        mini = pygame.Surface((MAP_W * cell, MAP_H * cell), pygame.SRCALPHA)
        for row in range(MAP_H):
            for col in range(MAP_W):
                spec = WALL_GRID[row][col]
                color = spec[0] if spec else FLOORS[FLOOR_GRID[row][col]]
                pygame.draw.rect(mini, (*color, 190), (col * cell, row * cell, cell, cell))
        screen.blit(mini, (ox, oy))
        p = self.player.pos * cell + (ox, oy)
        look = p + pygame.Vector2(math.cos(self.player.angle), math.sin(self.player.angle)) * 12
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

    # 마우스를 창 안에 가두고 커서 숨기기 (FPS 게임처럼)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()

    game = Game()
    running = True
    closed = False             # 창을 닫았는지 여부
    work_time, frames, check_timer = 0.0, 0, 0.0   # 자동 해상도 조절용 기록
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

        started = time.perf_counter()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        game.update(dt, pygame.key.get_pressed(), mouse_dx, mouse_dy, pygame.mouse.get_pressed())
        game.draw(screen)
        work_time += time.perf_counter() - started
        frames += 1
        check_timer += dt
        if check_timer >= 1.0:                   # 1초마다 선명도 조절
            game.adjust_quality(work_time / frames)
            work_time, frames, check_timer = 0.0, 0, 0.0

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
