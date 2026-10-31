"""자동 플레이 테스트: 화면 없이(headless) 모든 모드를 무작위 입력으로 돌려서 멈추는(오류) 곳이 없는지 봐요.

하는 일:
    1. 캠페인(여러 세트의 라운드), 좀비 모드, 미션 3개를 각각 시작해요.
    2. 정해진 시간 동안 무작위로 키를 누르고(이동, 사격, 무기 바꾸기, 스킬...), 가끔 적을 바라보고 쏴요.
    3. 죽으면 다시 시작(R)도 눌러 봐요.
    4. 메뉴 화면들(시작, 로드아웃, 스킬, 설정, 미션)도 한 번씩 그려 봐요.
    5. 한 장면 계산 시간(ms)을 같이 보여줘요.

실행 (저장소 맨 위 폴더에서):
    python .claude/skills/strike-zone-dev/scripts/smoke_test.py            # 기본: 판마다 20초
    python .claude/skills/strike-zone-dev/scripts/smoke_test.py --seconds 60

오류가 나면 그 자리의 Traceback을 보여주고 exit code 1.
저장 파일은 건드리지 않아요 (가짜 저장 정보로 돌려요).
"""
import asyncio
import math
import os
import random
import sys
import time
import traceback

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.getcwd())

import pygame  # noqa: E402
import shooter  # noqa: E402

shooter.write_save = lambda save: None        # 진짜 저장 파일을 덮어쓰지 않게


class Keys(dict):
    def __getitem__(self, key):
        return self.get(key, False)


HELD = [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
        pygame.K_DOWN, pygame.K_f, pygame.K_LSHIFT, pygame.K_SPACE]
TAPS = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_0, pygame.K_TAB, pygame.K_q, pygame.K_r, pygame.K_e,
        pygame.K_z, pygame.K_g, pygame.K_v, pygame.K_c, pygame.K_x, pygame.K_b, pygame.K_u, pygame.K_t,
        pygame.K_y, pygame.K_j]


def rich_save():
    """계급이 높고 스킬과 무기를 많이 가진 저장 정보 (기능을 최대한 많이 쓰게)"""
    return {"xp": 15000, "wkills": {"RIFLE": 80, "SMG": 30}, "unlocked": ["BURST", "DMR", "REVOLVER", "LAUNCHER"],
            "skills": {"VITALITY": 2, "MARKSMAN": 1, "FOCUS": 1, "MEDKIT": 1, "SCAN": 1}}


def play(label, game, seconds, rng):
    screen = pygame.display.get_surface()
    held, frames, deaths, work = set(), 0, 0, 0.0
    while frames < seconds * 60:
        if rng.random() < 0.08:
            held ^= {rng.choice(HELD)}
        if rng.random() < 0.03:
            game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=rng.choice(TAPS), mod=0, unicode=""))
        if game.enemies and rng.random() < 0.3:
            target = min(game.enemies, key=lambda e: e.pos.distance_to(game.player.pos))
            offset = target.pos - game.player.pos
            game.player.angle = math.atan2(offset.y, offset.x)
        game.pad_aim = rng.random() < 0.1
        started = time.perf_counter()
        game.update(1 / 60, Keys({k: True for k in held}), rng.randint(-3, 3), rng.randint(-2, 2),
                    (False, False, False))
        if frames % 3 == 0:
            game.draw(screen)
            work += time.perf_counter() - started
        if game.game_over:
            deaths += 1
            for i in range(240):                       # 킬캠과 사망 화면도 그려 봐요
                game.update(1 / 60, Keys(), 0, 0, (False, False, False))
                if i % 30 == 0:
                    game.draw(screen)
            game.retry_round()
        frames += 1
    ms = work / max(1, frames // 3) * 1000
    print(f"OK  {label:34s} round {game.round:3d}  deaths {deaths}  {ms:5.1f} ms/frame")


async def menus():
    """메뉴 화면들을 가짜 키 입력으로 한 번씩 열었다 닫아요"""
    escape = [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE, mod=0, unicode="")]
    script = []
    real = shooter.menu_events
    shooter.menu_events = lambda: script.pop(0) if script else escape
    try:
        save = rich_save()
        for screen_fn, args in ((shooter.settings_screen, (save,)), (shooter.skills_screen, (save,)),
                                (shooter.mission_screen, (save,)),
                                (shooter.loadout_screen, (save, dict(mode="campaign", round=1)))):
            script[:] = [[], []]
            await screen_fn(*args)
        script[:] = [[], [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_z, mod=0, unicode="")]]
        await shooter.intro_screen(save)
    finally:
        shooter.menu_events = real
    print("OK  menus (settings, skills, missions, loadout, intro)")


def main():
    seconds = float(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 20
    pygame.init()
    pygame.display.set_mode((shooter.WIDTH, shooter.HEIGHT))
    rng = random.Random(1)
    loadout = dict(primary="RIFLE", secondary="PISTOL", perk="HEAVY ROUNDS")
    cases = [(f"campaign round {r}", dict(start_round=r, mode="campaign")) for r in (1, 23, 47, 66, 100)]
    cases.append(("zombies", dict(start_round=1, mode="zombies")))
    cases += [(f"mission {m['name']}", dict(start_round=1, mode="mission", mission=i))
              for i, m in enumerate(shooter.MISSIONS)]
    failed = False
    try:
        asyncio.run(menus())
    except Exception:
        print("FAIL menus")
        traceback.print_exc()
        failed = True
    for label, kwargs in cases:
        try:
            game = shooter.Game(rich_save(), loadout=loadout, **kwargs)
            play(label, game, seconds, rng)
        except Exception:
            print(f"FAIL {label}")
            traceback.print_exc()
            failed = True
    print("\n결과:", "실패가 있어요" if failed else "모두 통과")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
