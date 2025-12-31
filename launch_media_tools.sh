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
    
    # Check and download FFmpeg
    echo "[3/3] Checking FFmpeg..."
    
    # Check if ffmpeg-portable exists
    if [ -f "ffmpeg-portable/bin/ffmpeg" ]; then
        echo "      ${GREEN}FFmpeg portable is available!${NC}"
    else
        # Check system FFmpeg
        if ! command -v ffmpeg &> /dev/null; then
            echo "      ${YELLOW}FFmpeg not found. Downloading portable version...${NC}"
            echo ""
            
            # Detect OS
            OS_TYPE="$(uname -s)"
            case "${OS_TYPE}" in
                Linux*)
                    echo "      Downloading FFmpeg for Linux..."
                    # Try to download FFmpeg static build for Linux
                    curl -L "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz" -o ffmpeg-portable.tar.xz 2>/dev/null
                    if [ $? -eq 0 ]; then
                        echo "      Extracting FFmpeg..."
                        tar -xf ffmpeg-portable.tar.xz
                        FFMPEG_DIR=$(find . -maxdepth 1 -type d -name "ffmpeg-*-static" | head -n 1)
                        if [ -n "$FFMPEG_DIR" ]; then
                            mkdir -p ffmpeg-portable/bin
                            mv "$FFMPEG_DIR/ffmpeg" ffmpeg-portable/bin/
                            mv "$FFMPEG_DIR/ffprobe" ffmpeg-portable/bin/
                            chmod +x ffmpeg-portable/bin/*
                            rm -rf "$FFMPEG_DIR" ffmpeg-portable.tar.xz
                            echo "      ${GREEN}FFmpeg ready!${NC}"
                        else
                            echo "      ${YELLOW}WARNING: Failed to extract FFmpeg!${NC}"
                        fi
                    else
                        echo "      ${YELLOW}WARNING: Download failed. Installing system FFmpeg...${NC}"
                        echo "      Run: sudo apt install ffmpeg  (Ubuntu/Debian)"
                        echo "      Or:  sudo dnf install ffmpeg  (Fedora/RHEL)"
                    fi
                    ;;
                Darwin*)
                    echo "      Downloading FFmpeg for macOS..."
                    # Check if Homebrew is available
                    if command -v brew &> /dev/null; then
                        echo "      Installing FFmpeg via Homebrew..."
                        brew install ffmpeg 2>/dev/null
                        if [ $? -eq 0 ]; then
                            echo "      ${GREEN}FFmpeg installed!${NC}"
                        else
                            echo "      ${YELLOW}WARNING: Failed to install FFmpeg!${NC}"
                        fi
                    else
                        echo "      ${YELLOW}WARNING: Homebrew not found!${NC}"
                        echo "      Please install Homebrew first: https://brew.sh"
                        echo "      Then run: brew install ffmpeg"
                    fi
                    ;;
                *)
                    echo "      ${YELLOW}WARNING: Unsupported OS for auto-download!${NC}"
                    echo "      Please install FFmpeg manually."
                    ;;
            esac
        else
            echo "      ${GREEN}System FFmpeg is available!${NC}"
        fi
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
