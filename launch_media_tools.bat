@echo off
REM ============================================
REM Media Tools Launcher - Fully Automated
REM Double-click to auto-setup and launch!
REM ============================================

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ========================================
    echo Python Not Found!
    echo ========================================
    echo.
    echo Python is required to run Media Tools.
    echo.
    echo Please install Python 3.8+ from:
    echo   https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    echo ========================================
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo.
    echo ========================================
    echo First Time Setup - Auto Installation
    echo ========================================
    echo.
    echo This is your first time running Media Tools.
    echo Setting up environment automatically...
    echo.
    echo Please wait, this may take a few minutes...
    echo.
    
    REM Create virtual environment
    echo [1/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to create virtual environment!
        echo.
        pause
        exit /b 1
    )
    echo       Done!
    echo.
    
    REM Install dependencies
    echo [2/3] Installing dependencies...
    echo       This may take 2-5 minutes depending on your internet speed...
    "venv\Scripts\python.exe" -m pip install --upgrade pip >nul 2>&1
    "venv\Scripts\python.exe" -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo.
        pause
        exit /b 1
    )
    echo       Done!
    echo.
    
    REM Check and download FFmpeg
    echo [3/3] Checking FFmpeg...
    
    REM Check if ffmpeg-portable exists
    if exist "ffmpeg-portable\bin\ffmpeg.exe" (
        echo       FFmpeg portable is available!
    ) else (
        REM Check system FFmpeg
        ffmpeg -version >nul 2>&1
        if errorlevel 1 (
            echo       FFmpeg not found. Downloading portable version...
            echo.
            
            REM Download FFmpeg portable
            powershell -Command "& {Write-Host '      Downloading FFmpeg...' -ForegroundColor Cyan; $url = 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip'; $output = 'ffmpeg-portable.zip'; [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri $url -OutFile $output -UserAgent 'Mozilla/5.0'; Write-Host '      Extracting FFmpeg...' -ForegroundColor Cyan; Expand-Archive -Path $output -DestinationPath 'ffmpeg-temp' -Force; $ffmpegDir = Get-ChildItem -Path 'ffmpeg-temp' -Directory | Select-Object -First 1; Move-Item -Path $ffmpegDir.FullName -Destination 'ffmpeg-portable' -Force; Remove-Item -Recurse -Force 'ffmpeg-temp', $output; Write-Host '      FFmpeg ready!' -ForegroundColor Green}"
            
            if exist "ffmpeg-portable\bin\ffmpeg.exe" (
                echo       Done!
            ) else (
                echo       WARNING: Failed to download FFmpeg!
                echo       Some features may not work without FFmpeg.
            )
        ) else (
            echo       System FFmpeg is available!
        )
    )
    echo.
    
    echo ========================================
    echo Setup Complete!
    echo ========================================
    echo.
    echo Starting Media Tools Launcher...
    echo.
    timeout /t 2 >nul
)

REM Launch the media tools launcher using the virtual environment
"venv\Scripts\python.exe" media_tools_launcher.py %*

REM Pause only if there was an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo Error occurred while running launcher
    echo ========================================
    echo.
    echo Troubleshooting:
    echo   1. Make sure all dependencies are installed
    echo   2. Try deleting 'venv' folder and run again
    echo   3. Check that Python 3.8+ is installed
    echo.
    pause
)