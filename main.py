"""
게임 시작 메뉴

두 게임 중 하나를 골라서 시작해요. 게임에서 ESC를 누르면 이 메뉴로 돌아와요.
웹 브라우저 버전도 이 파일에서 시작해요 (pygbag은 main.py를 찾아서 실행해요).

받아서 쓰는 앱(exe / 맥 앱)이면, 켤 때 새 버전이 있는지 확인해서 알려줘요.

실행 방법:
    pip install pygame
    python main.py
"""

import asyncio
import threading
import webbrowser

import pygame

import game
import shooter
from browser import IN_BROWSER, prepare_window

try:
    from build_info import BUILD      # 앱을 만들 때 GitHub가 버전(커밋 번호)을 적어 넣어요
except ImportError:
    BUILD = "dev"

WIDTH, HEIGHT = 960, 600
RELEASE_PAGE = "https://github.com/sungkyusky-design/gege2ya/releases/latest"
VERSION_URL = RELEASE_PAGE + "/download/version.txt"

# 메뉴에 보여줄 게임 목록: (키보드 숫자키, 제목, 설명, 실행 함수, 색)
GAMES = [
    (pygame.K_1, "1. Don't Look", "SCP-096 chase game", game.run, (220, 60, 60)),
    (pygame.K_2, "2. Strike Zone", "FPS in a neon 80s city", shooter.run, (70, 150, 240)),
]

latest_build = None     # 인터넷에서 확인한 최신 버전 (모르면 None)


def check_for_update():
    """최신 버전 번호를 받아 와요. 인터넷이 안 되면 조용히 넘어가요.
    (메뉴가 멈추지 않도록 따로 돌아가는 작업(스레드)에서 실행해요)"""
    global latest_build
    import ssl
    import urllib.request
    contexts = []
    try:
        import certifi                          # 앱 안에 들어 있는 인증서 목록
        contexts.append(ssl.create_default_context(cafile=certifi.where()))
    except ImportError:
        pass
    contexts.append(ssl.create_default_context())   # 컴퓨터에 깔린 인증서 목록 (회사/학교 네트워크용)
    for context in contexts:
        try:
            with urllib.request.urlopen(VERSION_URL, timeout=5, context=context) as response:
                latest_build = response.read().decode().strip()
            return
        except Exception:
            continue


def update_available():
    return BUILD != "dev" and latest_build is not None and latest_build != BUILD


def draw_menu(screen, title_font, font, small_font, buttons, mouse_pos):
    screen.fill((20, 22, 28))
    title = title_font.render("GAME SELECT", True, (240, 240, 240))
    screen.blit(title, title.get_rect(center=(WIDTH / 2, 120)))

    for rect, (_, name, desc, _, color) in zip(buttons, GAMES):
        hover = rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, color if hover else (45, 48, 58), rect, border_radius=16)
        pygame.draw.rect(screen, color, rect, 3, border_radius=16)
        text = font.render(name, True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=(rect.centerx, rect.centery - 18)))
        text = small_font.render(desc, True, (220, 220, 220))
        screen.blit(text, text.get_rect(center=(rect.centerx, rect.centery + 24)))

    hint = small_font.render("Click or press 1 / 2   -   ESC in game: back to menu", True, (150, 150, 160))
    screen.blit(hint, hint.get_rect(center=(WIDTH / 2, HEIGHT - 60)))
    if BUILD != "dev":
        label = small_font.render(f"version {BUILD}", True, (110, 110, 120))
        screen.blit(label, label.get_rect(bottomright=(WIDTH - 12, HEIGHT - 10)))
    if update_available():
        notice = font.render("NEW VERSION AVAILABLE!  Press U to download", True, (255, 220, 90))
        screen.blit(notice, notice.get_rect(center=(WIDTH / 2, HEIGHT - 110)))


async def main():
    pygame.init()
    if not IN_BROWSER and BUILD != "dev":
        threading.Thread(target=check_for_update, daemon=True).start()
    title_font = pygame.font.Font(None, 80)
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 28)
    # 게임 버튼 두 개를 나란히 배치
    buttons = [pygame.Rect(100 + i * 400, 230, 360, 200) for i in range(len(GAMES))]

    while True:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Game Select")
        prepare_window()
        chosen = None

        while chosen is None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    for key, *_, run, _ in GAMES:
                        if event.key == key:
                            chosen = run
                    if event.key == pygame.K_u and update_available():
                        webbrowser.open(RELEASE_PAGE)      # 다운로드 페이지 열기
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for rect, (_, _, _, run, _) in zip(buttons, GAMES):
                        if rect.collidepoint(event.pos):
                            chosen = run

            draw_menu(screen, title_font, font, small_font, buttons, pygame.mouse.get_pos())
            pygame.display.flip()
            await asyncio.sleep(0)

        # 고른 게임 실행. 창을 닫았으면(False) 프로그램 종료, ESC면 메뉴로
        if not await chosen():
            pygame.quit()
            return


if __name__ == "__main__":
    asyncio.run(main())
