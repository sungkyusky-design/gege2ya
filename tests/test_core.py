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

    def test_door_opens_when_near_and_closes_later(self):
        index = next(i for i, m in enumerate(shooter.MAPS) if m["name"] == "OFFICE BLOCK")
        game = shooter.Game({}, shooter.CAMPAIGN_MAPS.index(index) + 1, loadout=LOADOUT)
        game.briefing = None
        game.enemies = []
        (cx, cy) = next(iter(game.doors))
        game.player.pos = pygame.Vector2(cx + 0.5, cy + 1.5) if not shooter.is_blocked(cx + 0.5, cy + 1.5) \
            else pygame.Vector2(cx + 1.5, cy + 0.5)
        game.update_doors(0.1)
        self.assertFalse(shooter.is_blocked(cx + 0.5, cy + 0.5))
        game.player.pos = pygame.Vector2(1.5, 1.5)
        game.update_doors(5.0)
        self.assertTrue(shooter.is_blocked(cx + 0.5, cy + 0.5))

    def test_squadmates_follow_setting_and_skip_training(self):
        old = shooter.SETTINGS.get("squad", 2)
        try:
            shooter.SETTINGS["squad"] = 1
            self.assertEqual(len(shooter.Game({}, 3, loadout=LOADOUT).allies), 1)
            shooter.SETTINGS["squad"] = 2
            self.assertEqual(len(shooter.Game({}, 3, loadout=LOADOUT).allies), 2)
            self.assertEqual(len(shooter.Game({}, 1, mode="training", loadout=LOADOUT).allies), 0)
            self.assertEqual(len(shooter.Game({}, 1, loadout=LOADOUT, challenge="PISTOL").allies), 0)
        finally:
            shooter.SETTINGS["squad"] = old

    def test_ally_kills_give_half_xp_and_no_lifetime_kills(self):
        save = dict(xp=0)
        game = shooter.Game(save, 3, loadout=LOADOUT)
        game.on_kill(game.enemies[0], "ALLY")
        self.assertEqual(save["xp"], shooter.XP["kill"] // 2)
        self.assertNotIn("kills", save.get("lifetime", {}))
        self.assertEqual(game.streak, 0)

    def test_enemy_walks_around_a_building_to_reach_the_player(self):
        game = shooter.Game({}, 2, loadout=LOADOUT)
        game.briefing = None
        game.allies = []
        p = game.player
        # 나에게 곧장 걸어올 수 없는 (중간이 막힌) 먼 칸을 골라요
        cells = [pygame.Vector2(x + 0.5, y + 0.5) for y in range(shooter.MAP_H) for x in range(shooter.MAP_W)
                 if shooter.walkable_cell(x, y) and not shooter.is_blocked(x + 0.5, y + 0.5)]
        start = next(c for c in cells if 8 < c.distance_to(p.pos) < 14 and not shooter.walk_clear(c, p.pos)
                     and shooter.build_flow((int(p.pos.x), int(p.pos.y)))[int(c.y)][int(c.x)] is not None)
        enemy = shooter.Enemy(start.x, start.y, "GRUNT")
        enemy.t = dict(enemy.t, sight=0)
        for _ in range(60 * 25):
            if enemy.search is None:
                enemy.search = pygame.Vector2(p.pos)
            enemy.update(1 / 60, p)
            game.navigator.clock += 1 / 60
        self.assertLess(enemy.pos.distance_to(p.pos), 3.0)

    def _stealth_setup(self):
        game = shooter.Game({}, 1, loadout=LOADOUT)
        game.briefing, game.allies = None, []
        p = game.player
        for k in range(32):
            angle = k * math.pi / 16
            q = p.pos + pygame.Vector2(math.cos(angle), math.sin(angle)) * 5
            if shooter.walk_clear(p.pos, q) and shooter.can_see(p.pos, q):
                return game, q
        self.skipTest("트인 곳이 없어요")

    def test_enemy_only_notices_in_front(self):
        game, spot = self._stealth_setup()
        p = game.player
        for facing_me, expected in ((False, False), (True, True)):
            enemy = shooter.Enemy(spot.x, spot.y, "GRUNT")
            enemy.t = dict(enemy.t, speed=0)
            toward = (p.pos - enemy.pos).normalize()
            for _ in range(60 * 3):
                enemy.facing = toward if facing_me else -toward
                enemy.update(1 / 60, p)
            self.assertEqual(enemy.sees, expected)

    def test_silent_takedown_from_behind(self):
        game, spot = self._stealth_setup()
        p = game.player
        away = (spot - p.pos).normalize()
        enemy = shooter.Enemy(*(p.pos + away * 1.0), "HEAVY")      # 칼 한 번으론 안 죽는 적도 한 번에
        enemy.facing = pygame.Vector2(away)
        game.enemies = [enemy, shooter.Enemy(0.5, 0.5, "GRUNT")]
        p.angle = math.atan2(away.y, away.x)
        game.knife_attack()
        self.assertNotIn(enemy, game.enemies)

    def test_gunsmith_keeps_old_saves_and_changes_stats(self):
        save = {"wkills": {"RIFLE": 40}}
        old = shooter.current_weapon_spec(save, "RIFLE")               # 총기 개조 전: 예전처럼 자동 부착물
        same = shooter.current_weapon_spec(save, "RIFLE", shooter.gunsmith_default(save, "RIFLE"))
        self.assertEqual(old["mag"], same["mag"])
        fast = shooter.current_weapon_spec(save, "RIFLE", dict(shooter.gunsmith_default(save, "RIFLE"),
                                                                MAGAZINE="FAST MAG"))
        self.assertLess(fast["reload"], old["reload"])
        self.assertFalse(shooter.attachment_unlocked({"wkills": {}}, "RIFLE", "OPTIC", "4X SCOPE"))

    def test_smoke_blocks_enemy_view(self):
        a, b = pygame.Vector2(0, 0), pygame.Vector2(10, 0)
        shooter.SMOKES[:] = [[pygame.Vector2(5, 0.3), shooter.SMOKE_TIME / 2]]
        try:
            self.assertTrue(shooter.smoke_blocks(a, b))
            self.assertFalse(shooter.smoke_blocks(a, pygame.Vector2(0, 10)))
        finally:
            shooter.SMOKES.clear()

    def test_save_code_round_trip_and_rejects_typos(self):
        save = dict(xp=3000, best=21, res=2, wkills={"RIFLE": 50}, lifetime={"kills": 99})
        code = shooter.export_code(save)
        back = shooter.import_code(code[:40] + "\n " + code[40:])         # 줄바꿈/빈칸이 섞여도 돼요
        self.assertEqual(back, {k: v for k, v in save.items() if k != "res"})
        broken = code[:20] + ("x" if code[20] != "x" else "y") + code[21:]
        self.assertIsNone(shooter.import_code(broken))
        self.assertIsNone(shooter.import_code("nothing here"))

    def test_zombie_buyables(self):
        game = shooter.Game({}, 1, mode="zombies", loadout=LOADOUT)
        game.allies = []
        game.points = 5000
        barricade = next(b for b in game.buyables if b["kind"] == "barricade")
        cx, cy = barricade["cell"]
        self.assertTrue(shooter.is_blocked(cx + 0.5, cy + 0.5))
        game.buy_item(barricade)
        self.assertFalse(shooter.is_blocked(cx + 0.5, cy + 0.5))
        self.assertEqual(game.points, 5000 - shooter.BARRICADE_COST)
        wall = next(b for b in game.buyables if b["kind"] == "weapon")
        game.buy_item(wall)
        self.assertEqual(game.arsenal.current.spec["name"], wall["weapon"])
        self.assertEqual(game.price_of(wall), wall["cost"] // 2)           # 다시 사면 탄약만 반값

    def test_mounted_machine_gun(self):
        game = shooter.Game({}, 5, loadout=LOADOUT)
        game.briefing, game.allies = None, []
        self.assertTrue(game.turrets)
        game.player.pos = pygame.Vector2(game.turrets[0]["pos"]) + pygame.Vector2(0.5, 0)
        before = [w.spec["name"] for w in game.arsenal.weapons]
        self.assertTrue(game.toggle_mount())
        self.assertEqual(game.arsenal.current.spec["name"], "MOUNTED MG")
        game.player.pos += pygame.Vector2(3, 0)
        game.update_mounted(0.1)
        self.assertEqual(game.player.pos, game.turrets[0]["pos"])            # 자리 고정
        game.toggle_mount()
        self.assertEqual([w.spec["name"] for w in game.arsenal.weapons], before)

    def test_custom_map_validation_and_practice(self):
        rows = shooter.blank_map()
        self.assertEqual(shooter.validate_map(rows), [])
        walled = [list(r) for r in rows]
        walled[5] = list("R" * shooter.EDIT_W)                         # 적과 나 사이를 벽으로 완전히 막기
        self.assertTrue(shooter.validate_map(["".join(r) for r in walled]))
        save = dict(xp=100)
        game = shooter.Game(save, 1, mode="custom", loadout=LOADOUT, custom=dict(name="T", rows=rows))
        game.on_kill(game.enemies[0], "HEADSHOT!")
        self.assertEqual(save["xp"], 100)                                # 연습: 경험치 없음
        self.assertNotIn("lifetime", save)

    def test_ranking_keeps_top_ten_in_order(self):
        save = {}
        places = [shooter.add_ranking(save, "zombies", dict(score=s)) for s in (50, 10, 30)]
        self.assertEqual(places, [1, 2, 2])                               # 30 은 50 다음, 10 위로
        for s in range(20):
            shooter.add_ranking(save, "zombies", dict(score=100 + s))
        table = save["rankings"]["zombies"]
        self.assertEqual(len(table), shooter.RANK_SIZE)
        self.assertEqual([e["score"] for e in table], sorted([e["score"] for e in table], reverse=True))
        self.assertIsNone(shooter.add_ranking(save, "zombies", dict(score=1)))   # 10등 밖
        self.assertEqual(shooter.add_ranking(save, "zombies", dict(score=119)), 2)  # 같은 점수는 먼저 세운 기록이 위

    def test_zombie_death_goes_to_ranking_once(self):
        save = {}
        game = shooter.Game(save, 1, mode="zombies", loadout=LOADOUT)
        game.add_xp(500)
        game.player.hp = 0
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
        self.assertTrue(game.game_over)
        game.finish_run()                                                 # 메뉴로 나가도 두 번 들어가지 않아요
        table = save["rankings"]["zombies"]
        self.assertEqual(len(table), 1)
        self.assertEqual((table[0]["score"], table[0]["reached"]), (500, 1))
        self.assertEqual(game.run_place, 1)
        game.retry_round()                                                # 다시 하면 새 판
        self.assertEqual(game.run_score, 0)

    def test_weapon_wheel_reaches_every_weapon(self):
        game = shooter.Game({}, 45)                                       # 무기 14개 모두
        a = game.arsenal
        self.assertGreater(len(a.weapons), 10)
        tab = Keys({pygame.K_TAB: True})
        down = lambda key: game.handle_event(pygame.event.Event(pygame.KEYDOWN, key=key, mod=0, unicode=""))
        down(pygame.K_TAB)                                                # 짧게 누르면 다음 무기
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))
        self.assertEqual(a.index, 1)
        down(pygame.K_TAB)                                                # 꾹 누르면 휠
        for _ in range(30):
            game.update(1 / 60, tab, 0, 0, (False, False, False))
        self.assertTrue(game.wheel["open"])
        for _ in range(len(a.weapons) - 2):
            down(pygame.K_RIGHT)
        game.update(1 / 60, Keys(), 0, 0, (False, False, False))         # 떼면 고른 무기로
        self.assertIsNone(game.wheel)
        self.assertEqual(a.index, len(a.weapons) - 1)

    def test_fit_text(self):
        font = shooter.make_fonts()["small"]
        text = shooter.fit_text(font, "MACHINE PISTOL EXTRA LONG NAME", 80)
        self.assertLessEqual(font.size(text)[0], 80)
        self.assertTrue(text.endswith(".."))
        self.assertEqual(shooter.fit_text(font, "SMG", 80), "SMG")

    def test_split_hint_finds_keys(self):
        self.assertEqual(shooter.split_hint("↑↓ 고르기   Enter / ESC 저장하고 돌아가기   - 설명"),
                         [("↑↓", "고르기"), ("Enter / ESC", "저장하고 돌아가기"), ("", "- 설명")])
        self.assertEqual(shooter.split_hint("UP/DOWN choose   G gunsmith"), [("UP/DOWN", "choose"), ("G", "gunsmith")])

    def test_every_weapon_has_a_class(self):
        for spec in shooter.WEAPONS:
            self.assertNotEqual(shooter.weapon_class(spec["name"]), "OTHER", spec["name"])
        ordered = shooter.class_order(["PISTOL", "SMG", "RIFLE"])
        self.assertEqual(ordered, ["RIFLE", "SMG", "PISTOL"])

    def test_menu_translation(self):
        fonts = dict(ko_ui=True)
        self.assertEqual(shooter.tr(fonts, "SETTINGS"), "설정")
        self.assertEqual(shooter.tr(fonts, "ACHIEVEMENTS  3 / 16"), "업적  3 / 16")
        self.assertEqual(shooter.tr(fonts, "RIFLE"), "RIFLE")                  # 없는 글자는 그대로
        self.assertEqual(shooter.tr(dict(ko_ui=False), "SETTINGS"), "SETTINGS")
        before = shooter.SETTINGS["lang"]
        shooter.SETTINGS["lang"] = 0
        shooter.change_setting("lang", 1)                                    # 한국어 → 영어
        self.assertEqual(shooter.setting_text("lang"), "ENGLISH")
        self.assertFalse(shooter.make_fonts()["ko_ui"])
        shooter.SETTINGS["lang"] = before

    def test_key_labels_follow_rebinding(self):
        self.assertEqual(shooter.kl(pygame.K_g), "G")
        self.assertEqual(shooter.kl(pygame.K_LSHIFT), "SHIFT")
        shooter.rebind(pygame.K_g, pygame.K_y)                           # 수류탄을 Y 로
        self.assertEqual(shooter.kl(pygame.K_g), "Y")
        shooter.apply_keys({})                                           # 처음대로
        self.assertEqual(shooter.kl(pygame.K_g), "G")

    def test_set_of(self):
        self.assertEqual([shooter.set_of(r) for r in (1, 20, 21, 100, 150)], [1, 1, 2, 5, 5])


if __name__ == "__main__":
    unittest.main()
