# 📁 Media Tools - Project Structure

```
media-tools-py/
│
├── 📄 README.md                      # Main documentation (ID/EN/JP)
├── 📄 requirements.txt               # ⭐ Unified dependencies for all tools
├── 📄 .gitignore                     # Git ignore rules
│
├── 🚀 launch_media_tools.bat        # Windows launcher (auto-setup)
├── 🚀 launch_media_tools.sh         # Linux/macOS launcher
├── 🐍 media_tools_launcher.py       # Main GUI launcher (Flet)
├── 🐍 setup_media_tools.py          # Auto setup script
│
├── 🌐 language_config.py            # Multi-language support (ID/EN/JP)
├── 🌐 .language_config.json         # Language preferences
├── 🐍 add_multilang_readme.py       # README generator helper
│
├── 📁 venv/                         # Python virtual environment
│   └── ...                          # (auto-generated, in .gitignore)
│
├── 📁 audio-merger/                 # 🎵 Audio Merger Tool
│   ├── 📄 README.md                 # Tool-specific documentation
│   ├── 🐍 audio_merger.py           # CLI version
│   ├── 🐍 audio_merger_gui.py       # GUI version (Flet)
│   └── 📁 __pycache__/              # Python cache
│
├── 📁 media-codec-detector/         # 🎬 Media Codec Detector Tool
│   ├── 📄 README.md                 # Tool-specific documentation
│   ├── 🐍 media_codec_detector.py   # CLI version
│   ├── 🐍 media_codec_detector_gui.py # GUI version (Flet)
│   └── 📁 __pycache__/              # Python cache
│
├── 📁 yt-batch-downloader/          # 📥 YouTube Batch Downloader Tool
│   ├── 📄 README.md                 # Tool-specific documentation
│   ├── 🐍 batch_downloader.py       # CLI version
│   ├── 🐍 batch_downloader_gui.py   # GUI version (Tkinter - legacy)
│   ├── 🐍 batch_downloader_gui_flet.py # GUI version (Flet - modern)
│   └── 📁 __pycache__/              # Python cache
│
├── 📁 yt-playlist-downloader/       # 🎵 YouTube Playlist Downloader Tool
│   ├── 📄 README.md                 # Tool-specific documentation
│   ├── 🐍 playlist_downloader.py    # CLI version
│   ├── 🐍 playlist_downloader_gui.py # GUI version (Tkinter - legacy)
│   ├── 🐍 playlist_downloader_gui_flet.py # GUI version (Flet - modern)
│   └── 📁 __pycache__/              # Python cache
│
├── 📁 socmed-downloader/            # 📥 SocMed Downloader Tool
│   ├── 📄 README.md                 # Tool-specific documentation (ID/EN/JP)
│   ├── 🐍 socmed_downloader.py      # CLI version with batch support
│   ├── 🐍 socmed_downloader_gui.py  # GUI version (Flet) with batch support
│   ├── 🐍 batch_reader.py           # Batch file reader (TXT/CSV/JSON)
│   ├── 🐍 language_config.py        # Multi-language support
│   ├── 🚀 launch_downloader.bat     # Direct launcher for Windows
│   ├── 📁 test_samples/             # Sample batch files
│   │   ├── 📄 README_BATCH.md       # Comprehensive batch guide
│   │   ├── 📄 links.txt             # TXT format example
│   │   ├── 📄 links.csv             # CSV format example
│   │   └── 📄 links.json            # JSON format example
│   └── 📁 __pycache__/              # Python cache
│
└── 📁 media-looper/                 # 🔁 Media Looper Tool ⭐ NEW!
    ├── 📄 README.md                 # Tool-specific documentation
    ├── 🐍 media_looper_cli.py       # CLI version (unified)
    ├── 🐍 media_looper_gui_flet.py  # GUI version (Flet)
    └── 📁 __pycache__/              # Python cache
```

---

## 📦 Dependencies Management

### ✅ Unified Requirements

**All dependencies** are now in **one file**:
```
requirements.txt (root)
```

**Sub-folders NO LONGER have their own requirements.txt** because all tools are launched via the **unified launcher**.

### 📋 What's in requirements.txt?

```
flet>=0.25.0              # GUI framework (all tools)
pydub==0.25.1             # Audio processing
audioop-lts==0.2.2        # Audio operations
ffmpeg-python==0.2.0      # FFmpeg wrapper
Pillow>=10.0.0            # Image processing
filetype==1.2.0           # File type detection
yt-dlp>=2024.11.0         # Video/social media downloader
```

### 🔧 Installation

**One command installs everything:**
```bash
pip install -r requirements.txt
```

---

## 🚀 Launch Options

### 1. **GUI Launcher** (Recommended) ⭐
Launch all tools from one interface:
```bash
python media_tools_launcher.py
```
or double-click:
```
launch_media_tools.bat  (Windows)
```

### 2. **Individual Tool GUI**
Direct launch specific tool:
```bash
cd audio-merger
python audio_merger_gui.py
```

### 3. **Individual Tool CLI**
Command-line version:
```bash
cd audio-merger
python audio_merger.py
```

---

## 🎯 Tools Overview

| Tool | Purpose | Formats | Batch Support |
|------|---------|---------|---------------|
| **🎵 Audio Merger** | Merge audio files | MP3, WAV, FLAC, M4A, OGG | ❌ |
| **🎬 Media Detector** | Detect codecs | Images, Video, Audio | ❌ |
| **📥 YT Batch** | Download videos | YouTube only | ✅ (URL list) |
| **🎵 YT Playlist** | Download playlists | YouTube only | ✅ (Playlist) |
| **📥 SocMed** | Multi-platform DL | YT, TikTok, IG, FB, X | ✅ (TXT/CSV/JSON) |
| **🔁 Media Looper** | Loop media files | Audio & Video | ❌ |

---

## 🌟 Key Features

### Audio Merger
- ✅ Crossfade, Gap, Direct merge
- ✅ 7 audio formats support
- ✅ Real-time preview

### Media Codec Detector
- ✅ Detect container & codec
- ✅ Image, video, audio analysis
- ✅ Dummy file generator

### YouTube Batch Downloader
- ✅ Multiple videos at once
- ✅ Quality selection
- ✅ Auto-numbering

### YouTube Playlist Downloader
- ✅ Complete playlist download
- ✅ Flexible naming
- ✅ Per-video progress

### SocMed Downloader
- ✅ 5 platforms (YT, TikTok, IG, FB, X)
- ✅ Single & Batch mode
- ✅ TXT/CSV/JSON batch files
- ✅ Quality selector (480p-1080p)
- ✅ Video & Audio (MP3) support
- ✅ Multi-language (ID/EN/JP)
- ✅ Browser cookies for IG/FB

### Media Looper ⭐
- ✅ Stream copy (no re-encoding)
- ✅ Super fast processing
- ✅ Audio & Video support
- ✅ Zero quality loss
- ✅ Duration calculator

---

## 📚 Documentation Structure

```
📄 README.md (root)          → Main overview (this file)
├─ 📄 audio-merger/README.md
├─ 📄 media-codec-detector/README.md
├─ 📄 yt-batch-downloader/README.md
├─ 📄 yt-playlist-downloader/README.md
├─ 📄 socmed-downloader/README.md
└─ 📄 media-looper/README.md
├─ 📄 media-codec-detector/README.md
├─ 📄 yt-batch-downloader/README.md
├─ 📄 yt-playlist-downloader/README.md
└─ 📄 socmed-downloader/
   ├─ README.md              → Main SocMed documentation
   └─ test_samples/
      └─ README_BATCH.md     → Batch download guide
```

---

## 🔄 Version Control

**.gitignore** includes:
```
venv/                # Virtual environment
__pycache__/         # Python cache
*.pyc                # Compiled Python
*.mp3, *.mp4, *.wav  # Downloaded/processed media
.DS_Store            # macOS files
Thumbs.db            # Windows files
```

**Tracked files:**
- ✅ Source code (.py)
- ✅ Documentation (.md)
- ✅ Requirements (requirements.txt)
- ✅ Launchers (.bat, .sh)
- ✅ Sample files (test_samples/)

---

## 🛠️ System Requirements

### Minimum
- **Python:** 3.8+
- **RAM:** 4 GB
- **Disk:** 500 MB (+ space for media files)

### Required
- **FFmpeg:** Must be in system PATH
  ```bash
  # Windows
  choco install ffmpeg
  
  # macOS
  brew install ffmpeg
  
  # Linux
  sudo apt install ffmpeg
  ```

### Optional
- **Browser:** For Instagram/Facebook cookies (Chrome/Edge/Firefox/Brave)

---

## 📈 Development Workflow

```
1. Clone repository
   git clone https://github.com/zakkutsu/media-tools-py.git

2. Setup environment
   python setup_media_tools.py

3. Activate venv
   .\venv\Scripts\Activate.ps1

4. Install dependencies
   pip install -r requirements.txt

5. Run launcher
   python media_tools_launcher.py

6. Develop & Test
   - Make changes
   - Test individual tools
   - Test via launcher

7. Commit & Push
   git add .
   git commit -m "feat: description"
   git push origin main
```

---

## 🎨 Design Philosophy

1. **Unified Launcher** - One interface to rule them all
2. **No Duplicate Dependencies** - Single requirements.txt
3. **Modular Tools** - Each tool can run independently
4. **Modern GUI** - Flet framework for responsive UI
5. **Multi-Language** - ID/EN/JP support where applicable
6. **Auto-Setup** - Minimal manual configuration
7. **Cross-Platform** - Windows, macOS, Linux compatible

---

**Made with ❤️ for media enthusiasts**
