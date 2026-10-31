"""스트라이크 존 핵심 규칙 자동 테스트 (화면 없이 돌아가요)

실행 (저장소 맨 위 폴더에서):
    python -m unittest discover -s tests -v
"""
import math
import os
import sys
import unittest

os.environ.setdefault("SDL_VIDEODRIVER", "dummy")
os.environ.setdefault("SDL_AUDIODRIVER", "dummy")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pygame  # noqa: E402
import shooter  # noqa: E402

shooter.write_save = lambda save: None          # 진짜 저장 파일은 건드리지 않아요
LOADOUT = dict(primary="RIFLE", secondary="PISTOL", perk="IRON SKIN")


class Keys(dict):
    def __getitem__(self, key):
        return self.get(key, False)


def setUpModule():
    pygame.init()
    pygame.display.set_mode((shooter.WIDTH, shooter.HEIGHT))


class RaycastTest(unittest.TestCase):
    def setUp(self):
        shooter.load_map(shooter.CAMPAIGN_MAPS[0])

    def test_walls_are_sorted_by_distance(self):
        p = pygame.Vector2(shooter.find_cells("P")[0])
        for k in range(16):
            floors, walls = shooter.cast_ray(p.x, p.y, k * math.pi / 8)
            dists = [w[0] for w in walls]
            self.assertEqual(dists, sorted(dists))
            self.assertTrue(floors, "바닥 구간이 하나는 있어야 해요")

    def test_can_see_is_symmetric_and_blocked_by_walls(self):
        cells = [pygame.Vector2(x + 0.5, y + 0.5) for y in range(shooter.MAP_H) for x in range(shooter.MAP_W)
                 if not shooter.is_blocked(x + 0.5, y + 0.5)]
        a = cells[0]
        for b in cells[::37]:
            self.assertEqual(shooter.can_see(a, b), shooter.can_see(b, a))
        wall = next((x, y) for y in range(shooter.MAP_H) for x in range(shooter.MAP_W) if shooter.WALL_GRID[y][x])
        center = pygame.Vector2(wall[0] + 0.5, wall[1] + 0.5)
        left, right = center - pygame.Vector2(2, 0), center + pygame.Vector2(2, 0)
        if not shooter.is_opaque(left.x, left.y) and not shooter.is_opaque(right.x, right.y):
            self.assertFalse(shooter.can_see(left, right))


class KeyBindingTest(unittest.TestCase):
    def tearDown(self):
        shooter.apply_keys({})

    def test_rebind_swaps_keys(self):
        shooter.rebind(pygame.K_f, pygame.K_h)
        self.assertEqual(shooter.bound_key(pygame.K_f), pygame.K_h)
        self.assertEqual(shooter.KEY_MAP[pygame.K_f], pygame.K_h)    # F 는 원래 H 가 하던 일

    def test_saved_keys_round_trip(self):
        shooter.rebind(pygame.K_w, pygame.K_i)
        saved = shooter.saved_keys()
        shooter.apply_keys({})
        shooter.apply_keys(saved)
        self.assertEqual(shooter.bound_key(pygame.K_w), pygame.K_i)


class WeaponTest(unittest.TestCase):
    def test_weapon_level_increases_damage(self):
        rifle = shooter.WEAPON_BY_NAME["RIFLE"]
        self.assertGreater(shooter.apply_mods(rifle, [], 5)["body"], rifle["body"])
        self.assertEqual(shooter.apply_mods(rifle, [], 1)["body"], rifle["body"])

    def test_shotgun_loads_one_shell_at_a_time_and_firing_cancels(self):
        arsenal = shooter.Arsenal([shooter.WEAPON_BY_NAME["SHOTGUN"]])
        gun = arsenal.current
        gun.mag = 2
        arsenal.reload()
        arsenal.update(shooter.SHELL_RELOAD["SHOTGUN"] + 0.01)
        self.assertEqual(gun.mag, 3)
        self.assertTrue(arsenal.try_fire())
        self.assertEqual(arsenal.reload_left, 0.0)


class GameTest(unittest.TestCase):
    def test_old_save_without_new_keys_still_works(self):
        save = dict(xp=1200, best=7)                             # 예전 저장 파일처럼 키가 적어요
        game = shooter.Game(save, 7, loadout=LOADOUT)
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
        self.assertEqual(game.save["xp"], 1200)

    def test_destroyed_crate_does_not_change_original_map(self):
        index = next(i for i in shooter.CAMPAIGN_MAPS if any("K" in row for row in shooter.MAPS[i]["rows"]))
        game = shooter.Game({}, shooter.CAMPAIGN_MAPS.index(index) + 1, loadout=LOADOUT)
        cx, cy = next((x, y) for y, row in enumerate(shooter.GAME_MAP) for x, ch in enumerate(row) if ch == "K")
        game.destroy_cell(cx, cy)
        self.assertNotEqual(shooter.GAME_MAP[cy][cx], "K")
        self.assertEqual(shooter.MAPS[index]["rows"][cy][cx], "K")
        self.assertFalse(shooter.is_blocked(cx + 0.5, cy + 0.5))

    def test_training_gives_no_xp(self):
        game = shooter.Game(dict(xp=500), 1, mode="training", loadout=LOADOUT)
        game.on_kill(game.enemies[0], "HEADSHOT!")
        self.assertEqual(game.save["xp"], 500)
        self.assertNotIn("lifetime", game.save)

    def test_daily_challenge_is_the_same_all_day(self):
        a = shooter.Game({}, 1, loadout=LOADOUT, challenge="DAILY")
        b = shooter.Game({}, 1, loadout=LOADOUT, challenge="DAILY")
        self.assertEqual(a.round, b.round)
        self.assertEqual([(e.kind, tuple(e.pos)) for e in a.enemies], [(e.kind, tuple(e.pos)) for e in b.enemies])

    def test_challenge_does_not_move_campaign_progress(self):
        save = {"continue": 33}
        game = shooter.Game(save, 1, loadout=LOADOUT, challenge="PISTOL")
        game.player.hp = 0
        game.briefing = None
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
        self.assertTrue(game.game_over)
        self.assertEqual(save["continue"], 33)

    def test_set_of(self):
        self.assertEqual([shooter.set_of(r) for r in (1, 20, 21, 100, 150)], [1, 1, 2, 5, 5])


if __name__ == "__main__":
    unittest.main()
