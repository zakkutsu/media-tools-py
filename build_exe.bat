@echo off
REM =====================================================
REM Media Tools - Quick Build Script for Windows
REM =====================================================
REM This script builds the executable using PyInstaller
REM =====================================================

echo.
echo ========================================
echo   Media Tools - Build Executable
echo ========================================
echo.

REM Check if PyInstaller is installed
python -m PyInstaller --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] PyInstaller not found!
    echo.
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo [ERROR] Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo [1/3] Cleaning previous build...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
echo       Done!
echo.

echo [2/3] Building executable with PyInstaller...
echo       This may take a few minutes...
echo.
python -m PyInstaller MediaToolsZakkutsu.spec --clean

if errorlevel 1 (
    echo.
    echo [ERROR] Build failed!
    echo Please check the error messages above.
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
    
    REM Get file size
    for %%F in ("dist\MediaToolsZakkutsu.exe") do (
        set size=%%~zF
    )
    set /a sizeMB=!size! / 1048576
    echo Size: ~!sizeMB! MB
    echo.
    echo Ready for distribution!
    echo.
    echo Next steps:
    echo 1. Test the executable: dist\MediaToolsZakkutsu.exe
    echo 2. Create git tag: git tag -a v1.0.0 -m "Release v1.0.0"
    echo 3. Push tag: git push origin v1.0.0
    echo 4. Upload to GitHub Releases
    echo.
    echo See RELEASE_GUIDE.md for detailed instructions.
    echo ========================================
) else (
    echo       [ERROR] Executable not found!
    echo       Build may have failed.
)

echo.
pause
