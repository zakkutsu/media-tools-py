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

REM Cek Python availability
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo ERROR: Python tidak ditemukan!
    echo.
    echo Solusi:
    echo 1. Install Python 3.8+ dari python.org
    echo 2. Pastikan Python ada di PATH
    echo 3. Restart launcher ini
    echo.
    pause
    exit /b 1
)

REM Cek dan buat virtual environment jika belum ada
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo [1/3] Membuat virtual environment...
    echo      (First-time setup: Ini normal butuh beberapa saat)
    python -m venv venv
    IF ERRORLEVEL 1 (
        echo.
        echo ERROR: Gagal membuat virtual environment!
        echo Pastikan Python 3.8+ sudah terinstall.
        pause
        exit /b 1
    )
    echo      Virtual environment berhasil dibuat! [OK]
) ELSE (
    echo [1/3] Virtual environment sudah ada. [OK]
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
echo      (Ini mungkin butuh waktu beberapa menit di first run)
python -m pip install -r requirements.txt --upgrade

REM Verifikasi spotdl terinstall
echo.
echo [CHECK] Verifikasi spotdl...
python -m pip show spotdl >nul 2>&1
IF ERRORLEVEL 1 (
    echo      spotdl belum terinstall! Mencoba install...
    python -m pip install spotdl>=4.0.0
    IF ERRORLEVEL 1 (
        echo.
        echo ========================================
        echo   ERROR: Gagal install spotdl!
        echo ========================================
        echo   Solusi:
        echo   1. Cek koneksi internet
        echo   2. Manual install: pip install spotdl
        echo   3. Restart launcher ini
        echo ========================================
        pause
        exit /b 1
    )
    echo      spotdl berhasil diinstall!
) ELSE (
    echo      spotdl sudah terinstall [OK]
)

echo.
echo ========================================
echo   Setup Complete! Starting App...
echo ========================================
echo   Jika muncul alert "spotdl belum terinstall"
echo   di GUI, klik tombol "Install spotdl Sekarang"
echo ========================================
echo.

REM Jalankan GUI
python spotify_downloader_gui_flet.py

REM Jika error, tahan window
IF ERRORLEVEL 1 (
    echo.
    echo ========================================
    echo   ERROR: Aplikasi berhenti dengan error!
    echo ========================================
    echo   Troubleshooting:
    echo   1. Cek apakah FFmpeg sudah terinstall
    echo   2. Cek koneksi internet
    echo   3. Lihat README.md untuk solusi lengkap
    echo ========================================
    pause
)

pause
