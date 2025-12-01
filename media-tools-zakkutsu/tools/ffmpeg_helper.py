"""
FFmpeg Helper Module
Provides FFmpeg detection and user-friendly error handling
"""

import shutil
import subprocess
import os
from pathlib import Path

def find_ffmpeg():
    """
    Find FFmpeg executable in multiple locations
    Returns: (ffmpeg_path, ffprobe_path) or (None, None)
    """
    # Check local bin folder first (for bundled distribution)
    local_bin = Path(__file__).parent / "bin"
    local_ffmpeg = local_bin / "ffmpeg.exe" if os.name == 'nt' else local_bin / "ffmpeg"
    local_ffprobe = local_bin / "ffprobe.exe" if os.name == 'nt' else local_bin / "ffprobe"
    
    if local_ffmpeg.exists() and local_ffprobe.exists():
        return str(local_ffmpeg), str(local_ffprobe)
    
    # Check system PATH
    ffmpeg_path = shutil.which('ffmpeg')
    ffprobe_path = shutil.which('ffprobe')
    
    if ffmpeg_path and ffprobe_path:
        return ffmpeg_path, ffprobe_path
    
    return None, None

def check_ffmpeg():
    """
    Check if FFmpeg is available
    Returns: (is_available, ffmpeg_path, ffprobe_path, error_message)
    """
    ffmpeg_path, ffprobe_path = find_ffmpeg()
    
    if not ffmpeg_path or not ffprobe_path:
        error_msg = (
            "FFmpeg tidak ditemukan!\n\n"
            "Tools ini memerlukan FFmpeg untuk berfungsi.\n\n"
            "Cara Install:\n"
            "1. Via winget (recommended):\n"
            "   winget install ffmpeg\n\n"
            "2. Manual download:\n"
            "   https://ffmpeg.org/download.html\n\n"
            "3. Via Chocolatey:\n"
            "   choco install ffmpeg\n\n"
            "Setelah install, restart aplikasi ini."
        )
        return False, None, None, error_msg
    
    # Verify FFmpeg is working
    try:
        subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            timeout=5,
            check=True
        )
        return True, ffmpeg_path, ffprobe_path, None
    except Exception as e:
        error_msg = f"FFmpeg ditemukan tapi tidak bisa dijalankan:\n{str(e)}"
        return False, ffmpeg_path, ffprobe_path, error_msg

def get_ffmpeg_version():
    """Get FFmpeg version string"""
    ffmpeg_path, _ = find_ffmpeg()
    if not ffmpeg_path:
        return None
    
    try:
        result = subprocess.run(
            [ffmpeg_path, '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        # Extract version from first line
        first_line = result.stdout.split('\n')[0]
        return first_line
    except:
        return None

def setup_ffmpeg_environment():
    """
    Setup FFmpeg environment variables for tools like pydub
    Returns: (ffmpeg_path, ffprobe_path) or (None, None)
    """
    ffmpeg_path, ffprobe_path = find_ffmpeg()
    
    if ffmpeg_path and ffprobe_path:
        # Add FFmpeg directory to PATH if not already there
        ffmpeg_dir = str(Path(ffmpeg_path).parent)
        current_path = os.environ.get('PATH', '')
        
        if ffmpeg_dir not in current_path:
            os.environ['PATH'] = ffmpeg_dir + os.pathsep + current_path
        
        # Set explicit paths for libraries that need them
        os.environ['FFMPEG_BINARY'] = ffmpeg_path
        os.environ['FFPROBE_BINARY'] = ffprobe_path
    
    return ffmpeg_path, ffprobe_path

# Auto-setup on import
FFMPEG_PATH, FFPROBE_PATH = setup_ffmpeg_environment()
FFMPEG_AVAILABLE, _, _, FFMPEG_ERROR = check_ffmpeg()
