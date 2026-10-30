"""
스트라이크 존 - 1인칭 총게임 (레이캐스팅 FPS)

규칙:
    - 맵 곳곳에 숨어 있는 적을 모두 쓰러뜨리면 라운드 승리.
    - 라운드가 올라갈수록 적이 많아져요.
    - 체력이 0이 되면 게임 오버.

조작:
    W A S D      : 앞/왼쪽/뒤/오른쪽 이동
    마우스       : 시점 돌리기 (←/→ 방향키도 가능)
    마우스 왼쪽  : 사격 (꾹 누르면 연사, 연사할수록 총구가 위로 튀어요)
    R            : 재장전
    ESC          : 종료

팁:
    - 머리를 맞히면 한 방(HEADSHOT)!
    - 멀리 있는 적은 연사 대신 끊어 쏘는 게 잘 맞아요.
    - 움직이면서 쏘면 총알이 더 많이 퍼져요.

실행 방법:
    pip install pygame
    python shooter.py

원리 (레이캐스팅):
    화면을 세로 줄 여러 개로 나누고, 줄마다 플레이어 눈에서 광선(ray)을 쏴서
    벽까지의 거리를 재요. 가까운 벽은 길게, 먼 벽은 짧게 그리면 3D처럼 보여요.
"""

import math
import random

import pygame

# ---------------------------------------------------------------
# 화면 / 게임 설정값
# ---------------------------------------------------------------
WIDTH, HEIGHT = 960, 600
FPS = 60
FOV = math.radians(66)            # 시야각 (넓을수록 많이 보여요)
COL_W = 4                         # 세로 줄 하나의 폭(px). 작을수록 선명하지만 느려져요
NUM_RAYS = WIDTH // COL_W
PROJ = (WIDTH / 2) / math.tan(FOV / 2)   # 거리 → 화면 크기로 바꿀 때 쓰는 값
MAX_DEPTH = 30

MOVE_SPEED = 3.2                  # 1초에 몇 칸 움직이는지
TURN_SPEED = 2.6                  # 방향키로 돌 때 속도
MOUSE_SENS = 0.0025               # 마우스 감도

MAG_SIZE = 30                     # 탄창 하나에 든 총알
RESERVE_AMMO = 120                # 여분 총알
FIRE_DELAY = 0.1                  # 연사 간격(초)
RELOAD_TIME = 1.8
BODY_DAMAGE = 34                  # 몸통: 3발이면 쓰러짐
HEAD_DAMAGE = 100                 # 머리: 한 방

ENEMY_HP = 100
ENEMY_SPEED = 1.4
ENEMY_SIGHT = 12                  # 적이 플레이어를 알아보는 거리
ENEMY_REACTION = 0.7              # 적이 처음 발견하고 쏘기까지 걸리는 시간

# 맵: '#' 벽, '.' 바닥, 'P' 플레이어 시작 위치, 'E' 적이 나타날 수 있는 위치
GAME_MAP = [
    "########################",
    "#P.....#.......#.......#",
    "#......#.......#...E...#",
    "#..##..#..###..#..##...#",
    "#..##.....#E#.....##...#",
    "#.........#.#..........#",
    "####..#####.#####..#####",
    "#......................#",
    "#..E...##......##...E..#",
    "#......##......##......#",
    "####..#####.#####..#####",
    "#.........#.#..........#",
    "#..##.....#E#.....##...#",
    "#..##..#..###..#..##.E.#",
    "#..E...#.......#.......#",
    "#......#...E...#.......#",
    "########################",
]
MAP_W, MAP_H = len(GAME_MAP[0]), len(GAME_MAP)

WHITE = (240, 240, 240)
RED = (230, 50, 50)
YELLOW = (255, 220, 90)
GREEN = (90, 220, 120)
BLACK = (0, 0, 0)


# ---------------------------------------------------------------
# 맵 관련 도우미 함수
# ---------------------------------------------------------------
def is_wall(x, y):
    """(x, y) 위치가 벽이면 True. 맵 바깥도 벽으로 취급해요."""
    col, row = int(x), int(y)
    if not (0 <= col < MAP_W and 0 <= row < MAP_H):
        return True
    return GAME_MAP[row][col] == "#"


def find_cells(letter):
    """맵에서 특정 글자가 있는 칸들의 '가운데 좌표' 목록"""
    cells = []
    for row, line in enumerate(GAME_MAP):
        for col, ch in enumerate(line):
            if ch == letter:
                cells.append((col + 0.5, row + 0.5))
    return cells


def can_see(a, b):
    """a에서 b까지 벽에 가리지 않고 직선으로 보이면 True"""
    dist = a.distance_to(b)
    steps = int(dist / 0.1) + 1
    for i in range(1, steps):
        p = a.lerp(b, i / steps)
        if is_wall(p.x, p.y):
            return False
    return True


def move_with_collision(pos, delta, radius=0.2):
    """벽을 뚫지 않게 움직이기. x와 y를 따로 검사해서 벽을 따라 미끄러지게 해요."""
    new_x = pos.x + delta.x
    side_x = new_x + math.copysign(radius, delta.x) if delta.x else new_x
    if not is_wall(side_x, pos.y):
        pos.x = new_x
    new_y = pos.y + delta.y
    side_y = new_y + math.copysign(radius, delta.y) if delta.y else new_y
    if not is_wall(pos.x, side_y):
        pos.y = new_y


def cast_ray(px, py, angle):
    """한 방향으로 광선을 쏴서 벽까지의 거리를 구해요 (DDA 알고리즘).

    돌려주는 값: (거리, 세로벽인지 여부, 벽에 맞은 위치 0~1)
    """
    dx, dy = math.cos(angle), math.sin(angle)
    map_x, map_y = int(px), int(py)
    # 광선이 격자 한 칸을 가로지르는 데 필요한 길이
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

    # 가까운 격자선부터 하나씩 넘어가며 벽을 만날 때까지 반복
    vertical = False
    for _ in range(MAX_DEPTH * 2):
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
        if is_wall(map_x, map_y):
            hit = py + dy * dist if vertical else px + dx * dist
            return dist, vertical, hit - math.floor(hit)
    return MAX_DEPTH, False, 0.0


def angle_diff(a, b):
    """두 각도의 차이를 -π ~ π 범위로"""
    return (a - b + math.pi) % (2 * math.pi) - math.pi


# ---------------------------------------------------------------
# 적 그림 만들기 (이미지 파일 없이 도형으로 그려요)
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
            # 못 봤을 때: 어슬렁거리다가 벽에 막히면 방향 바꾸기
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
        self.hp = 100
        self.moving = False

    def update(self, dt, keys, mouse_dx):
        self.angle += mouse_dx * MOUSE_SENS
        if keys[pygame.K_LEFT]:
            self.angle -= TURN_SPEED * dt
        if keys[pygame.K_RIGHT]:
            self.angle += TURN_SPEED * dt

        forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
        right = pygame.Vector2(-forward.y, forward.x)
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move += forward
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move -= forward
        if keys[pygame.K_d]:
            move += right
        if keys[pygame.K_a]:
            move -= right
        self.moving = move.length() > 0
        if self.moving:
            move_with_collision(self.pos, move.normalize() * MOVE_SPEED * dt)


class Gun:
    """총알 수, 재장전, 반동을 관리"""

    def __init__(self):
        self.mag = MAG_SIZE
        self.reserve = RESERVE_AMMO
        self.cooldown = 0.0
        self.reload_left = 0.0
        self.recoil = 0.0          # 총구가 위로 튄 정도(px)
        self.since_shot = 1.0
        self.kick = 0.0            # 화면 아래 총이 뒤로 밀리는 효과

    def reload(self):
        if self.reload_left == 0 and self.mag < MAG_SIZE and self.reserve > 0:
            self.reload_left = RELOAD_TIME

    def update(self, dt):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.since_shot += dt
        self.kick = max(0.0, self.kick - dt * 8)
        if self.since_shot > 0.15:                     # 안 쏘면 반동이 서서히 돌아와요
            self.recoil = max(0.0, self.recoil - 140 * dt)
        if self.reload_left > 0:
            self.reload_left -= dt
            if self.reload_left <= 0:
                self.reload_left = 0.0
                need = MAG_SIZE - self.mag
                taken = min(need, self.reserve)
                self.mag += taken
                self.reserve -= taken

    def try_fire(self):
        """쏠 수 있으면 총알 하나를 쓰고 True"""
        if self.cooldown > 0 or self.reload_left > 0:
            return False
        if self.mag == 0:
            self.reload()
            return False
        self.mag -= 1
        self.cooldown = FIRE_DELAY
        self.since_shot = 0.0
        self.recoil = min(80.0, self.recoil + 7)
        self.kick = 1.0
        return True


class Game:
    def __init__(self):
        self.soldier = make_soldier_image()
        self.soldier_flash = make_soldier_image(flash=True)
        self.soldier_hurt = make_soldier_image(hurt=True)
        self.background = self.make_background()
        self.spawn_points = find_cells("E")
        self.zbuffer = [MAX_DEPTH] * NUM_RAYS
        self.reset()

    @staticmethod
    def make_background():
        """천장과 바닥을 그라데이션으로 미리 그려두기"""
        bg = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT // 2):
            t = y / (HEIGHT / 2)
            pygame.draw.line(bg, (int(60 - 30 * t), int(65 - 30 * t), int(80 - 30 * t)), (0, y), (WIDTH, y))
        for y in range(HEIGHT // 2, HEIGHT):
            t = (y - HEIGHT / 2) / (HEIGHT / 2)
            c = int(35 + 55 * t)
            pygame.draw.line(bg, (c, c - 5, c - 10), (0, y), (WIDTH, y))
        return bg

    def reset(self):
        self.round = 1
        self.kills = 0
        self.game_over = False
        self.start_round()

    def start_round(self):
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.gun = Gun()
        count = min(len(self.spawn_points), 2 + self.round)
        self.enemies = [Enemy(*p) for p in random.sample(self.spawn_points, count)]
        self.banner = f"ROUND {self.round}"
        self.banner_timer = 2.0
        self.round_clear_timer = 0.0
        self.damage_flash = 0.0
        self.hitmarker = 0.0
        self.hitmarker_kill = False
        self.feed = []             # 화면 오른쪽 위 킬 로그: [글자, 남은 시간]

    # ----- 게임 진행 -----
    def update(self, dt, keys, mouse_dx, mouse_down):
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

        self.player.update(dt, keys, mouse_dx)
        self.gun.update(dt)
        if keys[pygame.K_r]:
            self.gun.reload()
        if mouse_down and self.gun.try_fire():
            self.shoot()

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

    def aim_point(self):
        """반동이 적용된 조준점(화면 좌표)"""
        return WIDTH / 2, HEIGHT / 2 - self.gun.recoil

    def shoot(self):
        """총알 한 발: 조준점에 걸린 가장 가까운 적을 맞혀요."""
        spread = 3 + self.gun.recoil * 0.25 + (18 if self.player.moving else 0)
        ax, ay = self.aim_point()
        ax += random.uniform(-spread, spread)
        ay += random.uniform(-spread, spread) * 0.5

        target, target_dist, headshot = None, None, False
        for enemy in self.enemies:
            box = self.project(enemy)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            if not (sx - w / 2 <= ax <= sx + w / 2 and top <= ay <= bottom):
                continue
            col = int(ax // COL_W)
            if 0 <= col < NUM_RAYS and perp > self.zbuffer[col]:
                continue                      # 벽 뒤에 숨어 있음
            if target is None or perp < target_dist:
                target, target_dist = enemy, perp
                headshot = ay < top + (bottom - top) * 0.2   # 위쪽 20% = 머리

        if target is None:
            return
        target.hp -= HEAD_DAMAGE if headshot else BODY_DAMAGE
        target.hurt_timer = 0.08
        target.spotted = max(target.spotted, ENEMY_REACTION)   # 맞으면 바로 반격
        self.hitmarker = 0.15
        self.hitmarker_kill = target.hp <= 0
        if target.hp <= 0:
            self.enemies.remove(target)
            self.kills += 1
            self.feed.append(["HEADSHOT!" if headshot else "ENEMY DOWN", 2.5])

    def project(self, enemy):
        """적의 월드 위치 → 화면 위치/크기. 시야 밖이면 None"""
        offset = enemy.pos - self.player.pos
        dist = offset.length()
        rel = angle_diff(math.atan2(offset.y, offset.x), self.player.angle)
        if dist < 0.1 or abs(rel) > FOV / 2 + 0.3:
            return None
        perp = max(0.2, dist * math.cos(rel))
        size = PROJ / perp                    # 이 거리에서 벽 높이(px)
        sx = (rel + FOV / 2) / FOV * WIDTH
        bottom = HEIGHT / 2 + size / 2
        top = bottom - size * 0.9
        return sx, top, bottom, size * 0.45, perp

    # ----- 화면 그리기 -----
    def draw(self, screen, font, big_font):
        screen.blit(self.background, (0, 0))
        self.draw_walls(screen)
        self.draw_enemies(screen)
        self.draw_gun(screen)
        self.draw_hud(screen, font, big_font)

    def draw_walls(self, screen):
        p = self.player
        for i in range(NUM_RAYS):
            ray_angle = p.angle - FOV / 2 + FOV * (i + 0.5) / NUM_RAYS
            dist, vertical, wall_x = cast_ray(p.pos.x, p.pos.y, ray_angle)
            perp = max(0.01, dist * math.cos(ray_angle - p.angle))   # 물고기 눈 왜곡 보정
            self.zbuffer[i] = perp
            h = min(HEIGHT * 3, PROJ / perp)
            # 멀수록 어둡게, 세로벽은 살짝 더 어둡게 → 입체감
            shade = max(0.18, 1 - perp / 16) * (0.8 if vertical else 1.0)
            base = (60, 60, 50) if wall_x < 0.04 or wall_x > 0.96 else (150, 140, 120)
            color = tuple(int(c * shade) for c in base)
            pygame.draw.rect(screen, color, (i * COL_W, HEIGHT / 2 - h / 2, COL_W, h))

    def draw_enemies(self, screen):
        # 먼 적부터 그려야 가까운 적이 앞에 보여요
        boxes = []
        for enemy in self.enemies:
            box = self.project(enemy)
            if box:
                boxes.append((box, enemy))
        boxes.sort(key=lambda item: -item[0][4])

        for (sx, top, bottom, w, perp), enemy in boxes:
            if enemy.hurt_timer > 0:
                img = self.soldier_hurt
            elif enemy.flash_timer > 0:
                img = self.soldier_flash
            else:
                img = self.soldier
            h = bottom - top
            sprite = pygame.transform.scale(img, (max(1, int(w)), max(1, int(h))))
            x0 = int(sx - w / 2)
            # 세로 줄 단위로 그리면서, 벽보다 뒤에 있는 부분은 건너뛰어요
            for col in range(max(0, x0 // COL_W), min(NUM_RAYS, int(sx + w / 2) // COL_W + 1)):
                if perp < self.zbuffer[col]:
                    cx = col * COL_W
                    screen.blit(sprite, (cx, top), area=pygame.Rect(cx - x0, 0, COL_W, h))

    def draw_gun(self, screen):
        # 걸을 때 총이 살짝 흔들리고, 쏠 때 뒤로 밀려요
        t = pygame.time.get_ticks() / 1000
        bob = math.sin(t * 10) * 6 if self.player.moving else 0
        down = 120 if self.gun.reload_left > 0 else 0
        x = WIDTH / 2 + 120 + bob
        y = HEIGHT - 150 + abs(bob) + self.gun.kick * 18 + down
        pygame.draw.polygon(screen, (35, 35, 38), [(x, y + 40), (x + 40, y), (x + 120, y + 70),
                                                   (x + 120, y + 160), (x + 30, y + 160)])
        pygame.draw.polygon(screen, (55, 55, 60), [(x + 10, y + 30), (x + 40, y + 5),
                                                   (x + 60, y + 20), (x + 30, y + 50)])
        if self.gun.kick > 0.6:
            pygame.draw.circle(screen, YELLOW, (int(x + 22), int(y + 18)), 16)
            pygame.draw.circle(screen, WHITE, (int(x + 22), int(y + 18)), 7)

    def draw_hud(self, screen, font, big_font):
        # 맞았을 때 화면이 붉게
        if self.damage_flash > 0:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((200, 0, 0, int(110 * self.damage_flash)))
            screen.blit(overlay, (0, 0))

        # 조준선: 반동만큼 위로, 퍼짐만큼 벌어져요
        ax, ay = self.aim_point()
        gap = 6 + self.gun.recoil * 0.25 + (18 if self.player.moving else 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            start = (ax + dx * gap, ay + dy * gap)
            end = (ax + dx * (gap + 10), ay + dy * (gap + 10))
            pygame.draw.line(screen, GREEN, start, end, 2)
        if self.hitmarker > 0:
            color = RED if self.hitmarker_kill else WHITE
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                pygame.draw.line(screen, color, (ax + dx * 5, ay + dy * 5), (ax + dx * 12, ay + dy * 12), 2)

        # 왼쪽 아래 체력, 오른쪽 아래 총알
        hp_color = GREEN if self.player.hp > 40 else RED
        screen.blit(big_font.render(f"+ {self.player.hp}", True, hp_color), (24, HEIGHT - 70))
        ammo = "RELOADING..." if self.gun.reload_left > 0 else f"{self.gun.mag} / {self.gun.reserve}"
        image = big_font.render(ammo, True, WHITE)
        screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, HEIGHT - 20)))

        # 위쪽 정보
        info = f"ROUND {self.round}   ENEMIES {len(self.enemies)}   KILLS {self.kills}"
        screen.blit(font.render(info, True, WHITE), (16, 12))
        for i, (text, _) in enumerate(self.feed[-4:]):
            image = font.render(text, True, YELLOW)
            screen.blit(image, image.get_rect(topright=(WIDTH - 200, 12 + i * 26)))
        self.draw_minimap(screen)

        if self.banner_timer > 0:
            self.center_text(screen, big_font, self.banner, YELLOW, HEIGHT / 3)
        if self.game_over:
            self.center_text(screen, big_font, "YOU DIED", RED, HEIGHT / 2 - 40)
            self.center_text(screen, font, f"Round {self.round}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10)
            self.center_text(screen, font, "R: retry   ESC: quit", WHITE, HEIGHT / 2 + 40)

    def draw_minimap(self, screen):
        cell = 7
        ox, oy = WIDTH - MAP_W * cell - 12, 12
        mini = pygame.Surface((MAP_W * cell, MAP_H * cell), pygame.SRCALPHA)
        mini.fill((0, 0, 0, 120))
        for row, line in enumerate(GAME_MAP):
            for col, ch in enumerate(line):
                if ch == "#":
                    pygame.draw.rect(mini, (170, 170, 170, 200), (col * cell, row * cell, cell, cell))
        screen.blit(mini, (ox, oy))
        p = self.player.pos * cell + (ox, oy)
        look = p + pygame.Vector2(math.cos(self.player.angle), math.sin(self.player.angle)) * 10
        pygame.draw.line(screen, YELLOW, p, look, 2)
        pygame.draw.circle(screen, YELLOW, p, 3)

    @staticmethod
    def center_text(screen, font, text, color, y):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, y)))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Strike Zone")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 30)
    big_font = pygame.font.Font(None, 56)

    # 마우스를 창 안에 가두고 커서 숨기기 (FPS 게임처럼)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()

    game = Game()
    running = True
    while running:
        dt = min(0.05, clock.tick(FPS) / 1000)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game.game_over:
                    game.reset()

        mouse_dx = pygame.mouse.get_rel()[0]
        mouse_down = pygame.mouse.get_pressed()[0]
        game.update(dt, pygame.key.get_pressed(), mouse_dx, mouse_down)
        game.draw(screen, font, big_font)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
