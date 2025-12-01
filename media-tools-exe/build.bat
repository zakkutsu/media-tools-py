@echo off
REM =====================================================
REM Media Tools Zakkutsu - Build Script
REM =====================================================

echo.
echo ========================================
echo   Media Tools Zakkutsu - Build
echo ========================================
echo.

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [INFO] PyInstaller not found. Installing...
    python -m pip install pyinstaller
)

echo [1/3] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo       Done!
echo.

echo [2/3] Building executable...
echo       This may take 2-3 minutes...
echo.
python -m PyInstaller MediaToolsZakkutsu.spec --clean

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo [3/3] Verifying build...
if exist "dist\MediaToolsZakkutsu.exe" (
    echo       Build successful!
    echo.
    echo ========================================
    echo   Build Complete!
    echo ========================================
    echo.
    echo Output: dist\MediaToolsZakkutsu.exe
    
    for %%F in ("dist\MediaToolsZakkutsu.exe") do (
        set size=%%~zF
    )
    set /a sizeMB=!size! / 1048576
    echo Size: ~!sizeMB! MB
    echo.
    echo Ready to use!
    echo ========================================
) else (
    echo       [ERROR] Executable not found!
)

echo.
pause
