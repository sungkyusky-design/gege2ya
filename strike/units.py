"""무기와 적의 능력치 표 (숫자를 바꾸면 게임 밸런스가 바뀌어요. 바꾼 뒤엔 balance.py 로 확인)

shooter.py 가 이 파일의 값들을 가져다 써요."""


# 총마다 좌우 반동 (쏠 때 조준이 옆으로 살짝 튀어요, 단위: 라디안)
HORIZONTAL_KICK = {"RIFLE": 0.005, "PISTOL": 0.004, "SNIPER": 0.015, "SHOTGUN": 0.012, "SMG": 0.007,
                   "ROCKET": 0.01, "LMG": 0.006, "BURST": 0.004, "DMR": 0.008, "HEAVY AR": 0.008,
                   "AUTO SHOTGUN": 0.012, "REVOLVER": 0.012, "MACHINE PISTOL": 0.007, "LAUNCHER": 0.01}


# ----- RPG: 무기 해금, 무기 레벨, 스킬 -----
START_WEAPONS = ["RIFLE", "PISTOL"]


# 무기를 얻는 조건: ("level", 계급) / ("score", 한 라운드 점수) / ("heads", 한 라운드 헤드샷 수)
UNLOCKS = {
    "SMG": ("level", 2), "SHOTGUN": ("level", 3), "BURST": ("score", 1000), "MACHINE PISTOL": ("level", 4),
    "SNIPER": ("level", 5), "DMR": ("heads", 5), "HEAVY AR": ("level", 6), "REVOLVER": ("score", 1500),
    "AUTO SHOTGUN": ("level", 8), "LMG": ("level", 10), "LAUNCHER": ("score", 2500), "ROCKET": ("level", 12),
}


# 퍼크: (이름, 한국어 설명, 영어 설명)
PERKS = [
    ("HEAVY ROUNDS", "총알 피해 +25%", "Bullets deal 25% more damage"),
    ("QUICK HANDS", "재장전·무기 교체 40% 빠르게", "Reload and swap 40% faster"),
    ("LIGHTFOOT", "이동 +12%, 발소리를 적이 못 들어요", "Move 12% faster, enemies can't hear your steps"),
    ("IRON SKIN", "최대 체력 130", "Max health 130"),
    ("SCAVENGER", "탄약 1.5배, 수류탄 +2", "1.5x ammo, +2 grenades"),
]


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
    # 타이탄: 10웨이브마다 나오는 보스 좀비. 아주 단단하고, 가까이 오면 땅을 내리쳐요
    "TITAN": dict(hp=2600, speed=0.8, sight=99, reaction=0, keep=0, range=0,
                  fire=(1, 1), damage=(0, 0), accuracy=0, falloff=0,
                  height=1.55, width=1.0, melee=(48, 1.7),
                  look=dict(head="zombie", skin=(120, 70, 70), shirt=(40, 30, 35), pants=(30, 28, 35),
                            eyes=(255, 230, 60), big=True)),
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


# 총기 개조: 칸마다 고를 수 있는 부착물 (이름, 필요한 무기 레벨, 바뀌는 성능)
#   ads_spread: 정조준 때 퍼짐 (작을수록 정확, 기본 0.45)   ads: 정조준 확대 배율에 곱하기
#   hip: 그냥 쏠 때 퍼짐에 곱하기   kick: 위로 튀는 반동에 곱하기   recoil: 옆 반동에 곱하기
#   mag / reserve / reload / move: 탄창, 여분 탄, 재장전 시간, 움직이는 속도에 곱하기
ATTACHMENTS = {
    "OPTIC": [("IRON SIGHTS", 1, {}), ("RED DOT", 1, {"ads_spread": 0.40}),
              ("HOLO", 3, {"ads_spread": 0.36, "ads": 1.1}),
              ("4X SCOPE", 6, {"ads_spread": 0.30, "ads": 1.8, "move": 0.92})],
    "MUZZLE": [("NONE", 1, {}), ("COMPENSATOR", 3, {"kick": 0.8, "recoil": 0.7}),
               ("SUPPRESSOR", 8, {"suppressed": True})],
    "MAGAZINE": [("STANDARD", 1, {}), ("EXT MAG", 2, {"mag": 1.5, "reserve": 1.25, "reload": 1.1}),
                 ("FAST MAG", 4, {"reload": 0.75})],
    "GRIP": [("NONE", 1, {}), ("ANGLED GRIP", 3, {"hip": 0.8, "move": 1.04}),
             ("VERTICAL GRIP", 5, {"kick": 0.7, "recoil": 0.7})],
}
ATTACHMENT_INFO = {
    "IRON SIGHTS": ("기본 가늠쇠", "Basic sights"), "RED DOT": ("정조준이 조금 더 정확해요", "Slightly tighter aim"),
    "HOLO": ("정조준이 더 정확하고 살짝 확대", "Tighter aim, a bit more zoom"),
    "4X SCOPE": ("멀리 크게 보이고 아주 정확, 조금 느려져요", "Long zoom, very accurate, slower"),
    "NONE": ("없음", "None"), "COMPENSATOR": ("반동이 줄어요", "Less recoil"),
    "SUPPRESSOR": ("소음기: 적이 잘 못 들어요", "Quiet shots"), "STANDARD": ("기본 탄창", "Standard magazine"),
    "EXT MAG": ("탄창 1.5배, 재장전 조금 느림", "1.5x magazine, slower reload"),
    "FAST MAG": ("재장전이 25% 빨라요", "25% faster reload"),
    "ANGLED GRIP": ("그냥 쏠 때 덜 퍼지고 조금 빨라요", "Better hip fire, a bit faster"),
    "VERTICAL GRIP": ("반동이 크게 줄어요", "Much less recoil"),
}
# 전술 장비 (로드아웃에서 하나 골라요, N 으로 던져요)
TACTICALS = [("FLASHBANG", "섬광탄: 근처 적이 3초 동안 아무것도 못 해요", "Flashbang: stuns nearby enemies"),
             ("SMOKE", "연막탄: 10초 동안 연기가 적의 시야를 가려요", "Smoke: blocks enemy vision for 10s"),
             ("THROWING KNIFE", "투척 칼: 조용히 날아가 꽂혀요 (빗나가면 돌아와요)", "Throwing knife: silent, returns if it misses")]
