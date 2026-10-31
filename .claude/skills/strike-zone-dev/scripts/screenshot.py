"""게임 화면 스크린샷: 원하는 모드/라운드/맵을 화면 없이 그려서 PNG로 저장해요.

예 (저장소 맨 위 폴더에서):
    python .claude/skills/strike-zone-dev/scripts/screenshot.py --round 41 --out /tmp/r41.png
    python .claude/skills/strike-zone-dev/scripts/screenshot.py --map "SKI LODGE" --out /tmp/ski.png
    python .claude/skills/strike-zone-dev/scripts/screenshot.py --mode zombies --wait 8 --out /tmp/z.png
    python .claude/skills/strike-zone-dev/scripts/screenshot.py --mode mission --mission 1 --stage 2 --out /tmp/m.png
    python .claude/skills/strike-zone-dev/scripts/screenshot.py --all-maps --out /tmp/maps   # 맵마다 한 장

옵션:
    --mode campaign|zombies|mission   (기본 campaign)
    --round N        캠페인 라운드 (세트 분위기가 반영돼요: 41~60 밤, 61~80 폭풍우, 81~ 붉은 하늘)
    --map NAME       그 맵이 나오는 첫 라운드로 (캠페인)
    --mission N --stage N
    --wait SECONDS   찍기 전에 게임을 그만큼 진행 (적이 다가오는 모습 등). 기본 0
    --enemies        적을 지우지 않고 그대로 둬요 (기본은 풍경이 잘 보이게 적을 지워요)
    --out PATH       파일 (또는 --all-maps면 폴더)
"""
import math
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.getcwd())

import pygame  # noqa: E402
import shooter  # noqa: E402

shooter.write_save = lambda save: None


def arg(name, default=None, cast=str):
    return cast(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


class Keys(dict):
    def __getitem__(self, key):
        return self.get(key, False)


def look_open(game):
    """가장 멀리 트인 방향을 바라봐요 (벽만 찍히지 않게)"""
    p = game.player.pos

    def depth(k):
        walls = shooter.cast_ray(p.x, p.y, k * math.pi / 8)[1]
        return walls[0][0] if walls else 99
    if game.objective:
        offset = game.objective["pos"] - p
        game.player.angle = math.atan2(offset.y, offset.x)
    else:
        game.player.angle = max(range(16), key=depth) * math.pi / 8
    game.player.pitch = 10


def shoot(game, path):
    screen = pygame.display.get_surface()
    game.banner_timer = game.hint_timer = 0
    if "--enemies" not in sys.argv:
        game.enemies = [e for e in game.enemies if e.pos.distance_to(game.player.pos) > 40]
    look_open(game)
    for _ in range(int(arg("--wait", 0, float) * 60)):
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
    game.draw(screen)
    pygame.image.save(screen, path)
    print("saved", path)


def main():
    pygame.init()
    pygame.display.set_mode((shooter.WIDTH, shooter.HEIGHT))
    loadout = dict(primary="RIFLE", secondary="PISTOL", perk="HEAVY ROUNDS")
    out = arg("--out", "screenshot.png")
    if "--all-maps" in sys.argv:
        os.makedirs(out, exist_ok=True)
        for k, index in enumerate(shooter.CAMPAIGN_MAPS):
            game = shooter.Game({}, k + 1, loadout=loadout)
            shoot(game, os.path.join(out, f"{k + 1:02d}_{shooter.MAPS[index]['name'].replace(' ', '_')}.png"))
        return
    mode = arg("--mode", "campaign")
    round_no = arg("--round", 1, int)
    if arg("--map"):
        names = [shooter.MAPS[i]["name"] for i in shooter.CAMPAIGN_MAPS]
        round_no = names.index(arg("--map")) + 1
    game = shooter.Game({}, round_no, mode=mode, loadout=loadout,
                        mission=arg("--mission", 0, int), stage=arg("--stage", 0, int))
    shoot(game, out)


if __name__ == "__main__":
    main()
