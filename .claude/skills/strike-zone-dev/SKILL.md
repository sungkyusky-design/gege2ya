---
name: strike-zone-dev
description: Develop, test and ship the Strike Zone pygame FPS (shooter.py) in this repo. Use whenever the task touches shooter.py - adding or tuning weapons, enemies, maps, missions, RPG unlocks/skills, sounds, hit effects, HUD or menus - and whenever the user asks to test, screenshot, merge or release the game. Covers the code map, add-a-thing recipes, the test scripts, known gotchas and the merge/release flow.
---

# Strike Zone 개발 스킬

`shooter.py` (게임 코드, 약 7000줄) 와 `strike/` (데이터 표) 로 된 레이캐스팅 FPS (pygame)를 고치고, 검사하고, 배포하는 방법.
사용자는 **Python 초보, 맥북(Apple Silicon), 키보드 위주(마우스 불편)** 로 플레이해요.

## 꼭 지킬 것

- **키보드만으로 모든 것이 돼야 해요.** 새 기능에는 키를 주고 (마우스/패드는 덤), 시작 화면·도움말(`HELP_TEXT`)·README에 적어요.
  이미 쓰는 키: WASD Shift C Space 화살표 F E Z G V X Q R B U M H P T Y J Tab 0-9 Enter Esc (게임 중) /
  Enter Z C O K S D T R A X ←→ Esc (시작 화면). 게임패드는 `PAD_GAME_KEYS` / `PAD_MENU_KEYS` 에 연결.
  키 바꾸기: 게임 코드는 언제나 **기본 키**(`pygame.K_f` 등)로 쓰면 돼요. `run()` 이 `remap_event` / `RemappedKeys` 로
  사용자가 바꾼 키를 기본 키로 바꿔서 넘겨줘요. 새 게임 키를 만들면 `KEY_ACTIONS` 에도 한 줄 넣어요.
- **주석과 화면 설명은 한국어, 쉬운 말**로 (사용자가 코드를 읽어요). 화면에 나오는 게임 글자는 영어 대문자 위주
  (한글 글꼴은 `fonts["help"]`, `fonts["help_big"]` 만 한글을 그릴 수 있어요).
- **웹(pygbag)에서도 돌아야 해요**: 반복문은 `async` + `await asyncio.sleep(0)`, 파일 대신 `browser.py` 의 저장 함수.
- 저장 정보(`save` dict)의 키를 바꾸거나 지우지 말고 추가만 해요 (사용자의 기존 진행이 이어져야 해요).
  쓰는 키: xp, best, continue, res, settings, loadout, wkills, unlocked, skills, zbest, mission, missions_done,
  keys, lifetime, achievements, camo, challenges, daily, gunsmith (loadout 에 tactical 추가).
- 특정 실제 게임(콜오브듀티 등)의 맵·이름을 그대로 베끼지 않아요. 장르 느낌은 OK, 고유 이름/맵 복제는 X.

## 데이터 파일 (strike/)

| 파일 | 들어 있는 것 |
| --- | --- |
| `strike/maps.py` | `MAPS` (손으로 그린 맵, 글자 설명 주석), `WALLS`, `FLOORS` |
| `strike/units.py` | `WEAPONS`, `WEAPON_INFO`, `UNLOCKS`, `PERKS`, `HORIZONTAL_KICK`, `ENEMY_TYPES`, `ENEMY_MAGS`, `COVER_USERS`, `GUN_LOOKS` |
| `strike/sounds.py` | `SOUND_RECIPES`, `GUN_SOUNDS`, `STEP_SOUNDS`, `ENEMY_STEPS`, `MUFFLED_SOUNDS`, `SOUND_MARK_KINDS` |
| `strike/story.py` | `CHALLENGES`, `STORY`, `RADIO`, `HELP_TEXT` |

`shooter.py` 맨 위에서 `from strike.xxx import ...` 로 가져와요. 표에 **새 이름**을 만들면 그 import 줄에도 추가하세요.
화면 크기(`WIDTH`, `UI`)나 지금 맵(`GAME_MAP`, `WALL_GRID`)처럼 **게임 중에 바뀌는 전역 값을 쓰는 코드는 shooter.py 에 두세요**
(다른 파일로 옮기면 옛 값을 보게 돼요).

## 코드 지도 (shooter.py, 위에서 아래로)

| 부분 | 찾는 이름 |
| --- | --- |
| 화면/조작 설정, 설정 메뉴 값 | `WIDTH`, `SETTINGS`, `DIFFICULTIES`, `apply_settings` |
| 게임 수치 | `REGEN_*`, `GRENADE_*`, `KNIFE_*`, `XP`, `STREAKS`, `HORIZONTAL_KICK` |
| 라운드 목표 / 무기 성장 / RPG | `OBJECTIVES`, `OBJECTIVE_ORDER`, `WEAPON_LEVELS`, `UNLOCKS`, `SKILLS`, `ACTIVE_SKILLS`, `apply_mods` |
| 로드아웃 / 무기 | `PERKS`, `WEAPON_INFO`, `WEAPONS`, `WEAPON_BY_NAME` |
| 적 | `ENEMY_TYPES`, `scaled_type`, `ZOMBIE_KINDS`, `ENEMY_MAGS`, `COVER_USERS`, `ARMORED` |
| 손으로 그린 맵 | `MAPS` (글자 설명은 바로 위 주석), `WALLS`, `FLOORS` |
| 맵 생성기 | `MAP_STYLES`, `generate_map`, `fill_block` |
| 생성 맵 / 미션 / 세트 | `GENERATED_MAPS`, `MISSIONS`, `MISSION_STAGES`, `CAMPAIGN_MAPS`, `SETS`, `variant_theme` |
| 레이캐스팅 | `load_map`, `cast_ray`, `is_blocked`, `can_see`, `fog` |
| 그림 (이미지 파일 없음) | `make_enemy_image`, `make_zombie_image`, `make_objective_image`, `make_viewmodel`, `GUN_LOOKS` |
| 소리 (소리 파일 없음) | `SOUND_RECIPES`, `GUN_SOUNDS`, `ENEMY_STEPS`, `Sounds.play(name, volume, pan)` |
| 등장인물 | `Enemy` (`update`, `shoot_at`, `update_cover`, `update_zombie`), `Player`, `Weapon`, `Arsenal`, `Projectile`, `Corpse` |
| 게임 전체 | `Game`: `start_round` → `start_battle` / `start_wave` / `start_mission` → `reset_round_state`; `update`; `draw`; `draw_hud` |
| 입력 | `Game.handle_event` (키 한 번), `Game.update(keys...)` (누르고 있는 키), `Gamepad`, `KeyState` |
| 메뉴 화면 | `intro_screen`, `loadout_screen`, `skills_screen`, `mission_screen`, `settings_screen`, `run` |

모드: `Game.mode` = `"campaign"` (100라운드, `set_of(round)`), `"zombies"`, `"mission"` (`self.stage`),
`"training"` (사격장: 저장 복사본으로 실행, `add_xp`/무기 성장/업적 꺼짐).
도전 모드는 `mode="campaign"` + `Game.challenge` (규칙은 `CHALLENGES`, `start_challenge`, `finish_challenge`).
떠 있는 적은 타입에 `lift`, 화면 위치는 꼭 `self.enemy_box(enemy)` 로.
부서지는 벽: `DESTRUCTIBLE`, `hit_wall`, `destroy_cell` (맵 줄은 `load_map` 에서 복사돼요).
분대 AI: `Game.update_squad` (역할 배정, 무전), `Enemy.wander` (수색·순찰), 외침은 `Game.shout`.
업적: `ACHIEVEMENTS` 에 (이름, 한, 영, 검사 함수) 한 줄, 누적 기록은 `save["lifetime"]`.

## 무엇을 추가할 때 고칠 곳

**무기**: `WEAPONS` 에 dict 추가 → `GUN_LOOKS` (총 모양) → `GUN_SOUNDS` (+ 필요하면 `SOUND_RECIPES`) →
`HORIZONTAL_KICK` → `WEAPON_INFO` (한/영 설명) → `UNLOCKS` (얻는 조건; 처음부터 주려면 `START_WEAPONS`) →
README 무기 표 / 얻는 조건 표. 포물선 유탄은 `lobbed=True`, 로켓은 `projectile=True`.

**적**: `ENEMY_TYPES` 에 추가 (hp, speed, sight, reaction, keep, range, fire, damage, accuracy, falloff, height, width, look) →
새 머리 모양이면 `make_enemy_image` 의 `head` 분기 → 탄창이 있으면 `ENEMY_MAGS` → 숨는 적이면 `COVER_USERS` →
캠페인 등장은 `pick_enemy_kind` (라운드 조건) 와 `start_battle` 의 `news` (처음 나오는 라운드) →
미션은 `mission_enemy_kind`. 좀비는 `melee=(피해, 간격)` 을 넣고 `ZOMBIE_KINDS` 와 `spawn_zombie`.

**손으로 그린 맵**: `strike/maps.py` 의 `MAPS` 에 테마 dict (name, sky, haze, sun, stars, ground, lit, fog, snow, camo, op, brief, rows).
`P` 하나, 먼 `E` 6개 이상. 다 그리면 반드시 `check_maps.py`. 캠페인 맵은 `CAMPAIGN_MAPS` 순서대로 22개
(늘리면 `SET_SIZE` 와 README 표도 확인). 메아리는 `ECHOES` 에 맵 이름으로.
전술 장비: `TACTICALS` (strike/units.py), `throw_tactical`, `tactical_hit`, 연막 `SMOKES`/`smoke_blocks`, 쿠킹 `update_cooking`.
총기 개조: `ATTACHMENTS` (strike/units.py), `save["gunsmith"]`, `apply_gunsmith`, `current_weapon_spec`, `gunsmith_screen`.
잠입: 적의 `aware`(0~1, `in_view` 앞쪽 시야), `Player.visibility`, 몰래 처치 how=`"TAKEDOWN!"`, `check_bodies`. 손전등 `Game.flashlight`, `draw_darkness`.
길찾기: 적/동료를 움직일 땐 `steer(agent, 목표, dt)` 로 방향을 받아요 (막히면 `Navigator` 의 길찾기 지도로 돌아감). 맵 모양이 바뀌면 `self.navigator.clear()`.
동료: `Ally`, `Game.spawn_allies` (라운드마다), `update_allies`, `hurt_ally`, 명령 `SQUAD_ORDERS` (K). 동료 처치는 how=`"ALLY"`.
실내: 바닥 `w` 위에는 천장(`INDOOR_FLOORS`, `CEILING`), 실내 벽 `i`, 문 `d` (`DOORS`, `Game.update_doors`). 실내 벽은 천장 높이(1.4)로.

**생성 맵**: `MAP_STYLES` 에 스타일 → `GENERATED_MAPS` 에 `generate_map(style, 26, 18, seed)` 로 테마 추가.
생성기는 막힌 칸을 스스로 메우지만, 결과는 `check_maps.py` 와 `screenshot.py --map NAME` 으로 꼭 눈으로 확인.

**미션**: `MISSIONS` 에 (name, style, seed, desc(한,영), theme) 추가 → 큰 맵(64x44)이 자동으로 생겨요.
단계는 `MISSION_STAGES`, 단계 목표 종류는 `OBJECTIVES` (REACH, HOSTAGE, CACHE, HOLD, BOMB).

**스킬 / 퍼크**: `SKILLS` 에 한 줄 → 효과는 `Game.rank_of("이름")` 으로 읽어서 해당 위치에 적용
(체력 `__init__`, 재장전/탄약 `make_arsenal`, 이동 `update`, 헤드샷 `shoot`, 폭발 `explode`, 회복 `update_effects`).
액티브는 `ACTIVE_SKILLS` + `use_skill` + `handle_event` 키 + 패드 키.

**소리**: `SOUND_RECIPES` 에 (길이, 줄어드는 빠르기, 잡음, 부드러움, 쿵 높이, 쿵 양, 맑은 소리 높이, 양, 음량).
위치가 있는 소리는 `self.play_at(name, pos, reach)` (왼쪽/오른쪽 방향이 들려요).

## 테스트 (모두 저장소 맨 위 폴더에서)

1. 문법/실수: `python -m pyflakes shooter.py strike tests` (없으면 `pip install pyflakes`)
   단위 테스트: `python -m unittest discover -s tests -v` (핵심 규칙 12개, 새 규칙을 만들면 `tests/test_core.py` 에 추가)
2. 맵: `python .claude/skills/strike-zone-dev/scripts/check_maps.py` → 문제 0개여야 해요
3. 전체 자동 플레이: `python .claude/skills/strike-zone-dev/scripts/smoke_test.py --seconds 20`
   → 메뉴 + 캠페인 여러 세트 + 좀비 + 미션 3개, 모두 `OK` 여야 해요. ms/frame 이 25를 넘으면 느려진 거예요.
4. 눈으로 확인: `python .claude/skills/strike-zone-dev/scripts/screenshot.py --round 41 --out /tmp/a.png`
   (`--map`, `--mode zombies`, `--mode mission --mission 1 --stage 2`, `--all-maps --out 폴더`, `--wait 초`, `--enemies`)
   찍은 PNG 는 Read 도구로 직접 보고, 여러 장은 PIL 로 한 장에 모아서 보면 편해요.
5. 바뀐 기능만 따로: 위 스크립트처럼 `shooter.Game(save, round, mode=..., loadout=...)` 을 만들고
   `game.update(1/60, Keys({...}), 0, 0, (False, False, False))` 로 장면을 진행하며 값을 출력해요.
6. 웹: `bash .claude/skills/strike-zone-dev/scripts/web_smoke.sh [z|o]` → `browser errors: none` 이어야 해요.
7. 밸런스: `python .claude/skills/strike-zone-dev/scripts/balance.py` (무기 처치 시간, 적 초당 피해). 숫자를 바꿨으면 전후 비교.
8. PR을 만들면 `.github/workflows/test.yml` 이 1~4번과 단위 테스트를 GitHub에서 자동으로 돌려요. 병합 전에 결과(초록 체크)를 확인하세요.

## 테스트할 때 함정 (실제로 겪은 것)

- 적이 하나도 없으면 바로 **라운드 클리어 → 게임이 멈춰요**. 움직임을 재려면 멀리 가만히 있는 적
  (`t=dict(e.t, sight=0, speed=0)`)을 하나 두세요.
- 적을 쓰러뜨리면 **히트스톱(0.04~0.07초)** 동안 `update` 가 아무것도 안 해요. 바로 다음 장면의 사격은 무시돼요.
- 총은 연사 간격(`arsenal.cooldown`), 교체 시간(`switch_left`) 이 남아 있으면 안 나가요. 테스트에선 0으로.
- 적을 테스트 위치에 둘 때 벽 안이나 벽 뒤면 안 보여요 (`shooter.can_see`, `shooter.is_blocked` 로 확인).
- `shooter.write_save` 를 테스트에서 덮어써서 진짜 저장 파일(`~/.gege2ya_save.json`)을 건드리지 마세요.
- `web_smoke.sh` 는 매번 빈 포트를 써요. 화면이 'Directory listing' 이면 오류로 알려줘요.
- 셸에서 `pkill -f pygbag` 처럼 넓게 죽이면 **지금 실행 중인 명령 자체가 죽어요** (exit 144). 백그라운드 서버는 `timeout` 으로 띄우세요.
- 큰 패치는 Python 스크립트의 `rep(old, new)` (개수 확인 assert) 로 하면, 하나라도 안 맞을 때 파일이 안 바뀌어서 안전해요.
  단, 다음 명령을 `&&` 로 잇지 않으면 실패한 채로 커밋될 수 있어요.

## 병합과 배포

1. 지정된 작업 브랜치에서 커밋 (시작 전에 `git fetch origin main && git checkout -B <브랜치> origin/main`).
2. 푸시 → GitHub MCP 로 PR 만들기 (owner `sungkyusky-design`, repo `market_brief` 이름으로도 돼요) → 사용자가 원하면 병합.
3. 병합되면 Actions 가 웹(Pages)과 exe / 맥 앱 릴리스를 자동으로 만들어요. 확인:
   `bash .claude/skills/strike-zone-dev/scripts/release_check.sh <병합 커밋 sha>`
4. 사용자에게 한국어로: 바뀐 점(쉬운 말, 표), 확인한 것과 **확인 못 한 것** (예: 소리는 직접 못 들음, 실제 패드 없음),
   맥 다운로드 링크 https://github.com/sungkyusky-design/gege2ya/releases/latest/download/Games-mac.zip ,
   이미 받은 앱은 켜서 U 로 업데이트.
