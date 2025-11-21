#!/bin/bash
# ============================================
# Media Tools Launcher - Fully Automated
# Double-click to auto-setup and launch!
# ============================================

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "========================================"
    echo "Python Not Found!"
    echo "========================================"
    echo ""
    echo "Python 3.8+ is required to run Media Tools."
    echo ""
    echo "Installation:"
    echo "  macOS:   brew install python3"
    echo "  Ubuntu:  sudo apt install python3 python3-pip python3-venv"
    echo "  Fedora:  sudo dnf install python3 python3-pip"
    echo ""
    echo "========================================"
    read -p "Press Enter to continue..."
    exit 1
fi

# Check if virtual environment exists
if [ ! -f "venv/bin/python" ]; then
    echo ""
    echo "========================================"
    echo "First Time Setup - Auto Installation"
    echo "========================================"
    echo ""
    echo "This is your first time running Media Tools."
    echo "Setting up environment automatically..."
    echo ""
    echo "Please wait, this may take a few minutes..."
    echo ""
    
    # Create virtual environment
    echo "[1/3] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo ""
        echo "${RED}ERROR: Failed to create virtual environment!${NC}"
        echo ""
        read -p "Press Enter to continue..."
        exit 1
    fi
    echo "      ${GREEN}Done!${NC}"
    echo ""
    
    # Install dependencies
    echo "[2/3] Installing dependencies..."
    echo "      This may take 2-5 minutes depending on your internet speed..."
    "venv/bin/python" -m pip install --upgrade pip > /dev/null 2>&1
    "venv/bin/python" -m pip install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo ""
        echo "${RED}ERROR: Failed to install dependencies!${NC}"
        echo ""
        read -p "Press Enter to continue..."
        exit 1
    fi
    echo "      ${GREEN}Done!${NC}"
    echo ""
    
    # Check FFmpeg
    echo "[3/3] Checking FFmpeg..."
    if ! command -v ffmpeg &> /dev/null; then
        echo "      ${YELLOW}WARNING: FFmpeg not found!${NC}"
        echo "      Some features may not work without FFmpeg."
        echo ""
        echo "      To install FFmpeg:"
        echo "      - macOS:  brew install ffmpeg"
        echo "      - Ubuntu: sudo apt install ffmpeg"
        echo "      - Fedora: sudo dnf install ffmpeg"
        echo ""
    else
        echo "      ${GREEN}FFmpeg is available!${NC}"
    fi
    echo ""
    
    echo "========================================"
    echo "Setup Complete!"
    echo "========================================"
    echo ""
    echo "Starting Media Tools Launcher..."
    echo ""
    sleep 2
fi

# Launch the media tools launcher using the virtual environment
"venv/bin/python" media_tools_launcher.py "$@"

# Check exit code
if [ $? -ne 0 ]; then
    echo ""
    echo "========================================"
    echo "Error occurred while running launcher"
    echo "========================================"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Make sure all dependencies are installed"
    echo "  2. Try: rm -rf venv && ./launch_media_tools.sh"
    echo "  3. Check that Python 3.8+ is installed"
    echo ""
    read -p "Press Enter to continue..."
fi
