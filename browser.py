"""
실행 환경(웹 브라우저 / 컴퓨터)에 따라 필요한 도우미
"""

import sys

import pygame

IN_BROWSER = sys.platform == "emscripten"


def prepare_window():
    """pygame.display.set_mode()로 창을 만든 직후에 불러주세요.

    - 웹 브라우저(pygbag): 화면 비율을 새 창 크기에 맞춰요.
      pygbag은 처음 시작할 때의 캔버스 비율을 계속 쓰기 때문에,
      이걸 안 부르면 화면이 납작하거나 길쭉하게 늘어나 보여요.
    - 컴퓨터: 글자 입력기(IME)를 꺼요.
      한글 입력 상태면 입력기가 W A S D 같은 글자 키를 가로채서 한글을 조합하느라
      게임에 키가 전달되지 않아요. 입력기를 끄면 한글 상태여도 키가 바로 들어와요.
    """
    if IN_BROWSER:
        import platform
        platform.window.window_resize()
    else:
        pygame.key.stop_text_input()
