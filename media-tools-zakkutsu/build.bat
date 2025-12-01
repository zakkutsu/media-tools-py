@echo off
REM Build Media Tools Zakkutsu Executable

echo Building MediaToolsZakkutsu.exe...
python -m PyInstaller MediaToolsZakkutsu.spec --clean

if exist "dist\MediaToolsZakkutsu.exe" (
    echo.
    echo Build SUCCESS!
    echo Output: dist\MediaToolsZakkutsu.exe
) else (
    echo.
    echo Build FAILED!
)
pause
