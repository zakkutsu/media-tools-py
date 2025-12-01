@echo off
REM Media Tools Zakkutsu Launcher
REM Quick launcher untuk Windows

echo ========================================
echo   Media Tools Zakkutsu Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo [OK] Python found
echo.

REM Check if requirements are installed
python -c "import flet" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Dependencies not installed
    echo.
    echo Installing dependencies...
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [OK] Dependencies installed
    echo.
)

REM Launch the launcher
echo [INFO] Launching Media Tools Launcher...
echo.
python media_tools_launcher.py

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to launch
    pause
)
