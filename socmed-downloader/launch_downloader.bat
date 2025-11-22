@echo off
title SocMed Downloader GUI
color 0A

echo ========================================
echo    SOCMED DOWNLOADER GUI
echo    Starting Application...
echo ========================================
echo.

cd /d "%~dp0"
python socmed_downloader_gui.py

pause
