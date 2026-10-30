"""
실행 환경(웹 브라우저 / 컴퓨터)에 따라 필요한 도우미
"""

import json
import os
import sys

import pygame

IN_BROWSER = sys.platform == "emscripten"

SAVE_KEY = "gege2ya_save"                                            # 브라우저 저장 이름
SAVE_PATH = os.path.join(os.path.expanduser("~"), ".gege2ya_save.json")   # 컴퓨터 저장 파일


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


def load_save():
    """저장된 진행 상황을 읽어요. 없거나 읽을 수 없으면 빈 dict.
    컴퓨터: 내 폴더의 .gege2ya_save.json 파일 / 브라우저: 브라우저 저장소(localStorage)"""
    try:
        if IN_BROWSER:
            import platform
            raw = platform.window.localStorage.getItem(SAVE_KEY)
        else:
            with open(SAVE_PATH, encoding="utf-8") as f:
                raw = f.read()
        data = json.loads(raw) if raw else {}
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def write_save(data):
    """진행 상황을 저장해요. 저장에 실패해도 게임은 계속돼요."""
    try:
        raw = json.dumps(data)
        if IN_BROWSER:
            import platform
            platform.window.localStorage.setItem(SAVE_KEY, raw)
        else:
            with open(SAVE_PATH, "w", encoding="utf-8") as f:
                f.write(raw)
    except Exception:
        pass
