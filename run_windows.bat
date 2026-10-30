@echo off
rem 더블클릭하면 게임에 필요한 pygame을 설치하고 게임 메뉴를 열어요.
cd /d "%~dp0"
python -m pip install --quiet --user pygame
python main.py
if errorlevel 1 (
    echo.
    echo 실행하지 못했어요. Python이 설치되어 있는지 확인해 주세요: https://www.python.org/downloads/
    echo 설치할 때 "Add python.exe to PATH" 를 꼭 체크하세요.
    pause
)
