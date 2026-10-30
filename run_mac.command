#!/bin/bash
# 더블클릭하면 게임에 필요한 pygame을 설치하고 게임 메뉴를 열어요.
cd "$(dirname "$0")"
python3 -m pip install --quiet --user pygame
python3 main.py
