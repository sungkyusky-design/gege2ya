"""밸런스 보고서: 무기마다 일반병(GRUNT)을 쓰러뜨리는 데 걸리는 시간과, 적마다 나에게 주는 초당 피해를 계산해요.

숫자를 바꾼 뒤(WEAPONS, ENEMY_TYPES 등) 돌려 보면 너무 세거나 약한 것이 한눈에 보여요.
계산은 '모두 맞혔을 때' 기준이고, 실제 게임에선 빗나감이 있어요.

실행 (저장소 맨 위 폴더에서):
    python .claude/skills/strike-zone-dev/scripts/balance.py
"""
import math
import os
import sys

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.getcwd())

import shooter  # noqa: E402


def time_to_kill(spec, hp, head=False, level=1):
    """모두 맞혔을 때 hp를 깎는 데 걸리는 시간(초)과 발 수"""
    spec = shooter.apply_mods(spec, [], level)
    if spec["projectile"]:
        return None, None
    per_shot = (spec["head"] if head else spec["body"]) * spec["pellets"]
    shots = math.ceil(hp / per_shot)
    burst = spec.get("burst", 1)
    if burst > 1:                                   # 점사: 한 번에 여러 발
        groups = math.ceil(shots / burst)
        seconds = (groups - 1) * spec["delay"] + (shots - 1 - (groups - 1)) * spec.get("burst_delay", 0)
    else:
        seconds = (shots - 1) * spec["delay"]
    return seconds, shots


def main():
    hp = shooter.ENEMY_TYPES["GRUNT"]["hp"]
    print(f"무기 -> 일반병(체력 {hp}) 처치 시간 (모두 맞혔을 때, 레벨 1 / 레벨 10)")
    print(f"{'weapon':16s} {'body':>12s} {'head':>12s} {'body Lv10':>12s}")
    for spec in shooter.WEAPONS:
        body, n_body = time_to_kill(spec, hp)
        head, n_head = time_to_kill(spec, hp, head=True)
        body10, n10 = time_to_kill(spec, hp, level=10)
        if body is None:
            print(f"{spec['name']:16s} {'(explosive)':>12s}")
            continue
        print(f"{spec['name']:16s} {body:6.2f}s/{n_body:2d}발 {head:6.2f}s/{n_head:2d}발 {body10:6.2f}s/{n10:2d}발")

    print("\n적 -> 나에게 주는 초당 피해 (8칸 거리, 서 있을 때, 실력 100% / 200%)")
    for kind, t in shooter.ENEMY_TYPES.items():
        if "melee" in t:
            dmg, gap = t["melee"]
            print(f"{kind:10s} melee {dmg / gap:5.1f} /s (붙었을 때)")
            continue
        if not t["range"]:
            continue
        rates = []
        for skill in (1.0, 2.0):
            st = shooter.scaled_type(kind, skill)
            chance = max(0.08, st["accuracy"] - 8 * st["falloff"])
            per_shot = sum(st["damage"]) / 2
            gap = sum(st["fire"]) / 2
            rates.append(chance * per_shot / gap)
        print(f"{kind:10s} {rates[0]:5.1f} /s  ->  {rates[1]:5.1f} /s")


if __name__ == "__main__":
    main()
