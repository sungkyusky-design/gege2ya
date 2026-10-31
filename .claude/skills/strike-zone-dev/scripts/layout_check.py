"""화면 글자 겹침 검사: 여러 해상도와 UI SIZE 에서 메뉴와 게임 화면을 그려 보고,
글자끼리 겹치거나 화면 밖으로 잘리는 곳을 찾아요.

실행 (저장소 맨 위 폴더에서):
    python .claude/skills/strike-zone-dev/scripts/layout_check.py            # 기본: 1280x720, 100%
    python .claude/skills/strike-zone-dev/scripts/layout_check.py --all      # 해상도 4개 x UI SIZE 3개
    python .claude/skills/strike-zone-dev/scripts/layout_check.py --shots 폴더   # 화면 사진도 저장

문제가 하나라도 있으면 끝에 목록을 보여주고 실패(1)로 끝나요.
방법: 글자 그림(ShadowFont.render 가 만든 것)이 화면에 붙는 위치를 모두 기록해서 서로 겹치는지 봐요.
"""
import argparse
import asyncio
import os
import sys
import time

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, ROOT)

import pygame  # noqa: E402
import shooter  # noqa: E402

shooter.write_save = lambda save: None          # 진짜 저장 파일은 건드리지 않아요
LOADOUT = dict(primary="RIFLE", secondary="PISTOL", perk="IRON SKIN")
TEXT_IDS = {}                                   # 글자 그림들 (id → 그림, 그림을 붙잡아 둬야 id 가 다시 안 쓰여요)
_render = shooter.ShadowFont.render


def render(self, text, antialias, color):
    image = _render(self, text, antialias, color)
    TEXT_IDS[id(image)] = image
    return image


shooter.ShadowFont.render = render


class Recorder(pygame.Surface):
    """화면 대신 쓰는 그림판: 글자를 붙일 때마다 (글자 위치) 를 적어 둬요"""

    def __init__(self, size):
        super().__init__(size)
        self.texts = []

    def blit(self, source, dest, *args, **kwargs):
        rect = super().blit(source, dest, *args, **kwargs)
        if TEXT_IDS.get(id(source)) is source and not args:
            pos = dest.topleft if isinstance(dest, pygame.Rect) else dest
            self.texts.append(pygame.Rect(int(pos[0]), int(pos[1]), source.get_width(), source.get_height()))
        return rect


def problems_in(texts, size):
    """겹치는 글자 쌍과 화면 밖 글자"""
    found = []
    screen_rect = pygame.Rect((0, 0), size)
    # 그림자 2px 와 글자 안쪽 여백은 빼고 봐요
    boxes = [r.inflate(-4, -6) for r in texts if r.w > 6 and r.h > 6]
    for i, a in enumerate(boxes):
        if not screen_rect.contains(texts[i].inflate(-4, -4)):
            found.append(f"clipped at {tuple(texts[i])}")
        for b in boxes[i + 1:]:
            if a == b:
                continue                         # 같은 자리에 다시 그린 것 (덧그리기)
            cut = a.clip(b)
            if cut.w * cut.h > 0.2 * min(a.w * a.h, b.w * b.h):
                found.append(f"overlap {tuple(a)} x {tuple(b)}")
    return found


def run_menu(make_coro, screen):
    """메뉴 화면을 몇 장면 돌리고 마지막 장면의 글자 위치를 돌려줘요"""
    frames = [0]

    def events():
        frames[0] += 1
        if frames[0] == 4:
            return [pygame.event.Event(pygame.QUIT)]
        screen.texts.clear()                    # 마지막 장면만 검사
        return []

    shooter.menu_events = events
    asyncio.run(make_coro())
    return list(screen.texts)


def game_scene(screen, setup, frames=200):
    class Keys(dict):
        def __getitem__(self, key):
            return self.get(key, False)

    game = setup()
    game.briefing = None
    game.player.hp = 10 ** 6
    for _ in range(frames):
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
    game.player.hp = 100
    return game


def check(width, height, hud, shots):
    shooter.SETTINGS["hud"] = hud
    shooter.set_resolution(width, height)
    screen = Recorder((width, height))
    pygame.display.get_surface = lambda: screen
    shooter.open_window = lambda: screen
    shooter.available_resolutions = lambda: [(width, height)]
    shooter.present = lambda *a, **k: None
    pygame.display.flip = lambda: None
    save = dict(xp=25000, best=45, zbest=9, unlocked=[w["name"] for w in shooter.WEAPONS], wkills=dict(RIFLE=300))
    save["continue"] = 47
    for s in (5400, 3200):
        shooter.add_ranking(save, "zombies", dict(score=s, reached=9, kills=80, map="DEAD CITY", date="2026-10-31 14:00"))
    fonts = shooter.make_fonts()
    menus = {
        "intro": lambda: shooter.intro_screen(save),
        "settings": lambda: shooter.settings_screen(save),
        "controls": lambda: shooter.controls_screen(save),
        "skills": lambda: shooter.skills_screen(save),
        "stats": lambda: shooter.stats_screen(save),
        "challenges": lambda: shooter.challenge_screen(save),
        "achievements": lambda: shooter.achievements_screen(save),
        "missions": lambda: shooter.mission_screen(save),
        "my maps": lambda: shooter.map_slots_screen(save),
        "leaderboard": lambda: shooter.ranking_screen(save),
        "gunsmith": lambda: shooter.gunsmith_screen(save, "RIFLE"),
        "loadout": lambda: shooter.loadout_screen(save, dict(mode="campaign", round=1)),
        "help": lambda: shooter.help_screen(fonts),
    }
    results = {}
    for name, make in menus.items():
        results[name] = (run_menu(make, screen), screen.copy())

    def scene(name, setup, after=None, frames=200):
        game = game_scene(screen, setup, frames)
        if after:
            after(game)
        screen.texts.clear()
        game.draw(screen)
        results[name] = (list(screen.texts), screen.copy())

    scene("hud campaign", lambda: shooter.Game({}, 45), lambda g: setattr(g, "hint_timer", 5))
    scene("hud zombies", lambda: shooter.Game({}, 1, mode="zombies", loadout=LOADOUT))
    scene("round banner", lambda: shooter.Game({}, 2), frames=60)

    def wheel(g):
        g.wheel = dict(t=1.0, pick=11, open=True)
    scene("weapon wheel", lambda: shooter.Game({}, 45), wheel)

    def died(g):
        g.add_xp(1500)
        g.player.hp = 0
        g.game_over = True
        g.killcam_from = None
        g.finish_run()
        g.over_start = time.time() - 3
    scene("game over", lambda: shooter.Game(dict(save), 1, mode="zombies", loadout=LOADOUT), died)

    game = game_scene(screen, lambda: shooter.Game({}, 45), 30)
    screen.texts.clear()
    game.draw(screen, hud=False)
    shooter.draw_pause(screen, game.fonts, 0)
    results["pause"] = (list(screen.texts), screen.copy())

    bad = {}
    for name, (texts, image) in results.items():
        found = problems_in(texts, (width, height))
        if found:
            bad[name] = found
        if shots:
            os.makedirs(shots, exist_ok=True)
            pygame.image.save(image, os.path.join(shots, f"{width}x{height}_{hud}_{name.replace(' ', '_')}.png"))
    return bad


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true", help="여러 해상도와 UI SIZE")
    parser.add_argument("--shots", help="화면 사진을 저장할 폴더")
    parser.add_argument("--lang", choices=["ko", "en", "both"], default="both",
                        help="메뉴 언어 (ko 는 한글 글꼴이 있는 컴퓨터에서만, 없으면 건너뛰어요)")
    args = parser.parse_args()
    pygame.init()
    pygame.display.set_mode((320, 200))
    sizes = [(1280, 720)]
    huds = [100]
    if args.all:
        sizes = [(1280, 720), (1600, 900), (1920, 1080), (1024, 768)]
        huds = [75, 100, 125]
    langs = ["en", "ko"] if args.lang == "both" else [args.lang]
    if "ko" in langs and not shooter.korean_font_path():
        print("한글 글꼴이 없어서 한글 메뉴 검사는 건너뛰어요")
        langs.remove("ko")
    total = 0
    for lang in langs:
        shooter.SETTINGS["lang"] = 0 if lang == "ko" else 1
        for width, height in sizes:
            for hud in huds:
                bad = check(width, height, hud, args.shots and os.path.join(args.shots, lang))
                count = sum(len(v) for v in bad.values())
                total += count
                print(f"[{lang}] {width}x{height} UI {hud}%: {'OK' if not count else f'{count} problems'}")
                for name, found in bad.items():
                    for line in found[:6]:
                        print(f"    {name}: {line}")
                    if len(found) > 6:
                        print(f"    {name}: ... {len(found) - 6} more")
    print("결과: 겹침 없음" if total == 0 else f"결과: 문제 {total}개")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
