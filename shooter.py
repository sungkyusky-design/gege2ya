"""
스트라이크 존 - 1인칭 총게임 (레이캐스팅 FPS)

세 가지 모드:
    캠페인    : 100라운드 (맵 20개 x 5세트: 기본/강습/밤/폭풍우/베테랑). 라운드가 오를수록 적이 강해져요.
    좀비 모드 : 핏빛 달이 뜬 마을에서 좀비 웨이브를 버텨요. 점수로 탄약과 총 강화를 사요.
    미션      : 아주 큰 맵에서 다섯 단계 장기 작전. 단계마다 체크포인트에 저장돼요.

RPG: 계급이 오르면 스킬 포인트(K), 계급/점수로 새 무기를 얻고, 무기는 쓸수록 레벨이 올라요.
    스킬 T 집중(적이 느려짐) / Y 구급상자 / J 탐지(벽 너머 적 표시)

시작 전에 로드아웃(주무기 / 보조무기 / 퍼크)을 골라요.
    퍼크: HEAVY ROUNDS 피해+25%, QUICK HANDS 재장전 빠르게, LIGHTFOOT 조용한 발걸음,
          IRON SKIN 체력 130, SCAVENGER 탄약 1.5배

규칙:
    - 적을 모두 쓰러뜨리면 라운드 승리. 라운드가 올라갈수록 적이 많아지고 종류도 늘어나요.
    - 체력이 0이 되면 R: 그 라운드부터 다시 / N: 처음부터.
    - 진행한 라운드는 저장돼요. 다음에 켜면 C로 이어할 수 있어요.
    - 쓰러진 적은 탄약/체력/수류탄 상자를 떨어뜨려요. 맵 곳곳에도 상자가 있어요.

적 종류:
    일반병    : 평범한 적
    돌격병    : 빨간 모자. 빠르게 달려들어요. 체력은 낮지만 가까이서 아파요
    저격수    : 2라운드부터. 멀리서 쏴요. 쏘기 전에 빨간 불빛이 반짝여요
    중장갑병  : 3라운드부터. 체력 300. 느리지만 총알을 쉴 새 없이 쏴요
    폭탄병    : 4라운드부터. 수류탄을 던져요. GRENADE! 경고가 뜨면 피하세요
    방패병    : 6라운드부터. 앞에서 쏘면 방패에 막혀요. 머리를 노리거나 옆으로 돌아가세요
    보스      : 5라운드마다. 흰 정장. 체력 900, 연사와 수류탄
    측면 공격병: 7라운드부터. 크게 피하며 파고들어 가까이서 산탄총
    의무병    : 8라운드부터. 근처 적을 치료해요. 먼저 노리세요
    기관총 진지: 9라운드부터. 모래주머니 뒤에서 움직이지 않고 연사
    (좀비 모드: 좀비, 러너, 브루트, 폭탄 좀비, 침 좀비)

조작 (키보드만으로 다 할 수 있어요):
    W A S D          : 이동
    Shift            : 달리기 (W와 함께. 달리는 동안은 못 쏴요)
    C                : 앉기 / 일어나기. 달리다가 누르면 슬라이딩
    스페이스바       : 점프
    ← → / ↑ ↓        : 시점 돌리기 (좌우 / 위아래)    = 마우스
    F                : 사격 (꾹 누르면 연사)          = 마우스 왼쪽
    E                : 정조준 켜기/끄기 (저격총은 조준경) = 마우스 오른쪽 클릭
    Z                : 저격총 조준경 배율 (3 → 6 → 12배) = 조준경을 보면서 휠
    G                : 수류탄 던지기
    V                : 칼 공격
    1, 2             : 주무기 / 보조무기 = 휠
    B / U            : 좀비 모드 상점 - 탄약 가득(500점) / 들고 있는 총 강화(2500점)
    X                : 킬스트릭 쓰기 (죽지 않고 3킬 레이더 / 5킬 공습 / 7킬 자동 포탑)
    Q                : 방금 쓰던 무기로
    R                : 재장전
    H                : 도움말 (보는 동안 일시정지)
    M                : 소리 끄기 / 켜기
    P 또는 F3        : FPS와 화면 선명도 표시
    Enter 또는 F11   : 전체 화면 (컴퓨터에서 실행할 때)
    ESC              : 일시정지 메뉴 (계속 / 도움말 / 설정 / 메뉴로 나가기)

시작 화면:
    Enter : 캠페인    Z : 좀비 모드    C : 이어하기    T : 해상도 바꾸기 (컴퓨터에서)
로드아웃 화면:
    ↑↓ : 줄 고르기    ←→ : 바꾸기    Enter : 시작    ESC : 뒤로

점수와 계급:
    처치 +100, 헤드샷·칼 +50, 연속 처치 메달(DOUBLE / TRIPLE KILL), 라운드 클리어 +250.
    경험치 1000마다 계급(RANK)이 올라가고, 저장돼요.

실행 방법:
    pip install pygame
    python shooter.py

원리 (레이캐스팅):
    화면을 세로 줄 여러 개로 나누고, 줄마다 플레이어 눈에서 광선(ray)을 쏴서
    바닥과 벽까지의 거리를 재요. 가까운 것은 크게, 먼 것은 작게 그리면 3D처럼 보여요.
    세로 줄이 가늘수록 선명하지만 느려져요. 그래서 컴퓨터 속도에 맞춰 줄 폭을 자동으로 바꿔요.
"""

import array
import copy
import asyncio
import math
import random
import sys
import time
from collections import deque
import datetime

import pygame

from browser import load_save, prepare_window, write_save

# ---------------------------------------------------------------
# 화면 / 게임 설정값
# ---------------------------------------------------------------
WIDTH, HEIGHT = 1280, 720
UI = HEIGHT / 600                 # 화면 크기에 맞춰 글자/총 그림을 키우는 비율
FPS = 60
IN_BROWSER = sys.platform == "emscripten"
START_COL_W = 4 if IN_BROWSER else 2   # 세로 줄 하나의 폭(px). 작을수록 선명
MIN_COL_W = 2 if IN_BROWSER else 1     # 컴퓨터에서는 1px(가장 선명)까지 올라가요
MAX_COL_W = 8
FRAME_BUDGET = 0.014              # 한 장면 계산에 이보다 오래 걸리면 줄 폭을 넓혀요(초)
# 부서지는 엄폐물: 글자 -> 체력 (상자, 모래주머니). 총알과 폭발에 부서져요
DESTRUCTIBLE = {"K": 160, "Z": 260}
SHELL_RELOAD = {"SHOTGUN": 0.42}    # 한 발씩 넣는 총: 한 발 넣는 시간(초). 쏘면 바로 멈추고 쏴요
BOLT_ACTION = ("SNIPER",)            # 쏠 때마다 노리쇠를 당기는 총
MAX_DECALS = 240                     # 벽에 남는 총알 자국/그을음 최대 개수
MAX_TEXTURE_COL = 4               # 세로 줄 폭이 이보다 넓으면(느린 컴퓨터) 벽 질감 대신 단색으로
TEXTURE_DISTANCE = 9             # 이보다 먼 벽은 질감 없이 단색으로 (빠르게)
NORMAL_FOV = math.radians(66)     # 시야각
SCOPE_ZOOMS = [3, 6, 12]          # 저격총 조준경 배율
MAX_DEPTH = 60                    # 이보다 먼 곳은 안 그려요
EYE = 0.5                         # 눈높이 (1 = 건물 한 층 높이)
FOG_DIST = 32                     # 이 거리쯤 가면 노을 빛 안개에 묻혀요

MOVE_SPEED = 3.2                  # 1초에 몇 칸 움직이는지
AIM_MOVE = 0.6                    # 정조준 중에는 이만큼 느리게 움직여요
TURN_SPEED = 2.6                  # ←/→ 키로 돌 때 속도
LOOK_SPEED = 420 * UI             # ↑/↓ 키로 위아래 볼 때 속도
MOUSE_SENS = 0.0025               # 마우스 좌우 감도
MOUSE_SENS_Y = 1.0                # 마우스 위아래 감도
MAX_PITCH = 260 * UI              # 위아래로 볼 수 있는 한계(px)
JUMP_SPEED = 4.2                  # 점프 힘
GRAVITY = 13                      # 중력 (클수록 빨리 떨어져요)

# 설정 (시작 화면에서 S): 저장돼서 다음에도 그대로예요
SETTINGS = dict(look=1.0, mouse=1.0, assist=2, fov=66, volume=80, difficulty=2, v2=True, music=40,
                hud=100, shake=1, soundviz=0, colorblind=0)
ASSIST_LEVELS = ["OFF", "LOW", "NORMAL", "HIGH"]
ASSIST_PAD = [0.0, 0.6, 1.0, 1.5]          # 아깝게 빗나간 총알을 몸통에 맞혀 주는 정도
ASSIST_STICKY = [1.0, 0.75, 0.55, 0.4]     # 조준점이 적 위에 있을 때 시점이 느려지는 정도
# 난이도: (이름, 적 실력 배율, 내가 받는 피해 배율)
DIFFICULTIES = [("RECRUIT", 0.7, 0.45), ("EASY", 0.85, 0.65), ("NORMAL", 1.0, 1.0),
                ("HARD", 1.2, 1.35), ("VETERAN", 1.4, 1.8)]


# ----- 키 바꾸기 -----
# (이름, 기본 키, 한국어 설명). 게임 코드는 언제나 '기본 키'로 생각하고, 실제로 누른 키를 기본 키로 바꿔서 넘겨줘요.
KEY_ACTIONS = [
    ("FORWARD", pygame.K_w, "앞으로"), ("BACK", pygame.K_s, "뒤로"), ("LEFT", pygame.K_a, "왼쪽"),
    ("RIGHT", pygame.K_d, "오른쪽"), ("SPRINT", pygame.K_LSHIFT, "달리기"), ("CROUCH", pygame.K_c, "앉기 / 슬라이딩"),
    ("JUMP", pygame.K_SPACE, "점프"), ("FIRE", pygame.K_f, "사격"), ("AIM", pygame.K_e, "정조준"),
    ("RELOAD", pygame.K_r, "재장전"), ("GRENADE", pygame.K_g, "수류탄"), ("KNIFE", pygame.K_v, "칼"),
    ("STREAK", pygame.K_x, "킬스트릭"), ("NEXT WEAPON", pygame.K_q, "무기 바꾸기"), ("SCOPE ZOOM", pygame.K_z, "조준경 배율"),
    ("FOCUS", pygame.K_t, "스킬: 집중"), ("MEDKIT", pygame.K_y, "스킬: 구급상자"), ("SCAN", pygame.K_j, "스킬: 탐지"),
    ("INSPECT", pygame.K_i, "무기 살펴보기"), ("SHOP AMMO", pygame.K_b, "좀비 상점: 탄약"), ("SHOP UPGRADE", pygame.K_u, "좀비 상점: 강화"),
]
# 바꿀 수 없는 키: 메뉴/시점/전체 화면
KEY_FIXED = (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_UP, pygame.K_DOWN,
             pygame.K_LEFT, pygame.K_RIGHT, pygame.K_F11)
KEY_MAP = {}      # 실제로 누른 키 -> 게임이 알아듣는 키 (바꾼 것만)
KEY_INV = {}      # 게임이 알아듣는 키 -> 실제로 눌러야 하는 키


def apply_keys(saved):
    """저장된 키 설정 적용 (save["keys"]: {"누른 키 번호": 기본 키 번호})"""
    KEY_MAP.clear()
    for physical, logical in saved.items():
        if int(physical) != int(logical):
            KEY_MAP[int(physical)] = int(logical)
    KEY_INV.clear()
    KEY_INV.update({logical: physical for physical, logical in KEY_MAP.items()})


def bound_key(default):
    """그 기능을 하려면 실제로 누를 키"""
    return KEY_INV.get(default, default)


def key_label(key):
    return pygame.key.name(key).upper() or "?"


def rebind(default, new_key):
    """default 기능을 new_key로 옮겨요. new_key가 원래 하던 일은 이 기능이 쓰던 키로 (서로 바꾸기)"""
    old = bound_key(default)
    displaced = KEY_MAP.get(new_key, new_key)
    KEY_MAP[new_key] = default
    KEY_MAP[old] = displaced
    apply_keys(dict(KEY_MAP))


def saved_keys():
    return {str(physical): logical for physical, logical in KEY_MAP.items()}


class RemappedKeys:
    """누르고 있는 키 상태도 바꾼 키에 맞게 읽어요"""

    def __init__(self, pressed):
        self.pressed = pressed

    def __getitem__(self, key):
        return self.pressed[KEY_INV.get(key, key)]


def remap_event(event):
    if event.type in (pygame.KEYDOWN, pygame.KEYUP) and event.key in KEY_MAP:
        return pygame.event.Event(event.type, dict(event.dict, key=KEY_MAP[event.key]))
    return event


# ----- 도전 모드 -----
# (이름, 라운드, 한국어 설명, 영어 설명). DAILY 의 라운드와 적은 날짜로 정해져요
CHALLENGES = [
    ("DAILY", 0, "오늘의 도전: 날짜마다 바뀌는 맵과 적. 빨리 깰수록 좋아요", "Daily: map and enemies change every day"),
    ("HEADSHOTS", 12, "머리를 맞혀야만 피해가 들어가요", "Only headshots do damage"),
    ("PISTOL", 9, "권총 하나로만 싸워요", "Pistol only"),
    ("HARDCORE", 15, "한 방 맞으면 끝! 대신 내 총알 피해 2배", "One hit kills you, your bullets do double damage"),
    ("BLITZ", 7, "60초 안에 모든 적을 쓰러뜨리세요", "Clear the round in 60 seconds"),
]
BLITZ_TIME = 60


def daily_seed():
    return datetime.date.today().toordinal()


# ----- 업적과 위장 무늬 -----
# 누적 기록 save["lifetime"]: kills, heads, knife, explosive, rounds, streak
ACHIEVEMENTS = [
    ("FIRST BLOOD", "처음으로 적 처치", "Get your first kill", lambda s, l: l.get("kills", 0) >= 1),
    ("CENTURION", "누적 100명 처치", "100 total kills", lambda s, l: l.get("kills", 0) >= 100),
    ("WAR MACHINE", "누적 1000명 처치", "1000 total kills", lambda s, l: l.get("kills", 0) >= 1000),
    ("HEADHUNTER", "헤드샷 50번", "50 headshots", lambda s, l: l.get("heads", 0) >= 50),
    ("DEADEYE", "헤드샷 300번", "300 headshots", lambda s, l: l.get("heads", 0) >= 300),
    ("CLOSE QUARTERS", "칼로 10명 처치", "10 knife kills", lambda s, l: l.get("knife", 0) >= 10),
    ("DEMOLITION", "폭발로 25명 처치", "25 explosive kills", lambda s, l: l.get("explosive", 0) >= 25),
    ("ON FIRE", "한 판에서 연속 10명 처치", "10 kill streak", lambda s, l: l.get("streak", 0) >= 10),
    ("VETERAN", "라운드/웨이브 50번 깨기", "Clear 50 rounds or waves", lambda s, l: l.get("rounds", 0) >= 50),
    ("SET ONE", "캠페인 21라운드 도착", "Reach campaign round 21", lambda s, l: s.get("best", 0) >= 21),
    ("HALFWAY", "캠페인 51라운드 도착", "Reach campaign round 51", lambda s, l: s.get("best", 0) >= 51),
    ("LEGEND", "캠페인 100라운드 도착", "Reach campaign round 100", lambda s, l: s.get("best", 0) >= 100),
    ("SURVIVOR", "좀비 10웨이브 도착", "Reach zombie wave 10", lambda s, l: s.get("zbest", 0) >= 10),
    ("OPERATOR", "미션 하나 끝내기", "Complete a mission", lambda s, l: len(s.get("missions_done", [])) >= 1),
    ("ARSENAL", "무기 10종 얻기", "Own 10 weapons", lambda s, l: len(unlocked_weapons(s)) >= 10),
    ("CHALLENGER", "도전 모드 하나 깨기", "Complete a challenge", lambda s, l: bool(s.get("challenges"))),
]
# 위장 무늬: (이름, 필요한 업적 수, 몸통 색, 무늬 색)
CAMOS = [("NONE", 0, None, None), ("ARCTIC", 2, (225, 230, 235), (150, 160, 175)),
         ("JUNGLE", 4, (75, 100, 55), (45, 62, 35)), ("CRIMSON", 7, (150, 28, 34), (92, 16, 22)),
         ("DIAMOND", 11, (170, 235, 250), (90, 170, 210))]
CAMO_COLORS = {name: (body, accent) for name, need, body, accent in CAMOS if body}
CAMO_COLORS["gold"] = ((212, 175, 55), (165, 128, 35))


def earned_camos(save):
    count = len(save.get("achievements", []))
    return [name for name, need, body, accent in CAMOS if count >= need]


def apply_settings(settings):
    """저장된 설정을 게임에 적용해요"""
    global NORMAL_FOV, UI, RED, GREEN
    SETTINGS.update(settings)
    NORMAL_FOV = math.radians(SETTINGS["fov"])
    UI = HEIGHT / 600 * SETTINGS.get("hud", 100) / 100
    # 색약 모드: 빨강/초록 대신 주황/파랑 (조준선, 체력, 적 표시)
    RED, GREEN = ((255, 130, 20), (70, 160, 255)) if SETTINGS.get("colorblind") else ((230, 50, 50), (90, 220, 120))


# 고를 수 있는 해상도. 화면보다 큰 해상도는 전체 화면으로 열어요
RESOLUTIONS = [(1280, 720), (1600, 900), (1920, 1080), (2560, 1440)]


def set_resolution(width, height):
    """해상도를 바꿔요. 화면 크기에 따라 정해지는 값들도 같이 다시 계산해요."""
    global WIDTH, HEIGHT, UI, LOOK_SPEED, MAX_PITCH
    WIDTH, HEIGHT = width, height
    UI = HEIGHT / 600 * SETTINGS.get("hud", 100) / 100     # 설정의 UI SIZE 로 글자·표시 크기 조절
    LOOK_SPEED = 420 * UI
    MAX_PITCH = 260 * UI


SAFE_SPAWN = 8                    # 시작할 때 이 거리 안에는 적이 안 나와요

SPRINT_SPEED = 1.6                # 달리면 이만큼 빨라져요
SPRINT_RECOVER = 0.15             # 달리기를 멈추고 총을 다시 쏠 수 있을 때까지(초)
CROUCH_SPEED = 0.55               # 앉으면 이만큼 느려져요
CROUCH_DROP = 0.22                # 앉으면 눈높이가 이만큼 낮아져요
SLIDE_TIME = 0.7                  # 슬라이딩 시간(초)
SLIDE_SPEED = 2.3                 # 슬라이딩 처음 속도 (점점 느려져요)

# 킬스트릭: 죽지 않고 연속으로 쓰러뜨린 수 -> 받는 보상 (X 키로 사용)
STREAKS = [(3, "RADAR"), (5, "AIRSTRIKE"), (7, "SENTRY")]
STREAK_KILLS = ("AIRSTRIKE!", "SENTRY")   # 킬스트릭으로 쓰러뜨린 건 연속 처치 수에 안 세요
RADAR_TIME = 20                   # 레이더: 미니맵에 적이 다 보이는 시간(초)
AIRSTRIKE_BLAST = (2.6, 220)
SENTRY_TIME = 30                  # 자동 포탑이 버티는 시간(초)
SENTRY_RANGE = 12

# 체력 회복: 이 시간 동안 안 맞으면 체력이 빠르게 차요
REGEN_DELAY = 4.0
REGEN_RATE = 25                   # 1초에 차는 체력
BLOOD = (150, 10, 15)
MAX_CORPSES = 12                  # 바닥에 남는 쓰러진 적 수 (너무 많으면 느려져요)
MAX_SPLATS = 40                   # 바닥에 남는 피 웅덩이 수
CORPSE_TIME = 12.0                # 쓰러진 적이 남아 있는 시간(초)
# 총마다 좌우 반동 (쏠 때 조준이 옆으로 살짝 튀어요, 단위: 라디안)
HORIZONTAL_KICK = {"RIFLE": 0.005, "PISTOL": 0.004, "SNIPER": 0.015, "SHOTGUN": 0.012, "SMG": 0.007,
                   "ROCKET": 0.01, "LMG": 0.006, "BURST": 0.004, "DMR": 0.008, "HEAVY AR": 0.008,
                   "AUTO SHOTGUN": 0.012, "REVOLVER": 0.012, "MACHINE PISTOL": 0.007, "LAUNCHER": 0.01}

# 라운드 목표 (캠페인): 1라운드와 5의 배수 라운드는 전멸, 나머지는 돌아가며
#   HOSTAGE 인질 구출: 인질 옆에 3초 서 있기    BOMB 폭탄 해체: 75초 안에 폭탄 옆에 5초
#   HOLD 거점 지키기: 표시된 곳 안에서 20초 버티기 (적 지원군이 계속 와요)
OBJECTIVE_ORDER = {2: "HOSTAGE", 3: "BOMB", 4: "HOLD"}
OBJECTIVES = {
    "HOSTAGE": dict(need=3.0, radius=1.2, title="RESCUE THE HOSTAGE", doing="RESCUING", color=(255, 160, 60)),
    "BOMB": dict(need=5.0, radius=1.2, title="DEFUSE THE BOMB", doing="DEFUSING", color=(255, 70, 70)),
    "HOLD": dict(need=20.0, radius=2.0, title="HOLD THE POINT", doing="CAPTURING", color=(80, 240, 255)),
    "REACH": dict(need=0.3, radius=1.6, title="REACH THE MARKER", doing="ARRIVING", color=(255, 220, 90)),
    "CACHE": dict(need=3.0, radius=1.2, title="DESTROY THE CACHES", doing="PLANTING", color=(255, 140, 40)),
}
BOMB_TIME = 75.0
KILLCAM_TIME = 3.0                # 죽으면 이 시간 동안 나를 쓰러뜨린 적의 시점으로 보여줘요
# 무기 성장: 그 총으로 쓰러뜨린 수 -> 풀리는 부착물 (다음 라운드부터 자동으로 달려요)
WEAPON_LEVELS = [(10, "EXT MAG"), (25, "GRIP"), (45, "SUPPRESSOR"), (70, "GOLD CAMO")]
PLAYER_LOOK = dict(uniform=(60, 90, 140), vest=(40, 60, 100), pants=(40, 45, 60), head="helmet", gun=30)


# ----- RPG: 무기 해금, 무기 레벨, 스킬 -----
START_WEAPONS = ["RIFLE", "PISTOL"]
# 무기를 얻는 조건: ("level", 계급) / ("score", 한 라운드 점수) / ("heads", 한 라운드 헤드샷 수)
UNLOCKS = {
    "SMG": ("level", 2), "SHOTGUN": ("level", 3), "BURST": ("score", 1000), "MACHINE PISTOL": ("level", 4),
    "SNIPER": ("level", 5), "DMR": ("heads", 5), "HEAVY AR": ("level", 6), "REVOLVER": ("score", 1500),
    "AUTO SHOTGUN": ("level", 8), "LMG": ("level", 10), "LAUNCHER": ("score", 2500), "ROCKET": ("level", 12),
}
WEAPON_MAX_LEVEL = 10
KILLS_PER_WEAPON_LEVEL = 6
# 스킬: (이름, 최대 단계, 한국어 설명, 영어 설명, 쓰는 키(액티브 스킬))
SKILLS = [
    ("VITALITY", 3, "최대 체력 +15", "Max health +15", None),
    ("MARKSMAN", 3, "헤드샷 피해 +15%", "Headshot damage +15%", None),
    ("RELOAD MASTER", 3, "재장전 10% 빠르게", "Reload 10% faster", None),
    ("RUNNER", 3, "이동 6% 빠르게", "Move 6% faster", None),
    ("REGEN", 3, "체력이 0.7초 일찍, 30% 더 빨리 차요", "Health regen starts sooner, 30% faster", None),
    ("DEMOLITION", 3, "수류탄 +1, 폭발 피해 +20%", "+1 grenade, explosions +20%", None),
    ("AMMO PACK", 3, "탄약 +25%", "Ammo +25%", None),
    ("FOCUS", 1, "T: 5초 동안 적이 느려져요 (다시 쓰기 45초)", "T: enemies slow down for 5s (45s cooldown)", "T"),
    ("MEDKIT", 1, "Y: 체력 60 회복 (다시 쓰기 35초)", "Y: heal 60 (35s cooldown)", "Y"),
    ("SCAN", 1, "J: 8초 동안 벽 너머 모든 적 표시 (다시 쓰기 30초)", "J: reveal all enemies for 8s (30s cooldown)", "J"),
]
ACTIVE_SKILLS = {"FOCUS": (5.0, 45.0), "MEDKIT": (0.0, 35.0), "SCAN": (8.0, 30.0)}   # (지속 시간, 다시 쓰기)


def player_level(save):
    return 1 + save.get("xp", 0) // XP_PER_RANK


def skill_points(save):
    """쓸 수 있는 스킬 포인트: 계급이 오를 때마다 1점"""
    return player_level(save) - 1 - sum(save.get("skills", {}).values())


def unlocked_weapons(save):
    """가진 무기 목록 (계급 조건은 여기서 바로 풀려요)"""
    have = set(START_WEAPONS) | set(save.get("unlocked", []))
    have |= {name for name, (kind, need) in UNLOCKS.items() if kind == "level" and player_level(save) >= need}
    return [spec["name"] for spec in WEAPONS if spec["name"] in have]


def unlock_text(name, ko):
    kind, need = UNLOCKS[name]
    if kind == "level":
        return f"계급 {need}" if ko else f"rank {need}"
    if kind == "score":
        return f"한 판 {need}점" if ko else f"{need} pts/round"
    return f"한 판 헤드샷 {need}" if ko else f"{need} heads/round"


def weapon_level(kills):
    return min(WEAPON_MAX_LEVEL, 1 + kills // KILLS_PER_WEAPON_LEVEL)


def weapon_mods(kills):
    """쓰러뜨린 수로 풀린 부착물 목록"""
    return [mod for need, mod in WEAPON_LEVELS if kills >= need]


def apply_mods(spec, mods, level=1):
    """부착물과 무기 레벨을 적용한 무기 설정을 새로 만들어요
    EXT MAG 탄창 1.5배 / GRIP 반동 30% 줄임 / SUPPRESSOR 소음기(적이 잘 못 들어요) / GOLD CAMO 금색 총
    레벨마다 피해 +5%, 재장전 -3%, 반동 -3%"""
    spec = dict(spec)
    up = level - 1
    spec["level"] = level
    spec["body"] = spec["body"] * (1 + 0.05 * up)
    spec["head"] = spec["head"] * (1 + 0.05 * up)
    spec["reload"] = spec["reload"] * (1 - 0.03 * up)
    spec["kick"] = spec["kick"] * (1 - 0.03 * up)
    if "EXT MAG" in mods and not spec["projectile"]:
        spec["mag"] = int(spec["mag"] * 1.5)
        spec["reserve"] = int(spec["reserve"] * 1.25)
    if "GRIP" in mods:
        spec["kick"] = spec["kick"] * 0.7
        spec["recoil"] = 0.7
    if "SUPPRESSOR" in mods and not spec["projectile"]:
        spec["suppressed"] = True
    if "GOLD CAMO" in mods:
        spec["camo"] = "gold"
    return spec


# 맵마다 총소리 메아리: (늦게 들리는 시간 초, 크기). 좁은 골목·실내는 크게, 탁 트인 곳은 작게
ECHOES = {"NEON BEACH": (0.35, 0.12), "DOWNTOWN": (0.18, 0.35), "HARBOR": (0.22, 0.3), "DESERT TOWN": (0.25, 0.2),
          "SNOW BASE": (0.3, 0.2), "FOREST VILLAGE": (0.3, 0.22), "RAIN DISTRICT": (0.15, 0.4),
          "CARGO SHIP": (0.12, 0.3), "MOTEL": (0.2, 0.25), "SCRAPYARD": (0.2, 0.25), "BAZAAR": (0.12, 0.35),
          "OIL RIG": (0.3, 0.2), "LIGHTHOUSE POINT": (0.3, 0.18), "BLOOD MOON": (0.3, 0.3)}
PENETRATION = 0.5                 # 얇은 엄폐물(상자, 모래주머니) 너머 적을 맞히면 피해 비율


def recoil_pattern(name):
    """무기마다 정해진 좌우 반동 모양 (-1 ~ 1). 처음 두 발은 거의 똑바로, 그다음부터 정해진 대로 흔들려요.
    무작위가 아니라서 연습하면 반대로 살짝 돌려 잡을 수 있어요."""
    rng = random.Random(name)
    value, pattern = 0.0, [0.0, 0.1]
    for _ in range(30):
        value = max(-1.0, min(1.0, value + rng.uniform(-0.55, 0.55) + (0.15 if value < 0.3 else -0.1)))
        pattern.append(value)
    return pattern


# 경험치: 1000마다 계급(RANK)이 올라가요
XP = dict(kill=100, headshot=50, knife=50, boss=500, double=50, triple=100, multi=150, round=250)
XP_PER_RANK = 1000

GRENADES_START, GRENADES_MAX = 3, 6
GRENADE_FUSE = 1.8                # 던지고 터질 때까지(초)
GRENADE_THROW = 9.0               # 던지는 힘
GRENADE_BLAST = (3.2, 160)        # (폭발 반경, 가운데 피해)
ROCKET_SPEED = 16.0
ROCKET_BLAST = (2.8, 300)
SHELL_BLAST = (2.6, 190)          # 유탄
EXPLODER_BLAST = (2.6, 45)        # 다가와서 터지는 좀비
EXPLODER_SHOT_BLAST = (2.6, 130)  # 총에 맞아 터지면 주변 좀비까지 날려요
SELF_DAMAGE = 0.35                # 내 폭발에 내가 받는 피해 비율
ENEMY_GRENADE_FUSE = 1.5          # 적이 던진 수류탄
ENEMY_GRENADE_BLAST = (2.8, 70)

KNIFE_RANGE = 1.5
KNIFE_DAMAGE = 150
KNIFE_TIME = 0.3                  # 칼 휘두르는 시간
KNIFE_COOLDOWN = 0.6

PICKUP_RADIUS = 0.7
DROP_CHANCE = 0.8                 # 적이 상자를 떨어뜨릴 확률
DROP_WEIGHTS = {"ammo": 5, "health": 3, "grenade": 2}
HEALTH_PACK = 35

# 로드아웃: 시작하기 전에 주무기 / 보조무기 / 퍼크(특수 능력)를 골라요
PRIMARIES = ["RIFLE", "HEAVY AR", "BURST", "SMG", "SHOTGUN", "AUTO SHOTGUN", "LMG", "DMR", "SNIPER"]
SECONDARIES = ["PISTOL", "REVOLVER", "MACHINE PISTOL", "ROCKET", "LAUNCHER"]
# 퍼크: (이름, 한국어 설명, 영어 설명)
PERKS = [
    ("HEAVY ROUNDS", "총알 피해 +25%", "Bullets deal 25% more damage"),
    ("QUICK HANDS", "재장전·무기 교체 40% 빠르게", "Reload and swap 40% faster"),
    ("LIGHTFOOT", "이동 +12%, 발소리를 적이 못 들어요", "Move 12% faster, enemies can't hear your steps"),
    ("IRON SKIN", "최대 체력 130", "Max health 130"),
    ("SCAVENGER", "탄약 1.5배, 수류탄 +2", "1.5x ammo, +2 grenades"),
]
DEFAULT_LOADOUT = dict(primary="RIFLE", secondary="PISTOL", perk="HEAVY ROUNDS")
# 무기 설명: 이름 -> (한국어, 영어)
WEAPON_INFO = {
    "RIFLE": ("돌격소총 - 균형 잡힌 연사", "Assault rifle - balanced full auto"),
    "BURST": ("점사 소총 - 한 번에 3발, 정확해요", "Burst rifle - 3 round bursts, accurate"),
    "SMG": ("기관단총 - 아주 빠른 연사, 가까운 거리", "SMG - very fast fire, close range"),
    "SHOTGUN": ("산탄총 - 가까이서 한 방", "Shotgun - one shot up close"),
    "LMG": ("기관총 - 탄창 100발, 무거워요", "LMG - 100 round box, heavy"),
    "DMR": ("지정사수 소총 - 단발, 강하고 정확해요", "Marksman rifle - strong single shots"),
    "SNIPER": ("저격총 - 조준경, 몸통도 한 방", "Sniper - scope, one shot kills"),
    "PISTOL": ("권총 - 가볍고 빠르게 꺼내요", "Pistol - light and quick"),
    "ROCKET": ("로켓 - 넓은 폭발", "Rocket launcher - big explosion"),
    "HEAVY AR": ("중돌격소총 - 느리지만 한 발이 묵직해요", "Heavy rifle - slower, hits harder"),
    "AUTO SHOTGUN": ("자동 산탄총 - 꾹 누르면 연달아 쾅쾅", "Auto shotgun - hold to keep blasting"),
    "REVOLVER": ("리볼버 - 6발, 머리 한 방", "Revolver - 6 shots, one shot headshots"),
    "MACHINE PISTOL": ("기관권총 - 보조무기인데 연사돼요", "Machine pistol - full auto sidearm"),
    "LAUNCHER": ("유탄발사기 - 포물선으로 날아가 닿으면 쾅", "Grenade launcher - lobbed, explodes on impact"),
}

# 무기 목록
#   auto   : 꾹 누르면 연사되는지
#   delay  : 다음 발까지 걸리는 시간(초)
#   body / head : 몸통 / 머리 데미지
#   spread : 총알이 퍼지는 정도(px)
#   kick   : 한 발 쏠 때 시점이 위로 튀는 정도(px)
#   pellets: 한 번에 나가는 총알 수 (산탄총)
#   ads    : 정조준 배율
#   scope  : 조준경이 있는지 (저격총)     projectile : 총알 대신 로켓이 날아가는지
#   burst  : 한 번 누르면 몇 발이 나가는지 (점사), burst_delay: 점사 안에서 발 사이 간격
#   move   : 들고 있을 때 이동 속도 비율 (무거운 총은 느려요)
WEAPONS = [
    dict(name="RIFLE", auto=True, delay=0.1, mag=30, reserve=120, body=34, head=100,
         spread=4, kick=9, reload=1.8, pellets=1, ads=1.4, scope=False, projectile=False),
    dict(name="PISTOL", auto=False, delay=0.15, mag=12, reserve=60, body=40, head=100,
         spread=2, kick=16, reload=1.2, pellets=1, ads=1.3, scope=False, projectile=False),
    dict(name="SNIPER", auto=False, delay=1.2, mag=5, reserve=25, body=150, head=300,
         spread=45, kick=50, reload=2.5, pellets=1, ads=1, scope=True, projectile=False),
    dict(name="SHOTGUN", auto=False, delay=0.8, mag=8, reserve=32, body=20, head=40,
         spread=50, kick=40, reload=2.2, pellets=8, ads=1.15, scope=False, projectile=False),
    dict(name="SMG", auto=True, delay=0.065, mag=35, reserve=140, body=22, head=70,
         spread=7, kick=6, reload=1.6, pellets=1, ads=1.3, scope=False, projectile=False),
    dict(name="ROCKET", auto=False, delay=1.0, mag=1, reserve=5, body=0, head=0,
         spread=1, kick=60, reload=2.0, pellets=1, ads=1.3, scope=False, projectile=True),
    dict(name="LMG", auto=True, delay=0.085, mag=100, reserve=200, body=30, head=90,
         spread=7, kick=7, reload=4.0, pellets=1, ads=1.35, scope=False, projectile=False, move=0.85),
    dict(name="BURST", auto=False, delay=0.32, mag=30, reserve=120, body=32, head=95,
         spread=3, kick=6, reload=1.9, pellets=1, ads=1.45, scope=False, projectile=False,
         burst=3, burst_delay=0.06),
    dict(name="DMR", auto=False, delay=0.25, mag=15, reserve=60, body=55, head=150,
         spread=2, kick=22, reload=2.0, pellets=1, ads=2.2, scope=False, projectile=False),
    dict(name="HEAVY AR", auto=True, delay=0.12, mag=25, reserve=100, body=42, head=110,
         spread=5, kick=13, reload=2.0, pellets=1, ads=1.4, scope=False, projectile=False),
    dict(name="AUTO SHOTGUN", auto=True, delay=0.3, mag=12, reserve=36, body=15, head=30,
         spread=45, kick=28, reload=2.6, pellets=6, ads=1.15, scope=False, projectile=False, move=0.95),
    dict(name="REVOLVER", auto=False, delay=0.38, mag=6, reserve=36, body=75, head=170,
         spread=2, kick=34, reload=2.2, pellets=1, ads=1.35, scope=False, projectile=False),
    dict(name="MACHINE PISTOL", auto=True, delay=0.055, mag=20, reserve=100, body=18, head=50,
         spread=8, kick=5, reload=1.3, pellets=1, ads=1.25, scope=False, projectile=False),
    # lobbed: 포물선으로 날아가 닿는 순간 터지는 유탄
    dict(name="LAUNCHER", auto=False, delay=0.9, mag=4, reserve=12, body=0, head=0,
         spread=1, kick=40, reload=2.6, pellets=1, ads=1.25, scope=False, projectile=True, lobbed=True),
]

WEAPON_BY_NAME = {spec["name"]: spec for spec in WEAPONS}

# 적 종류
#   hp       : 체력            speed : 이동 속도        sight : 플레이어를 알아보는 거리
#   reaction : 발견 후 첫 사격까지 시간                 keep  : 이 거리까지만 다가와요
#   range    : 이보다 멀면 안 쏴요                      fire  : 사격 간격(초) 범위
#   damage   : 한 발 피해 범위  accuracy : 명중률       falloff : 거리 1칸마다 줄어드는 명중률
#   height / width : 크기 (눈높이 0.5 기준)
#   look     : 생김새 (옷 색, 머리 장비, 총 길이)
ENEMY_TYPES = {
    # 사격장 과녁: 움직이지도 쏘지도 않아요
    "TARGET": dict(hp=100, speed=0.0, sight=0, reaction=99, keep=0, range=0,
                   fire=(9, 9), damage=(0, 0), accuracy=0.0, falloff=0.0,
                   height=0.92, width=0.5,
                   look=dict(uniform=(205, 175, 125), vest=(230, 70, 60), pants=(150, 120, 80),
                             head="helmet", gun=0)),
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
    # 아래 셋은 수류탄을 던져요: throw = 던지는 간격(초) 범위, throw_range = 던지는 거리 범위
    "BOMBER": dict(hp=90, speed=1.3, sight=14, reaction=1.0, keep=7, range=0,
                   fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                   height=0.9, width=0.45, throw=(2.2, 3.2), throw_range=(3, 11),
                   look=dict(uniform=(110, 90, 60), vest=(70, 95, 55), pants=(60, 55, 45),
                             head="beret", gun=18, belt=True)),
    # shield=True: 앞에서 맞은 몸통 총알은 방패에 막혀요 (머리, 옆, 뒤, 폭발, 칼은 그대로)
    "SHIELD": dict(hp=150, speed=1.1, sight=14, reaction=0.8, keep=2.5, range=10,
                   fire=(0.8, 1.3), damage=(8, 12), accuracy=0.6, falloff=0.04,
                   height=0.92, width=0.6, shield=True,
                   look=dict(uniform=(35, 45, 80), vest=(25, 30, 55), pants=(30, 35, 50),
                             head="riot", gun=20, shield=True)),
    "BOSS": dict(hp=900, speed=1.0, sight=18, reaction=0.6, keep=5, range=16,
                 fire=(0.09, 0.15), damage=(4, 7), accuracy=0.33, falloff=0.02,
                 height=1.15, width=0.72, throw=(4, 6), throw_range=(3, 12),
                 look=dict(uniform=(240, 240, 235), vest=(240, 120, 170), pants=(235, 235, 230),
                           head="slick", gun=36)),
    # 측면 공격병: 빠르게 옆으로 돌아 들어와 가까이서 산탄총 (flank = 크게 좌우로 피해요)
    "FLANKER": dict(hp=90, speed=2.3, sight=15, reaction=0.5, keep=2.5, range=7,
                    fire=(0.7, 1.1), damage=(10, 16), accuracy=0.7, falloff=0.05,
                    height=0.88, width=0.44, flank=True,
                    look=dict(uniform=(35, 35, 40), vest=(25, 25, 28), pants=(30, 30, 35), head="mask", gun=24)),
    # 의무병: heal = (회복량, 간격 초, 거리). 근처 적을 치료해요 - 먼저 쓰러뜨리세요!
    "MEDIC": dict(hp=90, speed=1.2, sight=14, reaction=0.9, keep=6, range=12,
                  fire=(0.6, 1.1), damage=(5, 9), accuracy=0.5, falloff=0.04,
                  height=0.9, width=0.45, heal=(20, 1.2, 3.5),
                  look=dict(uniform=(225, 225, 220), vest=(240, 240, 235), pants=(70, 80, 70),
                            head="medic", gun=22, cross=True)),
    # 기관총 진지: 모래주머니 뒤에서 움직이지 않고 쉴 새 없이 쏴요. 옆으로 돌아가거나 수류탄으로
    "GUNNER": dict(hp=220, speed=0.0, sight=18, reaction=1.2, keep=99, range=18,
                   fire=(0.08, 0.13), damage=(3, 6), accuracy=0.38, falloff=0.02,
                   height=0.78, width=0.7,
                   look=dict(uniform=(70, 85, 60), vest=(45, 50, 40), pants=(40, 40, 45),
                             head="helmet", gun=40, sandbags=True)),
    # 정찰 드론: 머리 위(lift)에 떠서 빠르게 날아다니며 약한 총을 자주 쏴요. 작아서 맞히기 어려워요
    "DRONE": dict(hp=45, speed=2.6, sight=16, reaction=0.5, keep=5, range=12,
                  fire=(0.25, 0.45), damage=(3, 6), accuracy=0.5, falloff=0.03,
                  height=0.32, width=0.55, lift=1.15,
                  look=dict(uniform=(70, 75, 85), vest=(40, 42, 50), pants=(40, 42, 50), head="drone", gun=0)),
    # 레이저 저격수: 쏘기 전에 빨간 레이저가 나를 향해 좁혀 와요 (레이저가 보이면 숨으세요!)
    "LASER": dict(hp=90, speed=0.7, sight=32, reaction=1.6, keep=99, range=32,
                  fire=(2.6, 3.4), damage=(38, 48), accuracy=0.7, falloff=0.006,
                  height=0.9, width=0.45,
                  look=dict(uniform=(45, 50, 60), vest=(30, 32, 40), pants=(35, 38, 45), head="mask", gun=42)),
    # 좀비 모드: 총 대신 가까이 와서 할퀴어요. melee = (피해, 할퀴는 간격 초)
    "ZOMBIE": dict(hp=80, speed=1.25, sight=99, reaction=0, keep=0, range=0,
                   fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                   height=0.88, width=0.46, melee=(14, 1.0),
                   look=dict(head="zombie", skin=(125, 150, 105), shirt=(95, 85, 75), pants=(55, 50, 62),
                             eyes=(255, 225, 90))),
    "RUNNER": dict(hp=50, speed=2.5, sight=99, reaction=0, keep=0, range=0,
                   fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                   height=0.84, width=0.4, melee=(10, 0.7),
                   look=dict(head="zombie", skin=(150, 140, 120), shirt=(120, 40, 40), pants=(40, 45, 70),
                             eyes=(255, 60, 50), thin=True)),
    "BRUTE": dict(hp=650, speed=0.85, sight=99, reaction=0, keep=0, range=0,
                  fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                  height=1.12, width=0.72, melee=(32, 1.4),
                  look=dict(head="zombie", skin=(95, 120, 90), shirt=(60, 55, 50), pants=(40, 38, 45),
                            eyes=(255, 120, 40), big=True)),
    # 부풀어 오른 좀비: 다가와서 터져요. 총으로 미리 터뜨리면 주변 좀비까지 날아가요
    "EXPLODER": dict(hp=45, speed=2.0, sight=99, reaction=0, keep=0, range=0,
                     fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                     height=0.9, width=0.56, melee=(0, 0.5), explode=True,
                     look=dict(head="zombie", skin=(140, 160, 90), shirt=(110, 120, 60), pants=(60, 60, 50),
                               eyes=(180, 255, 80), bloated=True)),
    # 침 뱉는 좀비: 거리를 두고 초록 산성 침을 뱉어요 (sound = 쏠 때 소리)
    "SPITTER": dict(hp=90, speed=1.0, sight=20, reaction=0.8, keep=5, range=9,
                    fire=(2.0, 2.8), damage=(12, 18), accuracy=0.6, falloff=0.03,
                    height=0.86, width=0.44, sound="spit",
                    look=dict(head="zombie", skin=(110, 140, 110), shirt=(70, 90, 60), pants=(45, 50, 40),
                              eyes=(120, 255, 120), spit=True)),
}
ZOMBIE_KINDS = ("ZOMBIE", "RUNNER", "BRUTE", "EXPLODER", "SPITTER")
ARMORED = ("HEAVY", "BOSS", "BRUTE", "GUNNER")     # 맞으면 '깡' 장갑 소리
# 적 탄창: 이만큼 쏘면 재장전 (그동안 못 쏴요. 머리 위에 RELOADING 표시) -> (탄창, 재장전 초)
ENEMY_MAGS = {"GRUNT": (12, 2.2), "RUSHER": (8, 1.8), "SNIPER": (4, 2.6), "HEAVY": (45, 3.5), "SHIELD": (10, 2.2),
              "BOSS": (60, 3.0), "FLANKER": (6, 2.0), "MEDIC": (12, 2.2), "GUNNER": (50, 3.8)}
# 엄폐물을 쓰는 적: 다치거나 재장전하거나 제압당하면 숨었다가 고개를 내밀어 쏴요
COVER_USERS = ("GRUNT", "SNIPER", "MEDIC", "BOMBER", "SHIELD", "LASER")
ZOMBIE_POINTS = dict(hit=10, kill=60, headshot=100, knife=130, wave=250)
ZOMBIE_SHOP = dict(ammo=500, upgrade=2500)     # B: 탄약 가득, U: 들고 있는 총 강화


def scaled_type(kind, skill):
    """라운드가 올라갈수록 적이 강해져요 (skill 1.0 = 기본, 최대 2.0).
    더 정확하게, 더 빨리 반응하고, 더 자주 쏘고, 조금 더 단단해져요."""
    t = dict(ENEMY_TYPES[kind])
    if skill > 1.0:
        up = skill - 1.0
        t["accuracy"] = min(0.95, t["accuracy"] * (1 + up * 0.6))
        t["reaction"] = t["reaction"] / skill
        t["fire"] = (t["fire"][0] / skill ** 0.5, t["fire"][1] / skill ** 0.5)
        t["damage"] = tuple(round(d * (1 + up * 0.4)) for d in t["damage"])
        t["speed"] = t["speed"] * (1 + up * 0.25)
        t["sight"] = t["sight"] + up * 5
        t["hp"] = round(t["hp"] * (1 + up * 0.3))
        if "melee" in t:
            t["melee"] = (round(t["melee"][0] * (1 + up * 0.4)), t["melee"][1])
    return t

# ---------------------------------------------------------------
# 맵: 캠페인은 라운드마다 바뀌어요 (1 → 2 → ... → 9 → 1 ...). 마지막 맵은 좀비 모드 전용
# ---------------------------------------------------------------
#   바닥   '~' 바다(못 들어가요)  '.' 모래사장  '_' 보드워크  ':' 인도  '=' 차도
#          'g' 잔디  'x' 광장 타일  ',' 부두 콘크리트  'p' 나무 부두
#          ';' 사막 모래  '#' 흙길  '*' 눈  '-' 다져진 눈길
#   건물   'A' 분홍 호텔  'B' 민트 건물  'C' 노란 가게  'D' 하얀 아르데코 호텔
#          'R' 붉은 벽돌  'N' 나이트클럽  'G' 유리 오피스 타워  'S' 마천루
#          'W' 창고  'r' 'u' 'o' 빨강/파랑/주황 컨테이너  'Y' 두 층으로 쌓인 컨테이너
#          'M' 흙벽돌 집  'O' 콘크리트 벙커  'U' 연료 탱크  'J' 나무집  'V' 돌담  'Z' 모래주머니
#          'K' 나무 상자  'Q' 쓰레기통  'F' 분수/동상  (K Q F Z V 와 컨테이너는 엄폐물)  'H' 등대
#   장식   'T' 야자수  'c' 자동차(총알을 막아요)  'v' 불탄 차(총알을 막아요)  'L' 가로등
#          'b' 네온 광고판  'X' 크레인  'I' 침엽수
#   상자   'a' 탄약  'h' 체력  'n' 수류탄
#   위치   'P' 플레이어 시작  'E' 적이 나타날 수 있는 곳
#
# 분위기(theme):
#   sky    : 하늘 색 (위에서 아래로)   haze : 멀리 있는 것이 묻히는 안개 색
#   sun    : 해의 방향 (None이면 해 없음)   stars : 밤하늘 별
#   ground : 지평선 아래 기본 바닥        lit  : 창문 몇 개 중 하나에 불이 켜지는지
#   fog    : 안개 거리 비율 (작을수록 짙은 안개)   snow : 눈이 내리는지
#   camo   : 적 위장복 색 (None이면 기본 군복)
#   rain   : 비가 오는지     dark : 밤이라 바닥과 건물이 어두워지는 정도 (1 = 그대로)
#   sun_colors : 해(또는 달) 색 세 겹 (바깥 → 안쪽)
#   op / brief : 라운드 시작 때 나오는 작전 이름과 임무
MAPS = [
    dict(
        name="NEON BEACH",
        sky=[(0.0, (40, 30, 90)), (0.55, (150, 70, 140)), (0.85, (245, 120, 120)), (1.0, (250, 170, 140))],
        haze=(250, 170, 140), sun=math.pi, stars=False, ground=".", lit=4, fog=1.0, snow=False, camo=None,
        op="OPERATION SUNSET", brief="Hostiles have taken the boardwalk. Clear the beach district.",
        rows=[
            "~~~.._:==:::::::::::==:::E",
            "~~~.T_======c=============",
            "~~~.._==========c=========",
            "~~~..E:==:::::::::::==::::",
            "~~~.._L==:BBBBc:c:c:==:ggT",
            "~~~.P_:==:BBBB:::E::==:Egg",
            "~~~.._:c=:BBBB:Ka:::==:gEg",
            "~~~.T_:==:BBBB:c:c::==LggT",
            "~~~.._:==:CCCCCCCC::==:ggg",
            "~~~.n_:==:::::E:::::==::::",
            "~~~.._========c=========c=",
            "~~~.T_=============c======",
            "~~~.._:==:::::::::::==::::",
            "~~~.._:==:KK:K:KK:R:==:CC:",
            "~~~.E_L==::::K:::KR:==:CC:",
            "~~~.._:==:K:E:K:K:R:=c::E:",
            "~~~.T_:==:K:KKK:n:R:==:CC:",
            "~~~.._:==::E:::K::R:==:CCh",
            "~~~.T_:=c:RRRRRRRRR:==:CCC",
        ],
    ),
    dict(
        name="DOWNTOWN",
        sky=[(0.0, (8, 8, 30)), (0.6, (30, 20, 70)), (0.9, (90, 40, 110)), (1.0, (130, 60, 130))],
        haze=(70, 40, 95), sun=None, stars=True, ground=":", lit=2, fog=1.0, snow=False, camo=None,
        op="OPERATION NIGHTFALL", brief="Enemy snipers on the high-rises. Move fast between cover.",
        rows=[
            "SS:a::==:GxbxxE:==:AAA:NN:",
            "SSSSST==:GGG:GG:==:AAA:NN:",
            "SSSSS:==:GGG:GG:==LAAA:NN:",
            "::::::==::::::::==:::::::E",
            "===========c=========c====",
            "==P=======================",
            "::::::==::::::::==::::::::",
            "c:c:c:==:gggggg:==:xxxxxx:",
            "::::E:==TgTggbg:==:xbxxbxL",
            ":c:c::==:ggFFgg:==:xxKKxxE",
            "::::n:==:gEFFgg:==:xxKKxE:",
            "c:c:c:==LgggTgg:==:xbxxbxT",
            "RRRRR:==:gggggg:==:xxxxxx:",
            "::::::==::::E:::==::E:::::",
            "=======c================c=",
            "=============c============",
            "::::::==::E:::::==::::E:::",
            "CCCCC:==:DDD:DD:==:RR:RRR:",
        ],
    ),
    dict(
        name="HARBOR",
        sky=[(0.0, (60, 100, 165)), (0.6, (140, 165, 200)), (0.9, (250, 190, 140)), (1.0, (255, 215, 170))],
        haze=(225, 205, 185), sun=0.0, stars=False, ground=",", lit=6, fog=1.0, snow=False, camo=None,
        op="OPERATION TIDEWATER", brief="Secure the container yard before the shipment leaves.",
        rows=[
            "~~~,,,,,,,,,,,,,,,,,,,,,E,",
            "~~~,X,,,,,,,X,,,,,,,,,X,,,",
            "~~~,,rrr,uuu,,ooo,rrr,,uuu",
            "~~~,,rrr,uuu,,ooo,rrr,,uuu",
            "~~~,,,,,E,,,,E,,,,,,,,,,,,",
            "~~~,,YYY,ooo,,uuu,,K,,rrr,",
            "~~~,,YYY,ooo,,uuu,,KE,rrr,",
            "~~~,,,,,,,,,,,,,,,,,E,,,,E",
            "~~~,,uu,rr,oo,,YY,,,,uu,rr",
            "~~~=======================",
            "~~~=======E=====c========c",
            "~~~,,,L,,,,,,L,,,,,,L,,,,,",
            "~~~,WWWWW,,WWWWW,,BBBB,,c,",
            "~~~,WWWWW,,WWWWW,EBBBB,,,,",
            "~~~,WWWWW,,WWWWW,,BBBB,,c,",
            "~~~,,,,,,,E,,,,,,,,,,,,,,,",
            "~~~,,,QQ,KK,K,,QQ,,,h,,,,K",
            "~~~,P,,,,,,,,,,,,,,,,,,E,,",
            "~~~WWWWWWWWWWWWWWWWWWWWWWW",
            "~~~WWWWWWWWWWWWWWWWWWWWWWW",
        ],
    ),
    dict(
        name="DESERT TOWN",
        sky=[(0.0, (60, 110, 190)), (0.6, (130, 175, 225)), (0.9, (225, 215, 185)), (1.0, (240, 225, 195))],
        haze=(235, 220, 190), sun=-math.pi / 2, stars=False, ground=";", lit=9, fog=1.1, snow=False,
        camo=dict(uniform=(185, 160, 110), vest=(150, 125, 85), pants=(165, 140, 100)),
        op="OPERATION SANDSTORM", brief="Insurgents are holed up in the old town. Check every courtyard.",
        rows=[
            ";M;;;;M;E;h;M;;##;M;E;M;;;",
            ";MM;MMM;M;;;M;;##;MM;MM;M;",
            ";;;;;;;;MMMMM;;v#;;;;;;;MM",
            ";MMMM;;;;;;;;T;##;MMMM;;;;",
            ";MMMM;MMM;MMM;;##;MMMM;;;K",
            ";MMMM;M;;E;;M;;##;MMMM;;;E",
            ";MMMM;MMMMMMM;;##;MMMM;;;;",
            ";;;;;;;;;;;;;ZZ##;;T;;;;;E",
            "P####v####################",
            "######################v###",
            ";;;;;;;T;;;;;;;##ZZ;;;;;;;",
            ";MMMMM;;MMMMMM;##;MMMMM;;M",
            ";M;;;M;;M;;n;M;##;M;;;;;E;",
            ";M;h;;;;MM;MMM;##;M;ZZ;;a;",
            ";ME;;M;;;;;E;;;##;M;;;;K;;",
            ";MMMMM;;;;;;;;;##;M;;E;;K;",
            ";;;;;;;;;MMMMM;#v;M;ZZ;;;;",
            ";MM;MMM;;MMMMM;##;M;;;E;;;",
        ],
    ),
    dict(
        name="SNOW BASE",
        sky=[(0.0, (10, 15, 35)), (0.6, (35, 50, 80)), (0.9, (90, 110, 140)), (1.0, (150, 165, 185))],
        haze=(150, 165, 185), sun=None, stars=True, ground="*", lit=3, fog=0.8, snow=True,
        camo=dict(uniform=(225, 228, 232), vest=(165, 170, 180), pants=(200, 205, 212)),
        op="OPERATION WHITEOUT", brief="Infiltrate the arctic base. Watch the bunkers.",
        rows=[
            "**OOOOOOE*-*WWW**WWW**-***",
            "**********-***********-**E",
            "*****a****-********E*Z-***",
            "------c-------------------",
            "**********-Z********E*-***",
            "**JJJJJJ**-*OOOOOOOO**-**O",
            "**J**E*J**-*O**E***O**-**O",
            "**Ja***J**-****Kn*****-**O",
            "**JJ*JJJ**-*O****E*O**-**O",
            "**********-*OOOOOOOO**-***",
            "**********-***********-Z**",
            "P-------------------------",
            "*********Z-***********-**E",
            "**ZZZ*****-**ZZ*******-***",
            "**********-*********E*-*WW",
            "*******ZZ*-******h****-*WW",
            "***E******-*E*****ZZ**-*WW",
            "I*********-***********-***",
        ],
    ),
    dict(
        name="FOREST VILLAGE",
        sky=[(0.0, (85, 110, 140)), (0.6, (145, 165, 175)), (0.9, (195, 205, 195)), (1.0, (205, 212, 202))],
        haze=(190, 200, 190), sun=None, stars=False, ground="g", lit=5, fog=0.6, snow=False,
        camo=dict(uniform=(70, 95, 55), vest=(50, 70, 40), pants=(60, 70, 50)),
        op="OPERATION GREENWOOD", brief="Enemy squad spotted near the village. Use the trees for cover.",
        rows=[
            "ggggggggEgggggggggIg~~gggE",
            "ggggggggggggIggIgggg~~gggg",
            "####################pp####",
            "ggggggggg#gggggggEgg~~gggg",
            "ggggggggg#gJJJJJgggg~~gIgg",
            "ggVgIIggg#gJaggJJJJg~~gJJJ",
            "ggVghgggg#gJggEJJgJg~~gJng",
            "IgVgggggg#gJJgJJJggg~~gJgE",
            "ggVgggggg#ggggggJhJg~~gJgJ",
            "ggVVVVVVg#gJJJJgJJJg~~gggg",
            "ggIgggIgg#gJJJJggggg~~gggg",
            "ggggggggg#gJJJJggggg~~ggEI",
            "P###################pp####",
            "gggggggggggggggggggg~~EggI",
            "ggggEgggggggEgggggIg~~gJJJ",
            "gggggggggIIggggggggg~~gJJJ",
            "gIggggggggVVVVVVgggg~~gJJJ",
            "ggggggggggggaggggEgg~~gggg",
        ],
    ),
    dict(
        name="RAIN DISTRICT",
        sky=[(0.0, (12, 14, 24)), (0.6, (35, 40, 60)), (0.9, (70, 75, 95)), (1.0, (95, 100, 120))],
        haze=(70, 76, 96), sun=None, stars=False, ground=":", lit=2, fog=0.65, snow=False, rain=True, dark=0.72,
        camo=dict(uniform=(55, 60, 70), vest=(35, 38, 45), pants=(40, 42, 50)),
        op="OPERATION DOWNPOUR", brief="Neon alleys in heavy rain. Listen for their boots.",
        rows=[
            "SSSS:==:NNNNN:==:GGGG",
            "S:ES:==:N:::N:==:GGGG",
            "S:aS:==:::b:::==:::EG",
            "S:::L==:N:E:N:==:G::G",
            "SSSS:==:NNKNN:==LGGGG",
            ":::::==:::::::==:::::",
            "===c===========c=====",
            "========c============",
            ":E:::==:::::::==::E::",
            "RRRR:==:c:c::L==:CCCC",
            "R:K::==:::::::==:::EC",
            "R:E::==:c:E:c:==:::hC",
            "RRRR:==:KK:KK:==:CCCC",
            "::::L==:::::::==:::::",
            "======c==========c===",
            "=====================",
            ":P:::==:::E:::==:::E:",
        ],
    ),
    dict(
        name="CARGO SHIP",
        sky=[(0.0, (50, 60, 120)), (0.55, (160, 100, 120)), (0.85, (250, 150, 90)), (1.0, (255, 190, 120))],
        haze=(240, 170, 120), sun=math.pi / 2, stars=False, ground=",", lit=6, fog=1.0, snow=False, camo=None,
        op="OPERATION DEADWEIGHT", brief="Board the cargo ship. Containers everywhere - check every corner.",
        rows=[
            "~~~~~~~~~~~~~~~~~~~~~~~~",
            "~WWWW,,,,E,,,,,,,,E,,,,~",
            "~WWWW,rr,,uu,,oo,,YY,,a~",
            "~WWWW,rr,,uu,,oo,,YY,,,~",
            "~,,,,,,,,,,,,,,,,,,,,,,~",
            "~,E,,YY,,oo,,K,,rr,,uu,~",
            "~,,,,YY,,oo,,,E,rr,,uu,~",
            "~P,,,,,,,,,,,,,,,,,,,,E~",
            "~,,,,uu,,rr,,K,,oo,,YY,~",
            "~,n,,uu,,rr,,,,,oo,,YY,~",
            "~,,,,,,,,,,,E,,,,,,,,h,~",
            "~WWWW,oo,,YY,,uu,,rr,,,~",
            "~WWWW,oo,,YY,,uu,,rr,E,~",
            "~~~~~~~~~~~~~~~~~~~~~~~~",
        ],
    ),
    dict(
        name="MOTEL",
        sky=[(0.0, (70, 60, 130)), (0.6, (190, 110, 120)), (0.9, (250, 170, 110)), (1.0, (255, 205, 150))],
        haze=(245, 190, 150), sun=-math.pi / 2, stars=False, ground=";", lit=5, fog=1.1, snow=False,
        camo=dict(uniform=(185, 160, 110), vest=(150, 125, 85), pants=(165, 140, 100)),
        op="OPERATION ROADSIDE", brief="Hostiles holed up in a desert motel. Clear the rooms.",
        rows=[
            ";;;;;;;;;;;;;;;;;;;;;;",
            ";MMMMMMMMMMMMM;;;;T;E;",
            ";M;aM;EM;;M;hM;;UU;;;;",
            ";M;MM;MM;MM;MM;;UU;;E;",
            ";;;;;;;;;;;;;;;;;;;;;;",
            ";;c;;c;;c;;;;Z;;;;v;;;",
            "======================",
            "=====c=========v======",
            ";;;;;;;;;;;;;;;;;;;;;;",
            ";CCCCC;;Q;Q;;;KK;;;E;;",
            ";C;;;C;;;;;;;;KK;;;;;;",
            ";C;a;;;;Q;Q;;;;;;MMM;;",
            ";CCCCC;;;;;;;E;;;MEM;;",
            ";;;;;;;;Z;;;;;;;;M;M;;",
            ";P;;;;;;;;;;;;v;;;;;n;",
            ";;;T;;;;;;;E;;;;;;;;;;",
        ],
    ),
    dict(
        name="SCRAPYARD",
        sky=[(0.0, (85, 90, 100)), (0.6, (145, 145, 150)), (0.9, (185, 180, 170)), (1.0, (200, 195, 185))],
        haze=(185, 180, 170), sun=None, stars=False, ground="#", lit=9, fog=0.85, snow=False,
        camo=dict(uniform=(90, 85, 70), vest=(60, 58, 50), pants=(70, 65, 55)),
        op="OPERATION RUSTBELT", brief="Hostiles dug in among the wrecks. Every car is cover - for them too.",
        rows=[
            "WWWWW###E######v####E#",
            "W###W##vv##KK###rrr###",
            "W#a#####v#######rrr#v#",
            "WW#WW###########rrr###",
            "###########X##########",
            "#vv##KK#E####vv##UU##E",
            "#v###KK#####vv###UU###",
            "######################",
            "P##########E######v###",
            "##rr##uu##KK##oo##vv##",
            "##rr##uu##KK##oo##v##E",
            "######################",
            "#X###vv####h####n###KK",
            "#####v###E#####vv###KK",
            "##E######W#WW#########",
            "#########W#aW####E###v",
        ],
    ),
    dict(
        name="BAZAAR",
        sky=[(0.0, (55, 105, 185)), (0.6, (125, 170, 220)), (0.9, (230, 215, 180)), (1.0, (245, 228, 195))],
        haze=(240, 225, 195), sun=-math.pi / 3, stars=False, ground=";", lit=8, fog=1.0, snow=False,
        camo=dict(uniform=(185, 160, 110), vest=(150, 125, 85), pants=(165, 140, 100)),
        op="OPERATION SPICE ROAD", brief="Crowded market streets. Clear every stall and courtyard.",
        rows=[
            "MMMMMMM;;;;E;;;;MMMMMM",
            "M;;a;;M;;CC;CC;;M;;n;M",
            "M;;;;;;;;CC;CC;;;;;;;M",
            "MMM;MMM;;;;;;;;;MMM;MM",
            ";;;;;;;KK;;;;;KK;;;;;;",
            ";E;C;C;;;;FF;;;;C;C;E;",
            ";;;C;C;;;;FF;;;;C;C;;;",
            "xxxxxxxxxxxxxxxxxxxxxx",
            "P;;;;;;;;;;T;;;;;;;;;E",
            "MMMMM;CC;CC;CC;CC;MMMM",
            "M;;;M;CC;CC;CC;CC;M;EM",
            "M;h;;;;;;;;E;;;;;;;;;M",
            "MMMMM;KK;;;;;;KK;MMMMM",
            ";;;;;;;;;MMMM;E;;;;;;;",
            ";E;;Q;;;;M;aM;;;Q;;;E;",
            ";;;;;;;;;M;;;;;;;;;;E;",
        ],
    ),
    dict(
        name="OIL RIG",
        sky=[(0.0, (5, 8, 15)), (0.6, (20, 28, 40)), (0.9, (45, 55, 70)), (1.0, (60, 70, 85))],
        haze=(50, 60, 75), sun=None, stars=False, ground=",", lit=4, fog=0.6, snow=False, rain=True, dark=0.62,
        camo=dict(uniform=(55, 60, 70), vest=(35, 38, 45), pants=(40, 42, 50)),
        op="OPERATION BLACKWATER", brief="Storm over the rig. Secure the platform before the chopper arrives.",
        rows=[
            "~~~~~~~~~~~~~~~~~~~~~~",
            "~,,,,,,,,,E,,,,,,,,,E~",
            "~,UU,,X,,,,,,UU,,KK,,~",
            "~,UU,,,,WWWW,UU,,KK,,~",
            "~,,,,,,,W,,W,,,,,,,,,~",
            "~,E,,,,,W,a,,,,,YY,,,~",
            "~,,KK,,,WWWW,,E,YY,,,~",
            "~P,,,,,,,,,,,,,,,,,,,~",
            "~,,,,YY,,,,,,,KK,,,E,~",
            "~,,,,YY,,UU,,,KK,,,,,~",
            "~,h,,,,,,UU,,,,,,X,,,~",
            "~,,,KK,,,,,,,n,,,,,,,~",
            "~,E,,,,,,,,E,,,,,,,E,~",
            "~~~~~~~~~~~~~~~~~~~~~~",
        ],
    ),
    # 좀비 모드 전용 맵 (캠페인에는 안 나와요)
    dict(
        name="BLOOD MOON", zombie=True,
        sky=[(0.0, (5, 2, 8)), (0.6, (30, 8, 18)), (0.9, (70, 18, 25)), (1.0, (95, 30, 30))],
        haze=(60, 18, 22), sun=0.6, sun_colors=((120, 20, 20), (190, 35, 35), (235, 80, 70)),
        stars=True, ground="g", lit=7, fog=0.55, snow=False, dark=0.5, camo=None,
        op="BLOOD MOON", brief="They are coming. Survive as long as you can.",
        rows=[
            "IgIggIgg#gggIggIggIgggIg",
            "gEgggggg#ggggggggggggEgg",
            "ggJJJJgg#ggVgVgVgggJJJgg",
            "ggJggJgg#gggggggggJ;aJgg",
            "ggJgaJgg#ggVgVgVgggJ;Jgg",
            "ggJJgJgg#gggggggggggg;gg",
            "Egggggg########L#######E",
            "ggVVggg#gggggggggg#ggggg",
            "gggggLg#ggJJJJJJgg#gIggg",
            "gIggggg#ggJggggJgg#ggggg",
            "ggggggg#gggghggJgg#gVVgg",
            "gggVVgg#ggJggggJgg#ggggg",
            "Egggggg#ggJJgJJJgg#ggggE",
            "gggggLg#gggggggggg#gggLg",
            "########L####P#########g",
            "ggIggggg#gggggggg#gggggg",
            "gggJJJgg#ggVVgVVg#gJJJgg",
            "gggJnJgg#ggggggg#ggJgaJg",
            "gEgJ;Jgg#gggg#ggggggJ;Jg",
            "IgggggIgggEgggIggggEgggI",
        ],
    ),
]


# 건물 종류: 글자 -> (색, 높이, 무늬, 네온사인 색 또는 None)
#   무늬: True = 창문, "ribs" = 컨테이너/창고 세로 골, False = 무늬 없음
WALLS = {
    "A": ((235, 150, 170), 2.0, True, (255, 80, 200)),
    "B": ((100, 195, 185), 1.6, True, (80, 240, 255)),
    "C": ((240, 205, 110), 1.2, True, (255, 150, 60)),
    "D": ((235, 230, 215), 2.2, True, (190, 110, 255)),
    "R": ((190, 95, 75), 2.5, True, None),
    "N": ((70, 40, 90), 1.4, False, (120, 255, 140)),
    "G": ((110, 140, 175), 3.0, True, (80, 240, 255)),
    "S": ((70, 90, 130), 4.0, True, (255, 80, 200)),
    "W": ((150, 150, 155), 2.0, "ribs", None),
    "r": ((190, 60, 50), 1.3, "ribs", None),
    "u": ((50, 90, 170), 1.3, "ribs", None),
    "o": ((230, 130, 40), 1.3, "ribs", None),
    "Y": ((215, 185, 60), 2.6, "ribs", None),
    "K": ((150, 110, 70), 1.0, False, None),
    "Q": ((40, 110, 70), 0.9, False, None),
    "F": ((200, 220, 235), 0.8, False, None),
    "M": ((200, 160, 110), 1.4, True, None),
    "O": ((140, 145, 150), 1.3, False, None),
    "U": ((225, 225, 220), 2.2, "ribs", None),
    "J": ((125, 85, 50), 1.5, True, None),
    "V": ((120, 120, 112), 0.9, False, None),
    "Z": ((165, 145, 100), 0.7, "ribs", None),
    "H": ((240, 238, 230), 3.2, "ribs", (255, 225, 120)),     # 등대: 높은 흰 탑, 꼭대기에 불빛
}

# 바닥 종류: 글자 -> 색
FLOORS = {
    "~": (40, 110, 170),
    ".": (225, 200, 150),
    "_": (150, 105, 70),
    ":": (175, 170, 165),
    "=": (65, 65, 75),
    "g": (95, 160, 80),
    "x": (215, 190, 200),
    ",": (160, 160, 150),
    "p": (125, 90, 60),
    ";": (215, 185, 130),
    "#": (135, 105, 75),
    "*": (232, 238, 245),
    "-": (190, 198, 210),
}
CAR_COLORS = [(255, 90, 170), (60, 210, 230), (245, 245, 245), (220, 40, 50), (255, 210, 60)]
PICKUP_TILES = {"a": "ammo", "h": "health", "n": "grenade"}

# ---------------------------------------------------------------
# 맵 자동 생성기: 도시 블록(건물, 공원, 주차장, 컨테이너, 시장...)을 이어 붙여 맵을 지어요.
# 같은 seed면 언제나 같은 맵이 나와요. 모든 빈칸이 서로 이어지도록 스스로 검사하고 고쳐요.
# ---------------------------------------------------------------
# 스타일: floor 블록 바닥, road 길 바닥, walls 건물 글자들, cover 엄폐물, tree 나무, green 잔디,
#         block (블록 가로, 세로), road_w 길 폭, kinds 블록 종류와 비율, border 맵 테두리 건물(없으면 None)
MAP_STYLES = {
    "suburb": dict(floor=":", road="=", walls="JCB", cover="KQV", tree="I", green="g", block=(6, 4), road_w=1,
                   kinds=[("house", 5), ("park", 2), ("parking", 1), ("plaza", 1)], border=None),
    "airfield": dict(floor=",", road="-", walls="WO", cover="ZKr", tree=None, green=",", block=(7, 5), road_w=1,
                     kinds=[("hangar", 4), ("yard", 2), ("compound", 2), ("plaza", 1)], border=None),
    "canyon": dict(floor=";", road="#", walls="MO", cover="ZKv", tree="T", green=";", block=(6, 4), road_w=1,
                   kinds=[("house", 3), ("compound", 3), ("ruins", 2)], border="M"),
    "trainyard": dict(floor=",", road="=", walls="WU", cover="ZKQ", tree=None, green=",", block=(7, 4), road_w=1,
                      kinds=[("yard", 5), ("hangar", 1), ("compound", 1)], border=None),
    "ruins": dict(floor="#", road="g", walls="RV", cover="VZ", tree="I", green="g", block=(6, 4), road_w=1,
                  kinds=[("ruins", 5), ("park", 2), ("house", 1)], border=None),
    "ski": dict(floor="*", road="-", walls="JO", cover="ZK", tree="I", green="*", block=(6, 4), road_w=1,
                kinds=[("lodge", 4), ("park", 3), ("compound", 1)], border=None),
    "jungle": dict(floor="g", road="#", walls="JM", cover="KZ", tree="T", green="g", block=(6, 4), road_w=1,
                   kinds=[("park", 4), ("lodge", 3), ("compound", 2)], border=None),
    "market": dict(floor="x", road=":", walls="NCA", cover="KQ", tree="T", green="x", block=(6, 4), road_w=1,
                   kinds=[("market", 4), ("house", 3), ("plaza", 2)], border="S"),
    "city": dict(floor=":", road="=", walls="GSDRAB", cover="KQZ", tree="T", green="g", block=(9, 7), road_w=2,
                 kinds=[("house", 6), ("plaza", 2), ("parking", 2), ("park", 2), ("yard", 1), ("compound", 1)],
                 border="S"),
    "desert": dict(floor=";", road="#", walls="MO", cover="ZKv", tree="T", green=";", block=(9, 7), road_w=2,
                   kinds=[("house", 5), ("compound", 3), ("ruins", 2), ("market", 2)], border="M"),
    "arctic": dict(floor="*", road="-", walls="OWU", cover="ZK", tree="I", green="*", block=(9, 7), road_w=2,
                   kinds=[("compound", 4), ("hangar", 3), ("lodge", 2), ("park", 2), ("yard", 1)], border="O"),
}
GEN_BLOCKERS = set("~TcXIv")


def generate_map(style_name, width, height, seed, spawns=10, pickups=2):
    """스타일대로 맵 줄들(rows)을 만들어 돌려줘요"""
    style = MAP_STYLES[style_name]
    rng = random.Random(seed)
    grid = [[style["floor"]] * width for _ in range(height)]
    bw, bh = style["block"]
    rw = style["road_w"]

    def is_road(i, size):
        return i % (size + rw) < rw

    def put(x, y, ch):
        if 0 <= x < width and 0 <= y < height:
            grid[y][x] = ch

    # 길
    for y in range(height):
        for x in range(width):
            if is_road(x, bw) or is_road(y, bh):
                grid[y][x] = style["road"]
    # 블록 채우기
    for by in range(rw, height, bh + rw):
        for bx in range(rw, width, bw + rw):
            w, h = min(bw, width - bx), min(bh, height - by)
            if w < 3 or h < 3:
                continue
            kind = rng.choices([k for k, _ in style["kinds"]], weights=[n for _, n in style["kinds"]])[0]
            fill_block(grid, style, kind, bx, by, w, h, rng)
    # 큰 맵: 넓은 길에 가로등과 자동차
    if rw >= 2:
        for y in range(height):
            for x in range(width):
                if grid[y][x] == style["road"] and rng.random() < 0.012:
                    grid[y][x] = "c" if style["road"] == "=" else rng.choice(style["cover"])
                elif grid[y][x] == style["road"] and rng.random() < 0.006:
                    grid[y][x] = "L"
    # 테두리
    if style["border"]:
        for x in range(width):
            grid[0][x] = grid[height - 1][x] = style["border"]
        for y in range(height):
            grid[y][0] = grid[y][width - 1] = style["border"]
    # 시작 위치: 왼쪽 위 근처의 길
    start = None
    for d in range(2 * max(width, height)):
        for x in range(0, d + 1):
            y = d - x
            if 0 < x < width - 1 and 0 < y < height - 1 and grid[y][x] == style["road"]:
                start = (x, y)
                break
        if start:
            break
    # 이어지지 않은 빈칸은 막아요 (갇힌 안뜰 등)
    walkable = lambda x, y: grid[y][x] not in WALLS and grid[y][x] not in GEN_BLOCKERS
    seen = {start}
    queue = deque([start])
    while queue:
        x, y = queue.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in seen and walkable(nx, ny):
                seen.add((nx, ny))
                queue.append((nx, ny))
    for y in range(height):
        for x in range(width):
            if walkable(x, y) and (x, y) not in seen:
                grid[y][x] = style["walls"][0]
    # 적 출현 위치와 상자: 시작에서 멀리, 서로 떨어지게
    cells = [c for c in seen if c != start and grid[c[1]][c[0]] in FLOORS]
    rng.shuffle(cells)
    chosen = []
    for c in cells:
        if len(chosen) >= spawns:
            break
        if math.dist(c, start) > 9 and all(math.dist(c, o) > 3 for o in chosen):
            chosen.append(c)
    for x, y in chosen:
        grid[y][x] = "E"
    for letter in "ahn":
        placed = 0
        for x, y in cells:
            if placed >= pickups:
                break
            if grid[y][x] in FLOORS and math.dist((x, y), start) > 3:
                grid[y][x] = letter
                placed += 1
    grid[start[1]][start[0]] = "P"
    return ["".join(row) for row in grid]


def fill_block(grid, style, kind, bx, by, w, h, rng):
    """블록 하나를 종류대로 채워요 (가장자리 한 칸은 인도로 비워 둬요)"""
    floor, wall = style["floor"], rng.choice(style["walls"])

    def put(x, y, ch):
        if by <= y < by + h and bx <= x < bx + w:
            grid[y][x] = ch

    x0, y0, x1, y1 = bx + 1, by + 1, bx + w - 2, by + h - 2       # 안쪽 사각형
    if kind in ("house", "hangar", "lodge"):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(x, y, wall if kind != "lodge" else "J")
        big = x1 - x0 >= 3 and y1 - y0 >= 2
        if big and (kind == "hangar" or rng.random() < 0.6):
            # 안이 빈 건물: 문 1~2개, 안에 엄폐물
            for y in range(y0 + 1, y1):
                for x in range(x0 + 1, x1):
                    put(x, y, floor)
            doors = [((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1), (x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2)]
            for door in rng.sample(doors, 2 if kind == "hangar" else rng.randint(1, 2)):
                put(*door, floor)
            if x1 - x0 >= 4:
                put(rng.randint(x0 + 1, x1 - 1), rng.randint(y0 + 1, y1 - 1), rng.choice(style["cover"]))
    elif kind == "park":
        for y in range(by, by + h):
            for x in range(bx, bx + w):
                put(x, y, style["green"])
        for _ in range(w * h // 6):
            if style["tree"]:
                put(rng.randint(x0, x1), rng.randint(y0, y1), style["tree"])
    elif kind == "plaza":
        for y in range(by, by + h):
            for x in range(bx, bx + w):
                put(x, y, "x" if style["floor"] in ":x" else floor)
        cx, cy = bx + w // 2, by + h // 2
        put(cx, cy, "F")
        for _ in range(3):
            put(rng.randint(x0, x1), rng.randint(y0, y1), rng.choice(style["cover"]))
        put(x0, y0, "L")
    elif kind == "parking":
        for y in range(y0, y1 + 1, 2):
            for x in range(x0, x1 + 1, 2):
                if rng.random() < 0.7:
                    put(x, y, "c" if style["road"] == "=" else rng.choice(style["cover"]))
    elif kind == "yard":
        containers = "ruoY"
        for y in range(y0, y1 + 1, 2):
            x = x0
            while x <= x1:
                length = rng.randint(2, 3)
                ch = rng.choice(containers)
                for k in range(length):
                    if x + k <= x1:
                        put(x + k, y, ch)
                x += length + 1
    elif kind == "compound":
        low = rng.choice([c for c in style["cover"] if c in "VZ"] or ["Z"])
        for x in range(x0, x1 + 1):
            put(x, y0, low)
            put(x, y1, low)
        for y in range(y0, y1 + 1):
            put(x0, y, low)
            put(x1, y, low)
        for _ in range(3 if x1 - x0 >= 2 and y1 - y0 >= 2 else 0):   # 틈(출입구)
            if rng.random() < 0.5:
                put(rng.randint(x0 + 1, x1 - 1), rng.choice((y0, y1)), floor)
            else:
                put(rng.choice((x0, x1)), rng.randint(y0 + 1, y1 - 1), floor)
        if x1 - x0 >= 3 and y1 - y0 >= 2:
            put((x0 + x1) // 2, (y0 + y1) // 2, wall)          # 가운데 벙커
    elif kind == "ruins":
        for _ in range(w * h // 4):
            x, y = rng.randint(x0, x1), rng.randint(y0, y1)
            if rng.random() < 0.5:
                for k in range(rng.randint(1, 3)):
                    put(x + k, y, rng.choice("VV" + wall))
            else:
                for k in range(rng.randint(1, 2)):
                    put(x, y + k, rng.choice("VV" + wall))
    elif kind == "market":
        for y in range(by, by + h):
            for x in range(bx, bx + w):
                put(x, y, "x" if style["floor"] in ":x" else floor)
        for y in range(y0, y1 + 1, 2):
            for x in range(x0, x1 + 1, 3):
                put(x, y, rng.choice("KC" if "C" in style["walls"] else "KQ"))
                put(x + 1, y, rng.choice("KC" if "C" in style["walls"] else "KQ"))
        put(x0, y1, "L")

WHITE = (240, 240, 240)
RED = (230, 50, 50)
YELLOW = (255, 220, 90)
GREEN = (90, 220, 120)
BLACK = (0, 0, 0)


# ---------------------------------------------------------------
# 맵 관련 도우미 함수
# ---------------------------------------------------------------
def floor_of(col, row):
    """그 칸의 바닥 종류. 자동차는 차도, 가로등은 인도 위에 있어요.
    'P', 'E', 'T', 상자 같은 칸은 왼쪽 칸의 바닥을 따라가요."""
    special = {"c": "=", "L": ":", "b": ":", "X": ",", "v": "#"}
    while col >= 0:
        ch = GAME_MAP[row][col]
        if ch in FLOORS:
            return ch
        if ch in special:
            return special[ch]
        col -= 1
    return "."


def load_map(index, theme=None):
    """index번째 맵으로 바꿔요. 다른 함수들이 쓰는 맵 정보(전역 변수)를 새로 채워요.
    theme: 분위기를 바꾼 맵 정보 (세트마다 밤/폭풍우 등). 없으면 원래 맵"""
    global GAME_MAP, MAP_W, MAP_H, FLOOR_GRID, WALL_GRID, MAX_WALL, HAZE, LIT, FLOOR_COLORS
    theme = theme or MAPS[index]
    GAME_MAP = list(theme["rows"])     # 복사본: 게임 중에 상자가 부서져도 원래 맵은 그대로
    MAP_W, MAP_H = len(GAME_MAP[0]), len(GAME_MAP)
    # 매번 계산하지 않도록 칸마다 바닥/건물 정보를 미리 만들어 둬요
    FLOOR_GRID = [[floor_of(col, row) for col in range(MAP_W)] for row in range(MAP_H)]
    # 밤 맵(dark)은 바닥과 건물을 어둡게 칠해요. 네온사인은 그대로 밝게
    dark = theme.get("dark", 1.0)
    FLOOR_COLORS = {k: shade(c, dark) for k, c in FLOORS.items()}
    walls = {k: (shade(c, dark), h, pattern, neon) for k, (c, h, pattern, neon) in WALLS.items()}
    WALL_GRID = [[walls.get(ch) for ch in line] for line in GAME_MAP]
    # 이 맵에서 가장 높은 건물 (광선이 여기에 닿으면 더 멀리 안 봐도 돼요)
    MAX_WALL = max((spec[1] for line in WALL_GRID for spec in line if spec), default=1.0)
    HAZE = theme["haze"]
    LIT = theme["lit"]
    _fog_cache.clear()           # 안개 색이 바뀌었으니 기억해 둔 색을 지워요


def in_map(col, row):
    return 0 <= col < MAP_W and 0 <= row < MAP_H


def is_blocked(x, y):
    """그 위치로 걸어갈 수 없으면 True (건물, 바다, 나무, 자동차, 크레인, 맵 바깥)"""
    col, row = int(x), int(y)
    if not in_map(col, row):
        return True
    ch = GAME_MAP[row][col]
    return ch in WALLS or ch in "~TcXIv"


def is_opaque(x, y):
    """그 위치가 시야를 가리면 True (건물만 가려요)"""
    col, row = int(x), int(y)
    return in_map(col, row) and WALL_GRID[row][col] is not None


def obstacle_height(x, y):
    """날아가는 수류탄/로켓이 부딪히는 높이. 건물은 건물 높이, 자동차는 0.6, 맵 바깥은 아주 높게."""
    col, row = int(x), int(y)
    if not in_map(col, row):
        return 99.0
    spec = WALL_GRID[row][col]
    if spec:
        return spec[1]
    return 0.6 if GAME_MAP[row][col] in "cv" else 0.0


def find_cells(letter):
    """맵에서 특정 글자가 있는 칸들의 '가운데 좌표' 목록"""
    return [(col + 0.5, row + 0.5)
            for row, line in enumerate(GAME_MAP)
            for col, ch in enumerate(line) if ch == letter]


def can_see(a, b):
    """a에서 b까지 건물에 가리지 않고 직선으로 보이면 True"""
    dist = a.distance_to(b)
    steps = int(dist / 0.1) + 1
    x, y = a.x, a.y
    sx, sy = (b.x - x) / steps, (b.y - y) / steps
    grid, width, height = WALL_GRID, MAP_W, MAP_H
    for _ in range(1, steps):                    # 0.1칸씩 가며 건물에 막히는지 봐요
        x += sx
        y += sy
        col, row = int(x), int(y)
        if 0 <= col < width and 0 <= row < height and grid[row][col] is not None:
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
        walls : [(거리, 세로벽인지, 벽에 맞은 위치 0~1, 건물 정보, 칸 x, 칸 y), ...]  가까운 순서
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
    floor_grid, wall_grid, width, height, max_depth, max_wall = FLOOR_GRID, WALL_GRID, MAP_W, MAP_H, MAX_DEPTH, MAX_WALL
    cur_floor = floor_grid[map_y][map_x]
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

        if dist > max_depth or not (0 <= map_x < width and 0 <= map_y < height):
            if not walls:                      # 건물이 없으면 바닥이 지평선까지 이어져요
                floors.append((seg_start, math.inf, cur_floor))
            break

        spec = wall_grid[map_y][map_x]
        if spec:
            if not walls:
                floors.append((seg_start, dist, cur_floor))
            if spec[1] > tallest:
                hit = py + dy * dist if vertical else px + dx * dist
                walls.append((dist, vertical, hit - math.floor(hit), spec, map_x, map_y))
                tallest = spec[1]
                if tallest >= max_wall:
                    break
        elif not walls:
            f = floor_grid[map_y][map_x]
            if f != cur_floor:
                floors.append((seg_start, dist, cur_floor))
                seg_start, cur_floor = dist, f
    return floors, walls


def angle_diff(a, b):
    """두 각도의 차이를 -π ~ π 범위로"""
    return (a - b + math.pi) % (2 * math.pi) - math.pi


_fog_cache = {}


def fog(color, dist, fog_dist):
    """멀수록 노을 빛 안개 색에 가까워지게.
    같은 계산을 계속 반복하지 않도록, 한 번 구한 색은 기억해 뒀다가 다시 써요."""
    key = (color, int(dist * 4), fog_dist)
    if key not in _fog_cache:
        t = min(1.0, key[1] / 4 / fog_dist) * 0.8
        _fog_cache[key] = tuple(int(c + (h - c) * t) for c, h in zip(color, HAZE))
    return _fog_cache[key]


def shade(color, amount):
    return tuple(int(c * amount) for c in color)


# 생성기로 만든 캠페인 맵 8개 (모두 합쳐 20개)
def sky(top, mid, low, horizon):
    return [(0.0, top), (0.6, mid), (0.9, low), (1.0, horizon)]


DESERT_CAMO = dict(uniform=(185, 160, 110), vest=(150, 125, 85), pants=(165, 140, 100))
GENERATED_MAPS = [
    dict(name="SUBURB", sky=sky((70, 130, 210), (140, 185, 230), (215, 225, 230), (230, 235, 235)),
         haze=(220, 228, 232), sun=-1.0, stars=False, ground=":", lit=7, fog=1.0, snow=False, camo=None,
         op="OPERATION PICKET FENCE", brief="Hostiles holed up in a quiet neighborhood. Clear the houses.",
         rows=generate_map("suburb", 26, 18, 11)),
    dict(name="AIRFIELD", sky=sky((50, 50, 110), (170, 100, 120), (250, 160, 100), (255, 200, 140)),
         haze=(245, 180, 140), sun=math.pi * 0.8, stars=False, ground=",", lit=6, fog=1.1, snow=False, camo=None,
         op="OPERATION RUNWAY", brief="Take the airfield. Hangars and fuel depots - watch the open tarmac.",
         rows=generate_map("airfield", 26, 18, 12)),
    dict(name="CANYON OUTPOST", sky=sky((60, 110, 190), (130, 175, 225), (235, 205, 170), (245, 220, 185)),
         haze=(240, 215, 180), sun=-math.pi / 2, stars=False, ground=";", lit=9, fog=1.1, snow=False,
         camo=DESERT_CAMO, op="OPERATION RED ROCK", brief="An outpost hidden in the canyon. Sandbags everywhere.",
         rows=generate_map("canyon", 26, 18, 13)),
    dict(name="TRAINYARD", sky=sky((95, 100, 110), (150, 150, 155), (185, 180, 175), (195, 190, 185)),
         haze=(185, 180, 172), sun=None, stars=False, ground=",", lit=9, fog=0.85, snow=False,
         camo=dict(uniform=(90, 85, 70), vest=(60, 58, 50), pants=(70, 65, 55)),
         op="OPERATION IRON HORSE", brief="Rows of freight cars. Fight down the narrow lanes.",
         rows=generate_map("trainyard", 26, 18, 14)),
    dict(name="CASTLE RUINS", sky=sky((90, 115, 145), (150, 168, 180), (200, 205, 200), (210, 215, 208)),
         haze=(195, 202, 196), sun=None, stars=False, ground="g", lit=9, fog=0.6, snow=False,
         camo=dict(uniform=(70, 95, 55), vest=(50, 70, 40), pants=(60, 70, 50)),
         op="OPERATION OLD STONE", brief="Fog over the old ruins. Low walls - shoot over them.",
         rows=generate_map("ruins", 26, 18, 15)),
    dict(name="SKI LODGE", sky=sky((60, 120, 200), (140, 185, 230), (220, 230, 240), (235, 240, 248)),
         haze=(225, 232, 242), sun=0.4, stars=False, ground="*", lit=5, fog=0.9, snow=True,
         camo=dict(uniform=(225, 228, 232), vest=(165, 170, 180), pants=(200, 205, 212)),
         op="OPERATION POWDER", brief="Mountain lodges in fresh snow. They blend in - look closely.",
         rows=generate_map("ski", 26, 18, 16)),
    dict(name="JUNGLE CAMP", sky=sky((70, 110, 100), (130, 165, 140), (185, 200, 170), (195, 210, 180)),
         haze=(170, 190, 160), sun=None, stars=False, ground="g", lit=9, fog=0.5, snow=False,
         camo=dict(uniform=(60, 90, 45), vest=(45, 70, 35), pants=(55, 70, 45)),
         op="OPERATION GREEN HELL", brief="Thick jungle and hidden huts. Listen before you look.",
         rows=generate_map("jungle", 26, 18, 17)),
    dict(name="NIGHT MARKET", sky=sky((10, 8, 30), (40, 20, 70), (100, 40, 110), (140, 60, 130)),
         haze=(70, 40, 95), sun=None, stars=True, ground="x", lit=2, fog=0.9, snow=False, dark=0.8, camo=None,
         op="OPERATION LANTERN", brief="Crowded night market under neon. Stalls give cover to both sides.",
         rows=generate_map("market", 26, 18, 18)),
]
# 손으로 그린 맵: 노을 진 바닷가 절벽 어촌과 등대
#   위쪽 바다와 나무 부두 -> 해변과 어시장(W) -> 나무집 골목(J) -> 언덕 위 돌담(V)과 등대(U), 소나무 숲(I)
LIGHTHOUSE_POINT = dict(
    name="LIGHTHOUSE POINT", sky=sky((60, 70, 140), (190, 120, 130), (250, 170, 110), (255, 205, 150)),
    haze=(245, 190, 150), sun=-math.pi / 2, stars=False, ground=".", lit=4, fog=1.0, snow=False, camo=None,
    op="OPERATION BEACON", brief="A fishing village on the cliffs. Take the docks, then the lighthouse.",
    rows=[
               "~~~~~~~~~~~~~~~~~~~~~~~~~~",
               "~~~~pp~~~~~~~~~pp~~~~~~~~~",
               "~~~~pE~~~~~~~~~pp~~~~~~~~~",
               "~~..pp...~~~~..pp,,,~~~~~~",
               "~...,,,K..E.~..,,,,K,..~~~",
               "~..E,,,,......,,WWW,,.E.~~",
               "~.....:::::::.,,W,W,.....~",
               "~.JJJ.:.JJJ.:.,,,,,,.JJJE~",
               "~.J.J.:.J.J.:....:::.J.J.~",
               "~.J.JL:.J...:Ka..:.:.J...~",
               "~.....:::::::::::::::::..~",
               "~ggVVVg:.JJJJ.:.Q.:.VVVggg",
               "gggg.Vg:.J..J.:.F.:gVgggVg",
               "gEggIgg:.J.hJ.:...:gVgHHgg",
               "ggIggg#:.JJ.J.:Ln.:gggHHgE",
               "g#####P:......::::#ggVgggg",
               "gggIggg#############gVVVgI",
               "IgEggIggggggIggggEgggggIgg",
    ],
)
MAPS[-1:-1] = [LIGHTHOUSE_POINT] + GENERATED_MAPS     # 좀비 맵(마지막) 앞에 넣어요 (등대는 13번째 맵)

# 장기 미션: 아주 큰 맵(64x44칸)에서 다섯 단계 작전. 단계를 마칠 때마다 체크포인트에 저장돼요
MISSION_STAGES = [("REACH", "INFILTRATE - REACH THE RALLY POINT"), ("HOSTAGE", "RESCUE THE DOWNED PILOT"),
                  ("CACHE", "DESTROY 3 WEAPON CACHES"), ("HOLD", "HOLD THE LANDING ZONE"),
                  ("REACH", "REACH EXTRACTION")]
MISSIONS = [
    dict(name="IRON CITY", style="city", seed=21,
         desc=("해 질 녘 거대한 도시. 마천루와 광장, 주차장 사이를 뚫고 나가요.",
               "A huge city at dusk. Fight through towers, plazas and parking lots."),
         theme=dict(sky=sky((40, 30, 90), (150, 70, 140), (245, 120, 120), (250, 170, 140)), haze=(240, 160, 140),
                    sun=math.pi, stars=False, ground=":", lit=3, fog=0.9, snow=False, camo=None)),
    dict(name="DUST STORM", style="desert", seed=22,
         desc=("모래바람이 부는 사막 도시. 흙벽돌 골목과 진지를 지나요.",
               "A desert town in a sandstorm. Mud-brick alleys and fortified compounds."),
         theme=dict(sky=sky((150, 130, 100), (200, 175, 135), (225, 200, 160), (230, 210, 170)), haze=(215, 190, 150),
                    sun=None, stars=False, ground=";", lit=9, fog=0.55, snow=False, camo=DESERT_CAMO)),
    dict(name="FROSTBITE", style="arctic", seed=23,
         desc=("눈보라 치는 밤의 북극 기지. 격납고와 벙커를 차례로 장악해요.",
               "An arctic base on a snowy night. Take hangars and bunkers one by one."),
         theme=dict(sky=sky((10, 15, 35), (35, 50, 80), (90, 110, 140), (150, 165, 185)), haze=(150, 165, 185),
                    sun=None, stars=True, ground="*", lit=3, fog=0.7, snow=True, dark=0.7,
                    camo=dict(uniform=(225, 228, 232), vest=(165, 170, 180), pants=(200, 205, 212)))),
]
for _m in MISSIONS:
    MAPS.append(dict(_m["theme"], name=_m["name"], mission=True, op=f"MISSION {_m['name']}",
                     brief=_m["desc"][1], rows=generate_map(_m["style"], 64, 44, _m["seed"], spawns=55, pickups=10)))
    _m["map"] = len(MAPS) - 1

# 캠페인에서 라운드마다 돌아가며 나오는 맵 (좀비, 미션 맵은 빼고) - 21개.
# 세트는 20라운드씩이라 세트마다 시작 맵이 하나씩 밀려요
CAMPAIGN_MAPS = [i for i, m in enumerate(MAPS) if not m.get("zombie") and not m.get("mission")]
ZOMBIE_MAP = next(i for i, m in enumerate(MAPS) if m.get("zombie"))

# 캠페인 100라운드 = 20라운드 x 5세트 (맵 21개가 차례로 돌아요). 세트마다 분위기가 바뀌고 적이 강해져요
CAMPAIGN_ROUNDS = 100
SET_SIZE = 20
SETS = ["RECON", "ASSAULT", "NIGHT OPS", "STORM", "VETERAN"]


def set_of(round_no):
    return min(len(SETS), (round_no - 1) // SET_SIZE + 1)


def variant_theme(theme, set_no):
    """세트에 따라 맵 분위기를 바꿔요: 3세트 밤, 4세트 폭풍우, 5세트 붉은 하늘"""
    theme = dict(theme)
    if set_no == 3:
        theme.update(sky=[(t, shade(c, 0.3)) for t, c in theme["sky"]], haze=shade(theme["haze"], 0.35),
                     sun=None, stars=True, lit=2, dark=min(theme.get("dark", 1.0), 0.55), fog=theme["fog"] * 0.8)
    elif set_no == 4:
        theme.update(sky=[(t, shade(c, 0.5)) for t, c in theme["sky"]], haze=shade(theme["haze"], 0.55),
                     sun=None, dark=min(theme.get("dark", 1.0), 0.72), fog=theme["fog"] * 0.7,
                     rain=not theme["snow"])
    elif set_no == 5:
        theme.update(sky=[(t, (min(255, int(c[0] * 1.1) + 40), int(c[1] * 0.55), int(c[2] * 0.5)))
                          for t, c in theme["sky"]],
                     haze=(200, 110, 90), dark=min(theme.get("dark", 1.0), 0.85))
    return theme


load_map(0)       # 처음엔 첫 번째 맵


# ---------------------------------------------------------------
# 그림 만들기 (이미지 파일 없이 도형으로 그려요)
# ---------------------------------------------------------------
# ---------------------------------------------------------------
# 벽 질감: 그림 파일 없이 코드로 그려요. 32x32 한 장을 건물 높이만큼 위로 이어 붙여요
# ---------------------------------------------------------------
TEXTURE_KINDS = {"R": "brick", "M": "stucco", "A": "stucco", "B": "stucco", "C": "stucco", "D": "stucco",
                 "N": "panel", "G": "panel", "S": "panel", "W": "metal", "r": "metal", "u": "metal", "o": "metal",
                 "Y": "metal", "U": "metal", "H": "metal", "K": "planks", "J": "planks", "Q": "metal",
                 "F": "stone", "O": "concrete", "V": "stone", "Z": "sandbag"}
TEX = 32                          # 질감 한 장의 크기 (px)
FOG_LEVELS = 8                    # 안개 단계 (멀수록 안개 색에 가까운 그림을 미리 만들어 둬요)


def make_texture_tile(kind, color, seed):
    """벽 질감 한 장 (32x32)"""
    rng = random.Random(seed)
    tile = pygame.Surface((TEX, TEX))
    tile.fill(color)

    def dot(x, y, amount):
        tile.set_at((x % TEX, y % TEX), lighter(color, amount))

    if kind == "brick":
        mortar = lighter(color, 1.25)
        for row in range(4):                                 # 벽돌 4줄, 줄마다 엇갈리게
            y = row * 8
            offset = 8 if row % 2 else 0
            for col in range(3):
                x = (col * 16 + offset) % TEX
                pygame.draw.rect(tile, lighter(color, rng.uniform(0.82, 1.08)), (x, y, 15, 7))
            pygame.draw.line(tile, mortar, (0, y + 7), (TEX, y + 7))
            for col in range(3):
                pygame.draw.line(tile, mortar, ((col * 16 + offset + 15) % TEX, y), ((col * 16 + offset + 15) % TEX, y + 7))
    elif kind == "stucco":
        for _ in range(140):                                 # 회벽 얼룩
            dot(rng.randrange(TEX), rng.randrange(TEX), rng.uniform(0.86, 1.08))
        pygame.draw.line(tile, lighter(color, 0.85), (0, TEX - 1), (TEX, TEX - 1))
    elif kind == "planks":
        for y in range(0, TEX, 6):                           # 나무 판자 (가로)
            pygame.draw.rect(tile, lighter(color, rng.uniform(0.85, 1.08)), (0, y, TEX, 5))
            pygame.draw.line(tile, lighter(color, 0.6), (0, y + 5), (TEX, y + 5))
        for _ in range(30):
            dot(rng.randrange(TEX), rng.randrange(TEX), 0.75)          # 나뭇결
    elif kind == "metal":
        for x in range(0, TEX, 4):                           # 골함석 (세로 골)
            pygame.draw.line(tile, lighter(color, 1.12), (x, 0), (x, TEX))
            pygame.draw.line(tile, lighter(color, 0.72), (x + 2, 0), (x + 2, TEX))
        for _ in range(25):
            dot(rng.randrange(TEX), rng.randrange(TEX), rng.uniform(0.6, 0.85))   # 녹슨 자국
    elif kind == "panel":
        pygame.draw.line(tile, lighter(color, 0.7), (0, TEX - 1), (TEX, TEX - 1))
        pygame.draw.line(tile, lighter(color, 0.7), (TEX // 2, 0), (TEX // 2, TEX))
        for _ in range(40):
            dot(rng.randrange(TEX), rng.randrange(TEX), rng.uniform(0.9, 1.06))
    elif kind == "concrete":
        for _ in range(160):
            dot(rng.randrange(TEX), rng.randrange(TEX), rng.uniform(0.8, 1.06))
        pygame.draw.line(tile, lighter(color, 0.7), (0, TEX - 1), (TEX, TEX - 1))
    elif kind == "stone":
        for _ in range(12):                                  # 울퉁불퉁한 돌
            w, h = rng.randint(6, 11), rng.randint(5, 8)
            x, y = rng.randrange(TEX), rng.randrange(TEX)
            pygame.draw.rect(tile, lighter(color, rng.uniform(0.8, 1.1)), (x, y, w, h), border_radius=3)
            pygame.draw.rect(tile, lighter(color, 0.62), (x, y, w, h), 1, border_radius=3)
    elif kind == "sandbag":
        for row in range(4):
            for col in range(3):
                x = col * 12 - (6 if row % 2 else 0)
                pygame.draw.ellipse(tile, lighter(color, rng.uniform(0.88, 1.05)), (x, row * 8, 13, 9))
                pygame.draw.ellipse(tile, lighter(color, 0.7), (x, row * 8, 13, 9), 1)
    return tile


def make_wall_textures(letter, color, height, haze):
    """[세로벽/가로벽][안개 단계] -> 건물 높이만큼 이어 붙인 질감"""
    tile = make_texture_tile(TEXTURE_KINDS.get(letter, "concrete"), color, letter)
    repeats = max(1, round(height / 0.5))                    # 0.5칸(한 층의 절반)마다 한 장
    tall = pygame.Surface((TEX, TEX * repeats))
    for k in range(repeats):
        tall.blit(tile, (0, k * TEX))
    pygame.draw.line(tall, shade(color, 0.6), (0, 0), (0, tall.get_height()))          # 건물 모서리 선
    pygame.draw.line(tall, shade(color, 0.6), (TEX - 1, 0), (TEX - 1, tall.get_height()))
    sides = []
    for side_shade in (0.82, 1.0):                           # 세로벽은 조금 어둡게
        levels = []
        for k in range(FOG_LEVELS):
            t = 0.8 * k / (FOG_LEVELS - 1)                   # fog() 와 같은 섞는 비율
            img = tall.copy()
            keep = int(255 * side_shade * (1 - t))
            img.fill((keep, keep, keep), special_flags=pygame.BLEND_MULT)
            img.fill(tuple(int(h * t) for h in haze), special_flags=pygame.BLEND_ADD)
            levels.append(img)
        sides.append(levels)
    return sides


def make_glow(size, color):
    """빛 번짐 그림 (검은 바탕 + 가운데가 밝은 원). 더하기(BLEND_ADD)로 붙이면 빛처럼 보여요"""
    img = pygame.Surface((size, size))
    for k in range(12, 0, -1):
        amount = (1 - k / 12) ** 2
        pygame.draw.circle(img, tuple(int(c * amount) for c in color), (size // 2, size // 2), size // 2 * k // 12)
    return img


def make_drone_image(state="normal"):
    """정찰 드론: 납작한 몸통, 프로펠러 4개, 빨간 눈 (flash = 아래 총구 불꽃)"""
    img = pygame.Surface((60, 36), pygame.SRCALPHA)
    body = (230, 140, 140) if state == "hurt" else (70, 75, 85)
    for x in (4, 40):                                           # 프로펠러 팔과 날개
        pygame.draw.rect(img, (40, 42, 50), (x + 4, 12, 12, 4))
        pygame.draw.ellipse(img, (160, 170, 185), (x - 2, 6, 22, 6))
    pygame.draw.rect(img, body, (14, 12, 32, 16), border_radius=6)
    pygame.draw.rect(img, (40, 42, 50), (14, 12, 32, 16), 2, border_radius=6)
    pygame.draw.circle(img, (255, 50, 50) if state != "aim" else WHITE, (30, 21), 4)   # 카메라 눈
    pygame.draw.rect(img, (25, 25, 25), (27, 28, 6, 6))                           # 총
    if state == "flash":
        pygame.draw.circle(img, YELLOW, (30, 33), 4)
    return img


def make_enemy_image(look, state="normal"):
    """적 그림. state: normal(평소) / flash(총구 불꽃) / hurt(맞음) / aim(저격 조준 불빛)"""
    if look["head"] == "zombie":
        return make_zombie_image(look, state)
    if look["head"] == "drone":
        return make_drone_image(state)
    if state == "hurt":
        # 맞으면 붉게 물들고 몸에 핏자국이 생겨요
        img = make_enemy_image(look, "normal")
        img.fill((255, 120, 120, 255), special_flags=pygame.BLEND_RGBA_MULT)
        for x, y, r in ((24, 50, 7), (36, 62, 5), (30, 44, 4), (20, 70, 4)):
            pygame.draw.circle(img, BLOOD, (x, y), r)
        return img
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
        pygame.draw.rect(img, vest, (16, 38, 28, 30), border_radius=4)     # 조끼/셔츠
    if look["head"] == "slick" and not hurt:
        pygame.draw.lines(img, (240, 200, 60), False, [(22, 40), (30, 54), (38, 40)], 2)   # 금목걸이
    if look.get("belt"):
        for x in (18, 26, 34, 42):
            pygame.draw.circle(img, (60, 90, 50), (x, 72), 4)              # 허리의 수류탄
    if look.get("cross"):
        pygame.draw.rect(img, (220, 30, 30), (27, 42, 6, 20))              # 조끼의 빨간 십자
        pygame.draw.rect(img, (220, 30, 30), (20, 49, 20, 6))

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
    elif head == "beret":
        pygame.draw.circle(img, skin, (30, 20), 12)
        pygame.draw.ellipse(img, (150, 40, 40), (14, 3, 32, 13))                 # 베레모
        pygame.draw.rect(img, BLACK, (24, 19, 4, 3))
        pygame.draw.rect(img, BLACK, (33, 19, 4, 3))
    elif head == "riot":
        pygame.draw.circle(img, (30, 35, 60) if not hurt else pale, (30, 18), 15)   # 진압 헬멧
        pygame.draw.rect(img, (150, 200, 230), (18, 12, 24, 12), border_radius=3)    # 투명 가리개
    elif head == "slick":
        pygame.draw.circle(img, skin, (30, 20), 12)
        pygame.draw.rect(img, (40, 30, 25), (17, 5, 26, 9), border_radius=4)        # 넘긴 머리
        pygame.draw.rect(img, BLACK, (21, 17, 18, 5), border_radius=2)              # 선글라스
    elif head == "mask":
        pygame.draw.circle(img, (30, 30, 34), (30, 20), 12)                        # 복면
        pygame.draw.rect(img, skin, (22, 16, 16, 6))
        pygame.draw.rect(img, (200, 40, 40), (23, 17, 14, 4))                      # 빨간 고글
    elif head == "medic":
        pygame.draw.circle(img, skin, (30, 20), 12)
        pygame.draw.rect(img, (245, 245, 245), (18, 6, 24, 9), border_radius=5)    # 흰 모자
        pygame.draw.rect(img, (220, 30, 30), (28, 7, 4, 7))                        # 빨간 십자
        pygame.draw.rect(img, (220, 30, 30), (26, 9, 8, 3))
    else:  # heavy
        pygame.draw.circle(img, (40, 42, 55) if not hurt else pale, (30, 17), 15)   # 통 헬멧
        pygame.draw.rect(img, (120, 200, 230), (20, 14, 20, 6))                     # 바이저

    gun = look["gun"]
    gun_x = 26
    if look.get("shield"):
        # 방패: 몸 앞을 크게 가려요. 총은 방패 옆으로 내밀어요
        pygame.draw.rect(img, pale if hurt else (45, 55, 75), (0, 32, 46, 82), border_radius=6)
        pygame.draw.rect(img, (110, 120, 140), (0, 32, 46, 82), 3, border_radius=6)
        pygame.draw.rect(img, (150, 200, 230), (10, 44, 26, 6), border_radius=2)     # 들여다보는 창
        gun_x = 40
    pygame.draw.rect(img, (25, 25, 25), (gun_x, 52, min(gun, 60 - gun_x), 8 if heavy else 7))   # 총
    if look.get("sandbags"):
        # 모래주머니 진지: 다리를 가리고 총을 그 위에 걸쳐요
        for row, y in enumerate((96, 84, 72)):
            for k in range(4 - row % 2):
                x = 2 + k * 15 + (7 if row % 2 else 0)
                pygame.draw.ellipse(img, (175, 150, 105), (x, y, 16, 14))
                pygame.draw.ellipse(img, (130, 110, 75), (x, y, 16, 14), 1)
    if state == "flash":
        pygame.draw.circle(img, YELLOW, (min(59, gun_x + gun), 55), 8)            # 총구 불꽃
    if state == "aim":
        pygame.draw.circle(img, (255, 40, 40), (34, 50), 6)                       # 조준경 반짝임
        pygame.draw.circle(img, WHITE, (34, 50), 2)
    return img


def make_back_image(look):
    """뒷모습: 얼굴 대신 뒤통수나 헬멧 뒤, 조끼 대신 배낭 (총은 반대쪽으로)"""
    img = pygame.transform.flip(make_enemy_image(look, "normal"), True, False)
    head = look["head"]
    back_colors = {"helmet": (50, 60, 45), "cap": (210, 40, 40), "hood": look["vest"], "riot": (30, 35, 60),
                   "mask": (30, 30, 34), "medic": (245, 245, 245), "heavy": (40, 42, 55)}
    color = back_colors.get(head, (45, 33, 25))                 # 나머지는 머리카락
    if head in ("riot", "heavy", "hood"):
        pygame.draw.circle(img, color, (30, 18), 15)
    else:
        pygame.draw.circle(img, color, (30, 19), 13)
    pack = shade(look["vest"], 0.7)
    pygame.draw.rect(img, pack, (17, 36, 26, 32), border_radius=5)              # 배낭
    pygame.draw.rect(img, shade(look["vest"], 0.45), (17, 36, 26, 32), 2, border_radius=5)
    pygame.draw.rect(img, shade(look["vest"], 0.55), (21, 56, 18, 8), border_radius=2)   # 주머니
    return img


def walk_frame(img, side):
    """걷는 그림: 한쪽 다리를 들어 올린 모습 (side 0 = 왼다리, 1 = 오른다리)"""
    frame = img.copy()
    legs = img.subsurface((0, 80, 60, 40)).copy()
    frame.fill((0, 0, 0, 0), (0, 84, 60, 36))
    for half in (0, 1):
        lift = 7 if half == side else 0
        frame.blit(legs, (half * 30, 80 - lift), (half * 30, 0, 30, 40))
    return frame


def make_zombie_image(look, state="normal"):
    """좀비 그림: 찢어진 옷, 피 얼룩, 빛나는 눈, 앞으로 뻗은 팔. flash = 할퀴는 모습(팔을 들고 입을 벌려요)"""
    if state == "hurt":
        img = make_zombie_image(look, "normal")
        img.fill((255, 120, 120, 255), special_flags=pygame.BLEND_RGBA_MULT)
        for x, y, r in ((24, 50, 7), (36, 62, 5), (30, 30, 4)):
            pygame.draw.circle(img, BLOOD, (x, y), r)
        return img
    img = pygame.Surface((60, 120), pygame.SRCALPHA)
    skin, shirt, pants = look["skin"], look["shirt"], look["pants"]
    rot = shade(skin, 0.65)
    big, thin = look.get("big"), look.get("thin")
    bw = 44 if big else (26 if thin else 34)          # 몸통 폭
    bx = 30 - bw // 2
    # 다리: 한쪽을 질질 끌어요
    leg = bw // 2 - 3
    pygame.draw.rect(img, pants, (bx + 2, 80, leg, 40))
    pygame.draw.rect(img, pants, (31, 84, leg, 34))
    pygame.draw.rect(img, rot, (32, 112, leg - 2, 8))
    # 몸통: 찢어진 셔츠와 피 얼룩
    pygame.draw.rect(img, shirt, (bx, 32, bw, 50), border_radius=5)
    pygame.draw.polygon(img, (0, 0, 0, 0), [(bx, 82), (bx + bw * 0.3, 72), (bx + bw * 0.5, 82)])
    pygame.draw.polygon(img, (0, 0, 0, 0), [(bx + bw * 0.6, 82), (bx + bw * 0.8, 70), (bx + bw, 82)])
    pygame.draw.polygon(img, rot, [(bx + 5, 62), (bx + 12, 50), (bx + 16, 66)])
    for x, y, r in ((bx + 8, 44, 5), (bx + bw - 9, 58, 4), (30, 70, 6), (bx + bw - 6, 40, 3)):
        pygame.draw.circle(img, BLOOD, (x, y), r)
    # 머리: 썩은 자국, 헝클어진 머리카락, 빛나는 눈
    hr = 13 if big else 11
    pygame.draw.circle(img, skin, (30, 20), hr)
    pygame.draw.circle(img, rot, (25, 15), 4)
    pygame.draw.circle(img, rot, (36, 26), 3)
    for x in range(22, 40, 4):
        pygame.draw.line(img, (40, 35, 30), (x, 20 - hr + 2), (x + random.randint(-3, 3), 20 - hr - 4), 2)
    eyes = look["eyes"]
    for ex in (25, 35):
        pygame.draw.circle(img, (*eyes, 90), (ex, 19), 5)
        pygame.draw.circle(img, eyes, (ex, 19), 2)
    if state == "flash":
        pygame.draw.ellipse(img, (40, 0, 0), (25, 23, 10, 8))       # 벌린 입
    else:
        pygame.draw.line(img, (40, 10, 10), (25, 27), (35, 26), 2)
    if look.get("bloated"):
        # 부풀어 오른 배: 초록빛으로 빛나요
        pygame.draw.circle(img, (120, 170, 60), (30, 62), 19)
        pygame.draw.circle(img, (190, 240, 90), (30, 62), 12)
        pygame.draw.circle(img, (230, 255, 150), (26, 58), 5)
    if look.get("spit"):
        for x in (27, 30, 33):
            pygame.draw.line(img, (120, 255, 100), (x, 27), (x, 34 + (x % 3) * 2), 2)   # 초록 침
    # 팔: 나를 향해 앞으로 뻗어요 (할퀼 때는 높이 들어요)
    hand_y = 24 if state == "flash" else 40
    for side in (-1, 1):
        shoulder = (30 + side * (bw // 2 - 2), 38)
        hand = (max(5, min(55, 30 + side * (bw // 2 + 9))), hand_y)
        pygame.draw.line(img, shirt, shoulder, hand, 9 if big else 7)
        pygame.draw.circle(img, skin, hand, 6 if big else 5)
        for k in (-1, 0, 1):
            pygame.draw.line(img, rot, hand, (hand[0] + side * 4 + k * 2, hand[1] - 6), 1)
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


def make_car_image(color):
    """80년대 스포츠카"""
    img = pygame.Surface((180, 100), pygame.SRCALPHA)
    dark = tuple(int(c * 0.6) for c in color)
    pygame.draw.polygon(img, dark, [(40, 40), (60, 12), (125, 12), (145, 40)])    # 지붕
    pygame.draw.polygon(img, (40, 50, 70), [(50, 38), (65, 17), (120, 17), (135, 38)])  # 유리창
    pygame.draw.rect(img, color, (4, 38, 172, 40), border_radius=10)              # 차체
    pygame.draw.rect(img, dark, (4, 58, 172, 6))                                  # 옆줄
    pygame.draw.rect(img, (255, 250, 200), (6, 44, 18, 8), border_radius=3)       # 전조등
    pygame.draw.rect(img, (255, 60, 60), (156, 44, 18, 8), border_radius=3)       # 후미등
    for x in (38, 142):
        pygame.draw.circle(img, (20, 20, 20), (x, 80), 17)                        # 바퀴
        pygame.draw.circle(img, (160, 160, 170), (x, 80), 7)
    return img


def make_pine_image(snowy=False):
    """침엽수 (설원에서는 눈이 쌓여 있어요)"""
    img = pygame.Surface((100, 220), pygame.SRCALPHA)
    pygame.draw.rect(img, (90, 60, 35), (44, 170, 12, 50))                   # 줄기
    for i, (w, y) in enumerate(((90, 120), (72, 80), (54, 42), (34, 8))):     # 층층이 쌓인 잎
        points = [(50 - w / 2, y + 60), (50 + w / 2, y + 60), (50, y)]
        pygame.draw.polygon(img, (30, 80 + i * 8, 45), points)
        if snowy:
            pygame.draw.polygon(img, (235, 240, 248), [(50 - w / 4, y + 30), (50 + w / 4, y + 30), (50, y)])
    return img


def make_burnt_car_image():
    """불탄 차 (엄폐물)"""
    img = make_car_image((70, 60, 55))
    for x, y, r in ((50, 50, 10), (110, 45, 14), (140, 60, 8)):             # 그을음
        pygame.draw.circle(img, (30, 25, 25), (x, y), r)
    pygame.draw.polygon(img, (25, 25, 30), [(50, 38), (65, 17), (120, 17), (135, 38)])   # 깨진 유리창
    return img


def make_lamp_image():
    """가로등"""
    img = pygame.Surface((40, 220), pygame.SRCALPHA)
    pygame.draw.rect(img, (60, 60, 70), (17, 20, 6, 200))          # 기둥
    pygame.draw.rect(img, (60, 60, 70), (8, 14, 24, 8), border_radius=3)
    pygame.draw.circle(img, (255, 230, 150), (20, 26), 10)        # 불빛
    pygame.draw.circle(img, (255, 250, 220), (20, 26), 5)
    return img


def make_pickup_image(kind):
    """바닥에 놓인 상자: 탄약(초록 상자) / 체력(흰 상자에 빨간 십자) / 수류탄"""
    img = pygame.Surface((60, 44), pygame.SRCALPHA)
    if kind == "ammo":
        pygame.draw.rect(img, (85, 100, 55), (2, 10, 56, 32), border_radius=4)
        pygame.draw.rect(img, (60, 70, 40), (2, 10, 56, 8))
        for x in (14, 24, 34, 44):                                   # 총알 끝
            pygame.draw.rect(img, (230, 190, 70), (x, 2, 6, 12), border_radius=3)
    elif kind == "health":
        pygame.draw.rect(img, (245, 245, 245), (4, 8, 52, 34), border_radius=5)
        pygame.draw.rect(img, (220, 40, 40), (25, 13, 10, 24))
        pygame.draw.rect(img, (220, 40, 40), (18, 20, 24, 10))
    else:  # grenade
        pygame.draw.ellipse(img, (60, 90, 50), (16, 10, 28, 32))
        pygame.draw.rect(img, (120, 120, 120), (25, 4, 10, 8))
        pygame.draw.circle(img, (200, 200, 200), (38, 7), 5, 2)      # 안전핀
    return img


def make_grenade_image():
    img = pygame.Surface((24, 28), pygame.SRCALPHA)
    pygame.draw.ellipse(img, (60, 90, 50), (2, 6, 20, 22))
    pygame.draw.rect(img, (120, 120, 120), (8, 0, 8, 7))
    return img


def make_rocket_image():
    img = pygame.Surface((40, 24), pygame.SRCALPHA)
    pygame.draw.circle(img, (255, 170, 60), (8, 12), 8)            # 불꽃
    pygame.draw.circle(img, (255, 240, 180), (8, 12), 4)
    pygame.draw.rect(img, (90, 100, 70), (10, 7, 24, 10), border_radius=4)
    pygame.draw.polygon(img, (200, 60, 40), [(34, 7), (40, 12), (34, 17)])
    return img


def make_explosion_frames(count=8):
    """폭발 애니메이션: 하얀 불꽃 → 주황 불덩이 → 검은 연기"""
    frames = []
    for i in range(count):
        t = i / (count - 1)
        img = pygame.Surface((120, 120), pygame.SRCALPHA)
        alpha = int(255 * (1 - t * 0.8))
        r = int(25 + 35 * t)
        pygame.draw.circle(img, (90, 80, 80, int(alpha * 0.7)), (60, 60), min(59, r + 12))   # 연기
        pygame.draw.circle(img, (255, 120, 40, alpha), (60, 60), r)                           # 불덩이
        pygame.draw.circle(img, (255, 220, 120, alpha), (60, 60), int(r * (0.6 - 0.4 * t)))
        if t < 0.3:
            pygame.draw.circle(img, (255, 255, 230, alpha), (60, 60), int(r * 0.3))
        frames.append(img)
    return frames


def make_blood_pool_image():
    """바닥의 피 웅덩이 (멀리서 보면 납작하게 깔린 모양)"""
    img = pygame.Surface((120, 24), pygame.SRCALPHA)
    rng = random.Random(9)
    pygame.draw.ellipse(img, (110, 5, 10, 230), (10, 6, 100, 16))
    for _ in range(8):
        x, w = rng.randrange(0, 100), rng.randrange(10, 26)
        pygame.draw.ellipse(img, (130, 8, 12, 220), (x, rng.randrange(4, 12), w, 8))
    return img


def make_objective_image(kind):
    """목표 그림: 인질(주황 죄수복, 눈가리개, 묶인 손), 폭탄(빨간 불이 깜빡이는 상자), 깃발"""
    img = pygame.Surface((60, 120), pygame.SRCALPHA)
    if kind == "HOSTAGE":
        pygame.draw.rect(img, (235, 120, 40), (16, 62, 28, 34), border_radius=6)     # 무릎 꿇은 몸
        pygame.draw.rect(img, (215, 105, 35), (10, 92, 40, 20), border_radius=6)     # 꿇은 다리
        pygame.draw.circle(img, (230, 200, 170), (30, 52), 11)                       # 머리
        pygame.draw.rect(img, BLACK, (19, 48, 22, 5))                                # 눈가리개
        pygame.draw.line(img, (200, 180, 120), (14, 76), (46, 76), 3)                # 밧줄
    elif kind in ("BOMB", "CACHE"):
        pygame.draw.rect(img, (60, 75, 50), (6, 74, 48, 44), border_radius=4)        # 상자
        for x in range(6, 54, 12):                                                   # 노랑/검정 줄무늬
            pygame.draw.polygon(img, (230, 200, 40), [(x, 118), (x + 6, 118), (x + 12, 108), (x + 6, 108)])
        pygame.draw.rect(img, (20, 20, 20), (16, 80, 28, 14))                        # 타이머 화면
        pygame.draw.rect(img, (255, 40, 40), (19, 83, 22, 8))
        pygame.draw.circle(img, (255, 50, 50), (48, 72), 5)                          # 깜빡이는 불
        pygame.draw.lines(img, (220, 40, 40), False, [(10, 74), (14, 64), (20, 72)], 2)   # 전선
    else:
        pygame.draw.line(img, (200, 200, 205), (22, 8), (22, 118), 4)                # 깃대
        pygame.draw.polygon(img, (80, 240, 255), [(24, 10), (56, 18), (24, 30)])      # 깃발
        pygame.draw.ellipse(img, (90, 90, 95), (10, 112, 26, 8))
    return img


def make_screen_splat(seed):
    """화면에 묻는 핏자국 한 덩어리"""
    rng = random.Random(seed)
    size = 90
    img = pygame.Surface((size, size), pygame.SRCALPHA)
    for _ in range(9):
        r = rng.randint(6, 20)
        x, y = rng.randint(r, size - r), rng.randint(r, size - r)
        pygame.draw.circle(img, (120 + rng.randint(0, 40), 0, 8, 230), (x, y), r)
    for _ in range(5):                                   # 흘러내리는 줄기
        x = rng.randint(20, 70)
        pygame.draw.line(img, (110, 0, 8, 220), (x, 45), (x + rng.randint(-3, 3), 45 + rng.randint(15, 40)), 4)
    return img


def make_hurt_vignette(color=(140, 0, 0)):
    """다쳤을 때 화면 가장자리가 붉게 물드는 그림 (가운데는 투명). 검은색이면 제압당했을 때 어두워지는 그림"""
    img = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    steps = 24
    for i in range(steps):
        t = i / steps
        alpha = int(170 * (1 - t) ** 2)
        pad_x, pad_y = int(WIDTH * 0.22 * t), int(HEIGHT * 0.22 * t)
        pygame.draw.rect(img, (*color, alpha), (pad_x, pad_y, WIDTH - 2 * pad_x, HEIGHT - 2 * pad_y),
                         int(WIDTH * 0.22 / steps) + 2, border_radius=int(60 * UI))
    return img


def make_sentry_image(flash=False):
    """자동 포탑: 세 발 받침대 위의 총"""
    img = pygame.Surface((80, 90), pygame.SRCALPHA)
    for end in ((10, 89), (40, 89), (70, 89)):                  # 받침대
        pygame.draw.line(img, (70, 75, 80), (40, 50), end, 4)
    pygame.draw.rect(img, (90, 100, 95), (18, 26, 44, 28), border_radius=5)   # 몸통
    pygame.draw.rect(img, (40, 40, 45), (40, 34, 40, 8))         # 총열
    pygame.draw.circle(img, (255, 50, 50), (26, 32), 4)          # 빨간 불빛
    if flash:
        pygame.draw.circle(img, YELLOW, (76, 38), 9)
    return img


def make_flare_frames(count=6):
    """공습 목표 표시: 빨간 연막"""
    frames = []
    for i in range(count):
        img = pygame.Surface((80, 80), pygame.SRCALPHA)
        r = 14 + i * 4
        pygame.draw.circle(img, (255, 60, 60, 120), (40, 40), min(39, r + 8))
        pygame.draw.circle(img, (255, 120, 120, 200), (40, 40), r // 2)
        frames.append(img)
    return frames


def make_crane_image():
    """부두의 노란 크레인 (격자 기둥 + 위로 뻗은 팔)"""
    img = pygame.Surface((160, 300), pygame.SRCALPHA)
    yellow, dark = (235, 190, 40), (150, 120, 30)
    for x in (40, 80):                                             # 기둥 두 개
        pygame.draw.rect(img, yellow, (x, 60, 10, 240))
    for y in range(70, 300, 30):                                   # 격자
        pygame.draw.line(img, dark, (45, y), (85, y + 30), 3)
        pygame.draw.line(img, dark, (85, y), (45, y + 30), 3)
    pygame.draw.rect(img, yellow, (0, 50, 160, 14))                # 팔
    pygame.draw.rect(img, (60, 70, 90), (70, 64, 30, 26))          # 운전실
    pygame.draw.line(img, dark, (140, 64), (140, 150), 2)          # 매달린 줄
    pygame.draw.rect(img, dark, (130, 150, 20, 10))
    return img


def make_billboard_image():
    """기둥 위의 네온 광고판"""
    img = pygame.Surface((160, 220), pygame.SRCALPHA)
    pygame.draw.rect(img, (60, 60, 70), (74, 90, 12, 130))         # 기둥
    pygame.draw.rect(img, (30, 20, 50), (0, 0, 160, 96), border_radius=6)
    pygame.draw.rect(img, (255, 80, 200), (0, 0, 160, 96), 6, border_radius=6)   # 분홍 네온 테두리
    pygame.draw.circle(img, (255, 220, 90), (36, 48), 22)          # 노을 해
    for i, y in enumerate((38, 52, 66)):                           # 글자처럼 보이는 하늘색 줄
        pygame.draw.rect(img, (80, 240, 255), (70, y, 70 - i * 15, 7), border_radius=3)
    return img


def make_sky(theme):
    """하늘. 아래쪽 끝이 지평선에 오도록 그려요. 밤이면 별도 뿌려요."""
    h = int(HEIGHT + MAX_PITCH * 2 + 200)
    sky = pygame.Surface((WIDTH, h))
    stops = theme["sky"]
    for y in range(h):
        t = y / (h - 1)
        for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
            if t0 <= t <= t1:
                k = (t - t0) / (t1 - t0)
                color = tuple(int(a + (b - a) * k) for a, b in zip(c0, c1))
                pygame.draw.line(sky, color, (0, y), (WIDTH, y))
                break
    if theme["stars"]:
        rng = random.Random(7)                 # 별 위치는 매번 똑같이
        for _ in range(int(160 * UI)):
            x, y = rng.randrange(WIDTH), rng.randrange(int(h * 0.7))
            sky.set_at((x, y), (255, 255, 230) if rng.random() < 0.7 else (180, 200, 255))
    return sky


# ---------------------------------------------------------------
# 소리 (소리 파일 없이 코드로 만들어요)
# ---------------------------------------------------------------
# 이름 -> (길이초, 줄어드는 빠르기, 지직 소리 양, 소리 부드러움 0~1, 쿵 소리 높이, 쿵 크기, 삐 소리 높이, 삐 크기, 음량)
#   지직 소리(잡음)는 총소리·폭발, 쿵 소리는 묵직한 울림, 삐 소리는 맞힘/알림
SOUND_RECIPES = {
    "rifle":     (0.18, 28, 1.0, 0.50, 90, 0.5, 0, 0, 0.55),
    "pistol":    (0.14, 32, 1.0, 0.60, 140, 0.4, 0, 0, 0.50),
    "sniper":    (0.45, 9, 1.0, 0.35, 60, 0.8, 0, 0, 0.80),
    "shotgun":   (0.35, 12, 1.0, 0.30, 70, 0.9, 0, 0, 0.80),
    "smg":       (0.10, 45, 1.0, 0.65, 160, 0.3, 0, 0, 0.45),
    "lmg":       (0.16, 26, 1.0, 0.45, 80, 0.6, 0, 0, 0.55),
    "dmr":       (0.25, 16, 1.0, 0.45, 100, 0.6, 0, 0, 0.65),
    "rocket":    (0.60, 4, 1.0, 0.15, 0, 0, 0, 0, 0.50),
    "explosion": (1.00, 3.5, 1.0, 0.08, 45, 1.0, 0, 0, 0.90),
    "enemy":     (0.12, 35, 1.0, 0.35, 0, 0, 0, 0, 0.30),
    "hit":       (0.08, 45, 0.6, 0.30, 120, 0.4, 1800, 0.45, 0.55),
    "headshot":  (0.12, 25, 0.0, 0.0, 0, 0, 2600, 0.7, 0.55),
    "kill":      (0.16, 22, 0.7, 0.40, 90, 0.6, 1200, 0.45, 0.60),
    "heart":     (0.25, 12, 0.0, 0.0, 50, 1.0, 0, 0, 0.55),
    # 발소리: 바닥마다 달라요
    "step_hard": (0.06, 70, 0.8, 0.55, 140, 0.35, 0, 0, 0.35),
    "step_soft": (0.09, 45, 0.9, 0.85, 90, 0.30, 0, 0, 0.30),
    "step_snow": (0.12, 35, 1.0, 0.35, 0, 0, 0, 0, 0.26),
    "step_wood": (0.07, 55, 0.6, 0.60, 180, 0.50, 0, 0, 0.35),
    # 적 군화 소리: 내 발소리보다 낮고 묵직하고, 장비가 '찰칵' 부딪혀요
    "boot_hard": (0.11, 38, 0.7, 0.75, 72, 0.75, 2900, 0.07, 0.50),
    "boot_soft": (0.14, 28, 0.8, 0.90, 58, 0.65, 2900, 0.05, 0.45),
    "boot_snow": (0.17, 24, 1.0, 0.60, 52, 0.45, 0, 0, 0.40),
    "boot_wood": (0.12, 33, 0.6, 0.70, 105, 0.85, 2900, 0.06, 0.50),
    # 좀비: 질질 끄는 발소리, 그르렁, 할퀴기
    "zstep":     (0.22, 16, 0.9, 0.93, 48, 0.35, 0, 0, 0.40),
    "groan":     (0.80, 3.5, 0.35, 0.95, 82, 0.6, 130, 0.25, 0.50),
    "swipe":     (0.16, 16, 1.0, 0.55, 0, 0, 0, 0, 0.40),
    "cash":      (0.25, 10, 0.0, 0.0, 0, 0, 1500, 0.5, 0.45),
    "reload":    (0.05, 80, 1.0, 0.90, 0, 0, 2000, 0.3, 0.40),
    "heavyar":   (0.22, 20, 1.0, 0.40, 70, 0.8, 0, 0, 0.65),
    "revolver":  (0.32, 13, 1.0, 0.40, 72, 0.9, 0, 0, 0.75),
    "mpistol":   (0.09, 50, 1.0, 0.70, 170, 0.25, 0, 0, 0.42),
    "gl":        (0.22, 18, 0.7, 0.75, 65, 0.9, 0, 0, 0.60),
    # 타격감: 총알이 귀 옆을 스치는 소리, 장갑에 맞는 '깡', 침 뱉기, 치료
    "whiz":      (0.10, 28, 1.0, 0.05, 0, 0, 0, 0, 0.35),
    "armor":     (0.14, 26, 0.2, 0.30, 0, 0, 3400, 0.6, 0.45),
    "spit":      (0.30, 12, 0.8, 0.90, 0, 0, 300, 0.3, 0.45),
    "heal":      (0.30, 8, 0.0, 0.0, 0, 0, 1000, 0.3, 0.30),
    # 총소리 뒤에 남는 울림, 바닥에 떨어지는 탄피, 재장전 동작 소리
    "tail":      (0.70, 5, 0.6, 0.95, 40, 0.3, 0, 0, 0.35),
    "beep":      (0.08, 30, 0.0, 0.0, 0, 0, 2000, 0.6, 0.40),
    "thunder":   (1.80, 1.8, 1.0, 0.97, 32, 0.7, 0, 0, 0.80),
    "casing":    (0.08, 40, 0.0, 0.0, 0, 0, 4200, 0.5, 0.25),
    "magout":    (0.08, 60, 0.8, 0.60, 0, 0, 1200, 0.3, 0.40),
    "magin":     (0.07, 70, 0.9, 0.50, 200, 0.4, 2400, 0.3, 0.45),
    "bolt":      (0.12, 40, 0.9, 0.40, 150, 0.5, 1800, 0.4, 0.50),
    "streak":    (0.30, 6, 0.0, 0.0, 0, 0, 880, 0.6, 0.50),
    "knife":     (0.20, 12, 1.0, 0.70, 0, 0, 0, 0, 0.30),
    "throw":     (0.15, 15, 1.0, 0.60, 0, 0, 0, 0, 0.25),
    "hurt":      (0.12, 20, 0.6, 0.20, 0, 0, 220, 0.5, 0.40),
    # 총소리 겹치기: 쏠 때마다 "탕" 위에 노리쇠의 "착" + 가슴을 치는 낮은 "쿵"
    "mech":      (0.05, 80, 0.7, 0.10, 0, 0, 2600, 0.5, 0.30),
    "radio":     (0.14, 18, 0.7, 0.30, 0, 0, 1500, 0.35, 0.22),    # 적 무전 "치직"
    "glass":     (0.35, 9, 0.7, 0.05, 0, 0, 3400, 0.45, 0.40),      # 유리 깨지는 "쨍그랑"
    "smash":     (0.30, 11, 1.0, 0.55, 85, 0.7, 0, 0, 0.60),        # 상자/모래주머니가 부서지는 "와장창"
    "punch":     (0.16, 26, 0.0, 0.0, 52, 1.0, 0, 0, 0.55),
}
# 벽 너머에서 나는 소리는 먹먹하게 (높은 소리를 깎은 "_m" 소리를 따로 만들어요)
# 화면에 방향을 표시할 소리 (설정 SOUND MARKS)
SOUND_MARK_KINDS = {"enemy": "shot", "spit": "shot", "explosion": "shot", "boot_hard": "step", "boot_soft": "step",
                    "boot_snow": "step", "boot_wood": "step", "zstep": "step", "groan": "step"}
MUFFLED_SOUNDS = ("enemy", "spit", "explosion", "boot_hard", "boot_soft", "boot_snow", "boot_wood", "zstep", "groan")
# 바닥 -> 발소리 (없는 바닥은 step_hard)
STEP_SOUNDS = {".": "step_soft", ";": "step_soft", "g": "step_soft", "#": "step_soft",
               "*": "step_snow", "-": "step_snow", "_": "step_wood", "p": "step_wood"}


# 내 발소리 -> 같은 바닥에서 적이 내는 군화 소리
ENEMY_STEPS = {"step_hard": "boot_hard", "step_soft": "boot_soft", "step_snow": "boot_snow", "step_wood": "boot_wood"}


def step_sound_at(pos):
    col, row = int(pos.x), int(pos.y)
    floor = FLOOR_GRID[row][col] if in_map(col, row) else ":"
    return STEP_SOUNDS.get(floor, "step_hard")


# 총 이름 -> 총소리
GUN_SOUNDS = {"RIFLE": "rifle", "PISTOL": "pistol", "SNIPER": "sniper", "SHOTGUN": "shotgun", "SMG": "smg",
              "ROCKET": "rocket", "LMG": "lmg", "BURST": "rifle", "DMR": "dmr", "HEAVY AR": "heavyar",
              "AUTO SHOTGUN": "shotgun", "REVOLVER": "revolver", "MACHINE PISTOL": "mpistol", "LAUNCHER": "gl"}


class Sounds:
    """효과음. 소리를 낼 수 없는 환경이면 조용히 아무것도 안 해요. M 키로 끄고 켜요."""

    def __init__(self):
        self.bank = {}
        self.muted = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            freq, size, channels = pygame.mixer.get_init()
            if size != -16:
                return                       # 16비트 소리만 만들 줄 알아요
            pygame.mixer.set_num_channels(24)
            pygame.mixer.set_reserved(2)         # 0번: 배경 소리, 1번: 음악 (효과음이 빼앗지 않게)
            rng = random.Random(1)
            for name, recipe in SOUND_RECIPES.items():
                self.bank[name] = self.synth(freq, channels, rng, *recipe)
            for name in MUFFLED_SOUNDS:
                length, decay, noise, smooth, thump_hz, thump, tone_hz, tone, volume = SOUND_RECIPES[name]
                self.bank[name + "_m"] = self.synth(freq, channels, rng, length * 1.2, decay * 0.8, noise * 1.8,
                                                    max(smooth, 0.97), thump_hz, thump * 1.3, tone_hz, tone * 0.1,
                                                    volume * 0.8)
            self.format = (freq, channels)
        except Exception:
            self.bank = {}
        self.loops = {}            # 배경 소리 (한 번 만들면 계속 써요)
        self.background = None     # 지금 나오는 배경 소리 이름
        self.music_on = False

    def make_loop(self, kind):
        """끊김 없이 반복되는 배경 소리. wind 바람 / rain 빗소리 / night 밤벌레 / music 낮게 깔리는 음악"""
        freq, channels = self.format
        rng = random.Random(7)
        seconds = 8.0 if kind == "music" else 3.0
        step = 4 if kind in ("wind", "music") else 1      # 낮은 소리는 4칸마다 한 번만 계산 (빠르게)
        n = int(seconds * freq) // step
        fade = n // 8
        rate = freq / step
        values = []
        low = mid = 0.0
        notes = (55.0, 43.65, 65.41, 49.0)                 # 라-파-도-솔 (낮은 음, 2초씩)
        for i in range(n + fade):
            t = i / rate
            if kind == "wind":
                low += 0.01 * (rng.uniform(-1, 1) - low)
                v = low * 5 * (0.65 + 0.35 * math.sin(2 * math.pi * t / seconds))
            elif kind == "rain":
                mid += 0.5 * (rng.uniform(-1, 1) - mid)
                v = mid * 0.45 + (rng.uniform(-1, 1) * 0.6 if rng.random() < 0.002 else 0)
            elif kind == "night":
                low += 0.01 * (rng.uniform(-1, 1) - low)
                chirp = (t * 6) % 1 < 0.06 and int(t * 6) % 5 in (0, 1)
                v = low * 3 + (0.18 * math.sin(2 * math.pi * 4300 * t) if chirp else 0)
            else:   # music
                beat = (t % seconds) % 2.0
                note = notes[int((t % seconds) / 2.0)]
                pad = math.sin(2 * math.pi * note * t) + 0.4 * math.sin(2 * math.pi * note * 1.5 * t)
                v = 0.32 * pad * min(1.0, beat * 4) * (1 - beat / 2.6)
                pulse = (t % 0.5)
                v += 0.45 * math.sin(2 * math.pi * 48 * pulse) * math.exp(-pulse * 18)   # 둥 둥 (심장 박동)
            values.append(v)
        for i in range(fade):                              # 끝을 처음에 겹쳐서 이음새가 안 들리게
            w = i / fade
            values[i] = values[i] * w + values[n + i] * (1 - w)
        samples = array.array("h")
        for v in values[:n]:
            samples.extend([int(max(-1.0, min(1.0, v)) * 32767)] * (channels * step))
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def start_background(self, kind, music=False):
        """맵에 맞는 배경 소리 (+ 음악)를 계속 반복해요"""
        if not self.bank:
            return
        self.music_on = music and not IN_BROWSER     # 웹에서는 음악을 만드는 데 오래 걸려서 빼요
        for name, channel_no, on in ((kind, 0, True), ("music", 1, self.music_on)):
            channel = pygame.mixer.Channel(channel_no)
            if not on:
                channel.stop()
                continue
            if name not in self.loops:
                self.loops[name] = self.make_loop(name)
            if channel_no == 1 or self.background != kind or not channel.get_busy():
                if not (channel_no == 1 and channel.get_busy()):
                    channel.play(self.loops[name], loops=-1)
        self.background = kind
        self.refresh_background()

    def refresh_background(self):
        """소리 끄기(M)나 설정의 소리 크기를 배경 소리에도 반영해요"""
        if not self.bank:
            return
        volume = 0.0 if self.muted else SETTINGS["volume"] / 100
        pygame.mixer.Channel(0).set_volume(0.35 * volume)
        pygame.mixer.Channel(1).set_volume(0.5 * volume * SETTINGS.get("music", 40) / 100 if self.music_on else 0)

    def stop_background(self):
        if self.bank:
            pygame.mixer.Channel(0).stop()
            pygame.mixer.Channel(1).stop()
        self.background = None

    @staticmethod
    def synth(freq, channels, rng, duration, decay, noise, smooth, thump_hz, thump, tone_hz, tone, volume):
        samples = array.array("h")
        prev = 0.0
        alpha = 1 - smooth                   # 부드러울수록 잡음의 높은 소리를 깎아요
        for i in range(int(duration * freq)):
            t = i / freq
            env = math.exp(-t * decay)       # 점점 작아지는 소리
            prev += alpha * (rng.uniform(-1, 1) - prev)
            v = noise * prev * env
            if thump:
                v += thump * math.sin(2 * math.pi * thump_hz * t) * math.exp(-t * decay * 0.7)
            if tone:
                v += tone * math.sin(2 * math.pi * tone_hz * (1 + t * 2) * t) * env
            value = int(max(-1.0, min(1.0, v * volume)) * 32767)
            samples.extend([value] * channels)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name, volume=1.0, pan=0.0):
        """pan: -1이면 왼쪽, 1이면 오른쪽에서 들려요 (이어폰을 끼면 방향을 알 수 있어요)"""
        sound = self.bank.get(name)
        volume *= SETTINGS["volume"] / 100
        if sound and not self.muted and volume > 0.02:
            channel = sound.play()
            if channel:
                v = min(1.0, volume)
                channel.set_volume(v * min(1.0, 1 - pan * 0.85), v * min(1.0, 1 + pan * 0.85))


_sounds = None


def get_sounds():
    """효과음은 한 번만 만들어서 계속 써요"""
    global _sounds
    if _sounds is None:
        _sounds = Sounds()
    return _sounds


# ---------------------------------------------------------------
# 글자 / 도움말
# ---------------------------------------------------------------
# 한글 글꼴 후보 (맥 / 윈도우 / 리눅스). 없으면 영어로 보여줘요
KOREAN_FONTS = ["applesdgothicneo", "applegothic", "malgungothic", "nanumgothic",
                "notosanscjkkr", "notosanskr", "notosanscjk"]

HELP_TEXT = {
    "ko": dict(
        title="조작법",
        keys=[("W A S D", "이동"), ("Shift", "달리기 (W와 함께)"), ("C", "앉기 / 달리다가: 슬라이딩"),
              ("← → ↑ ↓", "시점 (마우스도 돼요)"), ("스페이스바", "점프"),
              ("F,  왼쪽 클릭", "사격 (꾹 누르면 연사)"), ("E,  오른쪽 클릭", "정조준 / 저격총 조준경"), ("Z", "조준경 배율 3·6·12배"),
              ("G", "수류탄"), ("V", "칼"), ("X", "킬스트릭 쓰기"), ("1~9, 0, Tab, Q", "무기 바꾸기 (가진 무기 전부)"), ("T,  Y,  J", "스킬: 집중 / 구급상자 / 탐지"),
              ("R,  B,  U", "재장전,  좀비 상점 (탄약 / 강화)"), ("H,  M", "도움말 (일시정지),  소리 끄기"), ("P,  Enter", "FPS 표시,  전체 화면"),
              ("ESC", "일시정지 (계속 / 설정 / 나가기)")],
        tips=["적을 모두 쓰러뜨리면 다음 라운드! 라운드마다 맵이 바뀌어요.",
              "죽지 않고 연속으로 쓰러뜨리면 킬스트릭: 3킬 레이더, 5킬 공습, 7킬 자동 포탑 (X).",
              "앉으면 덜 맞고 잘 맞혀요. 차·상자 뒤에 숨으면 총알을 막아요.",
              "GRENADE! 경고가 뜨면 빨리 피하세요. 방패병은 머리나 옆을 노리세요.",
              "라운드가 오를수록 적이 더 정확하고 빨라져요. 5라운드마다 보스!",
              "적 군화 소리는 묵직하게, 소리 난 방향에서 들려요. 달리거나 쏘면 적도 내 소리를 듣고 와요.",
              "좀비 모드: 웨이브를 버티며 점수를 모아 B 탄약, U 총 강화.",
              "죽으면 R: 다시,  N: 처음부터"],
        resume="H 를 누르면 계속해요",
    ),
    "en": dict(
        title="HOW TO PLAY",
        keys=[("W A S D", "move"), ("SHIFT", "sprint (with W)"), ("C", "crouch / slide while sprinting"),
              ("ARROWS", "look (or mouse)"), ("SPACE", "jump"),
              ("F, LEFT CLICK", "fire (hold for auto)"), ("E, RIGHT CLICK", "aim / sniper scope"), ("Z", "scope zoom 3/6/12x"),
              ("G", "grenade"), ("V", "knife"), ("X", "use killstreak"), ("1-9, 0, TAB, Q", "switch weapon (whole inventory)"), ("T, Y, J", "skills: focus / medkit / scan"),
              ("R, B, U", "reload, zombie shop"), ("H, M", "help (pause), mute"), ("P, ENTER", "show FPS, fullscreen"), ("ESC", "pause menu")],
        tips=["Kill every enemy to clear the round. The map changes each round.",
              "Killstreaks without dying: 3 radar, 5 airstrike, 7 sentry turret (X).",
              "Crouch to be harder to hit. Cars and crates stop bullets.",
              "GRENADE! warning: move away. Shield guys: aim for the head or flank.",
              "Enemies get sharper every round. A boss every 5 rounds.",
              "Enemy boots sound heavy and come from their direction. Sprinting or shooting gives you away.",
              "Zombies: survive waves, spend points on B ammo and U weapon upgrades.",
              "When you die: R retry, N new game."],
        resume="Press H to resume",
    ),
}


class ShadowFont:
    """글자 뒤에 검은 그림자를 넣어서 밝은 배경(눈, 하늘) 위에서도 잘 보이게 해요.
    같은 글자는 한 번 만든 그림을 다시 써서 빨라요."""

    def __init__(self, font):
        self.font = font
        self.cache = {}

    def render(self, text, antialias, color):
        key = (text, color)
        if key not in self.cache:
            if len(self.cache) > 400:          # 너무 많이 쌓이면 비워요
                self.cache.clear()
            base = self.font.render(text, antialias, color)
            shadow = self.font.render(text, antialias, (0, 0, 0))
            out = pygame.Surface((base.get_width() + 2, base.get_height() + 2), pygame.SRCALPHA)
            out.blit(shadow, (2, 2))
            out.blit(base, (0, 0))
            self.cache[key] = out
        return self.cache[key]

    def size(self, text):
        return self.font.size(text)

    def get_linesize(self):
        return self.font.get_linesize()


def make_fonts():
    """화면 크기에 맞춘 글꼴들. 한글 글꼴이 있으면 도움말을 한글로 보여줘요."""
    ko_path = None if IN_BROWSER else pygame.font.match_font(KOREAN_FONTS)
    fonts = {
        "tiny": pygame.font.Font(None, int(18 * UI)),
        "small": pygame.font.Font(None, int(22 * UI)),
        "normal": pygame.font.Font(None, int(30 * UI)),
        "big": pygame.font.Font(None, int(56 * UI)),
        "title": pygame.font.Font(None, int(100 * UI)),
        "lang": "ko" if ko_path else "en",
    }
    if ko_path:
        fonts["help"] = pygame.font.Font(ko_path, int(17 * UI))
        fonts["help_big"] = pygame.font.Font(ko_path, int(26 * UI))
    else:
        fonts["help"] = pygame.font.Font(None, int(24 * UI))
        fonts["help_big"] = pygame.font.Font(None, int(38 * UI))
    return {key: ShadowFont(f) if key != "lang" else f for key, f in fonts.items()}


def wrap_text(font, text, max_width):
    """글자가 max_width보다 길면 띄어쓰기 기준으로 여러 줄로 나눠요."""
    lines, line = [], ""
    for word in text.split(" "):
        test = (line + " " + word).strip()
        if line and font.size(test)[0] > max_width:
            lines.append(line)
            line = word
        else:
            line = test
    return lines + [line]


def draw_help(screen, fonts, footer):
    """조작법과 팁을 보여주는 판. footer: 맨 아래에 보여줄 안내 문구"""
    text = HELP_TEXT[fonts["lang"]]
    panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    panel.fill((10, 8, 25, 215))
    screen.blit(panel, (0, 0))
    big, small = fonts["help_big"], fonts["help"]
    title = big.render(text["title"], True, (255, 80, 200))
    screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.25)))

    line_h = small.get_linesize() * 1.15
    top = HEIGHT * 0.32
    left = WIDTH * 0.12
    for i, (key, desc) in enumerate(text["keys"]):
        y = top + i * line_h
        screen.blit(small.render(key, True, YELLOW), (left, y))
        screen.blit(small.render(desc, True, WHITE), (left + WIDTH * 0.13, y))
    tip_left = WIDTH * 0.52
    y = top
    for tip in text["tips"]:
        for j, line in enumerate(wrap_text(small, tip, WIDTH * 0.42)):
            screen.blit(small.render(("-  " if j == 0 else "   ") + line, True, (200, 230, 255)), (tip_left, y))
            y += line_h
        y += line_h * 0.25

    image = small.render(footer, True, YELLOW)
    screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.94)))


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
# 1인칭 총 화면: 위장복 소매와 장갑 낀 두 손이 총을 잡은 모습
# ---------------------------------------------------------------
SLEEVE = (78, 88, 64)            # 위장복 소매
SLEEVE_DARK = (55, 63, 45)
GLOVE = (40, 38, 36)             # 장갑
GLOVE_LIGHT = (70, 66, 60)
GUN_DARK = (28, 29, 32)

# 총 생김새
#   body / accent : 몸통 색 / 총열덮개·개머리판 색      length : 총 길이 비율    thick : 굵기 비율
#   mag    : 탄창 모양 (curved 휜 탄창, straight 곧은 탄창, box 짧은 탄창, drum 드럼, tube 산탄총, grip 권총)
#   optic  : 조준기 (reddot 도트사이트, scope 저격 조준경, scope_small 작은 조준경, iron 가늠쇠)
#   tube   : 로켓처럼 굵은 통 모양인지
GUN_LOOKS = {
    "RIFLE":   dict(body=(48, 50, 54), accent=(70, 72, 76), length=1.0, thick=1.0, mag="curved", optic="reddot"),
    "PISTOL":  dict(body=(42, 42, 46), accent=(80, 80, 86), length=0.5, thick=0.9, mag="grip", optic="iron"),
    "SNIPER":  dict(body=(62, 68, 52), accent=(45, 48, 40), length=1.25, thick=0.95, mag="box", optic="scope"),
    "SHOTGUN": dict(body=(40, 40, 44), accent=(125, 82, 45), length=1.05, thick=1.1, mag="tube", optic="iron"),
    "SMG":     dict(body=(40, 40, 44), accent=(66, 66, 72), length=0.75, thick=0.95, mag="straight", optic="reddot"),
    "ROCKET":  dict(body=(88, 98, 66), accent=(62, 68, 46), length=1.1, thick=1.9, mag=None, optic="iron", tube=True),
    "LMG":     dict(body=(52, 54, 50), accent=(78, 80, 72), length=1.15, thick=1.25, mag="drum", optic="reddot"),
    "BURST":   dict(body=(165, 145, 105), accent=(62, 62, 62), length=1.0, thick=1.0, mag="curved", optic="reddot"),
    "DMR":     dict(body=(72, 60, 46), accent=(42, 42, 42), length=1.15, thick=0.95, mag="straight", optic="scope_small"),
    "HEAVY AR": dict(body=(70, 58, 42), accent=(44, 40, 34), length=1.05, thick=1.1, mag="curved", optic="iron"),
    "AUTO SHOTGUN": dict(body=(36, 36, 40), accent=(58, 58, 64), length=0.95, thick=1.15, mag="drum", optic="reddot"),
    "REVOLVER": dict(body=(150, 150, 158), accent=(95, 62, 40), length=0.55, thick=0.95, mag="grip", optic="iron"),
    "MACHINE PISTOL": dict(body=(40, 40, 44), accent=(72, 72, 78), length=0.6, thick=0.9, mag="straight", optic="iron"),
    "LAUNCHER": dict(body=(72, 82, 56), accent=(50, 56, 40), length=0.8, thick=1.6, mag=None, optic="iron", tube=True),
}


def lighter(color, amount):
    return tuple(max(0, min(255, int(c * amount))) for c in color)


def draw_sleeve(surface, hand, elbow, width):
    """손에서 화면 밖 팔꿈치까지 이어지는 위장복 소매"""
    along = elbow - hand
    if along.length() == 0:
        return
    side = pygame.Vector2(-along.y, along.x).normalize() * width / 2
    pygame.draw.polygon(surface, SLEEVE, [hand + side, elbow + side * 1.3, elbow - side * 1.3, hand - side])
    pygame.draw.polygon(surface, SLEEVE_DARK, [hand - side * 0.2, elbow - side * 0.3, elbow - side * 1.3, hand - side])
    rng = random.Random(int(hand.x))
    for _ in range(6):                                   # 위장 무늬
        p = hand.lerp(elbow, rng.uniform(0.15, 0.9)) + side * rng.uniform(-0.6, 0.6)
        pygame.draw.circle(surface, SLEEVE_DARK, p, width * rng.uniform(0.12, 0.25))
    pygame.draw.circle(surface, SLEEVE_DARK, hand, width * 0.55)          # 소매 끝


def draw_glove(surface, center, radius):
    pygame.draw.circle(surface, GLOVE, center, radius)
    pygame.draw.circle(surface, GLOVE_LIGHT, center - pygame.Vector2(radius * 0.3, radius * 0.35), radius * 0.35)


def draw_hip_gun(surface, look):
    """허리 높이로 든 총 (오른쪽 아래에서 화면 가운데를 향해요). 총구 위치를 돌려줘요."""
    V = pygame.Vector2
    rear = V(WIDTH * 0.84, HEIGHT * 1.0)
    aim = V(WIDTH * 0.58, HEIGHT * 0.64)
    axis = (aim - rear) * min(1.15, 0.7 + 0.3 * look["length"])
    u = axis.normalize()
    n = V(-u.y, u.x)
    if n.y > 0:
        n = -n                                           # n: 총의 '위쪽' 방향
    base = 56 * UI * look["thick"]

    def w(t):                                            # 멀수록 가늘게 (원근감)
        return base * (1 - 0.5 * t)

    def P(t, h):                                         # 총 위의 한 점: t 앞뒤(0~1), h 위아래(-1~1)
        return rear + axis * t + n * h * w(t)

    def band(color, t0, t1, h0, h1):
        pygame.draw.polygon(surface, color, [P(t0, h0), P(t1, h0), P(t1, h1), P(t0, h1)])

    body, accent = look["body"], look["accent"]
    down = -n
    left_hand, right_hand = P(0.62, -1.05), P(0.17, -1.75)
    draw_sleeve(surface, left_hand, V(WIDTH * 0.42, HEIGHT * 1.25), 62 * UI)
    draw_sleeve(surface, right_hand, V(WIDTH * 1.08, HEIGHT * 1.2), 80 * UI)

    if look.get("tube"):                                 # 로켓 발사관
        band(lighter(body, 0.6), -0.15, 1.0, -1.15, -0.85)
        band(body, -0.15, 1.0, -0.9, 0.9)
        band(lighter(body, 1.35), -0.15, 1.0, 0.5, 0.95)
        band(accent, 0.86, 1.0, -1.08, 1.08)
        band(accent, -0.15, -0.02, -1.05, 1.05)
        band(GUN_DARK, 0.32, 0.38, 0.9, 1.6)             # 가늠쇠
        band(GUN_DARK, 0.15, 0.22, -0.9, -2.2)           # 손잡이
        draw_glove(surface, P(0.19, -2.0), w(0.19) * 0.9)
        draw_glove(surface, left_hand, w(0.62) * 0.85)
        return P(1.0, 0)

    # 개머리판
    stock = accent if look["mag"] == "tube" else lighter(body, 0.85)
    if look["mag"] != "grip":
        band(stock, -0.08, 0.12, -0.85, 0.65)
    # 손잡이 (오른손)
    grip = [P(0.12, -0.95), P(0.2, -0.95), P(0.2, -0.95) + down * w(0.2) * 1.8 - u * w(0.2) * 0.2,
            P(0.12, -0.95) + down * w(0.12) * 1.8 - u * w(0.12) * 0.5]
    pygame.draw.polygon(surface, GUN_DARK, grip)
    # 탄창
    mag = look["mag"]
    a, b = P(0.30, -0.95), P(0.40, -0.95)
    if mag == "curved":
        pygame.draw.polygon(surface, GUN_DARK, [a, b, b + down * w(0.4) * 2.4 + u * w(0.4) * 0.9,
                                                a + down * w(0.3) * 2.3 + u * w(0.3) * 0.5])
    elif mag in ("straight", "box"):
        depth = 2.3 if mag == "straight" else 1.3
        pygame.draw.polygon(surface, GUN_DARK, [a, b, b + down * w(0.4) * depth, a + down * w(0.3) * depth])
    elif mag == "drum":
        center = P(0.36, -0.95) + down * w(0.36) * 1.3
        pygame.draw.circle(surface, GUN_DARK, center, w(0.36) * 1.3)
        pygame.draw.circle(surface, lighter(GUN_DARK, 1.8), center, w(0.36) * 0.5)
    # 몸통
    band(lighter(body, 0.6), 0.1, 0.46, -1.15, -0.85)    # 아래 그림자
    band(body, 0.1, 0.46, -0.95, 0.95)
    band(lighter(body, 1.45), 0.1, 0.46, 0.7, 1.0)       # 위쪽 빛 반사
    # 총열덮개 + 레일 홈 (산탄총은 나무 펌프)
    band(accent, 0.46, 0.78, -0.75, 0.75)
    band(lighter(accent, 1.35), 0.46, 0.78, 0.5, 0.75)
    for k in range(6):
        t = 0.49 + k * 0.05
        pygame.draw.line(surface, lighter(accent, 0.55), P(t, 0.72), P(t, -0.35), max(1, int(2 * UI)))
    # 총열과 소염기
    band(GUN_DARK, 0.78, 1.0, -0.28, 0.28)
    band(lighter(GUN_DARK, 1.4), 0.94, 1.0, -0.4, 0.4)
    if mag == "tube":
        band(lighter(GUN_DARK, 1.2), 0.5, 0.95, -0.7, -0.35)   # 산탄총 아래 튜브
    # 조준기
    optic = look["optic"]
    if optic == "reddot":
        band(GUN_DARK, 0.22, 0.33, 1.0, 2.1)
        pygame.draw.line(surface, (120, 175, 215), P(0.33, 1.2), P(0.33, 1.9), max(2, int(3 * UI)))
    elif optic == "scope":
        band(GUN_DARK, 0.08, 0.15, 1.0, 2.35)
        band(GUN_DARK, 0.12, 0.5, 1.2, 2.1)
        band(GUN_DARK, 0.46, 0.55, 1.0, 2.45)
        pygame.draw.line(surface, (120, 175, 215), P(0.55, 1.15), P(0.55, 2.3), max(2, int(3 * UI)))
    elif optic == "scope_small":
        band(GUN_DARK, 0.18, 0.42, 1.15, 1.95)
        pygame.draw.line(surface, (120, 175, 215), P(0.42, 1.25), P(0.42, 1.85), max(2, int(3 * UI)))
    else:
        band(GUN_DARK, 0.14, 0.18, 1.0, 1.55)           # 가늠자
        band(GUN_DARK, 0.88, 0.91, 0.25, 1.0)           # 가늠쇠
    # 장갑 낀 손: 오른손은 손잡이, 왼손은 총열덮개를 감싸요
    draw_glove(surface, P(0.17, -1.75), w(0.17) * 0.95)
    draw_glove(surface, left_hand, w(0.62) * 0.85)
    band(GLOVE, 0.58, 0.67, 0.25, 0.8)                   # 총열덮개 위로 감싼 손가락
    return P(1.0, 0)


def draw_ads_gun(surface, look):
    """정조준: 총을 눈앞에 들고 조준기로 화면 가운데를 봐요. 총구 위치를 돌려줘요."""
    V = pygame.Vector2
    cx, cy = WIDTH / 2, HEIGHT / 2
    body, accent = look["body"], look["accent"]
    draw_sleeve(surface, V(cx - WIDTH * 0.08, HEIGHT * 0.87), V(WIDTH * 0.28, HEIGHT * 1.15), 38 * UI)
    draw_sleeve(surface, V(cx + WIDTH * 0.08, HEIGHT * 0.95), V(WIDTH * 0.75, HEIGHT * 1.15), 46 * UI)
    if look.get("tube"):
        pygame.draw.polygon(surface, body, [(cx - WIDTH * 0.2, HEIGHT), (cx - WIDTH * 0.02, HEIGHT),
                                            (cx - WIDTH * 0.05, cy + HEIGHT * 0.1), (cx - WIDTH * 0.13, cy + HEIGHT * 0.1)])
        pygame.draw.ellipse(surface, accent, (cx - WIDTH * 0.135, cy + HEIGHT * 0.06, WIDTH * 0.09, HEIGHT * 0.08))
        pygame.draw.ellipse(surface, GUN_DARK, (cx - WIDTH * 0.12, cy + HEIGHT * 0.07, WIDTH * 0.06, HEIGHT * 0.055))
    else:
        bottom = HEIGHT * 1.02
        top = cy + HEIGHT * 0.16
        pygame.draw.polygon(surface, lighter(body, 0.7), [(cx - WIDTH * 0.115, bottom), (cx + WIDTH * 0.115, bottom),
                                                          (cx + WIDTH * 0.048, top), (cx - WIDTH * 0.048, top)])
        pygame.draw.polygon(surface, body, [(cx - WIDTH * 0.09, bottom), (cx + WIDTH * 0.09, bottom),
                                            (cx + WIDTH * 0.04, top), (cx - WIDTH * 0.04, top)])
        pygame.draw.polygon(surface, lighter(body, 1.45), [(cx - WIDTH * 0.025, bottom), (cx + WIDTH * 0.025, bottom),
                                                           (cx + WIDTH * 0.01, top), (cx - WIDTH * 0.01, top)])
        pygame.draw.polygon(surface, accent, [(cx - WIDTH * 0.04, top), (cx + WIDTH * 0.04, top),
                                              (cx + WIDTH * 0.022, cy + HEIGHT * 0.08), (cx - WIDTH * 0.022, cy + HEIGHT * 0.08)])
        pygame.draw.rect(surface, GUN_DARK, (cx - WIDTH * 0.008, cy + HEIGHT * 0.035, WIDTH * 0.016, HEIGHT * 0.05))
    draw_glove(surface, V(cx - WIDTH * 0.075, HEIGHT * 0.88), HEIGHT * 0.055)
    draw_glove(surface, V(cx + WIDTH * 0.075, HEIGHT * 0.96), HEIGHT * 0.065)

    optic = look["optic"]
    if optic in ("reddot", "scope_small", "scope"):
        r = HEIGHT * (0.085 if optic == "reddot" else 0.14)
        thick = max(4, int(HEIGHT * 0.018))
        pygame.draw.rect(surface, GUN_DARK, (cx - WIDTH * 0.03, cy + r * 0.7, WIDTH * 0.06, HEIGHT * 0.16 - r * 0.7))
        glass = pygame.Surface((int(r * 2), int(r * 2)), pygame.SRCALPHA)
        pygame.draw.circle(glass, (140, 190, 230, 30), (r, r), r)
        surface.blit(glass, (cx - r, cy - r))
        pygame.draw.circle(surface, GUN_DARK, (cx, cy), r, thick)
        pygame.draw.circle(surface, lighter(GUN_DARK, 2.0), (cx, cy), r - thick, max(1, int(UI)))
        if optic == "reddot":
            pygame.draw.circle(surface, (255, 60, 60), (cx, cy), 4 * UI)
            pygame.draw.circle(surface, (255, 210, 210), (cx, cy), 1.5 * UI)
        else:                                            # 조준경 십자선
            pygame.draw.line(surface, BLACK, (cx - r, cy), (cx + r, cy), max(1, int(UI)))
            pygame.draw.line(surface, BLACK, (cx, cy - r), (cx, cy + r), max(1, int(UI)))
    else:                                                # 가늠자(아래 양쪽) + 가늠쇠(가운데 기둥)
        for sx in (-1, 1):
            pygame.draw.rect(surface, GUN_DARK, (cx + sx * WIDTH * 0.008 - (WIDTH * 0.03 if sx < 0 else 0),
                                                 cy + HEIGHT * 0.012, WIDTH * 0.03, HEIGHT * 0.05))
        pygame.draw.rect(surface, GUN_DARK, (cx - 3 * UI, cy, 6 * UI, HEIGHT * 0.06))
        pygame.draw.circle(surface, (230, 230, 120), (cx, cy + 2 * UI), 2 * UI)   # 야광 점
    return V(cx, cy + HEIGHT * 0.045)


def make_viewmodel(name, ads, camo=None):
    """총 그림을 미리 그려 둬요. (그림, 화면 위치, 총구 위치)를 돌려줘요. camo="gold"면 금색 총"""
    canvas = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    look = GUN_LOOKS[name]
    if camo in CAMO_COLORS:                   # 금색(무기 레벨) 또는 업적으로 얻은 위장 무늬
        body, accent = CAMO_COLORS[camo]
        look = dict(look, body=body, accent=accent)
    muzzle = (draw_ads_gun if ads else draw_hip_gun)(canvas, look)
    rect = canvas.get_bounding_rect()
    return canvas.subsurface(rect).copy(), (rect.x, rect.y), (muzzle.x, muzzle.y)


def draw_muzzle_flash(surface, pos, size):
    """별 모양 총구 불꽃 (쏠 때마다 모양이 조금씩 달라요)"""
    rot = random.uniform(0, math.tau)
    outer, inner = [], []
    for i in range(10):
        r = size * (1.0 if i % 2 == 0 else 0.42) * random.uniform(0.8, 1.2)
        angle = rot + i * math.pi / 5
        outer.append((pos[0] + math.cos(angle) * r, pos[1] + math.sin(angle) * r))
        inner.append((pos[0] + math.cos(angle) * r * 0.55, pos[1] + math.sin(angle) * r * 0.55))
    pygame.draw.polygon(surface, (255, 190, 80), outer)
    pygame.draw.polygon(surface, (255, 240, 190), inner)
    pygame.draw.circle(surface, WHITE, pos, size * 0.22)


# ---------------------------------------------------------------
# 등장인물과 물건들
# ---------------------------------------------------------------
class Enemy:
    def __init__(self, x, y, kind, skill=1.0):
        self.kind = kind
        self.skill = skill
        self.t = scaled_type(kind, skill)    # 이 종류의 능력치 (라운드가 오를수록 강해져요)
        self.pos = pygame.Vector2(x, y)
        self.hp = self.t["hp"]
        self.dir = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        self.facing = pygame.Vector2(self.dir)   # 바라보는 방향 (방패가 향하는 쪽)
        self.sees = False
        self.los_timer = random.uniform(0, 0.2)   # 시야 검사는 0.2초마다 (계산 아끼기)
        self.spotted = 0.0        # 플레이어를 보고 있던 시간
        self.shoot_timer = 0.0
        self.flash_timer = -1.0   # 총구 불꽃 표시 시간 (쏜 뒤 잠깐 미니맵에 빨간 점)
        self.hurt_timer = 0.0     # 맞았을 때 하얗게 번쩍이는 시간
        throw = self.t.get("throw")
        self.throw_timer = random.uniform(*throw) if throw else 0.0
        self.throw_at = None      # 수류탄을 던질 곳 (Game이 보고 수류탄을 만들어요)
        self.step_timer = random.uniform(0, 0.5)
        self.alert = 0.0          # 내 발소리나 총소리를 듣고 그쪽으로 가는 시간
        self.strafe = 0           # 옆으로 피하는 방향 (-1, 0, 1)
        self.strafe_timer = 0.0
        self.attack_timer = 0.0   # 좀비가 할퀴는 간격
        self.groan_timer = random.uniform(1, 6)   # 좀비가 그르렁거리는 간격
        self.heal_timer = 1.0     # 의무병이 치료하는 간격
        self.heal_flash = 0.0     # 치료받은 적 머리 위에 초록 + 표시
        self.boom = False         # 터지는 좀비가 나에게 닿았는지
        self.flinch = 0.0         # 맞고 움찔하는 시간
        self.flinch_pose = "flinch_l"
        self.suppressed = 0.0     # 내 총알이 가까이 지나가면 움츠러들어 덜 맞혀요
        self.walk = 0.0           # 걸은 거리 (다리 그림 바꾸기용)
        self.role = None          # 분대 역할: "suppress" 제압 사격 / "flank" 옆으로 돌아가기
        self.role_timer = 0.0
        self.flank_spot = None
        self.search = None        # 동료 무전이나 소리로 알게 된 내 마지막 위치 (찾으러 가요)
        self.look_timer = 0.0     # 찾던 곳에 도착하면 두리번거리는 시간
        self.waypoint = None      # 순찰: 다음에 걸어갈 곳
        self.pause_timer = random.uniform(0, 2)
        self.callout = None       # 머리 위 말풍선 [글자, 남은 시간]
        self.shout = None         # Game에게 "외치고 싶어요" (Game이 너무 자주 외치지 않게 골라요)
        self.moving = 0.0         # 방금 움직였는지
        self.mag, self.reload_time = ENEMY_MAGS.get(kind, (0, 0))
        self.ammo = self.mag
        self.reload_left = 0.0
        self.mode = "fight"       # fight 싸우기 / cover 숨기 / peek 고개 내밀어 쏘기
        self.cover_spot = None
        self.peek_spot = None
        self.hide_timer = 0.0
        self.peek_timer = 0.0
        self.cover_cycles = 0
        self.cover_cooldown = random.uniform(0, 3)
        self.stuck_timer = 0.0

    @property
    def aiming(self):
        """저격수가 곧 쏠 때 True (빨간 불빛으로 미리 알려줘요)"""
        return self.kind in ("SNIPER", "LASER") and self.sees and self.spotted > 0.4 and self.shoot_timer < 0.8

    def shield_blocks(self, from_pos):
        """from_pos 쪽에서 날아온 총알을 방패가 막는지 (방패병이 그쪽을 보고 있으면 막아요)"""
        to_shooter = from_pos - self.pos
        if not self.t.get("shield") or to_shooter.length() == 0:
            return False
        return to_shooter.normalize().dot(self.facing) > 0.4

    def update(self, dt, player):
        """적 행동. 플레이어에게 준 피해량을 돌려줘요."""
        t = self.t
        self.flash_timer -= dt
        self.hurt_timer -= dt
        self.heal_flash -= dt
        self.flinch -= dt
        self.suppressed -= dt
        dist = self.pos.distance_to(player.pos)
        if t.get("melee"):
            return self.update_zombie(dt, player, dist)
        self.los_timer -= dt
        if self.los_timer <= 0:
            self.los_timer = 0.2
            self.sees = dist < t["sight"] and can_see(self.pos, player.pos)
        self.cover_cooldown -= dt
        if self.reload_left > 0:                  # 재장전 중
            self.reload_left -= dt
            if self.reload_left <= 0:
                self.ammo = self.mag
        if self.mode != "fight":
            return self.update_cover(dt, player, dist)

        if not self.sees:
            # 못 봤을 때: 어슬렁거리다가 막히면 방향 바꾸기.
            # 내 발소리나 총소리가 들리면 소리 난 쪽으로 다가와요
            self.spotted = 0.0
            self.alert -= dt
            if dist < player.noise and dist > 0:
                self.search = pygame.Vector2(player.pos)     # 소리 난 곳으로
                self.alert = 2.5
            if self.role == "flank" and self.flank_spot is not None:
                self.search = self.flank_spot                # 옆으로 돌아가는 중이면 그 자리로
            self.wander(dt, player)
            return 0

        # 봤을 때: 플레이어 쪽을 보고, 너무 멀면 다가오고, 반응 시간이 지나면 공격
        self.spotted += dt
        if dist > 0:
            self.facing = (player.pos - self.pos).normalize()
        self.search = None
        self.role_timer -= dt
        if self.role and self.role_timer <= 0:
            self.role, self.flank_spot = None, None
        if self.role == "flank" and self.flank_spot is not None:
            offset = self.flank_spot - self.pos          # 옆으로 돌아 들어가요 (쏘면서)
            if offset.length() < 0.7:
                self.role, self.flank_spot = None, None
            else:
                move_with_collision(self.pos, offset.normalize() * t["speed"] * 1.1 * dt)
        elif dist > t["keep"] * (1.4 if self.role == "suppress" else 1.0):
            move_with_collision(self.pos, self.facing * t["speed"] * dt)
        # 옆으로 왔다 갔다 피해요 (실력이 좋을수록 많이). 저격수와 무거운 적은 안 피해요
        if self.kind not in ("SNIPER", "HEAVY", "BOSS", "GUNNER", "LASER"):
            self.strafe_timer -= dt
            if self.strafe_timer <= 0:
                self.strafe_timer = random.uniform(0.5, 1.4)
                self.strafe = random.choice((-1, 0, 1))
            if self.strafe:
                side = pygame.Vector2(-self.facing.y, self.facing.x)
                dodge = 0.95 if t.get("flank") else min(0.8, 0.25 + (self.skill - 1.0))
                move_with_collision(self.pos, side * self.strafe * t["speed"] * dodge * dt)
        if self.spotted < t["reaction"]:
            return 0

        # 엄폐: 다쳤거나, 재장전해야 하거나, 제압당하면 가까운 엄폐물 뒤로 숨어요
        hurt = self.hp < t["hp"] * 0.5
        if (self.kind in COVER_USERS and self.cover_cooldown <= 0 and dist > 3
                and (hurt or self.reload_left > 0 or self.suppressed > 0)):
            spot = self.find_cover(player)
            if spot:
                self.mode, self.cover_spot, self.cover_cycles, self.stuck_timer = "cover", spot, 0, 0.0
                self.hide_timer = random.uniform(1.2, 2.2)
                return 0
            self.cover_cooldown = 3.0

        # 수류탄 던지기 (폭탄병, 보스)
        throw = t.get("throw")
        if throw and t["throw_range"][0] <= dist <= t["throw_range"][1]:
            self.throw_timer -= dt
            if self.throw_timer <= 0:
                self.throw_timer = random.uniform(*throw)
                self.throw_at = pygame.Vector2(player.pos)
                self.shout = "GRENADE OUT!"

        return self.shoot_at(dt, player, dist)

    def wander(self, dt, player):
        """안 보일 때 움직임: 알게 된 위치로 찾아가고, 도착하면 두리번, 아니면 순찰 (갈 곳 -> 잠깐 멈춤 -> 다음 곳)"""
        t = self.t
        self.role_timer -= dt
        if self.role and self.role_timer <= 0:
            self.role, self.flank_spot = None, None
        before = pygame.Vector2(self.pos)
        if self.search is not None:
            offset = self.search - self.pos
            if offset.length() < 0.7:
                self.search, self.look_timer = None, random.uniform(1.5, 3.0)
                if self.role == "flank":
                    self.role, self.flank_spot = None, None
            else:
                self.dir = offset.normalize()
                move_with_collision(self.pos, self.dir * t["speed"] * dt)
                self.stuck_timer = self.stuck_timer + dt if self.pos.distance_to(before) < t["speed"] * dt * 0.3 else 0.0
                if self.stuck_timer > 0.8:                      # 막혔어요: 포기하고 두리번
                    self.search, self.stuck_timer, self.look_timer = None, 0.0, 1.5
                    self.dir = self.dir.rotate(random.choice((-90, 90)))
        elif self.look_timer > 0:
            self.look_timer -= dt
            self.dir = self.dir.rotate(dt * 140 * (1 if int(self.look_timer * 1.5) % 2 else -1))   # 두리번
        elif self.pause_timer > 0:
            self.pause_timer -= dt
        else:
            if self.waypoint is None:
                self.waypoint = self.pick_waypoint(player.pos)
            if self.waypoint is not None:
                offset = self.waypoint - self.pos
                if offset.length() < 0.4:
                    self.waypoint, self.pause_timer = None, random.uniform(0.5, 1.8)
                else:
                    self.dir = offset.normalize()
                    move_with_collision(self.pos, self.dir * t["speed"] * 0.65 * dt)
                    if self.pos.distance_to(before) < t["speed"] * dt * 0.1:
                        self.waypoint = None
        self.facing = pygame.Vector2(self.dir)

    def pick_waypoint(self, target):
        """순찰할 다음 곳: 3~7칸 떨어진, 막히지 않고 곧장 걸어갈 수 있는 곳.
        대체로 플레이어가 있는 쪽으로 순찰해요 (가만히 숨어 있어도 언젠가 마주쳐요)"""
        toward = math.degrees(math.atan2(target.y - self.pos.y, target.x - self.pos.x))
        for k in range(8):
            angle = toward + random.uniform(-70, 70) if k < 5 and random.random() < 0.7 else random.uniform(0, 360)
            spot = self.pos + pygame.Vector2(random.uniform(3, 7), 0).rotate(angle)
            if not is_blocked(spot.x, spot.y) and can_see(self.pos, spot):
                return spot
        return None

    def shoot_at(self, dt, player, dist):
        """쏠 수 있으면 쏴요. 플레이어에게 준 피해를 돌려줘요."""
        t = self.t
        if dist > t["range"] or not self.sees or self.reload_left > 0:
            return 0
        self.shoot_timer -= dt
        if self.shoot_timer > 0:
            return 0
        self.shoot_timer = random.uniform(*t["fire"]) * (0.6 if self.role == "suppress" else 1.0)
        self.flash_timer = 0.08
        if self.mag:
            self.ammo -= 1
            if self.ammo <= 0:
                self.reload_left = self.reload_time   # 탄창이 비었어요: 재장전
                self.shout = "RELOADING!"
        # 멀수록, 플레이어가 움직이거나 점프 중일수록 잘 안 맞아요
        chance = t["accuracy"] - dist * t["falloff"]
        if player.moving:
            chance -= 0.15
        if player.z > 0:
            chance -= 0.15
        if player.crouch_amt > 0.5:
            chance -= 0.1
        if player.sprinting or player.slide_timer > 0:
            chance -= 0.1
        if self.suppressed > 0:
            chance *= 0.5                         # 제압당해서 머리를 숙이고 쏴요
            self.shoot_timer += 0.25
        if self.role == "suppress":
            chance *= 0.7                         # 제압 사격: 많이 쏘지만 덜 정확해요
        if random.random() < max(0.08, chance):
            return random.randint(*t["damage"])
        return 0


    # 엄폐할 수 있는 자리: 건물/상자 바로 옆 칸 (Game이 맵마다 정해요)
    cover_spots = []

    def find_cover(self, player):
        """가까운 엄폐 자리 중 플레이어에게 안 보이는 곳 (가까운 순서로 몇 개만 검사)"""
        near = sorted((spot for spot in Enemy.cover_spots if spot.distance_to(self.pos) < 5),
                      key=lambda spot: spot.distance_to(self.pos))[:12]
        for spot in near:
            if spot.distance_to(player.pos) > 3 and not can_see(spot, player.pos):
                return spot
        return None

    def find_peek(self, player):
        """엄폐 자리 옆에서 플레이어가 보이는 곳 (고개를 내밀 자리)"""
        for k in range(8):
            spot = self.cover_spot + pygame.Vector2(1, 0).rotate(k * 45)
            if not is_blocked(spot.x, spot.y) and can_see(spot, player.pos):
                return spot
        return None

    def move_to(self, target, speed, dt):
        """목표 자리로 걸어가요. 도착했으면 True. 오래 막혀 있으면 포기해요."""
        offset = target - self.pos
        if offset.length() < 0.15:
            return True
        before = pygame.Vector2(self.pos)
        self.facing = offset.normalize()
        move_with_collision(self.pos, self.facing * min(speed * dt, offset.length()))
        self.stuck_timer = self.stuck_timer + dt if self.pos == before else 0.0
        if self.stuck_timer > 0.8:
            self.mode, self.cover_cooldown = "fight", 4.0
        return False

    def update_cover(self, dt, player, dist):
        """엄폐 행동: 숨기 → (재장전) → 고개를 내밀어 쏘기 → 다시 숨기. 세 번 하거나 가까이 오면 그만둬요."""
        t = self.t
        if dist < 3 or self.cover_cycles >= 3:
            self.mode, self.cover_cooldown = "fight", 6.0
            return 0
        if self.mode == "cover":
            if not self.move_to(self.cover_spot, t["speed"] * 1.3, dt):
                return 0
            if dist > 0:
                self.facing = (player.pos - self.pos).normalize()
            self.hide_timer -= dt
            if self.hide_timer <= 0 and self.reload_left <= 0:
                self.peek_spot = self.find_peek(player)
                if self.peek_spot is None:
                    self.mode, self.cover_cooldown = "fight", 4.0
                    return 0
                self.mode, self.peek_timer = "peek", random.uniform(1.5, 2.5)
            return 0
        # 고개 내밀기: 옆 칸으로 나와서 쏘고, 시간이 되거나 탄창이 비면 다시 숨어요
        self.move_to(self.peek_spot, t["speed"] * 1.3, dt)
        if dist > 0:
            self.facing = (player.pos - self.pos).normalize()
        self.spotted = max(self.spotted, t["reaction"])
        self.peek_timer -= dt
        if self.peek_timer <= 0 or self.reload_left > 0:
            self.mode, self.hide_timer = "cover", random.uniform(1.2, 2.2)
            self.cover_cycles += 1
            return 0
        return self.shoot_at(dt, player, dist)

    # 좀비 길찾기 지도: 칸마다 플레이어까지 몇 걸음인지 (Game이 0.3초마다 새로 만들어요)
    flow = None

    def update_zombie(self, dt, player, dist):
        """좀비: 건물을 돌아서 나에게 다가와 할퀴어요. 준 피해를 돌려줘요."""
        t = self.t
        self.sees = True
        self.attack_timer -= dt
        if dist > 0.7:
            target = self.next_step(player, dist)
            offset = target - self.pos
            if offset.length() > 0:
                self.facing = offset.normalize()
                move_with_collision(self.pos, self.facing * t["speed"] * dt)
            return 0
        if dist > 0:
            self.facing = (player.pos - self.pos).normalize()
        if t.get("explode"):
            self.boom = True                      # 터져요!
            return 0
        if self.attack_timer <= 0:
            self.attack_timer = t["melee"][1]
            self.flash_timer = 0.25               # 팔을 들고 할퀴는 모습
            return t["melee"][0]
        return 0

    def next_step(self, player, dist):
        """길찾기 지도에서 나에게 한 걸음 더 가까운 옆 칸의 가운데 (대각선은 모서리를 가로지르지 않게)"""
        flow = Enemy.flow
        if flow is None or dist < 1.5:
            return player.pos
        col, row = int(self.pos.x), int(self.pos.y)
        best, best_d = None, flow[row][col] if in_map(col, row) and flow[row][col] is not None else math.inf
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            c, r = col + dc, row + dr
            if not in_map(c, r) or flow[r][c] is None:
                continue
            if dc and dr and (is_blocked(col + dc, row) or is_blocked(col, row + dr)):
                continue
            if flow[r][c] < best_d:
                best, best_d = (c, r), flow[r][c]
        if best is None:
            return player.pos
        return pygame.Vector2(best[0] + 0.5, best[1] + 0.5)


class Player:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.angle = 0.0
        self.pitch = 0.0          # 위아래 시점 (+면 위를 봐요)
        self.z = 0.0              # 점프 높이
        self.vz = 0.0             # 위아래 속도
        self.hp = 100
        self.moving = False
        self.sprinting = False
        self.crouch = False       # 앉아 있는지
        self.crouch_amt = 0.0     # 앉은 정도 0(서 있음) ~ 1(앉음). 부드럽게 바뀌어요
        self.slide_timer = 0.0    # 슬라이딩 남은 시간
        self.slide_dir = pygame.Vector2(1, 0)
        self.noise = 0.0          # 내 소리가 들리는 거리 (적이 듣고 다가와요)
        self.turn_hold = 0.0      # 화살표 키를 누르고 있는 시간 (살짝 누르면 천천히, 오래 누르면 빠르게)
        self.look_hold = 0.0
        self.stick = (0.0, 0.0)   # 게임패드 오른쪽 스틱 (좌우 라디안/초, 위아래 px/초)

    @property
    def forward(self):
        return pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

    def toggle_crouch(self):
        """C: 서 있으면 앉고, 앉아 있으면 일어나요. 달리다가 누르면 슬라이딩!"""
        if self.sprinting and self.z == 0:
            self.slide_timer = SLIDE_TIME
            self.slide_dir = self.forward
            self.crouch = True
            self.sprinting = False
        else:
            self.crouch = not self.crouch

    def update(self, dt, keys, mouse_dx, mouse_dy, sens, speed, allow_sprint):
        """sens: 확대했을 때 감도를 낮추는 비율, speed: 이동 속도 비율 (정조준·무거운 총은 느리게)
        allow_sprint: 달릴 수 있는지 (정조준하거나 쏘는 중엔 못 달려요)"""
        self.angle += mouse_dx * MOUSE_SENS * SETTINGS["mouse"] * sens
        self.pitch -= mouse_dy * MOUSE_SENS_Y * SETTINGS["mouse"] * sens
        self.angle += self.stick[0] * sens * dt
        self.pitch += self.stick[1] * sens * dt
        # 화살표 키 가속: 처음엔 30% 속도로 천천히(정밀 조준), 누르고 있으면 점점 빨라져요
        turning = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
        self.turn_hold = self.turn_hold + dt if turning else 0.0
        looking = keys[pygame.K_UP] or keys[pygame.K_DOWN]
        self.look_hold = self.look_hold + dt if looking else 0.0
        turn = TURN_SPEED * SETTINGS["look"] * sens * dt * min(1.15, 0.3 + self.turn_hold * 2.0)
        look = LOOK_SPEED * SETTINGS["look"] * sens * dt * min(1.1, 0.35 + self.look_hold * 2.0)
        if keys[pygame.K_LEFT]:
            self.angle -= turn
        if keys[pygame.K_RIGHT]:
            self.angle += turn
        if keys[pygame.K_UP]:
            self.pitch += look
        if keys[pygame.K_DOWN]:
            self.pitch -= look
        self.pitch = max(-MAX_PITCH, min(MAX_PITCH, self.pitch))

        # 점프: 땅에 있을 때만. 앉아 있으면 점프 대신 일어나요
        if keys[pygame.K_SPACE] and self.z == 0 and self.slide_timer <= 0:
            if self.crouch:
                self.crouch = False
            else:
                self.vz = JUMP_SPEED
        self.vz -= GRAVITY * dt
        self.z = max(0.0, self.z + self.vz * dt)
        if self.z == 0:
            self.vz = 0.0

        # 앉은 정도를 부드럽게 바꿔요 (눈높이가 스르르 내려가요)
        target = 1.0 if self.crouch else 0.0
        step = 6 * dt
        self.crouch_amt += max(-step, min(step, target - self.crouch_amt))

        # 슬라이딩 중: 처음 방향으로 미끄러지다가 점점 느려져요
        if self.slide_timer > 0:
            self.slide_timer -= dt
            k = max(0.0, self.slide_timer / SLIDE_TIME)
            move_with_collision(self.pos, self.slide_dir * MOVE_SPEED * (1 + (SLIDE_SPEED - 1) * k) * dt)
            self.moving = True
            self.sprinting = False
            return

        forward = self.forward
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
        shift = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        self.sprinting = allow_sprint and self.moving and keys[pygame.K_w] and shift and self.z == 0
        if self.sprinting:
            self.crouch = False                   # 달리면 일어나요
        mult = speed * (SPRINT_SPEED if self.sprinting else 1.0) * (CROUCH_SPEED if self.crouch else 1.0)
        if self.moving:
            move_with_collision(self.pos, move.normalize() * MOVE_SPEED * mult * dt)


class Weapon:
    """무기 하나의 총알 수"""

    def __init__(self, spec, ammo_mult=1.0):
        self.spec = spec
        self.mag = spec["mag"]
        self.reserve = int(spec["reserve"] * ammo_mult)
        self.upgraded = False      # 좀비 모드에서 강화했는지


class Arsenal:
    """가지고 있는 무기들과 사격/재장전/반동/무기 교체, 수류탄 개수를 관리"""

    SWITCH_TIME = 0.4

    def __init__(self, specs=None, reload_mult=1.0, ammo_mult=1.0):
        """specs: 가지고 다닐 무기들 (로드아웃). 없으면 모든 무기"""
        self.ammo_mult = ammo_mult
        self.reload_mult = reload_mult
        self.SWITCH_TIME = Arsenal.SWITCH_TIME * reload_mult
        self.weapons = [Weapon(spec, ammo_mult) for spec in (specs or WEAPONS)]
        self.index = 0
        self.last_index = 1 % len(self.weapons)
        self.cooldown = 0.0
        self.reload_left = 0.0
        self.reload_total = 1.0
        self.reload_empty = False
        self.shell = False         # 한 발씩 넣는 재장전 중인지 (산탄총)
        self.shells_loaded = 0     # 이번 장면에 넣은 탄 수 (Game이 "착" 소리를 내요)
        self.switch_left = 0.0
        self.recoil = 0.0          # 반동으로 시점이 위로 튄 정도(px)
        self.since_shot = 1.0
        self.kick = 0.0            # 화면 아래 총이 뒤로 밀리는 효과
        self.zoom_index = 0        # 조준경 배율 (SCOPE_ZOOMS 중 몇 번째)
        self.grenades = GRENADES_START

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
            self.reload_empty = w.mag == 0          # 다 쏘고 하는 재장전은 노리쇠까지 당겨서 더 오래
            self.shell = w.spec["name"] in SHELL_RELOAD
            if self.shell:
                self.reload_left = SHELL_RELOAD[w.spec["name"]] * self.reload_mult
            else:
                self.reload_left = w.spec["reload"] * self.reload_mult * (1.25 if self.reload_empty else 1.0)
            self.reload_total = self.reload_left

    def add_ammo(self):
        """탄약 상자: 모든 무기의 여분 총알을 채워요. 하나라도 채웠으면 True"""
        added = False
        for w in self.weapons:
            cap = int(w.spec["reserve"] * 2 * self.ammo_mult)
            if w.reserve < cap:
                w.reserve = min(cap, w.reserve + max(1, int(w.spec["reserve"] * self.ammo_mult) // 2))
                added = True
        return added

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
                if self.shell:                          # 한 발 넣고, 더 넣을 수 있으면 계속
                    w.mag += 1
                    w.reserve -= 1
                    self.shells_loaded += 1
                    if w.mag < w.spec["mag"] and w.reserve > 0:
                        self.reload_left = self.reload_total
                    return
                taken = min(w.spec["mag"] - w.mag, w.reserve)
                w.mag += taken
                w.reserve -= taken

    def try_fire(self):
        """쏠 수 있으면 총알 하나를 쓰고 True"""
        w = self.current
        if self.shell and self.reload_left > 0 and w.mag > 0:
            self.reload_left = 0.0                      # 한 발씩 넣다가 쏘면 바로 멈춰요
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
    """야자수, 자동차, 가로등 같은 장식물. cover=True면 총알을 막아요."""

    def __init__(self, x, y, image, height, width, cover=False):
        self.pos = pygame.Vector2(x, y)
        self.image = image
        self.height = height
        self.width = width
        self.cover = cover
        self.glow = False


class Pickup:
    """바닥에 놓인 상자 (탄약 / 체력 / 수류탄)"""

    def __init__(self, x, y, kind):
        self.pos = pygame.Vector2(x, y)
        self.kind = kind
        self.phase = random.uniform(0, 6)    # 위아래로 둥둥 떠 있는 움직임


class Projectile:
    """날아가는 수류탄 / 로켓"""

    def __init__(self, kind, pos, z, vel, vz, owner="player"):
        self.kind = kind                      # "grenade" 또는 "rocket"
        self.owner = owner                    # "player" 또는 "enemy" (누가 던졌는지)
        self.pos = pygame.Vector2(pos)
        self.z = z
        self.vel = pygame.Vector2(vel)
        self.vz = vz
        self.bounced = False                  # 유탄: 어디든 닿았는지
        if kind == "rocket":
            self.timer = 4.0
        elif kind == "shell":
            self.timer = 3.0
        else:
            self.timer = GRENADE_FUSE if owner == "player" else ENEMY_GRENADE_FUSE

    def update(self, dt, enemies):
        """움직이기. 터져야 하면 True"""
        self.timer -= dt
        speed = math.hypot(self.vel.x, self.vel.y, self.vz)
        steps = max(1, int(speed * dt / 0.1) + 1)     # 빠르면 잘게 나눠서 벽을 뚫지 않게
        sdt = dt / steps
        for _ in range(steps):
            if self.kind == "grenade":
                self.bounce_step(sdt)
            elif self.kind == "shell":
                self.bounce_step(sdt)
                if self.bounced or any(e.pos.distance_to(self.pos) < 0.4 and self.z <= e.t["height"]
                                       for e in enemies):
                    return True                   # 유탄은 닿는 순간 터져요
            elif self.rocket_step(sdt, enemies):
                return True
        return self.timer <= 0

    def bounce_step(self, sdt):
        """수류탄: 중력으로 떨어지고, 벽과 바닥에 튕겨요."""
        self.vz -= GRAVITY * sdt
        nx = self.pos.x + self.vel.x * sdt
        if obstacle_height(nx, self.pos.y) > self.z:
            self.vel.x *= -0.5
            self.bounced = True
        else:
            self.pos.x = nx
        ny = self.pos.y + self.vel.y * sdt
        if obstacle_height(self.pos.x, ny) > self.z:
            self.vel.y *= -0.5
            self.bounced = True
        else:
            self.pos.y = ny
        self.z += self.vz * sdt
        if self.z < 0:
            self.z = 0.0
            self.bounced = True
            self.vz = -self.vz * 0.35 if abs(self.vz) > 1 else 0.0
            self.vel *= 0.6

    def rocket_step(self, sdt, enemies):
        """로켓: 똑바로 날아가다 무언가에 닿으면 터져요. 터져야 하면 True"""
        self.pos += self.vel * sdt
        self.z += self.vz * sdt
        if self.z <= 0 or obstacle_height(self.pos.x, self.pos.y) > self.z:
            self.pos -= self.vel.normalize() * 0.15     # 벽 안에서 터지지 않게 살짝 뒤로
            self.z = max(0.05, self.z)
            return True
        for e in enemies:
            if e.pos.distance_to(self.pos) < 0.4 and self.z <= e.t["height"]:
                return True
        return False


class Corpse:
    """쓰러진 적: 맞은 방향으로 밀려나며 넘어지고, 한동안 바닥에 남아요"""

    # 쓰러지는 방식: (밀려나는 세기, 그림이 넘어가는 빠르기 초, 위로 튀는 속도)
    STYLES = {"fall": (1.6, 0.12, 0.0),       # 보통: 맞은 방향으로 밀리며 넘어져요
              "drop": (0.3, 0.05, 0.0),       # 헤드샷: 그 자리에서 털썩
              "fly": (3.4, 0.09, 1.2),        # 센 한 방(산탄총·저격): 뒤로 날아가요
              "blast": (3.0, 0.1, 4.5)}       # 폭발: 공중으로 떴다가 떨어져요

    def __init__(self, enemy, push, style="fall"):
        strength, self.frame_time, self.vz = self.STYLES[style]
        self.pos = pygame.Vector2(enemy.pos)
        self.kind = enemy.kind
        self.vel = push * strength            # 밀려나는 속도
        self.z = 0.0                          # 공중에 뜬 높이
        self.age = 0.0
        self.side = random.choice((-1, 1))    # 왼쪽/오른쪽 중 쓰러지는 쪽


class Sentry:
    """킬스트릭 자동 포탑: 가까이 보이는 적을 알아서 쏴요"""

    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.timer = SENTRY_TIME
        self.cooldown = 0.0
        self.flash = 0.0


class Effect:
    """폭발 같은 잠깐 보였다 사라지는 효과"""

    def __init__(self, pos, frames, duration, size):
        self.pos = pygame.Vector2(pos)
        self.frames = frames
        self.duration = duration
        self.age = 0.0
        self.size = size

    @property
    def done(self):
        return self.age >= self.duration

    @property
    def frame(self):
        i = int(self.age / self.duration * len(self.frames))
        return self.frames[min(i, len(self.frames) - 1)]


# ---------------------------------------------------------------
# 게임 전체
# ---------------------------------------------------------------
class Game:
    def __init__(self, save, start_round=1, mode="campaign", loadout=None, mission=0, stage=0, challenge=None):
        """save: 저장 정보(dict). 라운드를 깨거나 죽을 때마다 고쳐서 파일에 써요.
        mode: "campaign"(라운드마다 맵이 바뀌는 전투) 또는 "zombies"(좀비 웨이브 버티기)
        loadout: 고른 주무기/보조무기/퍼크 (없으면 모든 무기를 들고 시작)"""
        self.mode = mode
        self.challenge = challenge  # 도전 모드 이름 (없으면 None)
        self.challenge_time = 0.0
        self.challenge_done = False
        self.loadout = loadout
        self.mission = mission     # 미션 모드: 몇 번째 미션인지
        self.stage = stage         # 미션 모드: 지금 단계 (0부터)
        self.mission_time = 0.0
        self.mission_complete = False
        self.perk = loadout["perk"] if loadout else None
        ranks = save.get("skills", {})
        self.max_hp = (130 if self.perk == "IRON SKIN" else 100) + 15 * ranks.get("VITALITY", 0)
        self.cooldowns = {}        # 액티브 스킬 다시 쓰기까지 남은 시간
        self.focus = 0.0           # FOCUS: 적이 느려지는 남은 시간
        self.scan = 0.0            # SCAN: 적이 다 보이는 남은 시간
        self.pickup_images = {kind: make_pickup_image(kind) for kind in DROP_WEIGHTS}
        self.decor_images = {
            "T": make_palm_image(), "L": make_lamp_image(),
            "X": make_crane_image(), "b": make_billboard_image(),
            "I": make_pine_image(), "v": make_burnt_car_image(),
        }
        self.snowy_pine = make_pine_image(snowy=True)
        rng = random.Random(3)            # 눈송이: (x, y, 떨어지는 속도)
        self.snowflakes = [(rng.random(), rng.random(), rng.uniform(0.08, 0.2)) for _ in range(160)]
        self.car_images = [make_car_image(color) for color in CAR_COLORS]
        self.grenade_image = make_grenade_image()
        self.rocket_image = make_rocket_image()
        self.explosion_frames = make_explosion_frames()
        self.flare_frames = make_flare_frames()
        self.sentry_images = (make_sentry_image(), make_sentry_image(flash=True))
        self.blood_pool = make_blood_pool_image()
        self.hurt_vignette = make_hurt_vignette()
        self.splat_images = [make_screen_splat(i) for i in range(4)]
        self.glow_image = make_glow(128, (255, 200, 120))      # 가로등 불빛
        self.flash_overlay = pygame.Surface((WIDTH, HEIGHT))
        self.flash_overlay.fill((230, 235, 255))
        self.lightning = 0.0       # 번개 번쩍임 남은 시간
        self.lightning_timer = 6.0
        self.muzzle_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.muzzle_light.fill((255, 220, 150, 28))
        self.scope_overlay = make_scope_overlay()
        self.sounds = get_sounds()
        self.was_reloading = False
        # 총 그림: 무기마다 허리 자세 / 정조준 자세 두 가지를 미리 그려 둬요
        self.viewmodels = {}       # 총 그림 (처음 들 때 그려서 기억해 둬요)
        self.sway = 0.0            # 고개를 돌리면 총이 살짝 늦게 따라와요
        self.step_timer = 0.0
        self.was_airborne = False
        self.fonts = make_fonts()
        self.font, self.big_font, self.small_font = self.fonts["normal"], self.fonts["big"], self.fonts["small"]
        self.save = save
        self.xp = save.get("xp", 0)
        self.map_index = None
        self.set_col_w(START_COL_W)
        self.fire_was_down = False
        self.click_queued = False
        self.aim_on = False        # E 키로 켠 정조준
        self.show_fps = False      # P 또는 F3
        self.show_help = False     # H
        self.fps = 0.0
        self.hitstop = 0.0         # 쓰러뜨리는 순간 화면이 아주 잠깐 멈춰요 (묵직한 손맛)
        self.slowmo = 0.0          # 라운드 마지막 적을 쓰러뜨리면 잠깐 느리게
        self.gun_noise = 0.0       # 방금 총을 쐈으면 적이 듣고 다가와요
        self.pad_aim = False       # 게임패드 왼쪽 트리거를 누르고 있으면 정조준
        self.on_target = False     # 조준점이 적 위에 있는지 (조준선이 빨개지고 시점이 살짝 끈적해져요)
        self.muzzle_screen = (WIDTH * 0.6, HEIGHT * 0.75)   # 화면에서 총구 위치 (총알 궤적 시작점)
        self.recoil_patterns = {}
        self.shot_index = 0        # 연사 중 몇 번째 발인지 (반동 모양)
        self.echoes = []           # 조금 뒤에 날 소리: [남은 시간, 소리, 크기]
        self.screen_blood = []     # 화면에 묻은 피: [x, y, 크기, 남은 시간]
        self.suppress = 0.0        # 적 총알이 가까이 스치면 올라가요 (화면이 어두워지고 조준이 흔들려요)
        self.dark_vignette = make_hurt_vignette((0, 0, 0))
        self.reload_prev = 0.0     # 재장전 진행 정도 (동작 소리 타이밍)
        self.objective_images = {kind: make_objective_image(kind) for kind in OBJECTIVES}
        self.objective = None      # 이번 라운드 목표 (없으면 전멸)
        self.gun_noise_radius = 16.0
        self.killcam_from = None   # 나를 쓰러뜨린 곳 (킬캠 카메라 위치)
        self.killcam_time = 0.0
        self.killcam_killer = ""
        self.killcam_zoom = None
        self.last_attacker = None
        self.last_source = None
        self.fail_reason = ""
        self.reset(start_round)

    def set_col_w(self, col_w):
        """세로 줄 폭 바꾸기 (작을수록 선명, 클수록 빠름)"""
        self.col_w = col_w
        self.num_rays = math.ceil(WIDTH / col_w)
        self.zbuffer = [math.inf] * self.num_rays
        self.wall_top = [HEIGHT] * self.num_rays    # 줄마다 가장 가까운 건물의 위쪽 y (총알 자국 위치 계산용)
        self.wall_thin = [False] * self.num_rays    # 줄마다 가장 가까운 벽이 총알이 뚫는 얇은 엄폐물인지
        self.wall_hit = [None] * self.num_rays      # 줄마다 가장 가까운 벽: (칸 x, 칸 y, 세로벽인지, 맞은 위치, 건물 정보)

    def adjust_quality(self, frame_time):
        """한 장면 계산 시간을 보고 선명도를 자동으로 조절해요."""
        if frame_time > FRAME_BUDGET and self.col_w < MAX_COL_W:
            self.set_col_w(self.col_w + 1)
        elif (self.col_w > MIN_COL_W
              and frame_time * self.col_w / (self.col_w - 1) < FRAME_BUDGET * 0.75):
            self.set_col_w(self.col_w - 1)

    def setup_map(self, index, set_no=1):
        """맵 바꾸기: 맵 정보, 장식물, 적 출현 위치, 미니맵, 하늘을 새로 만들어요."""
        self.theme = variant_theme(MAPS[index], set_no)
        load_map(index, self.theme)
        self.decals = {}           # 벽 자국: (칸 x, 칸 y, 세로벽인지) -> [(위치, 높이, "hole"/"scorch"), ...]
        self.decal_count = 0
        self.broken_windows = set()
        self.cover_hp = {}         # 부서지는 엄폐물 남은 체력
        self.map_index = index
        self.map_key = (index, set_no)
        self.decor = []
        images = dict(self.decor_images)
        if self.theme["snow"]:
            images["I"] = self.snowy_pine
        sizes = {"T": (2.4, 1.2), "L": (1.9, 0.3), "X": (5.5, 3.0), "b": (2.6, 1.8), "I": (2.6, 1.3)}
        for letter, (height, width) in sizes.items():
            self.decor += [Decor(x, y, images[letter], height, width) for x, y in find_cells(letter)]
        self.decor += [Decor(x, y, images["v"], 0.6, 1.1, cover=True) for x, y in find_cells("v")]
        for d in self.decor:
            d.glow = d.image is images["L"]           # 가로등은 밤에 빛나요
        # 적 그림: 맵에 맞는 위장복으로 다시 그려요 (일반병, 저격수)
        camo = self.theme["camo"]
        self.enemy_images = {}
        for kind, t in ENEMY_TYPES.items():
            look = dict(t["look"], **camo) if camo and kind in ("GRUNT", "SNIPER", "GUNNER") else t["look"]
            for state in ("normal", "flash", "hurt", "aim"):
                self.enemy_images[(kind, state)] = make_enemy_image(look, state)
            # 걷는 모습 2장, 뒷모습 (+ 걷는 뒷모습). 모래주머니 진지와 방패병은 그대로
            if not look.get("sandbags") and not look.get("shield") and look["head"] != "drone":
                bases = [("", self.enemy_images[(kind, "normal")])]
                if look["head"] != "zombie":
                    back = make_back_image(look)
                    self.enemy_images[(kind, "back")] = back
                    bases.append(("back_", back))
                for prefix, base in bases:
                    for side in (0, 1):
                        self.enemy_images[(kind, f"{prefix}walk{side}")] = walk_frame(base, side)
            # 맞고 움찔: 몸통은 옆으로 기울고, 머리를 맞으면 크게 젖혀져요
            hurt = self.enemy_images[(kind, "hurt")]
            self.enemy_images[(kind, "flinch_l")] = pygame.transform.rotate(hurt, 9)
            self.enemy_images[(kind, "flinch_r")] = pygame.transform.rotate(hurt, -9)
            self.enemy_images[(kind, "flinch_head")] = pygame.transform.rotate(hurt, 16 * random.choice((-1, 1)))
        # 쓰러지는 모습: 서 있는 그림을 25도, 55도, 90도로 기울인 그림 (왼쪽/오른쪽)
        self.corpse_frames = {}
        self.enemy_images[("PLAYER", "hurt")] = make_enemy_image(PLAYER_LOOK, "hurt")   # 킬캠에서 쓰러진 나
        for kind, t in list(ENEMY_TYPES.items()) + [("PLAYER", dict(height=0.9, width=0.45))]:
            img = self.enemy_images[(kind, "hurt")]
            for side in (-1, 1):
                frames = []
                for degrees in (25, 55, 90):
                    rad = math.radians(degrees)
                    h = t["height"] * math.cos(rad) + t["width"] * math.sin(rad)
                    w = t["width"] * math.cos(rad) + t["height"] * math.sin(rad)
                    frames.append((pygame.transform.rotate(img, degrees * side), h, w))
                self.corpse_frames[(kind, side)] = frames
        # 자동차 색은 위치에 따라 정해져요 (매번 똑같이)
        cars = self.car_images
        self.decor += [Decor(x, y, cars[int(x * 7 + y * 3) % len(cars)], 0.6, 1.1, cover=True)
                       for x, y in find_cells("c")]
        self.spawn_points = find_cells("E")
        dark = self.theme.get("dark", 1.0)
        used = {ch for line in GAME_MAP for ch in line if ch in WALLS}
        self.wall_textures = {ch: make_wall_textures(ch, shade(WALLS[ch][0], dark), WALLS[ch][1], HAZE) for ch in used}
        Enemy.cover_spots = [pygame.Vector2(col + 0.5, row + 0.5)
                             for row in range(MAP_H) for col in range(MAP_W)
                             if not is_blocked(col + 0.5, row + 0.5)
                             and any(in_map(col + dc, row + dr) and WALL_GRID[row + dr][col + dc]
                                     for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        dark = self.theme.get("dark", 1.0)          # 어두운 맵일수록 쏠 때 주변이 크게 번쩍여요
        self.muzzle_light.fill((255, 220, 150, int(28 + 90 * (1 - dark))))
        self.muzzle_glow = 50 + 110 * (1 - dark)
        self.night = dark < 0.95 or self.theme.get("stars", False)
        if self.theme.get("rain"):
            ambience = "rain"
        elif self.night and not self.theme["snow"]:
            ambience = "night"
        else:
            ambience = "wind"
        self.sounds.start_background(ambience, music=True)
        self.minimap = self.make_minimap()
        self.sky = make_sky(self.theme)

    def reset(self, start_round=1):
        """새 게임 (또는 저장된 라운드부터 시작)"""
        self.round = start_round
        self.fail_reason = ""
        self.killcam_from = None
        self.kills = 0
        self.points = 0            # 좀비 모드 점수 (B 탄약, U 총 강화에 써요)
        self.game_over = False
        self.hint_timer = 8.0      # 처음 8초 동안 화면 아래에 조작법 안내
        self.reset_streak()
        self.start_round()

    def reset_streak(self):
        """킬스트릭(죽지 않고 연속 처치)은 죽으면 처음부터 다시 세요"""
        self.streak = 0
        self.streaks_ready = []    # 받은 킬스트릭 (X로 하나씩 써요)

    def retry_round(self):
        """죽은 라운드부터 다시 (처치 수는 그대로). 좀비 모드는 1웨이브부터"""
        self.fail_reason = ""
        self.killcam_from = None
        self.map_key = None                      # 부서진 상자, 깨진 창문을 원래대로 (맵을 다시 불러요)
        self.map_index = None
        if self.mode == "zombies":
            self.reset(1)
            return
        if self.mode == "mission":
            if self.mission_complete:              # 다 깼으면 처음부터 다시
                self.stage = 0
                self.mission_time = 0.0
                self.reset(1)
            else:
                self.respawn_checkpoint()
            return
        self.game_over = False
        self.challenge_done = False
        self.reset_streak()
        self.start_round()

    def rank_of(self, skill):
        """스킬 단계 (안 배웠으면 0)"""
        return self.save.get("skills", {}).get(skill, 0)

    def weapon_spec(self, name):
        """그 무기의 지금 성능 (처치 수에 따른 레벨과 부착물 적용)"""
        kills = self.save.get("wkills", {}).get(name, 0)
        spec = apply_mods(WEAPON_BY_NAME[name], weapon_mods(kills), weapon_level(kills))
        camo = self.save.get("camo", "NONE")
        if camo != "NONE" and camo in earned_camos(self.save):
            spec["camo"] = camo                         # 업적 화면에서 고른 위장 무늬
        return spec

    def make_arsenal(self):
        """가진 무기를 모두 챙겨요 (인벤토리). 로드아웃의 시작 무기를 들고, 퍼크와 스킬도 적용해요."""
        specs, start, second = None, 0, 1
        if self.challenge == "PISTOL":
            specs = [self.weapon_spec("PISTOL")]
            start, second = 0, 0
        elif self.loadout:
            names = unlocked_weapons(self.save)
            specs = [self.weapon_spec(name) for name in names]
            start = names.index(self.loadout["primary"]) if self.loadout["primary"] in names else 0
            second = names.index(self.loadout["secondary"]) if self.loadout["secondary"] in names else 1 % len(names)
        reload_mult = (0.6 if self.perk == "QUICK HANDS" else 1.0) * (1 - 0.1 * self.rank_of("RELOAD MASTER"))
        ammo_mult = (1.5 if self.perk == "SCAVENGER" else 1.0) * (1 + 0.25 * self.rank_of("AMMO PACK"))
        arsenal = Arsenal(specs, reload_mult=reload_mult, ammo_mult=ammo_mult)
        arsenal.index, arsenal.last_index = start, second
        if self.perk == "SCAVENGER":
            arsenal.grenades += 2
        arsenal.grenades += self.rank_of("DEMOLITION")
        return arsenal

    def check_unlocks(self):
        """조건을 채운 무기를 얻어요. 얻는 순간 바로 들고 쓸 수 있어요."""
        if not self.loadout or self.mode == "training":
            return
        earned = self.save.setdefault("unlocked", [])
        for name, (kind, need) in UNLOCKS.items():
            if name in earned or kind == "level":
                continue
            if (kind == "score" and self.stats["score"] >= need) or (kind == "heads" and self.stats["heads"] >= need):
                earned.append(name)
                write_save(self.save)
        for name in unlocked_weapons(self.save):      # 계급 조건 무기도 여기서 손에 들어와요
            self.add_to_inventory(name)

    def add_to_inventory(self, name):
        if any(w.spec["name"] == name for w in self.arsenal.weapons):
            return
        self.arsenal.weapons.append(Weapon(self.weapon_spec(name), self.arsenal.ammo_mult))
        slot = len(self.arsenal.weapons)
        key = str(slot) if slot <= 9 else ("0" if slot == 10 else "TAB")
        self.popups.append([f"NEW WEAPON: {name}!  press {key}", (255, 200, 60), 3.5])
        self.sounds.play("streak")

    def refresh_weapon(self, name):
        """무기 레벨이 오르거나 부착물이 풀리면 들고 있는 그 무기에 바로 적용해요"""
        for w in self.arsenal.weapons:
            if w.spec["name"] == name and not w.upgraded:
                w.spec = self.weapon_spec(name)
                w.mag = min(w.mag, w.spec["mag"])

    def use_skill(self, name):
        """액티브 스킬 (T 집중 / Y 구급상자 / J 탐지)"""
        if not self.rank_of(name) or self.game_over:
            return
        if self.cooldowns.get(name, 0) > 0:
            self.popups.append([f"{name} READY IN {self.cooldowns[name]:.0f}s", WHITE, 1.0])
            return
        duration, cooldown = ACTIVE_SKILLS[name]
        self.cooldowns[name] = cooldown
        if name == "FOCUS":
            self.focus = duration
        elif name == "MEDKIT":
            self.player.hp = min(self.max_hp, self.player.hp + 60)
        elif name == "SCAN":
            self.scan = duration
            self.radar_timer = max(self.radar_timer, duration)
        self.popups.append([name + "!", (80, 240, 255), 1.2])
        self.sounds.play("heal" if name == "MEDKIT" else "streak")

    @property
    def skill(self):
        """적 실력: 캠페인은 라운드마다 1.5%씩 (100라운드에 약 250%, 최대 260%).
        좀비 모드는 웨이브마다 8%. 미션은 단계마다 10%. 난이도 설정에 따라 더 쉽거나 어렵게"""
        if self.mode == "campaign":
            base = 1 + 0.015 * (self.round - 1)
        elif self.mode == "mission":
            base = 1.2 + 0.1 * self.stage
        else:
            base = 1 + 0.08 * (self.round - 1)
        return min(2.6, base) * DIFFICULTIES[SETTINGS["difficulty"]][1]

    def pick_enemy_kind(self):
        """라운드가 올라갈수록 새로운 적이 섞여 나와요"""
        pool = ["GRUNT"] * 3 + ["RUSHER"] * 2
        if self.round >= 2:
            pool += ["SNIPER"] * 2
        if self.round >= 3:
            pool += ["HEAVY"] * 2
        if self.round >= 4:
            pool += ["BOMBER"] * 2
        if self.round >= 6:
            pool += ["SHIELD"] * 2
        if self.round >= 7:
            pool += ["FLANKER"] * 2
        if self.round >= 8:
            pool += ["MEDIC"]
        if self.round >= 9:
            pool += ["GUNNER"]
        if self.round >= 12:
            pool += ["DRONE"] * 2
        if self.round >= 14:
            pool += ["LASER"]
        return random.choice(pool)

    def start_round(self):
        if self.mode == "training":
            self.start_training()
        elif self.mode == "zombies":
            self.start_wave()
        elif self.mode == "mission":
            self.start_mission()
        elif self.challenge:
            self.start_challenge()
        else:
            self.start_battle()
        self.reset_round_state()
        if self.mode == "mission":
            self.banner_timer = 5.0

    def start_challenge(self):
        """도전 모드: 정해진 라운드 하나를 규칙대로 (목표 없이 적 모두 처치)"""
        name, round_no = next((c[0], c[1]) for c in CHALLENGES if c[0] == self.challenge)
        if name == "DAILY":
            seed = daily_seed()
            self.round = 6 + seed % 40
            random.seed(seed)                       # 오늘은 누구나 같은 맵, 같은 적
            self.start_battle()
            random.seed()
        else:
            self.round = round_no
            self.start_battle()
        self.objective = None
        self.challenge_time = 0.0
        self.challenge_done = False
        self.banner = f"CHALLENGE: {name}"
        info = next(c for c in CHALLENGES if c[0] == name)
        self.sub_banners = [(info[3], YELLOW), (f"{self.theme['name']}   ENEMIES {len(self.enemies)}", WHITE)]

    def finish_challenge(self):
        """도전 성공: 기록 저장 (오늘의 도전은 날짜별)"""
        self.challenge_done = True
        self.game_over = True
        t = round(self.challenge_time, 1)
        records = self.save.setdefault("challenges", {})
        if self.challenge == "DAILY":
            today = str(datetime.date.today())
            daily = self.save.get("daily", {})
            best = daily.get("best") if daily.get("date") == today else None
            self.challenge_best = min(t, best) if best else t
            self.save["daily"] = dict(date=today, best=self.challenge_best)
        else:
            self.challenge_best = min(t, records.get(self.challenge, t))
        records[self.challenge] = min(t, records.get(self.challenge, t))
        self.check_achievements()
        write_save(self.save)

    def start_training(self):
        """사격장: 움직이지 않는 과녁, 경험치/저장 없음, 단계별 연습 (화면 위 안내)"""
        index = CAMPAIGN_MAPS[0]
        if getattr(self, "map_key", None) != (index, 1):
            self.setup_map(index, 1)
        start = pygame.Vector2(find_cells("P")[0])
        self.player = Player(start.x, start.y)
        self.player.hp = self.max_hp
        self.arsenal = self.make_arsenal()
        # 과녁 자리: 나에게서 4~18칸, 곧장 보이는 곳
        cells = [pygame.Vector2(x + 0.5, y + 0.5) for y in range(MAP_H) for x in range(MAP_W)]
        self.target_spots = [c for c in cells if 4 < c.distance_to(start) < 18
                             and not is_blocked(c.x, c.y) and can_see(start, c)]
        self.enemies = []
        for _ in range(6):
            self.spawn_target()
        if self.enemies:
            middle = sum((e.pos for e in self.enemies), pygame.Vector2()) / len(self.enemies) - start
            self.player.angle = math.atan2(middle.y, middle.x)
        self.pickups = []
        self.objective = None
        self.zombies_left = 0
        self.target_timer = 0.0
        self.tutorial_step = 0
        self.keys_seen = set()
        self.start_angle = self.player.angle
        self.banner = "TRAINING RANGE"
        self.sub_banners = [("NO XP, NO SAVE - PRACTICE FREELY", WHITE), ("ESC: MENU", (200, 200, 255))]

    def spawn_target(self):
        free = [c for c in self.target_spots if all(c.distance_to(e.pos) > 1.5 for e in self.enemies)]
        if free:
            c = random.choice(free)
            self.enemies.append(Enemy(c.x, c.y, "TARGET", 1.0))

    def tutorial_steps(self):
        """사격장 안내: (한국어, 영어, 다 했는지 검사)"""
        k = key_label
        seen = self.keys_seen
        move = "/".join(k(bound_key(d)) for d in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d))
        return [
            (f"{move} 로 걸어 보세요", f"Walk with {move}", lambda: seen & {pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d}),
            ("화살표 ← → 로 둘러보세요", "Look around with the arrow keys",
             lambda: abs(self.player.angle - self.start_angle) > 0.3),
            (f"{k(bound_key(pygame.K_f))} 로 과녁을 쏘세요", f"Shoot a target with {k(bound_key(pygame.K_f))}",
             lambda: self.stats["hits"] > 0),
            (f"{k(bound_key(pygame.K_e))} 로 정조준하세요", f"Aim down sights with {k(bound_key(pygame.K_e))}",
             lambda: self.aiming),
            (f"{k(bound_key(pygame.K_r))} 로 재장전하세요", f"Reload with {k(bound_key(pygame.K_r))}",
             lambda: pygame.K_r in seen),
            (f"{k(bound_key(pygame.K_q))} 로 무기를 바꾸세요", f"Switch weapons with {k(bound_key(pygame.K_q))}",
             lambda: seen & {pygame.K_q, pygame.K_TAB, pygame.K_1, pygame.K_2, pygame.K_3}),
            (f"{k(bound_key(pygame.K_c))} 로 앉아 보세요", f"Crouch with {k(bound_key(pygame.K_c))}",
             lambda: pygame.K_c in seen),
            (f"{k(bound_key(pygame.K_SPACE))} 로 점프하세요", f"Jump with {k(bound_key(pygame.K_SPACE))}",
             lambda: pygame.K_SPACE in seen),
            (f"{k(bound_key(pygame.K_g))} 로 수류탄을 던지세요", f"Throw a grenade with {k(bound_key(pygame.K_g))}",
             lambda: pygame.K_g in seen),
            ("과녁 10개를 쓰러뜨리세요 (헤드샷을 노려 보세요)", "Knock down 10 targets (try headshots)",
             lambda: self.stats["kills"] >= 10),
        ]

    def update_training(self, dt):
        """사격장: 탄약은 끝없이, 쓰러진 과녁은 다시 서요, 안내 단계 넘기기"""
        for weapon in self.arsenal.weapons:
            weapon.reserve = max(weapon.reserve, weapon.spec["reserve"])
        self.arsenal.grenades = max(self.arsenal.grenades, 2)
        self.player.hp = self.max_hp
        self.target_timer -= dt
        if len(self.enemies) < 6 and self.target_timer <= 0:
            self.spawn_target()
            self.target_timer = 1.0
        for e in self.enemies:                       # 과녁은 언제나 나를 봐요
            offset = self.player.pos - e.pos
            if offset.length() > 0:
                e.dir = offset.normalize()
                e.facing = pygame.Vector2(e.dir)
        steps = self.tutorial_steps()
        if self.tutorial_step < len(steps) and steps[self.tutorial_step][2]():
            self.tutorial_step += 1
            self.sounds.play("streak" if self.tutorial_step == len(steps) else "beep")
            self.popups.append(["TRAINING COMPLETE!" if self.tutorial_step == len(steps) else "GOOD!",
                                (80, 255, 120), 1.5])

    def draw_compass(self, screen):
        """위쪽 가운데 나침반: N E S W 와 15도 눈금, 목표 위치(다이아몬드)"""
        width, top = WIDTH * 0.3, HEIGHT * 0.075
        left = WIDTH / 2 - width / 2
        span = math.radians(110)                     # 나침반에 보이는 범위
        panel = pygame.Surface((int(width), int(22 * UI)), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 90))
        screen.blit(panel, (left, top))
        heading = self.player.angle + math.pi / 2     # 맵 위쪽이 북쪽(N)
        names = {0: "N", 90: "E", 180: "S", 270: "W"}
        for deg in range(0, 360, 15):
            rel = angle_diff(math.radians(deg), heading)
            if abs(rel) > span / 2:
                continue
            x = WIDTH / 2 + rel / span * width
            if deg in names:
                label = self.small_font.render(names[deg], True, YELLOW if deg == 0 else WHITE)
                screen.blit(label, label.get_rect(center=(x, top + 11 * UI)))
            else:
                pygame.draw.line(screen, (200, 200, 210), (x, top + 6 * UI), (x, top + 16 * UI), 1)
        pygame.draw.line(screen, YELLOW, (WIDTH / 2, top - 2), (WIDTH / 2, top + 4 * UI), 2)
        if self.objective and not self.objective.get("done"):
            offset = self.objective["pos"] - self.player.pos
            rel = angle_diff(math.atan2(offset.y, offset.x), self.player.angle)
            x = WIDTH / 2 + max(-0.5, min(0.5, rel / span)) * width
            y = top + 11 * UI
            size = 6 * UI
            color = OBJECTIVES[self.objective["kind"]]["color"] if self.objective.get("kind") in OBJECTIVES else YELLOW
            pygame.draw.polygon(screen, color, [(x, y - size), (x + size, y), (x, y + size), (x - size, y)])

    def draw_training(self, screen):
        """사격장 안내판과 사격 기록"""
        ko = self.fonts["lang"] == "ko"
        steps = self.tutorial_steps()
        if self.tutorial_step < len(steps):
            text = steps[self.tutorial_step][0 if ko else 1]
            head = f"{self.tutorial_step + 1} / {len(steps)}   "
        else:
            text = "연습 끝! 마음껏 쏴 보세요. ESC → QUIT TO MENU" if ko else "Done! Shoot freely. ESC -> QUIT TO MENU"
            head = ""
        label = self.fonts["help_big" if "help_big" in self.fonts else "help"].render(head + text, True, YELLOW)
        rect = label.get_rect(midtop=(WIDTH / 2, HEIGHT * 0.13)).inflate(24 * UI, 12 * UI)
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel.fill((0, 0, 0, 160))
        screen.blit(panel, rect)
        screen.blit(label, label.get_rect(center=rect.center))
        st = self.stats
        accuracy = 100 * st["hits"] / st["shots"] if st["shots"] else 0
        info = f"SHOTS {st['shots']}   HITS {st['hits']}   ACCURACY {accuracy:.0f}%   HEADSHOTS {st['heads']}   TARGETS {st['kills']}"
        label = self.fonts["small"].render(info, True, WHITE)
        screen.blit(label, label.get_rect(midtop=(WIDTH / 2, rect.bottom + 6 * UI)))

    def start_mission(self):
        """장기 미션 시작 (또는 저장된 단계부터 이어하기). 맵 곳곳에 적이 배치돼 있어요."""
        m = MISSIONS[self.mission]
        if self.map_index != m["map"]:
            self.setup_map(m["map"])
        self.stage_points = self.mission_points()
        start = pygame.Vector2(find_cells("P")[0])
        if self.stage > 0:                                # 체크포인트: 앞 단계 목표 자리에서 시작
            start = pygame.Vector2(self.stage_points[self.stage - 1][0])
        self.checkpoint = start
        self.player = Player(start.x, start.y)
        self.player.hp = self.max_hp
        self.arsenal = self.make_arsenal()
        rng = random.Random(m["seed"] * 7 + self.stage)
        self.enemies = [Enemy(x, y, self.mission_enemy_kind(rng), self.skill)
                        for x, y in self.spawn_points if pygame.Vector2(x, y).distance_to(start) > 10]
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items() for x, y in find_cells(letter)]
        self.zombies_left = 0
        self.mission_complete = False
        self.banner = f"MISSION: {m['name']}"
        self.sub_banners = []
        self.set_stage_objective()
        self.face_objective()

    def face_objective(self):
        """목표 쪽을 바라보게 (시작, 이어하기, 체크포인트 부활)"""
        offset = self.objective["pos"] - self.player.pos
        if offset.length() > 0:
            self.player.angle = math.atan2(offset.y, offset.x)

    @staticmethod
    def mission_enemy_kind(rng):
        kinds = ["GRUNT"] * 4 + ["RUSHER", "RUSHER", "SNIPER", "SNIPER", "HEAVY", "BOMBER", "SHIELD",
                                 "FLANKER", "MEDIC", "GUNNER", "DRONE", "LASER"]
        return rng.choice(kinds)

    def mission_points(self):
        """단계마다 목표 자리: 시작에서 걸어서 먼 순서로 차례차례 (같은 미션이면 늘 같은 자리)"""
        start = tuple(int(v) for v in find_cells("P")[0])
        dist = {start: 0}
        queue = deque([start])
        while queue:
            col, row = queue.popleft()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                cell = (col + dc, row + dr)
                if cell not in dist and in_map(*cell) and not is_blocked(cell[0] + 0.5, cell[1] + 0.5):
                    dist[cell] = dist[(col, row)] + 1
                    queue.append(cell)
        cells = sorted((c for c in dist if GAME_MAP[c[1]][c[0]] in FLOORS), key=lambda c: dist[c])
        rng = random.Random(MISSIONS[self.mission]["seed"])

        def at(fraction, avoid=()):
            for k in range(200):
                c = cells[min(len(cells) - 1, int(len(cells) * fraction) + rng.randint(-30, 30))]
                if all(math.dist(c, a) > 6 for a in avoid):
                    return c
            return cells[int(len(cells) * fraction)]

        center = lambda c: (c[0] + 0.5, c[1] + 0.5)
        caches = []
        for f in (0.55, 0.65, 0.75):
            caches.append(at(f, caches))
        return [[center(at(0.22))], [center(at(0.42))], [center(c) for c in caches],
                [center(at(0.86))], [center(cells[-1])]]

    def set_stage_objective(self):
        kind, title = MISSION_STAGES[self.stage]
        points = list(self.stage_points[self.stage])
        self.objective = dict(kind=kind, pos=pygame.Vector2(points[0]), points=points, progress=0.0, done=False,
                              timer=BOMB_TIME, spawn=7.0, beep=0.0, title=title)
        self.sub_banners = [(f"STAGE {self.stage + 1} / {len(MISSION_STAGES)}:  {title}", OBJECTIVES[kind]["color"])]
        self.banner_timer = 4.0

    def advance_stage(self):
        """미션 단계 완료: 체크포인트 저장, 다음 목표 근처에 적 지원군"""
        self.stage += 1
        self.checkpoint = pygame.Vector2(self.player.pos)
        if self.stage >= len(MISSION_STAGES):
            self.mission_complete = True
            self.game_over = True
            self.save.pop("mission", None)
            done = self.save.setdefault("missions_done", [])
            if MISSIONS[self.mission]["name"] not in done:
                done.append(MISSIONS[self.mission]["name"])
            self.add_xp(2000, "MISSION COMPLETE  +2000", (80, 240, 255))
            write_save(self.save)
            return
        self.save["mission"] = dict(id=self.mission, stage=self.stage)
        write_save(self.save)
        self.popups.append(["CHECKPOINT SAVED", (80, 240, 255), 2.0])
        self.set_stage_objective()
        target = self.objective["pos"]
        near = [pt for pt in self.spawn_points if 4 < pygame.Vector2(pt).distance_to(target) < 12
                and pygame.Vector2(pt).distance_to(self.player.pos) > 8]
        for x, y in random.sample(near, min(4, len(near))):
            self.enemies.append(Enemy(x, y, self.mission_enemy_kind(random), self.skill))

    def respawn_checkpoint(self):
        """미션에서 죽으면: 마지막 체크포인트에서 다시 (쓰러뜨린 적은 그대로)"""
        self.game_over = False
        self.fail_reason = ""
        self.killcam_from = None
        self.player = Player(self.checkpoint.x, self.checkpoint.y)
        self.player.hp = self.max_hp
        self.arsenal = self.make_arsenal()
        self.enemies = [e for e in self.enemies if e.pos.distance_to(self.checkpoint) > 7]
        if self.objective:
            self.objective["progress"] = 0.0
            self.face_objective()
        self.reset_streak()
        self.reset_round_state()
        self.banner_timer = 0.0

    def start_wave(self):
        """좀비 웨이브: 1웨이브에서만 새로 시작하고, 다음 웨이브는 체력과 무기를 그대로 이어가요."""
        if self.map_index != ZOMBIE_MAP:
            self.setup_map(ZOMBIE_MAP)
        if self.round == 1 or not hasattr(self, "arsenal"):
            self.player = Player(*find_cells("P")[0])
            self.player.hp = self.max_hp
            self.arsenal = self.make_arsenal()
        else:
            self.arsenal.grenades = min(GRENADES_MAX, self.arsenal.grenades + 1)
        self.enemies = []
        self.zombies_left = 5 + self.round * 3     # 이번 웨이브에 나올 좀비 수
        self.spawn_timer = 2.5
        self.flow_timer = 0.0
        self.brute_due = self.round % 5 == 0       # 5웨이브마다 거대 좀비
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items()
                        for x, y in find_cells(letter)]
        self.banner = f"WAVE {self.round}"
        self.sub_banners = [(f"{self.zombies_left} ZOMBIES", RED)]
        if self.brute_due:
            self.sub_banners.append(("BRUTE INCOMING!", (255, 120, 40)))

    def start_battle(self):
        set_no = set_of(self.round)
        index = CAMPAIGN_MAPS[(self.round - 1) % len(CAMPAIGN_MAPS)]
        if (index, set_no) != getattr(self, "map_key", None):
            self.setup_map(index, set_no)
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.player.hp = self.max_hp
        self.arsenal = self.make_arsenal()
        far = [p for p in self.spawn_points if self.player.pos.distance_to(p) > SAFE_SPAWN]
        in_set = (self.round - 1) % SET_SIZE
        count = min(len(far), 3 + in_set // 4 + set_no - 1)
        self.enemies = [Enemy(*p, self.pick_enemy_kind(), self.skill) for p in random.sample(far, count)]
        # 새로운 적이 처음 나오는 라운드에는 그 적이 꼭 한 명은 있게. 5라운드마다 보스
        news = {2: "SNIPER", 3: "HEAVY", 4: "BOMBER", 6: "SHIELD", 7: "FLANKER", 8: "MEDIC", 9: "GUNNER",
                12: "DRONE", 14: "LASER"}
        special = "BOSS" if self.round % 10 == 0 else news.get(self.round)
        if special:
            first = self.enemies[0]
            self.enemies[0] = Enemy(first.pos.x, first.pos.y, special, self.skill)
        # 맵에 놓인 상자는 라운드마다 다시 채워져요
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items()
                        for x, y in find_cells(letter)]
        self.zombies_left = 0
        self.banner = f"ROUND {self.round}" + (f" / {CAMPAIGN_ROUNDS}" if self.round <= CAMPAIGN_ROUNDS else "")
        self.sub_banners = [(f"{self.theme['op']}  -  {self.theme['name']}", WHITE),
                            (f"SET {set_no}: {SETS[set_no - 1]}   ROUND {in_set + 1} / {SET_SIZE} OF THE SET", (200, 200, 255))]
        if special == "BOSS":
            self.sub_banners.append(("BOSS ROUND!", RED))
        elif special:
            self.sub_banners.append((f"NEW ENEMY: {special}", RED))
        if self.round > 1:
            self.sub_banners.append((f"ENEMY SKILL {self.skill * 100:.0f}%", (255, 160, 60)))
        # 라운드 목표
        kind = None if special == "BOSS" or self.round % 5 == 1 else OBJECTIVE_ORDER.get(self.round % 5)
        self.objective = None
        if kind and self.round > 1:
            self.objective = dict(kind=kind, pos=self.far_spot(), progress=0.0, done=False,
                                  timer=BOMB_TIME, spawn=7.0, beep=0.0)
            self.sub_banners.insert(1, (f"OBJECTIVE: {OBJECTIVES[kind]['title']}", OBJECTIVES[kind]["color"]))

    def reset_round_state(self):
        """라운드(웨이브)마다 새로 시작하는 것들"""
        self.contact_timer = 0.0       # 적이 나를 보고 있었던 뒤로 지난 시간 (CONTACT! 외침용)
        self.callout_cooldown = 0.0
        self.squad_timer = 0.0
        self.last_known = None
        self.projectiles = []
        self.effects = []
        self.tracers = []          # 내 총알 궤적: [x0, y0, x1, y1, 남은 시간]
        self.camp_pos = pygame.Vector2(self.player.pos)   # 한자리에 오래 있으면 적이 수류탄을 던져요
        self.stats = dict(shots=0, hits=0, heads=0, kills=0, best=0, weapons={}, score=0)   # 라운드 결과 화면용
        self.camp_timer = 0.0
        self.camp_nade = 5.0
        self.enemy_tracers = []    # 적 총알 궤적: [적, 남은 시간, 끝점 흔들림]
        self.pending_blasts = []   # 총에 맞아 터질 좀비 위치
        self.brief_age = 0.0       # 임무 설명이 타자 치듯 나와요
        self.banner_timer = 4.0
        self.round_clear_timer = 0.0
        self.damage_flash = 0.0
        self.hitmarker = 0.0
        self.hitmarker_kill = False
        self.aiming = False
        self.shake = 0.0
        self.shake_offset = 0.0
        self.knife_timer = 0.0     # 칼 휘두르는 중이면 0보다 커요
        self.knife_cooldown = 0.0
        self.feed = []             # 킬 로그: [글자, 남은 시간]
        self.seen_index = self.arsenal.index
        self.popups = []           # 점수/메달 글자: [글자, 색, 남은 시간]
        self.damage_dirs = []      # 맞은 방향 표시: [방향(각도), 남은 시간]
        self.puff_cache = {}
        self.smoke = []            # 총구 연기: [x, y (총구에서 떨어진 거리), 속도 x, 속도 y, 남은 시간, 크기]
        self.bolt_anim = 0.0       # 저격총 노리쇠 당기는 동작 남은 시간
        self.inspect_timer = 0.0   # 무기 살펴보기 (I) 남은 시간
        self.ads_anim = 0.0        # 정조준 들어가고 나올 때 총이 살짝 내려갔다 오는 동작
        self.was_aiming = False
        self.sound_marks = []      # 소리 표시 (설정 SOUND MARKS): [방향, "step"/"shot", 남은 시간]
        self.radar_timer = 0.0
        self.airstrikes = []       # 떨어질 폭탄: [위치, 남은 시간]
        self.sentries = []
        self.sprint_recover = 0.0
        self.burst_left = 0        # 점사에서 아직 안 나간 발 수
        self.burst_timer = 0.0
        self.time = 0.0            # 라운드 시작부터 흐른 시간 (연속 처치 계산용)
        self.particles = []        # 화면에 튀는 피와 탄피: [x, y, vx, vy, 남은 시간, 크기, 색, 탄피인지]
        self.corpses = []
        self.splats = []           # 피 웅덩이: [위치, 크기]
        self.since_hurt = 99.0     # 마지막으로 맞은 뒤 흐른 시간 (체력 회복용)
        self.heart_timer = 0.0
        self.light_timer = 0.0     # 총구 섬광
        self.hit_head = False      # 히트마커를 크게 (헤드샷)
        self.last_kill = -99.0
        self.multi = 0

    def start_killcam(self):
        """죽었어요: 나를 쓰러뜨린 적의 자리에서 쓰러진 나를 보여줘요"""
        killer = self.last_attacker if self.last_attacker in self.enemies else None
        source = killer.pos if killer else self.last_source
        self.killcam_time = 0.0
        self.killcam_from = pygame.Vector2(source) if source is not None else None
        self.killcam_killer = killer.kind if killer else ("BOMB" if self.fail_reason else "EXPLOSION")
        if self.killcam_from is not None and self.killcam_from.distance_to(self.player.pos) < 0.3:
            self.killcam_from = None                     # 너무 가까우면(내 수류탄 등) 킬캠 없이
        body = Corpse(type("Body", (), dict(pos=self.player.pos, kind="PLAYER"))(), pygame.Vector2(0, 0))
        body.age = 1.0                                   # 이미 쓰러진 모습
        self.corpses.append(body)

    def draw_killcam(self, screen):
        """킬캠: 나를 쓰러뜨린 적의 눈으로 천천히 확대해 보여줘요"""
        real = self.player
        camera = Player(self.killcam_from.x, self.killcam_from.y)
        offset = real.pos - self.killcam_from
        camera.angle = math.atan2(offset.y, offset.x) if offset.length() > 0 else real.angle
        self.player = camera
        self.killcam_zoom = 1 + 1.6 * min(1.0, self.killcam_time / 2.2)
        try:
            self.draw_sky(screen)
            self.draw_world(screen)
            self.draw_sprites(screen)
            self.draw_particles(screen, casings=False)
        finally:
            self.player = real
            self.killcam_zoom = None
        band = pygame.Surface((WIDTH, int(70 * UI)), pygame.SRCALPHA)
        band.fill((0, 0, 0, 170))
        screen.blit(band, (0, 0))
        screen.blit(band, (0, HEIGHT - band.get_height()))
        pygame.draw.rect(screen, RED, (0, 0, WIDTH, HEIGHT), max(3, int(5 * UI)))
        self.center_text(screen, self.big_font, "KILLCAM", RED, 36 * UI)
        dist = offset.length()
        self.center_text(screen, self.font, f"Killed by {self.killcam_killer}   {dist:.0f}m away",
                         WHITE, HEIGHT - 36 * UI)

    def far_spot(self):
        """시작 위치에서 걸어서 가장 먼 빈칸 (목표를 놓을 곳)"""
        start = (int(self.player.pos.x), int(self.player.pos.y))
        dist = {start: 0}
        queue = deque([start])
        while queue:
            col, row = queue.popleft()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                cell = (col + dc, row + dr)
                if cell not in dist and in_map(*cell) and not is_blocked(cell[0] + 0.5, cell[1] + 0.5):
                    dist[cell] = dist[(col, row)] + 1
                    queue.append(cell)
        good = [c for c in dist if GAME_MAP[c[1]][c[0]] not in "EP" + "".join(PICKUP_TILES)]
        best = max(dist[c] for c in good)
        col, row = random.choice([c for c in good if dist[c] >= best - 2])
        return pygame.Vector2(col + 0.5, row + 0.5)

    def update_objective(self, dt):
        """목표: 가까이 있으면 진행이 차요. 폭탄은 시간이 다 되면 터져요. 거점은 적 지원군이 와요."""
        o = self.objective
        if not o or o["done"]:
            return
        info = OBJECTIVES[o["kind"]]
        inside = self.player.pos.distance_to(o["pos"]) < info["radius"]
        if inside:
            o["progress"] += dt
        elif o["kind"] != "HOLD":
            o["progress"] = max(0.0, o["progress"] - dt * 0.5)    # 자리를 뜨면 조금씩 줄어요
        if o["kind"] == "BOMB":
            o["timer"] -= dt
            o["beep"] -= dt
            if o["beep"] <= 0:                                  # 시간이 줄수록 빨리 삑삑
                o["beep"] = 0.25 if o["timer"] < 10 else (0.5 if o["timer"] < 25 else 1.0)
                self.play_at("beep", o["pos"], 20, 1.0)
            if o["timer"] <= 0 and o["progress"] < info["need"]:
                o["done"] = True
                self.effects.append(Effect(o["pos"], self.explosion_frames, 1.0, 6.0))
                self.sounds.play("explosion", 1.0)
                self.shake = 1.0
                self.fail_reason = "BOMB DETONATED"
                self.player.hp = 0
                return
        if o["kind"] == "HOLD":                                # 지원군
            o["spawn"] -= dt
            close = sum(1 for e in self.enemies if e.pos.distance_to(o["pos"]) < 15)
            if o["spawn"] <= 0 and close < 6:
                o["spawn"] = 7.0
                far = [pt for pt in self.spawn_points if self.player.pos.distance_to(pt) > SAFE_SPAWN]
                if far:
                    x, y = random.choice(far)
                    self.enemies.append(Enemy(x, y, self.pick_enemy_kind(), self.skill))
        if o["progress"] >= info["need"] and o["kind"] == "CACHE" and len(o["points"]) > 1:
            # 캐시 하나 폭파! 다음 캐시로
            self.explode(pygame.Vector2(o["points"].pop(0)), 2.6, 200, owner="streak")
            o["pos"], o["progress"] = pygame.Vector2(o["points"][0]), 0.0
            self.popups.append([f"CACHE DESTROYED  ({3 - len(o['points'])}/3)", (255, 140, 40), 2.0])
            return
        if o["progress"] >= info["need"]:
            o["done"] = True
            if o["kind"] == "CACHE":
                self.explode(pygame.Vector2(o["pos"]), 2.6, 200, owner="streak")
            done_text = {"HOSTAGE": "HOSTAGE RESCUED", "BOMB": "BOMB DEFUSED", "HOLD": "POINT SECURED",
                         "REACH": "ARRIVED", "CACHE": "ALL CACHES DESTROYED"}[o["kind"]]
            self.popups.append([f"{done_text}  +{XP['round']}", (80, 240, 255), 2.5])
            self.add_xp(XP["round"])
            self.sounds.play("streak")
            if self.mode == "mission":
                self.advance_stage()

    def update_boss(self, boss, dt):
        """보스 패턴: 체력 60% 아래 → 화가 나서 빨라지고 돌진, 30% 아래 → 부하를 부르고 연막"""
        ratio = boss.hp / boss.t["hp"]
        phase = getattr(boss, "phase", 1)
        if phase == 1 and ratio < 0.6:
            boss.phase = 2
            boss.t = dict(boss.t, speed=boss.t["speed"] * 1.5, fire=(boss.t["fire"][0] * 0.8, boss.t["fire"][1] * 0.8))
            boss.charge_timer = 2.0
            self.popups.append(["BOSS ENRAGED!", RED, 2.0])
            self.shout(boss, "YOU'RE MINE!")
            self.sounds.play("streak")
        elif phase == 2 and ratio < 0.3:
            boss.phase = 3
            self.popups.append(["BOSS CALLS BACKUP!", RED, 2.0])
            self.callout_cooldown = 0.0
            self.shout(boss, "BACKUP! NOW!")
            spots = [pygame.Vector2(boss.pos.x + dx, boss.pos.y + dy) for dx in (-2, -1, 1, 2) for dy in (-2, -1, 1, 2)]
            spots = [q for q in spots if not is_blocked(q.x, q.y) and can_see(boss.pos, q)]
            for q in random.sample(spots, min(3, len(spots))):
                guard = Enemy(q.x, q.y, "GRUNT", self.skill)
                guard.search = pygame.Vector2(self.player.pos)
                self.enemies.append(guard)
            for k in range(5):                                   # 연막: 보스 둘레에 빨간 연기
                spot = boss.pos + pygame.Vector2(1.2, 0).rotate(k * 72)
                self.effects.append(Effect(spot, self.flare_frames, 4.0, 1.6))
        if getattr(boss, "phase", 1) >= 2 and boss.sees:        # 돌진: 6초마다 1.2초 동안 나에게 달려와요
            boss.charge_timer = getattr(boss, "charge_timer", 2.0) - dt
            if -1.2 < boss.charge_timer <= 0:
                offset = self.player.pos - boss.pos
                if offset.length() > 1.5:
                    move_with_collision(boss.pos, offset.normalize() * boss.t["speed"] * 1.8 * dt)
            elif boss.charge_timer <= -1.2:
                boss.charge_timer = 6.0

    def update_squad(self, dt):
        """분대 AI: 한 명이 나를 보면 무전으로 동료에게 알리고, 여럿이면 제압조와 측면조로 나눠요"""
        p = self.player
        soldiers = [e for e in self.enemies if "melee" not in e.t]
        seers = [e for e in soldiers if e.sees]
        self.callout_cooldown -= dt
        for e in self.enemies:
            if e.callout:
                e.callout[1] -= dt
                if e.callout[1] <= 0:
                    e.callout = None
        if seers:
            if self.contact_timer <= 0:
                self.shout(seers[0], "CONTACT!")
            self.contact_timer = 6.0
            self.last_known = pygame.Vector2(p.pos)
            for e in soldiers:                       # 무전: 가까운 동료가 내 위치로 와요
                if not e.sees and e.search is None and e.role != "flank" and e.pos.distance_to(seers[0].pos) < 11:
                    e.search = pygame.Vector2(self.last_known)
        else:
            self.contact_timer -= dt
        for e in soldiers:
            if e.shout:
                self.shout(e, e.shout)
                e.shout = None
        self.squad_timer -= dt
        if self.squad_timer > 0 or len(seers) < 2 or self.mode == "zombies":
            return
        self.squad_timer = 1.0
        # 제압조: 가장 멀리서 보고 있는 적 한 명이 자주 쏴서 나를 묶어 둬요
        if not any(e.role == "suppress" for e in soldiers):
            gunners = [e for e in seers if e.kind not in ("SNIPER",) and e.role is None]
            if gunners:
                e = max(gunners, key=lambda e: e.pos.distance_to(p.pos))
                e.role, e.role_timer = "suppress", 6.0
                self.shout(e, "SUPPRESSING!")
                self.squad_timer = 1.8              # 측면조는 조금 뒤에 (외침이 겹치지 않게)
                return
        # 측면조: 다른 한 명이 내 옆으로 돌아 들어와요
        if len(seers) >= 2 and not any(e.role == "flank" for e in soldiers):
            movers = [e for e in soldiers if e.role is None and e.kind not in ("SNIPER", "HEAVY", "BOSS", "GUNNER")
                      and e.mode == "fight" and e.pos.distance_to(p.pos) > 3]
            for e in sorted(movers, key=lambda e: e.pos.distance_to(p.pos)):
                to_me = p.pos - e.pos
                if to_me.length() == 0:
                    continue
                side = pygame.Vector2(-to_me.y, to_me.x).normalize()
                for sign in random.sample((1, -1), 2):
                    spot = p.pos + side * sign * 4 - to_me.normalize() * 1.5
                    if in_map(int(spot.x), int(spot.y)) and not is_blocked(spot.x, spot.y):
                        e.role, e.role_timer, e.flank_spot = "flank", 6.0, spot
                        self.shout(e, "FLANKING!")
                        return

    def shout(self, enemy, text):
        """적의 외침: 머리 위 말풍선 + 무전 소리 (너무 자주는 안 해요)"""
        if self.callout_cooldown > 0 or enemy.pos.distance_to(self.player.pos) > 20:
            return
        self.callout_cooldown = 1.6
        enemy.callout = [text, 1.4]
        self.play_at("radio", enemy.pos, 18, 0.8)

    def punish_camping(self, dt):
        """한자리에 7초 넘게 숨어 있으면, 나를 보는 적이 수류탄을 던져요"""
        p = self.player.pos
        if p.distance_to(self.camp_pos) > 1.2:
            self.camp_pos, self.camp_timer = pygame.Vector2(p), 0.0
        self.camp_timer += dt
        self.camp_nade -= dt
        if self.camp_timer > 7 and self.camp_nade <= 0:
            throwers = [e for e in self.enemies if e.sees and 3 < e.pos.distance_to(p) < 12 and "melee" not in e.t]
            if throwers:
                random.choice(throwers).throw_at = pygame.Vector2(p)
                self.camp_nade = 9.0

    def update_flow(self):
        """좀비 길찾기 지도: 플레이어 칸에서 시작해 걸어갈 수 있는 칸마다 걸음 수를 적어요 (너비 우선 탐색)"""
        start = (int(self.player.pos.x), int(self.player.pos.y))
        flow = [[None] * MAP_W for _ in range(MAP_H)]
        flow[start[1]][start[0]] = 0
        queue = deque([start])
        while queue:
            col, row = queue.popleft()
            d = flow[row][col] + 1
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                c, r = col + dc, row + dr
                if in_map(c, r) and flow[r][c] is None and not is_blocked(c + 0.5, r + 0.5):
                    flow[r][c] = d
                    queue.append((c, r))
        Enemy.flow = flow

    def spawn_zombie(self):
        """내가 안 보는 먼 곳에서 좀비가 나와요"""
        p = self.player.pos
        spots = [pt for pt in self.spawn_points
                 if p.distance_to(pt) > 6 and not can_see(p, pygame.Vector2(pt))]
        if not spots:
            spots = sorted(self.spawn_points, key=lambda pt: -p.distance_to(pt))[:3]
        x, y = random.choice(spots)
        if self.brute_due:
            kind, self.brute_due = "BRUTE", False
        elif self.round >= 6 and random.random() < 0.05:
            kind = "BRUTE"
        elif self.round >= 4 and random.random() < 0.1:
            kind = "EXPLODER"
        elif self.round >= 5 and random.random() < 0.12:
            kind = "SPITTER"
        elif self.round >= 3 and random.random() < min(0.45, 0.08 * self.round):
            kind = "RUNNER"
        else:
            kind = "ZOMBIE"
        skill = min(3.0, 1 + 0.12 * (self.round - 1))
        self.enemies.append(Enemy(x, y, kind, skill))
        self.zombies_left -= 1

    def update_zombies(self, dt):
        """좀비 모드: 길찾기 지도 갱신, 좀비 나오기, 서로 겹치지 않게 밀기, 그르렁 소리"""
        self.flow_timer -= dt
        if self.flow_timer <= 0:
            self.flow_timer = 0.3
            self.update_flow()
        cap = min(24, 6 + self.round * 2)          # 한 번에 나와 있는 좀비 수 한도
        if self.zombies_left > 0 and len(self.enemies) < cap:
            self.spawn_timer -= dt
            if self.spawn_timer <= 0:
                self.spawn_timer = max(0.35, 1.6 - self.round * 0.08)
                self.spawn_zombie()
        for i, a in enumerate(self.enemies):
            for b in self.enemies[i + 1:]:
                offset = a.pos - b.pos
                d = offset.length()
                if 0 < d < 0.45:
                    push = offset.normalize() * (0.45 - d) * 0.5
                    move_with_collision(a.pos, push)
                    move_with_collision(b.pos, -push)
            offset = a.pos - self.player.pos              # 내 몸 안으로는 못 들어와요
            if 0 < offset.length() < 0.5:
                move_with_collision(a.pos, offset.normalize() * (0.5 - offset.length()))
            a.groan_timer -= dt
            if a.groan_timer <= 0:
                a.groan_timer = random.uniform(3, 7)
                self.play_at("groan", a.pos, 14, 0.8)

    def buy(self, item):
        """좀비 모드 상점: B 탄약 가득 / U 들고 있는 총 강화 (피해 1.6배, 탄창 1.5배)"""
        cost = ZOMBIE_SHOP[item]
        w = self.arsenal.current
        if self.points < cost:
            self.popups.append([f"NEED {cost} POINTS", RED, 1.2])
            return
        if item == "ammo":
            for weapon in self.arsenal.weapons:
                weapon.reserve = int(weapon.spec["reserve"] * 2 * self.arsenal.ammo_mult)
                weapon.mag = weapon.spec["mag"]
            self.popups.append(["MAX AMMO!", (80, 240, 255), 1.5])
        else:
            if w.upgraded or w.spec["projectile"]:
                self.popups.append(["CAN'T UPGRADE THIS", RED, 1.2])
                return
            spec = dict(w.spec, body=w.spec["body"] * 1.6, head=w.spec["head"] * 1.6,
                        mag=int(w.spec["mag"] * 1.5), reserve=int(w.spec["reserve"] * 1.5))
            w.spec, w.mag, w.upgraded = spec, spec["mag"], True
            self.popups.append([f"{spec['name']} UPGRADED!", (255, 200, 60), 2.0])
        self.points -= cost
        self.sounds.play("cash")

    @property
    def rank(self):
        return 1 + self.xp // XP_PER_RANK

    def add_xp(self, amount, text=None, color=YELLOW):
        """경험치 추가. 계급이 오르면 크게 알려줘요."""
        if self.mode == "training":
            return                                   # 사격장: 경험치 없음
        before = self.rank
        self.xp += amount
        self.save["xp"] = self.xp
        self.stats["score"] = self.stats.get("score", 0) + amount
        if text:
            self.popups.append([text, color, 1.4])
        if self.rank > before:
            self.popups.append([f"RANK UP!  RANK {self.rank}  (+1 SKILL POINT)", (255, 80, 200), 2.5])
            self.check_unlocks()

    def record_progress(self, next_round):
        """저장: 다음에 이어할 라운드와 최고 기록"""
        self.save["continue"] = next_round
        self.save["best"] = max(self.save.get("best", 1), self.round)
        write_save(self.save)

    # ----- 시점 계산 -----
    @property
    def scoped(self):
        """저격총 조준경을 보고 있는지"""
        return self.aiming and self.arsenal.current.spec["scope"]

    @property
    def zoom(self):
        if self.killcam_zoom:
            return self.killcam_zoom
        if not self.aiming:
            return 1
        spec = self.arsenal.current.spec
        return SCOPE_ZOOMS[self.arsenal.zoom_index] if spec["scope"] else spec["ads"]

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
        return HEIGHT / 2 + (self.player.pitch + self.arsenal.recoil) * self.zoom + self.shake_offset

    @property
    def eye(self):
        """눈높이. 점프하면 높아지고 앉으면 낮아져요."""
        return EYE + self.player.z - CROUCH_DROP * self.player.crouch_amt

    @property
    def fog_dist(self):
        # 조준경으로 보면 안개가 걷혀서 멀리까지 선명해요. 숲은 안개가 짙어요
        return FOG_DIST * self.theme["fog"] * min(4, self.zoom)

    def aim_slope(self):
        """조준점(화면 가운데)이 가리키는 위아래 기울기 (수류탄/로켓 방향 계산용)"""
        normal_proj = (WIDTH / 2) / math.tan(NORMAL_FOV / 2)
        return (self.player.pitch + self.arsenal.recoil) / normal_proj

    # ----- 입력 -----
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.mode == "training":
            self.keys_seen.add(event.key)
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_F3):
            self.show_fps = not self.show_fps
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h and not self.game_over:
            self.show_help = not self.show_help
        if self.game_over or self.show_help:
            return
        a = self.arsenal
        # 마우스 클릭은 '눌렀다' 신호로도 받아요. 맥 트랙패드를 톡 치면 누름과 뗌이
        # 한순간에 지나가서, 지금 눌려 있는지만 보면 클릭을 놓쳐요.
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.click_queued = True
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:   # 오른쪽 클릭 = E (정조준 켜기/끄기)
            self.aim_on = not self.aim_on
        if event.type == pygame.MOUSEWHEEL:
            if self.scoped:      # 조준경을 보고 있으면 휠로 확대/축소
                a.zoom_index = max(0, min(len(SCOPE_ZOOMS) - 1, a.zoom_index + event.y))
            else:
                a.switch(a.index - event.y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:            # 소리 끄기/켜기
                self.sounds.muted = not self.sounds.muted
                self.sounds.refresh_background()
                self.popups.append(["SOUND OFF" if self.sounds.muted else "SOUND ON", WHITE, 1.0])
            elif pygame.K_1 <= event.key <= pygame.K_9 and event.key - pygame.K_1 < len(a.weapons):
                a.switch(event.key - pygame.K_1)
            elif event.key == pygame.K_0 and len(a.weapons) >= 10:
                a.switch(9)
            elif event.key == pygame.K_TAB:          # 다음 무기
                a.switch(a.index + 1)
            elif event.key == pygame.K_t:
                self.use_skill("FOCUS")
            elif event.key == pygame.K_y:
                self.use_skill("MEDKIT")
            elif event.key == pygame.K_j:
                self.use_skill("SCAN")
            elif event.key == pygame.K_q:
                a.switch(a.last_index)
            elif event.key == pygame.K_r:
                a.reload()
            elif event.key == pygame.K_i and not a.busy and not self.aiming:   # 무기 살펴보기
                self.inspect_timer = 2.4
            elif event.key == pygame.K_e:      # 정조준 켜기/끄기
                self.aim_on = not self.aim_on
            elif event.key == pygame.K_z:      # 배율 바꾸기 3 -> 6 -> 12 -> 3
                a.zoom_index = (a.zoom_index + 1) % len(SCOPE_ZOOMS)
            elif event.key == pygame.K_g:
                self.throw_grenade()
            elif event.key == pygame.K_v:
                self.knife_attack()
            elif event.key == pygame.K_c:
                self.player.toggle_crouch()
            elif event.key == pygame.K_x:
                self.use_streak()
            elif event.key == pygame.K_b and self.mode == "zombies":
                self.buy("ammo")
            elif event.key == pygame.K_u and self.mode == "zombies":
                self.buy("upgrade")

    # ----- 게임 진행 -----
    def update(self, dt, keys, mouse_dx, mouse_dy, buttons):
        if self.show_help:          # 도움말을 보는 동안은 멈춰요
            return
        waiting = []
        for item in self.echoes:    # 메아리, 탄피 소리
            item[0] -= dt
            if item[0] <= 0:
                self.sounds.play(item[1], item[2])
            else:
                waiting.append(item)
        self.echoes = waiting
        self.screen_blood = [[x, y, r, t - dt] for x, y, r, t in self.screen_blood if t - dt > 0]
        self.lightning = max(0.0, self.lightning - dt)
        if self.theme.get("rain"):                 # 폭풍우: 가끔 번개가 번쩍, 조금 뒤 천둥
            self.lightning_timer -= dt
            if self.lightning_timer <= 0:
                self.lightning_timer = random.uniform(8, 16)
                self.lightning = 0.3
                self.echoes.append([random.uniform(0.4, 1.5), "thunder", random.uniform(0.6, 1.0)])
        self.suppress = max(0.0, self.suppress - dt * 0.8)
        if self.hitstop > 0:        # 쓰러뜨린 순간: 아주 잠깐 멈춤 (묵직한 손맛)
            self.hitstop -= dt
            return
        if self.slowmo > 0:         # 마지막 적: 잠깐 슬로모션
            self.slowmo -= dt
            dt *= 0.35
        self.banner_timer -= dt
        self.brief_age += dt
        self.hint_timer -= dt
        self.damage_flash = max(0.0, self.damage_flash - dt * 2)
        self.hitmarker = max(0.0, self.hitmarker - dt)
        self.shake = max(0.0, self.shake - dt)
        # 폭발 흔들림: 이번 장면에서 화면이 위아래로 움직일 양
        self.shake_offset = random.uniform(-1, 1) * self.shake * 30 * UI * SETTINGS.get("shake", 1)
        self.feed = [[text, t - dt] for text, t in self.feed if t - dt > 0]
        self.popups = [[text, color, t - dt] for text, color, t in self.popups if t - dt > 0]
        self.damage_dirs = [[a, t - dt] for a, t in self.damage_dirs if t - dt > 0]
        for puff in self.smoke:                          # 연기는 위로 퍼지며 사라져요
            puff[0] += puff[2] * dt
            puff[1] += puff[3] * dt
            puff[4] -= dt
            puff[5] += 14 * UI * dt
        self.smoke = [puff for puff in self.smoke if puff[4] > 0]
        self.bolt_anim = max(0.0, self.bolt_anim - dt)
        self.inspect_timer = max(0.0, self.inspect_timer - dt)
        self.ads_anim = max(0.0, self.ads_anim - dt)
        if self.aiming != self.was_aiming:
            self.ads_anim = 0.16
            self.was_aiming = self.aiming
        self.sound_marks = [[a, k, t - dt] for a, k, t in self.sound_marks if t - dt > 0]
        self.tracers = [tr[:4] + [tr[4] - dt] for tr in self.tracers if tr[4] - dt > 0]
        self.enemy_tracers = [[e, t - dt, off] for e, t, off in self.enemy_tracers if t - dt > 0]
        self.time += dt
        for effect in self.effects:
            effect.age += dt
        self.effects = [e for e in self.effects if not e.done]
        self.killcam_time += dt
        if self.mode == "mission" and not self.game_over:
            self.mission_time += dt
        if self.game_over:
            return
        if self.challenge and self.banner_timer <= 0:
            self.challenge_time += dt
            if self.challenge == "BLITZ" and self.challenge_time > BLITZ_TIME:
                self.fail_reason = "TIME UP"
                self.game_over = True
                return

        if self.round_clear_timer > 0:
            self.round_clear_timer -= dt
            if self.round_clear_timer <= 0:
                self.round += 1
                self.start_round()
            if self.mode != "zombies":
                return                     # 좀비 모드는 쉬는 동안에도 움직이고 상점을 쓸 수 있어요

        arsenal = self.arsenal
        spec = arsenal.current.spec
        if arsenal.index != self.seen_index:       # 무기를 바꾸면 정조준과 점사 멈추기
            self.seen_index = arsenal.index
            self.aim_on = False
            self.burst_left = 0
        self.knife_timer = max(0.0, self.knife_timer - dt)
        self.knife_cooldown = max(0.0, self.knife_cooldown - dt)
        fire_down = bool(buttons[0] or keys[pygame.K_f] or self.click_queued)   # 왼쪽 클릭 = F
        self.click_queued = False
        self.aiming = ((self.aim_on or self.pad_aim) and not arsenal.busy
                       and self.knife_timer == 0 and not self.player.sprinting)
        speed = (AIM_MOVE if self.aiming else 1.0) * spec.get("move", 1.0)
        if self.perk == "LIGHTFOOT":
            speed *= 1.12
        speed *= 1 + 0.06 * self.rank_of("RUNNER")
        # 조준점이 적 위에 있으면 시점이 살짝 느리게 돌아요 (키보드로도 적을 놓치지 않게)
        self.on_target = self.enemy_at(WIDTH / 2, HEIGHT / 2) is not None
        sticky = ASSIST_STICKY[SETTINGS["assist"]] if self.on_target and not self.scoped else 1.0
        sens = min(1.0, 1.5 / self.zoom) * sticky
        angle_before = self.player.angle
        self.player.update(dt, keys, mouse_dx, mouse_dy, sens, speed,
                           allow_sprint=not self.aiming and not fire_down)
        turn = self.player.angle - angle_before
        self.sway = max(-50 * UI, min(50 * UI, self.sway * 0.85 - turn * 900 * UI))
        arsenal.update(dt)
        if arsenal.reload_left > 0 and not self.was_reloading:
            self.sounds.play("reload")
        self.was_reloading = arsenal.reload_left > 0
        if arsenal.shells_loaded:
            self.sounds.play("magin")                   # 산탄총: 한 발 넣을 때마다 "착"
            arsenal.shells_loaded = 0
        if arsenal.reload_left > 0 and arsenal.shell:
            self.reload_prev = 0.0
        elif arsenal.reload_left > 0:                # 재장전 동작 소리: 탄창 빼기 → 끼우기 → (빈 탄창이면) 노리쇠
            prog = 1 - arsenal.reload_left / arsenal.reload_total
            for mark, name in ((0.25, "magout"), (0.62, "magin"), (0.88, "bolt")):
                if self.reload_prev < mark <= prog and (name != "bolt" or arsenal.reload_empty):
                    self.sounds.play(name)
            self.reload_prev = prog
        else:
            self.reload_prev = 0.0
        # 달리는 중엔 못 쏘고, 멈춘 뒤 잠깐 있어야 쏠 수 있어요
        if self.player.sprinting:
            self.sprint_recover = SPRINT_RECOVER
        else:
            self.sprint_recover = max(0.0, self.sprint_recover - dt)
        ready = self.knife_timer == 0 and self.sprint_recover == 0

        # 사격: 마우스 왼쪽 또는 F 키
        # 자동 무기는 누르고 있으면 계속, 나머지는 누를 때마다 한 발 (점사는 한 번에 여러 발)
        pressed = fire_down and not self.fire_was_down
        self.fire_was_down = fire_down
        if ready and (fire_down if spec["auto"] else pressed) and arsenal.try_fire():
            self.gun_sound(spec)
            self.on_fire(spec)
            if spec.get("lobbed"):
                self.launch_shell()
            elif spec["projectile"]:
                self.launch_rocket()
            else:
                self.shoot(spec)
            arsenal.add_recoil()
            self.burst_left = spec.get("burst", 1) - 1
            self.burst_timer = spec.get("burst_delay", 0.0)
        if self.burst_left > 0:
            self.burst_timer -= dt
            if self.burst_timer <= 0 and arsenal.current.mag > 0 and not arsenal.busy:
                arsenal.current.mag -= 1
                self.gun_sound(spec)
                self.on_fire(spec)
                self.shoot(spec)
                arsenal.add_recoil()
                self.burst_left -= 1
                self.burst_timer = spec["burst_delay"]

        # 액티브 스킬 시간
        for name in list(self.cooldowns):
            self.cooldowns[name] = max(0.0, self.cooldowns[name] - dt)
        self.focus = max(0.0, self.focus - dt)
        self.scan = max(0.0, self.scan - dt)
        edt = dt * (0.35 if self.focus > 0 else 1.0)   # FOCUS 중엔 적과 총알이 느려져요
        # 내 소리가 들리는 거리: 걸으면 4.5칸, 달리면 9칸, 앉으면 안 들려요. 총을 쏘면 16칸
        p = self.player
        step_noise = 0.0
        if p.moving and p.z == 0 and not p.crouch and self.perk != "LIGHTFOOT":
            step_noise = 9.0 if p.sprinting else 4.5
        self.gun_noise = max(0.0, self.gun_noise - dt)
        p.noise = max(step_noise, self.gun_noise_radius if self.gun_noise > 0 else 0.0)
        if self.mode == "zombies":
            self.update_zombies(edt)
        else:
            if self.mode == "training":
                self.update_training(dt)
            else:
                self.punish_camping(dt)
                self.update_squad(dt)

        for enemy in self.enemies:
            if self.mode == "mission" and enemy.pos.distance_to(p.pos) > 28 and enemy.hp >= enemy.t["hp"]:
                continue                            # 큰 맵: 멀리 있는 적은 가만히 (계산 아끼기)
            before = pygame.Vector2(enemy.pos)
            damage = enemy.update(edt, self.player)
            if enemy.kind == "BOSS":
                self.update_boss(enemy, edt)
            moved = enemy.pos.distance_to(before)
            enemy.walk += moved
            enemy.moving = 0.15 if moved > 0.0005 else max(0.0, enemy.moving - dt)
            # 걷는 적의 군화 소리: 멀수록 작게, 소리 나는 방향(왼쪽/오른쪽)에서 들려요
            if enemy.pos != before and enemy.pos.distance_to(p.pos) < 13:
                enemy.step_timer -= dt * enemy.t["speed"] / 1.4
                if enemy.step_timer <= 0:
                    zombie = "melee" in enemy.t
                    enemy.step_timer = 0.65 if zombie else 0.5
                    name = "zstep" if zombie else ENEMY_STEPS[step_sound_at(enemy.pos)]
                    self.play_at(name, enemy.pos, 13, 0.95)
            if enemy.flash_timer == 0.08:          # 방금 쐈어요
                self.play_at(enemy.t.get("sound", "enemy"), enemy.pos, 24)
                off = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) * (40 if damage else 170) * UI
                self.enemy_tracers.append([enemy, 0.07 if "sound" not in enemy.t else 0.25, off])
                dist = enemy.pos.distance_to(p.pos)
                if not damage and "sound" not in enemy.t and dist < 16:
                    volume, pan = self.spatial(enemy.pos, 16)
                    self.sounds.play("whiz", 0.4 + volume * 0.5, pan)   # 총알이 귀 옆을 스쳐요
                    self.suppress = min(1.0, self.suppress + 0.3)
            heal = enemy.t.get("heal")
            if heal:                                # 의무병: 근처 적 치료
                enemy.heal_timer -= dt
                if enemy.heal_timer <= 0:
                    enemy.heal_timer = heal[1]
                    for other in self.enemies:
                        if (other is not enemy and other.hp < other.t["hp"]
                                and other.pos.distance_to(enemy.pos) < heal[2]):
                            other.hp = min(other.t["hp"], other.hp + heal[0])
                            other.heal_flash = 0.6
                            self.play_at("heal", other.pos, 12, 0.6)
            if damage:
                self.last_attacker = enemy
                if "melee" in enemy.t:
                    self.sounds.play("swipe")
                    self.splash_screen(3)            # 좀비에게 할퀴이면 화면에 피
                self.hurt_player(damage, enemy.pos)
            if enemy.throw_at is not None:
                self.enemy_throw(enemy, enemy.throw_at)
                enemy.throw_at = None

        # 터지는 좀비: 나에게 닿았거나(나만 다쳐요) 총에 맞았으면(주변 좀비까지) 쾅
        for enemy in [e for e in self.enemies if e.boom]:
            self.enemies.remove(enemy)
            self.chunks(enemy, 12, (90, 120, 30), 6)
            self.add_splat(enemy.pos, 1.2)
            self.explode(enemy.pos, *EXPLODER_BLAST, owner="enemy")
        for _ in range(10):                        # 연쇄 폭발 (한 장면에 10번까지)
            if not self.pending_blasts:
                break
            self.explode(self.pending_blasts.pop(0), *EXPLODER_SHOT_BLAST)
        self.update_projectiles(edt)
        self.update_streaks(dt)
        self.update_effects(dt)
        self.collect_pickups()
        if self.mode != "zombies":
            self.update_objective(dt)

        if self.player.hp <= 0 and not self.game_over:
            self.player.hp = 0
            self.game_over = True
            self.start_killcam()
            if self.mode == "zombies":
                self.save["zbest"] = max(self.save.get("zbest", 0), self.round)
                write_save(self.save)
            elif not self.challenge:
                self.record_progress(self.round)      # 다음에 이 라운드부터 이어할 수 있게
        elif self.mode == "zombies" and not self.enemies and self.zombies_left == 0 and self.round_clear_timer <= 0:
            self.slowmo = 0.8
            self.round_clear_timer = 6.0              # 다음 웨이브까지 숨 돌리기
            self.banner = f"WAVE {self.round} SURVIVED"
            self.sub_banners = [("NEXT WAVE IN 6s", WHITE)]
            self.banner_timer = 6.0
            self.points += ZOMBIE_POINTS["wave"]
            self.add_xp(XP["round"], f"WAVE CLEAR  +{ZOMBIE_POINTS['wave']} POINTS")
            self.count_round()
            self.save["zbest"] = max(self.save.get("zbest", 0), self.round + 1)
            write_save(self.save)
        elif self.challenge and not self.enemies:
            self.slowmo = 0.8
            self.add_xp(XP["round"], f"CHALLENGE CLEAR  +{XP['round']}")
            self.count_round()
            self.finish_challenge()
        elif self.mode == "campaign" and (self.objective["done"] if self.objective else not self.enemies):
            self.slowmo = 0.8                         # 마지막 한 명(또는 목표 완료): 슬로모션
            self.round_clear_timer = 4.0
            self.banner = "CAMPAIGN COMPLETE!" if self.round == CAMPAIGN_ROUNDS else "ROUND CLEAR"
            self.sub_banners = [] if self.round != CAMPAIGN_ROUNDS else [("All 100 rounds cleared - the war goes on", YELLOW)]
            self.banner_timer = 4.0
            self.add_xp(XP["round"], f"ROUND CLEAR  +{XP['round']}")
            self.count_round()
            self.record_progress(self.round + 1)

    def gun_sound(self, spec):
        self.sounds.play(GUN_SOUNDS[spec["name"]], 0.45 if spec.get("suppressed") else 1.0)
        self.sounds.play("mech", 0.6)                        # 노리쇠 "착"
        if not spec.get("suppressed"):
            self.sounds.play("punch", min(1.0, 0.35 + spec["body"] / 90))   # 센 총일수록 묵직한 "쿵"

    def on_fire(self, spec):
        """쏠 때마다: 조준이 옆으로 살짝 튀고, 화면이 번쩍이고, 탄피가 튀어나와요"""
        # 정해진 반동 모양 + 아주 조금의 무작위
        if self.arsenal.since_shot > 0.3:
            self.shot_index = 0
        kick = HORIZONTAL_KICK.get(spec["name"], 0.005) * spec.get("recoil", 1.0)
        pattern = self.recoil_patterns.setdefault(spec["name"], recoil_pattern(spec["name"]))
        self.player.angle += (pattern[min(self.shot_index, len(pattern) - 1)] * 1.4 + random.uniform(-0.2, 0.2)) * kick
        self.shot_index += 1
        self.light_timer = 0.05
        # 메아리와 울림: 맵마다 달라요. 탄피는 조금 뒤에 바닥에 '짤랑'
        delay, echo = ECHOES.get(self.theme["name"], (0.25, 0.2))
        loud = 0.5 if spec.get("suppressed") else 1.0
        self.sounds.play("tail", 0.6 * loud)
        self.echoes.append([delay, GUN_SOUNDS[spec["name"]], echo * loud])
        if not spec["projectile"] and (not spec["auto"] or random.random() < 0.4):
            self.echoes.append([random.uniform(0.3, 0.45), "casing", random.uniform(0.2, 0.35)])
        if spec["name"] in BOLT_ACTION:                # 노리쇠 당기기: 소리와 동작
            self.bolt_anim = 0.75
            self.echoes.append([0.35, "bolt", 0.9])
        if not spec.get("suppressed"):                   # 총구에서 연기가 피어올라요 (연사하면 더 많이)
            heat = 2 if spec["auto"] and self.shot_index > 4 else 1
            for _ in range(heat):
                self.smoke.append([0.0, 0.0, random.uniform(-15, 15) * UI, random.uniform(-60, -30) * UI,
                                   random.uniform(0.6, 1.0), random.uniform(6, 10) * UI])
            del self.smoke[:-24]
        self.gun_noise = 0.5
        self.gun_noise_radius = 6.0 if spec.get("suppressed") else 16.0   # 소음기: 가까운 적만 들어요
        self.stats["shots"] += 1
        self.shake = max(self.shake, 0.03 + spec["kick"] / 450)     # 총이 셀수록 화면이 크게 흔들려요
        if not spec["projectile"]:
            shotgun = spec["name"] == "SHOTGUN"
            x, y = WIDTH * (0.5 if self.aiming else 0.62), HEIGHT * 0.72
            self.particles.append([x, y, random.uniform(250, 450) * UI, random.uniform(-450, -280) * UI,
                                   0.6, 4 * UI, (190, 40, 40) if shotgun else (210, 165, 60), True])

    def spray_blood(self, x, y, perp, head):
        """화면의 (x, y)에서 피가 튀어요. 멀수록 작게, 헤드샷이면 크게"""
        near = min(1.0, 4 / perp)
        for _ in range(16 if head else 7):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 340 if head else 220) * UI * near
            self.particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed - 120 * UI * near,
                                   random.uniform(0.25, 0.5), max(1.5, random.uniform(2, 5) * UI * near),
                                   (random.randint(120, 190), 0, random.randint(5, 20)), False])
        if len(self.particles) > 300:
            del self.particles[:100]

    def splash_screen(self, count=5):
        """화면 가장자리에 피가 묻어요 (1.5초 동안 흐려져요)"""
        for _ in range(count):
            side = random.random()
            x = random.uniform(0, WIDTH * 0.3) if side < 0.5 else random.uniform(WIDTH * 0.7, WIDTH)
            y = random.uniform(HEIGHT * 0.1, HEIGHT * 0.8)
            self.screen_blood.append([x, y, random.uniform(0.8, 1.8) * UI, 1.5])

    def add_impact(self, x, y, damage=0):
        """빗나간 총알: 맞은 벽/바닥 자리에서 먼지와 불똥이 튀어요"""
        col = int(x // self.col_w)
        if not 0 <= col < self.num_rays:
            return
        if self.zbuffer[col] < math.inf and y >= self.wall_top[col]:
            perp = self.zbuffer[col]
            if damage and self.wall_hit[col]:
                cx, cy, vertical, wall_x, spec = self.wall_hit[col]
                size = self.proj / max(0.05, perp)
                height = (self.horizon + self.eye * size - y) / size       # 맞은 높이 (땅에서 몇 칸 위)
                self.hit_wall(cx, cy, vertical, wall_x, height, damage, spec)
        elif y > self.horizon + 2:
            perp = self.eye * self.proj / (y - self.horizon)
        else:
            return                                # 하늘
        near = min(1.0, 4 / max(0.5, perp))
        for _ in range(6):
            angle = random.uniform(math.pi * 1.05, math.pi * 1.95)     # 위쪽으로 퍼져요
            speed = random.uniform(60, 200) * UI * near
            grey = random.randint(140, 200)
            self.particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                                   random.uniform(0.2, 0.4), max(1.0, random.uniform(1.5, 3.5) * UI * near),
                                   (grey, grey - 10, grey - 30), False])
        self.particles.append([x, y, 0, 0, 0.05, max(2.0, 5 * UI * near), (255, 230, 140), False])   # 불똥

    def add_decal(self, cx, cy, vertical, wall_x, height, kind):
        marks = self.decals.setdefault((cx, cy, vertical), [])
        marks.append((wall_x, height, kind))
        self.decal_count += 1
        if self.decal_count > MAX_DECALS:                # 너무 많으면 오래된 것부터 지워요
            for key in list(self.decals):
                if self.decals[key]:
                    self.decals[key].pop(0)
                    self.decal_count -= 1
                    break

    def hit_wall(self, cx, cy, vertical, wall_x, height, damage, spec):
        """총알이 벽에 맞았어요: 부서지는 엄폐물은 체력이 깎이고, 창문은 깨지고, 나머지엔 총알 자국"""
        letter = GAME_MAP[cy][cx]
        if letter in DESTRUCTIBLE:
            self.damage_cover(cx, cy, damage)
            return
        if spec[2] is True and (0.18 < wall_x < 0.42 or 0.58 < wall_x < 0.82):
            k = int(height / 0.5)
            if 0.17 < height - k * 0.5 < 0.42:          # 창문에 맞음
                key = (cx, cy, vertical, 0 if wall_x < 0.5 else 1, k)
                if key not in self.broken_windows:
                    self.broken_windows.add(key)
                    self.play_at("glass", pygame.Vector2(cx + 0.5, cy + 0.5), 18)
                return
        self.add_decal(cx, cy, vertical, wall_x, height, "hole")

    def damage_cover(self, cx, cy, damage):
        letter = GAME_MAP[cy][cx]
        hp = self.cover_hp.get((cx, cy), DESTRUCTIBLE[letter]) - damage
        self.cover_hp[(cx, cy)] = hp
        if hp <= 0:
            self.destroy_cell(cx, cy)

    def destroy_cell(self, cx, cy):
        """상자/모래주머니가 부서져요: 그 칸은 바닥이 되고 조각이 튀어요"""
        color = WALL_GRID[cy][cx][0] if WALL_GRID[cy][cx] else (150, 120, 80)
        row = GAME_MAP[cy]
        GAME_MAP[cy] = row[:cx] + FLOOR_GRID[cy][cx] + row[cx + 1:]
        WALL_GRID[cy][cx] = None
        self.decals.pop((cx, cy, True), None)
        self.decals.pop((cx, cy, False), None)
        center = pygame.Vector2(cx + 0.5, cy + 0.5)
        self.play_at("smash", center, 20)
        box = self.project(center, 0.8, 1.0)
        if box:
            sx, top, bottom, w, perp = box
            near = min(1.0, 4 / max(0.5, perp))
            for _ in range(16):
                angle = random.uniform(math.pi * 1.1, math.pi * 1.9)
                speed = random.uniform(80, 300) * UI * near
                tone = random.uniform(0.6, 1.1)
                self.particles.append([sx + random.uniform(-w, w) * 0.4, (top + bottom) / 2,
                                       math.cos(angle) * speed, math.sin(angle) * speed, random.uniform(0.4, 0.8),
                                       max(2.0, random.uniform(3, 7) * UI * near),
                                       tuple(min(255, int(c * tone)) for c in color), False])
        self.minimap = self.make_minimap()

    def chunks(self, enemy, count, color, size, upward=False):
        """적 몸에서 조각이 튀어요 (헤드샷이면 헬멧, 폭발이면 살점)"""
        box = self.enemy_box(enemy)
        if not box:
            return
        sx, top, bottom, w, perp = box
        near = min(1.0, 4 / perp)
        y = top + (bottom - top) * (0.08 if upward else 0.45)
        for _ in range(count):
            angle = random.uniform(math.pi * 1.2, math.pi * 1.8) if upward else random.uniform(0, 2 * math.pi)
            speed = random.uniform(150, 380) * UI * near
            self.particles.append([sx, y, math.cos(angle) * speed, math.sin(angle) * speed - 150 * UI * near,
                                   random.uniform(0.5, 0.8), max(2.0, size * random.uniform(0.7, 1.3) * UI * near),
                                   color, False])

    def add_splat(self, pos, size):
        self.splats.append([pygame.Vector2(pos), size])
        if len(self.splats) > MAX_SPLATS:
            self.splats.pop(0)

    def hurt_player(self, damage, source=None):
        """나에게 피해. source(때린 위치)가 있으면 화면에 맞은 방향을 표시해요."""
        damage *= DIFFICULTIES[SETTINGS["difficulty"]][2]
        if self.challenge == "HARDCORE" and damage > 0:
            damage = max(damage, self.player.hp + 1)      # 한 방에 끝
        if source is not None:
            self.last_source = pygame.Vector2(source)
        self.player.hp -= int(damage)
        self.since_hurt = 0.0
        self.damage_flash = min(1.0, 0.4 + damage / 40)
        self.shake = max(self.shake, 0.08 + damage / 200)          # 맞으면 화면이 움찔
        self.sounds.play("hurt")
        if source is not None and source != self.player.pos:
            offset = source - self.player.pos
            self.damage_dirs.append([math.atan2(offset.y, offset.x), 1.2])

    def current_spread(self, spec):
        if spec["scope"]:
            spread = 1 if self.scoped else spec["spread"]
        else:
            spread = spec["spread"] + (self.arsenal.recoil * 0.1 if spec["auto"] else 0)
            if self.aiming:
                spread *= 0.45                     # 정조준하면 덜 퍼져요
        if self.player.moving:
            spread += 40 if spec["scope"] else (8 if self.aiming else 16)
        if self.player.z > 0:
            spread += 25
        spread += self.suppress * 14                # 제압당하면 조준이 흔들려요
        if self.player.slide_timer > 0:
            spread += 12
        elif self.player.crouch_amt > 0.5:
            spread *= 0.75                         # 앉으면 덜 퍼져요
        return spread * UI

    def damage_enemy(self, enemy, amount, how):
        """적에게 피해 주기. 쓰러지면 킬 로그에 남기고 상자를 떨어뜨려요."""
        enemy.hp -= amount
        enemy.hurt_timer = 0.08
        enemy.flinch = 0.16 if how == "HEADSHOT!" else 0.12
        enemy.flinch_pose = "flinch_head" if how == "HEADSHOT!" else random.choice(("flinch_l", "flinch_r"))
        enemy.spotted = max(enemy.spotted, enemy.t["reaction"])   # 맞으면 바로 반격
        enemy.sees = True
        if how not in STREAK_KILLS:
            self.sounds.play("hit")
            if enemy.kind in ARMORED:
                self.sounds.play("armor", 0.6)     # 장갑에 맞는 '깡' 
            if self.mode == "zombies" and enemy.hp > 0:
                self.points += ZOMBIE_POINTS["hit"]
        # 움찔: 잠깐 못 쏘고 뒤로 살짝 밀려요
        enemy.shoot_timer = max(enemy.shoot_timer, 0.2)
        away = enemy.pos - self.player.pos
        away = away.normalize() if away.length() > 0 else pygame.Vector2(1, 0)
        move_with_collision(enemy.pos, away * min(0.35, 0.05 + amount / 500))   # 셀수록 크게 밀려요
        self.hitmarker = 0.18
        self.hitmarker_kill = enemy.hp <= 0
        self.hit_head = how == "HEADSHOT!"
        if enemy.hp <= 0 and enemy in self.enemies:
            self.enemies.remove(enemy)
            if how not in STREAK_KILLS:
                self.hitstop = max(self.hitstop, 0.07 if how == "HEADSHOT!" else 0.04)
            if how == "HEADSHOT!" and enemy.t["look"]["head"] != "zombie":
                self.chunks(enemy, 1, (55, 62, 48), 9, upward=True)        # 헬멧/모자가 날아가요
            if how in ("BOOM!", "AIRSTRIKE!"):
                self.chunks(enemy, 12, (110, 0, 10), 5)                     # 폭발에 살점이 튀어요
            if enemy.t.get("explode"):
                self.pending_blasts.append(pygame.Vector2(enemy.pos))       # 맞아서 터지는 좀비
            if how in ("BOOM!", "AIRSTRIKE!"):
                style = "blast"
            elif how == "HEADSHOT!":
                style = "drop"
            elif amount >= 60:
                style = "fly"
            else:
                style = "fall"
            self.corpses.append(Corpse(enemy, away, style))
            if enemy.pos.distance_to(self.player.pos) < 2.2:
                self.splash_screen()                # 가까이서 쓰러뜨리면 화면에 피가 튀어요
            if len(self.corpses) > MAX_CORPSES:
                self.corpses.pop(0)
            self.kills += 1
            self.feed.append([f"{enemy.kind} {how}", 2.5])
            self.on_kill(enemy, how)
            if enemy.kind == "BOSS":               # 보스는 상자를 잔뜩 떨어뜨려요
                for i, kind in enumerate(("ammo", "health", "grenade", "health")):
                    offset = pygame.Vector2(0.5, 0).rotate(i * 90)
                    self.pickups.append(Pickup(enemy.pos.x + offset.x, enemy.pos.y + offset.y, kind))
            elif random.random() < (0.12 if self.mode == "zombies" else DROP_CHANCE):
                kind = random.choices(list(DROP_WEIGHTS), weights=list(DROP_WEIGHTS.values()))[0]
                self.pickups.append(Pickup(enemy.pos.x, enemy.pos.y, kind))

    def on_kill(self, enemy, how):
        """처치 보상: 경험치, 연속 처치 메달, 킬스트릭"""
        self.sounds.play("headshot" if how == "HEADSHOT!" else "kill")
        if self.mode != "training":                     # 누적 기록 (업적용)
            life = self.save.setdefault("lifetime", {})
            life["kills"] = life.get("kills", 0) + 1
            key = {"HEADSHOT!": "heads", "KNIFE!": "knife", "BOOM!": "explosive"}.get(how)
            if key:
                life[key] = life.get(key, 0) + 1
        stats = self.stats
        stats["kills"] += 1
        if how == "HEADSHOT!":
            stats["heads"] += 1
        if how in ("DOWN", "HEADSHOT!"):                 # 총으로 쓰러뜨렸으면 그 총의 경험
            name = self.arsenal.current.spec["name"]
            stats["weapons"][name] = stats["weapons"].get(name, 0) + 1
            if self.loadout and self.mode != "training":
                kills = self.save.setdefault("wkills", {})
                kills[name] = kills.get(name, 0) + 1
                changed = False
                for need, mod in WEAPON_LEVELS:
                    if kills[name] == need:
                        self.popups.append([f"{name}: {mod} UNLOCKED!", (255, 200, 60), 3.0])
                        self.sounds.play("streak")
                        changed = True
                level = weapon_level(kills[name])
                if level > weapon_level(kills[name] - 1):
                    self.popups.append([f"{name} LEVEL {level}  (DAMAGE +{5 * (level - 1)}%)", (255, 200, 60), 2.5])
                    changed = True
                if changed:
                    self.refresh_weapon(name)
        if self.mode == "zombies":
            key = {"HEADSHOT!": "headshot", "KNIFE!": "knife"}.get(how, "kill")
            self.points += ZOMBIE_POINTS[key]
        self.check_unlocks()
        xp = XP["kill"]
        if how == "HEADSHOT!":
            xp += XP["headshot"]
        elif how == "KNIFE!":
            xp += XP["knife"]
        if enemy.kind == "BOSS":
            xp += XP["boss"]
        self.add_xp(xp, f"+{xp}")

        # 3초 안에 또 쓰러뜨리면 연속 처치 메달
        self.multi = self.multi + 1 if self.time - self.last_kill < 3 else 1
        self.last_kill = self.time
        medals = {2: ("DOUBLE KILL", XP["double"]), 3: ("TRIPLE KILL", XP["triple"])}
        if self.multi >= 2:
            name, bonus = medals.get(self.multi, ("MULTI KILL", XP["multi"]))
            self.add_xp(bonus, f"{name}  +{bonus}", (255, 160, 60))

        # 킬스트릭 (킬스트릭으로 쓰러뜨린 건 안 세요)
        if how not in STREAK_KILLS:
            self.streak += 1
            self.stats["best"] = max(self.stats["best"], self.streak)
            if self.mode != "training":
                life = self.save.setdefault("lifetime", {})
                life["streak"] = max(life.get("streak", 0), self.streak)
            for need, name in STREAKS:
                if self.streak == need:
                    self.streaks_ready.append(name)
                    self.sounds.play("streak")
                    self.popups.append([f"{name} READY!  press X", (80, 240, 255), 2.5])
        self.check_achievements()

    def check_achievements(self):
        """새로 이룬 업적을 알려줘요 (위장 무늬를 새로 얻으면 그것도)"""
        if self.mode == "training":
            return
        done = self.save.setdefault("achievements", [])
        life = self.save.get("lifetime", {})
        before = earned_camos(self.save)
        for name, ko, en, test in ACHIEVEMENTS:
            if name not in done and test(self.save, life):
                done.append(name)
                self.sounds.play("streak")
                self.popups.append([f"ACHIEVEMENT: {name}", (255, 215, 80), 3.0])
        for camo in earned_camos(self.save):
            if camo not in before:
                self.popups.append([f"NEW CAMO: {camo}  (A on the start screen)", (80, 240, 255), 3.0])

    def count_round(self):
        """라운드/웨이브/미션 단계를 깰 때마다 누적 기록"""
        life = self.save.setdefault("lifetime", {})
        life["rounds"] = life.get("rounds", 0) + 1
        self.check_achievements()

    def use_streak(self):
        """X: 받은 킬스트릭을 하나 써요 (먼저 받은 것부터)"""
        if not self.streaks_ready or self.game_over:
            return
        name = self.streaks_ready.pop(0)
        p = self.player
        if name == "RADAR":
            self.radar_timer = RADAR_TIME
            self.popups.append(["RADAR ONLINE", (80, 240, 255), 1.5])
        elif name == "AIRSTRIKE":
            target = self.airstrike_target()
            self.effects.append(Effect(target, self.flare_frames, 1.5, 1.0))   # 빨간 연막으로 표시
            forward = p.forward
            for k in range(5):                       # 바라보는 방향으로 줄지어 5발
                spot = target + forward * (k - 2) * 1.5
                self.airstrikes.append([spot, 1.5 + k * 0.15])
            self.popups.append(["AIRSTRIKE INBOUND", (255, 120, 60), 1.5])
        elif name == "SENTRY":
            # 2칸 앞에 놓아요 (막혀 있으면 1칸 앞, 그것도 막혀 있으면 내 자리)
            for dist in (2.0, 1.0, 0.0):
                spot = p.pos + p.forward * dist
                if dist == 0 or (not is_blocked(spot.x, spot.y) and can_see(p.pos, spot)):
                    break
            self.sentries.append(Sentry(spot.x, spot.y))
            self.popups.append(["SENTRY DEPLOYED", (80, 240, 255), 1.5])

    def airstrike_target(self):
        """공습 위치: 조준점이 가리키는 땅 (멀면 12칸), 건물 앞에서 멈춰요"""
        p = self.player
        slope = self.aim_slope()
        dist = min(20.0, max(3.0, self.eye / -slope)) if slope < -0.03 else 12.0
        target = pygame.Vector2(p.pos)
        step = p.forward * 0.25
        travelled = 0.0
        while travelled < dist and not is_opaque(target.x + step.x, target.y + step.y):
            target += step
            travelled += 0.25
        return target

    def update_effects(self, dt):
        """체력 회복, 튀는 피와 탄피, 쓰러지는 적, 심장 박동, 발소리"""
        p = self.player
        # 발소리: 걸으면 일정한 간격으로, 달리면 빠르게, 앉으면 작고 느리게
        if p.moving and p.z == 0 and p.slide_timer <= 0:
            self.step_timer -= dt * (1.6 if p.sprinting else (0.65 if p.crouch else 1.0))
            if self.step_timer <= 0:
                self.step_timer = 0.42
                quiet = 0.5 if self.perk == "LIGHTFOOT" else 1.0
                volume = random.uniform(0.2, 0.3) if p.crouch else random.uniform(0.5, 0.65)
                self.sounds.play(step_sound_at(p.pos), volume * quiet)
        if self.was_airborne and p.z == 0:              # 점프하고 착지
            self.sounds.play(step_sound_at(p.pos), 1.0)
        self.was_airborne = p.z > 0
        self.since_hurt += dt
        self.light_timer = max(0.0, self.light_timer - dt)
        regen = self.rank_of("REGEN")
        if self.since_hurt > REGEN_DELAY - 0.7 * regen and 0 < p.hp < self.max_hp:
            p.hp = min(self.max_hp, p.hp + REGEN_RATE * (1 + 0.3 * regen) * dt)
        if 0 < p.hp < 30:                       # 체력이 낮으면 심장 소리
            self.heart_timer -= dt
            if self.heart_timer <= 0:
                self.heart_timer = 0.8
                self.sounds.play("heart")
        gravity = 1400 * UI
        alive = []
        for part in self.particles:
            part[0] += part[2] * dt
            part[1] += part[3] * dt
            part[3] += gravity * dt
            part[4] -= dt
            if part[4] > 0:
                alive.append(part)
        self.particles = alive
        for corpse in self.corpses:
            corpse.age += dt
            if corpse.vz or corpse.z > 0:       # 폭발로 떴다가 떨어져요
                corpse.z = max(0.0, corpse.z + corpse.vz * dt)
                corpse.vz = corpse.vz - GRAVITY * dt if corpse.z > 0 else 0.0
            if corpse.age < 0.35 or corpse.z > 0:   # 넘어지면서 밀려나요
                move_with_collision(corpse.pos, corpse.vel * dt)
                corpse.vel *= 0.85
            elif corpse.age - dt < 0.35:        # 다 쓰러지면 피 웅덩이
                self.add_splat(corpse.pos, random.uniform(0.8, 1.2))
        self.corpses = [c for c in self.corpses if c.age < CORPSE_TIME]

    def update_streaks(self, dt):
        self.radar_timer = max(0.0, self.radar_timer - dt)
        # 공습: 시간이 되면 폭발
        waiting = []
        for spot, t in self.airstrikes:
            if t - dt <= 0:
                self.explode(spot, *AIRSTRIKE_BLAST, owner="streak")
            else:
                waiting.append([spot, t - dt])
        self.airstrikes = waiting
        # 자동 포탑: 가까이 보이는 가장 가까운 적을 쏴요
        for sentry in self.sentries:
            sentry.timer -= dt
            sentry.cooldown -= dt
            sentry.flash -= dt
            if sentry.cooldown > 0:
                continue
            targets = [e for e in self.enemies
                       if e.pos.distance_to(sentry.pos) < SENTRY_RANGE and can_see(sentry.pos, e.pos)]
            if targets:
                target = min(targets, key=lambda e: e.pos.distance_to(sentry.pos))
                sentry.cooldown = 0.15
                sentry.flash = 0.06
                self.sounds.play("smg", 0.35)
                if random.random() < 0.55:
                    self.damage_enemy(target, 20, "SENTRY")
            else:
                sentry.cooldown = 0.3
        self.sentries = [s for s in self.sentries if s.timer > 0]

    def shoot(self, spec):
        """조준점(화면 가운데) 근처로 총알을 쏴서 맞은 적에게 피해를 줘요."""
        spread = self.current_spread(spec)
        damage = {}               # 적마다 받은 피해 (산탄총은 여러 발이 한 적에게 맞을 수 있어요)
        headshots = set()
        hits = []                 # 피가 튈 자리: (x, y, 거리, 머리인지)
        for _ in range(spec["pellets"]):
            ax = WIDTH / 2 + random.uniform(-spread, spread)
            ay = HEIGHT / 2 + random.uniform(-spread, spread) * 0.6
            # 정확히 맞았는지 보고, 아깝게 빗나갔으면 조준 보정으로 몸통에 맞혀요 (조준경 저격은 보정 없음)
            found = self.enemy_at(ax, ay)
            if not found and not self.scoped and ASSIST_PAD[SETTINGS["assist"]] > 0:
                found = self.enemy_at(ax, ay, assist=ASSIST_PAD[SETTINGS["assist"]])
            if not found:
                found = self.enemy_at(ax, ay, pierce=True)
                if not found:                     # 완전히 빗나감: 근처 적은 움츠러들어요 (제압)
                    near = self.enemy_at(ax, ay, assist=3.0)
                    if near:
                        near[0].suppressed = 1.2
            target, target_dist, head = found[:3] if found else (None, math.inf, False)
            if found:
                ax, ay = found[3], found[4]       # 피는 적 몸 위에서 튀게
            if target and self.blocked_by_cover(ax, ay, target_dist):
                target = None                     # 자동차에 막힘
            if not self.scoped:
                self.tracers.append([*self.muzzle_screen, ax, ay, 0.05])
            if not target:
                self.add_impact(ax, ay, spec["body"])     # 벽이나 바닥에 맞으면 먼지와 불똥 (+ 자국, 부서짐)
            if target and self.challenge == "HEADSHOTS" and not head:
                continue                          # 헤드샷 도전: 몸에 맞으면 피해 없음
            if target:
                amount = spec["head"] * (1 + 0.15 * self.rank_of("MARKSMAN")) if head else spec["body"]
                if self.challenge == "HARDCORE":
                    amount *= 2
                if self.perk == "HEAVY ROUNDS":
                    amount *= 1.25
                if found[5]:                      # 관통: 피해가 줄어요
                    amount *= PENETRATION
                    if not any(text == "WALLBANG" for text, _, _ in self.popups):
                        self.popups.append(["WALLBANG", (255, 160, 60), 0.8])
                if not head and target.shield_blocks(self.player.pos):
                    amount *= 0.15                # 방패에 막힘
                damage[target] = damage.get(target, 0) + amount
                if head:
                    headshots.add(target)
                if amount > spec["body"] * 0.5 or head:     # 방패에 막힌 총알은 피가 안 나요
                    hits.append((ax, ay, target_dist, head))

        if damage:
            self.stats["hits"] += 1
        for x, y, perp, head in hits:
            self.spray_blood(x, y, perp, head)
        for enemy, amount in damage.items():
            self.damage_enemy(enemy, amount, "HEADSHOT!" if enemy in headshots else "DOWN")

    def enemy_at(self, ax, ay, assist=0.0, pierce=False):
        """화면의 (ax, ay)에 보이는 가장 가까운 적.
        assist가 있으면 적 둘레를 조금 넓혀서 찾아요 (아깝게 빗나간 총알도 맞게 하는 조준 보정).
        pierce=True면 얇은 엄폐물(상자, 모래주머니) 바로 뒤의 적도 찾아요 (총알 관통).
        돌려주는 값: (적, 거리, 머리인지, 맞은 x, 맞은 y, 관통했는지) 또는 None"""
        best = None
        for enemy in self.enemies:
            box = self.enemy_box(enemy)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            pad = assist * (8 * UI + w * 0.3)
            if not (sx - w / 2 - pad <= ax <= sx + w / 2 + pad and top - pad * 0.5 <= ay <= bottom):
                continue
            hx = min(max(ax, sx - w * 0.4), sx + w * 0.4)
            hy = min(max(ay, top), bottom)
            col = int(hx // self.col_w)
            pierced = False
            if 0 <= col < self.num_rays and perp > self.zbuffer[col]:
                if not (pierce and self.wall_thin[col] and perp - self.zbuffer[col] < 2.5):
                    continue                      # 건물 뒤에 숨어 있음
                pierced = True                    # 상자 너머 적: 총알이 뚫고 들어가요
            if best is None or perp < best[1]:
                head = top <= ay < top + (bottom - top) * 0.2 and abs(ax - sx) <= w / 2   # 위쪽 20% = 머리
                best = (enemy, perp, head, hx, hy, pierced)
        return best

    def spatial(self, pos, reach):
        """pos에서 난 소리의 (크기, 방향). reach보다 멀면 안 들려요. 뒤에서 난 소리는 조금 작게."""
        offset = pos - self.player.pos
        dist = offset.length()
        if dist >= reach:
            return 0.0, 0.0
        rel = angle_diff(math.atan2(offset.y, offset.x), self.player.angle) if dist > 0 else 0.0
        volume = 1 - dist / reach
        if math.cos(rel) < 0:
            volume *= 0.8
        return volume, math.sin(rel)

    def play_at(self, name, pos, reach, loud=1.0):
        volume, pan = self.spatial(pos, reach)
        if SETTINGS.get("soundviz") and volume > 0.05 and name in SOUND_MARK_KINDS and len(self.sound_marks) < 12:
            offset = pos - self.player.pos
            if offset.length() > 0.5:
                self.sound_marks.append([math.atan2(offset.y, offset.x), SOUND_MARK_KINDS[name], 0.9])
        if volume > 0.02 and name in MUFFLED_SOUNDS and not can_see(self.player.pos, pos):
            name += "_m"            # 벽 너머: 먹먹한 소리
        self.sounds.play(name, volume * loud, pan)

    def throw_grenade(self):
        if self.arsenal.grenades <= 0 or self.knife_timer > 0:
            return
        self.arsenal.grenades -= 1
        self.sounds.play("throw")
        p = self.player
        forward = pygame.Vector2(math.cos(p.angle), math.sin(p.angle))
        slope = self.aim_slope()
        # 바라보는 방향으로 던져요. 위를 볼수록 높이 날아가요
        vel = forward * GRENADE_THROW * (1 - min(0.5, abs(slope) * 0.5))
        vz = 3.0 + slope * GRENADE_THROW
        self.projectiles.append(Projectile("grenade", p.pos + forward * 0.3, self.eye - 0.1, vel, vz))

    def enemy_throw(self, enemy, target):
        """적이 target 위치에 떨어지도록 수류탄을 던져요 (포물선 계산)"""
        offset = target - enemy.pos
        dist = offset.length()
        if dist == 0:
            return
        flight = max(0.6, min(1.3, dist / 7))          # 날아가는 시간(초)
        start_z = 0.7
        vz = (0.5 * GRAVITY * flight * flight - start_z) / flight
        self.projectiles.append(Projectile("grenade", enemy.pos, start_z, offset / flight, vz, owner="enemy"))

    def launch_rocket(self):
        p = self.player
        forward = pygame.Vector2(math.cos(p.angle), math.sin(p.angle))
        slope = self.aim_slope()
        horiz = ROCKET_SPEED / math.sqrt(1 + slope * slope)
        self.projectiles.append(Projectile("rocket", p.pos + forward * 0.3, self.eye - 0.1,
                                           forward * horiz, horiz * slope))

    def launch_shell(self):
        """유탄: 포물선으로 날아가요 (위를 볼수록 멀리)"""
        p = self.player
        forward = pygame.Vector2(math.cos(p.angle), math.sin(p.angle))
        slope = self.aim_slope()
        self.projectiles.append(Projectile("shell", p.pos + forward * 0.3, self.eye - 0.1,
                                           forward * 13, 2.0 + slope * 13))

    def update_projectiles(self, dt):
        alive = []
        for proj in self.projectiles:
            if proj.update(dt, self.enemies):
                if proj.kind == "rocket":
                    radius, damage = ROCKET_BLAST
                elif proj.kind == "shell":
                    radius, damage = SHELL_BLAST
                elif proj.owner == "enemy":
                    radius, damage = ENEMY_GRENADE_BLAST
                else:
                    radius, damage = GRENADE_BLAST
                self.explode(proj.pos, radius, damage, proj.owner)
            else:
                alive.append(proj)
        self.projectiles = alive

    def explode(self, pos, radius, damage, owner="player"):
        """폭발: 반경 안에서 건물에 가리지 않은 대상에게 피해.
        가운데 가까이(반경의 20% 안)는 최대 피해, 멀어질수록 약해져요.
        내 폭발은 적(과 가까이 있는 나)에게, 적의 폭발은 나에게만 피해를 줘요."""
        def power(d):
            return min(1.0, 1.25 * (1 - d / radius))

        self.effects.append(Effect(pos, self.explosion_frames, 0.5, radius * 0.9))
        self.play_at("explosion", pos, 25, 1.1)
        for row in range(int(pos.y) - 2, int(pos.y) + 3):      # 가까운 상자는 부서지고, 벽엔 그을음
            for col in range(int(pos.x) - 2, int(pos.x) + 3):
                if not in_map(col, row) or not WALL_GRID[row][col]:
                    continue
                center = pygame.Vector2(col + 0.5, row + 0.5)
                d = center.distance_to(pos)
                if d > radius * 0.75:
                    continue
                if GAME_MAP[row][col] in DESTRUCTIBLE:
                    self.damage_cover(col, row, damage * 3 * power(d))
                elif d < 1.6:
                    off = pos - center
                    vertical = abs(off.x) > abs(off.y)             # 폭발이 난 쪽의 벽면
                    wall_x = (pos.y - row) if vertical else (pos.x - col)
                    self.add_decal(col, row, vertical, min(0.95, max(0.05, wall_x)), 0.3, "scorch")
        if owner in ("player", "streak"):
            how = "AIRSTRIKE!" if owner == "streak" else "BOOM!"
            for enemy in list(self.enemies):
                d = enemy.pos.distance_to(pos)
                if d < radius and can_see(pos, enemy.pos):
                    boost = 1 + 0.2 * self.rank_of("DEMOLITION") if owner == "player" else 1.0
                    self.damage_enemy(enemy, damage * power(d) * boost, how)
                    self.add_splat(enemy.pos, 0.7)
        d = self.player.pos.distance_to(pos)
        if owner != "streak" and d < radius and can_see(pos, self.player.pos):
            self.hurt_player(damage * power(d) * (SELF_DAMAGE if owner == "player" else 1.0), pos)
        if d < 12:
            self.shake = max(self.shake, 0.4 * (1 - d / 12))

    def knife_attack(self):
        """칼: 바로 앞(1.5칸 안, 앞쪽 약 60도)에 있는 가장 가까운 적을 베요."""
        if self.knife_cooldown > 0 or self.arsenal.busy:
            return
        self.knife_timer = KNIFE_TIME
        self.knife_cooldown = KNIFE_COOLDOWN
        self.sounds.play("knife")
        self.aim_on = False
        p = self.player
        best, best_d = None, KNIFE_RANGE
        for enemy in self.enemies:
            offset = enemy.pos - p.pos
            d = offset.length()
            if d < best_d and abs(angle_diff(math.atan2(offset.y, offset.x), p.angle)) < 0.5:
                best, best_d = enemy, d
        if best:
            self.damage_enemy(best, KNIFE_DAMAGE, "KNIFE!")

    def collect_pickups(self):
        """가까이 간 상자를 주워요. 꽉 차서 못 쓰는 상자는 그대로 둬요."""
        left = []
        for item in self.pickups:
            if item.pos.distance_to(self.player.pos) > PICKUP_RADIUS:
                left.append(item)
                continue
            if item.kind == "ammo" and self.arsenal.add_ammo():
                self.feed.append(["+AMMO", 1.5])
            elif item.kind == "health" and self.player.hp < self.max_hp:
                self.player.hp = min(self.max_hp, self.player.hp + HEALTH_PACK)
                self.feed.append([f"+{HEALTH_PACK} HP", 1.5])
            elif item.kind == "grenade" and self.arsenal.grenades < GRENADES_MAX:
                self.arsenal.grenades += 1
                self.feed.append(["+1 GRENADE", 1.5])
            else:
                left.append(item)
        self.pickups = left

    def blocked_by_cover(self, ax, ay, target_dist):
        """화면의 (ax, ay)로 날아간 총알이 target_dist보다 가까운 자동차에 막히면 True"""
        for d in self.decor:
            if not d.cover:
                continue
            box = self.project(d.pos, d.height, d.width)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            if perp < target_dist and abs(ax - sx) < w * 0.45 and top + (bottom - top) * 0.2 <= ay <= bottom:
                return True
        return False

    def enemy_box(self, enemy):
        return self.project(enemy.pos, enemy.t["height"], enemy.t["width"], enemy.t.get("lift", 0.0))

    def project(self, pos, height, width, lift=0.0):
        """월드 위치 → 화면 위치/크기. 시야 밖이면 None
        lift: 바닥에서 떠 있는 높이 (날아가는 수류탄 등)

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
        bottom = self.horizon + (self.eye - lift) * size
        return sx, bottom - size * height, bottom, size * width, perp

    # ----- 화면 그리기 -----
    def draw(self, screen):
        if self.game_over and self.killcam_from is not None and self.killcam_time < KILLCAM_TIME:
            self.draw_killcam(screen)
            return
        self.draw_sky(screen)
        self.draw_world(screen)
        self.draw_sprites(screen)
        self.draw_particles(screen, casings=False)       # 튀는 피
        if self.lightning > 0:
            self.flash_overlay.set_alpha(int(190 * self.lightning / 0.3 * (0.75 + 0.25 * math.sin(self.lightning * 60))))
            screen.blit(self.flash_overlay, (0, 0))
        if self.theme["snow"]:
            self.draw_snow(screen)
        if self.theme.get("rain"):
            self.draw_rain(screen)
        if self.scoped:
            screen.blit(self.scope_overlay, (0, 0))
            label = self.font.render(f"x{self.zoom}", True, WHITE)
            screen.blit(label, label.get_rect(center=(WIDTH / 2 + HEIGHT * 0.3, HEIGHT / 2 + HEIGHT * 0.3)))
        elif self.knife_timer > 0:
            self.draw_knife(screen)
        else:
            self.draw_gun(screen)
        self.draw_particles(screen, casings=True)        # 탄피는 총 앞에
        self.draw_tracers(screen)
        if self.light_timer > 0:
            screen.blit(self.muzzle_light, (0, 0))       # 총구 섬광
        self.draw_hud(screen)
        if self.mode == "training":
            self.draw_training(screen)
        if self.show_help:
            draw_help(screen, self.fonts, HELP_TEXT[self.fonts["lang"]]["resume"])

    def draw_tracers(self, screen):
        """총알 궤적: 내 총알은 총구에서 맞은 곳까지, 적 총알은 적에게서 내 쪽으로 (침은 초록)"""
        for x0, y0, x1, y1, life in self.tracers:
            start = pygame.Vector2(x0, y0)
            end = pygame.Vector2(x1, y1)
            mid = start.lerp(end, 0.35 + (0.05 - life) * 8)  # 총알이 날아가는 것처럼 앞쪽만 그려요
            pygame.draw.line(screen, (255, 200, 110), mid, end, max(1, int(2 * UI)))
            pygame.draw.line(screen, (255, 250, 220), mid.lerp(end, 0.5), end, 1)
        for enemy, life, off in self.enemy_tracers:
            if enemy not in self.enemies:
                continue
            box = self.enemy_box(enemy)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            col = int(sx // self.col_w)
            if 0 <= col < self.num_rays and perp > self.zbuffer[col]:
                continue
            start = (sx + w * 0.35, top + (bottom - top) * 0.45)
            end = (WIDTH / 2 + off.x, HEIGHT / 2 + off.y)
            if "sound" in enemy.t:                 # 산성 침: 굵은 초록 줄
                pygame.draw.line(screen, (120, 230, 80), start, end, max(3, int(6 * UI)))
            else:
                pygame.draw.line(screen, (255, 225, 150), start, end, max(1, int(2 * UI)))

    def draw_particles(self, screen, casings):
        for x, y, vx, vy, life, size, color, is_casing in self.particles:
            if is_casing != casings:
                continue
            if is_casing:
                pygame.draw.rect(screen, color, (x, y, size, size * 2.2))
            else:
                pygame.draw.circle(screen, color, (x, y), size)

    def draw_snow(self, screen):
        """눈송이: 화면에서 천천히 떨어지고, 고개를 돌리면 옆으로 흘러가요"""
        t = pygame.time.get_ticks() / 1000
        shift = self.player.angle / self.fov * WIDTH
        for x0, y0, speed in self.snowflakes:
            x = (x0 * WIDTH - shift + math.sin(t + y0 * 10) * 15) % WIDTH
            y = (y0 + t * speed) % 1.0 * HEIGHT
            size = 2 if speed > 0.14 else 1
            pygame.draw.circle(screen, (240, 245, 255), (x, y), size * UI)

    def draw_rain(self, screen):
        """빗줄기: 비스듬히 빠르게 떨어져요"""
        t = pygame.time.get_ticks() / 1000
        shift = self.player.angle / self.fov * WIDTH
        length = 22 * UI
        for x0, y0, speed in self.snowflakes:
            y = (y0 + t * speed * 9) % 1.0 * HEIGHT
            x = (x0 * WIDTH - shift + y * 0.25) % WIDTH
            pygame.draw.line(screen, (150, 165, 200), (x, y), (x - length * 0.25, y + length), 1)

    def draw_sky(self, screen):
        horizon = self.horizon
        screen.blit(self.sky, (0, horizon - self.sky.get_height()))
        # 해 (노을 맵은 서쪽 바다 위, 하버는 동쪽에서 떠올라요)
        sun = self.theme["sun"]
        rel = angle_diff(sun, self.player.angle) if sun is not None else math.pi
        if abs(rel) < self.fov / 2 + 0.3:
            z = min(2, self.zoom)            # 조준경으로 봐도 해가 화면을 다 가리지 않게
            x = WIDTH / 2 + math.tan(rel) * self.proj
            y = horizon - 45 * UI * z
            outer, middle, inner = self.theme.get("sun_colors", ((255, 200, 140), (255, 225, 160), (255, 245, 210)))
            pygame.draw.circle(screen, outer, (x, y), 70 * UI * z)
            pygame.draw.circle(screen, middle, (x, y), 48 * UI * z)
            pygame.draw.circle(screen, inner, (x, y), 34 * UI * z)
        pygame.draw.rect(screen, FLOOR_COLORS[self.theme["ground"]], (0, horizon, WIDTH, max(0, HEIGHT - horizon)))

    def draw_world(self, screen):
        p = self.player
        horizon, proj, eye, fog_dist, col_w = self.horizon, self.proj, self.eye, self.fog_dist, self.col_w
        key = (self.num_rays, col_w, proj)
        if getattr(self, "ray_table_key", None) != key:
            # 세로 줄마다 바라보는 방향(가운데에서 벌어진 각도)과 물고기 눈 보정 값은 시야가 같으면 늘 같아요: 한 번만 계산
            self.ray_table_key = key
            self.ray_table = []
            for i in range(self.num_rays):
                offset = math.atan(((i + 0.5) * col_w - WIDTH / 2) / proj)
                self.ray_table.append((offset, math.cos(offset)))
        # 반복문 안에서 자주 쓰는 것들을 지역 이름으로 (파이썬은 지역 이름이 더 빨라요)
        draw_rect, blit, fill, scale = pygame.draw.rect, screen.blit, screen.fill, pygame.transform.scale
        wall_textures, game_map, zbuffer, wall_top, wall_thin = (self.wall_textures, GAME_MAP, self.zbuffer,
                                                                 self.wall_top, self.wall_thin)
        wall_hit, decals, broken = self.wall_hit, self.decals, self.broken_windows
        px, py, angle = p.pos.x, p.pos.y, p.angle
        textured = col_w <= MAX_TEXTURE_COL
        light = self.light_timer > 0
        for i, (offset, fix) in enumerate(self.ray_table):
            # i번째 세로 줄이 바라보는 방향. 화면에 평평하게 펼쳐지도록 tan으로 계산해요
            floors, walls = cast_ray(px, py, angle + offset)
            x = i * col_w

            # 1) 바닥: 구간마다 색을 칠해요 (멀수록 지평선 가까이)
            for d0, d1, kind in floors:
                y_near = HEIGHT if d0 < 0.05 else horizon + eye * proj / (d0 * fix)
                y_far = horizon if d1 == math.inf else horizon + eye * proj / (d1 * fix)
                if y_near > y_far and y_far < HEIGHT:
                    # 바닥은 벽보다 안개를 약하게 (바다가 회색으로 안 보이게)
                    color = fog(FLOOR_COLORS[kind], (min(d1, fog_dist) + d0) * 0.3, fog_dist)
                    draw_rect(screen, color, (x, y_far, col_w, min(HEIGHT, y_near) - y_far + 1))

            # 2) 건물: 먼 것부터 그려야 가까운 것이 앞에 보여요
            zbuffer[i] = walls[0][0] * fix if walls else math.inf
            if walls:
                near = proj / max(0.05, walls[0][0] * fix)
                wall_top[i] = horizon + eye * near - walls[0][3][1] * near
                wall_thin[i] = walls[0][3][1] <= 1.0          # 상자, 모래주머니, 돌담, 쓰레기통
                first = walls[0]
                wall_hit[i] = (first[4], first[5], first[1], first[2], first[3])
            else:
                wall_hit[i] = None
                wall_thin[i] = False
                wall_top[i] = HEIGHT
            # 가까운 벽부터 보며, 앞 벽에 가려지는 아래쪽은 그리지 않아요 (같은 곳을 두 번 칠하지 않게)
            clip = float(HEIGHT)
            spans = []
            for dist, vertical, wall_x, spec, cx, cy in walls:
                perp = max(0.05, dist * fix)
                size = proj / perp
                bottom = horizon + eye * size
                top = bottom - spec[1] * size
                if top < clip:
                    spans.append((perp, size, bottom, top, min(bottom, clip), vertical, wall_x, spec, cx, cy))
                    clip = top
            for perp, size, bottom, top, vis_b, vertical, wall_x, (color, height, pattern, neon), cx, cy in spans:
                if top > HEIGHT or vis_b < 0:
                    continue
                textures = None
                if textured and perp < TEXTURE_DISTANCE:     # 먼 벽은 안개에 묻혀서 단색으로
                    textures = wall_textures.get(game_map[cy][cx])
                if textures:
                    # 질감: 그림에서 세로 한 줄을 잘라 화면 높이만큼 늘려 붙여요 (보이는 부분만)
                    level = min(FOG_LEVELS - 1, int(min(1.0, perp / fog_dist) * (FOG_LEVELS - 1) + 0.5))
                    tex = textures[0 if vertical else 1][level]
                    tex_h = tex.get_height()
                    vis_top, vis_bottom = max(0.0, top), min(float(HEIGHT), vis_b)
                    if vis_bottom - vis_top < 1:
                        continue
                    v0 = int((vis_top - top) / (bottom - top) * tex_h)
                    v1 = max(v0 + 1, min(tex_h, int((vis_bottom - top) / (bottom - top) * tex_h + 1)))
                    strip = tex.subsurface((min(TEX - 1, int(wall_x * TEX)), v0, 1, v1 - v0))
                    blit(scale(strip, (col_w, int(vis_bottom - vis_top) + 1)), (x, vis_top))
                else:
                    base = shade(color, 0.82 if vertical else 1.0)
                    if wall_x < 0.03 or wall_x > 0.97:      # 건물 모서리 선
                        base = shade(base, 0.6)
                    elif pattern == "ribs" and (wall_x * 6) % 1 < 0.2:   # 컨테이너/창고의 세로 골
                        base = shade(base, 0.75)
                    draw_rect(screen, fog(base, perp, fog_dist), (x, top, col_w, vis_b - top + 1))
                if perp < 14:
                    # 벽 아래쪽 그림자 (땅과 닿는 곳이 어두워서 건물이 땅에 붙어 보여요)
                    shadow_top = max(top, bottom - 0.12 * size)
                    if shadow_top < min(HEIGHT, vis_b):
                        fill((150, 150, 155), (x, shadow_top, col_w, min(HEIGHT, vis_b) - shadow_top + 1),
                                    special_flags=pygame.BLEND_MULT)
                    if light and perp < 5:      # 총구 불빛이 가까운 벽을 비춰요
                        k = int(self.muzzle_glow * (1 - perp / 5))
                        fill((k, int(k * 0.8), int(k * 0.5)), (x, max(0, top), col_w, min(HEIGHT, vis_b) - max(0, top)),
                                    special_flags=pygame.BLEND_ADD)
                # 창문: 층마다 두 칸씩. 몇몇 창문은 불이 켜져 있어요
                if pattern is True and (0.18 < wall_x < 0.42 or 0.58 < wall_x < 0.82):
                    dark_glass = fog((60, 80, 120) if vertical else (90, 110, 150), perp, fog_dist)
                    lit_glass = fog((255, 215, 140), perp * 0.5, fog_dist)
                    half = 0 if wall_x < 0.5 else 1
                    for k in range(int(height / 0.5)):
                        y0 = bottom - (k * 0.5 + 0.42) * size
                        y1 = min(vis_b, bottom - (k * 0.5 + 0.17) * size)
                        if y1 > max(0, y0) and y0 < HEIGHT:
                            if broken and (cx, cy, vertical, half, k) in broken:     # 깨진 창문: 시커먼 구멍
                                draw_rect(screen, (14, 14, 18), (x, y0, col_w, y1 - y0))
                                continue
                            lit = (cx * 7 + cy * 13 + k * 5 + half * 3 + vertical) % LIT == 0
                            draw_rect(screen, lit_glass if lit else dark_glass, (x, y0, col_w, y1 - y0))
                # 총알 자국과 폭발 그을음
                marks = decals.get((cx, cy, vertical)) if decals else None
                if marks:
                    for mx_, mv, kind in marks:
                        gap = abs(mx_ - wall_x)
                        if kind == "hole" and gap < 0.03:
                            hy = bottom - mv * size
                            hs = max(2.0, 0.035 * size)
                            if hy < vis_b:
                                draw_rect(screen, (30, 26, 24), (x, hy - hs / 2, col_w, hs))
                        elif kind == "scorch" and gap < 0.32:
                            half_h = 0.32 * size * math.sqrt(1 - (gap / 0.32) ** 2)
                            y0 = max(top, bottom - mv * size - half_h)
                            y1 = min(vis_b, bottom - mv * size + half_h)
                            if y1 > y0:
                                fill((95, 88, 82), (x, y0, col_w, y1 - y0), special_flags=pygame.BLEND_MULT)
                # 네온사인: 건물 꼭대기에 빛나는 띠 (안개를 덜 타서 멀리서도 잘 보여요)
                if neon:
                    glow = fog(neon, perp * 0.3, fog_dist)
                    draw_rect(screen, glow, (x, top + 0.06 * size, col_w, max(2, 0.07 * size)))

    def draw_sprites(self, screen):
        items = []     # (화면 위치, 그림, 적 또는 None)
        for enemy in self.enemies:
            box = self.enemy_box(enemy)
            if box:
                if enemy.flinch > 0:
                    state = enemy.flinch_pose
                elif enemy.hurt_timer > 0:
                    state = "hurt"
                elif enemy.flash_timer > 0:
                    state = "flash"
                elif enemy.aiming:
                    state = "aim"
                else:
                    state = "normal"
                    # 등을 보이고 있으면 뒷모습, 걷고 있으면 다리를 번갈아 들어요
                    prefix = "back_" if (self.player.pos - enemy.pos).dot(enemy.facing) < 0 else ""
                    step = int(enemy.walk / 0.32) % 4 if enemy.moving > 0 else 0
                    name = prefix + ("walk0", "", "walk1", "")[step]
                    name = {"": "normal", "back_": "back"}.get(name, name)
                    if (enemy.kind, name) in self.enemy_images:
                        state = name
                items.append((box, self.enemy_images[(enemy.kind, state)], enemy))
        for d in self.decor:
            box = self.project(d.pos, d.height, d.width)
            if box:
                items.append((box, d.image, None))
        t = pygame.time.get_ticks() / 1000
        for item in self.pickups:
            box = self.project(item.pos, 0.3, 0.4, lift=0.08 + math.sin(t * 3 + item.phase) * 0.05)
            if box:
                items.append((box, self.pickup_images[item.kind], None))
        for proj in self.projectiles:
            if proj.kind in ("grenade", "shell"):
                img, h, w = self.grenade_image, 0.18, 0.15
            else:
                img, h, w = self.rocket_image, 0.2, 0.35
            box = self.project(proj.pos, h, w, lift=proj.z)
            if box:
                items.append((box, img, None))
        for pos, size in self.splats:
            box = self.project(pos, 0.08, size)
            if box:
                items.append((box, self.blood_pool, None))
        for corpse in self.corpses:
            frame = min(2, int(corpse.age / corpse.frame_time))
            img, h, w = self.corpse_frames[(corpse.kind, corpse.side)][frame]
            box = self.project(corpse.pos, h, w, lift=corpse.z)
            if box:
                items.append((box, img, None))
        for sentry in self.sentries:
            box = self.project(sentry.pos, 0.55, 0.5)
            if box:
                items.append((box, self.sentry_images[1 if sentry.flash > 0 else 0], None))
        o = self.objective
        if o and not (o["done"] and o["kind"] == "HOSTAGE"):
            height, width = {"HOSTAGE": (0.6, 0.45), "BOMB": (0.45, 0.4), "HOLD": (1.4, 0.6),
                             "REACH": (1.4, 0.6), "CACHE": (0.45, 0.4)}[o["kind"]]
            box = self.project(o["pos"], height, width)
            if box:
                items.append((box, self.objective_images[o["kind"]], None))
        for effect in self.effects:
            size = effect.size * (0.5 + 0.5 * effect.age / effect.duration)
            box = self.project(effect.pos, size, size, lift=0.6 - size / 2)
            if box:
                items.append((box, effect.frame, None))
        # 먼 것부터 그려야 가까운 것이 앞에 보여요
        items.sort(key=lambda item: -item[0][4])
        lights = []
        if self.night:                             # 밤: 가로등 불빛과 바닥의 빛 웅덩이
            for d in self.decor:
                if d.glow:
                    box = self.project(d.pos, d.height, d.width)
                    if box:
                        lights.append(box)
        for box, img, enemy in items:
            self.draw_sprite_columns(screen, img, *box)
            if enemy and enemy.hp < enemy.t["hp"]:
                self.draw_hp_bar(screen, enemy, box)
            if enemy and enemy.reload_left > 0 and box[4] < 14:   # 재장전 중: 지금이 기회!
                col = int(box[0] // self.col_w)
                if 0 <= col < self.num_rays and box[4] < self.zbuffer[col]:
                    label = self.fonts["tiny"].render("RELOADING", True, YELLOW)
                    screen.blit(label, label.get_rect(midbottom=(box[0], box[1] - 14 * UI)))
            if enemy and enemy.callout and box[4] < 18:     # 적의 외침 말풍선
                col = int(box[0] // self.col_w)
                if 0 <= col < self.num_rays and box[4] < self.zbuffer[col] + 0.3:
                    label = self.fonts["tiny"].render(enemy.callout[0], True, BLACK)
                    bubble = label.get_rect(midbottom=(box[0], box[1] - 30 * UI)).inflate(10 * UI, 6 * UI)
                    pygame.draw.rect(screen, WHITE, bubble, border_radius=int(5 * UI))
                    pygame.draw.polygon(screen, WHITE, [(box[0] - 4 * UI, bubble.bottom - 1), (box[0] + 4 * UI, bubble.bottom - 1),
                                                        (box[0], bubble.bottom + 6 * UI)])
                    screen.blit(label, label.get_rect(center=bubble.center))
            if enemy and enemy.heal_flash > 0:     # 치료받는 중: 머리 위에 초록 +
                sx, top = box[0], box[1]
                size = max(4, int(10 * UI))
                pygame.draw.rect(screen, (80, 255, 120), (sx - size / 2, top - 3.2 * size, size, size / 3))
                pygame.draw.rect(screen, (80, 255, 120), (sx - size / 6, top - 3.6 * size, size / 3, size * 1.1))
        if lights:
            self.draw_lights(screen, lights)
        # 레이저 저격수: 총구에서 내 쪽으로 빨간 선. 쏠 때가 다가올수록 조준점에 가까워져요
        for enemy in self.enemies:
            if enemy.kind != "LASER" or not enemy.sees or enemy.spotted < 0.3 or enemy.reload_left > 0:
                continue
            box = self.enemy_box(enemy)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            col = int(sx // self.col_w)
            if not (0 <= col < self.num_rays) or perp > self.zbuffer[col] + 0.3:
                continue
            start = (sx + w * 0.3, top + (bottom - top) * 0.45)
            spread = min(1.0, enemy.shoot_timer / 2.0) * 160 * UI
            t = pygame.time.get_ticks() / 300 + id(enemy) % 7
            end = (WIDTH / 2 + math.sin(t) * spread, HEIGHT / 2 + 40 * UI + math.cos(t * 1.3) * spread * 0.6)
            pygame.draw.line(screen, (255, 40, 40), start, end, max(1, int(2 * UI)))
            pygame.draw.circle(screen, (255, 120, 120), end, max(2, int(4 * UI)))

    def draw_lights(self, screen, lights):
        for sx, top, bottom, w, perp in lights:
            col = int(sx // self.col_w)
            if not (0 <= col < self.num_rays) or perp > self.zbuffer[col] + 0.5:
                continue                                # 건물 뒤에 가려진 가로등
            size = int(min(WIDTH, (bottom - top) * 1.1))
            if size < 4:
                continue
            glow = pygame.transform.scale(self.glow_image, (size, size))
            screen.blit(glow, glow.get_rect(center=(sx, top + (bottom - top) * 0.05)), special_flags=pygame.BLEND_ADD)
            pool = pygame.transform.scale(self.glow_image, (size * 2, max(2, size // 3)))
            screen.blit(pool, pool.get_rect(center=(sx, bottom)), special_flags=pygame.BLEND_ADD)

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
        """그림을 그리되, 건물보다 뒤에 있는 세로 줄은 건너뛰어요.

        화면에 보이는 부분만 잘라서 한 번에 늘린 뒤, 보이는 줄끼리 묶어서 붙여요.
        그래서 아주 가까이 있어도, 장식물이 많아도 느려지지 않아요.
        """
        h = bottom - top
        x0 = sx - w / 2
        vis_top, vis_bottom = max(0.0, top), min(float(HEIGHT), bottom)
        vis_left, vis_right = max(0.0, x0), min(float(WIDTH), x0 + w)
        if vis_bottom - vis_top < 1 or vis_right - vis_left < 1:
            return
        col_w, zbuffer = self.col_w, self.zbuffer
        first, last = int(vis_left // col_w), int((vis_right - 1) // col_w)
        if all(perp >= zbuffer[col] for col in range(first, last + 1)):
            return                                    # 전부 건물 뒤에 숨어 있음

        # 1) 그림에서 화면에 보이는 부분만 잘라서 한 번에 늘리기
        img_w, img_h = img.get_size()
        u0 = int((vis_left - x0) / w * img_w)
        u1 = min(img_w, max(u0 + 1, math.ceil((vis_right - x0) / w * img_w)))
        v0 = int((vis_top - top) / h * img_h)
        v1 = min(img_h, max(v0 + 1, math.ceil((vis_bottom - top) / h * img_h)))
        part_w, part_h = int(vis_right - vis_left) + 1, int(vis_bottom - vis_top) + 1
        part = pygame.transform.scale(img.subsurface((u0, v0, u1 - u0, v1 - v0)), (part_w, part_h))

        # 2) 건물보다 앞에 있는 줄들을 묶어서 붙이기
        run_start = None
        for col in range(first, last + 2):
            visible = col <= last and perp < zbuffer[col]
            if visible and run_start is None:
                run_start = col
            elif not visible and run_start is not None:
                left = max(vis_left, run_start * col_w)
                right = min(vis_right, col * col_w)
                screen.blit(part, (left, vis_top), area=pygame.Rect(left - vis_left, 0, right - left, part_h))
                run_start = None

    def draw_gun(self, screen):
        """미리 그려 둔 총 그림을 움직임에 맞춰 흔들어 그려요.
        걸으면 8자로 흔들리고, 달리면 내려가고, 쏘면 뒤로 밀리고, 숨 쉬듯 살짝 움직여요."""
        a = self.arsenal
        p = self.player
        ads = self.aiming
        key = (a.current.spec["name"], ads, a.current.spec.get("camo"))
        if key not in self.viewmodels:
            self.viewmodels[key] = make_viewmodel(*key)
        image, (ox, oy), (mx, my) = self.viewmodels[key]
        t = pygame.time.get_ticks() / 1000
        calm = 0.3 if ads else 1.0
        if p.sprinting:
            bx, by = math.sin(t * 14) * 16 * UI + 30 * UI, abs(math.cos(t * 14)) * 12 * UI + 50 * UI
        elif p.moving and p.z == 0:
            bx, by = math.sin(t * 8) * 10 * UI * calm, abs(math.cos(t * 8)) * 8 * UI * calm
        else:
            bx, by = 0.0, math.sin(t * 2) * 3 * UI * calm      # 숨쉬기
        down = 0
        tilt = 0.0
        prog = 1 - a.reload_left / a.reload_total if a.reload_left > 0 else None
        if prog is not None and a.shell:
            # 한 발씩 장전: 총을 기울인 채로, 한 발 넣을 때마다 살짝 들썩
            down = 70 + 18 * math.sin(prog * math.pi)
            bx -= 40 * UI
            prog = None
            shell_prog = 1 - a.reload_left / a.reload_total
        else:
            shell_prog = None
        if prog is not None:
            # 재장전: 총을 내리며 기울이고, 탄창을 빼고 끼운 뒤 다시 올려요
            down = 110 * math.sin(min(1.0, prog * 1.15) * math.pi) + 30
            bx -= 50 * UI * math.sin(prog * math.pi)
        elif a.switch_left > 0:
            down = 220 * a.switch_left / a.SWITCH_TIME
        if self.bolt_anim > 0:                      # 노리쇠: 총을 살짝 내리고 오른쪽으로 비틀었다 돌아와요
            k = math.sin((1 - self.bolt_anim / 0.75) * math.pi)
            down += 45 * k
            bx += 25 * UI * k
        if self.ads_anim > 0:                       # 정조준 전환: 잠깐 내려갔다 올라와요
            down += 55 * math.sin(self.ads_anim / 0.16 * math.pi)
        if self.inspect_timer > 0:                  # 살펴보기: 총을 왼쪽으로 돌려 옆면을 보여줘요
            k = math.sin((1 - self.inspect_timer / 2.4) * math.pi)
            tilt = 22 * k
            bx -= 160 * UI * k
            down -= 30 * k
        if ads:
            kx, ky = 0, a.kick * 12 * UI
        else:
            kx, ky = a.kick * 12 * UI, a.kick * 20 * UI
        dx = bx + kx + self.sway * calm
        dy = by + ky + down * UI + p.crouch_amt * 10 * UI
        if tilt:
            turned = pygame.transform.rotate(image, tilt)
            screen.blit(turned, turned.get_rect(center=(ox + dx + image.get_width() / 2, oy + dy + image.get_height() / 2)))
        else:
            screen.blit(image, (ox + dx, oy + dy))
        self.muzzle_screen = (mx + dx, my + dy)
        if shell_prog is not None:                  # 산탄총 탄이 아래에서 올라와 들어가요
            sx = ox + dx + image.get_width() * 0.45
            sy = oy + dy + image.get_height() * 0.62 + (1 - shell_prog) * 90 * UI
            pygame.draw.rect(screen, (200, 40, 40), (sx, sy, 12 * UI, 26 * UI), border_radius=3)
            pygame.draw.rect(screen, (210, 175, 70), (sx, sy + 18 * UI, 12 * UI, 8 * UI))
            draw_glove(screen, pygame.Vector2(sx + 6 * UI, sy + 34 * UI), 20 * UI)
        for x, y, vx, vy, life, size in self.smoke:      # 총구 연기 (같은 크기·진하기 그림은 한 번만 만들어요)
            key = (int(size), int(6 * min(1.0, life)))
            puff = self.puff_cache.get(key)
            if puff is None:
                r = key[0]
                puff = pygame.Surface((r * 2 + 2, r * 2 + 2), pygame.SRCALPHA)
                pygame.draw.circle(puff, (200, 200, 205, 15 * key[1]), (r + 1, r + 1), r)
                self.puff_cache[key] = puff
            screen.blit(puff, (mx + dx + x - size, my + dy + y - size))
        if prog is not None and not a.current.spec["projectile"]:
            # 탄창: 0.2~0.45 사이엔 빠져서 아래로 떨어지고, 0.5~0.75 사이엔 올라와 끼워져요
            mag_x = ox + dx + image.get_width() * 0.42
            mag_y = oy + dy + image.get_height() * 0.62
            if 0.2 < prog < 0.45:
                drop = (prog - 0.2) / 0.25
                pygame.draw.rect(screen, GUN_DARK, (mag_x, mag_y + drop * 180 * UI, 22 * UI, 46 * UI), border_radius=4)
            elif 0.5 < prog < 0.75:
                rise = 1 - (prog - 0.5) / 0.25
                pygame.draw.rect(screen, GUN_DARK, (mag_x, mag_y + rise * 140 * UI, 22 * UI, 46 * UI), border_radius=4)
                draw_glove(screen, pygame.Vector2(mag_x + 11 * UI, mag_y + rise * 140 * UI + 50 * UI), 22 * UI)
        if a.kick > 0.6:
            big = a.current.spec["name"] in ("SHOTGUN", "ROCKET", "SNIPER")
            size = (22 if ads else 34) * UI * (1.4 if big else 1.0) * (0.45 if a.current.spec.get("suppressed") else 1.0)
            draw_muzzle_flash(screen, (mx + dx, my + dy), size)

    def draw_knife(self, screen):
        """칼 휘두르기: 오른쪽 아래에서 가운데 위쪽으로 베는 모양"""
        p = 1 - self.knife_timer / KNIFE_TIME        # 0 → 1
        base = pygame.Vector2(WIDTH * (0.78 - 0.25 * p), HEIGHT * (1.0 - 0.15 * math.sin(p * math.pi)))
        d = pygame.Vector2(-0.3 - 0.6 * p, -1).normalize()   # 칼날 방향: 점점 왼쪽으로 기울어요
        side = pygame.Vector2(-d.y, d.x)
        tip = base + d * 200 * UI
        draw_sleeve(screen, base - d * 60 * UI, pygame.Vector2(WIDTH * 1.05, HEIGHT * 1.15), 44 * UI)
        pygame.draw.polygon(screen, (210, 215, 225), [base + side * 10 * UI, tip, base - side * 10 * UI])
        pygame.draw.line(screen, (150, 155, 165), base, tip, 2)
        pygame.draw.line(screen, (30, 30, 30), base, base - d * 70 * UI, int(20 * UI))
        draw_glove(screen, base - d * 40 * UI, 26 * UI)

    def draw_hud(self, screen):
        font, big_font = self.font, self.big_font
        # 다치면 화면 가장자리가 붉게 (체력이 낮을수록 진하게)
        for i, (x, y, r, t) in enumerate(self.screen_blood):     # 화면에 묻은 피
            img = self.splat_images[i % len(self.splat_images)]
            if r != 1.0:
                img = pygame.transform.scale(img, (int(img.get_width() * r), int(img.get_height() * r)))
            img.set_alpha(int(255 * min(1.0, t / 1.5)))
            screen.blit(img, img.get_rect(center=(x, y)))
        if self.suppress > 0.05:                                  # 제압: 화면 가장자리가 어두워져요
            self.dark_vignette.set_alpha(int(200 * min(1.0, self.suppress)))
            screen.blit(self.dark_vignette, (0, 0))
        low = max(0.0, 1 - self.player.hp / 60) if self.player.hp < 60 else 0.0
        strength = min(1.0, max(self.damage_flash, low))
        if strength > 0:
            self.hurt_vignette.set_alpha(int(255 * strength))
            screen.blit(self.hurt_vignette, (0, 0))

        # 조준선 (화면 가운데). 총알이 퍼지는 만큼 벌어져요. 정조준 중엔 빨간 점
        cx, cy = WIDTH / 2, HEIGHT / 2
        spec = self.arsenal.current.spec
        if self.aiming:
            pass                                   # 정조준: 총의 조준기(도트사이트/가늠쇠)로 조준해요
        elif not self.scoped and not self.player.sprinting:
            gap = 5 * UI + self.current_spread(spec) * 0.6
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                start = (cx + dx * gap, cy + dy * gap)
                end = (cx + dx * (gap + 10 * UI), cy + dy * (gap + 10 * UI))
                pygame.draw.line(screen, RED if self.on_target else GREEN, start, end, 2)
        if self.hitmarker > 0:
            # 히트마커: 맞히면 하얀 X, 쓰러뜨리면 빨간 X, 헤드샷이면 크게. 처음에 살짝 커졌다가 줄어요
            color = RED if self.hitmarker_kill else WHITE
            grow = 1 + self.hitmarker * 2
            inner, outer = 6 * UI * grow, (16 if self.hit_head else 12) * UI * grow
            width = 3 if self.hitmarker_kill or self.hit_head else 2
            for dx, dy in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
                pygame.draw.line(screen, color, (cx + dx * inner, cy + dy * inner),
                                 (cx + dx * outer, cy + dy * outer), width)

        # 맞은 방향: 조준점 둘레에 빨간 화살표 (위 = 앞, 아래 = 뒤)
        for angle, t in self.damage_dirs:
            rel = angle_diff(angle, self.player.angle)
            d = pygame.Vector2(math.sin(rel), -math.cos(rel))
            side = pygame.Vector2(-d.y, d.x)
            tip = pygame.Vector2(cx, cy) + d * 150 * UI
            base = pygame.Vector2(cx, cy) + d * 120 * UI
            color = (255, int(40 + 60 * (1 - t)), 40)
            pygame.draw.polygon(screen, color, [tip, base + side * 26 * UI, base - side * 26 * UI])

        # 소리 표시: 발소리는 회색 점, 총소리·폭발은 주황 삼각형 (위 = 앞)
        for angle, kind, t in self.sound_marks:
            rel = angle_diff(angle, self.player.angle)
            d = pygame.Vector2(math.sin(rel), -math.cos(rel))
            spot = pygame.Vector2(cx, cy) + d * 100 * UI
            alpha = min(1.0, t / 0.4)
            if kind == "step":
                pygame.draw.circle(screen, (int(200 * alpha), int(200 * alpha), int(210 * alpha)), spot, 5 * UI)
            else:
                side = pygame.Vector2(-d.y, d.x)
                pygame.draw.polygon(screen, (255, int(150 * alpha), 30), [spot + d * 10 * UI, spot - d * 6 * UI + side * 8 * UI,
                                                                         spot - d * 6 * UI - side * 8 * UI])

        # 점수/메달 글자 (조준점 아래)
        for i, (text, color, t) in enumerate(self.popups[-4:]):
            self.center_text(screen, font, text, color, HEIGHT * 0.58 + i * 30 * UI)

        # 적 수류탄이 가까이 있으면 경고 (깜빡여요)
        danger = any(p.owner == "enemy" and p.pos.distance_to(self.player.pos) < 4.5 for p in self.projectiles)
        if danger and pygame.time.get_ticks() // 150 % 2 == 0:
            self.center_text(screen, big_font, "GRENADE!", RED, HEIGHT * 0.38)

        # FOCUS: 화면이 푸르스름해져요 / SCAN: 벽 너머 적 위치 표시
        if self.focus > 0:
            tint = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            tint.fill((60, 120, 255, 45))
            screen.blit(tint, (0, 0))
        if self.scan > 0:
            for enemy in self.enemies:
                box = self.enemy_box(enemy)
                if box:
                    sx, top = box[0], box[1]
                    size = 7 * UI
                    pygame.draw.polygon(screen, RED, [(sx, top - 2 * size), (sx + size, top - size),
                                                      (sx, top), (sx - size, top - size)], 2)
        # 액티브 스킬 (오른쪽 가운데)
        y_skill = HEIGHT * 0.45
        for name, (duration, cooldown) in ACTIVE_SKILLS.items():
            if not self.rank_of(name):
                continue
            key = next(k for n, _, _, _, k in SKILLS if n == name)
            left = self.cooldowns.get(name, 0)
            text = f"[{key}] {name}" + (f"  {left:.0f}s" if left > 0 else "  READY")
            image = self.fonts["tiny"].render(text, True, (120, 120, 130) if left > 0 else (80, 240, 255))
            screen.blit(image, image.get_rect(topright=(WIDTH - 16, y_skill)))
            y_skill += 20 * UI
        # 왼쪽 아래: 킬스트릭 (받은 것 / 다음 것까지)
        y = HEIGHT - 100 * UI
        if self.streaks_ready:
            for name in reversed(self.streaks_ready):
                image = self.small_font.render(f"[X] {name}", True, (80, 240, 255))
                screen.blit(image, (24, y))
                y -= 22 * UI
        upcoming = [(need, name) for need, name in STREAKS if need > self.streak]
        streak_text = f"STREAK {self.streak}"
        if upcoming:
            streak_text += f"   next: {upcoming[0][1]} at {upcoming[0][0]}"
        screen.blit(self.small_font.render(streak_text, True, WHITE), (24, y))
        state = "SLIDE" if self.player.slide_timer > 0 else ("CROUCH" if self.player.crouch else "")
        if self.player.sprinting:
            state = "SPRINT"
        if state:
            screen.blit(self.small_font.render(state, True, YELLOW), (24, y - 22 * UI))

        # 왼쪽 아래 체력, 오른쪽 아래 총알과 수류탄
        hp_color = GREEN if self.player.hp > 40 else RED
        screen.blit(big_font.render(f"+ {int(self.player.hp)}", True, hp_color), (24, HEIGHT - 70 * UI))
        w = self.arsenal.current
        ammo = "RELOADING..." if self.arsenal.reload_left > 0 else f"{w.mag} / {w.reserve}"
        image = big_font.render(ammo, True, WHITE)
        rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, HEIGHT - 20 * UI)))
        image = font.render(f"GRENADE x{self.arsenal.grenades}", True, YELLOW)
        rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 4)))
        if self.mode == "zombies":
            image = font.render(f"POINTS {self.points}", True, (255, 200, 60))
            rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 4)))
            shop = f"B ammo {ZOMBIE_SHOP['ammo']}   U upgrade {ZOMBIE_SHOP['upgrade']}"
            image = self.fonts["tiny"].render(shop, True, WHITE)
            screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 2)))

        # 아래 가운데 무기 칸
        slot_w = 76 * UI
        if len(self.arsenal.weapons) <= 3:
            slot_w = 150 * UI                     # 로드아웃(무기 2개)은 칸을 넓게
        slot_w = min(slot_w, (WIDTH - 40) / len(self.arsenal.weapons))
        left = WIDTH / 2 - slot_w * len(self.arsenal.weapons) / 2
        for i, weapon in enumerate(self.arsenal.weapons):
            rect = pygame.Rect(left + i * slot_w + 3, HEIGHT - 44 * UI, slot_w - 6, 30 * UI)
            selected = i == self.arsenal.index
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 220, 90, 200) if selected else (0, 0, 0, 120))
            screen.blit(panel, rect)
            level = weapon.spec.get("level", 1)
            name = weapon.spec["name"] + (" +" if weapon.upgraded else "") + (f" L{level}" if level > 1 else "")
            color = BLACK if selected else ((255, 200, 60) if weapon.upgraded else WHITE)
            label = self.fonts["tiny"].render(f"{i + 1} {name}", True, color)
            screen.blit(label, label.get_rect(center=rect.center))
        if self.perk:
            label = self.fonts["tiny"].render(f"PERK: {self.perk}", True, (80, 240, 255))
            screen.blit(label, label.get_rect(center=(WIDTH / 2, HEIGHT - 54 * UI)))

        self.draw_compass(screen)
        boss = next((e for e in self.enemies if e.kind == "BOSS"), None)
        if boss:
            bar = pygame.Rect(WIDTH * 0.3, HEIGHT * 0.075 + 28 * UI, WIDTH * 0.4, 10 * UI)
            pygame.draw.rect(screen, (40, 20, 25), bar)
            fill_rect = pygame.Rect(bar.x, bar.y, int(bar.w * max(0.0, boss.hp) / boss.t["hp"]), bar.h)
            pygame.draw.rect(screen, (220, 40, 60) if getattr(boss, "phase", 1) < 3 else (255, 120, 40), fill_rect)
            pygame.draw.rect(screen, WHITE, bar, 1)
            for mark in (0.6, 0.3):                                     # 단계가 바뀌는 곳
                x = bar.x + bar.w * mark
                pygame.draw.line(screen, WHITE, (x, bar.y), (x, bar.bottom), 1)
            label = self.small_font.render(f"BOSS  PHASE {getattr(boss, 'phase', 1)}", True, WHITE)
            screen.blit(label, label.get_rect(midbottom=(WIDTH / 2, bar.y - 1)))
        # 위쪽 정보
        if self.mode == "mission":
            t = int(self.mission_time)
            info = (f"MISSION {self.theme['name']}   STAGE {min(self.stage + 1, len(MISSION_STAGES))}/"
                    f"{len(MISSION_STAGES)}   ENEMIES {len(self.enemies)}   KILLS {self.kills}   {t // 60}:{t % 60:02d}")
        elif self.mode == "training":
            info = f"TRAINING RANGE   {self.theme['name']}   TARGETS {len(self.enemies)}"
        elif self.challenge:
            t = self.challenge_time if self.challenge != "BLITZ" else max(0.0, BLITZ_TIME - self.challenge_time)
            info = (f"CHALLENGE {self.challenge}   {self.theme['name']}   ENEMIES {len(self.enemies)}   "
                    f"{'LEFT ' if self.challenge == 'BLITZ' else 'TIME '}{int(t) // 60}:{int(t) % 60:02d}")
        elif self.mode == "zombies":
            info = (f"WAVE {self.round}   {self.theme['name']}   "
                    f"ZOMBIES {len(self.enemies) + self.zombies_left}   KILLS {self.kills}")
        else:
            info = (f"ROUND {self.round}/{CAMPAIGN_ROUNDS}   SET {set_of(self.round)}   {self.theme['name']}   "
                    f"ENEMIES {len(self.enemies)}   KILLS {self.kills}")
        screen.blit(font.render(info, True, WHITE), (16, 12))
        # 계급과 경험치 막대
        rank_label = self.small_font.render(f"RANK {self.rank}", True, WHITE)
        screen.blit(rank_label, (16, 12 + 30 * UI))
        bar = pygame.Rect(16 + rank_label.get_width() + 10, 12 + 34 * UI, 140 * UI, 6 * UI)
        pygame.draw.rect(screen, (40, 40, 50), bar)
        bar.width = int(bar.width * (self.xp % XP_PER_RANK) / XP_PER_RANK)
        pygame.draw.rect(screen, (255, 80, 200), bar)
        if self.show_fps:
            text = f"FPS {self.fps:.0f}   RES {self.col_w}px   {WIDTH}x{HEIGHT}"
            screen.blit(self.small_font.render(text, True, YELLOW), (16, 12 + 54 * UI))
        map_bottom = self.draw_minimap(screen)
        for i, (text, _) in enumerate(self.feed[-4:]):
            image = font.render(text, True, YELLOW)
            screen.blit(image, image.get_rect(topright=(WIDTH - 12, map_bottom + 8 + i * 30 * UI)))

        if self.hint_timer > 0 and not self.game_over:
            hints = ["WASD move   SHIFT sprint   C crouch/slide   ARROWS look   SPACE jump   F fire   E aim",
                     f"G grenade   V knife   X killstreak   1-{len(self.arsenal.weapons)} weapon   R reload   H help (pause)"]
            for i, hint in enumerate(hints):
                self.center_text(screen, self.small_font, hint, WHITE, HEIGHT - (82 - i * 20) * UI)
        self.draw_objective(screen)
        if self.round_clear_timer > 0 or self.game_over:
            self.draw_summary(screen, HEIGHT * (0.66 if self.game_over else 0.5))
        if self.banner_timer > 0:
            self.center_text(screen, big_font, self.banner, YELLOW, HEIGHT / 3)
            for i, (text, color) in enumerate(self.sub_banners):
                self.center_text(screen, font, text, color, HEIGHT / 3 + (45 + i * 32) * UI)
            if self.round_clear_timer <= 0:
                typed = self.theme["brief"][:int(self.brief_age * 40)]
                y = HEIGHT / 3 + (45 + len(self.sub_banners) * 32) * UI
                self.center_text(screen, self.small_font, typed, (200, 230, 255), y)
        if self.game_over and self.mission_complete:
            t = int(self.mission_time)
            self.center_text(screen, big_font, "MISSION COMPLETE", (80, 240, 255), HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"{self.theme['name']}   Time {t // 60}:{t % 60:02d}   Kills {self.kills}",
                             WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, "R: play again    ESC: menu", YELLOW, HEIGHT / 2 + 45 * UI)
        elif self.game_over and self.challenge_done:
            self.center_text(screen, big_font, "CHALLENGE COMPLETE", (80, 240, 255), HEIGHT / 2 - 95 * UI)
            self.center_text(screen, font, f"{self.challenge}   TIME {self.challenge_time:.1f}s   BEST {self.challenge_best:.1f}s",
                             WHITE, HEIGHT / 2 - 45 * UI)
            self.center_text(screen, font, "R: try again    ESC: menu", YELLOW, HEIGHT / 2 - 12 * UI)
        elif self.game_over and self.challenge:
            self.center_text(screen, big_font, self.fail_reason or "CHALLENGE FAILED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"{self.challenge}   Kills {self.kills}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, "R: try again    ESC: menu", YELLOW, HEIGHT / 2 + 45 * UI)
        elif self.game_over and self.mode == "mission":
            self.center_text(screen, big_font, self.fail_reason or "YOU DIED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"Stage {self.stage + 1}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, "R: back to last checkpoint    ESC: menu", YELLOW, HEIGHT / 2 + 45 * UI)
        elif self.game_over and self.mode == "zombies":
            self.center_text(screen, big_font, "YOU DIED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"Survived to wave {self.round}  /  Kills {self.kills}  /  "
                                           f"Best wave {self.save.get('zbest', self.round)}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, "R: try again    ESC: menu", YELLOW, HEIGHT / 2 + 45 * UI)
        elif self.game_over:
            self.center_text(screen, big_font, self.fail_reason or "YOU DIED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"Round {self.round}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, f"R: retry round {self.round}    N: new game    ESC: menu",
                             YELLOW, HEIGHT / 2 + 45 * UI)

    def draw_objective(self, screen):
        """목표 위치 표시 (벽 너머로도 보여요), 거리, 진행 막대, 폭탄 타이머"""
        o = self.objective
        if not o or o["done"] or self.game_over:
            return
        info = OBJECTIVES[o["kind"]]
        offset = o["pos"] - self.player.pos
        dist = offset.length()
        rel = angle_diff(math.atan2(offset.y, offset.x), self.player.angle)
        if abs(rel) < self.fov / 2:
            x = WIDTH / 2 + math.tan(rel) * self.proj
        else:
            x = 40 * UI if rel < 0 else WIDTH - 40 * UI          # 화면 밖이면 가장자리에
        y = HEIGHT * 0.2
        size = 11 * UI
        pygame.draw.polygon(screen, info["color"], [(x, y - size), (x + size, y), (x, y + size), (x - size, y)])
        pygame.draw.polygon(screen, BLACK, [(x, y - size), (x + size, y), (x, y + size), (x - size, y)], 2)
        label = self.fonts["tiny"].render(f"{o['kind']}  {dist:.0f}m", True, info["color"])
        if self.mode == "mission":
            self.center_text(screen, self.small_font, f"STAGE {self.stage + 1}/{len(MISSION_STAGES)}:  {o['title']}",
                             info["color"], HEIGHT * 0.085)
        screen.blit(label, label.get_rect(midtop=(x, y + size + 3)))
        if o["kind"] == "BOMB":
            t = max(0, o["timer"])
            color = RED if t < 15 and pygame.time.get_ticks() // 250 % 2 else WHITE
            self.center_text(screen, self.font, f"BOMB  {int(t) // 60}:{int(t) % 60:02d}", color, HEIGHT * 0.12)
        if o["progress"] > 0:
            frac = min(1.0, o["progress"] / info["need"])
            bar = pygame.Rect(WIDTH / 2 - 150 * UI, HEIGHT * 0.66, 300 * UI, 14 * UI)
            pygame.draw.rect(screen, (30, 30, 40), bar)
            pygame.draw.rect(screen, info["color"], (bar.x, bar.y, bar.w * frac, bar.h))
            pygame.draw.rect(screen, WHITE, bar, 2)
            inside = self.player.pos.distance_to(o["pos"]) < info["radius"]
            text = f"{info['doing']}...  {frac * 100:.0f}%" if inside else "GET BACK TO THE OBJECTIVE"
            self.center_text(screen, self.small_font, text, info["color"], bar.y - 14 * UI)

    def draw_summary(self, screen, y):
        """라운드 결과: 명중률, 헤드샷, 처치, 최고 연속 처치, 가장 많이 쓴 무기"""
        st = self.stats
        accuracy = round(100 * st["hits"] / st["shots"]) if st["shots"] else 0
        top = max(st["weapons"], key=st["weapons"].get) if st["weapons"] else "-"
        text = (f"ACCURACY {accuracy}%    HEADSHOTS {st['heads']}    KILLS {st['kills']}    "
                f"BEST STREAK {st['best']}    TOP WEAPON {top}")
        image = self.small_font.render(text, True, WHITE)
        panel = pygame.Rect(0, 0, image.get_width() + 40 * UI, image.get_height() + 20 * UI)
        panel.center = (WIDTH / 2, y)
        shade_panel = pygame.Surface(panel.size, pygame.SRCALPHA)
        shade_panel.fill((0, 0, 0, 150))
        screen.blit(shade_panel, panel)
        pygame.draw.rect(screen, (255, 80, 200), panel, 2)
        screen.blit(image, image.get_rect(center=panel.center))

    def make_minimap(self):
        """미니맵 그림은 바뀌지 않으니 맵마다 한 번만 그려 둬요."""
        cell = self.minimap_cell
        mini = pygame.Surface((MAP_W * cell, MAP_H * cell), pygame.SRCALPHA)
        for row in range(MAP_H):
            for col in range(MAP_W):
                spec = WALL_GRID[row][col]
                color = spec[0] if spec else FLOOR_COLORS[FLOOR_GRID[row][col]]
                pygame.draw.rect(mini, (*color, 190), (col * cell, row * cell, cell, cell))
        return mini

    @property
    def minimap_cell(self):
        return max(3, int(4 * UI))

    def draw_minimap(self, screen):
        """오른쪽 위 작은 지도. 지도 아래쪽 y좌표를 돌려줘요."""
        cell = self.minimap_cell
        view_w, view_h = min(MAP_W, 34), min(MAP_H, 24)            # 큰 맵은 내 주변만 보여줘요
        left = max(0, min(MAP_W - view_w, int(self.player.pos.x - view_w / 2)))
        top = max(0, min(MAP_H - view_h, int(self.player.pos.y - view_h / 2)))
        x0, y0 = WIDTH - view_w * cell - 12, 12
        screen.blit(self.minimap, (x0, y0), area=pygame.Rect(left * cell, top * cell, view_w * cell, view_h * cell))
        ox, oy = x0 - left * cell, y0 - top * cell
        screen.set_clip(pygame.Rect(x0, y0, view_w * cell, view_h * cell))
        # 빨간 점: 방금 총을 쏜 적 (레이더를 켜면 모든 적)
        for enemy in self.enemies:
            if self.radar_timer > 0 or enemy.flash_timer > -0.6:
                pygame.draw.circle(screen, RED, enemy.pos * cell + (ox, oy), max(2, cell // 2 + 1))
        for sentry in self.sentries:
            pygame.draw.circle(screen, (80, 240, 255), sentry.pos * cell + (ox, oy), max(2, cell // 2))
        if self.objective and not self.objective["done"]:     # 목표 위치
            color = OBJECTIVES[self.objective["kind"]]["color"]
            pygame.draw.circle(screen, color, self.objective["pos"] * cell + (ox, oy), max(3, cell))
        p = self.player.pos * cell + (ox, oy)
        look = p + pygame.Vector2(math.cos(self.player.angle), math.sin(self.player.angle)) * 12
        pygame.draw.line(screen, BLACK, p, look, 2)
        pygame.draw.circle(screen, BLACK, p, 3)
        screen.set_clip(None)
        if self.radar_timer > 0:
            label = self.fonts["tiny"].render(f"RADAR {self.radar_timer:.0f}", True, (80, 240, 255))
            screen.blit(label, (x0, y0 + view_h * cell + 2))
        return y0 + view_h * cell + (16 * UI if self.radar_timer > 0 else 0)

    @staticmethod
    def center_text(screen, font, text, color, y):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, y)))


# ---------------------------------------------------------------
# 게임패드 (Xbox / PlayStation 컨트롤러를 블루투스로 연결하면 돼요)
# ---------------------------------------------------------------
# 버튼 -> 키보드 키 (게임 중). A 점프와 왼쪽 스틱 이동, 트리거는 따로 처리해요
PAD_GAME_KEYS = {"b": pygame.K_c, "x": pygame.K_r, "y": pygame.K_TAB, "rb": pygame.K_g, "lb": pygame.K_j,
                 "r3": pygame.K_v, "up": pygame.K_x, "down": pygame.K_b, "left": pygame.K_u, "start": pygame.K_ESCAPE,
                 "right": pygame.K_t, "back": pygame.K_y}
# 메뉴 화면에서: A 확인, B 뒤로, 십자키 이동, X 좀비 모드, Y 이어하기, 시작 버튼 설정
PAD_MENU_KEYS = {"a": pygame.K_RETURN, "b": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
                 "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "x": pygame.K_z, "y": pygame.K_c,
                 "start": pygame.K_s, "back": pygame.K_k, "lb": pygame.K_o, "rb": pygame.K_r}
PAD_LOOK_YAW = 3.2                # 오른쪽 스틱 끝까지 밀었을 때 1초에 도는 각도(라디안)
PAD_LOOK_PITCH = 520              # 1초에 위아래로 움직이는 px (화면 크기 비율을 곱해요)


class Gamepad:
    """연결된 게임패드를 읽어요. 없으면 아무것도 안 해요."""
    DEAD = 0.2                    # 스틱을 조금 건드린 건 무시

    def __init__(self):
        self.pad, self.kind = None, None
        self.down = set()         # 지금 눌린 버튼들
        self.sprint = False       # 왼쪽 스틱 누르기(L3)로 켜는 달리기
        self.connect()

    def connect(self):
        self.pad, self.kind = None, None
        try:
            from pygame._sdl2 import controller   # 버튼 배치가 표준으로 맞춰진 방식
            controller.init()
            for i in range(controller.get_count()):
                if controller.is_controller(i):
                    self.pad, self.kind = controller.Controller(i), "controller"
                    return
        except Exception:
            pass
        try:
            pygame.joystick.init()
            if pygame.joystick.get_count():
                self.pad, self.kind = pygame.joystick.Joystick(0), "joystick"
        except Exception:
            self.pad = None

    def _axis(self, name):
        if self.kind == "controller":
            value = self.pad.get_axis(getattr(pygame, "CONTROLLER_AXIS_" + name.upper())) / 32767
        else:
            index = {"leftx": 0, "lefty": 1, "rightx": 2, "righty": 3, "triggerleft": 4, "triggerright": 5}[name]
            if index >= self.pad.get_numaxes():
                return 0.0
            value = self.pad.get_axis(index)
            if name.startswith("trigger"):
                value = (value + 1) / 2   # 조이스틱은 -1(안 누름) ~ 1(끝까지)
        return max(-1.0, min(1.0, value))

    def _buttons(self):
        names = ["a", "b", "x", "y", "back", "guide", "start", "l3", "r3", "lb", "rb", "up", "down", "left", "right"]
        pressed = set()
        if self.kind == "controller":
            for i, name in enumerate(names):
                try:
                    if self.pad.get_button(i):
                        pressed.add(name)
                except Exception:
                    pass
        else:
            order = ["a", "b", "x", "y", "lb", "rb", "back", "start", "l3", "r3"]
            for i, name in enumerate(order[:self.pad.get_numbuttons()]):
                if self.pad.get_button(i):
                    pressed.add(name)
            if self.pad.get_numhats():
                hx, hy = self.pad.get_hat(0)
                pressed |= {n for n, on in (("left", hx < 0), ("right", hx > 0), ("up", hy > 0), ("down", hy < 0)) if on}
        return pressed

    def poll(self):
        """이번 장면의 패드 상태: (스틱/트리거 값, 새로 눌린 버튼들). 패드가 없으면 None"""
        if self.pad is None:
            return None, set()
        try:
            state = {k: self._axis(k) for k in ("leftx", "lefty", "rightx", "righty", "triggerleft", "triggerright")}
            now = self._buttons()
        except Exception:
            self.pad = None                    # 연결이 끊겼어요
            return None, set()
        pressed = now - self.down
        self.down = now
        if "l3" in pressed:
            self.sprint = not self.sprint
        return state, pressed

    def held_keys(self, state):
        """패드 상태를 '눌린 키'로 바꿔요 (왼쪽 스틱 = WASD, A = 점프, 오른쪽 트리거 = 사격)"""
        keys = set()
        x, y = state["leftx"], state["lefty"]
        if y < -0.35:
            keys.add(pygame.K_w)
        if y > 0.35:
            keys.add(pygame.K_s)
        if x < -0.35:
            keys.add(pygame.K_a)
        if x > 0.35:
            keys.add(pygame.K_d)
        if abs(x) < self.DEAD and abs(y) < self.DEAD:
            self.sprint = False                # 멈추면 달리기 꺼짐
        elif self.sprint:
            keys.add(pygame.K_LSHIFT)
        if "a" in self.down:
            keys.add(pygame.K_SPACE)
        if state["triggerright"] > 0.4:
            keys.add(pygame.K_f)
        return keys

    def look(self, state):
        """오른쪽 스틱 -> (좌우 라디안/초, 위아래 px/초). 살짝 밀면 아주 천천히 (정밀 조준)"""
        def curve(v):
            return 0.0 if abs(v) < self.DEAD else math.copysign(((abs(v) - self.DEAD) / (1 - self.DEAD)) ** 2, v)
        return (curve(state["rightx"]) * PAD_LOOK_YAW * SETTINGS["look"],
                -curve(state["righty"]) * PAD_LOOK_PITCH * UI * SETTINGS["look"])


class KeyState:
    """키보드 상태 + 게임패드로 '눌린' 키를 합쳐요"""

    def __init__(self, real, extra):
        self.real, self.extra = real, extra

    def __getitem__(self, key):
        return key in self.extra or bool(self.real[key])


_gamepad = None


def get_gamepad():
    global _gamepad
    if _gamepad is None:
        _gamepad = Gamepad()
    return _gamepad


def pad_menu_events():
    """메뉴 화면에서 패드 버튼을 키보드 누름으로 바꿔 줘요"""
    _, pressed = get_gamepad().poll()
    return [pygame.event.Event(pygame.KEYDOWN, key=PAD_MENU_KEYS[b], mod=0, unicode="")
            for b in pressed if b in PAD_MENU_KEYS]


def menu_events():
    events = pygame.event.get()
    for event in events:
        if event.type in (getattr(pygame, "CONTROLLERDEVICEADDED", -1), pygame.JOYDEVICEADDED):
            get_gamepad().connect()
    return events + pad_menu_events()


# ---------------------------------------------------------------
# 창 / 시작 화면 / 실행
# ---------------------------------------------------------------
def available_resolutions():
    """고를 수 있는 해상도 목록 (브라우저에서는 기본 해상도만)"""
    return RESOLUTIONS if not IN_BROWSER else RESOLUTIONS[:1]


def fits_desktop(width, height):
    """이 해상도 창이 모니터 안에 들어가는지 (안 들어가면 전체 화면으로 열어요)"""
    try:
        desk_w, desk_h = pygame.display.get_desktop_sizes()[0]
    except (pygame.error, IndexError, AttributeError):
        return True
    return width <= desk_w and height <= desk_h - 60      # 메뉴 막대 자리를 조금 남겨요


def open_window():
    """현재 해상도로 게임 창을 열어요."""
    flags = 0
    if not IN_BROWSER:
        # SCALED: 전체 화면에서 화면 크기에 맞춰 늘리거나 줄여줘요
        flags = pygame.SCALED | (0 if fits_desktop(WIDTH, HEIGHT) else pygame.FULLSCREEN)
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
    except pygame.error:
        set_resolution(*RESOLUTIONS[0])            # 안 되면 기본 해상도의 보통 창으로
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
    if screen.get_size() != (WIDTH, HEIGHT):
        set_resolution(*screen.get_size())         # 창이 다른 크기로 열렸으면 그 크기에 맞춰 그려요
    pygame.display.set_caption("Strike Zone")
    prepare_window()
    return screen


SETTING_ROWS = [
    ("look", "LOOK SPEED", "화살표/스틱 시점 속도", "Arrow / stick look speed"),
    ("mouse", "MOUSE SPEED", "마우스 감도", "Mouse sensitivity"),
    ("assist", "AIM ASSIST", "조준 보정 세기", "Aim assist strength"),
    ("fov", "FIELD OF VIEW", "시야각 (넓을수록 많이 보여요)", "Field of view"),
    ("volume", "VOLUME", "소리 크기", "Sound volume"),
    ("music", "MUSIC", "배경 음악 크기 (컴퓨터에서만, 웹은 없음)", "Background music (desktop only)"),
    ("difficulty", "DIFFICULTY", "난이도: 적 실력과 내가 받는 피해", "Enemy skill and damage taken"),
    ("hud", "UI SIZE", "글자와 화면 표시 크기 (다음 판부터)", "Text and HUD size (next game)"),
    ("shake", "SCREEN SHAKE", "쏘거나 맞을 때 화면 흔들림", "Camera shake when shooting or hit"),
    ("soundviz", "SOUND MARKS", "발소리·총소리 방향을 조준점 둘레에 표시", "Show footstep/gunshot directions"),
    ("colorblind", "COLORBLIND", "빨강/초록 대신 주황/파랑", "Orange/blue instead of red/green"),
    ("controls", "CONTROLS", "키 바꾸기 (Enter 로 열기)", "Rebind keys (press Enter)"),
]


def change_setting(key, step):
    """설정 한 칸 바꾸기 (←: -1, →: +1)"""
    if key in ("look", "mouse"):
        SETTINGS[key] = round(max(0.4, min(2.5, SETTINGS[key] + step * 0.1)), 1)
    elif key == "assist":
        SETTINGS[key] = (SETTINGS[key] + step) % len(ASSIST_LEVELS)
    elif key == "fov":
        SETTINGS[key] = max(56, min(90, SETTINGS[key] + step * 2))
    elif key in ("volume", "music"):
        SETTINGS[key] = max(0, min(100, SETTINGS[key] + step * 10))
    elif key == "hud":
        SETTINGS[key] = max(80, min(130, SETTINGS[key] + step * 10))
    elif key in ("shake", "soundviz", "colorblind"):
        SETTINGS[key] = 1 - SETTINGS[key]
    elif key == "difficulty":
        SETTINGS[key] = (SETTINGS[key] + step) % len(DIFFICULTIES)
    apply_settings({})


def setting_text(key):
    if key == "controls":
        return "ENTER"
    value = SETTINGS[key]
    if key == "assist":
        return ASSIST_LEVELS[value]
    if key == "difficulty":
        return DIFFICULTIES[value][0]
    if key in ("look", "mouse"):
        return f"x{value:.1f}"
    if key == "fov":
        return f"{value}"
    if key in ("shake", "soundviz", "colorblind"):
        return "ON" if value else "OFF"
    return f"{value}%"


async def settings_screen(save):
    """설정: ↑↓ 고르기, ←→ 바꾸기, Enter/ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    row = 0
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if SETTING_ROWS[row][0] == "controls" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER,
                                                                     pygame.K_RIGHT, pygame.K_d):
                if await controls_screen(save) == "closed":
                    return "closed"
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_s):
                save["settings"] = dict(SETTINGS)
                write_save(save)
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(SETTING_ROWS)
            elif event.key in (pygame.K_DOWN,):
                row = (row + 1) % len(SETTING_ROWS)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                change_setting(SETTING_ROWS[row][0], -1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                change_setting(SETTING_ROWS[row][0], 1)
        screen.fill((14, 10, 30))
        title = fonts["big"].render("SETTINGS", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.08)))
        for i, (key, name, desc_ko, desc_en) in enumerate(SETTING_ROWS):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.15 + i * 0.066), WIDTH * 0.88, HEIGHT * 0.06)
            selected = i == row
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 255, 255, 38) if selected else (0, 0, 0, 110))
            screen.blit(panel, rect)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 3 if selected else 1)
            label = fonts["normal"].render(name, True, WHITE)
            screen.blit(label, label.get_rect(midleft=(rect.x + 14, rect.centery)))
            desc = fonts["help"].render(desc_ko if ko else desc_en, True, (200, 230, 255))
            screen.blit(desc, desc.get_rect(midleft=(rect.x + rect.w * 0.24, rect.centery)))
            value = setting_text(key)
            image = fonts["normal"].render(f"<  {value}  >" if selected else value, True, YELLOW if selected else WHITE)
            screen.blit(image, image.get_rect(midright=(rect.right - 16, rect.centery)))
        hint = ("↑↓ 고르기     ←→ 바꾸기     Enter / ESC 저장하고 돌아가기" if ko
                else "UP/DOWN choose     LEFT/RIGHT change     ENTER / ESC save and back")
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def controls_screen(save):
    """키 바꾸기: ↑↓←→ 고르기, Enter 누른 뒤 새 키 누르기, Backspace 모두 처음대로, ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    row, waiting, note = 0, False, ""
    half = (len(KEY_ACTIONS) + 1) // 2
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if waiting:                                  # 새 키를 기다리는 중
                waiting = False
                if event.key == pygame.K_ESCAPE:
                    note = ""
                elif event.key in KEY_FIXED:
                    note = "그 키는 쓸 수 없어요 (ESC, Enter, 화살표)" if ko else "That key is reserved"
                else:
                    rebind(KEY_ACTIONS[row][1], event.key)
                    note = f"{KEY_ACTIONS[row][0]} = {key_label(event.key)}"
                continue
            if event.key == pygame.K_ESCAPE:
                save["keys"] = saved_keys()
                write_save(save)
                return None
            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                waiting, note = True, ""
            elif event.key == pygame.K_BACKSPACE:
                apply_keys({})
                note = "모든 키를 처음대로 돌렸어요" if ko else "All keys reset to default"
            elif event.key == pygame.K_UP:
                row = (row - 1) % len(KEY_ACTIONS)
            elif event.key == pygame.K_DOWN:
                row = (row + 1) % len(KEY_ACTIONS)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                row = (row + half) % (half * 2)
                row = min(row, len(KEY_ACTIONS) - 1)
        screen.fill((14, 10, 30))
        title = fonts["big"].render("CONTROLS", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.08)))
        for i, (name, default, desc) in enumerate(KEY_ACTIONS):
            col, line = divmod(i, half)
            rect = pygame.Rect(WIDTH * (0.05 + col * 0.46), HEIGHT * (0.16 + line * 0.072), WIDTH * 0.44, HEIGHT * 0.064)
            selected = i == row
            pygame.draw.rect(screen, (60, 40, 90) if selected else (24, 18, 44), rect, border_radius=6)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 2 if selected else 1,
                             border_radius=6)
            label = fonts["help"].render(desc if ko else name, True, WHITE)
            screen.blit(label, label.get_rect(midleft=(rect.x + 12, rect.centery)))
            key = "..." if selected and waiting else key_label(bound_key(default))
            changed = bound_key(default) != default
            image = fonts["normal"].render(key, True, YELLOW if selected else ((80, 240, 255) if changed else WHITE))
            screen.blit(image, image.get_rect(midright=(rect.right - 12, rect.centery)))
        if waiting:
            note = "바꿀 키를 누르세요 (ESC 취소)" if ko else "Press the new key (ESC cancel)"
        if note:
            image = fonts["help"].render(note, True, (80, 255, 120))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.9)))
        hint = ("↑↓←→ 고르기   Enter 바꾸기   Backspace 모두 처음대로   ESC 저장하고 돌아가기   (화살표 시점, ESC, Enter는 고정)"
                if ko else "ARROWS choose   ENTER change   BACKSPACE reset all   ESC save and back")
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.96)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def challenge_screen(save):
    """도전 모드 고르기: ↑↓ 고르기, Enter 시작, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    row = 0
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(CHALLENGES)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % len(CHALLENGES)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                return dict(mode="campaign", round=1, challenge=CHALLENGES[row][0])
        screen.fill((14, 10, 30))
        title = fonts["big"].render("CHALLENGES", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.09)))
        records = save.get("challenges", {})
        today = str(datetime.date.today())
        for i, (name, round_no, desc_ko, desc_en) in enumerate(CHALLENGES):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.2 + i * 0.13), WIDTH * 0.88, HEIGHT * 0.11)
            selected = i == row
            pygame.draw.rect(screen, (60, 40, 90) if selected else (24, 18, 44), rect, border_radius=8)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 3 if selected else 1,
                             border_radius=8)
            label = fonts["normal"].render(name + (f"  ({today})" if name == "DAILY" else ""), True, WHITE)
            screen.blit(label, (rect.x + 16, rect.y + rect.h * 0.12))
            desc = fonts["help"].render(desc_ko if ko else desc_en, True, (200, 230, 255))
            screen.blit(desc, (rect.x + 16, rect.y + rect.h * 0.58))
            if name == "DAILY":
                daily = save.get("daily", {})
                best = daily.get("best") if daily.get("date") == today else None
            else:
                best = records.get(name)
            text = f"BEST {best:.1f}s" if best else "-"
            image = fonts["normal"].render(text, True, YELLOW if best else (140, 140, 160))
            screen.blit(image, image.get_rect(midright=(rect.right - 20, rect.centery)))
        hint = "↑↓ 고르기   Enter 시작   ESC 돌아가기" if ko else "UP/DOWN choose   ENTER start   ESC back"
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def achievements_screen(save):
    """업적과 누적 기록. ←→ 로 위장 무늬 고르기 (업적을 모을수록 늘어나요), ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    previews = {}
    while True:
        clock.tick(30)
        camos = earned_camos(save)
        current = save.get("camo", "NONE")
        if current not in camos:
            current = "NONE"
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_a):
                write_save(save)
                return None
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                step = 1 if event.key == pygame.K_RIGHT else -1
                current = camos[(camos.index(current) + step) % len(camos)]
                save["camo"] = current
        done = save.get("achievements", [])
        life = save.get("lifetime", {})
        screen.fill((14, 10, 30))
        title = fonts["big"].render(f"ACHIEVEMENTS  {len(done)} / {len(ACHIEVEMENTS)}", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.05, HEIGHT * 0.08)))
        half = (len(ACHIEVEMENTS) + 1) // 2
        for i, (name, desc_ko, desc_en, test) in enumerate(ACHIEVEMENTS):
            col, line = divmod(i, half)
            rect = pygame.Rect(WIDTH * (0.04 + col * 0.47), HEIGHT * (0.15 + line * 0.069), WIDTH * 0.45, HEIGHT * 0.062)
            got = name in done
            pygame.draw.rect(screen, (50, 44, 20) if got else (24, 18, 44), rect, border_radius=6)
            pygame.draw.rect(screen, (255, 215, 80) if got else (70, 60, 100), rect, 2 if got else 1, border_radius=6)
            mark = fonts["normal"].render(("* " if got else "- ") + name, True, (255, 215, 80) if got else (140, 140, 160))
            screen.blit(mark, mark.get_rect(midleft=(rect.x + 10, rect.centery)))
            desc = fonts["help"].render(desc_ko if ko else desc_en, True, WHITE if got else (150, 150, 170))
            screen.blit(desc, desc.get_rect(midright=(rect.right - 10, rect.centery)))
        totals = (f"KILLS {life.get('kills', 0)}   HEADSHOTS {life.get('heads', 0)}   KNIFE {life.get('knife', 0)}   "
                  f"EXPLOSIVE {life.get('explosive', 0)}   BEST STREAK {life.get('streak', 0)}   ROUNDS {life.get('rounds', 0)}")
        image = fonts["small"].render(totals, True, (80, 240, 255))
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.73)))
        # 위장 무늬 고르기 + 미리보기
        names = []
        for name, need, body, accent in CAMOS:
            names.append(f"[{name}]" if name == current else (name if name in camos else f"{name}({need})"))
        image = fonts["normal"].render("CAMO:  " + "   ".join(names), True, WHITE)
        screen.blit(image, image.get_rect(midleft=(WIDTH * 0.05, HEIGHT * 0.8)))
        if current not in previews:
            previews[current] = make_viewmodel("RIFLE", False, None if current == "NONE" else current)[0]
        gun = previews[current]
        scale = HEIGHT * 0.16 / gun.get_height()
        gun = pygame.transform.smoothscale(gun, (int(gun.get_width() * scale), int(gun.get_height() * scale)))
        screen.blit(gun, gun.get_rect(midright=(WIDTH * 0.97, HEIGHT * 0.84)))
        hint = ("←→ 위장 무늬 고르기 (업적을 모으면 늘어나요)   ESC 돌아가기" if ko
                else "LEFT/RIGHT choose camo (earn more with achievements)   ESC back")
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def intro_screen(save):
    """시작 화면: 조작법을 보여주고 캠페인 / 좀비 모드 / 이어하기 / 해상도를 골라요.
    고른 것을 dict(mode=..., round=...)로 돌려줘요. ESC면 None, 창 닫기면 "closed"."""
    options = available_resolutions()
    res_index = min(save.get("res", 0), len(options) - 1)
    set_resolution(*options[res_index])
    screen = open_window()
    fonts = make_fonts()
    clock = pygame.time.Clock()
    continue_round = save.get("continue", 1)
    reached = max(save.get("best", 1), continue_round)
    set_starts = [1 + k * SET_SIZE for k in range(len(SETS)) if 1 + k * SET_SIZE <= reached]
    start_pick = 0
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                return dict(mode="campaign", round=set_starts[start_pick])
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT) and len(set_starts) > 1:
                start_pick = (start_pick + (1 if event.key == pygame.K_RIGHT else -1)) % len(set_starts)
            if event.key == pygame.K_d:
                SETTINGS["difficulty"] = (SETTINGS["difficulty"] + 1) % len(DIFFICULTIES)
                save["settings"] = dict(SETTINGS)
                write_save(save)
            if event.key == pygame.K_z:
                return dict(mode="zombies", round=1)
            if event.key == pygame.K_r:
                return dict(mode="training", round=1)
            if event.key == pygame.K_x:
                picked = await challenge_screen(save)
                if picked == "closed" or picked:
                    return picked
                continue
            if event.key == pygame.K_a:
                if await achievements_screen(save) == "closed":
                    return "closed"
                continue
            if event.key == pygame.K_o:
                picked = await mission_screen(save)
                if picked == "closed" or picked:
                    return picked
                continue
            if event.key == pygame.K_c and continue_round > 1:
                return dict(mode="campaign", round=continue_round)
            if event.key == pygame.K_s:
                if await settings_screen(save) == "closed":
                    return "closed"
                fonts = make_fonts()
                continue
            if event.key == pygame.K_k:
                if await skills_screen(save) == "closed":
                    return "closed"
                continue
            if event.key == pygame.K_t and len(options) > 1:
                res_index = (res_index + 1) % len(options)
                save["res"] = res_index
                write_save(save)
                set_resolution(*options[res_index])
                screen = open_window()
                fonts = make_fonts()

        ko = fonts["lang"] == "ko"
        first = set_starts[start_pick]
        if ko:
            parts = [f"Enter 캠페인 (라운드 {first})", "Z 좀비 모드"]
        else:
            parts = [f"ENTER campaign (round {first})", "Z zombies"]
        if len(set_starts) > 1:
            parts.append("←→ 시작 세트" if ko else "LEFT/RIGHT start set")
        diff = DIFFICULTIES[SETTINGS["difficulty"]][0]
        parts.append(f"D 난이도 {diff}" if ko else f"D difficulty {diff}")
        if continue_round > 1:
            parts.append(f"C 이어하기 (라운드 {continue_round})" if ko else f"C continue (round {continue_round})")
        if len(options) > 1:
            w, h = options[res_index]
            note = "" if fits_desktop(w, h) else (" 전체 화면" if ko else " fullscreen")
            parts.append(f"T 해상도 {w}x{h}{note}" if ko else f"T resolution {w}x{h}{note}")
        parts.append("O 미션" if ko else "O missions")
        parts.append("R 사격장" if ko else "R training range")
        parts.append("X 도전" if ko else "X challenges")
        parts.append("A 업적" if ko else "A achievements")
        parts.append("K 스킬" if ko else "K skills")
        parts.append("S 설정" if ko else "S settings")
        parts.append("ESC 메뉴" if ko else "ESC menu")
        screen.fill((15, 10, 35))
        draw_help(screen, fonts, "     ".join(parts))
        # 조작법 판 위에 제목과 네온 줄무늬
        for i in range(6):
            y = HEIGHT * (0.15 + i * 0.012)
            pygame.draw.line(screen, (255, 80, 200) if i % 2 else (80, 240, 255), (0, y), (WIDTH, y), 2)
        title = fonts["title"].render("STRIKE ZONE", True, (255, 80, 200))
        screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.09)))
        best, zbest = save.get("best", 0), save.get("zbest", 0)
        records = []
        if best:
            records.append(f"캠페인 최고 라운드 {best}" if ko else f"Campaign best: round {best}")
        if zbest:
            records.append(f"좀비 최고 웨이브 {zbest}" if ko else f"Zombies best: wave {zbest}")
        if records:
            label = fonts["help"].render("     ".join(records), True, WHITE)
            screen.blit(label, label.get_rect(center=(WIDTH / 2, HEIGHT * 0.88)))
        pygame.display.flip()
        await asyncio.sleep(0)


def weapon_stats(spec):
    """로드아웃 화면의 성능 막대 (0~1): 피해, 연사, 탄창, 정확도, 기동성"""
    if spec["projectile"]:
        damage = 1.0
    else:
        damage = min(1.0, spec["body"] * spec["pellets"] / 160)
    return [("DAMAGE", damage), ("FIRE RATE", min(1.0, 0.065 / spec["delay"])),
            ("MAGAZINE", min(1.0, spec["mag"] / 100)), ("ACCURACY", max(0.05, 1 - spec["spread"] / 50)),
            ("MOBILITY", spec.get("move", 1.0) * (0.85 if spec["scope"] else 1.0))]


async def mission_screen(save):
    """미션 고르기: ↑↓ 고르기, Enter 시작, C 저장된 단계부터 이어하기, ESC 뒤로"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    saved = save.get("mission")
    row = saved["id"] if saved else 0
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(MISSIONS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % len(MISSIONS)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                return dict(mode="mission", mission=row, stage=0, round=1)
            elif event.key == pygame.K_c and saved and saved["id"] == row:
                return dict(mode="mission", mission=row, stage=saved["stage"], round=1)
        screen.fill((14, 10, 30))
        title = fonts["big"].render("MISSIONS", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.09)))
        sub = "큰 맵에서 다섯 단계로 이어지는 긴 작전. 단계마다 체크포인트에 저장돼요." if ko else \
            "Long operations on huge maps: five stages, checkpoint saved after each one."
        screen.blit(fonts["help"].render(sub, True, (80, 240, 255)), (WIDTH * 0.06, HEIGHT * 0.15))
        done = save.get("missions_done", [])
        for i, m in enumerate(MISSIONS):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.22 + i * 0.17), WIDTH * 0.88, HEIGHT * 0.15)
            selected = i == row
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 255, 255, 38) if selected else (0, 0, 0, 110))
            screen.blit(panel, rect)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 3 if selected else 1)
            name = m["name"] + ("   [COMPLETE]" if m["name"] in done else "")
            screen.blit(fonts["big"].render(name, True, YELLOW if selected else WHITE), (rect.x + 16, rect.y + 8))
            screen.blit(fonts["help"].render(m["desc"][0 if ko else 1], True, (200, 230, 255)),
                        (rect.x + 16, rect.y + rect.h * 0.62))
            if saved and saved["id"] == i:
                text = f"C 이어하기: {saved['stage'] + 1}단계부터" if ko else f"C continue from stage {saved['stage'] + 1}"
                image = fonts["small"].render(text, True, (255, 200, 60))
                screen.blit(image, image.get_rect(topright=(rect.right - 16, rect.y + 12)))
        stages = "   >   ".join(title for _, title in MISSION_STAGES)
        screen.blit(fonts["tiny"].render(stages, True, (180, 180, 200)), (WIDTH * 0.06, HEIGHT * 0.75))
        hint = "↑↓ 고르기     Enter 처음부터     C 이어하기     ESC 뒤로" if ko else \
            "UP/DOWN choose     ENTER start     C continue     ESC back"
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def skills_screen(save):
    """스킬 트리: 계급이 오를 때마다 받는 포인트로 스킬을 배워요. ↑↓ 고르기, → 배우기, ← 되돌리기, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    row = 0
    ranks = save.setdefault("skills", {})
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            name, top = SKILLS[row][0], SKILLS[row][1]
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_k):
                write_save(save)
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(SKILLS)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % len(SKILLS)
            elif event.key in (pygame.K_RIGHT, pygame.K_d) and skill_points(save) > 0 and ranks.get(name, 0) < top:
                ranks[name] = ranks.get(name, 0) + 1
            elif event.key in (pygame.K_LEFT, pygame.K_a) and ranks.get(name, 0) > 0:
                ranks[name] -= 1                           # 언제든 되돌려서 다시 고를 수 있어요
        screen.fill((14, 10, 30))
        title = fonts["big"].render("SKILLS", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.08)))
        level = player_level(save)
        into = save.get("xp", 0) % XP_PER_RANK
        info = f"RANK {level}   XP {into} / {XP_PER_RANK}   SKILL POINTS {skill_points(save)}"
        screen.blit(fonts["normal"].render(info, True, (80, 240, 255)), (WIDTH * 0.06, HEIGHT * 0.14))
        for i, (name, top, desc_ko, desc_en, key) in enumerate(SKILLS):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.2 + i * 0.071), WIDTH * 0.88, HEIGHT * 0.062)
            selected = i == row
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 255, 255, 38) if selected else (0, 0, 0, 110))
            screen.blit(panel, rect)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 2 if selected else 1)
            kind = "ACTIVE" if key else "PASSIVE"
            screen.blit(fonts["small"].render(f"{name}  ({kind})", True, YELLOW if key else WHITE),
                        (rect.x + 12, rect.y + rect.h * 0.12))
            screen.blit(fonts["help"].render(desc_ko if ko else desc_en, True, (200, 230, 255)),
                        (rect.x + rect.w * 0.33, rect.y + rect.h * 0.18))
            have = ranks.get(name, 0)
            for k in range(top):                           # 배운 단계는 채운 칸
                box = pygame.Rect(rect.right - (top - k) * 26 * UI - 10, rect.centery - 8 * UI, 20 * UI, 16 * UI)
                pygame.draw.rect(screen, (255, 200, 60) if k < have else (60, 55, 80), box)
        hint = ("↑↓ 고르기     → 배우기     ← 되돌리기     ESC 돌아가기   (계급이 오를 때마다 포인트 1)" if ko
                else "UP/DOWN choose     RIGHT learn     LEFT undo     ESC back   (1 point per rank)")
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def loadout_screen(save, choice):
    """로드아웃: 주무기 / 보조무기 / 퍼크를 골라요. ↑↓ 줄 고르기, ←→ 바꾸기, Enter 시작, ESC 뒤로.
    고른 로드아웃(dict)을 돌려줘요. ESC면 None, 창 닫기면 "closed"."""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    perk_names = [name for name, _, _ in PERKS]
    owned = unlocked_weapons(save)
    options = [owned, owned, perk_names]
    labels = ["START WEAPON", "SECOND WEAPON (Q)", "PERK"]
    saved = dict(DEFAULT_LOADOUT, **save.get("loadout", {}))
    picks = [options[0].index(saved["primary"]) if saved["primary"] in options[0] else 0,
             options[1].index(saved["secondary"]) if saved["secondary"] in options[1] else 0,
             options[2].index(saved["perk"]) if saved["perk"] in options[2] else 0]
    row = 0
    previews = {}
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % 3
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % 3
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                picks[row] = (picks[row] - 1) % len(options[row])
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                picks[row] = (picks[row] + 1) % len(options[row])
            elif event.key == pygame.K_k:
                if await skills_screen(save) == "closed":
                    return "closed"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                loadout = dict(primary=options[0][picks[0]], secondary=options[1][picks[1]],
                               perk=options[2][picks[2]])
                save["loadout"] = loadout
                write_save(save)
                return loadout

        # 배경과 제목
        screen.fill((14, 10, 30))
        for i in range(0, HEIGHT, max(2, int(4 * UI))):
            shade_v = int(10 + 20 * i / HEIGHT)
            pygame.draw.line(screen, (shade_v, 8, shade_v + 18), (0, i), (WIDTH, i))
        title = fonts["big"].render("LOADOUT", True, (255, 80, 200))
        screen.blit(title, title.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.09)))
        if choice["mode"] == "zombies":
            mode_text = "ZOMBIES  -  BLOOD MOON"
        elif choice["mode"] == "mission":
            mode_text = f"MISSION  -  {MISSIONS[choice['mission']]['name']}"
        else:
            mode_text = f"CAMPAIGN  -  ROUND {choice['round']}"
        mode_text += f"     RANK {player_level(save)}   SKILL POINTS {skill_points(save)}"
        label = fonts["normal"].render(mode_text, True, (80, 240, 255))
        screen.blit(label, label.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.16)))

        # 왼쪽: 세 줄 (시작 무기 / 두 번째 무기 / 퍼크)
        card_w, card_h = WIDTH * 0.44, HEIGHT * 0.14
        for i in range(3):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.21 + i * 0.155), card_w, card_h)
            selected = i == row
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 255, 255, 38) if selected else (0, 0, 0, 110))
            screen.blit(panel, rect)
            pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 3 if selected else 1)
            screen.blit(fonts["small"].render(labels[i], True, (200, 200, 220)), (rect.x + 14, rect.y + 10))
            name = options[i][picks[i]]
            arrows = f"<  {name}  >" if selected else name
            image = fonts["big"].render(arrows, True, YELLOW if selected else WHITE)
            screen.blit(image, (rect.x + 14, rect.y + rect.h * 0.28))
            if i < 2:
                desc = WEAPON_INFO[name][0 if ko else 1]
            else:
                desc = PERKS[picks[2]][1 if ko else 2]
            image = fonts["help"].render(desc, True, (200, 230, 255))
            screen.blit(image, (rect.x + 14, rect.y + rect.h * 0.7))
        # 왼쪽 아래: 무기 인벤토리 (가진 무기는 레벨, 없는 무기는 얻는 조건)
        title = fonts["small"].render(f"INVENTORY  {len(owned)} / {len(WEAPONS)}   (in game: 1-9, 0, TAB)", True, WHITE)
        screen.blit(title, (WIDTH * 0.06, HEIGHT * 0.685))
        kills_all = save.get("wkills", {})
        for k, spec in enumerate(WEAPONS):
            name = spec["name"]
            x = WIDTH * (0.06 + (k % 2) * 0.235)
            y = HEIGHT * (0.72 + (k // 2) * 0.031)
            if name in owned:
                text = f"{name}  LV {weapon_level(kills_all.get(name, 0))}"
                color = (255, 200, 60) if name in (options[0][picks[0]], options[1][picks[1]]) else WHITE
            else:
                text = f"[LOCKED] {name}: {unlock_text(name, ko)}"
                color = (120, 120, 135)
            font = fonts["help"] if ko else fonts["tiny"]
            screen.blit(font.render(text, True, color), (x, y))

        # 오른쪽: 고른 무기 모습과 성능 막대
        weapon = options[1][picks[1]] if row == 1 else options[0][picks[0]]
        if weapon not in previews:
            image = make_viewmodel(weapon, False)[0]
            scale = min(WIDTH * 0.4 / image.get_width(), HEIGHT * 0.4 / image.get_height())
            previews[weapon] = pygame.transform.smoothscale(
                image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        box = pygame.Rect(WIDTH * 0.54, HEIGHT * 0.21, WIDTH * 0.40, HEIGHT * 0.41)
        pygame.draw.rect(screen, (0, 0, 0), box)
        pygame.draw.rect(screen, (70, 60, 100), box, 1)
        preview = previews[weapon]
        screen.blit(preview, preview.get_rect(bottomright=box.bottomright))
        screen.blit(fonts["normal"].render(weapon, True, WHITE), (box.x + 12, box.y + 10))
        kills = save.get("wkills", {}).get(weapon, 0)
        mods = weapon_mods(kills)
        upcoming = [(need, mod) for need, mod in WEAPON_LEVELS if kills < need]
        level = f"LV {weapon_level(kills)} / {WEAPON_MAX_LEVEL}  (DMG +{5 * (weapon_level(kills) - 1)}%)   {kills} kills"
        if upcoming:
            level += f"   next: {upcoming[0][1]} at {upcoming[0][0]}"
        screen.blit(fonts["tiny"].render(level, True, (255, 200, 60)), (box.x + 12, box.y + 10 + 30 * UI))
        if mods:
            screen.blit(fonts["tiny"].render(" + ".join(mods), True, (80, 240, 255)),
                        (box.x + 12, box.y + 10 + 50 * UI))
        kills = save.get("wkills", {}).get(weapon, 0)
        leveled = apply_mods(WEAPON_BY_NAME[weapon], weapon_mods(kills), weapon_level(kills))
        for k, (stat, value) in enumerate(weapon_stats(leveled)):
            y = HEIGHT * (0.69 + k * 0.045)
            screen.blit(fonts["small"].render(stat, True, (200, 200, 220)), (box.x, y))
            bar = pygame.Rect(box.x + WIDTH * 0.12, y + 4 * UI, WIDTH * 0.28, 10 * UI)
            pygame.draw.rect(screen, (45, 40, 70), bar)
            bar.width = int(bar.width * value)
            pygame.draw.rect(screen, (80, 240, 255), bar)

        hint = ("↑↓ 고르기     ←→ 바꾸기     Enter 시작     K 스킬     ESC 뒤로" if ko
                else "UP/DOWN choose     LEFT/RIGHT change     ENTER start     K skills     ESC back")
        image = fonts["help"].render(hint, True, YELLOW)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.95)))
        pygame.display.flip()
        await asyncio.sleep(0)


PAUSE_ITEMS = ["RESUME", "HELP", "SETTINGS", "QUIT TO MENU"]


def draw_pause(screen, fonts, row):
    """일시정지 메뉴: 게임 화면 위에 반투명 판"""
    shade_panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade_panel.fill((5, 5, 15, 215))
    screen.blit(shade_panel, (0, 0))
    title = fonts["big"].render("PAUSED", True, (255, 80, 200))
    screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.25)))
    for i, item in enumerate(PAUSE_ITEMS):
        selected = i == row
        rect = pygame.Rect(0, 0, WIDTH * 0.32, HEIGHT * 0.08)
        rect.center = (WIDTH / 2, HEIGHT * (0.38 + i * 0.1))
        panel = pygame.Surface(rect.size, pygame.SRCALPHA)
        panel.fill((255, 255, 255, 45) if selected else (0, 0, 0, 120))
        screen.blit(panel, rect)
        pygame.draw.rect(screen, (255, 80, 200) if selected else (70, 60, 100), rect, 3 if selected else 1)
        label = fonts["normal"].render(item, True, YELLOW if selected else WHITE)
        screen.blit(label, label.get_rect(center=rect.center))
    ko = fonts["lang"] == "ko"
    hint = "↑↓ 고르기   Enter 확인   ESC 계속하기" if ko else "UP/DOWN choose   ENTER select   ESC resume"
    image = fonts["help"].render(hint, True, YELLOW)
    screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.85)))


def grab_mouse(on):
    pygame.event.set_grab(on)
    pygame.mouse.set_visible(not on)
    pygame.mouse.get_rel()


async def run():
    """게임 한 판 실행. ESC를 누르면 끝나요.

    창을 닫으면 False, ESC로 끝내면 True를 돌려줘요 (메뉴로 돌아갈지 판단용).
    """
    save = load_save()
    settings = save.get("settings", {})
    if "difficulty" in settings and not settings.get("v2"):     # 예전 3단계 난이도 -> 새 5단계
        settings = dict(settings, difficulty=[1, 2, 3][min(2, settings["difficulty"])], v2=True)
    apply_settings(settings)
    apply_keys(save.get("keys", {}))
    while True:
        choice = await intro_screen(save)            # 모드 고르기
        if choice is None or choice == "closed":
            return choice is None
        loadout = await loadout_screen(save, choice)  # 무기와 퍼크 고르기 (ESC면 시작 화면으로)
        if loadout == "closed":
            return False
        if loadout:
            break
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # 마우스를 창 안에 가두고 커서 숨기기 (FPS 게임처럼)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()

    training = choice["mode"] == "training"
    # 사격장은 저장 정보의 복사본으로 (무엇을 해도 진짜 저장에는 남지 않아요)
    game = Game(copy.deepcopy(save) if training else save, choice["round"], mode=choice["mode"], loadout=loadout,
                mission=choice.get("mission", 0), stage=choice.get("stage", 0), challenge=choice.get("challenge"))
    running = True
    closed = False             # 창을 닫았는지 여부
    work_time, frames, check_timer = 0.0, 0, 0.0   # 자동 해상도 조절용 기록
    gamepad = get_gamepad()
    paused, pause_row = False, 0       # ESC: 일시정지 메뉴 (실수로 눌러도 진행이 날아가지 않아요)
    while running:
        dt = min(0.05, clock.tick(FPS) / 1000)
        events = [remap_event(event) for event in pygame.event.get()]   # 바꾼 키를 기본 키로
        pad, pad_pressed = gamepad.poll()
        if pad is not None:
            # 패드 버튼을 키 누름으로 바꿔서 같은 방식으로 처리해요
            if paused:
                mapping = PAD_MENU_KEYS
            else:
                mapping = dict(PAD_GAME_KEYS, a=pygame.K_r) if game.game_over else PAD_GAME_KEYS
            events += [pygame.event.Event(pygame.KEYDOWN, key=mapping[b], mod=0, unicode="")
                       for b in pad_pressed if b in mapping]
        if paused:
            choice = None
            for event in events:
                if event.type == pygame.QUIT:
                    running, closed = False, True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        choice = "RESUME"
                    elif event.key in (pygame.K_UP, pygame.K_w):
                        pause_row = (pause_row - 1) % len(PAUSE_ITEMS)
                    elif event.key in (pygame.K_DOWN, pygame.K_s):
                        pause_row = (pause_row + 1) % len(PAUSE_ITEMS)
                    elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                        choice = PAUSE_ITEMS[pause_row]
            if choice == "RESUME":
                paused = False
                grab_mouse(True)
            elif choice == "HELP":
                paused = False
                game.show_help = True                  # 도움말 (H로 닫으면 계속)
                grab_mouse(True)
            elif choice == "SETTINGS":
                if await settings_screen(save) == "closed":
                    running, closed = False, True
                game.sounds.refresh_background()
            elif choice == "QUIT TO MENU":
                running = False
            if not running:
                break
            game.draw(screen)
            draw_pause(screen, game.fonts, pause_row)
            pygame.display.flip()
            await asyncio.sleep(0)
            continue
        for event in events:
            if event.type in (getattr(pygame, "CONTROLLERDEVICEADDED", -1), pygame.JOYDEVICEADDED):
                gamepad.connect()
            if event.type == pygame.QUIT:
                running, closed = False, True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused, pause_row = True, 0
                grab_mouse(False)
            elif event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_r:
                game.retry_round()
            elif event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_n:
                game.reset(1)
            elif (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_F11)
                  and not IN_BROWSER):
                try:
                    pygame.display.toggle_fullscreen()
                except pygame.error:
                    pass                       # 전체 화면을 지원하지 않는 환경
            else:
                game.handle_event(event)
        if not running:
            break

        started = time.perf_counter()
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        game.fps = clock.get_fps()
        keys = RemappedKeys(pygame.key.get_pressed()) if KEY_MAP else pygame.key.get_pressed()
        if pad is not None:
            keys = KeyState(keys, gamepad.held_keys(pad))
            game.pad_aim = pad["triggerleft"] > 0.4
            game.player.stick = gamepad.look(pad)
        game.update(dt, keys, mouse_dx, mouse_dy, pygame.mouse.get_pressed())
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

    if not training:
        write_save(game.save)      # 경험치(계급) 저장
    game.sounds.stop_background()
    # 마우스 원래대로
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    return not closed


if __name__ == "__main__":
    pygame.init()
    asyncio.run(run())
    pygame.quit()
