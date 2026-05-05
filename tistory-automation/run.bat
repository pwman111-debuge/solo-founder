@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo === 티스토리 자동 포스팅 시작 ===
python post_tistory.py
echo.
pause
