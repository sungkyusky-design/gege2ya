"""글: 도전 모드 설명, 캠페인 이야기와 본부 무전, 도움말

shooter.py 가 이 파일의 값들을 가져다 써요."""


# ----- 도전 모드 -----
# (이름, 라운드, 한국어 설명, 영어 설명). DAILY 의 라운드와 적은 날짜로 정해져요
CHALLENGES = [
    ("DAILY", 0, "오늘의 도전: 날짜마다 바뀌는 맵과 적. 빨리 깰수록 좋아요", "Daily: map and enemies change every day"),
    ("HEADSHOTS", 12, "머리를 맞혀야만 피해가 들어가요", "Only headshots do damage"),
    ("PISTOL", 9, "권총 하나로만 싸워요", "Pistol only"),
    ("HARDCORE", 15, "한 방 맞으면 끝! 대신 내 총알 피해 2배", "One hit kills you, your bullets do double damage"),
    ("BLITZ", 7, "60초 안에 모든 적을 쓰러뜨리세요", "Clear the round in 60 seconds"),
]


# 캠페인 이야기: 세트마다 브리핑, 무전, 세트 마지막(20번째) 라운드의 이름 있는 보스
# 적: 바닷가 도시들을 점령한 무장 조직 "아이언 재칼(IRON JACKALS)"
STORY = [
    dict(op="OPERATION FIRST LIGHT", boss="JACKAL CAPTAIN", mid="JACKAL SERGEANT",
         ko=["아이언 재칼이 해안 도시들을 점령했다.", "정찰대가 먼저 들어간다. 놈들의 수와 무기를 확인하고 길을 열어라.",
             "세트 마지막 라운드: 해안을 지키는 재칼 대위를 쓰러뜨려라."],
         en=["The Iron Jackals have seized the coastal cities.", "Recon goes in first. Find out their numbers and open a path.",
             "Final round of the set: take down the Jackal Captain holding the coast."]),
    dict(op="OPERATION HAMMERFALL", boss="THE FOREMAN", mid="JACKAL ENFORCER",
         ko=["해안은 되찾았다. 이제 내륙으로 밀고 들어간다.", "놈들이 중장비와 증원군을 불러들였다. 정면 돌파다.",
             "세트 마지막 라운드: 보급 기지를 지휘하는 '포어맨'을 잡아라."],
         en=["The coast is ours. Now we push inland.", "They brought heavy gear and reinforcements. We go straight through.",
             "Final round of the set: capture the Foreman who runs their supply base."]),
    dict(op="OPERATION BLACKOUT", boss="NIGHT OWL", mid="SHADOW SCOUT",
         ko=["밤이다. 놈들의 보급선을 끊는다.", "어둠 속에서 총구 불빛이 위치를 알린다. 조용히, 빠르게.",
             "세트 마지막 라운드: 야간 저격대장 '나이트 아울'을 찾아라."],
         en=["Night falls. We cut their supply lines.", "Muzzle flashes give you away in the dark. Quiet and fast.",
             "Final round of the set: hunt down the Night Owl, their night sniper chief."]),
    dict(op="OPERATION STORMBREAK", boss="THUNDERHEAD", mid="STORM RAIDER",
         ko=["폭풍을 틈타 놈들이 반격한다.", "비가 발소리를 덮는다. 귀보다 눈을 믿어라.",
             "세트 마지막 라운드: 반격을 이끄는 '썬더헤드'를 막아라."],
         en=["They counter-attack under cover of the storm.", "Rain covers footsteps. Trust your eyes over your ears.",
             "Final round of the set: stop Thunderhead, who leads the counter-attack."]),
    dict(op="OPERATION LAST STAND", boss="THE WARLORD", mid="WARLORD'S GUARD",
         ko=["마지막 작전. 재칼의 우두머리 '워로드'가 숨은 곳을 찾았다.", "놈들은 가장 강한 병사들로 버틴다. 모든 기술을 쓰라.",
             "100라운드: 워로드를 끝내고 전쟁을 끝내라."],
         en=["The final operation. We found where the Warlord hides.", "Their best soldiers stand guard. Use everything you have.",
             "Round 100: end the Warlord and end this war."]),
]


# 본부(HQ) 무전: 상황 -> (한국어 목록, 영어 목록)
RADIO = {
    "start": (["HQ: 구역에 들어섰다. 적 위치를 확인해라.", "HQ: 조심해, 놈들이 기다리고 있다.", "HQ: 주변을 살피고 엄폐물을 써라."],
              ["HQ: You're in the zone. Locate the hostiles.", "HQ: Careful, they're waiting for you.",
               "HQ: Check your corners and use cover."]),
    "first": (["HQ: 한 명 쓰러뜨렸다. 계속 가.", "HQ: 좋은 사격이다."], ["HQ: One down. Keep moving.", "HQ: Good shot."]),
    "low": (["HQ: 많이 다쳤다! 엄폐하고 숨을 돌려라.", "HQ: 체력이 낮다. 물러서!"],
            ["HQ: You're hurt! Get to cover and breathe.", "HQ: Health is low. Fall back!"]),
    "boss": (["HQ: 지휘관이 나타났다. 체력을 깎으면 화를 낼 거다.", "HQ: 큰 놈이다. 거리를 두고 싸워라."],
             ["HQ: Their commander is here. He gets angry when hurt.", "HQ: Big one. Keep your distance."]),
    "last": (["HQ: 하나 남았다. 끝내라.", "HQ: 마지막 한 명이다."], ["HQ: One left. Finish it.", "HQ: Last hostile."]),
    "clear": (["HQ: 구역 확보. 잘했다.", "HQ: 깨끗하다. 다음 구역으로."], ["HQ: Area secure. Nice work.", "HQ: Clear. Move to the next zone."]),
    "set": (["HQ: 작전 성공! 다음 작전을 준비해라.", "HQ: 훌륭하다. 놈들이 흔들리고 있다."],
            ["HQ: Operation complete! Prepare for the next one.", "HQ: Outstanding. They're breaking."]),
}


HELP_TEXT = {
    "ko": dict(
        title="조작법",
        keys=[("W A S D", "이동"), ("Shift", "달리기 (W와 함께)"), ("C", "앉기 / 달리다가: 슬라이딩"),
              ("← → ↑ ↓", "시점 (마우스도 돼요)"), ("스페이스바", "점프"),
              ("F,  왼쪽 클릭", "사격 (꾹 누르면 연사)"), ("E,  오른쪽 클릭", "정조준 / 저격총 조준경"), ("Z", "조준경 배율 3·6·12배"),
              ("G", "수류탄"), ("V", "칼"), ("X", "킬스트릭 쓰기"), ("1~9, 0, Q", "무기 바꾸기,  Q: 방금 쓰던 무기"), ("Tab", "짧게: 다음 무기,  꾹: 무기 휠 (← → 고르고 떼기)"), ("T,  Y,  J", "스킬: 집중 / 구급상자 / 탐지"),
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
        keys=[("W A S D", "move"), ("SHIFT", "sprint (with W)"), ("C", "crouch / slide (sprinting)"),
              ("ARROWS", "look (or mouse)"), ("SPACE", "jump"),
              ("F, LEFT CLICK", "fire (hold for auto)"), ("E, RIGHT CLICK", "aim / sniper scope"), ("Z", "scope zoom 3/6/12x"),
              ("G", "grenade"), ("V", "knife"), ("X", "use killstreak"), ("1-9, 0, Q", "weapons, Q = last one"), ("TAB", "next weapon, hold = wheel"), ("T, Y, J", "focus / medkit / scan"),
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
