# 🎬 Media Tools Zakkutsu - All-in-One Standalone

**Complete media processing suite in ONE standalone file** - No separate folders needed!

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FFmpeg](https://img.shields.io/badge/FFmpeg-Required-red.svg)](https://ffmpeg.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> 💡 **Quick Start:** `python media_tools_standalone.py` or double-click `launch.bat`

---

## ⭐ Key Features

- ✅ **Single File Application** - Everything in `media_tools_standalone.py`
- ✅ **Unified Launcher** - Access all 4 tools from one interface
- ✅ **Easy Distribution** - Just share one Python file
- ✅ **Buildable to EXE** - Create Windows executable easily
- ✅ **No Folder Dependencies** - All code embedded in one file

---

## 🛠️ Tools Included

### 1. 🎵 YouTube Playlist Downloader
Download entire YouTube playlists in video or audio format.

**Features:**
- Batch download entire playlists
- Choose video quality (best, 720p, 480p)
- Extract audio in MP3 format
- Auto-numbering option
- Progress tracking

### 2. 🔁 Media Looper
Loop video/audio files instantly with FFmpeg stream copy.

**Features:**
- Loop any media file multiple times
- Use FFmpeg stream_loop for instant processing
- Support for video and audio formats
- No re-encoding needed (zero quality loss)

### 3. 🎵 Audio Merger
Merge multiple audio files with professional effects.

**Features:**
- Merge unlimited audio files
- Add crossfade effects (2s)
- Insert silence gaps (1s)
- Support multiple formats: MP3, WAV, FLAC, M4A, OGG

### 4. 🌐 SocMed Downloader
Download videos from various social media platforms.

**Features:**
- Support: YouTube, TikTok, Instagram, Facebook, Twitter/X
- Download as video or audio (MP3)
- Progress tracking

---

## 📦 Installation

### System Requirements
- **Python 3.8+** (or use standalone EXE)
- **FFmpeg** (required for most tools)

### Windows - Install FFmpeg:
```powershell
winget install FFmpeg
```

### Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### Run Python File:
```bash
python media_tools_standalone.py
```

### Or use launcher:
```bash
launch.bat          # Windows
./launch.sh         # Linux/macOS
```

### Build to EXE:
```bash
python build_exe.py
```

---

## 📂 File Structure

```
media-tools-zakkutsu/
├── media_tools_standalone.py   # 🌟 MAIN FILE (~1700 lines)
├── README.md                    # This file
├── requirements.txt             # Dependencies
├── launch.bat / launch.sh       # Quick launchers
└── build_exe.py / build_exe.bat # Build scripts
```

---

## 💡 Usage Guide

### 🎵 YT Playlist Downloader
1. Select "YT Playlist Downloader"
2. Paste playlist URL
3. Choose Video/Audio format
4. Click "Start Download"

### 🔁 Media Looper
1. Select "Media Looper"
2. Browse file
3. Enter loop count
4. Click "Process"

### 🎵 Audio Merger
1. Select "Audio Merger"
2. Browse folder with audio files
3. Choose effect (Normal/Crossfade/Gap)
4. Click "Merge Audio"

### 🌐 SocMed Downloader
1. Select "SocMed Downloader"
2. Paste URL
3. Choose Video/Audio format
4. Click "Download"

---

## 🐛 Troubleshooting

### FFmpeg Not Found
```powershell
# Windows
winget install FFmpeg

# Linux
sudo apt install ffmpeg

# macOS
brew install ffmpeg
```

### yt-dlp Issues
```bash
pip install --upgrade yt-dlp
```

### Dependencies Missing
```bash
pip install -r requirements.txt
```

### Build Errors
```bash
# Clean and rebuild
rmdir /s build dist
python build_exe.py
```

---

## 🎯 Version History

**v1.0 - All-in-One Edition**
- Consolidated all 4 tools into single file
- Unified launcher interface
- Build scripts for Windows EXE
- Complete documentation

---

## 🌟 Why All-in-One?

### Advantages:
- ✅ Easy to share (one file)
- ✅ Simple to build (no folder dependencies)
- ✅ Less confusion (everything in one place)
- ✅ Portable (works standalone)

### Trade-offs:
- ⚠️ Large file (~1700 lines)
- ⚠️ Harder to edit individual tools
- ⚠️ All dependencies loaded at once

**Perfect for distribution and end-users!**

---

## 📝 License

MIT License - Free to use, modify, and distribute.

## 👤 Author

**Zakkutsu**
- GitHub: [@zakkutsu](https://github.com/zakkutsu)
- Repository: [media-tools-py](https://github.com/zakkutsu/media-tools-py)

---

**Enjoy using Media Tools Zakkutsu! 🎉**
