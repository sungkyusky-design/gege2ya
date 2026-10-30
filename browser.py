"""
웹 브라우저(pygbag)에서 실행될 때만 필요한 도우미

컴퓨터에서 실행할 때는 아무 일도 하지 않아요.
"""

import sys


def fit_canvas():
    """게임 창 크기를 바꾼 뒤 호출하면, 브라우저 화면 비율을 새 크기에 맞춰줘요.

    pygbag은 처음 시작할 때의 캔버스 비율을 계속 쓰기 때문에,
    이걸 안 부르면 화면이 납작하거나 길쭉하게 늘어나 보여요.
    """
    if sys.platform == "emscripten":
        import platform
        platform.window.window_resize()
