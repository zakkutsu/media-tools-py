#!/bin/bash

echo "================================================"
echo "  MEDIA TOOLS ZAKKUTSU - ALL-IN-ONE"
echo "================================================"
echo

if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not found!"
    echo "Please install Python 3.8 or higher."
    exit 1
fi

echo "Starting Media Tools Standalone..."
echo

python3 media_tools_standalone.py

if [ $? -ne 0 ]; then
    echo
    echo "ERROR: Failed to start!"
    read -p "Press Enter to continue..."
fi

exit 0
