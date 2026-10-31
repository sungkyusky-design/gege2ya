"""맵 검사: 모든 맵이 올바른지 확인해요.

검사하는 것:
    - 줄 길이가 모두 같은지
    - 시작 위치 P가 딱 하나인지
    - 걸어갈 수 있는 모든 칸이 P에서 이어지는지 (갇힌 칸이 없는지)
    - 적 출현 위치 E 중 시작에서 충분히 먼 곳이 몇 개인지
    - 상자(a, h, n)와 E에 걸어서 갈 수 있는지

실행 (저장소 맨 위 폴더에서):
    python .claude/skills/strike-zone-dev/scripts/check_maps.py
    python .claude/skills/strike-zone-dev/scripts/check_maps.py --show "SUBURB"   # 맵 모양도 출력

문제가 있으면 끝날 때 exit code 1 (CI나 다른 스크립트에서 쓸 수 있어요).
"""
import math
import os
import sys
from collections import deque

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.getcwd())

import shooter  # noqa: E402  (저장소 맨 위 폴더에서 실행해야 해요)

BLOCKERS = set(shooter.WALLS) | set("~TcXIv")      # shooter.is_blocked 와 같은 기준
SAFE = shooter.SAFE_SPAWN


def check(theme):
    rows = theme["rows"]
    problems = []
    width = len(rows[0])
    if any(len(r) != width for r in rows):
        return [f"줄 길이가 달라요: {sorted(set(len(r) for r in rows))}"]
    starts = [(c, r) for r, line in enumerate(rows) for c, ch in enumerate(line) if ch == "P"]
    if len(starts) != 1:
        return [f"P가 {len(starts)}개예요 (1개여야 해요)"]
    start = starts[0]

    def walkable(c, r):
        return 0 <= r < len(rows) and 0 <= c < width and rows[r][c] not in BLOCKERS

    seen = {start}
    queue = deque([start])
    while queue:
        c, r = queue.popleft()
        for dc, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (c + dc, r + dr)
            if n not in seen and walkable(*n):
                seen.add(n)
                queue.append(n)
    all_walk = {(c, r) for r in range(len(rows)) for c in range(width) if walkable(c, r)}
    lost = all_walk - seen
    if lost:
        problems.append(f"갈 수 없는 빈칸 {len(lost)}개: {sorted(lost)[:6]}")
    spawns = [(c, r) for r, line in enumerate(rows) for c, ch in enumerate(line) if ch == "E"]
    far = [e for e in spawns if math.dist(e, start) > SAFE]
    need = 20 if theme.get("mission") else 6
    if len(far) < need:
        problems.append(f"먼 적 출현 위치가 {len(far)}개 (최소 {need}개)")
    for r, line in enumerate(rows):
        for c, ch in enumerate(line):
            if ch in "ahnE" and (c, r) not in seen:
                problems.append(f"'{ch}'에 갈 수 없어요 ({c}, {r})")
    return problems


def main():
    show = sys.argv[sys.argv.index("--show") + 1] if "--show" in sys.argv else None
    bad = 0
    for theme in shooter.MAPS:
        kind = "미션" if theme.get("mission") else ("좀비" if theme.get("zombie") else "캠페인")
        rows = theme["rows"]
        problems = check(theme)
        mark = "OK " if not problems else "BAD"
        print(f"{mark} [{kind}] {theme['name']:16s} {len(rows[0])}x{len(rows)}  E={sum(r.count('E') for r in rows)}")
        for p in problems:
            print("      -", p)
        bad += bool(problems)
        if show and theme["name"] == show:
            for i, line in enumerate(rows):
                print(f"      {i:2d} {line}")
    print(f"\n맵 {len(shooter.MAPS)}개 중 문제 있는 맵 {bad}개 (캠페인 맵 {len(shooter.CAMPAIGN_MAPS)}개)")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
