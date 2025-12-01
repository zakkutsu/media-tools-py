@echo off
REM =====================================================
REM Media Tools - Script Version Launcher
REM For Development & Debugging
REM =====================================================

echo.
echo ========================================
echo   Media Tools - Development Mode
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ first.
    pause
    exit /b 1
)

REM Check if requirements installed
python -c "import flet" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo [INFO] Starting Media Tools (Script Mode)...
echo.
python main.py

if errorlevel 1 (
    echo.
    echo [ERROR] Script failed to run
    pause
)
