#!/bin/bash
# Media Tools Zakkutsu Launcher
# Quick launcher for macOS/Linux

echo "========================================"
echo "  Media Tools Zakkutsu Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python not found!"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[OK] Python found"
echo ""

# Check if requirements are installed
python3 -c "import flet" &> /dev/null
if [ $? -ne 0 ]; then
    echo "[WARNING] Dependencies not installed"
    echo ""
    echo "Installing dependencies..."
    python3 -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to install dependencies"
        exit 1
    fi
    echo "[OK] Dependencies installed"
    echo ""
fi

# Launch the launcher
echo "[INFO] Launching Media Tools Launcher..."
echo ""
python3 media_tools_launcher.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to launch"
fi
