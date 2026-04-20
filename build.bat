@echo off
REM ============================================================
REM  FLP Organizer - Build script for Windows
REM ============================================================
REM  Requirements:
REM    - Python 3.9 or newer installed and on PATH
REM    - Run this script from the repo root
REM
REM  Output: dist\FLPOrganizer.exe  (single-file, no installer needed)
REM ============================================================

setlocal

echo.
echo [1/4] Creating virtual environment...
if not exist .venv (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: Could not create venv. Is Python installed?
        exit /b 1
    )
)

echo.
echo [2/4] Installing dependencies...
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Could not install dependencies.
    exit /b 1
)

echo.
echo [3/4] Building executable...
REM Remove old builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM If no icon is present, skip the icon parameter
if exist docs\icon.ico (
    pyinstaller FLPOrganizer.spec --noconfirm
) else (
    pyinstaller --onefile --noconsole --name FLPOrganizer ^
        --hidden-import tkinterdnd2 ^
        --paths src src\flp_gui.py
)

if errorlevel 1 (
    echo ERROR: Build failed.
    exit /b 1
)

echo.
echo [4/4] Done!
echo.
echo Executable: dist\FLPOrganizer.exe
echo.
dir dist\FLPOrganizer.exe

endlocal
