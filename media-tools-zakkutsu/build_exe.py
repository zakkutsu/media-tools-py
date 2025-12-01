#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build Executable untuk Media Tools Zakkutsu
Standalone All-in-One Edition
"""

import subprocess
import sys
import os
from pathlib import Path

# Set UTF-8 encoding for console output
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("="*60)
print("  Media Tools Zakkutsu - EXE Builder")
print("  All-in-One Standalone Edition")
print("="*60)
print()

# Check if PyInstaller is installed
try:
    import PyInstaller
    print("[OK] PyInstaller found")
except ImportError:
    print("[ERROR] PyInstaller not found")
    print("[INFO] Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'], check=True)
        print("[OK] PyInstaller installed successfully")
    except:
        print("[ERROR] Failed to install PyInstaller")
        print("Please run: pip install pyinstaller")
        sys.exit(1)

print()
print("[BUILD] Building standalone executable...")
print()

# Get current directory
current_dir = Path(__file__).parent

# Build command for standalone file
build_cmd = [
    sys.executable,
    '-m',
    'PyInstaller',
    '--name=MediaToolsZakkutsu',
    '--onefile',
    '--windowed',
    f'--add-data=language_config.py{os.pathsep}.',
    '--hidden-import=flet',
    '--hidden-import=yt_dlp',
    '--hidden-import=pydub',
    '--hidden-import=ffmpeg',
    '--hidden-import=audioop',
    '--collect-all=flet',
    '--collect-all=yt_dlp',
    '--copy-metadata=yt-dlp',
    '--noconsole',
    'media_tools_standalone.py'
]

print("Running PyInstaller...")
print("Command:", ' '.join(build_cmd))
print()

try:
    result = subprocess.run(build_cmd, cwd=current_dir, check=True)
    
    print()
    print("="*60)
    print("[SUCCESS] Build completed successfully!")
    print("="*60)
    print()
    print("[OUTPUT] Location: dist/MediaToolsZakkutsu.exe")
    print()
    print("[NOTES]")
    print("  - FFmpeg is NOT included in the EXE")
    print("  - yt-dlp IS included in the EXE")
    print("  - Users must install FFmpeg separately:")
    print("    winget install FFmpeg")
    print()
    print("[READY] Ready to distribute!")
    
except subprocess.CalledProcessError as e:
    print()
    print("="*60)
    print("[ERROR] Build failed!")
    print("="*60)
    print()
    print("Error:", e)
    print()
    print("Troubleshooting:")
    print("  1. Ensure all dependencies installed:")
    print("     pip install -r requirements.txt")
    print("  2. Delete build/ and dist/ folders and try again")
    print("  3. Run with verbose: pyinstaller --log-level=DEBUG")
    sys.exit(1)

except KeyboardInterrupt:
    print()
    print("[CANCELLED] Build cancelled by user")
    sys.exit(1)
