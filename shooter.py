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
import base64
import json
import zlib
import copy
import asyncio
import math
import random
import re
import sys
import time
from collections import deque
import datetime

import pygame

# 데이터 표는 strike/ 폴더에 나눠 두었어요 (맵, 무기·적, 소리, 이야기)
from strike.maps import MAPS, WALLS, FLOORS, OFFICE_BLOCK
from strike.units import (HORIZONTAL_KICK, START_WEAPONS, UNLOCKS, PERKS, WEAPON_INFO, WEAPONS, ENEMY_TYPES, ARMORED, ENEMY_MAGS, COVER_USERS, GUN_LOOKS,
                          ATTACHMENTS, ATTACHMENT_INFO, TACTICALS)
from strike.sounds import SOUND_RECIPES, SOUND_MARK_KINDS, MUFFLED_SOUNDS, STEP_SOUNDS, ENEMY_STEPS, GUN_SOUNDS
from strike.story import CHALLENGES, STORY, RADIO, HELP_TEXT

from browser import load_save, prepare_window, write_save, copy_text, paste_text, save_picture

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
SHELL_RELOAD = {"SHOTGUN": 0.42}
# 무기 종류마다 다른 재장전 동작: (내리는 정도, 옆으로, 기울기(도))
RELOAD_STYLES = {"RIFLES": (110, 50, 14), "SMGS": (90, 40, 20), "MARKSMAN": (115, 55, 10), "LMGS": (150, 30, 6),
                 "PISTOLS": (70, 25, 30), "LAUNCHERS": (130, 80, 4), "SHOTGUNS": (100, 45, 12)}    # 한 발씩 넣는 총: 한 발 넣는 시간(초). 쏘면 바로 멈추고 쏴요
BOLT_ACTION = ("SNIPER",)            # 쏠 때마다 노리쇠를 당기는 총
MAX_DECALS = 240                     # 벽에 남는 총알 자국/그을음 최대 개수
# 실내: 이 바닥 위에는 천장이 있어요. 천장 높이는 실내 벽 높이와 같아요
INDOOR_FLOORS = ("w",)
CEILING = 1.4
CEILING_COLOR = (200, 196, 188)
DOORS = ("d",)                       # 문: 사람이 가까이 오면 열리고, 아무도 없으면 4초 뒤 닫혀요
DOOR_OPEN_RANGE = 1.15
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
VAULT_WALLS = "KQFVZc"            # 뛰어넘을 수 있는 낮은 것 (상자, 울타리, 낮은 담, 자동차)
VAULT_TIME = 0.42                 # 뛰어넘는 데 걸리는 시간(초)
LEAN_DIST = 0.32                  # 몸을 기울이면 눈이 옆으로 이만큼 (칸)
GRAVITY = 13                      # 중력 (클수록 빨리 떨어져요)

# 설정 (시작 화면에서 S): 저장돼서 다음에도 그대로예요
SETTINGS = dict(look=1.0, mouse=1.0, assist=2, fov=66, volume=80, difficulty=2, v2=True, music=40,
                hud=100, shake=1, soundviz=0, colorblind=0, squad=2, fullscreen=0, lang=0, gfx=1)
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
    ("INSPECT", pygame.K_i, "무기 살펴보기"), ("SQUAD ORDER", pygame.K_k, "동료 명령: 따라와/대기/공격"),
    ("FLASHLIGHT", pygame.K_l, "손전등 켜기/끄기"), ("TACTICAL", pygame.K_n, "전술 장비 던지기"), ("USE / BUY", pygame.K_b, "사용·사기: 고정 기관총, 좀비 상점"), ("SHOP UPGRADE", pygame.K_u, "좀비 상점: 강화"),
    ("LEAN LEFT", pygame.K_COMMA, "몸 기울이기: 왼쪽"), ("LEAN RIGHT", pygame.K_PERIOD, "몸 기울이기: 오른쪽"),
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


SHORT_KEY_NAMES = {"LEFT SHIFT": "SHIFT", "RIGHT SHIFT": "SHIFT", "LEFT CTRL": "CTRL", "RIGHT CTRL": "CTRL",
                   "LEFT ALT": "ALT", "RIGHT ALT": "ALT", "RETURN": "ENTER", "ESCAPE": "ESC", "BACKSPACE": "BKSP"}


def kl(default):
    """화면에 보여줄 키 이름: 키를 바꿨으면 바꾼 키로 (예: kl(pygame.K_g) -> 'G')"""
    name = key_label(bound_key(default))
    return SHORT_KEY_NAMES.get(name, name)


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
    ("CONTRACTOR", "라운드 계약 10개 완료", "Complete 10 round contracts", lambda s, l: l.get("contracts", 0) >= 10),
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


# ----- 저장 코드 (웹 ↔ 맥 진행 옮기기) -----
# 내 컴퓨터 랭킹: 모드마다 점수가 높은 판을 10개까지 save["rankings"] 에 저장해요
# (모드 키, 화면 이름, 어디까지 갔는지 이름)
RANK_MODES = [("zombies", "ZOMBIES", "WAVE"), ("campaign", "CAMPAIGN", "ROUND"), ("mission", "MISSIONS", "STAGE"),
              ("deeprun", "DEEP RUN", "DEPTH")]
RANK_SIZE = 10


def add_ranking(save, mode, entry):
    """랭킹에 한 판을 넣고 몇 등인지 돌려줘요 (1등부터). 10등 안에 못 들면 None.
    점수가 같으면 먼저 세운 기록이 위에 남아요."""
    table = save.setdefault("rankings", {}).setdefault(mode, [])
    table.append(entry)
    table.sort(key=lambda e: -e["score"])      # sort 는 같은 점수끼리 원래 순서를 지켜요
    del table[RANK_SIZE:]
    for i, e in enumerate(table):
        if e is entry:
            return i + 1
    return None


def top_score(save, mode):
    """그 모드의 1등 점수 (기록이 없으면 0)"""
    table = save.get("rankings", {}).get(mode, [])
    return table[0]["score"] if table else 0


def export_code(save):
    """저장 정보를 글자 코드로: SZ1.<압축한 내용>.<검사 숫자>  (해상도는 기기마다 달라서 빼요)"""
    data = {k: v for k, v in save.items() if k != "res"}
    packed = base64.urlsafe_b64encode(zlib.compress(json.dumps(data, separators=(",", ":")).encode(), 9)).decode()
    return f"SZ1.{packed}.{zlib.crc32(packed.encode()):08x}"


def import_code(text):
    """코드를 저장 정보(dict)로. 틀린 코드면 None (한 글자라도 틀리면 검사 숫자가 안 맞아요)"""
    try:
        text = "".join(text.split())                   # 줄바꿈/빈칸 제거
        start = text.index("SZ1.")
        _, packed, check = text[start:].split(".")[:3]
        if f"{zlib.crc32(packed.encode()):08x}" != check[:8]:
            return None
        data = json.loads(zlib.decompress(base64.urlsafe_b64decode(packed.encode())).decode())
        return data if isinstance(data, dict) else None
    except Exception:
        return None


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
STREAKS = [(3, "RADAR"), (5, "AIRSTRIKE"), (7, "SENTRY"), (10, "CHOPPER")]
STREAK_KILLS = ("AIRSTRIKE!", "SENTRY", "ALLY", "TRAP", "CHOPPER")
CHOPPER_TIME, CHOPPER_RADIUS, CHOPPER_LIFT = 20.0, 5.5, 3.2   # 헬기 지원: 시간, 도는 반지름, 높이   # 킬스트릭으로 쓰러뜨린 건 연속 처치 수에 안 세요
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
ECHOES = {"OFFICE BLOCK": (0.12, 0.45), "NEON BEACH": (0.35, 0.12), "DOWNTOWN": (0.18, 0.35), "HARBOR": (0.22, 0.3), "DESERT TOWN": (0.25, 0.2),
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
# 잠입: 적이 나를 알아채는 데 걸리는 시간. 앞쪽 시야(약 140도) 안에서만 알아채요 (가까우면 바로)
VIEW_COS = math.cos(math.radians(70))
AWARE_DECAY = 0.25                # 안 보이면 1초에 이만큼 줄어요
TAKEDOWN_XP = 50                  # 뒤에서 몰래 처치 보너스
KNIFE_TIME = 0.3                  # 칼 휘두르는 시간
KNIFE_COOLDOWN = 0.6

PICKUP_RADIUS = 0.7
DROP_CHANCE = 0.8                 # 적이 상자를 떨어뜨릴 확률
DROP_WEIGHTS = {"ammo": 5, "health": 3, "grenade": 2}
HEALTH_PACK = 35

# 로드아웃: 시작하기 전에 주무기 / 보조무기 / 퍼크(특수 능력)를 골라요
PRIMARIES = ["RIFLE", "HEAVY AR", "BURST", "SMG", "SHOTGUN", "AUTO SHOTGUN", "LMG", "DMR", "SNIPER"]
SECONDARIES = ["PISTOL", "REVOLVER", "MACHINE PISTOL", "ROCKET", "LAUNCHER"]
DEFAULT_LOADOUT = dict(primary="RIFLE", secondary="PISTOL", perk="HEAVY ROUNDS", tactical="FLASHBANG")
TACTICAL_COUNT = 2                # 라운드마다 전술 장비 개수
CUSTOM_INDEX = None               # 내가 만든 맵을 MAPS 의 몇 번째에 넣었는지
# 하이라이트: 0.1초마다 작은 화면을 기억해 두었다가, 라운드의 가장 멋진 순간을 끝날 때 다시 보여줘요
CLIP_FPS, CLIP_BEFORE, CLIP_AFTER, CLIP_SIZE = 10, 2.5, 0.8, (320, 180)
# 좀비 모드 2탄: B 로 사는 것들 (가까이 가면 화면 아래에 이름과 가격)
BARRICADE_COST = 750
WALL_WEAPONS = [("SMG", 1000), ("SHOTGUN", 1250), ("AUTO SHOTGUN", 1750)]   # 맵의 'y' 를 읽는 순서대로
BOX_COST = 950
TRAP_COST, TRAP_TIME, TRAP_DPS = 1000, 15.0, 400
TITAN_POINTS = 1000
FLASH_RANGE = 7.0                 # 섬광탄이 닿는 거리
SMOKE_TIME, SMOKE_RADIUS = 10.0, 1.7
SMOKES = []                       # 지금 피어 있는 연막: [위치, 남은 시간] (적의 시야 검사에서 써요)


def smoke_blocks(a, b):
    """a와 b 사이에 연막이 있으면 True (선분과 원이 닿는지)"""
    for center, life in SMOKES:
        radius = SMOKE_RADIUS * min(1.0, life / 1.5, (SMOKE_TIME - life + 0.3) / 1.0)
        ab = b - a
        t = 0.0 if ab.length_squared() == 0 else max(0.0, min(1.0, (center - a).dot(ab) / ab.length_squared()))
        if (a + ab * t).distance_to(center) < radius:
            return True
    return False


def gunsmith_default(save, name):
    """총기 개조를 아직 안 했을 때의 부착물 (예전처럼 처치 수로 풀린 것을 자동으로)"""
    mods = weapon_mods(save.get("wkills", {}).get(name, 0))
    return {"OPTIC": "IRON SIGHTS", "MUZZLE": "SUPPRESSOR" if "SUPPRESSOR" in mods else "NONE",
            "MAGAZINE": "EXT MAG" if "EXT MAG" in mods else "STANDARD",
            "GRIP": "VERTICAL GRIP" if "GRIP" in mods else "NONE"}


def attachment_unlocked(save, name, slot, choice):
    kills = save.get("wkills", {}).get(name, 0)
    need = next(level for option, level, _ in ATTACHMENTS[slot] if option == choice)
    legacy = {"EXT MAG": "EXT MAG", "VERTICAL GRIP": "GRIP", "SUPPRESSOR": "SUPPRESSOR"}.get(choice)
    return weapon_level(kills) >= need or (legacy is not None and legacy in weapon_mods(kills))


def apply_gunsmith(spec, choices):
    """고른 부착물의 성능을 무기에 적용 (새 dict)"""
    spec = dict(spec)
    for slot, choice in choices.items():
        if slot == "OPTIC" and (spec["scope"] or spec["projectile"]):
            continue                                   # 저격총/발사기는 조준경을 안 바꿔요
        effect = next((e for option, _, e in ATTACHMENTS[slot] if option == choice), {})
        for key, value in effect.items():
            if key == "suppressed":
                if not spec["projectile"]:
                    spec["suppressed"] = True
            elif key == "ads_spread":
                spec["ads_spread"] = value
            elif key in ("mag", "reserve"):
                if not spec["projectile"]:
                    spec[key] = max(1, int(spec[key] * value))
            elif key in ("hip", "recoil", "move"):
                spec[key] = spec.get(key, 1.0) * value
            else:                                      # ads, kick, reload
                spec[key] = spec[key] * value
    spec["attachments"] = choices
    return spec


WEAPON_BY_NAME = {spec["name"]: spec for spec in WEAPONS}
# 고정 기관총 (맵의 모래주머니·돌담 뒤에 놓여 있어요, B 로 타고 내려요)
MOUNTED_MG = dict(WEAPON_BY_NAME["LMG"], name="MOUNTED MG", delay=0.07, mag=999, reserve=0, body=40, head=110,
                  spread=4, kick=4, move=0.0)
GUN_LOOKS["MOUNTED MG"] = GUN_LOOKS["LMG"]
GUN_SOUNDS["MOUNTED MG"] = "lmg"
MG_HEAT_PER_SHOT, MG_COOL, MG_OVERHEAT = 0.04, 0.45, 2.5   # 열: 한 발에 4%, 쉬면 1초에 45% 식음, 과열되면 2.5초 못 쏴요

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
    # 바닥 깊이감: 발밑(가까운 곳)은 조금 어둡고 멀어질수록 밝아져요 (거리 0~7칸)
    FLOOR_DEPTH.clear()
    FLOOR_DEPTH.update({k: [shade(c, 0.74 + 0.26 * min(1.0, d / 7)) for d in range(8)] for k, c in FLOOR_COLORS.items()})
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


def walk_clear(a, b, radius=0.18):
    """a에서 b까지 똑바로 걸어갈 수 있으면 True (몸 폭만큼 양옆도 검사, 닫힌 문은 막힘)"""
    offset = b - a
    dist = offset.length()
    if dist < 0.05:
        return True
    step = offset / dist
    side = pygame.Vector2(-step.y, step.x) * radius
    for k in range(1, int(dist / 0.3) + 1):
        q = a + step * (k * 0.3)
        if is_blocked(q.x, q.y) or is_blocked(q.x + side.x, q.y + side.y) or is_blocked(q.x - side.x, q.y - side.y):
            return False
    return True


def walkable_cell(col, row):
    """길찾기용: 걸어갈 수 있는 칸 (문은 가까이 가면 열리니까 지나갈 수 있어요)"""
    return in_map(col, row) and (not is_blocked(col + 0.5, row + 0.5) or GAME_MAP[row][col] in DOORS)


def build_flow(goal):
    """길찾기 지도: goal 칸에서 시작해 걸어갈 수 있는 칸마다 걸음 수를 적어요 (너비 우선 탐색)"""
    flow = [[None] * MAP_W for _ in range(MAP_H)]
    col, row = goal
    if not in_map(col, row):
        return flow
    flow[row][col] = 0
    queue = deque([goal])
    while queue:
        col, row = queue.popleft()
        d = flow[row][col] + 1
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c, r = col + dc, row + dr
            if 0 <= c < MAP_W and 0 <= r < MAP_H and flow[r][c] is None and walkable_cell(c, r):
                flow[r][c] = d
                queue.append((c, r))
    return flow


def flow_step(flow, pos):
    """길찾기 지도에서 목표에 한 걸음 더 가까운 옆 칸의 가운데 (대각선은 모서리를 가로지르지 않게)"""
    col, row = int(pos.x), int(pos.y)
    here = flow[row][col] if in_map(col, row) and flow[row][col] is not None else math.inf
    best, best_d = None, here
    for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
        c, r = col + dc, row + dr
        if not in_map(c, r) or flow[r][c] is None:
            continue
        if dc and dr and (not walkable_cell(col + dc, row) or not walkable_cell(col, row + dr)):
            continue
        d = flow[r][c] + (0.4 if dc and dr else 0)
        if d < best_d:
            best, best_d = (c, r), d
    return pygame.Vector2(best[0] + 0.5, best[1] + 0.5) if best else None


class Navigator:
    """길찾기 지도를 목표 칸마다 만들어 잠깐 기억해 둬요 (Game이 하나 가지고 있어요)"""

    def __init__(self):
        self.cache = {}
        self.clock = 0.0

    def clear(self):
        self.cache = {}

    def flow_to(self, goal):
        cell = (int(goal.x), int(goal.y))
        hit = self.cache.get(cell)
        if hit and self.clock - hit[1] < 2.0:
            return hit[0]
        if len(self.cache) > 24:                         # 오래된 것부터 버려요
            del self.cache[min(self.cache, key=lambda k: self.cache[k][1])]
        flow = build_flow(cell)
        self.cache[cell] = (flow, self.clock)
        return flow


def steer(agent, goal, dt):
    """agent(적/동료)가 goal 로 가려면 지금 어느 쪽으로 가야 하는지 (길이 1인 방향).
    똑바로 갈 수 있으면 곧장, 막혀 있으면 길찾기 지도를 따라 벽을 돌아가요. 0.25초마다 다시 계산."""
    agent.nav_timer -= dt
    target = agent.nav_target
    if (agent.nav_goal is None or agent.nav_goal.distance_to(goal) > 0.8 or agent.nav_timer <= 0
            or (target is not None and agent.pos.distance_to(target) < 0.25)):
        agent.nav_timer = 0.25
        agent.nav_goal = pygame.Vector2(goal)
        if walk_clear(agent.pos, goal) or NAVIGATOR is None:
            agent.nav_target = None                     # 곧장 가요
        else:
            agent.nav_target = flow_step(NAVIGATOR.flow_to(goal), agent.pos)
        target = agent.nav_target
    offset = (target if target is not None else goal) - agent.pos
    return offset.normalize() if offset.length() > 1e-6 else pygame.Vector2()


NAVIGATOR = None   # 지금 게임의 Navigator (Game.setup_map 에서 정해요)


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


FLOOR_DEPTH = {}                  # 바닥 글자 → 거리별 색 (load_map 에서 채워요)
GFX_NAMES = ["LOW", "NORMAL", "HIGH"]
# 맵 분위기별 색 보정: (곱할 색, 더할 색). 곱하면 색이 물들고, 조금 더하면 어두운 곳이 부드러워져요
GRADES = {"snow": ((222, 234, 255), (2, 6, 14)), "night": ((216, 220, 242), (2, 3, 12)),
          "rain": ((212, 218, 224), (6, 6, 10)), "warm": ((255, 236, 212), (12, 5, 0)),
          "default": ((248, 244, 238), (5, 4, 2))}


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
MAPS[-1:-1] = [LIGHTHOUSE_POINT] + GENERATED_MAPS + [OFFICE_BLOCK]   # 좀비 맵(마지막) 앞에 (등대 13번째, 사무실 22번째)

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

# 캠페인에서 라운드마다 돌아가며 나오는 맵 (좀비, 미션 맵은 빼고) - 22개.
# 세트는 20라운드씩이라 세트마다 시작 맵이 하나씩 밀려요
CAMPAIGN_MAPS = [i for i, m in enumerate(MAPS) if not m.get("zombie") and not m.get("mission")]
ZOMBIE_MAP = next(i for i, m in enumerate(MAPS) if m.get("zombie"))

# 캠페인 100라운드 = 20라운드 x 5세트 (맵 22개가 차례로 돌아요). 세트마다 분위기가 바뀌고 적이 강해져요
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
                 "F": "stone", "O": "concrete", "V": "stone", "Z": "sandbag", "i": "stucco", "d": "planks", "q": "planks", "y": "planks"}
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


def make_barrel_image():
    """터지는 빨간 드럼통 (노란 줄 + 불꽃 표시)"""
    img = pygame.Surface((40, 56), pygame.SRCALPHA)
    pygame.draw.rect(img, (190, 40, 35), (3, 4, 34, 50), border_radius=6)
    pygame.draw.rect(img, (140, 25, 25), (3, 4, 34, 50), 2, border_radius=6)
    for y in (16, 38):
        pygame.draw.rect(img, (230, 200, 60), (3, y, 34, 4))
    pygame.draw.polygon(img, (255, 230, 120), [(20, 22), (26, 32), (14, 32)])     # 위험 표시
    pygame.draw.ellipse(img, (120, 25, 25), (5, 1, 30, 8))
    return img


def make_alarm_image(on):
    """경보기: 기둥 위 노란 상자와 빨간 등 (울리면 밝아요)"""
    img = pygame.Surface((30, 120), pygame.SRCALPHA)
    pygame.draw.rect(img, (70, 70, 80), (13, 30, 5, 90))
    pygame.draw.rect(img, (220, 190, 40), (3, 10, 24, 24), border_radius=3)
    pygame.draw.rect(img, (40, 40, 40), (3, 10, 24, 24), 2, border_radius=3)
    pygame.draw.circle(img, (255, 60, 60) if on else (120, 30, 30), (15, 8), 7)
    if on:
        pygame.draw.circle(img, (255, 200, 200), (15, 8), 3)
    return img


def make_broken_lamp(image):
    """깨진 가로등: 불빛 부분을 어둡게"""
    img = image.copy()
    pygame.draw.circle(img, (50, 50, 55), (20, 26), 10)
    return img


class Device:
    """맵의 장치: 드럼통(쏘면 폭발) / 경보기(적이 나를 보고 8초 안에 못 부수면 증원)"""

    def __init__(self, kind, x, y):
        self.kind = kind
        self.pos = pygame.Vector2(x, y)
        self.hp = DEVICE_HP[kind]
        self.timer = 0.0          # 경보기: 울리기까지 / 울리는 시간
        self.state = "idle"       # 경보기: idle → arming → ringing → done


DEVICE_HP = {"barrel": 20, "alarm": 12}
DEVICE_SIZE = {"barrel": (0.6, 0.45), "alarm": (1.4, 0.3)}     # (높이, 너비)
BARREL_BLAST = (2.6, 95)          # 드럼통 폭발: (반경, 피해)
ALARM_DELAY = 8.0                 # 적이 나를 보고 경보가 울리기까지(초)
ALARM_BACKUP = 3                  # 경보가 울리면 오는 적 수


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


def make_chopper_image(flash=False):
    """지원 헬기 (옆모습): 몸통, 꼬리, 프로펠러"""
    img = pygame.Surface((120, 50), pygame.SRCALPHA)
    pygame.draw.ellipse(img, (55, 70, 55), (30, 16, 52, 28))                    # 몸통
    pygame.draw.ellipse(img, (150, 200, 230), (62, 20, 18, 14))                 # 조종석 유리
    pygame.draw.rect(img, (55, 70, 55), (2, 24, 34, 7))                         # 꼬리
    pygame.draw.rect(img, (40, 50, 40), (0, 16, 6, 16))                         # 꼬리 날개
    pygame.draw.rect(img, (30, 30, 30), (8, 6, 104, 3))                         # 위 프로펠러
    pygame.draw.rect(img, (30, 30, 30), (52, 8, 6, 9))
    pygame.draw.line(img, (30, 30, 30), (40, 46), (80, 46), 3)                 # 다리
    pygame.draw.rect(img, (25, 25, 25), (74, 38, 16, 5))                        # 기관총
    if flash:
        pygame.draw.circle(img, YELLOW, (92, 41), 6)
    return img


def make_mg_image():
    """고정 기관총: 삼각대 위의 큰 총"""
    img = pygame.Surface((70, 50), pygame.SRCALPHA)
    for x in (12, 35, 58):                                                     # 삼각대 다리
        pygame.draw.line(img, (40, 40, 45), (35, 22), (x, 49), 4)
    pygame.draw.rect(img, (45, 48, 52), (8, 12, 56, 12), border_radius=3)        # 총몸
    pygame.draw.rect(img, (30, 30, 34), (0, 15, 14, 5))                          # 총열
    pygame.draw.rect(img, (70, 75, 60), (36, 6, 14, 8))                          # 탄통
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


def step_sound_at(pos):
    col, row = int(pos.x), int(pos.y)
    floor = FLOOR_GRID[row][col] if in_map(col, row) else ":"
    return STEP_SOUNDS.get(floor, "step_hard")


# 상황 따라 바뀌는 음악: 같은 박자의 네 겹을 같이 틀고 크기만 바꿔요
MUSIC_LAYERS = ["music", "music_drums", "music_bass", "music_lead"]   # 잔잔한 패드, 드럼, 베이스, 리드
MUSIC_MIX = {"calm": (1.0, 0.0, 0.0, 0.0), "relax": (0.9, 0.3, 0.0, 0.0), "alert": (1.0, 0.65, 0.8, 0.0),
             "peak": (1.0, 1.0, 1.0, 0.7), "boss": (1.0, 1.0, 1.0, 1.0), "over": (0.5, 0.0, 0.0, 0.0)}


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
            pygame.mixer.set_reserved(2 + len(MUSIC_LAYERS) - 1)   # 0번: 배경 소리, 1~4번: 음악 겹 (효과음이 빼앗지 않게)
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
        self.levels = [1.0] + [0.0] * (len(MUSIC_LAYERS) - 1)   # 음악 겹마다 지금 크기 (0~1)

    def make_loop(self, kind):
        """끊김 없이 반복되는 배경 소리. wind 바람 / rain 빗소리 / night 밤벌레 / music 낮게 깔리는 음악"""
        freq, channels = self.format
        rng = random.Random(7)
        seconds = 8.0 if kind.startswith("music") else 3.0
        step = 4 if kind == "wind" or kind.startswith("music") else 1      # 낮은 소리는 4칸마다 한 번만 계산 (빠르게)
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
            elif kind == "music_drums":            # 쿵(킥) - 탁(스네어) - 츠츠(하이햇), 1초에 2박
                kick = t % 0.5
                v = 0.55 * math.sin(2 * math.pi * (60 - 40 * kick) * kick) * math.exp(-kick * 22)
                snare = (t - 0.5) % 1.0
                v += 0.45 * rng.uniform(-1, 1) * math.exp(-snare * 28)
                hat = t % 0.25
                v += 0.12 * rng.uniform(-1, 1) * math.exp(-hat * 90)
            elif kind == "music_bass":             # 8분음표로 뛰는 낮은 베이스 (코드 바뀌는 대로)
                note = notes[int((t % seconds) / 2.0)] * 2
                pulse = t % 0.25
                saw = 2 * ((note * t) % 1.0) - 1
                v = 0.42 * saw * math.exp(-pulse * 7)
            elif kind == "music_lead":             # 클라이맥스/보스: 빠른 아르페지오
                note = notes[int((t % seconds) / 2.0)] * 4
                step16 = int(t / 0.125) % 4
                hz = note * (1.0, 1.25, 1.5, 2.0)[step16]
                env = math.exp(-(t % 0.125) * 14)
                v = 0.22 * env * (math.sin(2 * math.pi * hz * t) + 0.3 * math.sin(2 * math.pi * hz * 3 * t))
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
        channel = pygame.mixer.Channel(0)
        if kind not in self.loops:
            self.loops[kind] = self.make_loop(kind)
        if self.background != kind or not channel.get_busy():
            channel.play(self.loops[kind], loops=-1)
        # 음악 겹들은 길이가 같아서 한꺼번에 틀면 박자가 계속 맞아요
        layers = [pygame.mixer.Channel(1 + i) for i in range(len(MUSIC_LAYERS))]
        if not self.music_on:
            for layer in layers:
                layer.stop()
        elif not layers[0].get_busy():
            for name in MUSIC_LAYERS:
                if name not in self.loops:
                    self.loops[name] = self.make_loop(name)
            for name, layer in zip(MUSIC_LAYERS, layers):
                layer.play(self.loops[name], loops=-1)
        self.background = kind
        self.refresh_background()

    def mix_music(self, targets, dt):
        """음악 겹 크기를 targets 쪽으로 부드럽게 (올릴 땐 빠르게, 내릴 땐 천천히)"""
        for i, goal in enumerate(targets):
            now = self.levels[i]
            speed = 1.6 if goal > now else 0.45
            self.levels[i] = now + max(-speed * dt, min(speed * dt, goal - now))
        self.refresh_background()

    def play_sting(self):
        """라운드를 깨면 짧은 승리 소리 (도-미-솔-도)"""
        if not self.bank or self.muted:
            return
        if "sting" not in self.loops:
            freq, channels = self.format
            samples = array.array("h")
            for k, hz in enumerate((261.6, 329.6, 392.0, 523.3)):
                length = 0.11 if k < 3 else 0.5
                for i in range(int(length * freq)):
                    t = i / freq
                    v = 0.35 * math.exp(-t * (9 if k < 3 else 3)) * (math.sin(2 * math.pi * hz * t)
                                                                      + 0.4 * math.sin(4 * math.pi * hz * t))
                    samples.extend([int(v * 32767)] * channels)
            self.loops["sting"] = pygame.mixer.Sound(buffer=samples.tobytes())
        sound = self.loops["sting"]
        sound.set_volume(SETTINGS["volume"] / 100 * max(0.3, SETTINGS.get("music", 40) / 100))
        sound.play()

    def refresh_background(self):
        """소리 끄기(M)나 설정의 소리 크기를 배경 소리에도 반영해요"""
        if not self.bank:
            return
        volume = 0.0 if self.muted else SETTINGS["volume"] / 100
        pygame.mixer.Channel(0).set_volume(0.35 * volume)
        music = 0.5 * volume * SETTINGS.get("music", 40) / 100 if self.music_on else 0
        music *= getattr(self, "duck", 1.0)
        for i, level in enumerate(self.levels):
            pygame.mixer.Channel(1 + i).set_volume(music * level)

    def stop_background(self):
        if self.bank:
            for i in range(1 + len(MUSIC_LAYERS)):
                pygame.mixer.Channel(i).stop()
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
        if name != "ring":
            volume *= getattr(self, "duck", 1.0)          # 큰 폭발 뒤: 잠깐 다른 소리가 작게
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


def korean_font_path():
    """컴퓨터에 있는 한글 글꼴 파일 (웹이나 없으면 None)"""
    return None if IN_BROWSER else pygame.font.match_font(KOREAN_FONTS)


KO_FONT_SCALE = 0.78       # 한글 글꼴은 같은 크기 숫자에서 더 커서 줄여 써요


def make_fonts(korean_ui=True):
    """화면 크기에 맞춘 글꼴들. 한글 글꼴이 있고 설정 LANGUAGE 가 KOREAN 이면 메뉴를 한글로 보여줘요.
    korean_ui=False: 게임 화면(HUD)용 - 숫자와 영어는 원래 글꼴, 도움말만 한글"""
    ko_path = korean_font_path()
    use_ko = bool(ko_path) and SETTINGS.get("lang", 0) == 0
    sizes = dict(tiny=18, small=22, normal=30, big=56, title=100)
    if use_ko and korean_ui:
        fonts = {name: pygame.font.Font(ko_path, int(size * KO_FONT_SCALE * UI)) for name, size in sizes.items()}
        for name in ("normal", "big", "title"):
            fonts[name].set_bold(True)             # 제목과 메뉴 이름은 굵게 (원래 글꼴처럼 또렷하게)
    else:
        fonts = {name: pygame.font.Font(None, int(size * UI)) for name, size in sizes.items()}
    if use_ko:
        fonts["help"] = pygame.font.Font(ko_path, int(17 * UI))
        fonts["help_big"] = pygame.font.Font(ko_path, int(26 * UI))
    else:
        fonts["help"] = pygame.font.Font(None, int(24 * UI))
        fonts["help_big"] = pygame.font.Font(None, int(38 * UI))
    fonts = {key: ShadowFont(f) for key, f in fonts.items()}
    fonts["lang"] = "ko" if use_ko else "en"
    fonts["ko_ui"] = use_ko and korean_ui
    return fonts


# 메뉴 글자 한글 이름 (설정 LANGUAGE = KOREAN 일 때). 없는 글자는 영어 그대로
KO_TEXT = {
    "SETTINGS": "설정", "CONTROLS": "키 설정", "MY MAPS": "내 맵", "LEADERBOARD": "랭킹", "STATS": "기록",
    "CHALLENGES": "도전", "MISSIONS": "미션", "SKILLS": "스킬", "LOADOUT": "로드아웃", "ACHIEVEMENTS": "업적",
    "GUNSMITH": "총기 개조", "PAUSED": "일시정지", "CAMPAIGN": "캠페인", "CONTINUE": "이어하기", "ZOMBIES": "좀비",
    "TRAINING": "사격장", "DIFFICULTY": "난이도", "RESOLUTION": "해상도", "HOW TO PLAY": "조작법",
    "PLAY": "플레이", "PROFILE": "내 정보", "RESUME": "계속하기", "HELP": "도움말", "PHOTO MODE": "사진 모드",
    "QUIT TO MENU": "메뉴로 나가기", "START WEAPON": "시작 무기", "SECOND WEAPON (Q)": "두 번째 무기 (Q)",
    "PERK": "퍼크", "TACTICAL (N)": "전술 장비 (N)", "INVENTORY": "무기 목록", "SCORE": "점수", "WAVE": "웨이브",
    "ROUND": "라운드", "STAGE": "단계", "KILLS": "처치", "MAP": "맵", "DATE": "날짜",
    "LOOK SPEED": "시점 속도", "MOUSE SPEED": "마우스 속도", "AIM ASSIST": "조준 보정", "FIELD OF VIEW": "시야각",
    "VOLUME": "소리", "MUSIC": "음악", "FULLSCREEN": "전체 화면", "SQUADMATES": "동료", "UI SIZE": "글자 크기",
    "SCREEN SHAKE": "화면 흔들림", "SOUND MARKS": "소리 표시", "COLORBLIND": "색약 모드", "LANGUAGE": "언어",
    "WEAPONS": "무기", "RECENT GAMES": "최근 판", "DEEP RUN": "딥 런", "DEPTH": "깊이", "DISPLAY": "화면", "SOUND": "소리", "INPUT": "조작", "GAME": "게임", "GRAPHICS": "그래픽",
}


def tr(fonts, text):
    """한글 메뉴면 KO_TEXT 로 바꿔요. 'ACHIEVEMENTS  3 / 16' 처럼 뒤에 숫자가 붙어도 앞 이름만 바꿔요"""
    if not fonts.get("ko_ui"):
        return text
    if text in KO_TEXT:
        return KO_TEXT[text]
    for key in sorted(KO_TEXT, key=len, reverse=True):
        if text.startswith(key + " "):
            return KO_TEXT[key] + text[len(key):]
    return text


# ----- 메뉴 화면 공통 부품 -----
# 모든 메뉴가 같은 배경, 제목, 칸, 아래 키 안내를 써서 모양과 간격이 똑같아요.
UI_ACCENT = (255, 80, 200)        # 분홍 (제목, 고른 칸 테두리)
UI_CYAN = (80, 240, 255)
UI_PANEL = (24, 18, 44)           # 칸 바탕
UI_PANEL_ON = (60, 40, 90)        # 고른 칸 바탕
UI_EDGE = (70, 60, 100)           # 칸 테두리
UI_DIM = (150, 150, 170)          # 흐린 글자
UI_KEY_WORDS = {"Enter", "Backspace", "Tab", "Shift", "Space", "Esc"}
_backdrop_cache = {}


def draw_backdrop(screen):
    """메뉴 배경: 위는 보라, 아래로 갈수록 어두워지고 바닥에 옅은 격자"""
    key = (WIDTH, HEIGHT)
    if key not in _backdrop_cache:
        _backdrop_cache.clear()
        image = pygame.Surface(key)
        for y in range(HEIGHT):
            t = y / HEIGHT
            image.fill((int(22 - 12 * t), int(14 - 6 * t), int(44 - 22 * t)), (0, y, WIDTH, 1))
        grid = pygame.Surface(key, pygame.SRCALPHA)
        horizon = HEIGHT * 0.62
        for i in range(1, 12):                              # 멀어질수록 촘촘한 가로줄
            y = horizon + (HEIGHT - horizon) * (i / 11) ** 1.8
            pygame.draw.line(grid, (255, 80, 200, 10 + i * 2), (0, y), (WIDTH, y))
        for i in range(-12, 13):                            # 한 점으로 모이는 세로줄
            pygame.draw.line(grid, (80, 240, 255, 14), (WIDTH / 2 + i * WIDTH * 0.02, horizon),
                             (WIDTH / 2 + i * WIDTH * 0.12, HEIGHT))
        image.blit(grid, (0, 0))
        _backdrop_cache[key] = image
    screen.blit(_backdrop_cache[key], (0, 0))


def draw_title(screen, fonts, text, pos, anchor="midleft"):
    """메뉴 제목 + 아래 분홍 밑줄"""
    image = fonts["big"].render(tr(fonts, text), True, UI_ACCENT)
    rect = image.get_rect(**{anchor: pos})
    screen.blit(image, rect)
    line = pygame.Rect(rect.x + 2, rect.bottom - 2 * UI, min(rect.width, 160 * UI), 3 * UI)
    pygame.draw.rect(screen, UI_ACCENT, line, border_radius=2)
    pygame.draw.rect(screen, UI_CYAN, (line.right + 4 * UI, line.y, 18 * UI, line.h), border_radius=2)
    return rect


def draw_panel(screen, rect, selected=False, radius=8):
    """메뉴 칸: 고른 칸은 밝은 바탕 + 분홍 테두리 + 은은한 빛"""
    rect = pygame.Rect(rect)
    if selected:
        glow = pygame.Surface((rect.w + 16, rect.h + 16), pygame.SRCALPHA)
        pygame.draw.rect(glow, (255, 80, 200, 50), glow.get_rect(), 6, border_radius=radius + 6)
        screen.blit(glow, (rect.x - 8, rect.y - 8))
    pygame.draw.rect(screen, UI_PANEL_ON if selected else UI_PANEL, rect, border_radius=radius)
    pygame.draw.line(screen, (255, 255, 255) if selected else (50, 44, 76),
                     (rect.x + radius, rect.y + 1), (rect.right - radius, rect.y + 1))     # 위쪽 하이라이트
    pygame.draw.rect(screen, UI_ACCENT if selected else UI_EDGE, rect, 3 if selected else 1, border_radius=radius)


def split_hint(hint):
    """'↑↓ 고르기   Enter 시작   - 설명' → [(키, 설명), ...]. 키가 없는 부분은 ('', 글자)"""
    items = []
    for part in re.split(r"\s{3,}", hint.strip()):
        words = part.split(" ")
        if part.startswith(("-", "(")):
            items.append(("", part))
            continue
        keys = []
        while words and (words[0] in UI_KEY_WORDS or words[0] == "/" or
                         not re.search(r"[a-z\uac00-\ud7a3]", words[0])):
            keys.append(words.pop(0))
        items.append((" ".join(keys), " ".join(words)))
    return items


def draw_keycap(screen, font, key, x, cy, color=YELLOW):
    """키 모양 상자 [Enter] 를 그리고 오른쪽 끝 x 를 돌려줘요"""
    image = font.render(key, True, color)
    rect = pygame.Rect(x, 0, image.get_width() + 12 * UI, image.get_height() + 4 * UI)
    rect.centery = cy
    pygame.draw.rect(screen, (34, 28, 58), rect, border_radius=int(5 * UI))
    pygame.draw.rect(screen, color, rect, 1, border_radius=int(5 * UI))
    screen.blit(image, image.get_rect(center=rect.center))
    return rect.right


def key_text_width(font, parts):
    """draw_key_text 로 그렸을 때의 너비"""
    gap, pad = 14 * UI, 6 * UI
    return sum((font.size(k)[0] + 12 * UI + pad if k else 0) + font.size(t)[0] for k, t in parts) + gap * (len(parts) - 1)


def draw_key_text(screen, font, parts, pos, anchor="center", color=WHITE, alpha=255):
    """키 상자 + 설명을 한 줄로: parts = [(키, 설명), ...] (키가 None 이면 설명만). 그린 범위를 돌려줘요"""
    gap, pad = 14 * UI, 6 * UI
    widths = [(font.size(k)[0] + 12 * UI + pad if k else 0) + font.size(t)[0] for k, t in parts]
    total = sum(widths) + gap * (len(parts) - 1)
    height = font.get_linesize() + 4 * UI
    area = pygame.Rect(0, 0, total, height)
    setattr(area, anchor, pos)
    layer = screen if alpha >= 255 else pygame.Surface(area.size, pygame.SRCALPHA)
    x, cy = (area.x, area.centery) if layer is screen else (0, area.h / 2)
    for (key, text), w in zip(parts, widths):
        if key:
            x = draw_keycap(layer, font, key, x, cy) + pad
        image = font.render(text, True, color)
        layer.blit(image, image.get_rect(midleft=(x, cy)))
        x += image.get_width() + gap
    if layer is not screen:
        layer.set_alpha(alpha)
        screen.blit(layer, area)
    return area


def draw_hint_bar(screen, fonts, hint):
    """화면 맨 아래 키 안내 띠. 너무 길면 설명(- ...)을 빼고, 그래도 길면 작은 글자로"""
    bar = pygame.Rect(0, HEIGHT - 40 * UI, WIDTH, 40 * UI)
    shade_img = pygame.Surface(bar.size, pygame.SRCALPHA)
    shade_img.fill((8, 6, 20, 210))
    screen.blit(shade_img, bar)
    pygame.draw.line(screen, UI_EDGE, bar.topleft, bar.topright)
    items = split_hint(hint)
    for font, keep_notes in ((fonts["help"], True), (fonts["help"], False), (fonts["tiny"], False)):
        shown = [it for it in items if keep_notes or it[0]]
        gap = 22 * UI
        width = sum(font.size(k)[0] + 16 * UI + font.size(t)[0] + gap for k, t in shown) - gap
        if width <= WIDTH * 0.96:
            break
    x = max(WIDTH * 0.02, (WIDTH - width) / 2)
    for key, text in shown:
        need = (font.size(key)[0] + 18 * UI if key else 0) + font.size(text)[0]
        if x + need > WIDTH * 0.99:
            break                                          # 더는 안 들어가요 (중요한 키가 앞에 있어요)
        if key:
            x = draw_keycap(screen, font, key, x, bar.centery) + 6 * UI
        image = font.render(text, True, WHITE if key else UI_DIM)
        screen.blit(image, image.get_rect(midleft=(x, bar.centery)))
        x += image.get_width() + gap


def big_ammo_width(game):
    """오른쪽 아래 총알 숫자(큰 글자)의 너비"""
    w = game.arsenal.current
    text = "RELOADING..." if game.arsenal.reload_left > 0 else f"{w.mag} / {w.reserve}"
    return game.fonts["big"].size(text)[0]


_icon_cache = {}


def make_icon(kind, h, color=(235, 235, 240)):
    """HUD 작은 그림 아이콘 (그림 파일 없이 코드로). kind: 무기 종류(RIFLES...) / GRENADE / FLASHBANG /
    SMOKE / THROWING KNIFE / RADAR / AIRSTRIKE / SENTRY / CHOPPER. 높이 h, 무기는 너비 3h"""
    key = (kind, int(h), color)
    if key in _icon_cache:
        return _icon_cache[key]
    h = max(8, int(h))
    wide = kind in ("RIFLES", "SMGS", "SHOTGUNS", "MARKSMAN", "LMGS", "LAUNCHERS", "PISTOLS", "OTHER")
    img = pygame.Surface((h * 3 if wide else h, h), pygame.SRCALPHA)
    u = h / 10                                                   # 그림 단위
    c, dark = color, tuple(int(v * 0.55) for v in color)

    def r(x, y, w, hh, col=c):
        pygame.draw.rect(img, col, (x * u, y * u, max(1, w * u), max(1, hh * u)))
    if kind == "PISTOLS":
        r(9, 2, 12, 3); r(10, 5, 3, 5); r(20, 2, 2, 2, dark)
    elif kind == "SMGS":
        r(5, 3, 16, 3); r(21, 3, 4, 2); r(11, 6, 2, 4); r(7, 6, 2, 3, dark); r(2, 3, 3, 2)
    elif kind == "SHOTGUNS":
        r(1, 3, 6, 3); r(7, 3, 22, 2); r(9, 5, 14, 2, dark); r(9, 5, 2, 4)
    elif kind == "MARKSMAN":
        r(1, 4, 6, 3); r(7, 4, 22, 2); r(10, 1, 8, 2, dark); r(12, 6, 2, 3); r(16, 6, 2, 2)
    elif kind == "LMGS":
        r(1, 3, 6, 3); r(7, 3, 21, 3); r(11, 6, 6, 4, dark); r(25, 6, 1, 4); r(23, 6, 1, 4)
    elif kind == "LAUNCHERS":
        r(2, 3, 26, 4); r(28, 2, 2, 6, dark); r(10, 7, 2, 3); r(16, 7, 2, 2)
    elif wide:                                                   # 돌격소총 (기본)
        r(1, 3, 6, 3); r(7, 3, 19, 3); r(26, 4, 4, 1); r(13, 6, 3, 4, dark); r(10, 6, 2, 3)
    elif kind == "GRENADE":
        pygame.draw.circle(img, c, (h * 0.5, h * 0.6), h * 0.36)
        r(4, 0, 3, 2, dark); r(6, 1, 3, 1)
    elif kind == "FLASHBANG":
        r(3, 2, 4, 8); r(3, 1, 4, 1, dark)
        pygame.draw.line(img, (255, 240, 120), (h * 0.1, h * 0.3), (h * 0.25, h * 0.45), max(1, int(u)))
    elif kind == "SMOKE":
        r(3, 3, 4, 7); pygame.draw.circle(img, dark, (h * 0.5, h * 0.2), h * 0.18)
    elif kind == "THROWING KNIFE":
        pygame.draw.polygon(img, c, [(h * 0.1, h * 0.9), (h * 0.85, h * 0.15), (h * 0.95, h * 0.25), (h * 0.25, h * 0.95)])
    elif kind == "RADAR":
        pygame.draw.circle(img, c, (h / 2, h / 2), h * 0.45, max(1, int(u)))
        pygame.draw.circle(img, c, (h / 2, h / 2), h * 0.2, max(1, int(u)))
        pygame.draw.line(img, c, (h / 2, h / 2), (h * 0.85, h * 0.2), max(1, int(u)))
    elif kind == "AIRSTRIKE":
        pygame.draw.polygon(img, c, [(h * 0.5, 0), (h * 0.62, h * 0.4), (h, h * 0.55), (h * 0.62, h * 0.6),
                                     (h * 0.6, h * 0.85), (h * 0.75, h), (h * 0.25, h), (h * 0.4, h * 0.85),
                                     (h * 0.38, h * 0.6), (0, h * 0.55), (h * 0.38, h * 0.4)])
    elif kind == "SENTRY":
        r(4, 1, 2, 5); r(2, 2, 7, 2); pygame.draw.line(img, c, (h * 0.5, h * 0.6), (h * 0.15, h), max(1, int(u)))
        pygame.draw.line(img, c, (h * 0.5, h * 0.6), (h * 0.85, h), max(1, int(u)))
    elif kind == "CHOPPER":
        r(1, 1, 8, 1); r(3, 3, 5, 4); r(8, 4, 2, 1); r(4, 2, 1, 1, dark); r(3, 8, 5, 1)
    else:
        pygame.draw.circle(img, c, (h / 2, h / 2), h * 0.4)
    _icon_cache[key] = img
    return img


def make_bottom_shade():
    """화면 아래쪽을 살짝 어둡게 하는 그라데이션 (HUD 글자가 잘 보이게)"""
    height = int(130 * UI)
    shade_img = pygame.Surface((WIDTH, height), pygame.SRCALPHA)
    for y in range(height):
        shade_img.fill((0, 0, 0, int(120 * (y / height) ** 1.6)), (0, y, WIDTH, 1))
    return shade_img


def fit_text(font, text, max_width):
    """글자가 max_width 보다 길면 뒤를 잘라서 '..' 을 붙여요 (칸 밖으로 안 넘치게)"""
    if font.size(text)[0] <= max_width:
        return text
    while len(text) > 1 and font.size(text + "..")[0] > max_width:
        text = text[:-1]
    return text.rstrip() + ".."


def weapon_key_label(index):
    """무기 칸 번호: 1~9, 10번은 0, 11번부터는 번호 키가 없어요 (Tab 휠로 골라요)"""
    return str(index + 1) if index < 9 else ("0" if index == 9 else "")


class MaskedKeys:
    """몇몇 키를 '안 눌린 것'으로 보여줘요 (무기 휠을 여는 동안 화살표로 시점이 돌지 않게)"""

    def __init__(self, real, hidden):
        self.real, self.hidden = real, hidden

    def __getitem__(self, key):
        return False if key in self.hidden else bool(self.real[key])


ENDING_TIME = 40.0               # 엔딩 크레딧 길이(초)
SPRINT_FOV = 0.07                # 달리면 시야가 이만큼 넓어져요 (7%)
DIRECTOR_PEAK = 0.85       # 긴장감이 이만큼 차면 클라이맥스
DIRECTOR_PEAK_TIME = 5.0   # 클라이맥스 길이(초)
DIRECTOR_RELAX_TIME = 7.0  # 숨 돌리기 최소 길이(초)
DIRECTOR_MAX_ASSIST = 0.25
WHEEL_KEYS = (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_1, pygame.K_2, pygame.K_3,
              pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0)
# 이 말로 시작하는 알림은 왼쪽 카드로 (나머지는 조준점 아래 짧은 글자)
TOAST_WORDS = ("NEW ", "CONTRACT", "SECOND WIND", "SUPPLY", "RANK UP", "CHECKPOINT", "ACHIEVEMENT", "GOT ", "MYSTERY BOX", "TRAINING COMPLETE",
               "BOSS", "TITAN", "BARRICADE", "ELECTRIC TRAP", "MAX AMMO", "CHOPPER", "RADAR", "AIRSTRIKE", "SENTRY",
               "SOUND ", "FLASHLIGHT", "MOUNTED", "DISMOUNTED")
STRIP_SLOTS = 5            # 아래 무기 칸에 한 번에 보여줄 무기 수
PROMPT_Y = 168             # "B: 사기" 같은 안내 글자 높이 (화면 아래에서 px)
WHEEL_HOLD = 0.22          # Tab 을 이만큼(초) 누르고 있으면 무기 휠이 열려요
WHEEL_SLOW = 0.3           # 휠이 열린 동안 시간이 이만큼 느려져요


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
    """조작법과 팁을 보여주는 판. footer: 맨 아래에 보여줄 안내 문구.
    글자가 커서(UI SIZE) 화면에 다 안 들어가면 판 전체를 줄여서 보여줘요."""
    text = HELP_TEXT[fonts["lang"]]
    panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    panel.fill((10, 8, 25, 215))
    screen.blit(panel, (0, 0))
    big, small = fonts["help_big"], fonts["help"]
    line_h = small.get_linesize() * 1.15
    left, tip_left = WIDTH * 0.08, WIDTH * 0.52
    key_w = max(small.size(key)[0] for key, _ in text["keys"]) + 18 * UI
    tip_lines = []
    for tip in text["tips"]:
        for j, line in enumerate(wrap_text(small, tip, WIDTH * 0.42)):
            tip_lines.append(("-  " if j == 0 else "   ") + line)
        tip_lines.append(None)                                  # 팁 사이 작은 틈
    title_h = big.get_linesize() + 20 * UI
    body_h = max(len(text["keys"]) * line_h, sum(line_h if t else line_h * 0.25 for t in tip_lines))
    canvas = pygame.Surface((WIDTH, int(title_h + body_h + 10)), pygame.SRCALPHA)
    title = big.render(text["title"], True, (255, 80, 200))
    canvas.blit(title, title.get_rect(midtop=(WIDTH / 2, 0)))
    for i, (key, desc) in enumerate(text["keys"]):
        y = title_h + i * line_h
        canvas.blit(small.render(key, True, YELLOW), (left, y))
        desc = fit_text(small, desc, tip_left - left - key_w - 16 * UI)
        canvas.blit(small.render(desc, True, WHITE), (left + key_w, y))
    y = title_h
    for line in tip_lines:
        if line is None:
            y += line_h * 0.25
            continue
        canvas.blit(small.render(line, True, (200, 230, 255)), (tip_left, y))
        y += line_h
    room = HEIGHT * 0.78                                        # 위 여백 ~ 아래 안내 줄 사이
    if canvas.get_height() > room:
        scale = room / canvas.get_height()
        canvas = pygame.transform.smoothscale(canvas, (int(WIDTH * scale), int(canvas.get_height() * scale)))
    screen.blit(canvas, canvas.get_rect(midtop=(WIDTH / 2, max(HEIGHT * 0.08, (HEIGHT * 0.9 - canvas.get_height()) / 2))))
    if footer:
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
        self.nav_timer, self.nav_goal, self.nav_target = 0.0, None, None   # 길찾기 (steer)
        self.aware = 0.0          # 나를 알아챈 정도 0~1 (1이 되면 공격). 머리 위에 ? 로 보여요
        self.in_view = False
        self.combat_timer = 0.0   # 싸우는 중 (이때는 뒤도 봐요)
        self.alarm = 0.0          # 방금 알아챘을 때 머리 위 ! 표시 시간
        self.stun = 0.0           # 섬광탄에 멍해진 남은 시간 (아무것도 못 해요)
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
        if self.stun > 0:                         # 섬광탄: 눈이 부셔서 아무것도 못 해요
            self.stun -= dt
            self.sees = False
            return 0
        if t.get("melee"):
            return self.update_zombie(dt, player, dist)
        self.los_timer -= dt
        if self.los_timer <= 0:
            self.los_timer = 0.2
            # 시야 안에 있는지: 싸우는 중이거나 아주 가까우면 사방, 아니면 앞쪽만
            front = True
            if dist > 2.0 and self.combat_timer <= 0 and dist > 0:
                front = (player.pos - self.pos).normalize().dot(self.facing) > VIEW_COS
            self.in_view = (dist < t["sight"] and front and can_see(self.pos, player.pos)
                            and not (SMOKES and smoke_blocks(self.pos, player.pos)))
        self.combat_timer -= dt
        self.alarm -= dt
        if self.in_view:
            if not self.sees:                       # 알아채는 중: 가까울수록, 눈에 띌수록 빨리
                rate = player.visibility * max(1.0, self.skill) / (0.25 + dist * 0.06)
                self.aware = min(1.0, self.aware + rate * dt)
                if self.aware >= 1.0:
                    self.sees, self.alarm = True, 1.0
            self.combat_timer = max(self.combat_timer, 6.0) if self.sees else self.combat_timer
        else:
            self.sees = False
            self.aware = max(0.0, self.aware - AWARE_DECAY * dt)
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
                move_with_collision(self.pos, steer(self, self.flank_spot, dt) * t["speed"] * 1.1 * dt)
        elif dist > t["keep"] * (1.4 if self.role == "suppress" else 1.0):
            move_with_collision(self.pos, steer(self, player.pos, dt) * t["speed"] * dt)
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
                self.dir = steer(self, self.search, dt) or offset.normalize()
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
        self.facing = steer(self, target, dt) or offset.normalize()
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
        self.visibility = 1.0     # 눈에 띄는 정도 (앉으면/어두우면 작게, 손전등을 켜면 크게)
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


# 맞은 곳 재질: 벽 글자 / 바닥 글자 → 재질 이름
WALL_MATERIAL = {"W": "metal", "r": "metal", "u": "metal", "o": "metal", "Y": "metal", "U": "metal", "Z": "sand",
                 "R": "brick", "M": "brick", "K": "wood", "J": "wood", "d": "wood", "q": "wood", "y": "wood", "m": "wood",
                 "Q": "foliage", "V": "stone", "O": "stone", "F": "snow"}
FLOOR_MATERIAL = {"~": "water", ".": "sand", ";": "sand", "_": "dirt", "#": "dirt", "p": "dirt", "g": "grass",
                  "*": "snow", "-": "snow", "w": "wood"}
# 재질 → (파편 개수, 색들, 속도 범위, 수명 범위, 크기 범위, 소리)
IMPACT_STYLES = {
    "metal": (9, [(255, 230, 120), (255, 200, 80), (255, 255, 220)], (180, 420), (0.08, 0.22), (1.0, 2.2), "ping"),
    "wood": (7, [(150, 105, 60), (190, 140, 85), (110, 75, 45)], (60, 190), (0.3, 0.6), (2.0, 4.0), "thunk"),
    "brick": (8, [(170, 90, 70), (200, 120, 95), (150, 140, 130)], (60, 200), (0.25, 0.5), (1.5, 3.5), "chip"),
    "concrete": (7, [(170, 165, 155), (200, 195, 185), (140, 135, 130)], (60, 200), (0.2, 0.45), (1.5, 3.5), "chip"),
    "stone": (7, [(150, 150, 140), (120, 120, 112), (190, 185, 170)], (60, 210), (0.2, 0.45), (1.5, 3.5), "chip"),
    "water": (10, [(120, 180, 240), (200, 230, 255), (80, 140, 210)], (120, 300), (0.3, 0.6), (1.5, 3.0), "splash"),
    "sand": (8, [(225, 200, 150), (200, 175, 125), (240, 220, 180)], (40, 140), (0.35, 0.7), (2.0, 4.0), "puff"),
    "dirt": (8, [(130, 95, 65), (100, 75, 50), (160, 120, 80)], (40, 150), (0.35, 0.7), (2.0, 4.0), "puff"),
    "grass": (8, [(95, 160, 80), (70, 130, 60), (130, 95, 65)], (40, 150), (0.3, 0.6), (1.5, 3.5), "puff"),
    "snow": (10, [(240, 245, 255), (220, 230, 245), (255, 255, 255)], (40, 160), (0.4, 0.8), (2.0, 4.5), "puff"),
    "foliage": (8, [(60, 140, 70), (90, 170, 80), (40, 110, 60)], (40, 140), (0.4, 0.8), (2.0, 4.0), "thunk"),
}


# 세트 마지막 보스 5명의 싸움 방식: (방식, 약점 안내)
BOSS_STYLES = {1: ("barrage", "WEAK POINT: HEAD  -  DODGE THE GRENADE FANS"),
               2: ("armored", "FRONT ARMOR  -  HIT HIM FROM THE SIDE OR BEHIND"),
               3: ("sniper", "RED LASER = SHOT INCOMING  -  BREAK LINE OF SIGHT"),
               4: ("storm", "RED CIRCLES = AIRSTRIKE  -  KEEP MOVING"),
               5: ("warlord", "ALL OF THE ABOVE  -  ARMOR IN FRONT")}
BOSS_ARMOR = 0.35                 # 앞에서 쏘면 받는 피해 비율 (armored)
BOSS_SNIPE = (32, 1.3)            # 저격 보스: (피해, 레이저 조준 시간)
BOSS_STRIKE = (2.2, 40, 2.0)      # 공습 표시: (반경, 피해, 터지기까지 초)


# ----- 캠페인 특별 장면 -----
# 세트마다 7번째·14번째 라운드: 탈출(시간 안에 착륙장으로) / 소등(어둠 속 들키지 않기) / 호송(트럭 지키기)
SETPIECE_PLAN = {1: ("extraction", "lights"), 2: ("convoy", "extraction"), 3: ("lights", "convoy"),
                 4: ("extraction", "convoy"), 5: ("lights", "extraction")}
SETPIECE_INFO = {"extraction": ("EXTRACTION", "REACH THE LZ BEFORE THE HELI LEAVES", (255, 220, 90)),
                 "lights": ("LIGHTS OUT", "STAY UNSEEN FOR A GHOST BONUS  -  L = FLASHLIGHT", (150, 170, 255)),
                 "convoy": ("CONVOY", "ESCORT THE TRUCK  -  CLEAR THE ROAD AHEAD", (255, 160, 60))}
EXTRACT_TIME = 45.0               # 탈출: 착륙장까지 시간(초)
CONVOY_HP, CONVOY_SPEED = 300, 0.9   # 호송 트럭 체력, 빠르기(칸/초)
GHOST_BONUS = 500


def setpiece_for(round_no):
    """그 라운드의 특별 장면 이름 (없으면 None)"""
    in_set = (round_no - 1) % SET_SIZE
    plan = SETPIECE_PLAN.get(set_of(round_no))
    if not plan or in_set not in (6, 13):
        return None
    return plan[0 if in_set == 6 else 1]


def grid_path(start, goal):
    """칸 단위 최단 길 (너비 우선 탐색). 못 가면 []"""
    prev = {start: None}
    queue = deque([start])
    while queue:
        cell = queue.popleft()
        if cell == goal:
            break
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nxt = (cell[0] + dc, cell[1] + dr)
            if nxt not in prev and in_map(*nxt) and not is_blocked(nxt[0] + 0.5, nxt[1] + 0.5):
                prev[nxt] = cell
                queue.append(nxt)
    if goal not in prev:
        return []
    path, cell = [], goal
    while cell is not None:
        path.append(cell)
        cell = prev[cell]
    return path[::-1]


# ----- 라운드 미니 계약 -----
# 라운드마다 선택 목표 2개. 깨면 보너스 경험치 (+ 누적 기록, 10개면 업적 CONTRACTOR)
CONTRACTS = {  # 키: (이름, 한국어, 영어, 목표 수, 좀비 모드에서도?)
    "clean": ("CLEAN SWEEP", "한 번도 안 맞고 클리어", "Clear without taking damage", 1, False),
    "blade": ("BLADE WORK", "칼로 2명", "2 knife kills", 2, True),
    "heads": ("HEADHUNTER", "헤드샷으로 4명", "4 headshot kills", 4, True),
    "boom": ("DEMOLITION", "폭발로 2명", "2 explosive kills", 2, True),
    "close": ("CLOSE QUARTERS", "4m 안에서 3명", "3 kills within 4m", 3, True),
    "long": ("LONG SHOT", "20m 넘게 떨어진 적 1명", "1 kill from 20m+", 1, False),
    "fast": ("BLITZ", "60초 안에 클리어", "Clear within 60s", 1, False),
    "ghost": ("GHOST", "몰래 처치 2명", "2 takedowns", 2, False),
}
CONTRACT_XP = 300


# ----- DEEP RUN (로그라이트) -----
# 라운드를 깰 때마다 강화(boon) 3개 중 1개를 골라요. 죽으면 처음부터 (강화도 없어져요).
# 대신 내려간 깊이를 모두 더한 "총 깊이"가 쌓이면 새 강화가 풀려요 (save["deeprun"]).
BOONS = [  # (키, 이름, 한국어 설명, 영어 설명, 풀리는 총 깊이)
    ("vampire", "VAMPIRE", "처치할 때마다 체력 +8", "+8 HP per kill", 0),
    ("glass", "GLASS CANNON", "주는 피해 +35%, 최대 체력 -25", "+35% damage, -25 max HP", 0),
    ("thick", "THICK SKIN", "최대 체력 +30", "+30 max HP", 0),
    ("feet", "QUICK FEET", "이동 속도 +15%", "+15% move speed", 0),
    ("steady", "STEADY AIM", "탄 퍼짐 -30%", "-30% bullet spread", 0),
    ("adrenaline", "ADRENALINE", "처치하면 탄창에 3발", "Kills put 3 rounds in the mag", 0),
    ("boom", "EXPLOSIVE HEADSHOTS", "헤드샷으로 쓰러뜨리면 그 자리가 폭발", "Headshot kills explode", 8),
    ("shield", "RELOAD SHIELD", "재장전 중 받는 피해 -40%", "-40% damage taken while reloading", 15),
    ("wind", "SECOND WIND", "라운드마다 한 번, 쓰러질 피해를 체력 30으로 버텨요", "Once per round, survive a lethal hit", 25),
    ("scav", "SCAVENGER", "상자가 두 배로 떨어져요", "Double drop chance", 35),
    ("nades", "DEMOLITIONIST", "라운드마다 수류탄 +2", "+2 grenades each round", 50),
]
BOON_BY_KEY = {b[0]: b for b in BOONS}
DEEP_STEP = 2                     # 깊이 1 내려갈 때마다 캠페인 라운드 2개만큼 강해져요


def unlocked_boons(save):
    total = save.get("deeprun", {}).get("total", 0)
    return [b for b in BOONS if b[4] <= total]


class Director:
    """AI 디렉터: 싸움의 긴장감을 재서 '몰아치기 → 클라이맥스 → 숨 돌리기' 흐름을 만들어요.
    - intensity(0~1): 내가 맞거나 가까이서 싸우면 오르고, 조용하면 내려가요
    - phase: "build"(조금씩 세짐) → "peak"(가장 거셈, 몇 초) → "relax"(잠깐 쉬어요, 보급 상자)
    - assist: 같은 라운드에서 여러 번 죽으면 적 피해를 조금 줄여줘요 (최대 25%)"""

    def __init__(self):
        self.intensity = 0.0
        self.phase = "build"
        self.timer = 0.0           # 지금 단계에서 지난 시간
        self.supplied = False      # 이번 숨 돌리기에서 보급을 줬는지
        self.assist = 0.0
        self.deaths_here = 0

    def on_damage(self, damage):
        self.intensity = min(1.0, self.intensity + damage / 90)

    def on_kill(self, distance):
        self.intensity = min(1.0, self.intensity + (0.09 if distance < 5 else 0.04))

    def on_death(self):
        self.deaths_here += 1
        self.assist = min(DIRECTOR_MAX_ASSIST, 0.08 * self.deaths_here)

    def new_round(self):
        """라운드가 바뀌면(다시 하기 포함) 긴장감은 처음부터"""
        self.intensity, self.phase, self.timer, self.supplied = 0.0, "build", 0.0, False

    def on_clear(self):
        """라운드를 깨면 도움은 천천히 줄여요"""
        self.deaths_here = 0
        self.assist = max(0.0, self.assist - 0.08)

    def update(self, dt, in_combat):
        self.timer += dt
        decay = 0.05 if in_combat else 0.12
        if self.phase == "relax":
            decay *= 1.8
        self.intensity = max(0.0, self.intensity - decay * dt)
        if self.phase == "build" and self.intensity >= DIRECTOR_PEAK:
            self.phase, self.timer = "peak", 0.0
        elif self.phase == "peak" and self.timer > DIRECTOR_PEAK_TIME:
            self.phase, self.timer, self.supplied = "relax", 0.0, False
        elif self.phase == "relax" and self.timer > DIRECTOR_RELAX_TIME and self.intensity < 0.4:
            self.phase, self.timer = "build", 0.0

    @property
    def spawn_mult(self):
        """좀비가 나오는 빠르기 배율"""
        return {"build": 1.0, "peak": 1.45, "relax": 0.15}[self.phase]


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
        elif kind == "flash":
            self.timer = 1.4
        elif kind == "smoke":
            self.timer = 1.0
        elif kind == "tknife":
            self.timer = 2.0
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
            if self.kind in ("grenade", "flash", "smoke"):
                self.bounce_step(sdt)
            elif self.kind == "tknife":
                if self.knife_step(sdt, enemies):
                    return True
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

    def knife_step(self, sdt, enemies):
        """투척 칼: 살짝 떨어지며 날아가요. 적이나 벽에 닿으면 True"""
        self.vz -= GRAVITY * 0.25 * sdt
        self.pos += self.vel * sdt
        self.z += self.vz * sdt
        if self.z <= 0 or obstacle_height(self.pos.x, self.pos.y) > self.z:
            self.pos -= self.vel.normalize() * 0.2
            self.vel = pygame.Vector2()
            return True
        for e in enemies:
            if e.pos.distance_to(self.pos) < 0.35 and self.z <= e.t["height"] + e.t.get("lift", 0):
                self.hit = e
                return True
        return False

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


# AI 동료: 나를 따라다니며 보이는 적을 쏴요. K 로 명령 (따라와 → 대기 → 공격)
ALLY_NAMES = ("ALPHA", "BRAVO")
ALLY_HP = 150
ALLY_LOOK = dict(uniform=(95, 110, 80), vest=(55, 95, 160), pants=(70, 75, 60), head="helmet", gun=32)
SQUAD_ORDERS = ("FOLLOW", "HOLD", "ATTACK")


class Ally:
    def __init__(self, x, y, name):
        self.pos = pygame.Vector2(x, y)
        self.name = name
        self.hp = ALLY_HP
        self.down = False
        self.facing = pygame.Vector2(1, 0)
        self.walk = 0.0
        self.moving = 0.0
        self.shoot_timer = random.uniform(0.3, 0.8)
        self.target = None
        self.look_timer = 0.0     # 적 찾기는 0.25초마다
        self.nav_timer, self.nav_goal, self.nav_target = 0.0, None, None   # 길찾기 (steer)
        self.flash = 0.0
        self.callout = None


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
    def __init__(self, save, start_round=1, mode="campaign", loadout=None, mission=0, stage=0, challenge=None,
                 custom=None, deeprun=False):
        """save: 저장 정보(dict). 라운드를 깨거나 죽을 때마다 고쳐서 파일에 써요.
        mode: "campaign"(라운드마다 맵이 바뀌는 전투) 또는 "zombies"(좀비 웨이브 버티기)
        loadout: 고른 주무기/보조무기/퍼크 (없으면 모든 무기를 들고 시작)"""
        self.mode = mode
        self.custom = custom        # 내가 만든 맵: dict(name, rows)
        self.practice = mode in ("training", "custom")   # 연습: 경험치·무기 성장·업적·기록이 안 바뀌어요
        self.challenge = challenge  # 도전 모드 이름 (없으면 None)
        self.allies = []           # AI 동료 (설정 SQUADMATES)
        self.squad_order = 0       # SQUAD_ORDERS 중 몇 번째
        self.flashlight = False    # 손전등 (L)
        self.chopper = None        # 지원 헬기 (킬스트릭)
        self.clip_frames = []      # 최근 장면들 (하이라이트용)
        self.clip_timer = 0.0
        self.highlight = None      # 이번 라운드 최고의 순간: dict(label, score, frames)
        self.frame_dt = 1 / 60
        self.recording = None      # 하이라이트를 찍는 중 (순간 뒤 조금 더)
        self.mounted = None        # 지금 타고 있는 고정 기관총
        self.mg_heat = 0.0
        self.turrets = []
        self.tactical = (loadout or {}).get("tactical", "FLASHBANG")
        self.tactical_left = 0
        self.cooking = None        # 수류탄을 쥐고 있는 시간 (G 를 꾹 누르면 쿠킹, 떼면 던져요)
        self.flashed = 0.0         # 내가 섬광탄에 눈부신 남은 시간
        self.body_timer = 0.0      # 시체 발견 검사 간격
        self.hold_pos = None
        self.world_tracers = []    # 동료와 적이 서로 쏜 총알 궤적: [시작 위치, 끝 위치, 남은 시간]
        self.briefing = None       # 세트 브리핑 화면을 보여준 시간 (None이면 안 보여줌)
        self.briefed = set()       # 이번에 이미 본 세트 브리핑
        self.radio_msg = None      # 본부 무전 [글자, 지난 시간]
        self.challenge_time = 0.0
        self.challenge_done = False
        self.game_shots = self.game_hits = 0   # 이번 판 전체 (기록 화면용)
        self.started = time.time()
        self.loadout = loadout
        self.mission = mission     # 미션 모드: 몇 번째 미션인지
        self.stage = stage         # 미션 모드: 지금 단계 (0부터)
        self.mission_time = 0.0
        self.mission_complete = False
        self.perk = loadout["perk"] if loadout else None
        ranks = save.get("skills", {})
        self.base_max_hp = (130 if self.perk == "IRON SKIN" else 100) + 15 * ranks.get("VITALITY", 0)
        self.max_hp = self.base_max_hp
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
        self.knife_image = pygame.Surface((30, 8), pygame.SRCALPHA)        # 투척 칼
        pygame.draw.polygon(self.knife_image, (210, 215, 225), [(8, 1), (30, 4), (8, 7)])
        pygame.draw.rect(self.knife_image, (40, 40, 40), (0, 2, 9, 4))
        self.smoke_images = []                                              # 연기 (진하기 4단계)
        for alpha in (60, 110, 160, 205):
            puff = pygame.Surface((64, 64), pygame.SRCALPHA)
            for r, a in ((31, alpha // 2), (24, alpha * 3 // 4), (16, alpha)):
                pygame.draw.circle(puff, (190, 192, 195, a), (32, 32), r)
            self.smoke_images.append(puff)
        rng = random.Random(3)            # 눈송이: (x, y, 떨어지는 속도)
        self.snowflakes = [(rng.random(), rng.random(), rng.uniform(0.08, 0.2)) for _ in range(160)]
        self.car_images = [make_car_image(color) for color in CAR_COLORS]
        self.grenade_image = make_grenade_image()
        self.rocket_image = make_rocket_image()
        self.explosion_frames = make_explosion_frames()
        self.flare_frames = make_flare_frames()
        self.sentry_images = (make_sentry_image(), make_sentry_image(flash=True))
        self.chopper_images = (make_chopper_image(), make_chopper_image(flash=True))
        self.mg_image = make_mg_image()
        self.blood_pool = make_blood_pool_image()
        self.hurt_vignette = make_hurt_vignette()
        self.splat_images = [make_screen_splat(i) for i in range(4)]
        self.glow_image = make_glow(128, (255, 200, 120))      # 가로등 불빛
        self.shadow_cache, self.flash_glow_cache = {}, {}
        self.device_images = {"barrel": make_barrel_image(), "alarm": make_alarm_image(False),
                              "alarm_on": make_alarm_image(True)}
        self.devices = []
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
        self.fonts = make_fonts(korean_ui=False)     # 게임 화면은 원래 글꼴 (도움말만 한글)
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
        self.wheel = None          # 무기 휠: dict(t=누른 시간, pick=고른 칸, open=열렸는지)
        self.director = Director() # 긴장감 조절 (몰아치기 / 숨 돌리기)
        self.deeprun = deeprun      # DEEP RUN (로그라이트) 인지
        self.boons = {}             # 고른 강화: {키: 개수}
        self.boon_choice = None     # 고르는 중인 강화 3개 (키 목록)
        self.boon_sel = 0
        self.depth = 1
        self.wind_used = False
        self.deeprun_saved = False
        self.boon_blasts = []       # 헤드샷 폭발 (다음 장면에 터져요)
        self.boss_marks = []        # 공습 표시: [위치, 남은 시간]
        self.boss_laser = None      # 저격 보스 레이저: [보스, 남은 시간]
        self.boss_tip = ""
        self.impact_sound_cd = 0.0  # 맞은 곳 소리 간격
        self.vault = None           # 뛰어넘는 중: dict(start, end, t)
        self.lean = 0.0             # 몸 기울이기 (-1 왼쪽 ~ 1 오른쪽)
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
        self.bottom_shade = make_bottom_shade()
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
        global NAVIGATOR
        NAVIGATOR = self.navigator = Navigator()
        self.decals = {}           # 벽 자국: (칸 x, 칸 y, 세로벽인지) -> [(위치, 높이, "hole"/"scorch"), ...]
        self.decal_count = 0
        self.broken_windows = set()
        self.cover_hp = {}         # 부서지는 엄폐물 남은 체력
        self.buyables = self.find_buyables()
        self.turrets = self.find_turrets()
        self.trap_timer = 0.0
        self.doors = {cell: 0.0 for cell in ((x, y) for y, row in enumerate(GAME_MAP) for x, ch in enumerate(row)
                                              if ch in DOORS)}   # 문 칸 -> 닫히기까지 남은 시간 (0이면 닫힘)
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
        # 동료 그림: 파란 조끼 (앞, 뒤, 걷기, 쏘기, 쓰러짐)
        normal = make_enemy_image(ALLY_LOOK)
        back = make_back_image(ALLY_LOOK)
        self.ally_images = {"normal": normal, "flash": make_enemy_image(ALLY_LOOK, "flash"), "back": back,
                            "down": pygame.transform.rotate(make_enemy_image(ALLY_LOOK, "hurt"), 90)}
        for side in (0, 1):
            self.ally_images[f"walk{side}"] = walk_frame(normal, side)
            self.ally_images[f"back_walk{side}"] = walk_frame(back, side)
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
        self.door_spec = (shade(WALLS["d"][0], dark), *WALLS["d"][1:])   # 닫힌 문 모양 (밤이면 어둡게)
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
        if getattr(self, "deeprun", False):
            self.boons, self.boon_choice, self.depth, self.deeprun_saved = {}, None, 1, False
            self.max_hp = self.base_max_hp
        self.round = start_round
        self.fail_reason = ""
        self.killcam_from = None
        self.kills = 0
        self.points = 0            # 좀비 모드 점수 (B 탄약, U 총 강화에 써요)
        self.game_over = False
        self.hint_timer = 8.0      # 처음 8초 동안 화면 아래에 조작법 안내
        self.reset_streak()
        self.start_run()
        self.start_round()

    def start_run(self):
        """랭킹용 한 판 시작: 점수(이번 판에 얻은 경험치)를 0부터 세요"""
        self.run_score = 0
        self.run_kills_start = self.kills
        self.run_recorded = False
        self.run_place = None      # 랭킹 몇 등에 들었는지 (못 들면 None)

    def finish_run(self):
        """한 판이 끝나면 (죽음, 미션 완료, 메뉴로 나가기) 랭킹에 기록해요. 한 판에 한 번만."""
        if self.run_recorded or self.practice or self.challenge or self.run_score <= 0:
            return
        mode = "deeprun" if self.deeprun else self.mode
        if mode not in [m for m, _, _ in RANK_MODES]:
            return
        self.run_recorded = True
        if self.deeprun:
            reached, where = self.depth, self.theme["name"]
        elif self.mode == "mission":
            reached, where = min(self.stage + 1, len(MISSION_STAGES)), MISSIONS[self.mission]["name"]
        else:
            reached, where = self.round, self.theme["name"]
        entry = dict(score=self.run_score, reached=reached, kills=self.kills - self.run_kills_start,
                     map=where, date=time.strftime("%Y-%m-%d %H:%M"))
        self.run_place = add_ranking(self.save, mode, entry)
        if self.run_place:
            self.popups.append([f"NEW RECORD!  RANK #{self.run_place}", (255, 200, 60), 3.0])
        write_save(self.save)

    def reset_streak(self):
        """킬스트릭(죽지 않고 연속 처치)은 죽으면 처음부터 다시 세요"""
        self.streak = 0
        self.streaks_ready = []    # 받은 킬스트릭 (X로 하나씩 써요)

    def retry_round(self):
        """죽은 라운드부터 다시 (처치 수는 그대로). 좀비 모드는 1웨이브부터. DEEP RUN 은 깊이 1부터"""
        self.fail_reason = ""
        self.killcam_from = None
        if self.deeprun:
            self.map_key = None
            self.map_index = None
            self.reset(1)
            return
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
        self.start_run()               # 죽은 판은 랭킹에 들어갔으니 새 판으로 세요
        self.start_round()

    def rank_of(self, skill):
        """스킬 단계 (안 배웠으면 0)"""
        return self.save.get("skills", {}).get(skill, 0)

    def weapon_spec(self, name):
        """그 무기의 지금 성능 (처치 수에 따른 레벨과 부착물 적용)"""
        kills = self.save.get("wkills", {}).get(name, 0)
        chosen = self.save.get("gunsmith", {}).get(name)
        if chosen:                                    # 총기 개조 화면에서 고른 부착물
            gold = [m for m in weapon_mods(kills) if m == "GOLD CAMO"]
            spec = apply_gunsmith(apply_mods(WEAPON_BY_NAME[name], gold, weapon_level(kills)), chosen)
        else:
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
        if not self.loadout or self.practice:
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
        self.devices = []                       # 장치는 캠페인 전투(start_battle)에서만 다시 놓여요
        piece = getattr(self, "setpiece", None)
        if piece and piece["kind"] == "lights":  # 소등 장면이 끝났으면 원래 밝기로
            self.night, self.dark_key = piece["night_before"], None
        self.setpiece = None
        if self.mode == "training":
            self.start_training()
        elif self.mode == "zombies":
            self.start_wave()
        elif self.mode == "mission":
            self.start_mission()
        elif self.challenge:
            self.start_challenge()
        elif self.mode == "custom":
            self.start_custom()
        else:
            self.start_battle()
        self.reset_round_state()
        if self.mode == "mission":
            self.banner_timer = 5.0
        if self.deeprun:
            self.wind_used = False
            self.arsenal.grenades += 2 * self.boons.get("nades", 0)
            self.player.hp = self.max_hp
            self.banner = f"DEPTH {self.depth}"
            names = ", ".join(f"{BOON_BY_KEY[k][1]}" + (f" x{n}" if n > 1 else "") for k, n in self.boons.items())
            self.sub_banners = [(f"DEEP RUN  -  {self.theme['name']}", WHITE)] + \
                ([(fit_text(self.font, names, WIDTH * 0.8), (80, 240, 255))] if names else [])

    def start_custom(self):
        """내가 만든 맵: 웨이브마다 적이 늘고 강해져요 (E 자리에서 나와요)"""
        global CUSTOM_INDEX
        theme = dict(MAPS[CAMPAIGN_MAPS[0]], name=self.custom["name"], rows=list(self.custom["rows"]),
                     op="CUSTOM MAP", brief="Your own map. Clear every wave.", custom=True)
        if CUSTOM_INDEX is None:
            MAPS.append(theme)
            CUSTOM_INDEX = len(MAPS) - 1
        else:
            MAPS[CUSTOM_INDEX] = theme
        if self.round == 1 or getattr(self, "map_key", None) is None or self.map_index != CUSTOM_INDEX:
            self.setup_map(CUSTOM_INDEX)
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.player.hp = self.max_hp
        self.arsenal = self.make_arsenal()
        spots = find_cells("E")
        count = min(len(spots), 2 + self.round)
        self.enemies = [Enemy(*q, self.pick_enemy_kind(), self.skill) for q in random.sample(spots, count)]
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items() for x, y in find_cells(letter)]
        self.zombies_left = 0
        self.objective = None
        self.banner = f"WAVE {self.round}"
        self.sub_banners = [(f"CUSTOM MAP  -  {self.custom['name']}", WHITE), ("PRACTICE: NO XP", (200, 200, 255))]

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

    def draw_darkness(self, screen):
        """밤: 화면 가장자리가 어두워요. 손전등을 켜면 가운데가 밝게 비춰져요"""
        key = (WIDTH, HEIGHT, self.night, self.flashlight)
        if getattr(self, "dark_key", None) != key:
            self.dark_key = key
            small = pygame.Surface((160, 90))
            add = pygame.Surface((160, 90))
            small.fill((255, 255, 255))
            add.fill((0, 0, 0))
            if self.night:
                edge = 55 if self.flashlight else 80
                for r in range(95, 0, -3):                 # 바깥에서 안쪽으로 점점 밝게
                    k = r / 95
                    v = int(255 - (255 - edge) * k ** 1.6)
                    pygame.draw.ellipse(small, (v, v, int(v * 1.02) if v < 250 else 255),
                                        (80 - r * 1.1, 45 - r * 0.62, r * 2.2, r * 1.24))
            if self.flashlight:
                for r in range(30, 0, -2):                 # 손전등 빛: 가운데가 밝고 따뜻하게
                    k = 1 - r / 30
                    pygame.draw.ellipse(add, (int(95 * k), int(88 * k), int(62 * k)), (80 - r * 1.3, 48 - r, r * 2.6, r * 2))
            self.dark_mult = pygame.transform.smoothscale(small, (WIDTH, HEIGHT)) if self.night else None
            self.dark_add = pygame.transform.smoothscale(add, (WIDTH, HEIGHT)) if self.flashlight else None
        if self.dark_add is not None:
            screen.blit(self.dark_add, (0, 0), special_flags=pygame.BLEND_ADD)
        if self.dark_mult is not None:
            screen.blit(self.dark_mult, (0, 0), special_flags=pygame.BLEND_MULT)

    def draw_highlight(self, screen):
        """라운드가 끝나면 오른쪽에 최고의 순간을 다시 보여줘요 (반복)"""
        frames = self.highlight["frames"]
        if not frames:
            return
        shown = self.round_clear_timer
        k = int((10.0 - shown) * CLIP_FPS * 0.8) % len(frames)           # 조금 느리게
        w, h = int(WIDTH * 0.26), int(WIDTH * 0.26 * 9 / 16)
        frame = pygame.transform.scale(frames[k], (w, h))
        rect = frame.get_rect(topright=(WIDTH - 16 * UI, HEIGHT * 0.31))
        pygame.draw.rect(screen, (255, 80, 200), rect.inflate(6, 6), 3)
        screen.blit(frame, rect)
        label = self.small_font.render(f"HIGHLIGHT: {self.highlight['label']}", True, (255, 220, 90))
        screen.blit(label, label.get_rect(bottomleft=(rect.x, rect.y - 6)))
        if k % 10 < 6:                                                  # 깜빡이는 다시보기 표시
            pygame.draw.circle(screen, RED, (rect.right - 14 * UI, rect.y + 14 * UI), 6 * UI)

    def draw_popups(self, screen, font):
        """알림 글자 두 종류:
        - 중요한 알림(새 무기, 계급, 업적...)은 왼쪽 가운데에 카드로 쌓여요 (옆에서 미끄러져 들어와요)
        - 전투 글자(헤드샷 +150, 수류탄...)는 조준점 아래에서 살짝 떠오르며 사라져요"""
        toasts = [p for p in self.popups if p[0].startswith(TOAST_WORDS)]
        quick = [p for p in self.popups if not p[0].startswith(TOAST_WORDS)]
        y = max(HEIGHT * 0.34, 12 + 232 * UI)              # HQ 무전 상자 아래부터
        limit = HEIGHT * 0.58 - 6 if getattr(self, "contracts", None) else HEIGHT * 0.75   # 계약 목록 위까지
        for p in reversed(toasts[-4:]):                     # 새 알림부터 위에
            text, color, left = p[0], p[1], p[2]
            age = (p[3] if len(p) > 3 else left) - left
            image = self.small_font.render(text, True, WHITE)
            box = pygame.Rect(0, y, image.get_width() + 34 * UI, image.get_height() + 14 * UI)
            if box.bottom > limit:
                break                                       # 자리가 없으면 오래된 알림은 생략
            slide = 1 - min(1.0, age / 0.18)
            box.x = 16 - slide * (box.w + 20)
            alpha = min(1.0, left / 0.4)
            panel = pygame.Surface(box.size, pygame.SRCALPHA)
            panel.fill((10, 8, 24, int(200 * alpha)))
            screen.blit(panel, box)
            pygame.draw.rect(screen, color, (box.x, box.y, 5 * UI, box.h))                # 색 띠
            image = image.copy()
            image.set_alpha(int(255 * alpha))
            screen.blit(image, image.get_rect(midleft=(box.x + 18 * UI, box.centery)))
            y += box.h + 6 * UI
        for i, p in enumerate(quick[-3:]):
            text, color, left = p[0], p[1], p[2]
            age = (p[3] if len(p) > 3 else left) - left
            rise = min(1.0, age / 0.35) * 10 * UI
            image = font.render(text, True, color).copy()
            pop = 1 + 0.3 * max(0.0, 1 - age / 0.12)                     # 처음에 톡 커졌다가
            if pop > 1.001:
                image = pygame.transform.smoothscale(image, (int(image.get_width() * pop), int(image.get_height() * pop)))
            image.set_alpha(int(255 * min(1.0, left / 0.35)))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.6 + i * 30 * UI - rise)))

    def draw_banner(self, screen, big_font, font):
        """라운드 시작/클리어 알림: 가로 띠가 펼쳐지고, 제목 → 설명 줄 → 임무 글이 차례로 나와요"""
        length = getattr(self, "banner_len", self.banner_timer) or 1.0
        age = max(0.0, length - self.banner_timer)
        fade = min(1.0, self.banner_timer / 0.5, age / 0.2)                 # 처음과 끝에 부드럽게
        lines = list(self.sub_banners)
        brief = ""
        if self.round_clear_timer <= 0 and self.theme.get("brief"):
            brief = self.theme["brief"][:int(self.brief_age * 40)]
        brief_lines = wrap_text(self.small_font, brief, WIDTH * 0.7) if brief else []
        title_h, line_h, brief_h = 56 * UI, 30 * UI, 22 * UI
        band_h = title_h + len(lines) * line_h + len(brief_lines) * brief_h + 26 * UI
        top = max(HEIGHT * 0.24, 12 + 228 * UI)                        # HQ 무전 상자 아래
        grow = min(1.0, age / 0.25)                                        # 띠가 가운데서 양옆으로
        band = pygame.Rect(0, top, WIDTH * grow, band_h)
        band.centerx = WIDTH / 2
        shade_img = pygame.Surface(band.size, pygame.SRCALPHA)
        shade_img.fill((8, 6, 20, int(150 * fade)))
        screen.blit(shade_img, band)
        for y in (band.top, band.bottom - 2):
            pygame.draw.line(screen, UI_ACCENT if y == band.top else UI_CYAN, (band.left, y), (band.right, y), 2)
        title = big_font.render(self.banner, True, YELLOW).copy()
        pop = 1 + 0.25 * max(0.0, 1 - age / 0.25)                          # 처음엔 살짝 크게 나타나요
        if pop > 1.001:
            title = pygame.transform.smoothscale(title, (int(title.get_width() * pop), int(title.get_height() * pop)))
        title.set_alpha(int(255 * fade))
        screen.blit(title, title.get_rect(center=(WIDTH / 2, top + title_h / 2 + 8 * UI)))
        y = top + title_h + 8 * UI
        for i, (text, color) in enumerate(lines):
            show = min(1.0, (age - 0.25 - 0.18 * i) / 0.25) * fade             # 한 줄씩 차례로
            if show > 0:
                image = font.render(text, True, color).copy()
                image.set_alpha(int(255 * show))
                screen.blit(image, image.get_rect(center=(WIDTH / 2, y + line_h / 2)))
            y += line_h
        for line in brief_lines:
            image = self.small_font.render(line, True, (200, 230, 255)).copy()
            image.set_alpha(int(255 * fade))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, y + brief_h / 2)))
            y += brief_h

    def draw_radio(self, screen):
        """본부 무전: 왼쪽 위 정보 아래에 'HQ' 상자와 한 글자씩 나오는 말 (길면 두 줄)"""
        text, age = self.radio_msg
        if text.startswith("HQ:"):                                 # 'HQ' 는 상자 이름표로 보여줘요
            text = text[3:].strip()
        typed = text[:int(age * 45)]
        font = self.fonts["help"]
        width = WIDTH * 0.42
        lines = wrap_text(font, text, width)
        shown, left = [], len(typed)
        for line in lines:                                        # 친 글자만큼만 줄마다 나눠서
            shown.append(line[:max(0, left)])
            left -= len(line) + 1
        line_h = font.get_linesize()
        box = pygame.Rect(16, 12 + 152 * UI, max(font.size(line)[0] for line in lines) + 70 * UI,
                          line_h * len(lines) + 14 * UI)
        alpha = min(1.0, (5.0 - age) * 2, age * 6)
        panel = pygame.Surface(box.size, pygame.SRCALPHA)
        panel.fill((0, 30, 10, int(170 * alpha)))
        screen.blit(panel, box)
        pygame.draw.rect(screen, (80, 200, 120), box, 1, border_radius=int(6 * UI))
        pygame.draw.rect(screen, (80, 255, 120), (box.x, box.y, 4 * UI, box.h))        # 왼쪽 초록 띠
        tag = self.small_font.render("HQ", True, (80, 255, 120))
        screen.blit(tag, (box.x + 10 * UI, box.y + 8 * UI))
        if int(age * 6) % 2 == 0 and age < 1.5:                  # 무전 신호 깜빡임
            pygame.draw.circle(screen, (80, 255, 120), (box.x + 46 * UI, box.y + 16 * UI), 4 * UI)
        for i, line in enumerate(shown):
            label = font.render(line, True, (200, 255, 200))
            screen.blit(label, (box.x + 58 * UI, box.y + 7 * UI + i * line_h))

    def draw_briefing(self, screen):
        """세트 브리핑: 작전 이름과 이야기를 한 줄씩 보여줘요"""
        set_no = set_of(self.round)
        story = STORY[set_no - 1]
        ko = self.fonts["lang"] == "ko"
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((5, 8, 15, 248))
        screen.blit(dim, (0, 0))
        self.center_text(screen, self.small_font, f"SET {set_no} / {len(SETS)}:  {SETS[set_no - 1]}", (80, 240, 255), HEIGHT * 0.22)
        self.center_text(screen, self.big_font, story["op"], YELLOW, HEIGHT * 0.3)
        font = self.fonts["help_big" if "help_big" in self.fonts else "help"]
        shown = self.briefing * 40                            # 한 글자씩
        for i, line in enumerate(story["ko" if ko else "en"]):
            part = line[:max(0, int(shown))]
            shown -= len(line) + 8
            if part:
                image = font.render(part, True, WHITE)
                screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * (0.44 + i * 0.08))))
        if self.briefing > 0.8 and int(self.briefing * 2) % 2 == 0:
            hint = "스페이스 / F : 작전 시작" if ko else "SPACE / F : START"
            image = self.fonts["help"].render(hint, True, YELLOW)
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.8)))

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
            self.finish_run()
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
        self.spawn_allies()
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
        self.titan_due = self.round % 10 == 0      # 10웨이브마다 보스 좀비 타이탄
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items()
                        for x, y in find_cells(letter)]
        self.banner = f"WAVE {self.round}"
        self.sub_banners = [(f"{self.zombies_left} ZOMBIES", RED)]
        if self.titan_due:
            self.sub_banners.append(("BOSS WAVE: TITAN!", RED))
        elif self.brute_due:
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
        story = STORY[set_no - 1]
        finale = in_set == SET_SIZE - 1
        if special == "BOSS":
            boss = self.enemies[0]
            boss.name = story["boss"] if finale else story["mid"]
            if finale:                                  # 세트 마지막: 더 단단한 보스 + 호위 2명
                boss.t = dict(boss.t, hp=int(boss.t["hp"] * 1.4))
                boss.hp = boss.t["hp"]
                boss.style, tip = BOSS_STYLES[min(set_no, len(BOSS_STYLES))]
                boss.pattern_timer = 4.0                # 첫 패턴까지 숨 돌릴 시간
                boss.pattern_step = 0
                self.boss_tip = tip
                extra = [p for p in far if boss.pos.distance_to(p) > 2][:2]
                self.enemies += [Enemy(*p, "GRUNT", self.skill) for p in extra]
            self.sub_banners.append((f"{'SET FINALE' if finale else 'BOSS ROUND'}: {boss.name}", RED))
            if finale:
                self.sub_banners.append((self.boss_tip, (255, 200, 60)))
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
        if not self.challenge:
            if in_set == 0 and set_no not in self.briefed and self.round <= CAMPAIGN_ROUNDS and not self.deeprun:
                self.briefing = 0.0                     # 새 세트: 작전 브리핑부터
                self.briefed.add(set_no)
            self.pending_radio = "boss" if special == "BOSS" else "start"
        self.place_devices(set_no, special == "BOSS")
        kind = setpiece_for(self.round) if not self.challenge and special != "BOSS" else None
        if kind:
            self.start_setpiece(kind)

    def radio(self, key, force=False):
        """본부 무전: 화면 왼쪽에 글자 + 무전 소리 (캠페인에서만)"""
        if self.mode != "campaign" or self.challenge:
            return
        if self.radio_msg and self.radio_msg[1] < 2.5 and not force:
            return
        lines = RADIO[key][0 if self.fonts["lang"] == "ko" else 1]
        self.radio_msg = [random.choice(lines), 0.0]
        self.sounds.play("radio", 0.9)

    def spawn_allies(self):
        """동료를 내 뒤에 세워요 (쓰러졌던 동료도 다시 일어나요)"""
        count = SETTINGS.get("squad", 2) if self.mode in ("campaign", "mission", "zombies", "custom") and not self.challenge else 0
        p = self.player
        back = -p.forward
        side = pygame.Vector2(-back.y, back.x)
        self.allies = []
        for k in range(count):
            spot = p.pos + back * 1.2 + side * (0.9 if k == 0 else -0.9)
            if is_blocked(spot.x, spot.y) or not can_see(p.pos, spot):
                spot = pygame.Vector2(p.pos)
            self.allies.append(Ally(spot.x, spot.y, ALLY_NAMES[k]))
        self.squad_order, self.hold_pos = 0, None

    def reset_round_state(self):
        """라운드(웨이브)마다 새로 시작하는 것들"""
        self.contracts = self.roll_contracts()
        self.round_time = 0.0
        self.boss_marks, self.boss_laser, self.armor_hint = [], None, False
        self.director.new_round()
        self.low_warned = False        # 체력 낮음 무전을 이번 라운드에 했는지
        self.tactical_left = TACTICAL_COUNT + (1 if self.perk == "SCAVENGER" else 0)
        self.mounted, self.mg_heat = None, 0.0
        self.highlight, self.recording, self.clip_frames = None, None, []
        self.cooking = None
        SMOKES.clear()
        self.spawn_allies()
        self.world_tracers = []
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
        self.strafe_tilt = 0.0     # 옆으로 걸으면 총이 살짝 기울어요
        self.land_dip = 0.0        # 착지하면 총이 쿵 내려갔다 올라와요
        self.was_air = False
        self.dry_cd = 0.0
        self.tilt_cache = {}
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

    def check_bodies(self):
        """눈치 못 챈 적이 쓰러진 동료를 보면: "MAN DOWN!" 외치고 그쪽을 수색해요 (근처 동료도)"""
        for corpse in self.corpses:
            if getattr(corpse, "found", False):
                continue
            for enemy in self.enemies:
                if enemy.sees or "melee" in enemy.t or enemy.kind == "TARGET":
                    continue
                offset = corpse.pos - enemy.pos
                d = offset.length()
                if d < 9 and (d < 2 or offset.normalize().dot(enemy.facing) > VIEW_COS) and can_see(enemy.pos, corpse.pos):
                    corpse.found = True
                    self.callout_cooldown = 0.0
                    self.shout(enemy, "MAN DOWN!")
                    for other in self.enemies:
                        if other.pos.distance_to(enemy.pos) < 10 and not other.sees and "melee" not in other.t:
                            other.search = pygame.Vector2(corpse.pos)
                            other.aware = max(other.aware, 0.5)
                            other.combat_timer = 6.0
                    break

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

    def start_setpiece(self, kind):
        """특별 장면 준비 (목표, 어둠, 트럭)"""
        title, tip, color = SETPIECE_INFO[kind]
        self.objective = None
        if kind == "extraction":
            self.objective = dict(kind="REACH", pos=self.far_spot(), progress=0.0, done=False,
                                  timer=BOMB_TIME, spawn=7.0, beep=0.0)
            self.setpiece = dict(kind=kind, timer=EXTRACT_TIME)
        elif kind == "lights":
            self.setpiece = dict(kind=kind, spotted=False, night_before=self.night)
            self.night, self.dark_key = True, None
        else:
            start = (int(self.player.pos.x), int(self.player.pos.y))
            goal = self.far_spot()
            path = grid_path(start, (int(goal.x), int(goal.y)))
            if len(path) < 4:
                self.setpiece = None
                return
            truck = dict(pos=pygame.Vector2(path[1][0] + 0.5, path[1][1] + 0.5), path=path, step=1, hp=CONVOY_HP)
            self.setpiece = dict(kind=kind, truck=truck, spawn=10.0)
        self.sub_banners.insert(1, (f"SET PIECE: {title}  -  {tip}", color))

    def fail_setpiece(self, reason):
        if not self.game_over:
            self.fail_reason = reason
            self.player.hp = 0                      # 다음 장면에 게임 오버 (다시 하기 R)

    def update_setpiece(self, dt):
        piece = self.setpiece
        if not piece or self.game_over or self.round_clear_timer > 0:
            return
        if piece["kind"] == "extraction":
            if self.banner_timer <= 0:
                piece["timer"] -= dt
            if piece["timer"] <= 0 and not (self.objective and self.objective["done"]):
                self.fail_setpiece("TOO LATE - THE HELI LEFT")
        elif piece["kind"] == "lights":
            if not piece["spotted"] and any(e.sees for e in self.enemies):
                piece["spotted"] = True
                self.popups.append(["SPOTTED! NO GHOST BONUS", RED, 1.8])
        else:
            self.update_convoy(piece, dt)

    def update_convoy(self, piece, dt):
        """호송: 앞길에 적이 없으면 트럭이 길을 따라 가요. 가까이서 트럭을 보는 적은 트럭을 쏴요"""
        truck = piece["truck"]
        blocked = any(e.pos.distance_to(truck["pos"]) < 4.5 for e in self.enemies if "melee" not in e.t)
        if not blocked and truck["step"] < len(truck["path"]) - 1:
            nxt = pygame.Vector2(truck["path"][truck["step"] + 1]) + pygame.Vector2(0.5, 0.5)
            offset = nxt - truck["pos"]
            move = CONVOY_SPEED * dt
            if offset.length() <= move:
                truck["pos"].update(nxt)
                truck["step"] += 1
            else:
                truck["pos"] += offset.normalize() * move
        for e in self.enemies:
            if e.pos.distance_to(truck["pos"]) < 7 and can_see(e.pos, truck["pos"]):
                truck["hp"] -= 3.5 * dt
        piece["spawn"] -= dt
        if piece["spawn"] <= 0 and len(self.enemies) < 8:
            piece["spawn"] = 11.0
            ahead = truck["path"][min(len(truck["path"]) - 1, truck["step"] + 6)]
            spots = [pt for pt in self.spawn_points if pygame.Vector2(pt).distance_to(pygame.Vector2(ahead)) < 9
                     and pygame.Vector2(pt).distance_to(self.player.pos) > 6]
            for x, y in random.sample(spots, min(2, len(spots))):
                self.enemies.append(Enemy(x, y, "GRUNT", self.skill))
        if truck["hp"] <= 0:
            self.fail_setpiece("CONVOY DESTROYED")
        elif truck["step"] >= len(truck["path"]) - 1:              # 도착: 라운드 클리어
            self.objective = dict(kind="REACH", pos=pygame.Vector2(truck["pos"]), progress=1.0, done=True,
                                  timer=0, spawn=0, beep=0)
            self.popups.append(["CONVOY ARRIVED", (80, 240, 255), 2.0])

    def setpiece_on_clear(self):
        piece = self.setpiece
        if piece and piece["kind"] == "lights" and not piece["spotted"]:
            self.add_xp(GHOST_BONUS)
            self.popups.append([f"GHOST BONUS  +{GHOST_BONUS}", (150, 170, 255), 2.5])

    def draw_setpiece(self, screen):
        piece = self.setpiece
        if not piece or self.game_over:
            return
        y = 12 + 108 * UI                                  # 왼쪽 위 정보 아래, 가운데
        if piece["kind"] == "extraction":
            t = max(0, piece["timer"])
            color = RED if t < 10 and pygame.time.get_ticks() // 250 % 2 else (255, 220, 90)
            self.center_text(screen, self.font, f"EXTRACTION  {int(t) // 60}:{int(t) % 60:02d}", color, y)
        elif piece["kind"] == "lights":
            text = "LIGHTS OUT  -  SPOTTED" if piece["spotted"] else "LIGHTS OUT  -  UNSEEN"
            self.center_text(screen, self.small_font, text, RED if piece["spotted"] else (150, 170, 255), y)
        else:
            truck = piece["truck"]
            done = truck["step"] / max(1, len(truck["path"]) - 1)
            hp = max(0, truck["hp"]) / CONVOY_HP
            self.center_text(screen, self.small_font, f"CONVOY  HP {hp * 100:.0f}%   ROUTE {done * 100:.0f}%",
                             RED if hp < 0.3 else (255, 160, 60), y)

    def place_devices(self, set_no, boss_round):
        """전투 시작: 벽 옆 빈 칸에 드럼통 몇 개, 가끔 적들 근처에 경보기"""
        self.devices = []
        if self.mode != "campaign" or self.challenge:
            return
        start = self.player.pos
        cells = []
        for row, line in enumerate(GAME_MAP):
            for col, ch in enumerate(line):
                spot = pygame.Vector2(col + 0.5, row + 0.5)
                if is_blocked(spot.x, spot.y) or spot.distance_to(start) < 6:
                    continue
                if any(e.pos.distance_to(spot) < 1.5 for e in self.enemies) or any(p.pos == spot for p in self.pickups):
                    continue
                if any(in_map(col + dx, row + dy) and GAME_MAP[row + dy][col + dx] in WALLS
                       for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    cells.append(spot)
        rng = random.Random(self.round * 31 + set_no)
        for spot in rng.sample(cells, min(len(cells), 2 + set_no // 2)):
            self.devices.append(Device("barrel", spot.x, spot.y))
        if not boss_round and self.round % 3 == 0 and len(self.enemies) >= 4 and cells:
            middle = sum((e.pos for e in self.enemies), pygame.Vector2()) / len(self.enemies)
            spot = min(cells, key=lambda c: c.distance_to(middle))
            self.devices.append(Device("alarm", spot.x, spot.y))
            self.sub_banners.append(("ALARM ON SITE  -  DESTROY IT BEFORE THEY USE IT", (255, 200, 60)))

    def device_hit(self, ax, ay, max_dist):
        """화면 (ax, ay) 에 보이는 장치나 켜진 가로등 (적보다 가까운 것만)"""
        col = int(ax // self.col_w)
        wall = self.zbuffer[col] if 0 <= col < self.num_rays else math.inf
        best, best_d = None, min(max_dist, wall)
        things = [(dev, *DEVICE_SIZE[dev.kind]) for dev in self.devices]
        things += [(d, d.height, 0.5) for d in self.decor if d.glow]
        for thing, height, width in things:
            box = self.project(thing.pos, height, width)
            if not box:
                continue
            sx, top, bottom, w, perp = box
            if perp < best_d and abs(ax - sx) < max(w / 2, 4) and top <= ay <= bottom:
                best, best_d = thing, perp
        return best

    def shoot_device(self, ax, ay, max_dist, damage):
        thing = self.device_hit(ax, ay, max_dist)
        if thing is None:
            return False
        if isinstance(thing, Device):
            self.damage_device(thing, damage)
        else:                                               # 가로등: 깨지고 꺼져요
            thing.glow = False
            thing.image = make_broken_lamp(thing.image)
            self.play_at("glass", thing.pos, 16)
            self.popups.append(["LIGHT OUT", (150, 150, 170), 1.0])
        self.add_impact(ax, ay, 0)
        return True

    def damage_device(self, dev, damage):
        if dev not in self.devices:
            return
        dev.hp -= damage
        if dev.hp > 0:
            return
        self.devices.remove(dev)
        if dev.kind == "barrel":
            self.boon_blasts.append((pygame.Vector2(dev.pos), *BARREL_BLAST))      # 다음 장면에 쾅 (연쇄 폭발)
        else:
            self.play_at("smash", dev.pos, 18)
            if dev.state in ("idle", "arming"):
                self.popups.append(["ALARM DESTROYED", (80, 240, 255), 1.5])
                self.add_xp(100)

    def update_devices(self, dt):
        """경보기: 적이 나를 보면 8초 뒤 울려요 → 증원. 울리기 전에 부수면 끝"""
        for dev in self.devices:
            if dev.kind != "alarm" or dev.state == "done":
                continue
            if dev.state == "idle" and any(e.sees for e in self.enemies):
                dev.state, dev.timer = "arming", ALARM_DELAY
                self.popups.append(["ALARM ARMING! SHOOT IT", RED, 2.0])
            elif dev.state == "arming":
                dev.timer -= dt
                if not self.enemies:
                    dev.state = "done"
                elif dev.timer <= 0:
                    dev.state, dev.timer = "ringing", 6.0
                    self.popups.append(["ALARM! REINFORCEMENTS", RED, 2.5])
                    far = [pt for pt in self.spawn_points if pygame.Vector2(pt).distance_to(self.player.pos) > 8]
                    for x, y in random.sample(far, min(ALARM_BACKUP, len(far))):
                        guard = Enemy(x, y, "GRUNT", self.skill)
                        guard.search = pygame.Vector2(self.player.pos)
                        self.enemies.append(guard)
            elif dev.state == "ringing":
                before = dev.timer
                dev.timer -= dt
                if int(before * 2) != int(dev.timer * 2):
                    self.play_at("beep", dev.pos, 30, 0.7)
                if dev.timer <= 0:
                    dev.state = "done"

    def update_boss_pattern(self, boss, dt):
        """세트 마지막 보스의 특별 패턴 (경고 표시가 먼저 나오고 그다음 공격)"""
        style = boss.style
        faster = 0.7 if getattr(boss, "phase", 1) >= 2 else 1.0           # 화나면 더 자주
        boss.pattern_timer -= dt
        if style == "warlord":                                          # 워로드: 세 가지를 돌아가며
            style = ("barrage", "storm", "sniper")[boss.pattern_step % 3]
        if boss.pattern_timer > 0:
            return
        boss.pattern_step += 1
        p = self.player.pos
        if style == "barrage":                                          # 수류탄 부채꼴 3발
            self.callout_cooldown = 0.0
            self.shout(boss, "FIRE IN THE HOLE!")
            side = pygame.Vector2(-(p - boss.pos).y, (p - boss.pos).x)
            side = side.normalize() * 2.2 if side.length() else pygame.Vector2(2.2, 0)
            for offset in (-side, pygame.Vector2(0, 0), side):
                self.enemy_throw(boss, p + offset)
            boss.pattern_timer = 7.0 * faster
        elif style == "storm":                                          # 공습 표시 3개
            self.callout_cooldown = 0.0
            self.shout(boss, "BRING THE THUNDER!")
            for k in range(3):
                spot = p + pygame.Vector2(random.uniform(0.5, 2.5) * (k > 0), 0).rotate(random.uniform(0, 360))
                self.boss_marks.append([spot, BOSS_STRIKE[2] + k * 0.35])
            boss.pattern_timer = 6.5 * faster
        elif style == "sniper":                                         # 빨간 레이저 → 묵직한 한 발
            if boss.sees:
                self.boss_laser = [boss, BOSS_SNIPE[1]]
                self.play_at("beep", boss.pos, 25, 0.8)
            boss.pattern_timer = 6.0 * faster
        elif style == "armored" and getattr(boss, "phase", 1) >= 2:     # 화나면 내 엄폐물을 부숴요
            near = [(c, r) for r, line in enumerate(GAME_MAP) for c, ch in enumerate(line)
                    if ch in DESTRUCTIBLE and p.distance_to(pygame.Vector2(c + 0.5, r + 0.5)) < 5]
            for c, r in random.sample(near, min(2, len(near))):
                self.destroy_cell(c, r)
            if near:
                self.popups.append(["COVER DESTROYED!", RED, 1.5])
            boss.pattern_timer = 8.0
        else:
            boss.pattern_timer = 2.0

    def update_boss_effects(self, dt):
        """공습 표시가 터지고, 저격 레이저가 끝나면 쏴요"""
        strike_r, strike_dmg, _ = BOSS_STRIKE
        for mark in self.boss_marks:
            mark[1] -= dt
            if mark[1] <= 0:
                self.explode(mark[0], strike_r, strike_dmg, owner="enemy")
                if self.mode == "campaign" and set_of(self.round) >= 4:
                    self.lightning = 0.25                               # 번쩍!
        self.boss_marks = [m for m in self.boss_marks if m[1] > 0]
        if self.boss_laser:
            boss, left = self.boss_laser
            self.boss_laser[1] = left - dt
            if boss not in self.enemies:
                self.boss_laser = None
            elif self.boss_laser[1] <= 0:
                self.boss_laser = None
                self.play_at("sniper", boss.pos, 40)
                if can_see(boss.pos, self.player.pos) and not smoke_blocks(boss.pos, self.player.pos):
                    self.last_attacker = boss
                    self.hurt_player(BOSS_SNIPE[0], boss.pos)
                # 쏜 다음엔 연기 속으로 자리를 옮겨요
                SMOKES.append([pygame.Vector2(boss.pos), 4.0])
                spots = [pygame.Vector2(pt) for pt in self.spawn_points
                         if 6 < pygame.Vector2(pt).distance_to(self.player.pos) < 16]
                if spots:
                    boss.pos.update(random.choice(spots))

    def boss_armor(self, enemy, amount):
        """앞쪽 장갑: armored/warlord 보스는 앞에서 쏘면 덜 아파요 (옆이나 뒤가 약점)"""
        if enemy.kind != "BOSS" or getattr(enemy, "style", None) not in ("armored", "warlord"):
            return amount
        to_me = self.player.pos - enemy.pos
        if to_me.length() == 0 or to_me.normalize().dot(enemy.facing) < 0.35:
            return amount * 1.3                                         # 옆·뒤: 더 아파요
        if not getattr(self, "armor_hint", False):
            self.armor_hint = True
            self.popups.append(["ARMOR! FLANK HIM", (255, 200, 60), 2.0])
        return amount * BOSS_ARMOR

    def draw_boss_telegraphs(self, screen):
        """공습 표시(바닥의 빨간 원)와 저격 레이저(빨간 선)"""
        strike_r, _, total = BOSS_STRIKE
        for pos, left in self.boss_marks:
            blink = 120 + int(135 * abs(math.sin(left * (10 if left < 0.8 else 5))))
            # 바깥 원(터지는 범위)과 안쪽 원(줄어들수록 곧 터져요)을 바닥에 원근감 있게
            for radius, color, width in ((strike_r, (255, 40, 40), 3),
                                         (strike_r * max(0.05, 1 - left / total), (255, blink, 60), 2)):
                points = []
                for k in range(24):
                    spot = pos + pygame.Vector2(radius, 0).rotate(k * 15)
                    box = self.project(spot, 0.0, 0.01)
                    if not box or box[4] < 0.3:
                        points = []
                        break
                    points.append((box[0], box[2]))
                if len(points) > 2:
                    pygame.draw.polygon(screen, color, points, width)
        if self.boss_laser:
            boss, left = self.boss_laser
            box = self.enemy_box(boss)
            if box:
                sx, top, bottom, w, perp = box
                start = (sx, top + (bottom - top) * 0.3)
                width = 1 + int(4 * (1 - left / BOSS_SNIPE[1]))
                pygame.draw.line(screen, (255, 30, 30), start, (WIDTH / 2, HEIGHT / 2 + 30 * UI), width)

    def update_allies(self, dt):
        """동료: 명령에 따라 움직이고, 보이는 가장 가까운 적을 쏴요"""
        p = self.player
        order = SQUAD_ORDERS[self.squad_order]
        side = pygame.Vector2(-p.forward.y, p.forward.x)
        self.world_tracers = [[tr[0], tr[1], tr[2] - dt, *tr[3:]] for tr in self.world_tracers if tr[2] - dt > 0]
        for k, ally in enumerate(self.allies):
            ally.flash = max(0.0, ally.flash - dt)
            if ally.callout:
                ally.callout[1] -= dt
                if ally.callout[1] <= 0:
                    ally.callout = None
            if ally.down:
                continue
            # 적 고르기: 보이는 적 중 가장 가까운 (0.25초마다)
            ally.look_timer -= dt
            if ally.look_timer <= 0:
                ally.look_timer = 0.25
                seen = [e for e in self.enemies if e.pos.distance_to(ally.pos) < 15 and can_see(ally.pos, e.pos)]
                ally.target = min(seen, key=lambda e: e.pos.distance_to(ally.pos)) if seen else None
            if ally.target not in self.enemies:
                ally.target = None
            # 갈 곳
            offset_side = side * (0.9 if k == 0 else -0.9)
            if order == "HOLD" and self.hold_pos is not None:
                goal = self.hold_pos + offset_side
            elif order == "ATTACK" and self.enemies:
                aim = ally.target or min(self.enemies, key=lambda e: e.pos.distance_to(ally.pos))
                goal = aim.pos if ally.pos.distance_to(aim.pos) > 5 or not ally.target else ally.pos
            else:
                goal = p.pos - p.forward * 1.5 + offset_side
            before = pygame.Vector2(ally.pos)
            offset = goal - ally.pos
            dist = offset.length()
            if dist > 0.6:
                speed = 3.6 if dist > 5 else 2.6
                move_with_collision(ally.pos, (steer(ally, goal, dt) or offset.normalize()) * speed * dt)
                if dist > 12 and not can_see(ally.pos, p.pos) and order == "FOLLOW":
                    spot = p.pos - p.forward * 1.0                # 너무 멀리 떨어지면 내 뒤로 따라붙어요
                    if not is_blocked(spot.x, spot.y):
                        ally.pos = pygame.Vector2(spot)
            moved = ally.pos.distance_to(before)
            ally.walk += moved
            ally.moving = 0.15 if moved > 0.0005 else max(0.0, ally.moving - dt)
            if ally.target:
                face = ally.target.pos - ally.pos
            else:
                face = ally.pos - before if moved > 0.0005 else p.forward
            if face.length() > 0:
                ally.facing = face.normalize()
            # 쏘기
            ally.shoot_timer -= dt
            if ally.target and ally.shoot_timer <= 0:
                ally.shoot_timer = random.uniform(0.45, 0.9)
                ally.flash = 0.08
                self.play_at("rifle", ally.pos, 20, 0.45)
                self.world_tracers.append([pygame.Vector2(ally.pos), pygame.Vector2(ally.target.pos), 0.07])
                chance = 0.55 - ally.pos.distance_to(ally.target.pos) * 0.02
                if random.random() < chance:
                    target = ally.target
                    self.damage_enemy(target, random.randint(10, 16), "ALLY")
                    if target not in self.enemies and not ally.callout:
                        ally.callout = [random.choice(("TANGO DOWN!", "GOT ONE!", "HOSTILE DOWN!")), 1.2]

    def hurt_ally(self, ally, damage):
        ally.hp -= damage
        if ally.hp <= 0 and not ally.down:
            ally.down = True
            self.popups.append([f"{ally.name} IS DOWN!", (90, 170, 255), 2.0])
            self.sounds.play("radio")

    def find_turrets(self):
        """캠페인 맵: 시작 자리에서 3~9칸, 적이 오는 쪽으로 멀리 트여 있는 곳에 기관총 하나 (맵마다 늘 같은 자리).
        바로 옆에 엄폐물(상자·모래주머니·돌담)이 있으면 더 좋은 자리예요."""
        spawns = find_cells("E")
        if self.theme.get("zombie") or self.theme.get("mission") or not spawns:
            return []
        start = pygame.Vector2(find_cells("P")[0])
        enemy_side = sum((pygame.Vector2(p) for p in spawns), pygame.Vector2()) / len(spawns)
        best = None
        for row in range(MAP_H):
            for col in range(MAP_W):
                spot = pygame.Vector2(col + 0.5, row + 0.5)
                if is_blocked(spot.x, spot.y) or not 3 <= spot.distance_to(start) <= 9:
                    continue
                toward = enemy_side - spot
                if toward.length() < 4:
                    continue
                facing = math.atan2(toward.y, toward.x)
                walls = cast_ray(spot.x, spot.y, facing)[1]
                depth = min(walls[0][0], 20) if walls else 20             # 앞이 얼마나 트였는지
                if depth < 8:
                    continue
                cover = sum(1 for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1))
                            if in_map(col + dc, row + dr) and GAME_MAP[row + dr][col + dc] in "ZVKJ")
                score = depth + cover * 4 - spot.distance_to(start) * 0.3
                if best is None or score > best[0]:
                    best = (score, spot, facing)
        return [dict(pos=best[1], facing=best[2])] if best else []

    def toggle_mount(self):
        """B: 가까운 고정 기관총에 타요 / 내려요"""
        a = self.arsenal
        if self.mounted:
            a.weapons = [w for w in a.weapons if w.spec["name"] != "MOUNTED MG"]
            a.index, a.switch_left = min(self.mount_return, len(a.weapons) - 1), 0.3
            self.mounted = None
            self.popups.append(["DISMOUNTED", WHITE, 1.0])
            return True
        turret = next((t for t in self.turrets if t["pos"].distance_to(self.player.pos) < 1.2), None)
        if not turret or self.game_over:
            return False
        self.mounted = turret
        self.mount_return = a.index
        a.weapons.append(Weapon(MOUNTED_MG))
        a.index, a.switch_left, a.reload_left = len(a.weapons) - 1, 0.3, 0.0
        self.player.pos = pygame.Vector2(turret["pos"])
        self.player.angle = turret["facing"]
        self.sounds.play("bolt")
        self.popups.append([f"MOUNTED MG  ({kl(pygame.K_b)}: get off)", (255, 200, 60), 1.5])
        return True

    def update_mounted(self, dt):
        """기관총에 탄 동안: 자리 고정, 좌우 60도까지만 돌기, 탄약 무한, 과열"""
        t = self.mounted
        self.player.pos = pygame.Vector2(t["pos"])
        rel = angle_diff(self.player.angle, t["facing"])
        if abs(rel) > 1.05:
            self.player.angle = t["facing"] + math.copysign(1.05, rel)
        w = self.arsenal.current
        if w.spec["name"] == "MOUNTED MG":
            w.mag = w.spec["mag"]
        if self.arsenal.since_shot > 0.25:                 # 쏘지 않을 때만 식어요
            self.mg_heat = max(0.0, self.mg_heat - MG_COOL * dt)

    def update_chopper(self, dt):
        """지원 헬기: 내 위를 크게 돌며 아래에 보이는 적을 쏴요"""
        c = self.chopper
        c["time"] -= dt
        if c["time"] <= 0:
            self.chopper = None
            self.popups.append(["CHOPPER LEAVING", (80, 240, 255), 1.5])
            return
        c["center"] += (self.player.pos - c["center"]) * min(1.0, dt * 0.5)     # 천천히 나를 따라와요
        c["angle"] += dt * 0.6
        c["pos"] = c["center"] + pygame.Vector2(CHOPPER_RADIUS, 0).rotate_rad(c["angle"])
        c["rotor"] -= dt
        if c["rotor"] <= 0:                                  # 두두두 프로펠러 소리
            c["rotor"] = 0.16
            self.play_at("punch", c["pos"], 30, 0.35)
        c["cooldown"] -= dt
        c["flash"] -= dt
        if c["cooldown"] > 0:
            return
        targets = [e for e in self.enemies if e.pos.distance_to(c["pos"]) < 13]
        if not targets:
            c["cooldown"] = 0.3
            return
        target = min(targets, key=lambda e: e.pos.distance_to(c["pos"]))
        c["cooldown"], c["flash"] = 0.12, 0.06
        self.play_at("lmg", c["pos"], 30, 0.5)
        self.world_tracers.append([pygame.Vector2(c["pos"]), pygame.Vector2(target.pos), 0.06, CHOPPER_LIFT])
        if random.random() < 0.5:
            self.damage_enemy(target, 26, "CHOPPER")

    def find_buyables(self):
        """좀비 맵에서 B 로 살 수 있는 것: 바리케이드(q), 벽 무기(y), 미스터리 상자(m), 전기 함정(z)"""
        items = []
        walls = 0
        for row, line in enumerate(GAME_MAP):
            for col, ch in enumerate(line):
                spot = pygame.Vector2(col + 0.5, row + 0.5)
                if ch == "q":
                    items.append(dict(kind="barricade", cell=(col, row), pos=spot, cost=BARRICADE_COST,
                                      name="OPEN BARRICADE"))
                elif ch == "y":
                    name, cost = WALL_WEAPONS[walls % len(WALL_WEAPONS)]
                    walls += 1
                    items.append(dict(kind="weapon", cell=(col, row), pos=spot, cost=cost, weapon=name,
                                      name=f"BUY {name}"))
                elif ch == "m":
                    items.append(dict(kind="box", cell=(col, row), pos=spot, cost=BOX_COST, name="MYSTERY BOX"))
        traps = [pygame.Vector2(c + 0.5, r + 0.5) for r, line in enumerate(GAME_MAP) for c, ch in enumerate(line) if ch == "z"]
        if traps:
            center = sum(traps, pygame.Vector2()) / len(traps)
            items.append(dict(kind="trap", pos=center, cells=traps, cost=TRAP_COST, name="ELECTRIC TRAP"))
        return items

    def nearby_buyable(self):
        """B 로 살 수 있는 가장 가까운 것 (1.4칸 안, 함정은 칸 어디든 가까우면)"""
        if self.mode != "zombies":
            return None
        p = self.player.pos
        best, best_d = None, 1.4
        for item in self.buyables:
            spots = item.get("cells", [item["pos"]])
            d = min(p.distance_to(q) for q in spots)
            if d < best_d:
                best, best_d = item, d
        return best

    def price_of(self, item):
        if item["kind"] == "weapon" and any(w.spec["name"] == item["weapon"] for w in self.arsenal.weapons):
            return item["cost"] // 2                         # 이미 있으면 탄약만 (반값)
        return item["cost"]

    def buy_item(self, item):
        cost = self.price_of(item)
        if item["kind"] == "trap" and self.trap_timer > 0:
            return
        if self.points < cost:
            self.popups.append([f"NEED {cost} POINTS", RED, 1.2])
            return
        self.points -= cost
        self.sounds.play("cash")
        if item["kind"] == "barricade":
            col, row = item["cell"]
            line = GAME_MAP[row]
            GAME_MAP[row] = line[:col] + FLOOR_GRID[row][col] + line[col + 1:]
            WALL_GRID[row][col] = None
            self.navigator.clear()
            self.buyables.remove(item)
            self.minimap = self.make_minimap()
            self.play_at("smash", item["pos"], 16)
            self.popups.append(["BARRICADE OPENED", (255, 200, 60), 1.5])
        elif item["kind"] == "weapon":
            self.give_weapon(item["weapon"])
        elif item["kind"] == "box":
            owned = [w.spec["name"] for w in self.arsenal.weapons]
            pool = [w["name"] for w in WEAPONS if w["name"] != self.arsenal.current.spec["name"]]
            name = random.choice([n for n in pool if n not in owned] or pool)
            self.give_weapon(name)
            self.sounds.play("streak")
            self.popups.append([f"MYSTERY BOX: {name}!", (200, 120, 255), 2.0])
        else:
            self.trap_timer = TRAP_TIME
            self.popups.append(["ELECTRIC TRAP ON!", (120, 200, 255), 1.5])

    def give_weapon(self, name):
        """무기를 받아요: 있으면 탄약을 가득, 없으면 새로 들고 바로 꺼내요"""
        a = self.arsenal
        for k, w in enumerate(a.weapons):
            if w.spec["name"] == name:
                w.mag = w.spec["mag"]
                w.reserve = int(w.spec["reserve"] * 2 * a.ammo_mult)
                a.switch(k)
                self.popups.append([f"{name} AMMO FULL", (80, 240, 255), 1.5])
                return
        a.weapons.append(Weapon(self.weapon_spec(name), a.ammo_mult))
        a.switch(len(a.weapons) - 1)
        self.popups.append([f"GOT {name}!", (255, 200, 60), 1.5])

    def update_trap(self, dt):
        """켜진 전기 함정 위의 좀비는 큰 피해 (불꽃이 튀어요)"""
        self.trap_timer -= dt
        trap = next((b for b in self.buyables if b["kind"] == "trap"), None)
        if not trap:
            return
        for enemy in list(self.enemies):
            if any(enemy.pos.distance_to(c) < 0.6 for c in trap["cells"]):
                self.damage_enemy(enemy, TRAP_DPS * dt, "TRAP")
        if random.random() < 0.5:                            # 지직: 함정 위 불꽃
            box = self.project(random.choice(trap["cells"]), 0.1, 0.3)
            if box:
                self.particles.append([box[0], box[2], random.uniform(-80, 80) * UI, random.uniform(-160, -60) * UI,
                                       0.2, max(2.0, 3 * UI), (150, 210, 255), False])

    def update_doors(self, dt):
        """문: 나나 적이 가까이 오면 열리고, 4초 동안 아무도 없으면 닫혀요 (그 칸에 아무도 없을 때만)"""
        people = [self.player.pos] + [e.pos for e in self.enemies] + [a.pos for a in self.allies if not a.down]
        for (cx, cy), timer in self.doors.items():
            center = pygame.Vector2(cx + 0.5, cy + 0.5)
            near = min(center.distance_to(q) for q in people)
            if near < DOOR_OPEN_RANGE:
                if timer <= 0:                                   # 열기: 그 칸을 바닥으로
                    row = GAME_MAP[cy]
                    GAME_MAP[cy] = row[:cx] + INDOOR_FLOORS[0] + row[cx + 1:]
                    WALL_GRID[cy][cx] = None
                    FLOOR_GRID[cy][cx] = INDOOR_FLOORS[0]
                    self.play_at("door", center, 14)
                self.doors[(cx, cy)] = 4.0
            elif timer > 0:                                      # 아무도 없으면 시간이 줄고, 다 되면 닫혀요
                timer -= dt
                if timer <= 0:
                    row = GAME_MAP[cy]
                    GAME_MAP[cy] = row[:cx] + DOORS[0] + row[cx + 1:]
                    WALL_GRID[cy][cx] = self.door_spec
                    self.play_at("door", center, 14, 0.7)
                self.doors[(cx, cy)] = max(0.0, timer)

    def music_state(self):
        """지금 음악 분위기: calm / relax / alert / peak / boss / over"""
        if self.game_over:
            return "over"
        if self.mode == "training":
            return "calm"
        if any(e.kind in ("BOSS", "TITAN") for e in self.enemies):
            return "boss"
        d = self.director
        if d.phase == "peak":
            return "peak"
        if d.phase == "relax":
            return "relax"
        if d.intensity > 0.3 or any(e.sees for e in self.enemies):
            return "alert"
        return "calm"

    def roll_contracts(self):
        """이번 라운드 계약 2개 (캠페인·DEEP RUN·좀비, 도전/연습/미션은 없음)"""
        if self.mode not in ("campaign", "zombies") or self.challenge or self.practice:
            return []
        keys = [k for k, c in CONTRACTS.items() if self.mode != "zombies" or c[4]]
        return [dict(key=k, count=0, done=False, failed=False) for k in random.sample(keys, 2)]

    def contract_progress(self, key, amount=1):
        for c in getattr(self, "contracts", []):
            if c["key"] == key and not c["done"] and not c["failed"]:
                c["count"] += amount
                if c["count"] >= CONTRACTS[key][3]:
                    self.complete_contract(c)

    def complete_contract(self, c):
        c["done"] = True
        name = CONTRACTS[c["key"]][0]
        self.add_xp(CONTRACT_XP)
        self.popups.append([f"CONTRACT COMPLETE: {name}  +{CONTRACT_XP}", (255, 200, 60), 2.5])
        self.sounds.play("cash", 0.7)
        if not self.practice:
            life = self.save.setdefault("lifetime", {})
            life["contracts"] = life.get("contracts", 0) + 1

    def contracts_on_clear(self):
        """라운드를 깨는 순간 판정하는 계약 (안 맞기, 빨리 깨기)"""
        for c in getattr(self, "contracts", []):
            if c["done"] or c["failed"]:
                continue
            if c["key"] == "clean" or (c["key"] == "fast" and self.round_time <= 60):
                self.complete_contract(c)
            elif c["key"] in ("clean", "fast"):
                c["failed"] = True

    def draw_contracts(self, screen):
        """왼쪽: 이번 라운드 계약 (진행 / 완료 초록 / 실패 빨강)"""
        if not getattr(self, "contracts", None):
            return
        tiny = self.fonts["tiny"]
        y = HEIGHT * 0.58
        screen.blit(tiny.render("CONTRACTS", True, UI_DIM), (16, y))
        for c in self.contracts:
            y += tiny.get_linesize() + 2 * UI
            name, _, en, goal, _ = CONTRACTS[c["key"]]
            if c["done"]:
                text, color = f"[OK] {name}", GREEN
            elif c["failed"]:
                text, color = f"[X] {name}", RED
            else:
                state = f"{c['count']}/{goal}" if goal > 1 else ""
                if c["key"] == "fast":
                    state = f"{max(0, 60 - int(self.round_time))}s"
                text, color = f"{name}  {state}  - {en}", WHITE
            screen.blit(tiny.render(fit_text(tiny, text, WIDTH * 0.24), True, color), (16, y))

    def offer_boons(self):
        """DEEP RUN: 강화 3개를 보여줘요 (SECOND WIND 는 하나만)"""
        pool = [b[0] for b in unlocked_boons(self.save) if not (b[0] == "wind" and self.boons.get("wind"))]
        self.boon_choice = random.sample(pool, min(3, len(pool)))
        self.boon_sel = 0
        self.sounds.play("streak", 0.6)

    def pick_boon(self, index):
        key = self.boon_choice[index]
        self.boons[key] = self.boons.get(key, 0) + 1
        self.boon_choice = None
        self.max_hp = max(40, self.base_max_hp + 30 * self.boons.get("thick", 0) - 25 * self.boons.get("glass", 0))
        self.popups.append([f"NEW BOON: {BOON_BY_KEY[key][1]}", (255, 200, 60), 2.0])
        self.sounds.play("heal", 0.6)

    def boon_on_kill(self, enemy, how):
        b = self.boons
        if b.get("vampire"):
            self.player.hp = min(self.max_hp, self.player.hp + 8 * b["vampire"])
        if b.get("adrenaline"):
            w = self.arsenal.current
            w.mag = min(w.spec["mag"], w.mag + 3 * b["adrenaline"])
        if b.get("boom") and how == "HEADSHOT!" and enemy.pos.distance_to(self.player.pos) > 2.2:
            self.boon_blasts.append((pygame.Vector2(enemy.pos), 1.6, 60 + 20 * b["boom"]))   # 다음 장면에 쾅

    def boon_on_hurt(self, damage):
        if self.boons.get("shield") and self.arsenal.reload_left > 0:
            damage *= 0.6
        if self.boons.get("wind") and not self.wind_used and self.player.hp - damage <= 0:
            self.wind_used = True
            self.popups.append(["SECOND WIND!", (80, 240, 255), 2.0])
            return self.player.hp - 30                      # 맞고 나면 체력 30 (낮았으면 오히려 채워져요)
        return damage

    def end_deeprun(self):
        """DEEP RUN 이 끝나면 기록: 최고 깊이, 총 깊이 (새 강화가 풀려요)"""
        if self.deeprun_saved:
            return
        self.deeprun_saved = True
        data = self.save.setdefault("deeprun", {})
        before = len(unlocked_boons(self.save))
        data["best"] = max(data.get("best", 0), self.depth)
        data["total"] = data.get("total", 0) + self.depth
        data["runs"] = data.get("runs", 0) + 1
        for boon in unlocked_boons(self.save)[before:]:
            self.popups.append([f"NEW BOON UNLOCKED: {boon[1]}", (255, 200, 60), 3.5])
        write_save(self.save)

    def draw_boon_choice(self, screen):
        """강화 고르기 카드 3장"""
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((5, 4, 12, 170))
        screen.blit(dim, (0, 0))
        ko = self.fonts["lang"] == "ko"
        self.center_text(screen, self.big_font, "CHOOSE A BOON", (255, 200, 60), HEIGHT * 0.2)
        n = len(self.boon_choice)
        card_w, gap = min(WIDTH * 0.27, 330 * UI), WIDTH * 0.02
        left = WIDTH / 2 - (n * card_w + (n - 1) * gap) / 2
        for i, key in enumerate(self.boon_choice):
            _, name, desc_ko, desc_en, _ = BOON_BY_KEY[key]
            rect = pygame.Rect(left + i * (card_w + gap), HEIGHT * 0.3, card_w, HEIGHT * 0.36)
            draw_panel(screen, rect, i == self.boon_sel, radius=12)
            draw_keycap(screen, self.small_font, str(i + 1), rect.x + 14 * UI, rect.y + 24 * UI)
            have = self.boons.get(key, 0)
            if have:
                tag = self.fonts["tiny"].render(f"HAVE x{have}", True, UI_CYAN)
                screen.blit(tag, tag.get_rect(topright=(rect.right - 12 * UI, rect.y + 14 * UI)))
            title = fit_text(self.font, name, rect.w - 24 * UI)
            image = self.font.render(title, True, YELLOW if i == self.boon_sel else WHITE)
            screen.blit(image, image.get_rect(center=(rect.centerx, rect.y + rect.h * 0.38)))
            for k, line in enumerate(wrap_text(self.fonts["help"], desc_ko if ko else desc_en, rect.w - 30 * UI)[:3]):
                text = self.fonts["help"].render(line, True, (200, 230, 255))
                screen.blit(text, text.get_rect(center=(rect.centerx, rect.y + rect.h * 0.58 + k * self.fonts["help"].get_linesize())))
        draw_key_text(screen, self.small_font, [("1-3", "pick"), ("LEFT/RIGHT", "move"), ("SPACE", "take")],
                      (WIDTH / 2, HEIGHT * 0.74))

    def update_director(self, dt):
        """디렉터: 긴장감 계산, 숨 돌리기에 들어가면 체력/탄약이 모자랄 때 보급 상자 하나"""
        d = self.director
        before = d.phase
        d.update(dt, any(e.sees for e in self.enemies))
        if d.phase == "relax" and before != "relax":
            self.relax_supply()

    def relax_supply(self):
        """숨 돌리기 보급: 체력이 낮으면 구급상자, 탄약이 적으면 탄약 상자를 가까운 곳에"""
        d = self.director
        if d.supplied:
            return
        w = self.arsenal.current
        kind = "health" if self.player.hp < 55 else ("ammo" if w.reserve < w.spec["mag"] * 1.5 else None)
        if kind is None:
            return
        p = self.player.pos
        for _ in range(40):
            spot = p + pygame.Vector2(random.uniform(2.5, 5), 0).rotate(random.uniform(0, 360))
            if in_map(int(spot.x), int(spot.y)) and not is_blocked(spot.x, spot.y) and can_see(p, spot):
                self.pickups.append(Pickup(spot.x, spot.y, kind))
                self.popups.append(["SUPPLY DROP NEARBY", (80, 240, 255), 2.0])
                d.supplied = True
                return

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
        self.squad_timer -= dt * (1.6 if self.director.phase == "peak" else 1.0)
        if self.director.phase == "relax":
            return                                   # 숨 돌리기: 새 작전(제압·측면)은 잠깐 쉬어요
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
        Enemy.flow = build_flow((int(self.player.pos.x), int(self.player.pos.y)))

    def spawn_zombie(self):
        """내가 안 보는 먼 곳에서 좀비가 나와요"""
        p = self.player.pos
        flow = Enemy.flow
        spots = [pt for pt in self.spawn_points
                 if p.distance_to(pt) > 6 and not can_see(p, pygame.Vector2(pt))
                 and (flow is None or flow[int(pt[1])][int(pt[0])] is not None)]     # 바리케이드 안쪽은 빼요
        if not spots:
            spots = sorted(self.spawn_points, key=lambda pt: -p.distance_to(pt))[:3]
        x, y = random.choice(spots)
        if getattr(self, "titan_due", False):
            kind, self.titan_due = "TITAN", False
            self.popups.append(["TITAN HAS ARRIVED!", RED, 2.5])
            self.sounds.play("streak")
        elif self.brute_due:
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
            self.spawn_timer -= dt * self.director.spawn_mult
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
        if self.practice:
            return                                   # 사격장: 경험치 없음
        before = self.rank
        self.xp += amount
        self.save["xp"] = self.xp
        self.run_score += amount                     # 랭킹 점수
        self.stats["score"] = self.stats.get("score", 0) + amount
        if text:
            self.popups.append([text, color, 1.4])
        if self.rank > before:
            self.popups.append([f"RANK UP!  RANK {self.rank}  (+1 SKILL POINT)", (255, 80, 200), 2.5])
            self.check_unlocks()

    def record_history(self):
        """판이 끝나면 최근 기록에 한 줄 (최근 10판만)"""
        if self.practice or (time.time() - self.started < 20 and self.kills == 0):
            return
        mode = f"CHALLENGE {self.challenge}" if self.challenge else self.mode.upper()
        if self.mode == "mission":
            mode += f" {MISSIONS[self.mission]['name']}"
        entry = dict(date=time.strftime("%Y-%m-%d %H:%M"), mode=mode, round=self.round, kills=self.kills,
                     acc=round(100 * self.game_hits / self.game_shots) if self.game_shots else 0,
                     minutes=round((time.time() - self.started) / 60, 1))
        history = self.save.setdefault("history", [])
        history.append(entry)
        del history[:-10]

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
        # 배율만큼 시야를 좁혀요 (tan을 써야 정확히 '몇 배'가 돼요). 달리면 살짝 넓어져요
        wide = 1 + SPRINT_FOV * round(getattr(self, "sprint_fov", 0.0), 2)
        return 2 * math.atan(math.tan(NORMAL_FOV * wide / 2) / self.zoom)

    @property
    def proj(self):
        """거리 1에 있는 높이 1짜리 물체가 화면에서 몇 px인지"""
        return (WIDTH / 2) / math.tan(self.fov / 2)

    @property
    def horizon(self):
        """지평선의 화면 y좌표. 위를 보거나 반동이 생기면 아래로 내려가요."""
        return HEIGHT / 2 + (self.player.pitch + self.arsenal.recoil) * self.zoom + self.shake_offset + \
            getattr(self, "cam_offset", 0.0)

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
        if event.type == pygame.KEYDOWN and self.boon_choice:      # DEEP RUN 강화 고르기
            if pygame.K_1 <= event.key < pygame.K_1 + len(self.boon_choice):
                self.pick_boon(event.key - pygame.K_1)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.boon_sel = (self.boon_sel - 1) % len(self.boon_choice)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.boon_sel = (self.boon_sel + 1) % len(self.boon_choice)
            elif event.key in (pygame.K_SPACE, pygame.K_f):
                self.pick_boon(self.boon_sel)
            return
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
            elif self.wheel and self.wheel["open"] and event.key in WHEEL_KEYS:
                self.move_wheel(event.key)
            elif pygame.K_1 <= event.key <= pygame.K_9 and event.key - pygame.K_1 < len(a.weapons):
                a.switch(event.key - pygame.K_1)
            elif event.key == pygame.K_0 and len(a.weapons) >= 10:
                a.switch(9)
            elif event.key == pygame.K_TAB:          # 짧게: 다음 무기, 꾹: 무기 휠 (update 에서)
                if self.wheel is None:
                    self.wheel = dict(t=0.0, pick=a.index, open=False)
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
            elif event.key == pygame.K_k and self.allies:      # 동료 명령: 따라와 → 대기 → 공격
                self.squad_order = (self.squad_order + 1) % len(SQUAD_ORDERS)
                order = SQUAD_ORDERS[self.squad_order]
                self.hold_pos = pygame.Vector2(self.player.pos) if order == "HOLD" else None
                text = {"FOLLOW": "SQUAD: ON ME!", "HOLD": "SQUAD: HOLD THIS POSITION", "ATTACK": "SQUAD: ATTACK!"}[order]
                self.popups.append([text, (90, 170, 255), 1.5])
                self.sounds.play("radio")
                for ally in self.allies:
                    if not ally.down:
                        ally.callout = [{"FOLLOW": "ON YOU!", "HOLD": "HOLDING!", "ATTACK": "MOVING IN!"}[order], 1.2]
            elif event.key == pygame.K_l:                       # 손전등
                self.flashlight = not self.flashlight
                self.sounds.play("beep", 0.4)
                self.popups.append(["FLASHLIGHT ON" if self.flashlight else "FLASHLIGHT OFF", WHITE, 0.8])
            elif event.key == pygame.K_i and not a.busy and not self.aiming:   # 무기 살펴보기
                self.inspect_timer = 2.4
            elif event.key == pygame.K_e:      # 정조준 켜기/끄기
                self.aim_on = not self.aim_on
            elif event.key == pygame.K_z:      # 배율 바꾸기 3 -> 6 -> 12 -> 3
                a.zoom_index = (a.zoom_index + 1) % len(SCOPE_ZOOMS)
            elif event.key == pygame.K_g:
                if self.arsenal.grenades > 0 and self.knife_timer == 0 and self.cooking is None:
                    self.cooking = 0.0                   # 핀 뽑기: 떼면 던져요 (오래 쥐면 짧게 터져요)
                    self.sounds.play("mech", 0.8)
            elif event.key == pygame.K_n:
                self.throw_tactical()
            elif event.key == pygame.K_v:
                self.knife_attack()
            elif event.key == pygame.K_c:
                self.player.toggle_crouch()
            elif event.key == pygame.K_x:
                self.use_streak()
            elif event.key == pygame.K_b and self.mode != "zombies":
                self.toggle_mount()
            elif event.key == pygame.K_b and self.mode == "zombies":
                item = self.nearby_buyable()
                if item:
                    self.buy_item(item)
                else:
                    self.buy("ammo")
            elif event.key == pygame.K_u and self.mode == "zombies":
                self.buy("upgrade")

    # ----- 게임 진행 -----
    def vault_target(self):
        """앞에 낮은 엄폐물(한 칸 두께)이 있고 그 뒤가 비어 있으면 넘어갈 자리를 돌려줘요"""
        p = self.player
        f = p.forward
        ahead = p.pos + f * 0.6
        col, row = int(ahead.x), int(ahead.y)
        if not in_map(col, row) or GAME_MAP[row][col] not in VAULT_WALLS:
            return None
        for k in range(8, 24):                            # 엄폐물 뒤 첫 빈 자리
            spot = p.pos + f * (k / 10)
            if (int(spot.x), int(spot.y)) == (col, row):
                continue
            if is_blocked(spot.x, spot.y):
                return None                               # 두 칸 넘게 막혀 있으면 못 넘어요
            end = spot + f * 0.3
            return end if not is_blocked(end.x, end.y) else None
        return None

    def update_movement2(self, dt, keys):
        """움직임 2.0: 낮은 엄폐물 뛰어넘기(앞으로 가며 스페이스), 몸 기울이기(, .)"""
        p = self.player
        strafe = (1 if keys[pygame.K_d] else 0) - (1 if keys[pygame.K_a] else 0)
        self.strafe_tilt += (-3.5 * strafe - self.strafe_tilt) * min(1.0, 8 * dt)
        if self.was_air and p.z == 0:
            self.land_dip = 0.25
        self.was_air = p.z > 0
        self.land_dip = max(0.0, self.land_dip - dt)
        self.dry_cd -= dt
        want = (1 if keys[pygame.K_PERIOD] else 0) - (1 if keys[pygame.K_COMMA] else 0)
        if p.sprinting or p.slide_timer > 0 or self.vault:
            want = 0
        self.lean += max(-6 * dt, min(6 * dt, want - self.lean))
        if self.vault:                                    # 넘는 중: 걷기·점프 키는 잠깐 쉬어요
            return MaskedKeys(keys, (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_SPACE, pygame.K_c))
        if keys[pygame.K_SPACE] and keys[pygame.K_w] and p.z == 0 and not p.crouch and p.slide_timer <= 0:
            end = self.vault_target()
            if end is not None:
                self.vault = dict(start=pygame.Vector2(p.pos), end=end, t=0.0)
                self.sounds.play("thunk", 0.45)
                return MaskedKeys(keys, (pygame.K_SPACE,))
        return keys

    def finish_vault_step(self):
        """뛰어넘는 움직임: 앞으로 미끄러지며 살짝 올라갔다 내려와요"""
        v, p = self.vault, self.player
        v["t"] += self.frame_dt
        k = min(1.0, v["t"] / VAULT_TIME)
        ease = k * k * (3 - 2 * k)
        p.pos.update(v["start"].lerp(v["end"], ease))
        p.z = 0.32 * math.sin(math.pi * k)
        p.vz = 0.0
        if k >= 1.0:
            p.z = 0.0
            self.vault = None

    def lean_offset(self):
        """기울인 만큼 눈이 옆으로 (벽 안으로는 안 들어가요)"""
        if abs(self.lean) < 0.02:
            return pygame.Vector2(0, 0)
        f = self.player.forward
        side = pygame.Vector2(-f.y, f.x) * self.lean * LEAN_DIST
        for scale in (1.0, 0.6, 0.3):
            spot = self.player.pos + side * scale
            if not is_blocked(spot.x, spot.y):
                return side * scale
        return pygame.Vector2(0, 0)

    def move_wheel(self, key):
        """무기 휠: ←↑ 이전, →↓ 다음, 숫자 키는 그 칸으로"""
        n = len(self.arsenal.weapons)
        if key in (pygame.K_LEFT, pygame.K_UP):
            self.wheel["pick"] = (self.wheel["pick"] - 1) % n
        elif key in (pygame.K_RIGHT, pygame.K_DOWN):
            self.wheel["pick"] = (self.wheel["pick"] + 1) % n
        else:
            index = 9 if key == pygame.K_0 else key - pygame.K_1
            if index < n:
                self.wheel["pick"] = index
        self.sounds.play("beep", 0.25)

    def update_wheel(self, dt, keys):
        """Tab 을 떼면: 휠이 열렸으면 고른 무기, 아니면 다음 무기"""
        if self.wheel is None:
            return keys
        a = self.arsenal
        if keys[pygame.K_TAB] and not self.game_over:
            self.wheel["t"] += dt
            if not self.wheel["open"] and self.wheel["t"] >= WHEEL_HOLD:
                self.wheel["open"] = True
                self.wheel["pick"] = a.index
        else:
            if self.wheel["open"]:
                a.switch(self.wheel["pick"])
            elif not self.game_over:
                a.switch(a.index + 1)
            self.wheel = None
            return keys
        if self.wheel["open"]:          # 화살표는 휠에 쓰니까 시점은 안 돌아요
            return MaskedKeys(keys, (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN))
        return keys

    def update(self, dt, keys, mouse_dx, mouse_dy, buttons):
        self.frame_dt = dt
        self.sounds.mix_music(MUSIC_MIX[self.music_state()], dt)
        keys = self.update_wheel(dt, keys)
        if self.wheel and self.wheel["open"]:
            dt *= WHEEL_SLOW                       # 휠을 보는 동안 시간이 느려져요
        if self.show_help:          # 도움말을 보는 동안은 멈춰요
            return
        if getattr(self, "ending", None) is not None:   # 엔딩 크레딧: 스페이스로 넘기기
            self.ending += dt
            if (self.ending > 2.0 and (keys[pygame.K_SPACE] or keys[pygame.K_f] or buttons[0])) or \
                    self.ending > ENDING_TIME:
                self.ending = None
            return
        if self.briefing is not None:   # 세트 브리핑: 스페이스/사격/클릭(패드 A)으로 시작
            self.briefing += dt
            if self.briefing > 0.8 and (keys[pygame.K_SPACE] or keys[pygame.K_f] or buttons[0]):
                self.briefing = None
            return
        if getattr(self, "pending_radio", None) and self.banner_timer < 2.5:
            self.radio(self.pending_radio, force=True)
            self.pending_radio = None
        if self.radio_msg:
            self.radio_msg[1] += dt
            if self.radio_msg[1] > 5.0:
                self.radio_msg = None
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
        self.navigator.clock += dt
        self.flashed = max(0.0, self.flashed - dt)
        if SMOKES:
            for cloud in SMOKES:
                cloud[1] -= dt
            SMOKES[:] = [c for c in SMOKES if c[1] > 0]
        if self.doors:
            self.update_doors(dt)
        if self.mode == "zombies" and self.trap_timer > 0:
            self.update_trap(dt)
        if self.allies and not self.game_over and self.round_clear_timer <= 0:
            self.update_allies(dt)
        if self.theme.get("rain"):                 # 폭풍우: 가끔 번개가 번쩍, 조금 뒤 천둥
            self.lightning_timer -= dt
            if self.lightning_timer <= 0:
                self.lightning_timer = random.uniform(8, 16)
                self.lightning = 0.3
                self.echoes.append([random.uniform(0.4, 1.5), "thunder", random.uniform(0.6, 1.0)])
        self.suppress = max(0.0, self.suppress - dt * 0.8)
        self.impact_sound_cd -= dt
        if self.round_clear_timer <= 0:
            self.round_time = getattr(self, "round_time", 0.0) + dt
        blasts, self.boon_blasts = self.boon_blasts, []
        for pos, radius, damage in blasts:
            self.explode(pos, radius, damage)
        if self.boss_marks or self.boss_laser:
            self.update_boss_effects(dt)
        if self.devices:
            self.update_devices(dt)
        if getattr(self, "setpiece", None):
            self.update_setpiece(dt)
        if self.hitstop > 0:        # 쓰러뜨린 순간: 아주 잠깐 멈춤 (묵직한 손맛)
            self.hitstop -= dt
            return
        if self.slowmo > 0:         # 마지막 적: 잠깐 슬로모션
            self.slowmo -= dt
            dt *= 0.35
        if self.banner_timer > getattr(self, "banner_prev", 0.0) + 0.01:    # 새 배너가 시작됐어요
            self.banner_len = self.banner_timer
        self.banner_timer -= dt
        self.banner_prev = self.banner_timer
        self.brief_age += dt
        self.hint_timer -= dt
        self.damage_flash = max(0.0, self.damage_flash - dt * 2)
        self.hitmarker = max(0.0, self.hitmarker - dt)
        self.shake = max(0.0, self.shake - dt)
        self.update_camera(dt)
        # 폭발 흔들림: 이번 장면에서 화면이 위아래로 움직일 양
        self.shake_offset = random.uniform(-1, 1) * self.shake * 30 * UI * SETTINGS.get("shake", 1)
        self.feed = [[text, t - dt] for text, t in self.feed if t - dt > 0]
        # [글자, 색, 남은 시간, 처음 시간] (처음 시간은 나타나고 사라지는 움직임에 써요)
        self.popups = [[p[0], p[1], p[2] - dt, p[3] if len(p) > 3 else p[2]] for p in self.popups if p[2] - dt > 0]
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
            if self.boon_choice:
                return                     # 강화를 고를 때까지 기다려요
            self.round_clear_timer -= dt
            if self.round_clear_timer <= 0:
                if self.deeprun:
                    self.round += DEEP_STEP
                    self.depth += 1
                else:
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
        speed *= 1 + 0.15 * self.boons.get("feet", 0)
        # 조준점이 적 위에 있으면 시점이 살짝 느리게 돌아요 (키보드로도 적을 놓치지 않게)
        self.on_target = self.enemy_at(WIDTH / 2, HEIGHT / 2) is not None
        sticky = ASSIST_STICKY[SETTINGS["assist"]] if self.on_target and not self.scoped else 1.0
        sens = min(1.0, 1.5 / self.zoom) * sticky
        angle_before = self.player.angle
        keys = self.update_movement2(dt, keys)
        speed *= 1 - 0.45 * abs(self.lean)                # 기울이고 있으면 천천히
        self.player.update(dt, keys, mouse_dx, mouse_dy, sens, speed,
                           allow_sprint=not self.aiming and not fire_down and abs(self.lean) < 0.2)
        if self.vault:
            self.finish_vault_step()
        turn = self.player.angle - angle_before
        self.sway = max(-50 * UI, min(50 * UI, self.sway * 0.85 - turn * 900 * UI))
        arsenal.update(dt)
        self.update_cooking(dt, keys)
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
        w_now = arsenal.current
        if pressed and w_now.mag == 0 and w_now.reserve == 0 and self.dry_cd <= 0 and not arsenal.busy:
            self.sounds.play("dry")                       # 빈 총: 딸깍
            self.dry_cd = 0.3
            self.popups.append([f"OUT OF AMMO  -  {kl(pygame.K_TAB)} SWITCH", RED, 1.2])
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
        # 눈에 띄는 정도: 앉으면 작게, 달리면 크게, 어두운 맵은 작게, 손전등을 켜면 크게
        vis = 1.0
        if p.crouch_amt > 0.5:
            vis *= 0.55
        if p.sprinting:
            vis *= 1.4
        elif p.moving:
            vis *= 1.15
        if self.night:
            vis *= 1.8 if self.flashlight else 0.6
            if any(d.glow and d.pos.distance_to(p.pos) < 3.5 for d in self.decor):
                vis *= 1.5                                  # 켜진 가로등 아래는 들키기 쉬워요 (쏴서 끄기)
        p.visibility = vis
        self.body_timer -= dt
        if self.body_timer <= 0 and self.mode != "zombies":
            self.body_timer = 0.5
            self.check_bodies()
        if self.mode not in ("training", "custom") and not self.challenge:
            self.update_director(dt)
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
                if getattr(enemy, "style", None):
                    self.update_boss_pattern(enemy, edt)
            if enemy.alarm >= 0.99 and not getattr(enemy, "alarm_played", False):
                enemy.alarm_played = True                      # 들켰어요! (한 번만)
                self.play_at("beep", enemy.pos, 18, 0.7)
            elif enemy.alarm < 0:
                enemy.alarm_played = False
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
            if enemy.flash_timer == 0.08 and self.allies and "melee" not in enemy.t:
                # 나보다 가까이 보이는 동료가 있으면 절반은 동료를 쏴요
                dist_me = enemy.pos.distance_to(p.pos)
                close = [a for a in self.allies if not a.down and a.pos.distance_to(enemy.pos) < min(dist_me, enemy.t["range"])
                         and can_see(enemy.pos, a.pos)]
                if close and random.random() < 0.5:
                    ally = min(close, key=lambda a: a.pos.distance_to(enemy.pos))
                    self.play_at(enemy.t.get("sound", "enemy"), enemy.pos, 24)
                    self.world_tracers.append([pygame.Vector2(enemy.pos), pygame.Vector2(ally.pos), 0.07])
                    if random.random() < enemy.t["accuracy"] * 0.7:
                        self.hurt_ally(ally, random.randint(*enemy.t["damage"]))
                    damage = 0
                    enemy.flash_timer = 0.079              # 아래에서 내 쪽 궤적을 또 그리지 않게
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
        if self.chopper:
            self.update_chopper(dt)
        if not self.allies and self.world_tracers:
            self.world_tracers = [[tr[0], tr[1], tr[2] - dt, *tr[3:]] for tr in self.world_tracers if tr[2] - dt > 0]
        if self.mounted:
            self.update_mounted(dt)
        self.update_effects(dt)
        self.collect_pickups()
        if self.mode != "zombies":
            self.update_objective(dt)

        if self.player.hp <= 0 and not self.game_over:
            self.player.hp = 0
            self.game_over = True
            self.director.on_death()
            self.start_killcam()
            if self.mode == "zombies":
                self.save["zbest"] = max(self.save.get("zbest", 0), self.round)
                write_save(self.save)
            elif self.deeprun:
                self.end_deeprun()
            elif not self.challenge and not self.practice:
                self.record_progress(self.round)      # 다음에 이 라운드부터 이어할 수 있게
            if self.mode != "mission":                # 미션은 체크포인트에서 이어지니까 아직 안 끝났어요
                self.finish_run()
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
        elif self.mode == "custom" and not self.enemies and self.round_clear_timer <= 0:
            self.slowmo = 0.8
            self.round_clear_timer = 4.0
            self.banner = "WAVE CLEAR"
            self.sub_banners = [("NEXT WAVE: MORE ENEMIES", WHITE)]
            self.banner_timer = 4.0
        elif self.challenge and not self.enemies:
            self.slowmo = 0.8
            self.add_xp(XP["round"], f"CHALLENGE CLEAR  +{XP['round']}")
            self.count_round()
            self.finish_challenge()
        elif self.mode == "campaign" and (self.objective["done"] if self.objective else not self.enemies):
            self.slowmo = 0.8                         # 마지막 한 명(또는 목표 완료): 슬로모션
            self.round_clear_timer = 4.0
            self.banner = "CAMPAIGN COMPLETE!" if self.round == CAMPAIGN_ROUNDS else "ROUND CLEAR"
            if self.round == CAMPAIGN_ROUNDS and not self.deeprun and not self.challenge:
                self.ending = 0.0                         # 100라운드: 엔딩 크레딧
                self.save["campaign_done"] = True
            self.sub_banners = [] if self.round != CAMPAIGN_ROUNDS else [("All 100 rounds cleared - the war goes on", YELLOW)]
            if self.round % SET_SIZE == 0 and self.round < CAMPAIGN_ROUNDS:       # 세트 끝
                story = STORY[set_of(self.round) - 1]
                self.banner = f"{story['op']} COMPLETE"
                self.sub_banners = [(f"SET {set_of(self.round)}: {SETS[set_of(self.round) - 1]} CLEARED", YELLOW)]
                self.radio("set", force=True)
            else:
                self.radio("clear", force=True)
            self.banner_timer = 4.0
            self.add_xp(XP["round"], f"ROUND CLEAR  +{XP['round']}")
            self.count_round()
            if self.deeprun:
                self.banner = f"DEPTH {self.depth} CLEAR"
                self.sub_banners = []
                self.offer_boons()
            else:
                self.record_progress(self.round + 1)

    def heat_up(self, spec):
        """고정 기관총 과열"""
        if spec["name"] != "MOUNTED MG":
            return
        self.mg_heat += MG_HEAT_PER_SHOT
        if self.mg_heat >= 1.0:
            self.mg_heat = 1.0
            self.arsenal.cooldown = MG_OVERHEAT
            self.popups.append(["OVERHEATED!", RED, 1.5])
            self.sounds.play("tail", 0.8)

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
        delay, echo, room = self.acoustics()
        loud = 0.5 if spec.get("suppressed") else 1.0
        self.sounds.play("tail", (0.85 if room == "indoor" else 0.6) * loud)
        self.echoes.append([delay, GUN_SOUNDS[spec["name"]], echo * loud])
        if room in ("indoor", "alley"):                   # 좁은 곳: 짧게 한 번 더 튕겨 울려요
            self.echoes.append([delay * 2.1, GUN_SOUNDS[spec["name"]], echo * 0.45 * loud])
        if not spec["projectile"] and (not spec["auto"] or random.random() < 0.4):
            self.echoes.append([random.uniform(0.3, 0.45), "casing", random.uniform(0.2, 0.35)])
        self.heat_up(spec)
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
        self.game_shots += 1
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
        """빗나간 총알: 맞은 곳의 재질(쇠, 나무, 벽돌, 물, 흙, 눈...)에 맞는 파편과 소리"""
        col = int(x // self.col_w)
        if not 0 <= col < self.num_rays:
            return
        material = "concrete"
        if self.zbuffer[col] < math.inf and y >= self.wall_top[col]:
            perp = self.zbuffer[col]
            if self.wall_hit[col]:
                cx, cy, vertical, wall_x, spec = self.wall_hit[col]
                material = WALL_MATERIAL.get(GAME_MAP[cy][cx], "concrete")
                if damage:
                    size = self.proj / max(0.05, perp)
                    height = (self.horizon + self.eye * size - y) / size       # 맞은 높이 (땅에서 몇 칸 위)
                    self.hit_wall(cx, cy, vertical, wall_x, height, damage, spec)
        elif y > self.horizon + 2:
            perp = self.eye * self.proj / (y - self.horizon)
        else:
            return                                # 하늘
        ray = self.player.angle + math.atan((x - WIDTH / 2) / self.proj)
        spot = self.player.pos + pygame.Vector2(math.cos(ray), math.sin(ray)) * perp / max(0.2, math.cos(ray - self.player.angle))
        if material == "concrete" and not (self.zbuffer[col] < math.inf and y >= self.wall_top[col]):
            col_, row_ = int(spot.x), int(spot.y)
            material = FLOOR_MATERIAL.get(FLOOR_GRID[row_][col_] if in_map(col_, row_) else ":", "concrete")
        self.impact_particles(x, y, min(1.0, 4 / max(0.5, perp)), material)
        if self.impact_sound_cd <= 0:                 # 산탄총 여러 발이어도 소리는 한 번
            self.impact_sound_cd = 0.06
            self.play_at(IMPACT_STYLES[material][5], spot, 14, 0.8)

    def impact_particles(self, x, y, near, material):
        """재질별 파편: (개수, 색들, 속도, 수명, 크기, 소리)"""
        count, colors, speed_range, life_range, size_range, _ = IMPACT_STYLES[material]
        for _ in range(count):
            angle = random.uniform(math.pi * 1.05, math.pi * 1.95)     # 위쪽으로 퍼져요
            speed = random.uniform(*speed_range) * UI * near
            self.particles.append([x, y, math.cos(angle) * speed, math.sin(angle) * speed,
                                   random.uniform(*life_range), max(1.0, random.uniform(*size_range) * UI * near),
                                   random.choice(colors), False])
        flash = (255, 240, 170) if material == "metal" else (255, 230, 140)
        if material in ("metal", "concrete", "brick", "stone"):
            self.particles.append([x, y, 0, 0, 0.05, max(2.0, (7 if material == "metal" else 4) * UI * near), flash, False])

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
        self.navigator.clear()                       # 길이 새로 생겼어요
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
        if self.mounted:
            damage *= 0.7                                  # 기관총 방패와 담 뒤라서 덜 아파요
        if self.challenge == "HARDCORE" and damage > 0:
            damage = max(damage, self.player.hp + 1)      # 한 방에 끝
        damage *= 1 - self.director.assist              # 같은 곳에서 여러 번 죽으면 조금 덜 아파요
        self.stagger = min(1.0, getattr(self, "stagger", 0.0) + damage / 35)    # 맞으면 화면이 휘청
        if self.boons:
            damage = self.boon_on_hurt(damage)
        if source is not None:
            self.last_source = pygame.Vector2(source)
        self.director.on_damage(damage)
        if damage > 0:
            for c in getattr(self, "contracts", []):
                if c["key"] == "clean" and not c["done"]:
                    c["failed"] = True
        self.player.hp -= int(damage)
        if 0 < self.player.hp < 35 and not self.low_warned:
            self.low_warned = True
            self.radio("low", force=True)
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
                spread *= spec.get("ads_spread", 0.45)   # 정조준하면 덜 퍼져요 (조준경이 좋을수록 더)
            else:
                spread *= spec.get("hip", 1.0)
        spread *= 0.7 ** self.boons.get("steady", 0)
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
        amount = self.boss_armor(enemy, amount)
        enemy.hp -= amount
        enemy.hurt_timer = 0.08
        enemy.flinch = 0.16 if how == "HEADSHOT!" else 0.12
        enemy.flinch_pose = "flinch_head" if how == "HEADSHOT!" else random.choice(("flinch_l", "flinch_r"))
        enemy.spotted = max(enemy.spotted, enemy.t["reaction"])   # 맞으면 바로 반격
        enemy.aware, enemy.combat_timer = 1.0, 6.0               # 맞으면 바로 알아채고 사방을 봐요
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
        if how != "TRAP":
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
            elif random.random() < (0.12 if self.mode == "zombies" else DROP_CHANCE) * (2 if self.boons.get("scav") else 1):
                kind = random.choices(list(DROP_WEIGHTS), weights=list(DROP_WEIGHTS.values()))[0]
                self.pickups.append(Pickup(enemy.pos.x, enemy.pos.y, kind))

    def on_kill(self, enemy, how):
        """처치 보상: 경험치, 연속 처치 메달, 킬스트릭"""
        if getattr(self, "contracts", None):
            dist = enemy.pos.distance_to(self.player.pos)
            if how in ("KNIFE!", "TAKEDOWN!"):
                self.contract_progress("blade")
            if how == "TAKEDOWN!":
                self.contract_progress("ghost")
            if how == "HEADSHOT!":
                self.contract_progress("heads")
            if how == "BOOM!":
                self.contract_progress("boom")
            if dist < 4:
                self.contract_progress("close")
            if dist >= 20 and how not in STREAK_KILLS:
                self.contract_progress("long")
        if self.boons:
            self.boon_on_kill(enemy, how)
        self.director.on_kill(enemy.pos.distance_to(self.player.pos))
        self.sounds.play("headshot" if how == "HEADSHOT!" else "kill")
        if not self.practice and how != "ALLY":   # 누적 기록 (업적용, 내가 쓰러뜨린 것만)
            life = self.save.setdefault("lifetime", {})
            life["kills"] = life.get("kills", 0) + 1
            key = {"HEADSHOT!": "heads", "KNIFE!": "knife", "TAKEDOWN!": "knife", "BOOM!": "explosive"}.get(how)
            if key:
                life[key] = life.get(key, 0) + 1
        stats = self.stats
        stats["kills"] += 1
        if stats["kills"] == 1:
            self.radio("first")
        elif len(self.enemies) == 1 and not self.objective:
            self.radio("last", force=True)
        if how == "HEADSHOT!":
            stats["heads"] += 1
        if how in ("DOWN", "HEADSHOT!"):                 # 총으로 쓰러뜨렸으면 그 총의 경험
            name = self.arsenal.current.spec["name"]
            stats["weapons"][name] = stats["weapons"].get(name, 0) + 1
            if self.loadout and not self.practice and name in WEAPON_BY_NAME:   # 고정 기관총은 성장 없음
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
            self.points += ZOMBIE_POINTS[key] + (TITAN_POINTS if enemy.kind == "TITAN" else 0)
        self.check_unlocks()
        xp = XP["kill"]
        if how == "HEADSHOT!":
            xp += XP["headshot"]
        elif how == "KNIFE!":
            xp += XP["knife"]
        elif how == "TAKEDOWN!":
            xp += XP["knife"] + TAKEDOWN_XP
            self.popups.append(["SILENT TAKEDOWN", (150, 220, 255), 1.5])
        if enemy.kind == "BOSS":
            xp += XP["boss"]
        if how == "ALLY":
            xp //= 2                                     # 동료가 쓰러뜨림: 절반
        self.add_xp(xp, f"+{xp}")

        self.score_highlight(enemy, how)
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
            if not self.practice:
                life = self.save.setdefault("lifetime", {})
                life["streak"] = max(life.get("streak", 0), self.streak)
            for need, name in STREAKS:
                if self.streak == need:
                    self.streaks_ready.append(name)
                    self.sounds.play("streak")
                    self.popups.append([f"{name} READY!  press {kl(pygame.K_x)}", (80, 240, 255), 2.5])
        self.check_achievements()

    def score_highlight(self, enemy, how):
        """이 처치가 이번 라운드의 가장 멋진 순간인지 (연속 처치, 몰래 처치, 먼 헤드샷, 보스)"""
        if how in STREAK_KILLS or self.practice:
            return
        multi = self.multi + 1 if self.time - self.last_kill < 3 else 1
        score, label = 1, "KILL"
        dist = enemy.pos.distance_to(self.player.pos)
        if multi >= 2:
            score, label = 2 + multi, {2: "DOUBLE KILL", 3: "TRIPLE KILL"}.get(multi, "MULTI KILL")
        if how == "TAKEDOWN!":
            score, label = max(score, 4), "SILENT TAKEDOWN"
        if how == "HEADSHOT!" and dist > 14:
            score, label = max(score, 4), f"LONG SHOT {dist:.0f}m"
        if enemy.kind in ("BOSS", "TITAN"):
            score, label = 9, f"{getattr(enemy, 'name', enemy.kind)} DOWN"
        best = max(self.highlight["score"] if self.highlight else 0, self.recording["score"] if self.recording else 0)
        if score >= max(2, best + (0 if self.recording and self.recording["label"] == label else 1)):
            self.recording = dict(label=label, score=score, frames=list(self.clip_frames), after=CLIP_AFTER)

    def capture_clip(self, screen, dt):
        """0.1초마다 작은 화면 한 장 (최근 2.5초만 기억)"""
        self.clip_timer -= dt
        if self.clip_timer > 0:
            return
        self.clip_timer = 1 / CLIP_FPS
        frame = pygame.transform.scale(screen, CLIP_SIZE)
        self.clip_frames.append(frame)
        del self.clip_frames[:-int(CLIP_BEFORE * CLIP_FPS)]
        if self.recording:
            self.recording["frames"].append(frame)
            self.recording["after"] -= 1 / CLIP_FPS
            if self.recording["after"] <= 0:
                self.highlight, self.recording = self.recording, None

    def check_achievements(self):
        """새로 이룬 업적을 알려줘요 (위장 무늬를 새로 얻으면 그것도)"""
        if self.practice:
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
        self.director.on_clear()
        self.setpiece_on_clear()
        self.contracts_on_clear()
        self.sounds.play_sting()
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
        elif name == "CHOPPER":
            self.chopper = dict(time=CHOPPER_TIME, center=pygame.Vector2(p.pos), angle=random.uniform(0, 6.28),
                                pos=pygame.Vector2(p.pos), cooldown=1.0, flash=0.0, rotor=0.0)
            self.popups.append(["CHOPPER INBOUND", (80, 240, 255), 1.5])
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
            if not target and self.shoot_device(ax, ay, target_dist, spec["body"]):
                pass                              # 드럼통·경보기·가로등에 맞음
            elif not target:
                self.add_impact(ax, ay, spec["body"])     # 벽이나 바닥에 맞으면 먼지와 불똥 (+ 자국, 부서짐)
            if target and self.challenge == "HEADSHOTS" and not head:
                continue                          # 헤드샷 도전: 몸에 맞으면 피해 없음
            if target:
                amount = spec["head"] * (1 + 0.15 * self.rank_of("MARKSMAN")) if head else spec["body"]
                amount *= 1 + 0.35 * self.boons.get("glass", 0)          # DEEP RUN: 유리 대포
                if self.challenge == "HARDCORE":
                    amount *= 2
                if self.perk == "HEAVY ROUNDS":
                    amount *= 1.25
                if found[5]:                      # 관통: 피해가 줄어요
                    amount *= PENETRATION
                    if not any(p[0] == "WALLBANG" for p in self.popups):
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
            self.game_hits += 1
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

    def acoustics(self):
        """내가 선 곳의 울림: (메아리 시간, 크기, 공간 이름). 실내 / 좁은 골목 / 탁 트인 곳
        0.5초마다 한 번만 주변 칸을 세어서 계산해요"""
        now = self.time
        cached = getattr(self, "_acoustics", None)
        if cached and abs(now - cached[0]) < 0.5:
            return cached[1]
        col, row = int(self.player.pos.x), int(self.player.pos.y)
        floor = FLOOR_GRID[row][col] if in_map(col, row) else ":"
        walls = sum(1 for dr in range(-2, 3) for dc in range(-2, 3)
                    if (dr or dc) and (not in_map(col + dc, row + dr) or WALL_GRID[row + dr][col + dc]))
        base_delay, base_echo = ECHOES.get(self.theme["name"], (0.25, 0.2))
        if floor in INDOOR_FLOORS:
            result = (0.07, 0.55, "indoor")
        elif walls >= 10:
            result = (0.11, max(base_echo, 0.38), "alley")
        else:
            result = (base_delay, base_echo, "open")
        self._acoustics = (now, result)
        return result

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
        if volume > 0.02 and name in MUFFLED_SOUNDS and (volume < 0.3 or not can_see(self.player.pos, pos)):
            name += "_m"            # 벽 너머이거나 아주 멀면: 먹먹한 소리 (높은 소리가 먼저 사라져요)
        self.sounds.play(name, volume * loud, pan)

    def update_cooking(self, dt, keys):
        """수류탄 쿠킹: G 를 쥐고 있는 동안 시간이 가요. 떼면 던지고, 너무 오래 쥐면 손에서 터져요"""
        if self.cooking is None:
            return
        self.cooking += dt
        if self.cooking >= GRENADE_FUSE:
            self.cooking = None
            self.arsenal.grenades -= 1
            self.popups.append(["COOKED TOO LONG!", RED, 1.5])
            self.explode(pygame.Vector2(self.player.pos), *GRENADE_BLAST, owner="player")
        elif not keys[pygame.K_g]:
            cook, self.cooking = self.cooking, None
            self.throw_grenade(cook)

    def throw_tactical(self):
        """전술 장비 던지기 (N): 섬광탄 / 연막탄 / 투척 칼"""
        if self.tactical_left <= 0 or self.knife_timer > 0 or self.game_over:
            return
        self.tactical_left -= 1
        self.sounds.play("throw")
        p = self.player
        forward = pygame.Vector2(math.cos(p.angle), math.sin(p.angle))
        slope = self.aim_slope()
        if self.tactical == "THROWING KNIFE":
            vel = forward * 16
            proj = Projectile("tknife", p.pos + forward * 0.3, self.eye - 0.1, vel, slope * 16 + 0.5)
        else:
            kind = "flash" if self.tactical == "FLASHBANG" else "smoke"
            vel = forward * GRENADE_THROW * (1 - min(0.5, abs(slope) * 0.5))
            proj = Projectile(kind, p.pos + forward * 0.3, self.eye - 0.1, vel, 3.0 + slope * GRENADE_THROW)
        self.projectiles.append(proj)

    def tactical_hit(self, proj):
        """전술 장비가 터지거나 꽂혔어요"""
        if proj.kind == "flash":
            self.play_at("flash", proj.pos, 26, 1.0)
            self.effects.append(Effect(proj.pos, self.explosion_frames, 0.15, 0.8))
            stunned = 0
            for enemy in self.enemies:
                d = enemy.pos.distance_to(proj.pos)
                if d < FLASH_RANGE and can_see(proj.pos, enemy.pos) and "melee" not in enemy.t:
                    enemy.stun = 1.0 + 2.5 * (1 - d / FLASH_RANGE)
                    enemy.aware, enemy.combat_timer = 1.0, 6.0
                    stunned += 1
            if stunned:
                self.popups.append([f"FLASHED x{stunned}", WHITE, 1.2])
            d = self.player.pos.distance_to(proj.pos)
            off = proj.pos - self.player.pos
            facing = d < 0.5 or abs(angle_diff(math.atan2(off.y, off.x), self.player.angle)) < math.pi / 2
            if d < FLASH_RANGE and facing and can_see(proj.pos, self.player.pos):
                self.flashed = max(self.flashed, 2.5 * (1 - d / FLASH_RANGE) + 0.3)   # 나도 눈부셔요
        elif proj.kind == "smoke":
            self.play_at("throw", proj.pos, 16, 0.6)
            SMOKES.append([pygame.Vector2(proj.pos), SMOKE_TIME])
        else:                                            # 투척 칼
            target = getattr(proj, "hit", None)
            if target in self.enemies:
                unaware = not target.sees and target.aware < 1.0
                self.damage_enemy(target, 9999 if unaware and target.kind != "BOSS" else 110,
                                  "TAKEDOWN!" if unaware and target.kind != "BOSS" else "KNIFE!")
            else:
                self.play_at("casing", proj.pos, 10, 1.0)
                self.tactical_left += 1                  # 빗나간 칼은 주워 와요

    def throw_grenade(self, cook=0.0):
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
        grenade = Projectile("grenade", p.pos + forward * 0.3, self.eye - 0.1, vel, vz)
        grenade.timer = max(0.15, GRENADE_FUSE - cook)       # 쿠킹한 만큼 빨리 터져요
        self.projectiles.append(grenade)

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
                if proj.kind in ("flash", "smoke", "tknife"):
                    self.tactical_hit(proj)
                    continue
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
        near = pos.distance_to(self.player.pos)
        if near < 4.5:
            self.deafen(0.85 * (1 - near / 4.5))
        if pos.distance_to(self.player.pos) < 10:          # 가까운 폭발: 주변이 확 밝아져요
            self.light_timer = max(self.light_timer, 0.14)
            self.muzzle_glow = max(self.muzzle_glow, 230)
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
        for dev in list(self.devices):
            if dev.pos.distance_to(pos) < radius and dev.pos.distance_to(pos) > 0.05:
                self.damage_device(dev, damage)
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
            behind = (p.pos - best.pos).dot(best.facing) < 0
            if not best.sees and best.aware < 1.0 and behind and best.kind != "BOSS" and "melee" not in best.t:
                self.damage_enemy(best, 9999, "TAKEDOWN!")      # 눈치 못 챈 적을 뒤에서: 한 번에, 조용히
            else:
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
    def draw(self, screen, hud=True):
        """기울이고 있으면 옆으로 옮긴 눈 위치에서 그려요 (몸은 그대로)"""
        shift = self.lean_offset() if not self.game_over else pygame.Vector2(0, 0)
        self.player.pos += shift
        try:
            self.draw_frame(screen, hud)
        finally:
            self.player.pos -= shift

    def draw_frame(self, screen, hud=True):
        if self.game_over and self.killcam_from is not None and self.killcam_time < KILLCAM_TIME:
            self.draw_killcam(screen)
            return
        self.draw_sky(screen)
        self.draw_world(screen)
        self.draw_sprites(screen)
        self.draw_boss_telegraphs(screen)
        self.draw_particles(screen, casings=False)       # 튀는 피
        if self.lightning > 0:
            self.flash_overlay.set_alpha(int(190 * self.lightning / 0.3 * (0.75 + 0.25 * math.sin(self.lightning * 60))))
            screen.blit(self.flash_overlay, (0, 0))
        if self.night or self.flashlight:
            self.draw_darkness(screen)
        piece = getattr(self, "setpiece", None)
        if piece and piece["kind"] == "lights":            # 소등: 세상 전체가 더 어두워요
            dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dim.fill((0, 0, 12, 90 if self.flashlight else 160))
            screen.blit(dim, (0, 0))
        if self.theme["snow"]:
            self.draw_snow(screen)
        if self.theme.get("rain"):
            self.draw_rain(screen)
        if not hud:                                       # 사진 모드: 총과 화면 글자 없이
            return
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
        if self.flashed > 0:                              # 섬광탄에 눈부심: 하얀 화면
            self.flash_overlay.set_alpha(int(255 * min(1.0, self.flashed / 1.2)))
            screen.blit(self.flash_overlay, (0, 0))
        self.post_process(screen)
        if self.wheel and self.wheel["open"]:
            self.draw_wheel(screen)                       # 휠을 보는 동안은 HUD 대신 휠만
        else:
            self.draw_hud(screen)
        if self.boon_choice and not self.game_over:
            self.draw_boon_choice(screen)
        if self.round_clear_timer <= 0 and not self.game_over and self.briefing is None:
            self.capture_clip(screen, self.frame_dt)
        elif self.round_clear_timer > 0:
            if self.recording:                               # 마지막 처치로 끝났으면 찍던 장면을 그대로
                self.highlight, self.recording = self.recording, None
            if self.highlight:
                self.draw_highlight(screen)
        if self.radio_msg and not self.game_over and not (self.wheel and self.wheel["open"]):
            self.draw_radio(screen)
        if self.briefing is not None:
            self.draw_briefing(screen)
        if getattr(self, "ending", None) is not None:
            self.draw_ending(screen)
        if self.mode == "training":
            self.draw_training(screen)
        if self.show_help:
            draw_help(screen, self.fonts, HELP_TEXT[self.fonts["lang"]]["resume"])

    def draw_tracers(self, screen):
        """총알 궤적: 내 총알은 총구에서 맞은 곳까지, 적 총알은 적에게서 내 쪽으로 (침은 초록)"""
        if self.world_tracers:
            self.draw_world_tracers(screen)
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

    def draw_world_tracers(self, screen):
        """동료 ↔ 적 사이 총알 궤적 (둘 다 화면 안에 있을 때)"""
        for tracer in self.world_tracers:
            start, end = tracer[0], tracer[1]
            lift = tracer[3] if len(tracer) > 3 else 0.0      # 헬기에서 쏜 총알은 하늘에서
            a = self.project(start, 0.9, 0.45, lift=lift)
            b = self.project(end, 0.9, 0.45)
            if a and b:
                pa = (a[0], a[1] + (a[2] - a[1]) * 0.45)
                pb = (b[0], b[1] + (b[2] - b[1]) * 0.45)
                pygame.draw.line(screen, (255, 225, 150), pa, pb, max(1, int(2 * UI)))

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

    def update_camera(self, dt):
        """카메라 연출: 달리기 시야, 맞았을 때 휘청, 착지 쿵, 큰 폭발 뒤 귀 먹먹함"""
        p = self.player
        want = 1.0 if p.sprinting else 0.0
        self.sprint_fov = getattr(self, "sprint_fov", 0.0)
        self.sprint_fov += (want - self.sprint_fov) * min(1.0, 6 * dt)
        self.stagger = max(0.0, getattr(self, "stagger", 0.0) - dt * 2.5)
        self.stagger_t = getattr(self, "stagger_t", 0.0) + dt
        shake_on = SETTINGS.get("shake", 1)
        offset = self.stagger * math.sin(self.stagger_t * 28) * 14 * UI * shake_on
        if self.land_dip > 0:
            offset += math.sin(self.land_dip / 0.25 * math.pi) * 10 * UI * shake_on
        self.cam_offset = offset
        sounds = self.sounds
        if getattr(sounds, "duck", 1.0) < 1.0:
            sounds.duck = min(1.0, sounds.duck + dt * 0.35)
            sounds.refresh_background()

    def deafen(self, amount):
        """큰 폭발이 가까우면: 귀가 삐- 하고 다른 소리가 잠깐 작아져요"""
        self.sounds.duck = max(0.25, min(getattr(self.sounds, "duck", 1.0), 1 - amount))
        if amount > 0.4:
            self.sounds.play("ring", amount * 0.6)

    def ending_lines(self):
        """엔딩 크레딧 글: 이야기 마무리 + 내 기록 + 만든 사람들"""
        life = self.save.get("lifetime", {})
        lines = [("STRIKE ZONE", "title"), ("", None), ("ALL 100 ROUNDS CLEARED", "big"),
                 ("The five operations are over. The coast is quiet again.", "normal"),
                 ("HQ: Outstanding work, soldier. Get some rest.", "normal"), ("", None),
                 ("YOUR WAR", "big"),
                 (f"RANK {self.rank}", "normal"),
                 (f"TOTAL KILLS {life.get('kills', 0)}   HEADSHOTS {life.get('heads', 0)}", "normal"),
                 (f"ROUNDS CLEARED {life.get('rounds', 0)}   BEST STREAK {life.get('streak', 0)}", "normal"),
                 (f"ACHIEVEMENTS {len(self.save.get('achievements', []))} / {len(ACHIEVEMENTS)}", "normal"),
                 ("", None), ("MADE WITH", "big"), ("Python + pygame", "normal"),
                 ("Every picture and sound is drawn in code", "normal"),
                 ("Game design and play testing: YOU", "normal"), ("Code: you and Claude", "normal"),
                 ("", None), ("THANK YOU FOR PLAYING", "big"), ("", None),
                 ("The war goes on: keep playing for higher rounds", "small")]
        return lines

    def draw_ending(self, screen):
        """엔딩: 화면이 어두워지고 글이 아래에서 위로 천천히 올라가요"""
        t = self.ending
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((6, 4, 16, int(min(235, t * 160))))
        screen.blit(dim, (0, 0))
        fonts = {"title": self.fonts["title"], "big": self.big_font, "normal": self.font, "small": self.small_font}
        y = HEIGHT - (t - 0.8) * 46 * UI
        for text, kind in self.ending_lines():
            if kind is None:
                y += 40 * UI
                continue
            font = fonts[kind]
            color = UI_ACCENT if kind in ("title", "big") else WHITE
            if -60 < y < HEIGHT + 60:
                self.center_text(screen, font, text, color, y)
            y += font.get_linesize() + 10 * UI
        if t > 2.0:
            draw_key_text(screen, self.small_font, [(kl(pygame.K_SPACE), "skip")], (WIDTH - 20, HEIGHT - 20), "bottomright")

    def mood(self):
        """맵 분위기 이름 (색 보정용)"""
        if self.theme.get("snow"):
            return "snow"
        if self.theme.get("rain"):
            return "rain"
        if self.night:
            return "night"
        if self.theme.get("ground") in (".", ";") or self.theme.get("sun") is not None:
            return "warm"
        return "default"

    def post_process(self, screen):
        """그래픽 품질 NORMAL: 맵 분위기 색 보정 / HIGH: + 밝은 곳이 은은하게 번지는 빛 (bloom)"""
        gfx = SETTINGS.get("gfx", 1)
        if gfx <= 0:
            return
        key = (WIDTH, HEIGHT, self.mood())
        if getattr(self, "grade_key", None) != key:
            self.grade_key = key
            mult, add = GRADES[key[2]]
            self.grade_mult = pygame.Surface((WIDTH, HEIGHT))
            self.grade_mult.fill(mult)
            self.grade_add = pygame.Surface((WIDTH, HEIGHT))
            self.grade_add.fill(add)
        if gfx >= 2:                                     # 빛 번짐: 작게 줄여 밝은 부분만 남기고 키워서 더해요
            small = pygame.transform.scale(screen, (WIDTH // 8, HEIGHT // 8))
            small.fill((150, 150, 150), special_flags=pygame.BLEND_SUB)
            glow = pygame.transform.smoothscale(small, (WIDTH // 4, HEIGHT // 4))
            screen.blit(pygame.transform.scale(glow, (WIDTH, HEIGHT)), (0, 0), special_flags=pygame.BLEND_ADD)
        screen.blit(self.grade_mult, (0, 0), special_flags=pygame.BLEND_MULT)
        screen.blit(self.grade_add, (0, 0), special_flags=pygame.BLEND_ADD)

    def draw_actor_extras(self, screen, box, actor, before):
        """사람(적·동료) 꾸미기: 발밑 그림자, 걸을 때 위아래 출렁임 / 총 쏠 때 총구 불빛"""
        sx, top, bottom, w, perp = box
        col = int(sx // self.col_w)
        visible = 0 <= col < self.num_rays and perp < self.zbuffer[col] + 0.2
        if before:
            if visible and perp < 25 and not getattr(actor, "t", {}).get("lift"):
                size = max(6, int(w * 0.9) // 4 * 4)                     # 4픽셀 단위로 (그림을 다시 써요)
                shadow = self.shadow_cache.get(size)
                if shadow is None:
                    shadow = pygame.Surface((size, max(3, size // 5)), pygame.SRCALPHA)
                    pygame.draw.ellipse(shadow, (0, 0, 0, 90), shadow.get_rect())
                    self.shadow_cache[size] = shadow
                screen.blit(shadow, shadow.get_rect(center=(sx, bottom - 1)))
            if getattr(actor, "moving", 0) > 0 and perp < 18:          # 걸음마다 살짝 출렁
                bob = abs(math.sin(actor.walk * math.pi / 0.32)) * (bottom - top) * 0.025
                return (sx, top - bob, bottom - bob, w, perp)
            return box
        if visible and perp < 9 and getattr(actor, "flash_timer", 0) > 0:   # 적 총구 불빛
            size = max(8, int(w * 1.6) // 8 * 8)
            glow = self.flash_glow_cache.get(size)
            if glow is None:
                glow = pygame.transform.smoothscale(self.glow_image, (size, size))
                self.flash_glow_cache[size] = glow
            screen.blit(glow, glow.get_rect(center=(sx + w * 0.22, top + (bottom - top) * 0.38)),
                        special_flags=pygame.BLEND_ADD)
        return box

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
        if getattr(self, "bar_key", None) != (col_w, HEIGHT):      # 그림자/불빛 막대 (크기가 바뀌면 다시)
            self.bar_key = (col_w, HEIGHT)
            self.shadow_bar = pygame.Surface((col_w, HEIGHT))
            self.shadow_bar.fill((150, 150, 155))
            self.light_bars = {}
        shadow_bar, light_bars = self.shadow_bar, self.light_bars
        depth_floor = SETTINGS.get("gfx", 1) >= 1 and FLOOR_DEPTH
        for i, (offset, fix) in enumerate(self.ray_table):
            # i번째 세로 줄이 바라보는 방향. 화면에 평평하게 펼쳐지도록 tan으로 계산해요
            floors, walls = cast_ray(px, py, angle + offset)
            x = i * col_w

            # 1) 바닥: 구간마다 색을 칠해요 (멀수록 지평선 가까이)
            for d0, d1, kind in floors:
                y_near = HEIGHT if d0 < 0.05 else horizon + eye * proj / (d0 * fix)
                y_far = horizon if d1 == math.inf else horizon + eye * proj / (max(d1, 0.01) * fix)
                if y_near > y_far and y_far < HEIGHT:
                    # 바닥은 벽보다 안개를 약하게 (바다가 회색으로 안 보이게)
                    base = FLOOR_DEPTH[kind][min(7, int(d0))] if depth_floor else FLOOR_COLORS[kind]
                    color = fog(base, (min(d1, fog_dist) + d0) * 0.3, fog_dist)
                    draw_rect(screen, color, (x, y_far, col_w, min(HEIGHT, y_near) - y_far + 1))
                if kind == "z" and self.trap_timer > 0 and y_near > y_far:      # 켜진 전기 함정: 파랗게 번쩍
                    glow = 140 + int(100 * abs(math.sin(self.time * 25)))
                    draw_rect(screen, (60, glow // 2, glow), (x, y_far, col_w, min(HEIGHT, y_near) - y_far + 1))
                if kind in INDOOR_FLOORS and d1 != math.inf:
                    # 천장: 바닥을 위아래로 뒤집은 모양 (실내 바닥 위에만)
                    c_near = 0.0 if d0 < 0.05 else horizon + (eye - CEILING) * proj / (d0 * fix)
                    c_far = horizon + (eye - CEILING) * proj / (max(d1, 0.01) * fix)
                    if c_far > max(0.0, c_near):
                        draw_rect(screen, fog(CEILING_COLOR, (d0 + d1) * 0.5, fog_dist),
                                  (x, max(0.0, c_near), col_w, c_far - max(0.0, c_near) + 1))

            # 2) 건물: 먼 것부터 그려야 가까운 것이 앞에 보여요
            zbuffer[i] = walls[0][0] * fix if walls else math.inf
            indoor = bool(floors) and floors[-1][2] in INDOOR_FLOORS     # 첫 벽 바로 앞이 실내 바닥
            if indoor and walls and walls[0][3][1] > CEILING:
                first = walls[0]
                spec = first[3]
                walls = [(first[0], first[1], first[2], (spec[0], CEILING, spec[2], None), first[4], first[5])]
            elif indoor:
                walls = walls[:1]                    # 천장 위로 보이는 먼 건물은 없어요
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
                if textured and perp < TEXTURE_DISTANCE and pattern != "box":     # 먼 벽은 안개에 묻혀서 단색으로
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
                    elif pattern == "box" and (wall_x < 0.08 or wall_x > 0.92 or 0.45 < wall_x < 0.55):
                        base = (230, 190, 70)                               # 미스터리 상자: 금색 테두리
                    elif pattern == "door" and 0.08 < wall_x < 0.14:      # 문 손잡이 쪽 어두운 줄
                        base = shade(base, 0.7)
                    elif pattern == "ribs" and (wall_x * 6) % 1 < 0.2:   # 컨테이너/창고의 세로 골
                        base = shade(base, 0.75)
                    draw_rect(screen, fog(base, perp, fog_dist), (x, top, col_w, vis_b - top + 1))
                if perp < 14:
                    # 벽 아래쪽 그림자 (땅과 닿는 곳이 어두워서 건물이 땅에 붙어 보여요)
                    # (색을 칠한 세로 막대 그림을 잘라 붙여요: 특수 효과 fill 보다 blit 이 훨씬 빨라요)
                    shadow_top = max(top, bottom - 0.12 * size)
                    if shadow_top < min(HEIGHT, vis_b):
                        blit(shadow_bar, (x, shadow_top), (0, 0, col_w, min(HEIGHT, vis_b) - shadow_top + 1),
                             special_flags=pygame.BLEND_MULT)
                    if light and perp < 5:      # 총구 불빛이 가까운 벽을 비춰요
                        k = int(self.muzzle_glow * (1 - perp / 5)) // 16 * 16
                        bar = light_bars.get(k)
                        if bar is None:
                            bar = light_bars[k] = pygame.Surface((col_w, HEIGHT))
                            bar.fill((k, int(k * 0.8), int(k * 0.5)))
                        blit(bar, (x, max(0, top)), (0, 0, col_w, min(HEIGHT, vis_b) - max(0, top)),
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
                if pattern == "weapon" and 0.2 < wall_x < 0.8:          # 벽 무기: 분필로 그린 총 모양
                    y0 = bottom - (0.78 if wall_x < 0.35 else 0.85) * size
                    y1 = bottom - 0.68 * size
                    if y1 < vis_b:
                        draw_rect(screen, fog((235, 225, 190), perp, fog_dist), (x, y0, col_w, max(1.0, y1 - y0)))
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
        piece = getattr(self, "setpiece", None)
        if piece and piece["kind"] == "convoy":
            box = self.project(piece["truck"]["pos"], 0.9, 1.4)
            if box:
                items.append((box, self.car_images[0], None))
        for dev in self.devices:
            height, width = DEVICE_SIZE[dev.kind]
            box = self.project(dev.pos, height, width)
            if box:
                ringing = dev.kind == "alarm" and dev.state in ("arming", "ringing") and pygame.time.get_ticks() // 200 % 2
                items.append((box, self.device_images["alarm_on" if ringing else dev.kind], None))
        t = pygame.time.get_ticks() / 1000
        for item in self.pickups:
            box = self.project(item.pos, 0.3, 0.4, lift=0.08 + math.sin(t * 3 + item.phase) * 0.05)
            if box:
                items.append((box, self.pickup_images[item.kind], None))
        for proj in self.projectiles:
            if proj.kind in ("grenade", "shell", "flash", "smoke"):
                img, h, w = self.grenade_image, 0.18, 0.15
            elif proj.kind == "tknife":
                img, h, w = self.knife_image, 0.08, 0.3
            else:
                img, h, w = self.rocket_image, 0.2, 0.35
            box = self.project(proj.pos, h, w, lift=proj.z)
            if box:
                items.append((box, img, None))
        for center, life in SMOKES:                       # 연막: 회색 연기 덩어리 여러 개
            fade = min(1.0, life / 1.5, (SMOKE_TIME - life + 0.3) / 1.0)
            img = self.smoke_images[max(0, min(3, int(fade * 4) - 1))]
            for k in range(6):
                spot = center + pygame.Vector2(0.9 if k else 0, 0).rotate(k * 60 + 15)
                box = self.project(spot, 1.7 * fade + 0.2, 1.9 * fade + 0.2)
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
        if self.chopper:
            box = self.project(self.chopper["pos"], 1.0, 2.4, lift=CHOPPER_LIFT)
            if box:
                items.append((box, self.chopper_images[1 if self.chopper["flash"] > 0 else 0], None))
        for turret in self.turrets:
            if turret is not self.mounted:
                box = self.project(turret["pos"], 0.75, 0.9)
                if box:
                    items.append((box, self.mg_image, None))
        for ally in self.allies:
            if ally.down:
                box = self.project(ally.pos, 0.3, 0.9)
                if box:
                    items.append((box, self.ally_images["down"], None))
                continue
            box = self.project(ally.pos, 0.9, 0.45)
            if box:
                prefix = "back_" if (self.player.pos - ally.pos).dot(ally.facing) < 0 else ""
                step = int(ally.walk / 0.32) % 4 if ally.moving > 0 else 0
                name = "flash" if ally.flash > 0 and not prefix else prefix + ("walk0", "", "walk1", "")[step]
                name = {"": "normal", "back_": "back"}.get(name, name)
                items.append((box, self.ally_images[name], ally))
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
            if enemy is not None:
                box = self.draw_actor_extras(screen, box, enemy, before=True)
            self.draw_sprite_columns(screen, img, *box)
            if enemy is not None:
                self.draw_actor_extras(screen, box, enemy, before=False)
            if isinstance(enemy, Ally):                    # 동료: 파란 이름표 (+ 말풍선)
                col = int(box[0] // self.col_w)
                if 0 <= col < self.num_rays and box[4] < self.zbuffer[col] + 0.3 and box[4] < 20:
                    tag = self.fonts["tiny"].render(enemy.name, True, (90, 170, 255))
                    screen.blit(tag, tag.get_rect(midbottom=(box[0], box[1] - 4 * UI)))
                    if enemy.callout:
                        label = self.fonts["tiny"].render(enemy.callout[0], True, BLACK)
                        bubble = label.get_rect(midbottom=(box[0], box[1] - 22 * UI)).inflate(10 * UI, 6 * UI)
                        bubble.clamp_ip(screen.get_rect().inflate(-6, -6))
                        pygame.draw.rect(screen, (200, 225, 255), bubble, border_radius=int(5 * UI))
                        screen.blit(label, label.get_rect(center=bubble.center))
                continue
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
                    bubble.clamp_ip(screen.get_rect().inflate(-6, -6))          # 화면 가장자리에서도 다 보이게
                    pygame.draw.rect(screen, WHITE, bubble, border_radius=int(5 * UI))
                    pygame.draw.polygon(screen, WHITE, [(box[0] - 4 * UI, bubble.bottom - 1), (box[0] + 4 * UI, bubble.bottom - 1),
                                                        (box[0], bubble.bottom + 6 * UI)])
                    screen.blit(label, label.get_rect(center=bubble.center))
            if isinstance(enemy, Enemy) and box[4] < 25 and "melee" not in enemy.t and enemy.kind != "TARGET" and (
                    (not enemy.sees and enemy.aware > 0.05) or enemy.alarm > 0 or enemy.stun > 0):
                col = int(box[0] // self.col_w)
                if 0 <= col < self.num_rays and box[4] < self.zbuffer[col] + 0.3:
                    if enemy.stun > 0:                       # 섬광탄에 멍함
                        mark, color = "*", WHITE
                    elif enemy.alarm > 0:                    # 들켰어요
                        mark, color = "!", RED
                    else:                                     # 알아채는 중: 노란 ? 가 점점 진해져요
                        k = enemy.aware
                        mark, color = "?", (255, int(255 - 120 * k), int(90 * (1 - k)))
                    label = self.big_font.render(mark, True, color)
                    label = pygame.transform.smoothscale(label, (max(4, int(label.get_width() * 0.6)), max(4, int(label.get_height() * 0.6))))
                    screen.blit(label, label.get_rect(midbottom=(box[0], box[1] - 16 * UI)))
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
            # 재장전: 무기 종류마다 다르게 (권총은 휙 기울이고, 기관총은 크게 내려요)
            lower, side, roll = RELOAD_STYLES.get(weapon_class(a.current.spec["name"]), (110, 50, 14))
            k = math.sin(min(1.0, prog * 1.15) * math.pi)
            down = lower * k + 30
            bx -= side * UI * math.sin(prog * math.pi)
            tilt += roll * k
        elif a.switch_left > 0:
            down = 220 * a.switch_left / a.SWITCH_TIME
        if self.bolt_anim > 0:                      # 노리쇠: 총을 살짝 내리고 오른쪽으로 비틀었다 돌아와요
            k = math.sin((1 - self.bolt_anim / 0.75) * math.pi)
            down += 45 * k
            bx += 25 * UI * k
        if self.ads_anim > 0:                       # 정조준 전환: 잠깐 내려갔다 올라와요
            down += 55 * math.sin(self.ads_anim / 0.16 * math.pi)
        if self.land_dip > 0:                       # 착지: 쿵
            down += 40 * math.sin(self.land_dip / 0.25 * math.pi)
        tilt += self.strafe_tilt * calm
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
        angle = int(round(tilt / 2)) * 2                            # 2도 단위로 (돌린 그림을 다시 써요)
        if angle:
            turned = self.tilt_cache.get((key, angle))
            if turned is None:
                if len(self.tilt_cache) > 48:
                    self.tilt_cache.clear()
                turned = pygame.transform.rotate(image, angle)
                self.tilt_cache[(key, angle)] = turned
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

    def draw_gear_line(self, screen, key, kind, count, color, bottomright):
        """오른쪽 아래 장비 한 줄: [키] 아이콘 x개 (오른쪽 끝 맞춤). 그린 범위를 돌려줘요"""
        font = self.small_font
        icon = make_icon(kind, font.get_linesize() * 0.95, color)
        count_img = font.render(count, True, color)
        cap_w = font.size(key)[0] + 12 * UI
        total = cap_w + 6 * UI + icon.get_width() + 4 * UI + count_img.get_width()
        area = pygame.Rect(0, 0, total, font.get_linesize() + 4 * UI)
        area.bottomright = bottomright
        x = draw_keycap(screen, font, key, area.x, area.centery) + 6 * UI
        screen.blit(icon, icon.get_rect(midleft=(x, area.centery)))
        screen.blit(count_img, count_img.get_rect(midleft=(x + icon.get_width() + 4 * UI, area.centery)))
        return area

    def hint_layout(self):
        """처음 몇 초 보이는 조작 안내: 양쪽 HUD 사이 빈 곳에 들어가게 줄을 나눠요.
        (줄들, 상자, 줄 높이) - 너무 좁으면 줄 없이"""
        tiny = self.fonts["tiny"]
        move = "".join(kl(k) for k in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d))
        items = [(move, "move"), (kl(pygame.K_LSHIFT), "sprint"), (kl(pygame.K_c), "crouch"), (kl(pygame.K_SPACE), "jump"),
                 ("ARROWS", "look"), (kl(pygame.K_f), "fire"), (kl(pygame.K_e), "aim"), (kl(pygame.K_r), "reload"),
                 (kl(pygame.K_g), "grenade"), (kl(pygame.K_v), "knife"), (kl(pygame.K_TAB), "weapons"), (kl(pygame.K_h), "help")]
        side = max(self.small_font.size("STREAK 0   next: AIRSTRIKE at 5")[0],
                   key_text_width(self.small_font, [(kl(pygame.K_n), "FLASHBANG x2")]), big_ammo_width(self)) + 40 * UI
        room = min(WIDTH * 0.42, WIDTH - 2 * side)
        lines, line = [], []
        for item in items:
            if line and key_text_width(tiny, line + [item]) > room - 16 * UI:
                lines.append(line)
                line = []
            line.append(item)
        lines.append(line)
        line_h = tiny.get_linesize() + 6 * UI
        if room < 120 * UI or len(lines) > 4:
            return [], pygame.Rect(0, HEIGHT, 0, 0), line_h
        box = pygame.Rect(0, 0, room, len(lines) * line_h + 10 * UI)
        box.midbottom = (WIDTH / 2, HEIGHT - 66 * UI)
        return lines, box, line_h

    def prompt_y(self):
        """'B: 사기' 같은 안내 높이 (조작 안내 상자가 보이면 그 위로)"""
        y = HEIGHT - PROMPT_Y * UI
        if self.hint_timer > 0 and not self.game_over:
            lines, box, _ = self.hint_layout()
            if lines:
                y = min(y, box.top - 18 * UI)
        return y

    def draw_weapon_strip(self, screen):
        """아래 가운데 무기 칸: 지금 무기와 앞뒤 2개씩만 (나머지는 개수로, Tab 꾹 = 전체 휠)"""
        weapons, index = self.arsenal.weapons, self.arsenal.index
        n = len(weapons)
        show = min(n, STRIP_SLOTS)
        start = max(0, min(index - show // 2, n - show))
        reserve = max(250 * UI, big_ammo_width(self) + 60 * UI)          # 양쪽 HUD 자리
        room = WIDTH - 2 * reserve
        slot_w = min((150 if n <= 3 else 104) * UI, room / show)
        while show > 1 and slot_w < 72 * UI:                                # 너무 좁으면 칸 수를 줄여요
            show -= 2 if show > 2 else 1
            start = max(0, min(index - show // 2, n - show))
            slot_w = min(104 * UI, room / show)
        left = WIDTH / 2 - slot_w * show / 2
        tiny = self.fonts["tiny"]
        top = HEIGHT - 42 * UI
        for j, i in enumerate(range(start, start + show)):
            weapon = weapons[i]
            rect = pygame.Rect(left + j * slot_w + 3, top, slot_w - 6, 28 * UI)
            selected = i == index
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 220, 90, 215) if selected else (10, 8, 24, 150))
            screen.blit(panel, rect)
            if not selected:
                pygame.draw.rect(screen, (90, 80, 120), rect, 1)
            key = weapon_key_label(i)
            color = (20, 16, 10) if selected else ((255, 200, 60) if weapon.upgraded else (225, 225, 235))
            icon = make_icon(weapon_class(weapon.spec["name"]), rect.h * 0.62, color)     # 무기 모양 그림
            screen.blit(icon, icon.get_rect(center=(rect.centerx + 6 * UI, rect.centery)))
            if key:
                label = tiny.render(key, True, color)
                screen.blit(label, label.get_rect(midleft=(rect.x + 5 * UI, rect.centery)))
            if weapon.upgraded:
                plus = tiny.render("+", True, color)
                screen.blit(plus, plus.get_rect(midright=(rect.right - 4 * UI, rect.centery)))
        mid = top + 14 * UI
        if start > 0:
            label = tiny.render(f"< {start}", True, (200, 200, 220))
            screen.blit(label, label.get_rect(midright=(left - 6, mid)))
        if start + show < n:
            label = tiny.render(f"{n - start - show} >", True, (200, 200, 220))
            screen.blit(label, label.get_rect(midleft=(left + slot_w * show + 6, mid)))
        caption = f"PERK: {self.perk}" if self.perk else ""
        if n > show:
            caption += ("     " if caption else "") + f"HOLD {kl(pygame.K_TAB)}: ALL WEAPONS"
        if caption:
            label = tiny.render(caption, True, (80, 240, 255))
            screen.blit(label, label.get_rect(center=(WIDTH / 2, top - 9 * UI)))

    def draw_wheel(self, screen):
        """무기 휠: 가진 무기를 타원으로 늘어놓고, 고른 칸을 크게 보여줘요"""
        weapons = self.arsenal.weapons
        n = len(weapons)
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((8, 6, 20, 150))
        screen.blit(dim, (0, 0))
        cx, cy = WIDTH / 2, HEIGHT * 0.48
        rx, ry = min(WIDTH * 0.36, HEIGHT * 0.62), HEIGHT * 0.34
        box_w, box_h = min(150 * UI, 2 * math.pi * rx / max(n, 1) * 0.86), 46 * UI
        tiny, small = self.fonts["tiny"], self.fonts["small"]
        for i, w in enumerate(weapons):
            ang = -math.pi / 2 + 2 * math.pi * i / n
            rect = pygame.Rect(0, 0, box_w, box_h)
            rect.center = (cx + rx * math.cos(ang), cy + ry * math.sin(ang))
            chosen = i == self.wheel["pick"]
            if chosen:
                rect.inflate_ip(14 * UI, 8 * UI)
            fill = (70, 40, 100) if chosen else ((40, 34, 60) if i == self.arsenal.index else (22, 18, 38))
            pygame.draw.rect(screen, fill, rect, border_radius=int(10 * UI))
            pygame.draw.rect(screen, (255, 80, 200) if chosen else (90, 80, 120), rect, 3 if chosen else 1,
                             border_radius=int(10 * UI))
            label = weapon_key_label(i)
            if label:
                image = tiny.render(label, True, YELLOW)
                screen.blit(image, (rect.x + 7 * UI, rect.y + 5 * UI))
            name = fit_text(small, w.spec["name"], rect.width - 30 * UI)
            image = small.render(name, True, WHITE if chosen else (200, 200, 220))
            screen.blit(image, image.get_rect(center=(rect.centerx + 6 * UI, rect.centery - 6 * UI)))
            ammo = tiny.render(f"{w.mag}/{w.reserve}", True, (150, 220, 255))
            screen.blit(ammo, ammo.get_rect(center=(rect.centerx + 6 * UI, rect.centery + 12 * UI)))
        pick = weapons[self.wheel["pick"]]
        self.center_text(screen, self.fonts["big"], pick.spec["name"], (255, 80, 200), cy - 14 * UI)
        info = WEAPON_INFO.get(pick.spec["name"], ("", ""))[1]
        if info:
            self.center_text(screen, small, fit_text(small, info, rx * 1.4), WHITE, cy + 26 * UI)
        self.center_text(screen, tiny, f"ARROWS / 1-9 0 pick     release {kl(pygame.K_TAB)} to equip", YELLOW, cy + 52 * UI)

    def draw_hud(self, screen):
        font, big_font = self.font, self.big_font
        if getattr(self, "ending", None) is not None:
            return                               # 엔딩 크레딧 동안은 HUD 없이
        if self.game_over:                       # 끝났으면 결과 카드만 (HUD 글자가 카드 뒤로 비치지 않게)
            self.draw_game_over(screen, big_font, font)
            return
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

        self.draw_popups(screen, font)

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
            text = name + (f"  {left:.0f}s" if left > 0 else "  READY")
            area = draw_key_text(screen, self.fonts["tiny"], [(kl(pygame.key.key_code(key.lower())), text)],
                                 (WIDTH - 16, y_skill), "topright", (120, 120, 130) if left > 0 else (80, 240, 255))
            y_skill += area.h + 2 * UI
        screen.blit(self.bottom_shade, (0, HEIGHT - self.bottom_shade.get_height()))
        # 왼쪽 아래: 킬스트릭 (받은 것 / 다음 것까지)
        y = HEIGHT - 104 * UI
        if self.streaks_ready:
            for name in reversed(self.streaks_ready):
                area = draw_key_text(screen, self.small_font, [(kl(pygame.K_x), name)], (24, y), "topleft", (80, 240, 255))
                icon = make_icon(name, area.h * 0.8, (80, 240, 255))
                screen.blit(icon, icon.get_rect(midleft=(area.right + 6 * UI, area.centery)))
                y -= 26 * UI
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
        screen.blit(big_font.render(f"+ {int(self.player.hp)}", True, hp_color), (24, HEIGHT - 74 * UI))
        bar = pygame.Rect(24, HEIGHT - 22 * UI, 170 * UI, 6 * UI)          # 체력 막대
        pygame.draw.rect(screen, (40, 40, 50), bar, border_radius=3)
        pygame.draw.rect(screen, hp_color, (bar.x, bar.y, bar.w * min(1.0, max(0.0, self.player.hp) / self.max_hp), bar.h),
                         border_radius=3)
        w = self.arsenal.current
        ammo = "RELOADING..." if self.arsenal.reload_left > 0 else f"{w.mag} / {w.reserve}"
        low = self.arsenal.reload_left <= 0 and w.mag <= max(1, w.spec["mag"] // 4)
        image = big_font.render(ammo, True, RED if low and pygame.time.get_ticks() // 300 % 2 else WHITE)
        rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, HEIGHT - 20 * UI)))
        name = w.spec["name"] + (" +" if w.upgraded else "")
        image = self.small_font.render(name, True, (200, 200, 220))
        rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 26, rect.top + 2)))
        rect = self.draw_gear_line(screen, kl(pygame.K_g), "GRENADE", f"x{self.arsenal.grenades}", YELLOW,
                                   (WIDTH - 26, rect.top - 2))
        if self.mode != "training":                       # 전술 장비는 그 위 줄에
            rect = self.draw_gear_line(screen, kl(pygame.K_n), self.tactical, f"x{self.tactical_left}",
                                       (150, 220, 255), (WIDTH - 26, rect.top))
        if self.cooking is not None:                     # 쿠킹: 남은 시간 막대
            left = max(0.0, GRENADE_FUSE - self.cooking)
            bar = pygame.Rect(WIDTH / 2 - 60 * UI, HEIGHT * 0.62, 120 * UI, 8 * UI)
            pygame.draw.rect(screen, (60, 30, 30), bar)
            pygame.draw.rect(screen, RED if left < 0.6 else YELLOW, (bar.x, bar.y, bar.w * left / GRENADE_FUSE, bar.h))
            self.center_text(screen, self.small_font, f"COOKING  {left:.1f}s", WHITE, bar.y - 10 * UI)
        if self.mounted:                                   # 기관총 열 막대
            bar = pygame.Rect(WIDTH / 2 - 80 * UI, HEIGHT * 0.7, 160 * UI, 9 * UI)
            pygame.draw.rect(screen, (40, 40, 50), bar)
            hot = self.arsenal.cooldown > 0.2 and self.mg_heat >= 0.99
            pygame.draw.rect(screen, RED if self.mg_heat > 0.75 or hot else (255, 170, 60),
                             (bar.x, bar.y, bar.w * self.mg_heat, bar.h))
            self.center_text(screen, self.small_font, "OVERHEATED" if hot else f"HEAT   ({kl(pygame.K_b)}: get off)", WHITE,
                             bar.y - 10 * UI)
        elif any(t["pos"].distance_to(self.player.pos) < 1.2 for t in self.turrets) and not self.game_over:
            draw_key_text(screen, font, [(kl(pygame.K_b), "MOUNT MACHINE GUN")], (WIDTH / 2, self.prompt_y()),
                          color=(255, 220, 90))
        if self.chopper:
            label = self.small_font.render(f"CHOPPER {self.chopper['time']:.0f}s", True, (80, 240, 255))
            screen.blit(label, (16, 12 + 90 * UI))
        item = self.nearby_buyable()
        if item and not self.game_over:
            key, text = kl(pygame.K_b), f"{item['name']}  ({self.price_of(item)} POINTS)"
            if item["kind"] == "weapon" and self.price_of(item) < item["cost"]:
                text = f"{item['weapon']} AMMO  ({self.price_of(item)} POINTS)"
            if item["kind"] == "trap" and self.trap_timer > 0:
                key, text = None, f"TRAP ACTIVE  {self.trap_timer:.0f}s"
            color = (255, 220, 90) if self.points >= self.price_of(item) else (200, 120, 120)
            draw_key_text(screen, font, [(key, text)], (WIDTH / 2, self.prompt_y()), color=color)
        if self.mode == "zombies":
            image = font.render(f"POINTS {self.points}", True, (255, 200, 60))
            rect = screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 4)))
            shop = [(kl(pygame.K_b), f"ammo {ZOMBIE_SHOP['ammo']}"), (kl(pygame.K_u), f"upgrade {ZOMBIE_SHOP['upgrade']}")]
            rect = draw_key_text(screen, self.fonts["tiny"], shop, (WIDTH - 24, rect.top - 2), "bottomright")
            best = top_score(self.save, "zombies")
            score = f"SCORE {self.run_score}" + (f"   #1 {best}" if best else "")
            color = (255, 200, 60) if self.run_score > best else WHITE      # 1등을 넘으면 금색
            image = self.fonts["tiny"].render(score, True, color)
            screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 2)))

        self.draw_weapon_strip(screen)

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
            label = self.small_font.render(f"{getattr(boss, 'name', 'BOSS')}   PHASE {getattr(boss, 'phase', 1)}", True, WHITE)
            screen.blit(label, label.get_rect(midbottom=(WIDTH / 2, bar.y - 1)))
        # 위쪽 정보
        if self.mode == "mission":
            t = int(self.mission_time)
            info = (f"MISSION {self.theme['name']}   STAGE {min(self.stage + 1, len(MISSION_STAGES))}/"
                    f"{len(MISSION_STAGES)}   ENEMIES {len(self.enemies)}   KILLS {self.kills}   {t // 60}:{t % 60:02d}")
        elif self.mode == "training":
            info = f"TRAINING RANGE   {self.theme['name']}   TARGETS {len(self.enemies)}"
        elif self.mode == "custom":
            info = f"CUSTOM  {self.theme['name']}   WAVE {self.round}   ENEMIES {len(self.enemies)}   KILLS {self.kills}"
        elif self.challenge:
            t = self.challenge_time if self.challenge != "BLITZ" else max(0.0, BLITZ_TIME - self.challenge_time)
            info = (f"CHALLENGE {self.challenge}   {self.theme['name']}   ENEMIES {len(self.enemies)}   "
                    f"{'LEFT ' if self.challenge == 'BLITZ' else 'TIME '}{int(t) // 60}:{int(t) % 60:02d}")
        elif self.mode == "zombies":
            info = (f"WAVE {self.round}   {self.theme['name']}   "
                    f"ZOMBIES {len(self.enemies) + self.zombies_left}   KILLS {self.kills}")
        elif self.deeprun:
            info = f"DEEP RUN   DEPTH {self.depth}   {self.theme['name']}   ENEMIES {len(self.enemies)}   KILLS {self.kills}"
        else:
            info = (f"ROUND {self.round}/{CAMPAIGN_ROUNDS}   SET {set_of(self.round)}   {self.theme['name']}   "
                    f"ENEMIES {len(self.enemies)}   KILLS {self.kills}")
        screen.blit(font.render(info, True, WHITE), (16, 12))
        # 계급과 경험치 막대
        rank_label = self.small_font.render(f"RANK {self.rank}", True, WHITE)
        screen.blit(rank_label, (16, 12 + 30 * UI))
        if self.flashlight:
            label = self.small_font.render("LIGHT ON", True, (255, 240, 170))
            screen.blit(label, (16, 12 + 70 * UI))
        if self.allies:
            parts = [f"SQUAD [{SQUAD_ORDERS[self.squad_order]}]"]
            parts += [f"{a.name} {'DOWN' if a.down else int(a.hp)}" for a in self.allies]
            label = self.small_font.render("   ".join(parts), True, (90, 170, 255))
            screen.blit(label, (16, 12 + 50 * UI))
        bar = pygame.Rect(16 + rank_label.get_width() + 10, 12 + 34 * UI, 140 * UI, 6 * UI)
        pygame.draw.rect(screen, (40, 40, 50), bar)
        bar.width = int(bar.width * (self.xp % XP_PER_RANK) / XP_PER_RANK)
        pygame.draw.rect(screen, (255, 80, 200), bar)
        if self.show_fps:
            d = self.director
            text = (f"FPS {self.fps:.0f}   RES {self.col_w}px   {WIDTH}x{HEIGHT}   "
                    f"DIRECTOR {d.phase.upper()} {d.intensity:.2f} ASSIST {d.assist:.2f}")
            screen.blit(self.small_font.render(text, True, YELLOW), (16, 12 + 54 * UI))
        map_bottom = self.draw_minimap(screen)
        for i, (text, _) in enumerate(self.feed[-4:]):
            image = font.render(text, True, YELLOW)
            screen.blit(image, image.get_rect(topright=(WIDTH - 12, map_bottom + 8 + i * 30 * UI)))

        if self.hint_timer > 0 and not self.game_over:
            hints, box, line_h = self.hint_layout()
            fade = min(1.0, self.hint_timer)                  # 마지막 1초 동안 흐려지며 사라져요
            if hints:
                panel = pygame.Surface(box.size, pygame.SRCALPHA)
                panel.fill((10, 8, 24, int(150 * fade)))
                screen.blit(panel, box)
            for i, parts in enumerate(hints):
                draw_key_text(screen, self.fonts["tiny"], parts, (WIDTH / 2, box.y + 5 * UI + (i + 0.5) * line_h),
                              alpha=int(255 * fade))
        self.draw_objective(screen)
        self.draw_contracts(screen)
        self.draw_setpiece(screen)
        alarm = next((d for d in self.devices if d.kind == "alarm" and d.state == "arming"), None)
        if alarm and not self.game_over:
            text = f"ALARM IN {alarm.timer:.0f}s  -  SHOOT THE YELLOW BOX"
            color = RED if pygame.time.get_ticks() // 300 % 2 else (255, 200, 60)      # 빨강/노랑 깜빡
            self.center_text(screen, self.small_font, text, color, 12 + 108 * UI + (22 * UI if self.setpiece else 0))
        if self.round_clear_timer > 0 and not self.game_over:
            self.draw_summary(screen, HEIGHT * 0.5)
        if self.banner_timer > 0:
            self.draw_banner(screen, big_font, font)
        self.over_start = None                  # 결과 카드가 다시 나올 때 처음부터 움직이게

    def game_over_text(self):
        """게임 오버 카드의 (제목, 색, 설명 줄, 누를 키들)"""
        r = kl(pygame.K_r)
        retry = [(r, "TRY AGAIN"), ("ESC", "MENU")]
        if self.mission_complete:
            t = int(self.mission_time)
            return ("MISSION COMPLETE", UI_CYAN, f"{self.theme['name']}   TIME {t // 60}:{t % 60:02d}   KILLS {self.kills}",
                    [(r, "PLAY AGAIN"), ("ESC", "MENU")])
        if self.challenge_done:
            return ("CHALLENGE COMPLETE", UI_CYAN,
                    f"{self.challenge}   TIME {self.challenge_time:.1f}s   BEST {self.challenge_best:.1f}s", retry)
        if self.challenge:
            return (self.fail_reason or "CHALLENGE FAILED", RED, f"{self.challenge}   KILLS {self.kills}", retry)
        if self.mode == "custom":
            return ("YOU DIED", RED, f"{self.theme['name']}   WAVE {self.round}   KILLS {self.kills}", retry)
        if self.mode == "mission":
            return (self.fail_reason or "YOU DIED", RED, f"STAGE {self.stage + 1}   KILLS {self.kills}",
                    [(r, "BACK TO CHECKPOINT"), ("ESC", "MENU")])
        if self.mode == "zombies":
            return ("YOU DIED", RED, f"WAVE {self.round}   KILLS {self.kills}   BEST WAVE {self.save.get('zbest', self.round)}",
                    retry)
        return (self.fail_reason or "YOU DIED", RED, f"ROUND {self.round}   KILLS {self.kills}",
                [(r, f"RETRY ROUND {self.round}"), (kl(pygame.K_n), "NEW GAME"), ("ESC", "MENU")])

    def draw_tiles(self, screen, items, rect):
        """작은 칸 여러 개에 (이름, 값)을 나란히: 명중률, 헤드샷..."""
        gap = 8 * UI
        w = (rect.w - gap * (len(items) - 1)) / len(items)
        for i, (name, value) in enumerate(items):
            tile = pygame.Rect(rect.x + i * (w + gap), rect.y, w, rect.h)
            draw_panel(screen, tile, False, radius=6)
            label = self.fonts["tiny"].render(fit_text(self.fonts["tiny"], name, tile.w - 8 * UI), True, UI_DIM)
            screen.blit(label, label.get_rect(midtop=(tile.centerx, tile.y + 6 * UI)))
            text = fit_text(self.small_font, str(value), tile.w - 10 * UI)
            image = self.small_font.render(text, True, WHITE)
            screen.blit(image, image.get_rect(midbottom=(tile.centerx, tile.bottom - 6 * UI)))

    def summary_items(self):
        st = self.stats
        accuracy = round(100 * st["hits"] / st["shots"]) if st["shots"] else 0
        top = max(st["weapons"], key=st["weapons"].get) if st["weapons"] else "-"
        return [("ACCURACY", f"{accuracy}%"), ("HEADSHOTS", st["heads"]), ("KILLS", st["kills"]),
                ("BEST STREAK", st["best"]), ("TOP WEAPON", top)]

    def draw_game_over(self, screen, big_font, font):
        """게임 오버 / 완료 카드: 제목, 설명, 점수(숫자가 올라가요)와 랭킹, 이번 라운드 기록, 누를 키"""
        if getattr(self, "over_start", None) is None:
            self.over_start = time.time()
        age = time.time() - self.over_start
        show = min(1.0, age / 0.3)
        title, color, sub, actions = self.game_over_text()
        dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        dim.fill((5, 4, 12, int(120 * show)))
        screen.blit(dim, (0, 0))
        recorded = getattr(self, "run_recorded", False)
        need = (46 + 46 + 62 + (74 if recorded else 10) + 12 + 52 + 30 + 60) * UI      # 안에 들어갈 것들의 높이
        card = pygame.Rect(0, 0, min(WIDTH * 0.62, 760 * UI), max(HEIGHT * 0.62, min(need, HEIGHT * 0.96)))
        card.center = (WIDTH / 2, HEIGHT * 0.47 + (1 - show) * 30 * UI)
        back = pygame.Surface(card.size, pygame.SRCALPHA)
        pygame.draw.rect(back, (14, 10, 30, int(230 * show)), back.get_rect(), border_radius=int(14 * UI))
        screen.blit(back, card)
        pygame.draw.rect(screen, color, (card.x, card.y, card.w, 4 * UI), border_top_left_radius=int(14 * UI),
                         border_top_right_radius=int(14 * UI))
        y = card.y + 46 * UI
        self.center_text(screen, big_font, title, color, y)
        y += 46 * UI
        self.center_text(screen, font, fit_text(font, sub, card.w - 40 * UI), WHITE, y)
        y += 62 * UI
        if getattr(self, "run_recorded", False):                       # 점수: 1초 동안 0부터 올라가요
            shown = int(self.run_score * min(1.0, age / 1.0))
            self.center_text(screen, big_font, f"{shown}", (255, 200, 60), y)
            label = self.fonts["tiny"].render("SCORE", True, UI_DIM)
            screen.blit(label, label.get_rect(center=(WIDTH / 2, y - 30 * UI)))
            y += 40 * UI
            if age > 1.0:
                if self.run_place:
                    pop = 1 + 0.3 * max(0.0, 1 - (age - 1.0) / 0.2)
                    badge = self.small_font.render(f"NEW RECORD!  #{self.run_place}", True, BLACK)
                    pill = pygame.Rect(0, 0, (badge.get_width() + 30 * UI) * pop, (badge.get_height() + 10 * UI) * pop)
                    pill.center = (WIDTH / 2, y)
                    pygame.draw.rect(screen, (255, 200, 60), pill, border_radius=int(pill.h / 2))
                    screen.blit(badge, badge.get_rect(center=pill.center))
                else:
                    best = top_score(self.save, self.mode)
                    self.center_text(screen, self.small_font, f"#1 SCORE {best}" if best else "", UI_DIM, y)
            y += 34 * UI
        else:
            y += 10 * UI
        label = self.fonts["tiny"].render("THIS ROUND", True, UI_DIM)
        screen.blit(label, label.get_rect(midleft=(card.x + 24 * UI, y)))
        tiles = pygame.Rect(card.x + 24 * UI, y + 12 * UI, card.w - 48 * UI, 52 * UI)
        self.draw_tiles(screen, self.summary_items(), tiles)
        # 누를 키 (키 모양 상자)
        tiny = self.small_font
        widths = [tiny.size(k)[0] + 12 * UI + 8 * UI + tiny.size(t)[0] for k, t in actions]
        x = WIDTH / 2 - (sum(widths) + 28 * UI * (len(actions) - 1)) / 2
        cy = card.bottom - 30 * UI
        for (key, text), w in zip(actions, widths):
            x = draw_keycap(screen, tiny, key, x, cy) + 8 * UI
            image = tiny.render(text, True, WHITE)
            screen.blit(image, image.get_rect(midleft=(x, cy)))
            x += image.get_width() + 28 * UI

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
        spot = label.get_rect(midtop=(x, y + size + 3))
        spot.clamp_ip(screen.get_rect().inflate(-8, -8))
        screen.blit(label, spot)
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
        """라운드 결과: 명중률, 헤드샷, 처치, 최고 연속 처치, 가장 많이 쓴 무기 (작은 칸 5개)"""
        rect = pygame.Rect(0, 0, min(WIDTH * 0.62, 760 * UI), 52 * UI)
        rect.center = (WIDTH / 2, y)
        self.draw_tiles(screen, self.summary_items(), rect)

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
        for turret in self.turrets:                          # 노란 네모: 고정 기관총
            pygame.draw.rect(screen, (255, 210, 60), (*(turret["pos"] * cell + (ox - 2, oy - 2)), 5, 5))
        for ally in self.allies:                             # 파란 점: 동료
            pygame.draw.circle(screen, (60, 120, 200) if ally.down else (90, 170, 255),
                               ally.pos * cell + (ox, oy), max(2, cell // 2))
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
        full = SETTINGS.get("fullscreen") or not fits_desktop(WIDTH, HEIGHT)   # 설정이 켜져 있거나 모니터보다 크면
        flags = pygame.SCALED | (pygame.FULLSCREEN if full else 0)
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
    ("fullscreen", "FULLSCREEN", "전체 화면 (게임 중 Enter 로도)", "Fullscreen (Enter in game too)"),
    ("squad", "SQUADMATES", "같이 싸우는 AI 동료 수 0~2 (다음 판부터, K 로 명령)", "AI squadmates 0-2 (next game, K = orders)"),
    ("hud", "UI SIZE", "글자와 화면 표시 크기 (다음 판부터)", "Text and HUD size (next game)"),
    ("shake", "SCREEN SHAKE", "쏘거나 맞을 때 화면 흔들림", "Camera shake when shooting or hit"),
    ("soundviz", "SOUND MARKS", "발소리·총소리 방향을 조준점 둘레에 표시", "Show footstep/gunshot directions"),
    ("colorblind", "COLORBLIND", "빨강/초록 대신 주황/파랑", "Orange/blue instead of red/green"),
    ("lang", "LANGUAGE", "메뉴 글자: 한국어 / 영어", "Menu language: Korean / English"),
    ("gfx", "GRAPHICS", "LOW 가장 빠르게 / NORMAL 색감 / HIGH 색감 + 빛 번짐", "LOW fastest / NORMAL color grade / HIGH + bloom"),
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
    elif key == "squad":
        SETTINGS[key] = (SETTINGS[key] + step) % 3
    elif key in ("shake", "soundviz", "colorblind"):
        SETTINGS[key] = 1 - SETTINGS[key]
    elif key == "fullscreen" and not IN_BROWSER:
        SETTINGS[key] = 1 - SETTINGS[key]
        open_window()                                   # 바로 전체 화면 / 창으로
    elif key == "difficulty":
        SETTINGS[key] = (SETTINGS[key] + step) % len(DIFFICULTIES)
    elif key == "lang":
        SETTINGS[key] = 1 - SETTINGS[key]
    elif key == "gfx":
        SETTINGS[key] = (SETTINGS.get(key, 1) + step) % len(GFX_NAMES)
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
    if key == "fullscreen":
        return "BROWSER" if IN_BROWSER else ("ON" if value else "OFF")
    if key == "squad":
        return str(value)
    if key == "gfx":
        return GFX_NAMES[value]
    if key == "lang":
        if value == 1:
            return "ENGLISH"
        return "KOREAN" if korean_font_path() else "KOREAN (NO FONT)"
    return f"{value}%"


# 설정 화면 탭: (탭 이름, 그 탭의 설정 키들). 새 설정을 만들면 여기 한 곳에 꼭 넣어요
SETTING_TABS = [("DISPLAY", ("fullscreen", "gfx", "fov", "hud", "shake", "colorblind", "lang")),
                ("SOUND", ("volume", "music", "soundviz")),
                ("INPUT", ("look", "mouse", "assist", "controls")),
                ("GAME", ("difficulty", "squad"))]


def draw_setting_preview(screen, fonts, key, rect):
    """고른 설정의 미리보기 (글자 크기, 색약 색, 시야각...)"""
    if key == "hud":                                             # 이 크기로 HUD 글자가 보여요
        size = SETTINGS["hud"] / 100
        font = pygame.font.Font(None, int(56 * HEIGHT / 600 * size))
        image = font.render("30 / 120", True, WHITE)
        screen.blit(image, image.get_rect(midright=(rect.right - 20 * UI, rect.centery)))
    elif key == "colorblind":                                    # 적 조준 / 체력 색
        for i, color in enumerate((RED, GREEN)):
            pygame.draw.circle(screen, color, (rect.right - (60 - i * 34) * UI, rect.centery), 12 * UI)
    elif key == "fov":                                           # 시야각 부채꼴
        cx, cy, r = rect.right - 70 * UI, rect.bottom - 10 * UI, rect.h * 0.75
        half = math.radians(SETTINGS["fov"] / 2)
        points = [(cx, cy)] + [(cx + r * math.sin(a), cy - r * math.cos(a))
                               for a in (-half + k * half / 6 for k in range(13))]
        pygame.draw.polygon(screen, (80, 240, 255), points, 2)
    elif key in ("volume", "music"):                             # 소리 막대
        bar = pygame.Rect(rect.right - 170 * UI, rect.centery - 6 * UI, 150 * UI, 12 * UI)
        pygame.draw.rect(screen, (45, 40, 70), bar, border_radius=4)
        pygame.draw.rect(screen, UI_CYAN, (bar.x, bar.y, bar.w * SETTINGS[key] / 100, bar.h), border_radius=4)


async def settings_screen(save):
    """설정: 탭(화면 / 소리 / 조작 / 게임). Tab 또는 1~4 탭 바꾸기, ↑↓ 고르기, ←→ 바꾸기, Enter/ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    rows_by_key = {row[0]: row for row in SETTING_ROWS}
    tab, row = 0, 0
    while True:
        clock.tick(30)
        keys = SETTING_TABS[tab][1]
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            key = keys[row]
            if key == "controls" and event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_RIGHT, pygame.K_d):
                if await controls_screen(save) == "closed":
                    return "closed"
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_s):
                save["settings"] = dict(SETTINGS)
                write_save(save)
                return None
            if event.key == pygame.K_TAB or pygame.K_1 <= event.key <= pygame.K_1 + len(SETTING_TABS) - 1:
                tab = (tab + 1) % len(SETTING_TABS) if event.key == pygame.K_TAB else event.key - pygame.K_1
                row = 0
                keys = SETTING_TABS[tab][1]
            elif event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(keys)
            elif event.key in (pygame.K_DOWN,):
                row = (row + 1) % len(keys)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                change_setting(key, -1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                change_setting(key, 1)
            if key == "lang" and event.key in (pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d):
                fonts = make_fonts()                       # 언어를 바꾸면 글꼴도 바로
                ko = fonts["lang"] == "ko"
            screen = pygame.display.get_surface()       # 전체 화면을 바꾸면 새 화면
        draw_backdrop(screen)
        draw_title(screen, fonts, "SETTINGS", (WIDTH * 0.06, HEIGHT * 0.08))
        # 탭
        tab_w = WIDTH * 0.2
        for i, (name, _) in enumerate(SETTING_TABS):
            rect = pygame.Rect(WIDTH * 0.06 + i * (tab_w + WIDTH * 0.0133), HEIGHT * 0.15, tab_w, HEIGHT * 0.065)
            draw_panel(screen, rect, i == tab)
            label = fonts["normal"].render(tr(fonts, name), True, WHITE if i == tab else UI_DIM)
            screen.blit(label, label.get_rect(center=(rect.centerx + 8 * UI, rect.centery)))
            num = fonts["tiny"].render(str(i + 1), True, YELLOW)
            screen.blit(num, num.get_rect(midleft=(rect.x + 10 * UI, rect.centery)))
        # 고른 탭의 설정들
        step = HEIGHT * min(0.075, 0.5 / max(len(k) for _, k in SETTING_TABS))
        for i, key in enumerate(keys):
            _, name, desc_ko, desc_en = rows_by_key[key]
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * 0.25 + i * step, WIDTH * 0.88, step * 0.86)
            selected = i == row
            draw_panel(screen, rect, selected)
            label = fonts["normal"].render(tr(fonts, name), True, YELLOW if selected else WHITE)
            screen.blit(label, label.get_rect(midleft=(rect.x + 16 * UI, rect.centery)))
            value = setting_text(key)
            image = fonts["normal"].render(f"<  {value}  >" if selected else value, True, YELLOW if selected else WHITE)
            screen.blit(image, image.get_rect(midright=(rect.right - 16 * UI, rect.centery)))
        # 아래: 고른 설정 설명 + 미리보기
        key = keys[row]
        _, name, desc_ko, desc_en = rows_by_key[key]
        most = max(len(k) for _, k in SETTING_TABS)              # 가장 긴 탭 아래에 설명 칸
        box = pygame.Rect(WIDTH * 0.06, HEIGHT * 0.25 + most * step + HEIGHT * 0.01, WIDTH * 0.88,
                          HEIGHT - 44 * UI - (HEIGHT * 0.26 + most * step) - HEIGHT * 0.01)
        draw_panel(screen, box, False)
        desc = fit_text(fonts["help"], desc_ko if ko else desc_en, box.w * 0.62)
        screen.blit(fonts["help"].render(desc, True, (200, 230, 255)),
                    fonts["help"].render(desc, True, WHITE).get_rect(midleft=(box.x + 16 * UI, box.centery)))
        draw_setting_preview(screen, fonts, key, box)
        hint = ("Tab / 1~4 탭     ↑↓ 고르기     ←→ 바꾸기     Enter / ESC 저장하고 돌아가기" if ko
                else "TAB / 1-4 tabs     UP/DOWN choose     LEFT/RIGHT change     ENTER / ESC save and back")
        draw_hint_bar(screen, fonts, hint)
        present("settings_screen")
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
        draw_backdrop(screen)
        draw_title(screen, fonts, "CONTROLS", (WIDTH * 0.06, HEIGHT * 0.08))
        for i, (name, default, desc) in enumerate(KEY_ACTIONS):
            col, line = divmod(i, half)
            step = min(0.066, 0.7 / half)                     # 키가 늘어도 아래 안내 줄 위까지
            rect = pygame.Rect(WIDTH * (0.05 + col * 0.46), HEIGHT * (0.15 + line * step), WIDTH * 0.44, HEIGHT * step * 0.88)
            selected = i == row
            draw_panel(screen, rect, selected, radius=6)
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
        draw_hint_bar(screen, fonts, hint)
        present("controls_screen")
        await asyncio.sleep(0)


# ----- 맵 만들기 (에디터) -----
EDIT_W, EDIT_H, MAP_SLOTS = 26, 18, 5
# 붓: (글자, 한국어, 영어). 바닥 / 벽·건물 / 물건 순서
BRUSHES = [(".", "모래", "sand"), (":", "인도", "sidewalk"), ("=", "도로", "road"), ("g", "잔디", "grass"),
           (",", "콘크리트", "concrete"), ("*", "눈", "snow"), ("w", "실내 바닥(천장)", "indoor floor"),
           ("R", "벽돌 건물", "brick building"), ("M", "낮은 건물", "low building"), ("S", "고층 빌딩", "tower"),
           ("W", "창고", "warehouse"), ("i", "실내 벽", "indoor wall"), ("d", "문", "door"),
           ("K", "나무 상자(부서짐)", "crate"), ("Z", "모래주머니(부서짐)", "sandbags"), ("V", "돌담", "stone wall"),
           ("~", "물", "water"), ("P", "시작 위치", "player start"), ("E", "적", "enemy"), ("T", "야자수", "palm"),
           ("I", "소나무", "pine"), ("c", "자동차", "car"), ("L", "가로등", "street lamp"),
           ("a", "탄약 상자", "ammo"), ("h", "구급 상자", "health"), ("n", "수류탄 상자", "grenades")]
EDIT_COLORS = {"P": (80, 255, 120), "E": (255, 70, 70), "T": (60, 150, 60), "I": (40, 110, 60), "c": (200, 60, 60),
               "L": (250, 230, 150), "a": (230, 200, 60), "h": (240, 240, 240), "n": (90, 120, 70)}


def blank_map():
    """새 맵: 잔디 테두리 안에 인도, 아래 가운데 시작 위치, 위쪽에 적 몇 명"""
    rows = []
    for r in range(EDIT_H):
        rows.append("".join("g" if r in (0, EDIT_H - 1) or c in (0, EDIT_W - 1) else ":" for c in range(EDIT_W)))
    rows = [list(row) for row in rows]
    rows[EDIT_H - 3][EDIT_W // 2] = "P"
    for c in (4, 12, 21):
        rows[2][c] = "E"
    return ["".join(row) for row in rows]


def validate_map(rows):
    """만든 맵 검사: 문제 목록 (한국어, 영어). 비어 있으면 플레이할 수 있어요."""
    problems = []
    cells = [(c, r, ch) for r, row in enumerate(rows) for c, ch in enumerate(row)]
    starts = [(c, r) for c, r, ch in cells if ch == "P"]
    enemies = [(c, r) for c, r, ch in cells if ch == "E"]
    if len(starts) != 1:
        problems.append((f"시작 위치(P)가 {len(starts)}개예요. 딱 1개여야 해요", f"Need exactly 1 start (P), found {len(starts)}"))
    if len(enemies) < 3:
        problems.append((f"적(E)이 {len(enemies)}명이에요. 3명 이상 놓아 주세요", f"Place at least 3 enemies (E), found {len(enemies)}"))
    if len(starts) == 1:
        blockers = (set(WALLS) | set("~TcIv")) - set(DOORS)
        start = starts[0]
        seen, queue = {start}, deque([start])
        while queue:
            c, r = queue.popleft()
            for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                q = (c + dc, r + dr)
                if 0 <= q[0] < len(rows[0]) and 0 <= q[1] < len(rows) and q not in seen and rows[q[1]][q[0]] not in blockers:
                    seen.add(q)
                    queue.append(q)
        stuck = [e for e in enemies if e not in seen]
        if stuck:
            problems.append((f"갈 수 없는 곳에 적이 {len(stuck)}명 있어요 (벽에 갇힘)", f"{len(stuck)} enemies are walled off"))
        close = [e for e in enemies if math.dist(e, start) < 5]
        if close:
            problems.append((f"시작 위치에 너무 가까운 적이 {len(close)}명 (5칸 이상 떨어뜨려요)", f"{len(close)} enemies within 5 tiles of start"))
    return problems


async def map_slots_screen(save):
    """내 맵 5칸: ↑↓ 고르기, Enter 만들기/고치기, P 플레이, Backspace 지우기, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    slots = (save.get("custom_maps") or []) + [None] * MAP_SLOTS
    save["custom_maps"] = slots = slots[:MAP_SLOTS]
    row, message, confirm = 0, "", False
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if confirm:
                if event.key == pygame.K_y:
                    slots[row] = None
                    write_save(save)
                    message = "지웠어요" if ko else "Deleted"
                confirm = False
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % MAP_SLOTS
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % MAP_SLOTS
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                if slots[row] is None:
                    slots[row] = dict(name=f"MY MAP {row + 1}", rows=blank_map())
                result = await map_editor(save, slots[row])
                if result == "closed":
                    return "closed"
                if result == "play":
                    return dict(mode="custom", round=1, custom_map=dict(slots[row]))
            elif event.key == pygame.K_p and slots[row]:
                problems = validate_map(slots[row]["rows"])
                if problems:
                    message = problems[0][0 if ko else 1]
                else:
                    return dict(mode="custom", round=1, custom_map=dict(slots[row]))
            elif event.key == pygame.K_BACKSPACE and slots[row]:
                confirm = True
                message = "정말 지울까요? Y = 예" if ko else "Delete this map? Y = yes"
        draw_backdrop(screen)
        draw_title(screen, fonts, "MY MAPS", (WIDTH * 0.06, HEIGHT * 0.09))
        for i, slot in enumerate(slots):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.2 + i * 0.13), WIDTH * 0.88, HEIGHT * 0.11)
            selected = i == row
            draw_panel(screen, rect, selected)
            if slot:
                problems = validate_map(slot["rows"])
                status = ("플레이 가능" if ko else "READY") if not problems else ("고칠 곳 있음" if ko else "NEEDS FIXES")
                label = fonts["normal"].render(slot["name"], True, WHITE)
                screen.blit(label, (rect.x + 16, rect.y + rect.h * 0.15))
                screen.blit(fonts["help"].render(status, True, (80, 255, 120) if not problems else (255, 160, 90)),
                            (rect.x + 16, rect.y + rect.h * 0.6))
                # 작은 미리보기
                cell = max(1, int(rect.h * 0.8 / EDIT_H))
                ox, oy = rect.right - EDIT_W * cell - 16, rect.y + (rect.h - EDIT_H * cell) / 2
                for r, line in enumerate(slot["rows"]):
                    for c, ch in enumerate(line):
                        pygame.draw.rect(screen, edit_color(ch), (ox + c * cell, oy + r * cell, cell, cell))
            else:
                screen.blit(fonts["normal"].render("(EMPTY)  -  Enter: NEW MAP", True, (140, 140, 160)),
                            (rect.x + 16, rect.y + rect.h * 0.3))
        if message:
            image = fonts["help"].render(message, True, (80, 255, 120))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.88)))
        hint = ("↑↓ 고르기   Enter 만들기/고치기   P 플레이   Backspace 지우기   ESC 돌아가기" if ko
                else "UP/DOWN choose   ENTER edit   P play   BACKSPACE delete   ESC back")
        draw_hint_bar(screen, fonts, hint)
        present("map_slots_screen")
        await asyncio.sleep(0)


def edit_color(ch):
    if ch in EDIT_COLORS:
        return EDIT_COLORS[ch]
    if ch in WALLS:
        return WALLS[ch][0]
    if ch in FLOORS:
        return FLOORS[ch]
    return (60, 60, 60)


async def map_editor(save, slot):
    """맵 그리기: 화살표 커서, 스페이스 칠하기 (누른 채 움직이면 계속), Tab/Q 붓 바꾸기, X 지우기,
    C 검사, Enter 저장하고 플레이, ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    rows = [list(line) for line in slot["rows"]]
    cx, cy, brush = EDIT_W // 2, EDIT_H // 2, 7
    message = ""
    cell = int(min(WIDTH * 0.62 / EDIT_W, HEIGHT * 0.8 / EDIT_H))
    ox, oy = int(WIDTH * 0.03), int(HEIGHT * 0.12)

    def paint(letter):
        if letter == "P":                                 # 시작 위치는 하나만
            for line in rows:
                for k, ch in enumerate(line):
                    if ch == "P":
                        line[k] = ":"
        rows[cy][cx] = letter

    def store():
        slot["rows"] = ["".join(line) for line in rows]
        write_save(save)

    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                store()
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key
            if key == pygame.K_ESCAPE:
                store()
                return None
            moved = {pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0), pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1),
                     pygame.K_a: (-1, 0), pygame.K_d: (1, 0), pygame.K_w: (0, -1), pygame.K_s: (0, 1)}.get(key)
            if moved:
                cx = max(0, min(EDIT_W - 1, cx + moved[0]))
                cy = max(0, min(EDIT_H - 1, cy + moved[1]))
                if pygame.key.get_pressed()[pygame.K_SPACE]:     # 스페이스를 누른 채 움직이면 계속 칠해요
                    paint(BRUSHES[brush][0])
            elif key == pygame.K_SPACE:
                paint(BRUSHES[brush][0])
            elif key == pygame.K_x:
                rows[cy][cx] = ":"
            elif key == pygame.K_TAB:
                brush = (brush + 1) % len(BRUSHES)
            elif key == pygame.K_q:
                brush = (brush - 1) % len(BRUSHES)
            elif key == pygame.K_c:
                problems = validate_map(["".join(line) for line in rows])
                message = problems[0][0 if ko else 1] if problems else ("문제 없어요! Enter 로 플레이" if ko else "Looks good! ENTER to play")
            elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                store()
                problems = validate_map(slot["rows"])
                if problems:
                    message = problems[0][0 if ko else 1]
                else:
                    return "play"
        draw_backdrop(screen)
        title = fonts["normal"].render(f"MAP EDITOR  -  {slot['name']}", True, (255, 80, 200))
        screen.blit(title, (ox, HEIGHT * 0.04))
        for r, line in enumerate(rows):
            for c, ch in enumerate(line):
                rect = pygame.Rect(ox + c * cell, oy + r * cell, cell - 1, cell - 1)
                pygame.draw.rect(screen, edit_color(ch), rect)
                if ch in EDIT_COLORS:                     # 물건은 글자도
                    label = fonts["tiny"].render(ch, True, BLACK)
                    screen.blit(label, label.get_rect(center=rect.center))
        cursor = pygame.Rect(ox + cx * cell - 2, oy + cy * cell - 2, cell + 3, cell + 3)
        pygame.draw.rect(screen, YELLOW if pygame.time.get_ticks() // 300 % 2 else WHITE, cursor, 2)
        # 오른쪽: 붓 목록
        px = ox + EDIT_W * cell + int(WIDTH * 0.02)
        screen.blit(fonts["small"].render("BRUSH (TAB / Q)", True, WHITE), (px, oy))
        for i, (letter, name_ko, name_en) in enumerate(BRUSHES):
            y = oy + 24 * UI + i * 17 * UI
            selected = i == brush
            pygame.draw.rect(screen, edit_color(letter), (px, y + 2, 14 * UI, 12 * UI))
            text = f"{letter}  {name_ko if ko else name_en}"
            font = fonts["help"] if ko else fonts["tiny"]
            screen.blit(font.render(("> " if selected else "  ") + text, True, YELLOW if selected else (200, 200, 220)),
                        (px + 18 * UI, y))
        if message:
            image = fonts["help"].render(message, True, (80, 255, 120))
            screen.blit(image, (ox, oy + EDIT_H * cell + 8))
        hint = ("화살표 이동  스페이스 칠하기(누른 채 움직이면 계속)  X 지우기  C 검사  Enter 저장+플레이  ESC 저장+돌아가기" if ko
                else "ARROWS move  SPACE paint (hold to draw)  X erase  C check  ENTER save+play  ESC save+back")
        draw_hint_bar(screen, fonts, hint)
        present("map_editor")
        await asyncio.sleep(0)


async def ranking_screen(save, mode_index=0):
    """랭킹 화면 (내 컴퓨터): ←→ 모드 바꾸기, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_l):
                return None
            if event.key in (pygame.K_LEFT, pygame.K_a):
                mode_index = (mode_index - 1) % len(RANK_MODES)
            elif event.key in (pygame.K_RIGHT, pygame.K_d, pygame.K_TAB):
                mode_index = (mode_index + 1) % len(RANK_MODES)
        mode, title, reached_name = RANK_MODES[mode_index]
        draw_backdrop(screen)
        draw_title(screen, fonts, "LEADERBOARD", (WIDTH * 0.06, HEIGHT * 0.09))
        # 위쪽 모드 칸
        for i, (_, name, _) in enumerate(RANK_MODES):
            rect = pygame.Rect(WIDTH * (0.06 + i * 0.2), HEIGHT * 0.17, WIDTH * 0.18, HEIGHT * 0.06)
            selected = i == mode_index
            draw_panel(screen, rect, selected)
            image = fonts["normal"].render(tr(fonts, name), True, WHITE if selected else (150, 150, 170))
            screen.blit(image, image.get_rect(center=rect.center))
        # 표 머리
        cols = [0.06, 0.12, 0.26, 0.38, 0.48, 0.74]
        heads = ["#", "SCORE", reached_name, "KILLS", "MAP", "DATE"]
        for x, head in zip(cols, heads):
            screen.blit(fonts["small"].render(tr(fonts, head), True, (80, 240, 255)), (WIDTH * x, HEIGHT * 0.27))
        table = save.get("rankings", {}).get(mode, [])
        medal = {0: (255, 200, 60), 1: (210, 210, 225), 2: (220, 140, 80)}     # 금, 은, 동
        for i, e in enumerate(table):
            y = HEIGHT * (0.33 + i * 0.05)
            color = medal.get(i, WHITE)
            values = [f"{i + 1}", f"{e['score']}", f"{e['reached']}", f"{e['kills']}", e["map"], e["date"]]
            for x, value in zip(cols, values):
                screen.blit(fonts["small"].render(value, True, color), (WIDTH * x, y))
        if not table:
            text = "아직 기록이 없어요. 한 판 하고 오세요!" if ko else "No records yet. Go play a game!"
            image = fonts["help"].render(text, True, (150, 150, 170))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.5)))
        hint = ("←→ 모드 바꾸기   ESC 돌아가기   - 점수 = 그 판에 얻은 경험치 (처치, 헤드샷, 라운드 클리어...)"
                if ko else "LEFT / RIGHT change mode   ESC back   - score = XP earned in that game")
        draw_hint_bar(screen, fonts, hint)
        present("ranking_screen")
        await asyncio.sleep(0)


async def stats_screen(save):
    """기록 화면: 누적 기록, 무기별 처치·레벨, 최근 판. E 저장 코드 내보내기, I 가져오기, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    message, pending = "", None
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if pending is not None:                          # 가져오기 확인: Y 바꾸기 / 다른 키 취소
                if event.key == pygame.K_y:
                    res = save.get("res")
                    save.clear()
                    save.update(pending)
                    if res is not None:
                        save["res"] = res
                    apply_settings(save.get("settings", {}))
                    apply_keys(save.get("keys", {}))
                    write_save(save)
                    message = "저장을 가져왔어요!" if ko else "Save imported!"
                else:
                    message = "취소했어요" if ko else "Cancelled"
                pending = None
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key == pygame.K_e:
                where = copy_text(export_code(save))
                message = (f"코드를 복사했어요 ({where})" if ko else f"Code copied ({where})") if where else \
                    ("복사하지 못했어요" if ko else "Could not copy")
            elif event.key == pygame.K_i:
                data = import_code(paste_text())
                if data is None:
                    message = "코드가 없거나 틀렸어요 (한 글자도 빠지면 안 돼요)" if ko else "No valid code found"
                else:
                    pending = data
                    message = (f"가져올 저장: 계급 {player_level(data)}, 캠페인 최고 {data.get('best', 0)}라운드. "
                               "지금 저장을 바꿀까요? Y = 예" if ko else
                               f"Import: rank {player_level(data)}, best round {data.get('best', 0)}. Replace? Y = yes")
        draw_backdrop(screen)
        draw_title(screen, fonts, "STATS", (WIDTH * 0.05, HEIGHT * 0.08))
        life = save.get("lifetime", {})
        lines = [f"RANK {player_level(save)}   XP {save.get('xp', 0)}   CAMPAIGN BEST ROUND {save.get('best', 0)}   "
                 f"ZOMBIES BEST WAVE {save.get('zbest', 0)}   MISSIONS {len(save.get('missions_done', []))}",
                 f"KILLS {life.get('kills', 0)}   HEADSHOTS {life.get('heads', 0)}   KNIFE {life.get('knife', 0)}   "
                 f"EXPLOSIVE {life.get('explosive', 0)}   BEST STREAK {life.get('streak', 0)}   ROUNDS {life.get('rounds', 0)}   "
                 f"ACHIEVEMENTS {len(save.get('achievements', []))}/{len(ACHIEVEMENTS)}"]
        for i, line in enumerate(lines):
            font = fonts["small"] if fonts["small"].size(line)[0] <= WIDTH * 0.9 else fonts["tiny"]
            screen.blit(font.render(fit_text(font, line, WIDTH * 0.9), True, (80, 240, 255)),
                        (WIDTH * 0.05, HEIGHT * (0.15 + i * 0.04)))
        # 왼쪽: 무기별 처치와 레벨 (많이 쓴 순서)
        screen.blit(fonts["normal"].render(tr(fonts, "WEAPONS"), True, WHITE), (WIDTH * 0.05, HEIGHT * 0.26))
        kills = save.get("wkills", {})
        ranked = sorted(kills.items(), key=lambda kv: -kv[1])[:12]
        top = max([k for _, k in ranked] + [1])
        for i, (name, count) in enumerate(ranked):
            y = HEIGHT * (0.32 + i * 0.045)
            screen.blit(fonts["small"].render(f"{name}", True, WHITE), (WIDTH * 0.05, y))
            bar = pygame.Rect(WIDTH * 0.2, y + 3 * UI, WIDTH * 0.18 * count / top, 10 * UI)
            pygame.draw.rect(screen, (255, 200, 60), bar)
            screen.blit(fonts["tiny"].render(f"{count} kills  LV {weapon_level(count)}", True, (200, 200, 220)),
                        (WIDTH * 0.39, y))
        if not ranked:
            screen.blit(fonts["help"].render("아직 기록이 없어요" if ko else "No kills yet", True, (150, 150, 170)),
                        (WIDTH * 0.05, HEIGHT * 0.32))
        # 오른쪽: 최근 판
        screen.blit(fonts["normal"].render(tr(fonts, "RECENT GAMES"), True, WHITE), (WIDTH * 0.52, HEIGHT * 0.26))
        for i, game in enumerate(reversed(save.get("history", []))):
            y = HEIGHT * (0.32 + i * 0.045)
            text = (f"{game['date']}  {game['mode']}  R{game['round']}  KILLS {game['kills']}  "
                    f"ACC {game['acc']}%  {game['minutes']}min")
            screen.blit(fonts["tiny"].render(fit_text(fonts["tiny"], text, WIDTH * 0.45), True, (200, 200, 220)),
                        (WIDTH * 0.52, y))
        if message:
            image = fonts["help"].render(message, True, (80, 255, 120))
            screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.88)))
        hint = ("E 저장 코드 내보내기(복사)   I 코드 가져오기(붙여넣기)   ESC 돌아가기   - 웹과 맥 사이에 진행을 옮길 수 있어요"
                if ko else "E export save code   I import save code   ESC back")
        draw_hint_bar(screen, fonts, hint)
        present("stats_screen")
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
        draw_backdrop(screen)
        draw_title(screen, fonts, "CHALLENGES", (WIDTH * 0.06, HEIGHT * 0.09))
        records = save.get("challenges", {})
        today = str(datetime.date.today())
        for i, (name, round_no, desc_ko, desc_en) in enumerate(CHALLENGES):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.2 + i * 0.13), WIDTH * 0.88, HEIGHT * 0.11)
            selected = i == row
            draw_panel(screen, rect, selected)
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
        draw_hint_bar(screen, fonts, hint)
        present("challenge_screen")
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
        draw_backdrop(screen)
        draw_title(screen, fonts, f"ACHIEVEMENTS  {len(done)} / {len(ACHIEVEMENTS)}", (WIDTH * 0.05, HEIGHT * 0.08))
        half = (len(ACHIEVEMENTS) + 1) // 2
        for i, (name, desc_ko, desc_en, test) in enumerate(ACHIEVEMENTS):
            col, line = divmod(i, half)
            step = min(0.069, 0.55 / half)                     # 업적이 늘어도 아래 기록 줄 위까지
            rect = pygame.Rect(WIDTH * (0.04 + col * 0.47), HEIGHT * (0.15 + line * step), WIDTH * 0.45, HEIGHT * step * 0.9)
            got = name in done
            pygame.draw.rect(screen, (50, 44, 20) if got else (24, 18, 44), rect, border_radius=6)
            pygame.draw.rect(screen, (255, 215, 80) if got else (70, 60, 100), rect, 2 if got else 1, border_radius=6)
            mark = fonts["normal"].render(("* " if got else "- ") + name, True, (255, 215, 80) if got else (140, 140, 160))
            screen.blit(mark, mark.get_rect(midleft=(rect.x + 10, rect.centery)))
            room = rect.w - mark.get_width() - 34
            desc = fonts["help"].render(fit_text(fonts["help"], desc_ko if ko else desc_en, room), True,
                                        WHITE if got else (150, 150, 170))
            screen.blit(desc, desc.get_rect(midright=(rect.right - 10, rect.centery)))
        totals = (f"KILLS {life.get('kills', 0)}   HEADSHOTS {life.get('heads', 0)}   KNIFE {life.get('knife', 0)}   "
                  f"EXPLOSIVE {life.get('explosive', 0)}   BEST STREAK {life.get('streak', 0)}   ROUNDS {life.get('rounds', 0)}")
        image = fonts["small"].render(fit_text(fonts["small"], totals, WIDTH * 0.92), True, (80, 240, 255))
        screen.blit(image, image.get_rect(center=(WIDTH / 2, HEIGHT * 0.73)))
        # 위장 무늬 고르기 + 미리보기
        names = []
        for name, need, body, accent in CAMOS:
            names.append(f"[{name}]" if name == current else (name if name in camos else f"{name}({need})"))
        camo_text = fit_text(fonts["normal"], "CAMO:  " + "   ".join(names), WIDTH * 0.7)
        image = fonts["normal"].render(camo_text, True, WHITE)
        screen.blit(image, image.get_rect(midleft=(WIDTH * 0.05, HEIGHT * 0.8)))
        if current not in previews:
            previews[current] = make_viewmodel("RIFLE", False, None if current == "NONE" else current)[0]
        gun = previews[current]
        scale = HEIGHT * 0.16 / gun.get_height()
        gun = pygame.transform.smoothscale(gun, (int(gun.get_width() * scale), int(gun.get_height() * scale)))
        screen.blit(gun, gun.get_rect(midright=(WIDTH * 0.97, HEIGHT * 0.84)))
        hint = ("←→ 위장 무늬 고르기 (업적을 모으면 늘어나요)   ESC 돌아가기" if ko
                else "LEFT/RIGHT choose camo (earn more with achievements)   ESC back")
        draw_hint_bar(screen, fonts, hint)
        present("achievements_screen")
        await asyncio.sleep(0)


# 시작 화면 메뉴: (키, 키 글자, 이름, 한글 설명, 영어 설명, 칸(0 = 왼쪽 PLAY, 1 = 오른쪽 PROFILE))
INTRO_ITEMS = [
    (pygame.K_RETURN, "Enter", "CAMPAIGN", "100라운드 전쟁. ←→ 로 시작할 세트를 골라요", "100 rounds of war. LEFT/RIGHT picks the start set", 0),
    (pygame.K_c, "C", "CONTINUE", "저장된 라운드부터 이어해요", "Pick up from your saved round", 0),
    (pygame.K_z, "Z", "ZOMBIES", "웨이브를 버티며 점수를 모아요", "Survive the waves, earn points", 0),
    (pygame.K_o, "O", "MISSIONS", "큰 맵에서 5단계 작전", "Five-stage operations on huge maps", 0),
    (pygame.K_x, "X", "CHALLENGES", "오늘의 도전, 헤드샷만, 권총만...", "Daily, headshots only, pistol only...", 0),
    (pygame.K_r, "R", "TRAINING", "사격장에서 연습 (기록 안 바뀜)", "Practice range (no progress)", 0),
    (pygame.K_g, "G", "DEEP RUN", "로그라이트: 깰 때마다 강화를 골라 더 깊이", "Roguelite: pick a boon after every clear", 0),
    (pygame.K_e, "E", "MY MAPS", "맵을 직접 그리고 플레이해요", "Draw your own maps and play them", 0),
    (pygame.K_l, "L", "LEADERBOARD", "모드별 점수 TOP 10", "Top 10 scores per mode", 1),
    (pygame.K_v, "V", "STATS", "누적 기록, 최근 판, 저장 옮기기", "Lifetime stats, recent games, save code", 1),
    (pygame.K_a, "A", "ACHIEVEMENTS", "업적과 위장 무늬", "Achievements and camo", 1),
    (pygame.K_k, "K", "SKILLS", "계급 포인트로 스킬 배우기", "Spend rank points on skills", 1),
    (pygame.K_s, "S", "SETTINGS", "화면, 소리, 조작, 키 바꾸기", "Display, sound, controls, keys", 1),
    (pygame.K_d, "D", "DIFFICULTY", "←→ 로 적의 강함을 바꿔요", "LEFT/RIGHT changes enemy strength", 1),
    (pygame.K_t, "T", "RESOLUTION", "←→ 로 화면 크기를 바꿔요", "LEFT/RIGHT changes the window size", 1),
    (pygame.K_h, "H", "HOW TO PLAY", "조작법과 팁", "Controls and tips", 1),
]


async def help_screen(fonts):
    """조작법 화면: 아무 키나 누르면 돌아가요"""
    screen = pygame.display.get_surface()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type == pygame.KEYDOWN:
                return None
        draw_backdrop(screen)
        draw_help(screen, fonts, "")
        draw_hint_bar(screen, fonts, "Enter / ESC 돌아가기 (아무 키)" if ko else "ANY KEY back")
        present("help_screen")
        await asyncio.sleep(0)


_splash_shown = [False]


async def splash_screen():
    """게임을 켜면 한 번: 2.5초 타이틀 연출 (아무 키나 누르면 바로 넘어가요).
    넘기려고 누른 키는 버리지 않고 돌려줘서 메뉴가 그대로 받아요"""
    if _splash_shown[0]:
        return []
    _splash_shown[0] = True
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    clock = pygame.time.Clock()
    t = 0.0
    while t < SPLASH_TIME:
        t += clock.tick(60) / 1000
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type == pygame.KEYDOWN:
                return [event]
        draw_backdrop(screen)
        # 네온 줄이 왼쪽에서 오른쪽으로 쓸고 지나가요
        sweep = min(1.0, t / 0.8)
        for i in range(5):
            y = HEIGHT * (0.45 + i * 0.014)
            color = UI_ACCENT if i % 2 else UI_CYAN
            pygame.draw.line(screen, color, (0, y), (WIDTH * sweep, y), 2)
        # 제목: 크게 나타났다가 제자리로 (살짝 깜빡이는 네온)
        k = min(1.0, max(0.0, (t - 0.4) / 0.6))
        if k > 0:
            title = fonts["title"].render("STRIKE ZONE", True, UI_ACCENT).copy()
            scale = 1.6 - 0.6 * (1 - (1 - k) ** 3)
            title = pygame.transform.smoothscale(title, (int(title.get_width() * scale), int(title.get_height() * scale)))
            flicker = 0.75 if 1.0 < t < 1.15 else 1.0
            title.set_alpha(int(255 * k * flicker))
            screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.36)))
        if t > 1.3:
            sub = fonts["normal"].render("A RAYCAST SHOOTER", True, UI_CYAN).copy()
            sub.set_alpha(int(255 * min(1.0, (t - 1.3) / 0.4)))
            screen.blit(sub, sub.get_rect(center=(WIDTH / 2, HEIGHT * 0.58)))
        fade = min(1.0, max(0.0, (t - (SPLASH_TIME - 0.4)) / 0.4))    # 끝에 어두워지며 메뉴로
        if fade:
            dim = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dim.fill((0, 0, 0, int(255 * fade)))
            screen.blit(dim, (0, 0))
        present("splash_screen")
        await asyncio.sleep(0)
    return []


SPLASH_TIME = 2.6


async def intro_screen(save):
    """시작 화면: 왼쪽 PLAY(게임 모드), 오른쪽 PROFILE(기록·설정) 메뉴.
    ↑↓ 고르기, ←→ 값 바꾸기(세트·난이도·해상도) 또는 옆 칸으로, Enter 실행. 칸마다 단축키도 그대로.
    고른 것을 dict(mode=..., round=...)로 돌려줘요. ESC면 None, 창 닫기면 "closed"."""
    options = available_resolutions()
    res_index = min(save.get("res", 0), len(options) - 1)
    set_resolution(*options[res_index])
    screen = open_window()
    replay = await splash_screen()                 # 오프닝 (넘길 때 누른 키는 메뉴로)
    if replay == "closed":
        return "closed"
    fonts = make_fonts()
    clock = pygame.time.Clock()
    continue_round = save.get("continue", 1)
    reached = max(save.get("best", 1), continue_round)
    set_starts = [1 + k * SET_SIZE for k in range(len(SETS)) if 1 + k * SET_SIZE <= reached]
    start_pick = 0
    sel = 0
    cursor = None                    # 고른 칸 빛이 부드럽게 따라가는 위치
    t = 0.0

    def change_res(step):
        nonlocal res_index, screen, fonts, cursor
        res_index = (res_index + step) % len(options)
        save["res"] = res_index
        write_save(save)
        set_resolution(*options[res_index])
        screen = open_window()
        fonts = make_fonts()
        cursor = None

    while True:
        t += clock.tick(30) / 1000
        items = [it for it in INTRO_ITEMS
                 if not (it[0] == pygame.K_c and continue_round <= 1) and not (it[0] == pygame.K_t and len(options) < 2)]
        sel = min(sel, len(items) - 1)
        events, replay = replay + menu_events(), []
        for event in events:
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            key = event.key
            if key == pygame.K_ESCAPE:
                return None
            if key in (pygame.K_UP, pygame.K_DOWN):
                sel = (sel + (1 if key == pygame.K_DOWN else -1)) % len(items)
                continue
            if key in (pygame.K_LEFT, pygame.K_RIGHT):
                step = 1 if key == pygame.K_RIGHT else -1
                item = items[sel]
                if item[0] == pygame.K_RETURN and len(set_starts) > 1:
                    start_pick = (start_pick + step) % len(set_starts)
                elif item[0] == pygame.K_d:
                    SETTINGS["difficulty"] = (SETTINGS["difficulty"] + step) % len(DIFFICULTIES)
                    save["settings"] = dict(SETTINGS)
                    write_save(save)
                elif item[0] == pygame.K_t:
                    change_res(step)
                else:                                  # 옆 칸의 같은 줄로
                    col = item[5]
                    mine = [i for i, it in enumerate(items) if it[5] == col]
                    other = [i for i, it in enumerate(items) if it[5] != col]
                    sel = other[min(mine.index(sel), len(other) - 1)]
                continue
            if key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                key = items[sel][0]                    # 고른 칸 실행
            else:                                      # 단축키를 누르면 그 칸으로 커서도 옮겨요
                sel = next((i for i, it in enumerate(items) if it[0] == key), sel)
            if key == pygame.K_RETURN:
                return dict(mode="campaign", round=set_starts[start_pick])
            if key == pygame.K_d:
                SETTINGS["difficulty"] = (SETTINGS["difficulty"] + 1) % len(DIFFICULTIES)
                save["settings"] = dict(SETTINGS)
                write_save(save)
            if key == pygame.K_z:
                return dict(mode="zombies", round=1)
            if key == pygame.K_g:
                return dict(mode="campaign", round=1, deeprun=True)
            if key == pygame.K_r:
                return dict(mode="training", round=1)
            if key == pygame.K_h:
                if await help_screen(fonts) == "closed":
                    return "closed"
                continue
            if key == pygame.K_v:
                if await stats_screen(save) == "closed":
                    return "closed"
                continue
            if key == pygame.K_l:
                if await ranking_screen(save) == "closed":
                    return "closed"
                continue
            if key == pygame.K_e:
                picked = await map_slots_screen(save)
                if picked == "closed" or picked:
                    return picked
                continue
            if key == pygame.K_x:
                picked = await challenge_screen(save)
                if picked == "closed" or picked:
                    return picked
                continue
            if key == pygame.K_a:
                if await achievements_screen(save) == "closed":
                    return "closed"
                continue
            if key == pygame.K_o:
                picked = await mission_screen(save)
                if picked == "closed" or picked:
                    return picked
                continue
            if key == pygame.K_c and continue_round > 1:
                return dict(mode="campaign", round=continue_round)
            if key == pygame.K_s:
                if await settings_screen(save) == "closed":
                    return "closed"
                screen = pygame.display.get_surface()
                fonts = make_fonts()
                cursor = None
                continue
            if key == pygame.K_k:
                if await skills_screen(save) == "closed":
                    return "closed"
                continue
            if key == pygame.K_t and len(options) > 1:
                change_res(1)

        ko = fonts["lang"] == "ko"
        draw_backdrop(screen)
        # 제목과 네온 줄무늬 (천천히 빛나요)
        glow = 0.5 + 0.5 * math.sin(t * 2)
        for i in range(5):
            y = HEIGHT * (0.165 + i * 0.01)
            color = UI_ACCENT if i % 2 else UI_CYAN
            line = pygame.Surface((WIDTH, 2), pygame.SRCALPHA)
            line.fill((*color, int(110 + 120 * (glow if i % 2 else 1 - glow))))
            screen.blit(line, (0, y))
        title = fonts["title"].render("STRIKE ZONE", True, UI_ACCENT)
        screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.09)))
        # 두 칸 메뉴
        col_x = [WIDTH * 0.08, WIDTH * 0.53]
        col_w, row_h, gap = WIDTH * 0.39, HEIGHT * 0.058, HEIGHT * 0.067
        heads = ["PLAY", "PROFILE"]
        rects = []
        rows = [0, 0]
        for col in (0, 1):
            screen.blit(fonts["small"].render(tr(fonts, heads[col]), True, UI_CYAN), (col_x[col], HEIGHT * 0.215))
        for item in items:
            col = item[5]
            rects.append(pygame.Rect(col_x[col], HEIGHT * 0.25 + rows[col] * gap, col_w, row_h))
            rows[col] += 1
        target = pygame.Vector2(rects[sel].topleft)
        cursor = target if cursor is None else cursor.lerp(target, 0.35)
        for i, (item, rect) in enumerate(zip(items, rects)):
            draw_panel(screen, rect, False)
        moving = pygame.Rect(cursor.x, cursor.y, col_w, row_h)        # 움직이는 선택 칸
        draw_panel(screen, moving, True)
        diff = DIFFICULTIES[SETTINGS["difficulty"]][0]
        for i, (item, rect) in enumerate(zip(items, rects)):
            key, cap, name, _, _, _ = item
            selected = i == sel
            label = fonts["normal"].render(tr(fonts, name), True, YELLOW if selected else WHITE)
            screen.blit(label, label.get_rect(midleft=(rect.x + 14 * UI, rect.centery)))
            value = ""
            if key == pygame.K_RETURN:
                value = f"ROUND {set_starts[start_pick]}" + ("  < >" if len(set_starts) > 1 and selected else "")
            elif key == pygame.K_c:
                value = f"ROUND {continue_round}"
            elif key == pygame.K_d:
                value = diff + ("  < >" if selected else "")
            elif key == pygame.K_t:
                w, h = options[res_index]
                value = f"{w}x{h}" + ("" if fits_desktop(w, h) else " FULL") + ("  < >" if selected else "")
            right = rect.right - 10 * UI
            cap_w = fonts["tiny"].size(cap)[0] + 12 * UI
            draw_keycap(screen, fonts["tiny"], cap, right - cap_w, rect.centery)
            if value:
                room = right - cap_w - 12 * UI - (label.get_rect(midleft=(rect.x + 14 * UI, 0)).right + 10 * UI)
                font = fonts["small"] if fonts["small"].size(value)[0] <= room else fonts["tiny"]
                image = font.render(fit_text(font, value, room), True, UI_CYAN)
                screen.blit(image, image.get_rect(midright=(right - cap_w - 12 * UI, rect.centery)))
        # 고른 칸 설명과 기록
        item = items[sel]
        desc = fonts["help"].render(item[3] if ko else item[4], True, (200, 230, 255))
        bottom = HEIGHT * 0.25 + max(rows) * gap
        screen.blit(desc, desc.get_rect(center=(WIDTH / 2, bottom + 6 * UI)))
        records = [f"RANK {player_level(save)}"]
        if save.get("best"):
            records.append(f"CAMPAIGN BEST ROUND {save['best']}")
        if save.get("zbest"):
            records.append(f"ZOMBIES BEST WAVE {save['zbest']}")
        image = fonts["small"].render("     ".join(records), True, UI_DIM)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, bottom + 32 * UI)))
        hint = ("↑↓ 고르기   ←→ 값 바꾸기 / 옆 칸   Enter 실행   ESC 뒤로   - 칸 오른쪽 글자는 바로 가는 키" if ko else
                "UP/DOWN choose   LEFT/RIGHT change / other column   ENTER select   ESC back   - letters are shortcuts")
        draw_hint_bar(screen, fonts, hint)
        present("intro_screen")
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
        draw_backdrop(screen)
        draw_title(screen, fonts, "MISSIONS", (WIDTH * 0.06, HEIGHT * 0.09))
        sub = "큰 맵에서 다섯 단계로 이어지는 긴 작전. 단계마다 체크포인트에 저장돼요." if ko else \
            "Long operations on huge maps: five stages, checkpoint saved after each one."
        sub = fit_text(fonts["help"], sub, WIDTH * 0.88)
        screen.blit(fonts["help"].render(sub, True, (80, 240, 255)), (WIDTH * 0.06, HEIGHT * 0.15))
        done = save.get("missions_done", [])
        for i, m in enumerate(MISSIONS):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.22 + i * 0.17), WIDTH * 0.88, HEIGHT * 0.15)
            selected = i == row
            draw_panel(screen, rect, selected)
            name = m["name"] + ("   [COMPLETE]" if m["name"] in done else "")
            screen.blit(fonts["big"].render(name, True, YELLOW if selected else WHITE), (rect.x + 16, rect.y + 8))
            desc = fit_text(fonts["help"], m["desc"][0 if ko else 1], rect.w - 32)
            screen.blit(fonts["help"].render(desc, True, (200, 230, 255)), (rect.x + 16, rect.y + rect.h * 0.62))
            if saved and saved["id"] == i:
                text = f"C 이어하기: {saved['stage'] + 1}단계부터" if ko else f"C continue from stage {saved['stage'] + 1}"
                image = fonts["small"].render(text, True, (255, 200, 60))
                screen.blit(image, image.get_rect(topright=(rect.right - 16, rect.y + 12)))
        stages = "   >   ".join(title for _, title in MISSION_STAGES)
        for k, line in enumerate(wrap_text(fonts["tiny"], stages, WIDTH * 0.88)):
            screen.blit(fonts["tiny"].render(line, True, (180, 180, 200)),
                        (WIDTH * 0.06, HEIGHT * 0.74 + k * fonts["tiny"].get_linesize()))
        hint = "↑↓ 고르기     Enter 처음부터     C 이어하기     ESC 뒤로" if ko else \
            "UP/DOWN choose     ENTER start     C continue     ESC back"
        draw_hint_bar(screen, fonts, hint)
        present("mission_screen")
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
        draw_backdrop(screen)
        draw_title(screen, fonts, "SKILLS", (WIDTH * 0.06, HEIGHT * 0.08))
        level = player_level(save)
        into = save.get("xp", 0) % XP_PER_RANK
        info = f"RANK {level}   XP {into} / {XP_PER_RANK}   SKILL POINTS {skill_points(save)}"
        screen.blit(fonts["normal"].render(info, True, (80, 240, 255)), (WIDTH * 0.06, HEIGHT * 0.14))
        for i, (name, top, desc_ko, desc_en, key) in enumerate(SKILLS):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * (0.2 + i * 0.071), WIDTH * 0.88, HEIGHT * 0.062)
            selected = i == row
            draw_panel(screen, rect, selected, radius=6)
            kind = "ACTIVE" if key else "PASSIVE"
            label = fit_text(fonts["small"], f"{name}  ({kind})", rect.w * 0.33 - 20)
            screen.blit(fonts["small"].render(label, True, YELLOW if key else WHITE),
                        fonts["small"].render(label, True, WHITE).get_rect(midleft=(rect.x + 12, rect.centery)))
            desc = fit_text(fonts["help"], desc_ko if ko else desc_en, rect.w * 0.67 - top * 26 * UI - 30)
            image = fonts["help"].render(desc, True, (200, 230, 255))
            screen.blit(image, image.get_rect(midleft=(rect.x + rect.w * 0.33, rect.centery)))
            have = ranks.get(name, 0)
            for k in range(top):                           # 배운 단계는 채운 칸
                box = pygame.Rect(rect.right - (top - k) * 26 * UI - 10, rect.centery - 8 * UI, 20 * UI, 16 * UI)
                pygame.draw.rect(screen, (255, 200, 60) if k < have else (60, 55, 80), box)
        hint = ("↑↓ 고르기     → 배우기     ← 되돌리기     ESC 돌아가기   (계급이 오를 때마다 포인트 1)" if ko
                else "UP/DOWN choose     RIGHT learn     LEFT undo     ESC back   (1 point per rank)")
        draw_hint_bar(screen, fonts, hint)
        present("skills_screen")
        await asyncio.sleep(0)


def current_weapon_spec(save, name, choices=None):
    """저장 정보 기준으로 그 무기의 지금 성능 (choices 를 주면 그 부착물로)"""
    kills = save.get("wkills", {}).get(name, 0)
    chosen = choices or save.get("gunsmith", {}).get(name)
    if chosen:
        gold = [m for m in weapon_mods(kills) if m == "GOLD CAMO"]
        return apply_gunsmith(apply_mods(WEAPON_BY_NAME[name], gold, weapon_level(kills)), chosen)
    return apply_mods(WEAPON_BY_NAME[name], weapon_mods(kills), weapon_level(kills))


async def gunsmith_screen(save, name):
    """총기 개조: 칸(조준경·총구·탄창·손잡이)마다 부착물을 골라요. ↑↓ 칸, ←→ 부착물, Enter/ESC 저장하고 돌아가기"""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    slots = list(ATTACHMENTS)
    choices = dict(save.get("gunsmith", {}).get(name) or gunsmith_default(save, name))
    base = current_weapon_spec(save, name)
    row = 0
    preview = make_viewmodel(name, False)[0]
    scale = min(WIDTH * 0.36 / preview.get_width(), HEIGHT * 0.3 / preview.get_height())
    preview = pygame.transform.smoothscale(preview, (int(preview.get_width() * scale), int(preview.get_height() * scale)))
    level = weapon_level(save.get("wkills", {}).get(name, 0))
    while True:
        clock.tick(30)
        for event in menu_events():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_g):
                save.setdefault("gunsmith", {})[name] = choices
                write_save(save)
                return None
            if event.key in (pygame.K_UP, pygame.K_w):
                row = (row - 1) % len(slots)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % len(slots)
            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_a, pygame.K_d):
                slot = slots[row]
                names = [option for option, _, _ in ATTACHMENTS[slot]]
                step = 1 if event.key in (pygame.K_RIGHT, pygame.K_d) else -1
                k = names.index(choices[slot])
                for _ in range(len(names)):                    # 잠긴 것은 건너뛰어요
                    k = (k + step) % len(names)
                    if attachment_unlocked(save, name, slot, names[k]):
                        choices[slot] = names[k]
                        break
        spec = current_weapon_spec(save, name, choices)
        draw_backdrop(screen)
        draw_title(screen, fonts, f"GUNSMITH  -  {name}", (WIDTH * 0.05, HEIGHT * 0.08))
        screen.blit(fonts["small"].render(f"WEAPON LEVEL {level}  (level up by getting kills with this weapon)", True,
                                          (255, 200, 60)), (WIDTH * 0.05, HEIGHT * 0.14))
        label_h, name_h, info_h = (fonts[k].get_linesize() for k in ("small", "normal", "help"))
        row_h = max(HEIGHT * 0.115, label_h + name_h + info_h + 8 * UI)       # 글자가 커도 안 겹치게
        for i, slot in enumerate(slots):
            rect = pygame.Rect(WIDTH * 0.05, HEIGHT * 0.2 + i * (row_h + HEIGHT * 0.015), WIDTH * 0.5, row_h)
            selected = i == row
            draw_panel(screen, rect, selected)
            screen.blit(fonts["small"].render(slot, True, (200, 200, 220)), (rect.x + 12, rect.y + 4 * UI))
            choice = choices[slot]
            text = f"<  {choice}  >" if selected else choice
            screen.blit(fonts["normal"].render(text, True, YELLOW if selected else WHITE),
                        (rect.x + 12, rect.y + 4 * UI + label_h))
            info = ATTACHMENT_INFO[choice][0 if ko else 1]
            if slot == "OPTIC" and (spec["scope"] or spec["projectile"]):
                info = "이 무기는 조준경을 바꿀 수 없어요" if ko else "This weapon keeps its own sight"
            info = fit_text(fonts["help"], info, rect.w - 24)
            screen.blit(fonts["help"].render(info, True, (200, 230, 255)), (rect.x + 12, rect.bottom - info_h - 3 * UI))
            # 오른쪽 끝: 이 칸의 부착물들 (잠긴 것은 필요한 레벨)
            parts = []
            for option, need, _ in ATTACHMENTS[slot]:
                parts.append(option if attachment_unlocked(save, name, slot, option) else f"LV{need}")
            slot_w = fonts["small"].size(slot)[0] + 30
            label = fonts["tiny"].render(fit_text(fonts["tiny"], "  ".join(parts), rect.w - slot_w - 20), True, (150, 150, 175))
            screen.blit(label, label.get_rect(topright=(rect.right - 10, rect.y + 8)))
        box = pygame.Rect(WIDTH * 0.58, HEIGHT * 0.2, WIDTH * 0.37, HEIGHT * 0.32)
        pygame.draw.rect(screen, (0, 0, 0), box)
        screen.blit(preview, preview.get_rect(center=box.center))
        stats = weapon_stats(spec) + [("ADS AIM", max(0.05, 1 - spec["spread"] * spec.get("ads_spread", 0.45) / 22))]
        before = weapon_stats(base) + [("ADS AIM", max(0.05, 1 - base["spread"] * base.get("ads_spread", 0.45) / 22))]
        for k, ((stat, value), (_, old)) in enumerate(zip(stats, before)):
            y = HEIGHT * (0.56 + k * 0.055)
            screen.blit(fonts["small"].render(stat, True, (200, 200, 220)), (box.x, y))
            bar = pygame.Rect(box.x + WIDTH * 0.12, y + 4 * UI, WIDTH * 0.25, 10 * UI)
            pygame.draw.rect(screen, (45, 40, 70), bar)
            pygame.draw.rect(screen, (80, 240, 255), (bar.x, bar.y, bar.w * min(1.0, value), bar.h))
            if abs(value - old) > 0.005:                     # 바뀐 만큼 초록(좋아짐) / 빨강(나빠짐)
                color = (80, 255, 120) if value > old else (255, 90, 90)
                x0, x1 = sorted((bar.w * min(1.0, old), bar.w * min(1.0, value)))
                pygame.draw.rect(screen, color, (bar.x + x0, bar.y, max(2, x1 - x0), bar.h))
        hint = ("↑↓ 칸 고르기   ←→ 부착물 바꾸기   Enter / ESC 저장하고 돌아가기" if ko
                else "UP/DOWN slot   LEFT/RIGHT attachment   ENTER / ESC save and back")
        draw_hint_bar(screen, fonts, hint)
        present("gunsmith_screen")
        await asyncio.sleep(0)


# 로드아웃 화면의 무기 종류 (이 순서대로 늘어놓고, Tab 으로 종류를 건너뛰어요)
WEAPON_CLASSES = [("RIFLES", ("RIFLE", "BURST", "HEAVY AR")), ("SMGS", ("SMG", "MACHINE PISTOL")),
                  ("SHOTGUNS", ("SHOTGUN", "AUTO SHOTGUN")), ("MARKSMAN", ("DMR", "SNIPER")), ("LMGS", ("LMG",)),
                  ("PISTOLS", ("PISTOL", "REVOLVER")), ("LAUNCHERS", ("LAUNCHER", "ROCKET"))]


def weapon_class(name):
    """무기 이름 → 종류 이름 (표에 없으면 OTHER)"""
    return next((cls for cls, names in WEAPON_CLASSES if name in names), "OTHER")


def class_order(names):
    """무기들을 종류 순서대로 정렬"""
    order = [n for _, group in WEAPON_CLASSES for n in group]
    return sorted(names, key=lambda n: order.index(n) if n in order else len(order))


def draw_stat_bar(screen, rect, value, old=None):
    """성능 막대. old 를 주면 바뀐 만큼 초록(좋아짐)/빨강(나빠짐)으로 보여줘요"""
    pygame.draw.rect(screen, (45, 40, 70), rect, border_radius=3)
    if old is None or abs(old - value) < 0.005:
        pygame.draw.rect(screen, UI_CYAN, (rect.x, rect.y, rect.w * value, rect.h), border_radius=3)
        return
    low, high = min(old, value), max(old, value)
    pygame.draw.rect(screen, UI_CYAN, (rect.x, rect.y, rect.w * low, rect.h), border_radius=3)
    color = (90, 230, 120) if value > old else (240, 80, 90)
    pygame.draw.rect(screen, color, (rect.x + rect.w * low, rect.y, rect.w * (high - low), rect.h))


async def loadout_screen(save, choice):
    """로드아웃: 주무기 / 보조무기 / 퍼크를 골라요. ↑↓ 줄 고르기, ←→ 바꾸기, Enter 시작, ESC 뒤로.
    고른 로드아웃(dict)을 돌려줘요. ESC면 None, 창 닫기면 "closed"."""
    screen = pygame.display.get_surface()
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"
    clock = pygame.time.Clock()
    perk_names = [name for name, _, _ in PERKS]
    tactical_names = [name for name, _, _ in TACTICALS]
    owned = class_order(unlocked_weapons(save))
    options = [owned, owned, perk_names, tactical_names]
    labels = ["START WEAPON", "SECOND WEAPON (Q)", "PERK", "TACTICAL (N)"]
    saved = dict(DEFAULT_LOADOUT, **save.get("loadout", {}))
    picks = [options[0].index(saved["primary"]) if saved["primary"] in options[0] else 0,
             options[1].index(saved["secondary"]) if saved["secondary"] in options[1] else 0,
             options[2].index(saved["perk"]) if saved["perk"] in options[2] else 0,
             options[3].index(saved["tactical"]) if saved["tactical"] in options[3] else 0]
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
                row = (row - 1) % 4
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                row = (row + 1) % 4
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                picks[row] = (picks[row] - 1) % len(options[row])
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                picks[row] = (picks[row] + 1) % len(options[row])
            elif event.key == pygame.K_TAB and row < 2:          # 다음 종류의 첫 무기로
                now = weapon_class(owned[picks[row]])
                for step in range(1, len(owned) + 1):
                    k = (picks[row] + step) % len(owned)
                    if weapon_class(owned[k]) != now:
                        picks[row] = k
                        break
            elif event.key == pygame.K_k:
                if await skills_screen(save) == "closed":
                    return "closed"
            elif event.key == pygame.K_g:                     # 총기 개조 (지금 고른 무기)
                weapon = options[1][picks[1]] if row == 1 else options[0][picks[0]]
                if await gunsmith_screen(save, weapon) == "closed":
                    return "closed"
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                loadout = dict(primary=options[0][picks[0]], secondary=options[1][picks[1]],
                               perk=options[2][picks[2]], tactical=options[3][picks[3]])
                save["loadout"] = loadout
                write_save(save)
                return loadout

        # 배경과 제목
        draw_backdrop(screen)
        draw_title(screen, fonts, "LOADOUT", (WIDTH * 0.06, HEIGHT * 0.09))
        if choice["mode"] == "zombies":
            mode_text = "ZOMBIES  -  BLOOD MOON"
        elif choice["mode"] == "mission":
            mode_text = f"MISSION  -  {MISSIONS[choice['mission']]['name']}"
        elif choice["mode"] == "custom":
            mode_text = f"CUSTOM MAP  -  {choice['custom_map']['name']}  (PRACTICE)"
        elif choice.get("deeprun"):
            best = save.get("deeprun", {}).get("best", 0)
            mode_text = f"DEEP RUN  -  BEST DEPTH {best}"
        else:
            mode_text = f"CAMPAIGN  -  ROUND {choice['round']}"
        mode_text += f"     RANK {player_level(save)}   SKILL POINTS {skill_points(save)}"
        label = fonts["small"].render(mode_text, True, UI_CYAN)
        screen.blit(label, label.get_rect(midleft=(WIDTH * 0.06, HEIGHT * 0.165)))

        # 왼쪽: 네 칸 (시작 무기 / 두 번째 무기 / 퍼크 / 전술 장비)
        label_h, name_h, desc_h = (fonts[k].get_linesize() for k in ("tiny", "normal", "help"))
        card_w, card_h = WIDTH * 0.44, max(HEIGHT * 0.112, label_h + name_h + desc_h + 10 * UI)   # 글자가 커도 안 겹치게
        for i in range(4):
            rect = pygame.Rect(WIDTH * 0.06, HEIGHT * 0.2 + i * (card_h + HEIGHT * 0.013), card_w, card_h)
            selected = i == row
            draw_panel(screen, rect, selected)
            screen.blit(fonts["tiny"].render(tr(fonts, labels[i]), True, UI_DIM), (rect.x + 14 * UI, rect.y + 7 * UI))
            name = options[i][picks[i]]
            if i < 2:                                           # 무기 칸: 종류 이름표 + 몇 번째인지
                tag = f"{weapon_class(name)}   {picks[i] + 1}/{len(owned)}"
                image = fonts["tiny"].render(tag, True, (255, 200, 60))
                screen.blit(image, image.get_rect(topright=(rect.right - 14 * UI, rect.y + 7 * UI)))
            arrows = f"<  {name}  >" if selected else name
            image = fonts["normal"].render(arrows, True, YELLOW if selected else WHITE)
            screen.blit(image, (rect.x + 14 * UI, rect.y + 4 * UI + label_h))
            if i < 2:
                desc = WEAPON_INFO[name][0 if ko else 1]
            elif i == 2:
                desc = PERKS[picks[2]][1 if ko else 2]
            else:
                desc = TACTICALS[picks[3]][1 if ko else 2]
            desc = fit_text(fonts["help"], desc, rect.w - 28 * UI)
            screen.blit(fonts["help"].render(desc, True, (200, 230, 255)), (rect.x + 14 * UI, rect.bottom - desc_h - 3 * UI))

        # 왼쪽 아래: 무기 인벤토리를 종류별로 (가진 무기는 레벨, 없는 무기는 자물쇠)
        top = rect.bottom + 10 * UI                       # 마지막 칸 바로 아래부터
        title = fonts["small"].render(tr(fonts, f"INVENTORY  {len(owned)} / {len(WEAPONS)}"), True, WHITE)
        if top + title.get_height() <= HEIGHT - 44 * UI:          # 자리가 있을 때만
            screen.blit(title, (WIDTH * 0.06, top))
        kills_all = save.get("wkills", {})
        chosen = (options[0][picks[0]], options[1][picks[1]])
        rows_needed = (len(WEAPONS) + 1) // 2
        room = HEIGHT - 44 * UI - (top + title.get_height() + 4 * UI)      # 아래 키 안내 띠 위까지
        font = next((f for f in ([fonts["help"]] if ko else []) + [fonts["tiny"]]
                     if f.get_linesize() * rows_needed <= room), fonts["tiny"])
        line_h = font.get_linesize()
        col_w = WIDTH * 0.22
        k = 0
        if line_h * rows_needed > room:                     # 자리가 모자라면 (큰 글자) 잠긴 무기만 짧게
            locked = [spec["name"] for spec in WEAPONS if spec["name"] not in owned]
            text = ("LOCKED: " + ", ".join(locked)) if locked else "ALL WEAPONS UNLOCKED"
            y = top + title.get_height() + 4 * UI
            for line in wrap_text(font, text, WIDTH * 0.44)[:int(room // line_h)]:
                screen.blit(font.render(line, True, UI_DIM), (WIDTH * 0.06, y))
                y += line_h
        for cls, names in ([] if line_h * rows_needed > room else WEAPON_CLASSES):
            for name in names:
                if name not in WEAPON_BY_NAME:
                    continue
                x = WIDTH * 0.06 + (k % 2) * (col_w + WIDTH * 0.005)
                y = top + title.get_height() + 4 * UI + (k // 2) * line_h
                if name in owned:
                    text = f"{name}  LV {weapon_level(kills_all.get(name, 0))}"
                    color = (255, 200, 60) if name in chosen else WHITE
                else:
                    text = f"[LOCKED] {name}: {unlock_text(name, ko)}"
                    color = (120, 120, 135)
                screen.blit(font.render(fit_text(font, text, col_w), True, color), (x, y))
                k += 1

        # 오른쪽: 고른 무기 모습과 성능 막대 (바꾸면 전과 비교)
        weapon = options[1][picks[1]] if row == 1 else options[0][picks[0]]
        before = saved["secondary"] if row == 1 else saved["primary"]
        if weapon not in previews:
            image = make_viewmodel(weapon, False)[0]
            scale = min(WIDTH * 0.4 / image.get_width(), HEIGHT * 0.4 / image.get_height())
            previews[weapon] = pygame.transform.smoothscale(
                image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        box = pygame.Rect(WIDTH * 0.54, HEIGHT * 0.2, WIDTH * 0.40, HEIGHT * 0.45)
        draw_panel(screen, box, False)
        preview = previews[weapon]
        screen.blit(preview, preview.get_rect(bottomright=(box.right - 4, box.bottom - 4)))
        screen.blit(fonts["normal"].render(weapon, True, WHITE), (box.x + 14 * UI, box.y + 10 * UI))
        kills = kills_all.get(weapon, 0)
        mods = weapon_mods(kills)
        upcoming = [(need, mod) for need, mod in WEAPON_LEVELS if kills < need]
        level = f"LV {weapon_level(kills)} / {WEAPON_MAX_LEVEL}  (DMG +{5 * (weapon_level(kills) - 1)}%)   {kills} kills"
        if upcoming:
            level += f"   next: {upcoming[0][1]} at {upcoming[0][0]}"
        width = box.w - 28 * UI
        screen.blit(fonts["tiny"].render(fit_text(fonts["tiny"], level, width), True, (255, 200, 60)),
                    (box.x + 14 * UI, box.y + 10 * UI + 30 * UI))
        if mods:
            screen.blit(fonts["tiny"].render(fit_text(fonts["tiny"], " + ".join(mods), width), True, UI_CYAN),
                        (box.x + 14 * UI, box.y + 10 * UI + 48 * UI))
        leveled = current_weapon_spec(save, weapon)
        if save.get("gunsmith", {}).get(weapon):
            parts = [v for v in save["gunsmith"][weapon].values() if v not in ("NONE", "STANDARD", "IRON SIGHTS")]
            text = fit_text(fonts["tiny"], "GUNSMITH: " + (" + ".join(parts) or "-"), width)
            screen.blit(fonts["tiny"].render(text, True, (150, 220, 255)), (box.x + 14 * UI, box.y + 10 * UI + 66 * UI))
        old_stats = None
        if row < 2 and before != weapon and before in WEAPON_BY_NAME:
            old_stats = dict(weapon_stats(current_weapon_spec(save, before)))
            note = f"vs {before}"
            image = fonts["tiny"].render(note, True, UI_DIM)
            screen.blit(image, image.get_rect(topright=(box.right, box.bottom + 8 * UI)))
        for k, (stat, value) in enumerate(weapon_stats(leveled)):
            y = box.bottom + HEIGHT * (0.035 + k * 0.042)
            screen.blit(fonts["small"].render(stat, True, (200, 200, 220)), (box.x, y))
            bar = pygame.Rect(box.x + WIDTH * 0.12, y + 4 * UI, WIDTH * 0.24, 10 * UI)
            old = old_stats.get(stat) if old_stats else None
            draw_stat_bar(screen, bar, min(1.0, value), None if old is None else min(1.0, old))
            if old is not None and abs(old - value) >= 0.005:
                diff = round(100 * (value - old))
                image = fonts["tiny"].render(f"{diff:+d}", True, (90, 230, 120) if diff > 0 else (240, 80, 90))
                screen.blit(image, image.get_rect(midleft=(bar.right + 6 * UI, bar.centery)))

        hint = ("↑↓ 고르기     ←→ 바꾸기     Tab 다음 종류     Enter 시작     G 총기 개조     K 스킬     ESC 뒤로" if ko
                else "UP/DOWN choose     LEFT/RIGHT change     TAB next type     ENTER start     G gunsmith     K skills     ESC back")
        draw_hint_bar(screen, fonts, hint)
        present("loadout_screen")
        await asyncio.sleep(0)


PAUSE_ITEMS = ["RESUME", "HELP", "SETTINGS", "PHOTO MODE", "QUIT TO MENU"]


async def photo_mode(game):
    """사진 모드 (일시정지 → PHOTO MODE): 게임이 멈춘 채로 카메라만 자유롭게.
    WASD 이동, 화살표 시점, 1~4 필터, H 글자 숨기기, 스페이스 사진 저장, ESC 돌아가기"""
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    p = game.player
    saved = (pygame.Vector2(p.pos), p.angle, p.pitch)
    filters = ["NORMAL", "BLACK & WHITE", "SEPIA", "VIGNETTE"]
    filt, show_text, message, msg_time = 0, True, "", 0.0
    vignette = pygame.Surface((160, 90))
    vignette.fill((255, 255, 255))
    for r in range(95, 0, -3):
        v = int(255 - 150 * (r / 95) ** 1.8)
        pygame.draw.ellipse(vignette, (v, v, v), (80 - r * 1.1, 45 - r * 0.62, r * 2.2, r * 1.24))
    vignette = pygame.transform.smoothscale(vignette, (WIDTH, HEIGHT))
    fonts = make_fonts()
    ko = fonts["lang"] == "ko"

    def render():
        game.draw(screen, hud=False)
        if filt == 1:
            screen.blit(pygame.transform.grayscale(screen), (0, 0))
        elif filt == 2:
            screen.blit(pygame.transform.grayscale(screen), (0, 0))
            screen.fill((255, 225, 175), special_flags=pygame.BLEND_MULT)
        elif filt == 3:
            screen.blit(vignette, (0, 0), special_flags=pygame.BLEND_MULT)

    while True:
        dt = min(0.05, clock.tick(30) / 1000)
        msg_time -= dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                p.pos, p.angle, p.pitch = saved
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                p.pos, p.angle, p.pitch = saved                  # 카메라를 원래 자리로
                return None
            if event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4):
                filt = event.key - pygame.K_1
            elif event.key == pygame.K_h:
                show_text = not show_text
            elif event.key == pygame.K_SPACE:
                render()
                where = save_picture(screen)
                message = (f"사진 저장: {where}" if ko else f"Saved: {where}") if where else \
                    ("저장하지 못했어요" if ko else "Could not save")
                msg_time = 3.0
        keys = pygame.key.get_pressed()
        forward = pygame.Vector2(math.cos(p.angle), math.sin(p.angle))
        side = pygame.Vector2(-forward.y, forward.x)
        move = pygame.Vector2()
        move += forward * ((keys[pygame.K_w]) - (keys[pygame.K_s]))
        move += side * ((keys[pygame.K_d]) - (keys[pygame.K_a]))
        if move.length() > 0:
            move_with_collision(p.pos, move.normalize() * 3.0 * dt)
        p.angle += (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 1.6 * dt
        p.pitch = max(-MAX_PITCH, min(MAX_PITCH, p.pitch + (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * 300 * UI * dt))
        render()
        if show_text:
            hint = (f"사진 모드  [{filters[filt]}]   WASD 이동  화살표 시점  1~4 필터  H 글자 숨기기  스페이스 사진 저장  ESC 돌아가기"
                    if ko else f"PHOTO MODE [{filters[filt]}]  WASD move  ARROWS look  1-4 filter  H hide  SPACE save  ESC back")
            image = fonts["help"].render(hint, True, WHITE)
            panel = pygame.Surface((image.get_width() + 20, image.get_height() + 10), pygame.SRCALPHA)
            panel.fill((0, 0, 0, 150))
            screen.blit(panel, panel.get_rect(midbottom=(WIDTH / 2, HEIGHT - 10)))
            screen.blit(image, image.get_rect(midbottom=(WIDTH / 2, HEIGHT - 15)))
        if msg_time > 0:
            image = fonts["help"].render(message, True, (80, 255, 120))
            screen.blit(image, image.get_rect(midtop=(WIDTH / 2, 12)))
        present("photo_mode")
        await asyncio.sleep(0)


def blur_screen(screen, amount=10):
    """화면을 흐리게: 작게 줄였다가 다시 키우면 뿌옇게 돼요"""
    w, h = screen.get_size()
    small = pygame.transform.smoothscale(screen, (max(1, w // amount), max(1, h // amount)))
    screen.blit(pygame.transform.smoothscale(small, (w, h)), (0, 0))


_pause_cursor = [None]


def draw_pause(screen, fonts, row, age=1.0, blur=True):
    """일시정지 메뉴: 게임 화면을 흐리고 어둡게, 가운데 카드에 메뉴. 처음 0.2초 동안 부드럽게 나타나요
    blur=False: 이미 흐린 배경을 깔았을 때 (매 장면 흐리게 하면 느려요)"""
    show = min(1.0, age / 0.2)
    if blur:
        blur_screen(screen)
    shade_panel = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    shade_panel.fill((5, 5, 15, int(150 * show)))
    screen.blit(shade_panel, (0, 0))
    card = pygame.Rect(0, 0, WIDTH * 0.4, HEIGHT * (0.2 + len(PAUSE_ITEMS) * 0.095))
    card.center = (WIDTH / 2, HEIGHT * 0.5 + (1 - show) * 30 * UI)            # 아래에서 살짝 올라와요
    back = pygame.Surface(card.size, pygame.SRCALPHA)
    pygame.draw.rect(back, (14, 10, 30, int(225 * show)), back.get_rect(), border_radius=int(12 * UI))
    screen.blit(back, card)
    pygame.draw.rect(screen, UI_EDGE, card, 1, border_radius=int(12 * UI))
    draw_title(screen, fonts, "PAUSED", (WIDTH / 2, card.y + 46 * UI), anchor="center")
    rects = []
    for i, item in enumerate(PAUSE_ITEMS):
        rect = pygame.Rect(0, 0, card.w * 0.8, HEIGHT * 0.075)
        rect.center = (WIDTH / 2, card.y + 110 * UI + i * HEIGHT * 0.095)
        rects.append(rect)
        draw_panel(screen, rect, False)
    target = pygame.Vector2(rects[row].topleft)
    cur = _pause_cursor[0]
    cur = target if cur is None or age < 0.05 else cur.lerp(target, 0.35)    # 고른 칸이 부드럽게 움직여요
    _pause_cursor[0] = cur
    draw_panel(screen, pygame.Rect(cur.x, cur.y, rects[0].w, rects[0].h), True)
    for i, (item, rect) in enumerate(zip(PAUSE_ITEMS, rects)):
        label = fonts["normal"].render(tr(fonts, item), True, YELLOW if i == row else WHITE)
        screen.blit(label, label.get_rect(center=rect.center))
    ko = fonts["lang"] == "ko"
    hint = "↑↓ 고르기   Enter 확인   ESC 계속하기" if ko else "UP/DOWN choose   ENTER select   ESC resume"
    draw_hint_bar(screen, fonts, hint)


# 화면이 바뀔 때(메뉴 → 다른 메뉴, 메뉴 → 게임) 앞 화면이 0.22초 동안 부드럽게 사라져요
FADE_TIME = 0.22
_present = dict(key=None, frame=None, fade=None, start=0.0)


def present(key, keep=True):
    """pygame.display.flip() 대신 써요. key: 지금 화면 이름 (바뀌면 앞 화면에서 부드럽게 넘어가요)
    keep=False 면 이 화면은 기억하지 않아요 (게임 화면은 매 장면 복사하면 느려서)"""
    st = _present
    screen = pygame.display.get_surface()
    if key != st["key"]:
        old = st["frame"]
        st["fade"] = old if old is not None and old.get_size() == screen.get_size() else None
        st["start"], st["key"] = time.time(), key
    fresh = screen.copy() if keep else None
    if st["fade"] is not None:
        alpha = 1 - (time.time() - st["start"]) / FADE_TIME
        if alpha <= 0:
            st["fade"] = None
        else:
            st["fade"].set_alpha(int(255 * alpha))
            screen.blit(st["fade"], (0, 0))
    st["frame"] = fresh
    pygame.display.flip()


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

    training = choice["mode"] in ("training", "custom")      # 연습: 진짜 저장에 남지 않아요
    # 사격장은 저장 정보의 복사본으로 (무엇을 해도 진짜 저장에는 남지 않아요)
    game = Game(copy.deepcopy(save) if training else save, choice["round"], mode=choice["mode"], loadout=loadout,
                mission=choice.get("mission", 0), stage=choice.get("stage", 0), challenge=choice.get("challenge"),
                custom=choice.get("custom_map"), deeprun=choice.get("deeprun", False))
    running = True
    closed = False             # 창을 닫았는지 여부
    work_time, frames, check_timer = 0.0, 0, 0.0   # 자동 해상도 조절용 기록
    gamepad = get_gamepad()
    paused, pause_row = False, 0       # ESC: 일시정지 메뉴 (실수로 눌러도 진행이 날아가지 않아요)
    pause_started = 0.0                # 일시정지 메뉴가 나타나는 움직임용
    pause_bg = None                    # 일시정지 뒤에 깔 흐린 게임 화면
    pause_fonts = None
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
                screen = pygame.display.get_surface()      # 설정에서 전체 화면을 바꿨을 수 있어요
            elif choice == "PHOTO MODE":
                if await photo_mode(game) == "closed":
                    running, closed = False, True
            elif choice == "QUIT TO MENU":
                running = False
            if not running:
                break
            if pause_bg is None or pause_bg.get_size() != screen.get_size():
                game.draw(screen, hud=False)             # 멈춘 화면을 한 번만 그리고 흐리게 해서 기억해요
                blur_screen(screen)
                pause_bg = screen.copy()
            screen.blit(pause_bg, (0, 0))
            if pause_fonts is None:
                pause_fonts = make_fonts()             # 메뉴 글꼴 (한글 메뉴면 한글)
            draw_pause(screen, pause_fonts, pause_row, time.time() - pause_started, blur=False)
            present("pause")
            await asyncio.sleep(0)
            continue
        for event in events:
            if event.type in (getattr(pygame, "CONTROLLERDEVICEADDED", -1), pygame.JOYDEVICEADDED):
                gamepad.connect()
            if event.type == pygame.QUIT:
                running, closed = False, True
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                paused, pause_row = True, 0
                pause_started, pause_bg, pause_fonts = time.time(), None, None
                grab_mouse(False)
            elif event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_r:
                game.retry_round()
            elif event.type == pygame.KEYDOWN and game.game_over and event.key == pygame.K_n:
                game.reset(1)
            elif (event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_F11)
                  and not IN_BROWSER):
                try:
                    pygame.display.toggle_fullscreen()
                    SETTINGS["fullscreen"] = 1 - SETTINGS.get("fullscreen", 0)   # 설정에도 기억해요
                    save["settings"] = dict(SETTINGS)
                    write_save(save)
                except pygame.error:
                    pass                       # 전체 화면을 지원하지 않는 환경
                screen = pygame.display.get_surface()
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

        present("game", keep=False)
        # 웹 브라우저에서 화면이 멈추지 않도록 잠깐 차례를 넘겨줘요
        await asyncio.sleep(0)

    if not training:
        game.finish_run()          # 메뉴로 나가도 그 판은 랭킹에 들어가요
        game.record_history()
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
