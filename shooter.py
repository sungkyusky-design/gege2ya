"""
스트라이크 존 - 1인칭 총게임 (레이캐스팅 FPS)

80년대 해변 도시를 무대로 라운드마다 맵이 바뀌어요.
    네온 비치 (노을) : 해변, 호텔 안뜰, 오피스 골목, 주차장, 공원, 공사장, 시장 골목
    다운타운 (밤)    : 마천루, 네온 간판이 빛나는 광장, 주차장, 좁은 골목
    하버 (새벽)      : 컨테이너 미로, 크레인, 창고, 바다로 뻗은 부두

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

조작 (키보드만으로 다 할 수 있어요):
    W A S D          : 이동
    Shift            : 달리기 (W와 함께. 달리는 동안은 못 쏴요)
    C                : 앉기 / 일어나기. 달리다가 누르면 슬라이딩
    스페이스바       : 점프
    ← → / ↑ ↓        : 시점 돌리기 (좌우 / 위아래)    = 마우스
    F                : 사격 (꾹 누르면 연사)          = 마우스 왼쪽
    E                : 정조준 켜기/끄기 (저격총은 조준경) = 마우스 오른쪽(누르고 있기)
    Z                : 저격총 조준경 배율 (3 → 6 → 12배) = 조준경을 보면서 휠
    G                : 수류탄 던지기
    V                : 칼 공격
    1 ~ 9            : 무기 바꾸기 = 휠
                       (소총/권총/저격총/산탄총/기관단총/로켓/기관총/점사 소총/지정사수 소총)
    X                : 킬스트릭 쓰기 (죽지 않고 3킬 레이더 / 5킬 공습 / 7킬 자동 포탑)
    Q                : 방금 쓰던 무기로
    R                : 재장전
    H                : 도움말 (보는 동안 일시정지)
    M                : 소리 끄기 / 켜기
    P 또는 F3        : FPS와 화면 선명도 표시
    Enter 또는 F11   : 전체 화면 (컴퓨터에서 실행할 때)
    ESC              : 종료 (메뉴로)

시작 화면:
    Enter : 새 게임    C : 이어하기    T : 해상도 바꾸기 (컴퓨터에서)

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
import asyncio
import math
import random
import sys
import time

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

# 고를 수 있는 해상도. 화면보다 큰 해상도는 전체 화면으로 열어요
RESOLUTIONS = [(1280, 720), (1600, 900), (1920, 1080)]


def set_resolution(width, height):
    """해상도를 바꿔요. 화면 크기에 따라 정해지는 값들도 같이 다시 계산해요."""
    global WIDTH, HEIGHT, UI, LOOK_SPEED, MAX_PITCH
    WIDTH, HEIGHT = width, height
    UI = HEIGHT / 600
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
                   "ROCKET": 0.01, "LMG": 0.006, "BURST": 0.004, "DMR": 0.008}

# 경험치: 1000마다 계급(RANK)이 올라가요
XP = dict(kill=100, headshot=50, knife=50, boss=500, double=50, triple=100, multi=150, round=250)
XP_PER_RANK = 1000

GRENADES_START, GRENADES_MAX = 3, 6
GRENADE_FUSE = 1.8                # 던지고 터질 때까지(초)
GRENADE_THROW = 9.0               # 던지는 힘
GRENADE_BLAST = (3.2, 160)        # (폭발 반경, 가운데 피해)
ROCKET_SPEED = 16.0
ROCKET_BLAST = (2.8, 300)
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
}

# ---------------------------------------------------------------
# 맵 6개: 라운드마다 바뀌어요 (1 → 2 → ... → 6 → 1 ...)
# ---------------------------------------------------------------
#   바닥   '~' 바다(못 들어가요)  '.' 모래사장  '_' 보드워크  ':' 인도  '=' 차도
#          'g' 잔디  'x' 광장 타일  ',' 부두 콘크리트  'p' 나무 부두
#          ';' 사막 모래  '#' 흙길  '*' 눈  '-' 다져진 눈길
#   건물   'A' 분홍 호텔  'B' 민트 건물  'C' 노란 가게  'D' 하얀 아르데코 호텔
#          'R' 붉은 벽돌  'N' 나이트클럽  'G' 유리 오피스 타워  'S' 마천루
#          'W' 창고  'r' 'u' 'o' 빨강/파랑/주황 컨테이너  'Y' 두 층으로 쌓인 컨테이너
#          'M' 흙벽돌 집  'O' 콘크리트 벙커  'U' 연료 탱크  'J' 나무집  'V' 돌담  'Z' 모래주머니
#          'K' 나무 상자  'Q' 쓰레기통  'F' 분수/동상  (K Q F Z V 와 컨테이너는 엄폐물)
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
#   op / brief : 라운드 시작 때 나오는 작전 이름과 임무
MAPS = [
    dict(
        name="NEON BEACH",
        sky=[(0.0, (40, 30, 90)), (0.55, (150, 70, 140)), (0.85, (245, 120, 120)), (1.0, (250, 170, 140))],
        haze=(250, 170, 140), sun=math.pi, stars=False, ground=".", lit=4, fog=1.0, snow=False, camo=None,
        op="OPERATION SUNSET", brief="Hostiles have taken the boardwalk. Clear the beach district.",
        rows=[
            "~~~.T_:==:DDDDDxRRR:==:GGGG:CCCCC:GG",
            "~~~.._L==:DxxxxxRRR:==:GGGG:CCCCC:GG",
            "~~~.E_:=c:DxFFxxxaR:==:GGGG:::K:::GG",
            "~~~.._:==:DxFFxExxR:==:GGGGE:NNNN:GG",
            "~~~.T_:==:DxxxxxxxR:c=:::::::NNNN:GG",
            "~~~.._:==:DDDxDDQxR:==:AAAA:hNNNN:GG",
            "~~~..h:==LDDDxDDDxR:==:AAAA:KNNNN:GG",
            "~~~.._:==:::::::::::==::::::::::::GG",
            "~~~.T_======c==============c========",
            "~~~.._==========c=============c=====",
            "~~~..E:==:::::::::::==::::::::::::GG",
            "~~~.._L==:BBBBc:c:c:==:ggTgggg:NN:GG",
            "~~~.P_:==:BBBB:::E::==:gggFFgg:NN:GG",
            "~~~.._:c=:BBBB:Ka:::==:gEgFFgh:NN:GG",
            "~~~.T_:==:BBBB:c:c::==LggTggTg:NN:GG",
            "~~~.._:==:CCCCCCCC::==:ggggggEgNN:GG",
            "~~~.n_:==:::::::::::==::::::::::::GG",
            "~~~.._========c=========c===========",
            "~~~.T_=============c============c===",
            "~~~.._:==:::::::::::==::::::::::::GG",
            "~~~.._:==:KK:K:KK:R:==:CC:AA:BB:D:GG",
            "~~~.E_L==::::K:::KR:==:CC:AA:BB:D:GG",
            "~~~.._:==:K:E:K:K:R:=c:::::E::::::GG",
            "~~~.T_:==:K:KKK:n:R:==:CC:AA:BB:D:GG",
            "~~~.._:==::::::K::R:==:CCh:A:BB:D:GG",
            "~~~.T_:=c:RRRRRRRRR:==:CCCAAABBBD:GG",
        ],
    ),
    dict(
        name="DOWNTOWN",
        sky=[(0.0, (8, 8, 30)), (0.6, (30, 20, 70)), (0.9, (90, 40, 110)), (1.0, (130, 60, 130))],
        haze=(70, 40, 95), sun=None, stars=True, ground=":", lit=2, fog=1.0, snow=False, camo=None,
        op="OPERATION NIGHTFALL", brief="Enemy snipers on the high-rises. Move fast between cover.",
        rows=[
            "SSSSS:==:GGGGGG:==:NNNEAA:==:SSS",
            "SSSSSL==:Gxxxx::==:NNNhAA:==:SSS",
            "SS::::==:GxFFx::==T::E::::==:SSS",
            "SS:a::==:GxbxxE:==:AAA:NN:==:::E",
            "SSSSST==:GGG:GG:==:AAA:NN:==:SSS",
            "SSSSS:==:GGG:GG:==LAAA:NN:==:SSS",
            "::::::==::::::::==::::::::==::E:",
            "===========c=========c==========",
            "==P==========================c==",
            "::::::==::::::::==::::::::==::::",
            "c:c:c:==:gggggg:==:xxxxxx:==:BBB",
            "::::E:==TgTggbg:==:xbxxbxL==:BBB",
            ":c:c::==:ggFFgg:==:xxKKxx:==::a:",
            "::::n:==:gEFFgg:==:xxKKxE:==:BBB",
            "c:c:c:==LgggTgg:==:xbxxbxT==:BBB",
            "RRRRR:==:gggggg:==:xxxxxx:==:BBB",
            "::::::==::::E:::==::::::::==::::",
            "=======c================c=======",
            "=============c================c=",
            "::::::==::::::::==::::E:::==::::",
            "CCCCC:==:DDD:DD:==:RR:RRR:==LSSS",
            ":::E:L==:DDD:DD:==:RR:RRR:==:SSS",
            "CCCCC:==:DDDEDD:==:RRnRRR:==:SSS",
            "CCCCC:==:DDDDDD:==:RRRRRR:==TSSS",
        ],
    ),
    dict(
        name="HARBOR",
        sky=[(0.0, (60, 100, 165)), (0.6, (140, 165, 200)), (0.9, (250, 190, 140)), (1.0, (255, 215, 170))],
        haze=(225, 205, 185), sun=0.0, stars=False, ground=",", lit=6, fog=1.0, snow=False, camo=None,
        op="OPERATION TIDEWATER", brief="Secure the container yard before the shipment leaves.",
        rows=[
            "~~~~~~pp~~~~~~~~pp~~~~~~~~pp~~~~",
            "~~~~~~pp~~~~~~~~pp~~~~~~~~pp~~~~",
            "~~~~~~pE~~~~~~~~pp~~~~~~~~Ep~~~~",
            "~~~~~~pp~~~~~~~~pa~~~~~~~~pp~~~~",
            "~~~,,,,,,,,,,,,,,,,,,,,,,,,,E,,,",
            "~~~,X,,,,,,,X,,,,,,,,,X,,,,,,,L,",
            "~~~,,rrr,uuu,,ooo,rrr,,uuu,YY,,,",
            "~~~,,rrr,uuu,,ooo,rrr,,uuu,YY,a,",
            "~~~,,,,,,,,,,E,,,,,,,,,,,,,,,,,,",
            "~~~,,YYY,ooo,,uuu,,K,,rrr,ooo,,,",
            "~~~,,YYY,ooo,,uuu,,KE,rrr,ooo,,,",
            "~~~,,,,,,,,,,,,,,,,,E,,,,,,,,,n,",
            "~~~,,uu,rr,oo,,YY,,,,uu,rr,,E,,,",
            "~~~=============================",
            "~~~=======E=====c========c======",
            "~~~,,,L,,,,,,L,,,,,,L,,,,,,L,,,,",
            "~~~,WWWWW,,WWWWW,,BBBB,,c,c,c,,,",
            "~~~,WWWWW,,WWWWW,,BBBB,,,,,,,E,,",
            "~~~,WWWWW,,WWWWW,,BBBB,,c,c,c,,,",
            "~~~,,,,,,,E,,,,,,,,,,,,,,,,,,,E,",
            "~~~,,,QQ,KK,K,,QQ,,,h,,,,KK,,,,,",
            "~~~,P,,,,,,,,,,,,,,,,,,E,,,,,,,,",
            "~~~WWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
            "~~~WWWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        ],
    ),
    dict(
        name="DESERT TOWN",
        sky=[(0.0, (60, 110, 190)), (0.6, (130, 175, 225)), (0.9, (225, 215, 185)), (1.0, (240, 225, 195))],
        haze=(235, 220, 190), sun=-math.pi / 2, stars=False, ground=";", lit=9, fog=1.1, snow=False,
        camo=dict(uniform=(185, 160, 110), vest=(150, 125, 85), pants=(165, 140, 100)),
        op="OPERATION SANDSTORM", brief="Insurgents are holed up in the old town. Check every courtyard.",
        rows=[
            ";;;;;;;;;;;;E;;##;;;;;;;;;;;;;;;",
            ";MMMMMM;MMMMM;;##;MMMMM;MMMMMMM;",
            ";M;a;;M;M;;;M;;##;ME;nM;M;;;;EM;",
            ";M;;;;M;;;h;M;;##;M;;;M;;;;a;;M;",
            ";MM;MMM;M;;;M;;##;MM;MM;M;;;;;M;",
            ";;;;;;;;MMMMM;;v#;;;;;;;MMM;MMM;",
            ";MMMM;;;;;;;;T;##;MMMM;;;;;;;;;;",
            ";MMMM;MMM;MMM;;##;MMMM;;;K;K;;;;",
            ";MMMM;M;;E;;M;;##;MMMM;;;E;;;K;;",
            ";MMMM;MMMMMMM;;##;MMMM;;;;K;K;;;",
            ";;;;;;;;;;;;;ZZ##;;T;;;;;;;;;;;;",
            "P####v######################v###",
            "######################v#######E#",
            ";;;;;;;T;;;;;;;##ZZ;;;;;;;;E;;T;",
            ";MMMMM;;MMMMMM;##;MMMMM;;MMMMM;;",
            ";M;;;M;;M;;n;M;##;M;;;;;;;;;;M;;",
            ";M;h;;;;MM;MMM;##;M;ZZ;;a;ZZ;M;;",
            ";ME;;M;;;;;;;;;##;M;;;;K;;;;;M;;",
            ";MMMMM;;;;;;;;;##;M;;E;;K;;;;M;;",
            ";;;;;;;;;MMMMM;#v;M;ZZ;;;;ZZ;M;;",
            ";MM;MMM;;MMMMM;##;M;;;;;;;;;EM;;",
            ";M;E;;M;;MMMMM;##;MMMMM;;MMMMM;;",
            ";MMMMMM;;MMMMM;#E;;;;;;;;;;;;;;;",
            ";;;;;;;;;;;;;;;##;;;;;;;;;;;;;;;",
        ],
    ),
    dict(
        name="SNOW BASE",
        sky=[(0.0, (10, 15, 35)), (0.6, (35, 50, 80)), (0.9, (90, 110, 140)), (1.0, (150, 165, 185))],
        haze=(150, 165, 185), sun=None, stars=True, ground="*", lit=3, fog=0.8, snow=True,
        camo=dict(uniform=(225, 228, 232), vest=(165, 170, 180), pants=(200, 205, 212)),
        op="OPERATION WHITEOUT", brief="Infiltrate the arctic base. Watch the bunkers.",
        rows=[
            "II*I******-***********-*****I*I*",
            "*****I**E*-***********-*********",
            "**OOOOOO**-*WWWWWWWW**-*UU*****I",
            "I*OOOOOO**-*W*E****W**-*UU**UU**",
            "**OOOOOO**-*W*h****W**-*****UU**",
            "**OOOOOO**-*WWW**WWW**-*********",
            "**********-***********-******E**",
            "*****a****-********E*Z-****a****",
            "------c-------------------------",
            "**********-Z**********-*********",
            "**JJJJJJ**-*OOOOOOOO**-**OOOOO**",
            "**J**E*J**-*O******O**-**OOOOO**",
            "**Ja***J**-****Kn*****-**OOOOO**",
            "**JJ*JJJ**-*O****E*O**-**OOOOO**",
            "**********-*OOOOOOOO**-***E***n*",
            "**********-***********-Z********",
            "P--------------------------c----",
            "*********Z-***********-*********",
            "**ZZZ*****-**ZZ*******-***ZZZ*E*",
            "**********-*********E*-*WWWWW***",
            "*******ZZ*-******h****-*WWWWW***",
            "***E******-*E*****ZZ**-*WWWWW*I*",
            "I*********-***********-*****E***",
            "******I***-***********-**I*****I",
        ],
    ),
    dict(
        name="FOREST VILLAGE",
        sky=[(0.0, (85, 110, 140)), (0.6, (145, 165, 175)), (0.9, (195, 205, 195)), (1.0, (205, 212, 202))],
        haze=(190, 200, 190), sun=None, stars=False, ground="g", lit=5, fog=0.6, snow=False,
        camo=dict(uniform=(70, 95, 55), vest=(50, 70, 40), pants=(60, 70, 50)),
        op="OPERATION GREENWOOD", brief="Enemy squad spotted near the village. Use the trees for cover.",
        rows=[
            "ggggIggggggggggggggI~~ggggg#gggg",
            "gIgIgIIggggggggEIgIg~~ggggg#gggg",
            "ggggggggEIggIggggIgg~~gIgEg#gJJJ",
            "gggggggggggIgIgIgggg~~ggggg#ggaJ",
            "ggggggggggggggggggIg~~ggggg#gJEJ",
            "ggggggggggggIggIgggg~~ggggg#IJJJ",
            "####################pp##########",
            "ggggggggg#gggggggEgg~~ggggg#gggg",
            "ggggggggg#gJJJJJgggg~~gIggg#Iggg",
            "ggVgIIggg#gJaggJJJJg~~gJJJJ#gggg",
            "ggVghgggg#gJggEJJgJg~~gJngJ#gggg",
            "IgVgggggg#gJJgJJJggg~~gJgEg#gggg",
            "ggVgggggg#ggggggJhJg~~gJJJJ#gggg",
            "ggVVVVVVg#gJJJJgJJJg~~ggggg#ggEg",
            "ggIgggIgg#gJJJJggggg~~ggggg#gggg",
            "ggggggggg#gJJJJggggg~~ggEIg#gggg",
            "P###################pp##########",
            "gggggggggggggggggggg~~gggIg#gggg",
            "ggggEgggggggEgggggIg~~gJJJg#gggg",
            "gggggggggIIggggggggg~~gJJJI#gggg",
            "gIggggggggVVVVVVgggg~~gJJJg#gEgg",
            "ggggggggggggaggggggg~~ggggg#gggg",
            "gggggggggggggggggggg~~Igggg#ggIg",
            "gggIggIggggggggggggg~~ggggg#gggg",
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


def load_map(index):
    """index번째 맵으로 바꿔요. 다른 함수들이 쓰는 맵 정보(전역 변수)를 새로 채워요."""
    global GAME_MAP, MAP_W, MAP_H, FLOOR_GRID, WALL_GRID, MAX_WALL, HAZE, LIT
    theme = MAPS[index]
    GAME_MAP = theme["rows"]
    MAP_W, MAP_H = len(GAME_MAP[0]), len(GAME_MAP)
    # 매번 계산하지 않도록 칸마다 바닥/건물 정보를 미리 만들어 둬요
    FLOOR_GRID = [[floor_of(col, row) for col in range(MAP_W)] for row in range(MAP_H)]
    WALL_GRID = [[WALLS.get(ch) for ch in line] for line in GAME_MAP]
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
                walls.append((dist, vertical, hit - math.floor(hit), spec, map_x, map_y))
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


load_map(0)       # 처음엔 첫 번째 맵


# ---------------------------------------------------------------
# 그림 만들기 (이미지 파일 없이 도형으로 그려요)
# ---------------------------------------------------------------
def make_enemy_image(look, state="normal"):
    """적 그림. state: normal(평소) / flash(총구 불꽃) / hurt(맞음) / aim(저격 조준 불빛)"""
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
    if state == "flash":
        pygame.draw.circle(img, YELLOW, (min(59, gun_x + gun), 55), 8)            # 총구 불꽃
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


def make_hurt_vignette():
    """다쳤을 때 화면 가장자리가 붉게 물드는 그림 (가운데는 투명)"""
    img = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    steps = 24
    for i in range(steps):
        t = i / steps
        alpha = int(170 * (1 - t) ** 2)
        pad_x, pad_y = int(WIDTH * 0.22 * t), int(HEIGHT * 0.22 * t)
        pygame.draw.rect(img, (140, 0, 0, alpha), (pad_x, pad_y, WIDTH - 2 * pad_x, HEIGHT - 2 * pad_y),
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
    "reload":    (0.05, 80, 1.0, 0.90, 0, 0, 2000, 0.3, 0.40),
    "streak":    (0.30, 6, 0.0, 0.0, 0, 0, 880, 0.6, 0.50),
    "knife":     (0.20, 12, 1.0, 0.70, 0, 0, 0, 0, 0.30),
    "throw":     (0.15, 15, 1.0, 0.60, 0, 0, 0, 0, 0.25),
    "hurt":      (0.12, 20, 0.6, 0.20, 0, 0, 220, 0.5, 0.40),
}
# 총 이름 -> 총소리
GUN_SOUNDS = {"RIFLE": "rifle", "PISTOL": "pistol", "SNIPER": "sniper", "SHOTGUN": "shotgun", "SMG": "smg",
              "ROCKET": "rocket", "LMG": "lmg", "BURST": "rifle", "DMR": "dmr"}


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
            rng = random.Random(1)
            for name, recipe in SOUND_RECIPES.items():
                self.bank[name] = self.synth(freq, channels, rng, *recipe)
        except Exception:
            self.bank = {}

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

    def play(self, name, volume=1.0):
        sound = self.bank.get(name)
        if sound and not self.muted and volume > 0.02:
            channel = sound.play()
            if channel:
                channel.set_volume(min(1.0, volume))


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
              ("F", "사격 (꾹 누르면 연사)"), ("E", "정조준 / 저격총 조준경"), ("Z", "조준경 배율 3·6·12배"),
              ("G", "수류탄"), ("V", "칼"), ("X", "킬스트릭 쓰기"), ("1 ~ 9,  Q", "무기 바꾸기,  직전 무기"),
              ("R", "재장전"), ("H,  M", "도움말 (일시정지),  소리 끄기"), ("P,  Enter", "FPS 표시,  전체 화면"),
              ("ESC", "메뉴로")],
        tips=["적을 모두 쓰러뜨리면 다음 라운드! 라운드마다 맵이 바뀌어요.",
              "죽지 않고 연속으로 쓰러뜨리면 킬스트릭: 3킬 레이더, 5킬 공습, 7킬 자동 포탑 (X).",
              "처치·헤드샷·연속 처치로 경험치를 모으면 계급(RANK)이 올라가요.",
              "앉으면 덜 맞고 잘 맞혀요. 차·상자 뒤에 숨으면 총알을 막아요.",
              "GRENADE! 경고가 뜨면 빨리 피하세요. 방패병은 머리나 옆을 노리세요.",
              "5라운드마다 보스가 나와요.",
              "죽으면 R: 그 라운드부터 다시,  N: 처음부터"],
        resume="H 를 누르면 계속해요",
    ),
    "en": dict(
        title="HOW TO PLAY",
        keys=[("W A S D", "move"), ("SHIFT", "sprint (with W)"), ("C", "crouch / slide while sprinting"),
              ("ARROWS", "look (or mouse)"), ("SPACE", "jump"),
              ("F", "fire (hold for auto)"), ("E", "aim / sniper scope"), ("Z", "scope zoom 3/6/12x"),
              ("G", "grenade"), ("V", "knife"), ("X", "use killstreak"), ("1-9, Q", "weapons, last weapon"),
              ("R", "reload"), ("H, M", "help (pause), mute"), ("P, ENTER", "show FPS, fullscreen"), ("ESC", "menu")],
        tips=["Kill every enemy to clear the round. The map changes each round.",
              "Killstreaks without dying: 3 radar, 5 airstrike, 7 sentry turret (X).",
              "Kills, headshots and multi-kills give XP. Rank up every 1000 XP.",
              "Crouch to be harder to hit. Cars and crates stop bullets.",
              "GRENADE! warning: move away. Shield guys: aim for the head or flank.",
              "A boss shows up every 5 rounds.",
              "When you die: R retry the round, N new game."],
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
        y += line_h * 0.4

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
# 등장인물과 물건들
# ---------------------------------------------------------------
class Enemy:
    def __init__(self, x, y, kind):
        self.kind = kind
        self.t = ENEMY_TYPES[kind]           # 이 종류의 능력치
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

    @property
    def aiming(self):
        """저격수가 곧 쏠 때 True (빨간 불빛으로 미리 알려줘요)"""
        return self.kind == "SNIPER" and self.sees and self.spotted > 0.4 and self.shoot_timer < 0.8

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
            self.facing = pygame.Vector2(self.dir)
            return 0

        # 봤을 때: 플레이어 쪽을 보고, 너무 멀면 다가오고, 반응 시간이 지나면 공격
        self.spotted += dt
        if dist > 0:
            self.facing = (player.pos - self.pos).normalize()
        if dist > t["keep"]:
            move_with_collision(self.pos, self.facing * t["speed"] * dt)
        if self.spotted < t["reaction"]:
            return 0

        # 수류탄 던지기 (폭탄병, 보스)
        throw = t.get("throw")
        if throw and t["throw_range"][0] <= dist <= t["throw_range"][1]:
            self.throw_timer -= dt
            if self.throw_timer <= 0:
                self.throw_timer = random.uniform(*throw)
                self.throw_at = pygame.Vector2(player.pos)

        if dist > t["range"]:
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
        if player.crouch_amt > 0.5:
            chance -= 0.1
        if player.sprinting or player.slide_timer > 0:
            chance -= 0.1
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
        self.sprinting = False
        self.crouch = False       # 앉아 있는지
        self.crouch_amt = 0.0     # 앉은 정도 0(서 있음) ~ 1(앉음). 부드럽게 바뀌어요
        self.slide_timer = 0.0    # 슬라이딩 남은 시간
        self.slide_dir = pygame.Vector2(1, 0)

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

    def __init__(self, spec):
        self.spec = spec
        self.mag = spec["mag"]
        self.reserve = spec["reserve"]


class Arsenal:
    """가지고 있는 무기들과 사격/재장전/반동/무기 교체, 수류탄 개수를 관리"""

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
            self.reload_left = w.spec["reload"]

    def add_ammo(self):
        """탄약 상자: 모든 무기의 여분 총알을 채워요. 하나라도 채웠으면 True"""
        added = False
        for w in self.weapons:
            cap = w.spec["reserve"] * 2
            if w.reserve < cap:
                w.reserve = min(cap, w.reserve + max(1, w.spec["reserve"] // 2))
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
    """야자수, 자동차, 가로등 같은 장식물. cover=True면 총알을 막아요."""

    def __init__(self, x, y, image, height, width, cover=False):
        self.pos = pygame.Vector2(x, y)
        self.image = image
        self.height = height
        self.width = width
        self.cover = cover


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
        if kind == "rocket":
            self.timer = 4.0
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
            elif self.rocket_step(sdt, enemies):
                return True
        return self.timer <= 0

    def bounce_step(self, sdt):
        """수류탄: 중력으로 떨어지고, 벽과 바닥에 튕겨요."""
        self.vz -= GRAVITY * sdt
        nx = self.pos.x + self.vel.x * sdt
        if obstacle_height(nx, self.pos.y) > self.z:
            self.vel.x *= -0.5
        else:
            self.pos.x = nx
        ny = self.pos.y + self.vel.y * sdt
        if obstacle_height(self.pos.x, ny) > self.z:
            self.vel.y *= -0.5
        else:
            self.pos.y = ny
        self.z += self.vz * sdt
        if self.z < 0:
            self.z = 0.0
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

    def __init__(self, enemy, push):
        self.pos = pygame.Vector2(enemy.pos)
        self.kind = enemy.kind
        self.vel = push                       # 밀려나는 속도
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
    def __init__(self, save, start_round=1):
        """save: 저장 정보(dict). 라운드를 깨거나 죽을 때마다 고쳐서 파일에 써요."""
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
        self.muzzle_light = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.muzzle_light.fill((255, 220, 150, 28))
        self.scope_overlay = make_scope_overlay()
        self.sounds = get_sounds()
        self.was_reloading = False
        self.fonts = make_fonts()
        self.font, self.big_font, self.small_font = self.fonts["normal"], self.fonts["big"], self.fonts["small"]
        self.save = save
        self.xp = save.get("xp", 0)
        self.map_index = None
        self.set_col_w(START_COL_W)
        self.fire_was_down = False
        self.aim_on = False        # E 키로 켠 정조준
        self.show_fps = False      # P 또는 F3
        self.show_help = False     # H
        self.fps = 0.0
        self.reset(start_round)

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

    def setup_map(self, index):
        """맵 바꾸기: 맵 정보, 장식물, 적 출현 위치, 미니맵, 하늘을 새로 만들어요."""
        load_map(index)
        self.map_index = index
        self.theme = MAPS[index]
        self.decor = []
        images = dict(self.decor_images)
        if self.theme["snow"]:
            images["I"] = self.snowy_pine
        sizes = {"T": (2.4, 1.2), "L": (1.9, 0.3), "X": (5.5, 3.0), "b": (2.6, 1.8), "I": (2.6, 1.3)}
        for letter, (height, width) in sizes.items():
            self.decor += [Decor(x, y, images[letter], height, width) for x, y in find_cells(letter)]
        self.decor += [Decor(x, y, images["v"], 0.6, 1.1, cover=True) for x, y in find_cells("v")]
        # 적 그림: 맵에 맞는 위장복으로 다시 그려요 (일반병, 저격수)
        camo = self.theme["camo"]
        self.enemy_images = {}
        for kind, t in ENEMY_TYPES.items():
            look = dict(t["look"], **camo) if camo and kind in ("GRUNT", "SNIPER") else t["look"]
            for state in ("normal", "flash", "hurt", "aim"):
                self.enemy_images[(kind, state)] = make_enemy_image(look, state)
        # 쓰러지는 모습: 서 있는 그림을 25도, 55도, 90도로 기울인 그림 (왼쪽/오른쪽)
        self.corpse_frames = {}
        for kind, t in ENEMY_TYPES.items():
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
        self.minimap = self.make_minimap()
        self.sky = make_sky(self.theme)

    def reset(self, start_round=1):
        """새 게임 (또는 저장된 라운드부터 시작)"""
        self.round = start_round
        self.kills = 0
        self.game_over = False
        self.hint_timer = 8.0      # 처음 8초 동안 화면 아래에 조작법 안내
        self.reset_streak()
        self.start_round()

    def reset_streak(self):
        """킬스트릭(죽지 않고 연속 처치)은 죽으면 처음부터 다시 세요"""
        self.streak = 0
        self.streaks_ready = []    # 받은 킬스트릭 (X로 하나씩 써요)

    def retry_round(self):
        """죽은 라운드부터 다시 (처치 수는 그대로)"""
        self.game_over = False
        self.reset_streak()
        self.start_round()

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
        return random.choice(pool)

    def start_round(self):
        index = (self.round - 1) % len(MAPS)
        if index != self.map_index:
            self.setup_map(index)
        start = find_cells("P")[0]
        self.player = Player(*start)
        self.arsenal = Arsenal()
        far = [p for p in self.spawn_points if self.player.pos.distance_to(p) > SAFE_SPAWN]
        count = min(len(far), 2 + self.round)
        self.enemies = [Enemy(*p, self.pick_enemy_kind()) for p in random.sample(far, count)]
        # 새로운 적이 처음 나오는 라운드에는 그 적이 꼭 한 명은 있게. 5라운드마다 보스
        news = {2: "SNIPER", 3: "HEAVY", 4: "BOMBER", 6: "SHIELD"}
        special = "BOSS" if self.round % 5 == 0 else news.get(self.round)
        if special:
            first = self.enemies[0]
            self.enemies[0] = Enemy(first.pos.x, first.pos.y, special)
        # 맵에 놓인 상자는 라운드마다 다시 채워져요
        self.pickups = [Pickup(x, y, kind) for letter, kind in PICKUP_TILES.items()
                        for x, y in find_cells(letter)]
        self.projectiles = []
        self.effects = []
        self.banner = f"ROUND {self.round}"
        self.sub_banners = [(f"{self.theme['op']}  -  {self.theme['name']}", WHITE)]
        self.brief_age = 0.0       # 임무 설명이 타자 치듯 나와요
        if special == "BOSS":
            self.sub_banners.append(("BOSS ROUND!", RED))
        elif special:
            self.sub_banners.append((f"NEW ENEMY: {special}", RED))
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

    @property
    def rank(self):
        return 1 + self.xp // XP_PER_RANK

    def add_xp(self, amount, text=None, color=YELLOW):
        """경험치 추가. 계급이 오르면 크게 알려줘요."""
        before = self.rank
        self.xp += amount
        self.save["xp"] = self.xp
        if text:
            self.popups.append([text, color, 1.4])
        if self.rank > before:
            self.popups.append([f"RANK UP!  RANK {self.rank}", (255, 80, 200), 2.5])

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
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_p, pygame.K_F3):
            self.show_fps = not self.show_fps
        if event.type == pygame.KEYDOWN and event.key == pygame.K_h and not self.game_over:
            self.show_help = not self.show_help
        if self.game_over or self.show_help:
            return
        a = self.arsenal
        if event.type == pygame.MOUSEWHEEL:
            if self.scoped:      # 조준경을 보고 있으면 휠로 확대/축소
                a.zoom_index = max(0, min(len(SCOPE_ZOOMS) - 1, a.zoom_index + event.y))
            else:
                a.switch(a.index - event.y)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:            # 소리 끄기/켜기
                self.sounds.muted = not self.sounds.muted
                self.popups.append(["SOUND OFF" if self.sounds.muted else "SOUND ON", WHITE, 1.0])
            elif pygame.K_1 <= event.key <= pygame.K_9:
                a.switch(event.key - pygame.K_1)
            elif event.key == pygame.K_q:
                a.switch(a.last_index)
            elif event.key == pygame.K_r:
                a.reload()
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

    # ----- 게임 진행 -----
    def update(self, dt, keys, mouse_dx, mouse_dy, buttons):
        if self.show_help:          # 도움말을 보는 동안은 멈춰요
            return
        self.banner_timer -= dt
        self.brief_age += dt
        self.hint_timer -= dt
        self.damage_flash = max(0.0, self.damage_flash - dt * 2)
        self.hitmarker = max(0.0, self.hitmarker - dt)
        self.shake = max(0.0, self.shake - dt)
        # 폭발 흔들림: 이번 장면에서 화면이 위아래로 움직일 양
        self.shake_offset = random.uniform(-1, 1) * self.shake * 30 * UI
        self.feed = [[text, t - dt] for text, t in self.feed if t - dt > 0]
        self.popups = [[text, color, t - dt] for text, color, t in self.popups if t - dt > 0]
        self.damage_dirs = [[a, t - dt] for a, t in self.damage_dirs if t - dt > 0]
        self.time += dt
        for effect in self.effects:
            effect.age += dt
        self.effects = [e for e in self.effects if not e.done]
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
        if arsenal.index != self.seen_index:       # 무기를 바꾸면 정조준과 점사 멈추기
            self.seen_index = arsenal.index
            self.aim_on = False
            self.burst_left = 0
        self.knife_timer = max(0.0, self.knife_timer - dt)
        self.knife_cooldown = max(0.0, self.knife_cooldown - dt)
        fire_down = buttons[0] or keys[pygame.K_f]
        self.aiming = (bool(buttons[2] or self.aim_on) and not arsenal.busy
                       and self.knife_timer == 0 and not self.player.sprinting)
        speed = (AIM_MOVE if self.aiming else 1.0) * spec.get("move", 1.0)
        self.player.update(dt, keys, mouse_dx, mouse_dy, min(1.0, 1.5 / self.zoom), speed,
                           allow_sprint=not self.aiming and not fire_down)
        arsenal.update(dt)
        if arsenal.reload_left > 0 and not self.was_reloading:
            self.sounds.play("reload")
        self.was_reloading = arsenal.reload_left > 0
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
            self.sounds.play(GUN_SOUNDS[spec["name"]])
            self.on_fire(spec)
            if spec["projectile"]:
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
                self.sounds.play(GUN_SOUNDS[spec["name"]])
                self.on_fire(spec)
                self.shoot(spec)
                arsenal.add_recoil()
                self.burst_left -= 1
                self.burst_timer = spec["burst_delay"]

        for enemy in self.enemies:
            damage = enemy.update(dt, self.player)
            if enemy.flash_timer == 0.08:          # 방금 쐈어요: 멀수록 작게 들려요
                self.sounds.play("enemy", 1 - enemy.pos.distance_to(self.player.pos) / 22)
            if damage:
                self.hurt_player(damage, enemy.pos)
            if enemy.throw_at is not None:
                self.enemy_throw(enemy, enemy.throw_at)
                enemy.throw_at = None

        self.update_projectiles(dt)
        self.update_streaks(dt)
        self.update_effects(dt)
        self.collect_pickups()

        if self.player.hp <= 0:
            self.player.hp = 0
            self.game_over = True
            self.record_progress(self.round)          # 다음에 이 라운드부터 이어할 수 있게
        elif not self.enemies:
            self.round_clear_timer = 2.5
            self.banner = "ROUND CLEAR"
            self.sub_banners = []
            self.banner_timer = 2.5
            self.add_xp(XP["round"], f"ROUND CLEAR  +{XP['round']}")
            self.record_progress(self.round + 1)

    def on_fire(self, spec):
        """쏠 때마다: 조준이 옆으로 살짝 튀고, 화면이 번쩍이고, 탄피가 튀어나와요"""
        self.player.angle += random.uniform(-1, 1) * HORIZONTAL_KICK.get(spec["name"], 0.005)
        self.light_timer = 0.05
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

    def add_splat(self, pos, size):
        self.splats.append([pygame.Vector2(pos), size])
        if len(self.splats) > MAX_SPLATS:
            self.splats.pop(0)

    def hurt_player(self, damage, source=None):
        """나에게 피해. source(때린 위치)가 있으면 화면에 맞은 방향을 표시해요."""
        self.player.hp -= int(damage)
        self.since_hurt = 0.0
        self.damage_flash = min(1.0, 0.4 + damage / 40)
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
        if self.player.slide_timer > 0:
            spread += 12
        elif self.player.crouch_amt > 0.5:
            spread *= 0.75                         # 앉으면 덜 퍼져요
        return spread * UI

    def damage_enemy(self, enemy, amount, how):
        """적에게 피해 주기. 쓰러지면 킬 로그에 남기고 상자를 떨어뜨려요."""
        enemy.hp -= amount
        enemy.hurt_timer = 0.08
        enemy.spotted = max(enemy.spotted, enemy.t["reaction"])   # 맞으면 바로 반격
        enemy.sees = True
        if how not in STREAK_KILLS:
            self.sounds.play("hit")
        # 움찔: 잠깐 못 쏘고 뒤로 살짝 밀려요
        enemy.shoot_timer = max(enemy.shoot_timer, 0.2)
        away = enemy.pos - self.player.pos
        away = away.normalize() if away.length() > 0 else pygame.Vector2(1, 0)
        move_with_collision(enemy.pos, away * 0.06)
        self.hitmarker = 0.18
        self.hitmarker_kill = enemy.hp <= 0
        self.hit_head = how == "HEADSHOT!"
        if enemy.hp <= 0 and enemy in self.enemies:
            self.enemies.remove(enemy)
            self.corpses.append(Corpse(enemy, away * (3.0 if how in ("BOOM!", "AIRSTRIKE!") else 1.6)))
            if len(self.corpses) > MAX_CORPSES:
                self.corpses.pop(0)
            self.kills += 1
            self.feed.append([f"{enemy.kind} {how}", 2.5])
            self.on_kill(enemy, how)
            if enemy.kind == "BOSS":               # 보스는 상자를 잔뜩 떨어뜨려요
                for i, kind in enumerate(("ammo", "health", "grenade", "health")):
                    offset = pygame.Vector2(0.5, 0).rotate(i * 90)
                    self.pickups.append(Pickup(enemy.pos.x + offset.x, enemy.pos.y + offset.y, kind))
            elif random.random() < DROP_CHANCE:
                kind = random.choices(list(DROP_WEIGHTS), weights=list(DROP_WEIGHTS.values()))[0]
                self.pickups.append(Pickup(enemy.pos.x, enemy.pos.y, kind))

    def on_kill(self, enemy, how):
        """처치 보상: 경험치, 연속 처치 메달, 킬스트릭"""
        self.sounds.play("headshot" if how == "HEADSHOT!" else "kill")
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
            for need, name in STREAKS:
                if self.streak == need:
                    self.streaks_ready.append(name)
                    self.sounds.play("streak")
                    self.popups.append([f"{name} READY!  press X", (80, 240, 255), 2.5])

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
        """체력 회복, 튀는 피와 탄피, 쓰러지는 적, 심장 박동"""
        p = self.player
        self.since_hurt += dt
        self.light_timer = max(0.0, self.light_timer - dt)
        if self.since_hurt > REGEN_DELAY and 0 < p.hp < 100:
            p.hp = min(100, p.hp + REGEN_RATE * dt)
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
            if corpse.age < 0.35:               # 넘어지면서 밀려나요
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
            if target and self.blocked_by_cover(ax, ay, target_dist):
                target = None                     # 자동차에 막힘
            if target:
                amount = spec["head"] if head else spec["body"]
                if not head and target.shield_blocks(self.player.pos):
                    amount *= 0.15                # 방패에 막힘
                damage[target] = damage.get(target, 0) + amount
                if head:
                    headshots.add(target)
                if amount > spec["body"] * 0.5 or head:     # 방패에 막힌 총알은 피가 안 나요
                    hits.append((ax, ay, target_dist, head))

        for x, y, perp, head in hits:
            self.spray_blood(x, y, perp, head)
        for enemy, amount in damage.items():
            self.damage_enemy(enemy, amount, "HEADSHOT!" if enemy in headshots else "DOWN")

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

    def update_projectiles(self, dt):
        alive = []
        for proj in self.projectiles:
            if proj.update(dt, self.enemies):
                if proj.kind == "rocket":
                    radius, damage = ROCKET_BLAST
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
        self.sounds.play("explosion", 1.1 - self.player.pos.distance_to(pos) / 25)
        if owner in ("player", "streak"):
            how = "AIRSTRIKE!" if owner == "streak" else "BOOM!"
            for enemy in list(self.enemies):
                d = enemy.pos.distance_to(pos)
                if d < radius and can_see(pos, enemy.pos):
                    self.damage_enemy(enemy, damage * power(d), how)
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
            elif item.kind == "health" and self.player.hp < 100:
                self.player.hp = min(100, self.player.hp + HEALTH_PACK)
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
        self.draw_sky(screen)
        self.draw_world(screen)
        self.draw_sprites(screen)
        self.draw_particles(screen, casings=False)       # 튀는 피
        if self.theme["snow"]:
            self.draw_snow(screen)
        if self.scoped:
            screen.blit(self.scope_overlay, (0, 0))
            label = self.font.render(f"x{self.zoom}", True, WHITE)
            screen.blit(label, label.get_rect(center=(WIDTH / 2 + HEIGHT * 0.3, HEIGHT / 2 + HEIGHT * 0.3)))
        elif self.knife_timer > 0:
            self.draw_knife(screen)
        else:
            self.draw_gun(screen)
        self.draw_particles(screen, casings=True)        # 탄피는 총 앞에
        if self.light_timer > 0:
            screen.blit(self.muzzle_light, (0, 0))       # 총구 섬광
        self.draw_hud(screen)
        if self.show_help:
            draw_help(screen, self.fonts, HELP_TEXT[self.fonts["lang"]]["resume"])

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
            pygame.draw.circle(screen, (255, 200, 140), (x, y), 70 * UI * z)
            pygame.draw.circle(screen, (255, 225, 160), (x, y), 48 * UI * z)
            pygame.draw.circle(screen, (255, 245, 210), (x, y), 34 * UI * z)
        pygame.draw.rect(screen, FLOORS[self.theme["ground"]], (0, horizon, WIDTH, max(0, HEIGHT - horizon)))

    def draw_world(self, screen):
        p = self.player
        horizon, proj, eye, fog_dist, col_w = self.horizon, self.proj, self.eye, self.fog_dist, self.col_w
        for i in range(self.num_rays):
            # i번째 세로 줄이 바라보는 방향. 화면에 평평하게 펼쳐지도록 tan으로 계산해요
            ray_angle = p.angle + math.atan(((i + 0.5) * col_w - WIDTH / 2) / proj)
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
            for dist, vertical, wall_x, (color, height, pattern, neon), cx, cy in reversed(walls):
                perp = max(0.05, dist * fix)
                size = proj / perp
                bottom = horizon + eye * size
                top = bottom - height * size
                if top > HEIGHT or bottom < 0:
                    continue
                base = shade(color, 0.82 if vertical else 1.0)
                if wall_x < 0.03 or wall_x > 0.97:      # 건물 모서리 선
                    base = shade(base, 0.6)
                elif pattern == "ribs" and (wall_x * 6) % 1 < 0.2:   # 컨테이너/창고의 세로 골
                    base = shade(base, 0.75)
                pygame.draw.rect(screen, fog(base, perp, fog_dist), (x, top, col_w, bottom - top + 1))
                # 창문: 층마다 두 칸씩. 몇몇 창문은 불이 켜져 있어요
                if pattern is True and (0.18 < wall_x < 0.42 or 0.58 < wall_x < 0.82):
                    dark_glass = fog((60, 80, 120) if vertical else (90, 110, 150), perp, fog_dist)
                    lit_glass = fog((255, 215, 140), perp * 0.5, fog_dist)
                    half = 0 if wall_x < 0.5 else 1
                    for k in range(int(height / 0.5)):
                        y0 = bottom - (k * 0.5 + 0.42) * size
                        y1 = bottom - (k * 0.5 + 0.17) * size
                        if y1 > 0 and y0 < HEIGHT:
                            lit = (cx * 7 + cy * 13 + k * 5 + half * 3 + vertical) % LIT == 0
                            pygame.draw.rect(screen, lit_glass if lit else dark_glass, (x, y0, col_w, y1 - y0))
                # 네온사인: 건물 꼭대기에 빛나는 띠 (안개를 덜 타서 멀리서도 잘 보여요)
                if neon:
                    glow = fog(neon, perp * 0.3, fog_dist)
                    pygame.draw.rect(screen, glow, (x, top + 0.06 * size, col_w, max(2, 0.07 * size)))

    def draw_sprites(self, screen):
        items = []     # (화면 위치, 그림, 적 또는 None)
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
        t = pygame.time.get_ticks() / 1000
        for item in self.pickups:
            box = self.project(item.pos, 0.3, 0.4, lift=0.08 + math.sin(t * 3 + item.phase) * 0.05)
            if box:
                items.append((box, self.pickup_images[item.kind], None))
        for proj in self.projectiles:
            if proj.kind == "grenade":
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
            frame = min(2, int(corpse.age / 0.12))
            img, h, w = self.corpse_frames[(corpse.kind, corpse.side)][frame]
            box = self.project(corpse.pos, h, w)
            if box:
                items.append((box, img, None))
        for sentry in self.sentries:
            box = self.project(sentry.pos, 0.55, 0.5)
            if box:
                items.append((box, self.sentry_images[1 if sentry.flash > 0 else 0], None))
        for effect in self.effects:
            size = effect.size * (0.5 + 0.5 * effect.age / effect.duration)
            box = self.project(effect.pos, size, size, lift=0.6 - size / 2)
            if box:
                items.append((box, effect.frame, None))
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
        # 걸을 때 흔들리고, 쏠 때 뒤로 밀리고, 재장전/교체할 때 내려가요
        # 정조준하면 화면 가운데로 올라와요
        a = self.arsenal
        t = pygame.time.get_ticks() / 1000
        bob = math.sin(t * 10) * 6 if self.player.moving and self.player.z == 0 else 0
        if self.aiming:
            bob *= 0.3
        down = 0
        if self.player.sprinting:
            bob = math.sin(t * 14) * 12           # 달릴 땐 크게 흔들리고 총이 내려가요
            down = 70
        if a.reload_left > 0:
            down = 120
        elif a.switch_left > 0:
            down = 200 * a.switch_left / a.SWITCH_TIME
        if self.aiming:
            x = WIDTH / 2 - 30 * UI + bob
            y = HEIGHT - 175 * UI + (a.kick * 10 + down) * UI
        else:
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
        elif name == "SHOTGUN":
            poly(dark, [(-10, 40), (30, 0), (70, 30), (30, 70)])
            poly(wood, [(30, 70), (70, 30), (130, 90), (130, 160), (60, 160)])
            muzzle = at(8, 28)
        elif name == "SMG":
            poly(dark, [(10, 40), (45, 10), (110, 65), (110, 160), (40, 160)])
            poly(mid, [(55, 70), (75, 55), (95, 120), (75, 135)])          # 탄창
            muzzle = at(28, 26)
        elif name == "LMG":
            poly(dark, [(-10, 30), (40, -5), (140, 80), (140, 160), (30, 160)])
            poly((70, 75, 60), [(40, 60), (80, 40), (110, 90), (70, 110)])       # 탄통
            muzzle = at(10, 10)
        elif name == "BURST":
            poly((150, 130, 95), [(0, 40), (40, 0), (120, 70), (120, 160), (30, 160)])   # 사막색 소총
            poly(dark, [(10, 30), (40, 5), (60, 20), (30, 50)])
            muzzle = at(22, 18)
        elif name == "DMR":
            poly((60, 50, 40), [(-20, 20), (5, -5), (130, 90), (130, 160), (40, 160)])
            poly(BLACK, [(20, 10), (35, -5), (75, 25), (60, 40)])           # 작은 조준경
            muzzle = at(-12, 8)
        else:  # ROCKET
            poly((85, 95, 65), [(-40, 20), (0, -20), (140, 100), (100, 140)])   # 발사관
            poly((60, 65, 45), [(-40, 20), (0, -20), (10, -10), (-30, 30)])
            poly(dark, [(60, 90), (80, 75), (110, 160), (80, 160)])            # 손잡이
            muzzle = at(-20, 0)

        if a.kick > 0.6:
            pygame.draw.circle(screen, YELLOW, muzzle, 18 * UI)
            pygame.draw.circle(screen, WHITE, muzzle, 8 * UI)

    def draw_knife(self, screen):
        """칼 휘두르기: 오른쪽 아래에서 가운데 위쪽으로 베는 모양"""
        p = 1 - self.knife_timer / KNIFE_TIME        # 0 → 1
        base = pygame.Vector2(WIDTH * (0.78 - 0.25 * p), HEIGHT * (1.0 - 0.15 * math.sin(p * math.pi)))
        d = pygame.Vector2(-0.3 - 0.6 * p, -1).normalize()   # 칼날 방향: 점점 왼쪽으로 기울어요
        side = pygame.Vector2(-d.y, d.x)
        tip = base + d * 200 * UI
        pygame.draw.polygon(screen, (210, 215, 225), [base + side * 10 * UI, tip, base - side * 10 * UI])
        pygame.draw.line(screen, (150, 155, 165), base, tip, 2)
        pygame.draw.line(screen, (30, 30, 30), base, base - d * 70 * UI, int(20 * UI))

    def draw_hud(self, screen):
        font, big_font = self.font, self.big_font
        # 다치면 화면 가장자리가 붉게 (체력이 낮을수록 진하게)
        low = max(0.0, 1 - self.player.hp / 60) if self.player.hp < 60 else 0.0
        strength = min(1.0, max(self.damage_flash, low))
        if strength > 0:
            self.hurt_vignette.set_alpha(int(255 * strength))
            screen.blit(self.hurt_vignette, (0, 0))

        # 조준선 (화면 가운데). 총알이 퍼지는 만큼 벌어져요. 정조준 중엔 빨간 점
        cx, cy = WIDTH / 2, HEIGHT / 2
        spec = self.arsenal.current.spec
        if self.aiming and not self.scoped:
            pygame.draw.circle(screen, (255, 40, 40), (cx, cy), max(2, 3 * UI))
        elif not self.scoped and not self.player.sprinting:
            gap = 5 * UI + self.current_spread(spec) * 0.6
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                start = (cx + dx * gap, cy + dy * gap)
                end = (cx + dx * (gap + 10 * UI), cy + dy * (gap + 10 * UI))
                pygame.draw.line(screen, GREEN, start, end, 2)
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

        # 점수/메달 글자 (조준점 아래)
        for i, (text, color, t) in enumerate(self.popups[-4:]):
            self.center_text(screen, font, text, color, HEIGHT * 0.58 + i * 30 * UI)

        # 적 수류탄이 가까이 있으면 경고 (깜빡여요)
        danger = any(p.owner == "enemy" and p.pos.distance_to(self.player.pos) < 4.5 for p in self.projectiles)
        if danger and pygame.time.get_ticks() // 150 % 2 == 0:
            self.center_text(screen, big_font, "GRENADE!", RED, HEIGHT * 0.38)

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
        screen.blit(image, image.get_rect(bottomright=(WIDTH - 24, rect.top - 4)))

        # 아래 가운데 무기 칸
        slot_w = 76 * UI
        left = WIDTH / 2 - slot_w * len(WEAPONS) / 2
        for i, weapon in enumerate(self.arsenal.weapons):
            rect = pygame.Rect(left + i * slot_w + 3, HEIGHT - 44 * UI, slot_w - 6, 30 * UI)
            selected = i == self.arsenal.index
            panel = pygame.Surface(rect.size, pygame.SRCALPHA)
            panel.fill((255, 220, 90, 200) if selected else (0, 0, 0, 120))
            screen.blit(panel, rect)
            label = self.fonts["tiny"].render(f"{i + 1} {weapon.spec['name']}", True, BLACK if selected else WHITE)
            screen.blit(label, label.get_rect(center=rect.center))

        # 위쪽 정보
        info = f"ROUND {self.round}   {self.theme['name']}   ENEMIES {len(self.enemies)}   KILLS {self.kills}"
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
                     "G grenade   V knife   X killstreak   1-9 weapon   R reload   H help (pause)"]
            for i, hint in enumerate(hints):
                self.center_text(screen, self.small_font, hint, WHITE, HEIGHT - (82 - i * 20) * UI)
        if self.banner_timer > 0:
            self.center_text(screen, big_font, self.banner, YELLOW, HEIGHT / 3)
            for i, (text, color) in enumerate(self.sub_banners):
                self.center_text(screen, font, text, color, HEIGHT / 3 + (45 + i * 32) * UI)
            if self.round_clear_timer <= 0:
                typed = self.theme["brief"][:int(self.brief_age * 40)]
                y = HEIGHT / 3 + (45 + len(self.sub_banners) * 32) * UI
                self.center_text(screen, self.small_font, typed, (200, 230, 255), y)
        if self.game_over:
            self.center_text(screen, big_font, "YOU DIED", RED, HEIGHT / 2 - 40 * UI)
            self.center_text(screen, font, f"Round {self.round}  /  Kills {self.kills}", WHITE, HEIGHT / 2 + 10 * UI)
            self.center_text(screen, font, f"R: retry round {self.round}    N: new game    ESC: menu",
                             YELLOW, HEIGHT / 2 + 45 * UI)

    def make_minimap(self):
        """미니맵 그림은 바뀌지 않으니 맵마다 한 번만 그려 둬요."""
        cell = self.minimap_cell
        mini = pygame.Surface((MAP_W * cell, MAP_H * cell), pygame.SRCALPHA)
        for row in range(MAP_H):
            for col in range(MAP_W):
                spec = WALL_GRID[row][col]
                color = spec[0] if spec else FLOORS[FLOOR_GRID[row][col]]
                pygame.draw.rect(mini, (*color, 190), (col * cell, row * cell, cell, cell))
        return mini

    @property
    def minimap_cell(self):
        return max(3, int(4 * UI))

    def draw_minimap(self, screen):
        """오른쪽 위 작은 지도. 지도 아래쪽 y좌표를 돌려줘요."""
        cell = self.minimap_cell
        ox, oy = WIDTH - MAP_W * cell - 12, 12
        screen.blit(self.minimap, (ox, oy))
        # 빨간 점: 방금 총을 쏜 적 (레이더를 켜면 모든 적)
        for enemy in self.enemies:
            if self.radar_timer > 0 or enemy.flash_timer > -0.6:
                pygame.draw.circle(screen, RED, enemy.pos * cell + (ox, oy), max(2, cell // 2 + 1))
        for sentry in self.sentries:
            pygame.draw.circle(screen, (80, 240, 255), sentry.pos * cell + (ox, oy), max(2, cell // 2))
        if self.radar_timer > 0:
            label = self.fonts["tiny"].render(f"RADAR {self.radar_timer:.0f}", True, (80, 240, 255))
            screen.blit(label, (ox, oy + MAP_H * cell + 2))
        p = self.player.pos * cell + (ox, oy)
        look = p + pygame.Vector2(math.cos(self.player.angle), math.sin(self.player.angle)) * 12
        pygame.draw.line(screen, BLACK, p, look, 2)
        pygame.draw.circle(screen, BLACK, p, 3)
        return oy + MAP_H * cell + (16 * UI if self.radar_timer > 0 else 0)

    @staticmethod
    def center_text(screen, font, text, color, y):
        image = font.render(text, True, color)
        screen.blit(image, image.get_rect(center=(WIDTH / 2, y)))


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


async def intro_screen(save):
    """시작 화면: 조작법을 보여주고 새 게임 / 이어하기 / 해상도를 골라요.
    고른 시작 라운드를 돌려줘요. ESC나 창 닫기면 None (닫기는 "closed")."""
    options = available_resolutions()
    res_index = min(save.get("res", 0), len(options) - 1)
    set_resolution(*options[res_index])
    screen = open_window()
    fonts = make_fonts()
    clock = pygame.time.Clock()
    continue_round = save.get("continue", 1)
    while True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "closed"
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_ESCAPE:
                return None
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_KP_ENTER):
                return 1
            if event.key == pygame.K_c and continue_round > 1:
                return continue_round
            if event.key == pygame.K_t and len(options) > 1:
                res_index = (res_index + 1) % len(options)
                save["res"] = res_index
                write_save(save)
                set_resolution(*options[res_index])
                screen = open_window()
                fonts = make_fonts()

        ko = fonts["lang"] == "ko"
        parts = ["Enter 새 게임" if ko else "ENTER new game"]
        if continue_round > 1:
            parts.append(f"C 이어하기 (라운드 {continue_round})" if ko else f"C continue (round {continue_round})")
        if len(options) > 1:
            w, h = options[res_index]
            note = "" if fits_desktop(w, h) else (" 전체 화면" if ko else " fullscreen")
            parts.append(f"T 해상도 {w}x{h}{note}" if ko else f"T resolution {w}x{h}{note}")
        parts.append("ESC 메뉴" if ko else "ESC menu")
        screen.fill((15, 10, 35))
        draw_help(screen, fonts, "     ".join(parts))
        # 조작법 판 위에 제목과 네온 줄무늬
        for i in range(6):
            y = HEIGHT * (0.15 + i * 0.012)
            pygame.draw.line(screen, (255, 80, 200) if i % 2 else (80, 240, 255), (0, y), (WIDTH, y), 2)
        title = fonts["title"].render("STRIKE ZONE", True, (255, 80, 200))
        screen.blit(title, title.get_rect(center=(WIDTH / 2, HEIGHT * 0.09)))
        best = save.get("best", 0)
        if best:
            label = fonts["help"].render(f"최고 기록: 라운드 {best}" if ko else f"Best: round {best}", True, WHITE)
            screen.blit(label, label.get_rect(center=(WIDTH / 2, HEIGHT * 0.88)))
        pygame.display.flip()
        await asyncio.sleep(0)


async def run():
    """게임 한 판 실행. ESC를 누르면 끝나요.

    창을 닫으면 False, ESC로 끝내면 True를 돌려줘요 (메뉴로 돌아갈지 판단용).
    """
    save = load_save()
    start_round = await intro_screen(save)
    if start_round is None or start_round == "closed":
        return start_round is None
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()

    # 마우스를 창 안에 가두고 커서 숨기기 (FPS 게임처럼)
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)
    pygame.mouse.get_rel()

    game = Game(save, start_round)
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

    write_save(game.save)          # 경험치(계급) 저장
    # 마우스 원래대로
    pygame.event.set_grab(False)
    pygame.mouse.set_visible(True)
    return not closed


if __name__ == "__main__":
    pygame.init()
    asyncio.run(run())
    pygame.quit()
