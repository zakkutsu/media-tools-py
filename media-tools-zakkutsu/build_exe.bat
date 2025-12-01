@echo off
echo ================================================
echo   MEDIA TOOLS ZAKKUTSU - EXE BUILDER
echo   All-in-One Standalone Edition
echo ================================================
echo.

echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo Building executable...
echo.

python build_exe.py

echo.
pause
exit /b 0
