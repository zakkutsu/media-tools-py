@echo off
REM ========================================
REM  Spotify Downloader Pro - Launcher
REM  Setup otomatis & jalankan GUI
REM ========================================

cd /d %~dp0

echo ========================================
echo   Spotify Downloader Pro - Launcher
echo ========================================
echo.

REM Cek dan buat virtual environment jika belum ada
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [1/3] Membuat virtual environment...
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo ERROR: Gagal membuat virtual environment!
        pause
        exit /b 1
    )
    echo      Virtual environment berhasil dibuat!
) ELSE (
    echo [1/3] Virtual environment sudah ada.
)

REM Aktifkan virtual environment
echo [2/3] Mengaktifkan virtual environment...
IF EXIST "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) ELSE (
    echo ERROR: Virtual environment tidak ditemukan!
    pause
    exit /b 1
)

REM Install/update requirements
echo [3/3] Menginstall/update dependencies...
python -m pip install -r requirements.txt --upgrade --quiet

echo.
echo ========================================
echo   Memulai Spotify Downloader Pro...
echo ========================================
echo.

REM Jalankan GUI
python spotify_downloader_gui_flet.py

pause
