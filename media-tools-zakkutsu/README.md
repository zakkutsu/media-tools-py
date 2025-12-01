# 🎬 Media Tools Zakkutsu Collection

Koleksi tools media processing yang powerful dan mudah digunakan.

## 📦 Tools Included

### 1. 🎵 YT Playlist Downloader
Download playlist YouTube lengkap dengan mudah.
- **Features:**
  - Download video (best quality, 720p, 480p)
  - Download audio only (MP3)
  - Auto file numbering
  - Progress tracking
  - GUI modern dengan Flet

### 2. 🔁 Media Looper
Loop file media dengan instant processing (stream copy).
- **Features:**
  - Single Loop (A-A-A...)
  - Alternating Loop (A-B-A-B...)
  - Optional delay/silence insertion
  - Video & audio support
  - Zero quality loss (stream copy)
  - GUI & CLI versions

### 3. 🎵 Audio Merger
Gabungkan multiple file audio menjadi satu.
- **Features:**
  - Merge tanpa efek (direct join)
  - Crossfade transition
  - Gap/silence between tracks
  - Support: MP3, WAV, FLAC, M4A, OGG, AAC, WMA
  - Progress tracking
  - Custom output folder

### 4. 🌐 SocMed Downloader
Download dari berbagai platform social media.
- **Features:**
  - Support: TikTok, Instagram, Facebook, Twitter/X, YouTube
  - Single & batch download mode
  - Video & audio (MP3) options
  - Quality selector
  - Browser cookies support (for private content)
  - Batch file support (TXT, CSV, JSON)
  - Multi-language (ID, EN, JP)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt
```

### 2. Install FFmpeg (REQUIRED!)

**Windows:**
```bash
winget install FFmpeg
# or
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

### 3. Launch Tools

**Option A: Quick Launch (Easiest)**
```bash
# Windows - Double click or run:
launch.bat

# macOS/Linux:
chmod +x launch.sh
./launch.sh
```

**Option B: Use Python Launcher**
```bash
# Launcher with GUI selector
python media_tools_launcher.py
```

**Option C: Run Individual Tools**

### 2. Install FFmpeg (REQUIRED!)

**Windows:**
```bash
winget install FFmpeg
# atau
choco install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify Installation:**
```bash
ffmpeg -version
ffprobe -version
```

**YT Playlist Downloader:**
```bash
# GUI (Flet)
python yt-playlist-downloader/playlist_downloader_gui_flet.py

# CLI
python yt-playlist-downloader/playlist_downloader.py
```

**Media Looper:**
```bash
# GUI (Flet)
python media-looper/media_looper_gui_flet.py

# CLI
python media-looper/media_looper_cli.py
```

**Audio Merger:**
```bash
# GUI
python audio-merger/audio_merger_gui.py

# CLI
python audio-merger/audio_merger.py
```

**SocMed Downloader:**
```bash
# GUI
python socmed-downloader/socmed_downloader_gui.py

# CLI
python socmed-downloader/socmed_downloader.py
```

## 📋 System Requirements

- **Python:** 3.8 or higher
- **FFmpeg:** Required (must be in system PATH)
- **OS:** Windows, macOS, Linux

## 🔧 Dependencies

- **flet** >= 0.25.0 - Modern GUI framework
- **yt-dlp** >= 2024.11.0 - Video/social media downloader
- **pydub** == 0.25.1 - Audio processing
- **audioop-lts** == 0.2.2 - Audio operations
- **ffmpeg-python** == 0.2.0 - FFmpeg wrapper

See `requirements.txt` for complete list.

## 📁 Structure

```
media-tools-zakkutsu/
├── requirements.txt              # All dependencies
├── README.md                     # This file (complete documentation)
├── launch.bat                    # ⚡ Windows quick launcher
├── launch.sh                     # ⚡ macOS/Linux quick launcher
├── media_tools_launcher.py       # 🚀 Main launcher GUI
├── language_config.py            # Language support
├── yt-playlist-downloader/
│   ├── playlist_downloader_gui_flet.py
│   ├── playlist_downloader.py
│   └── README.md
├── media-looper/
│   ├── media_looper_gui_flet.py
│   ├── media_looper_cli.py
│   └── README.md
├── audio-merger/
│   ├── audio_merger_gui.py
│   ├── audio_merger.py
│   └── README.md
└── socmed-downloader/
    ├── socmed_downloader_gui.py
    ├── socmed_downloader.py
    ├── batch_reader.py
    ├── language_config.py
    └── README.md
```

## 💡 Tips

### YT Playlist Downloader
- Gunakan auto numbering untuk urutan file yang rapi
- Pilih quality 480p/720p untuk hemat bandwidth
- Check info playlist sebelum download

### Media Looper
- Stream copy = instant processing, no re-encoding
- Gunakan alternating loop untuk Q&A drill atau intro-content pattern
- Add delay untuk thinking time antar tracks

### Audio Merger
- Crossfade untuk transisi halus antar lagu
- Gap untuk memberi jeda antar track
- Semua format audio otomatis di-convert saat merge

### SocMed Downloader
- Gunakan browser cookies untuk download private content
- Batch mode support TXT, CSV, JSON
- Multi-platform: TikTok, IG, FB, Twitter/X, YouTube

## 🎯 Individual Tool Usage

### YT Playlist Downloader
```bash
# GUI
python yt-playlist-downloader/playlist_downloader_gui_flet.py

# CLI
python yt-playlist-downloader/playlist_downloader.py
```

### Media Looper
```bash
# GUI
python media-looper/media_looper_gui_flet.py

# CLI
python media-looper/media_looper_cli.py
```

### Audio Merger
```bash
# GUI
python audio-merger/audio_merger_gui.py

# CLI
python audio-merger/audio_merger.py
```

### SocMed Downloader
```bash
# GUI
python socmed-downloader/socmed_downloader_gui.py

# CLI
python socmed-downloader/socmed_downloader.py
```

## ❓ Troubleshooting

### FFmpeg not found
```bash
# Check if FFmpeg is installed
ffmpeg -version

# Add to PATH if installed but not detected (Windows)
setx PATH "%PATH%;C:\path\to\ffmpeg\bin"
```

### yt-dlp errors
```bash
# Update yt-dlp to latest version
pip install --upgrade yt-dlp
```

### Python module errors
```bash
# Reinstall all dependencies
pip install -r requirements.txt --force-reinstall
```

### Launcher won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Test individual tools
python media_tools_launcher.py
```

### Tool-specific issues
- **YT Playlist**: Check internet connection and playlist URL
- **Media Looper**: Ensure FFmpeg is in PATH
- **Audio Merger**: Check if pydub is installed correctly
- **SocMed Downloader**: Some platforms may require browser cookies

## 📝 Notes

- All tools support drag-and-drop untuk file input
- GUI menggunakan Flet framework (modern & responsive)
- CLI versions available untuk automation
- Zero quality loss dengan stream copy (Media Looper)
- Progress tracking di semua tools

## 🌟 Features Highlights

✅ **Modern GUI** - Flet-based interface yang smooth  
✅ **Multi-Platform** - Windows, macOS, Linux  
✅ **Fast Processing** - Stream copy untuk instant results  
✅ **Batch Support** - Process multiple files/links  
✅ **Quality Options** - Flexible quality selection  
✅ **Progress Tracking** - Real-time progress display  
✅ **Multi-Language** - Support bahasa Indonesia, English, 日本語  

## 📄 License

Part of Media Tools Suite by Zakkutsu

---

**Last Updated:** December 2025  
**Collection:** Media Tools Zakkutsu  
**Version:** 1.0
