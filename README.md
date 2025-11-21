# Media Tools 🎬🎵# Media Tools 🎬🎵



Koleksi tools untuk pemrosesan dan analisis file media (audio, video) dengan **GUI Launcher terpadu** dan fitur-fitur modern.Koleksi tools untuk pemrosesan dan analisis file media (audio, video, gambar) dengan **GUI Launcher terpadu**.



## 📋 Tools yang Tersedia## 🚀 Quick Start (Recommended)



### 🎵 Audio Merger### ⚠️ FIRST TIME SETUP (IMPORTANT!)

Menggabungkan multiple file audio dengan efek transisi profesional.

- **Fitur**: Crossfade, Gap/Jeda, Preview, Drag & DropIf you just cloned this repository, **run setup first**:

- **Format**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA

- **Dokumentasi**: [audio-merger/README.md](audio-merger/README.md)```bash

# Navigate to folder

### 🎬 Media Codec Detectorcd media-tools

Analisis codec dan format file media secara detail.

- **Fitur**: Deteksi codec video/audio, format container, metadata# Run automatic setup

- **Format**: Semua format yang didukung FFmpegpython setup_media_tools.py

- **Dokumentasi**: [media-codec-detector/README.md](media-codec-detector/README.md)```



### 📥 YouTube Batch DownloaderOr manually:

Download multiple video YouTube individual secara batch.```bash

- **Fitur**: Multi-quality, audio-only, retry failed, progress tracking, **thumbnail & metadata embedding**# 1. Create virtual environment

- **Format Output**: MP4, WebM, MP3, M4A (dengan cover art!)python -m venv venv

- **Dokumentasi**: [yt-batch-downloader/README.md](yt-batch-downloader/README.md)

# 2. Activate it

### 🎵 YouTube Playlist Downloader.\venv\Scripts\Activate.ps1  # Windows PowerShell

Download playlist YouTube lengkap dengan auto-numbering.# OR

- **Fitur**: Full playlist, quality selection, auto-numbering, **thumbnail & metadata embedding**source venv/bin/activate     # Linux/macOS

- **Format Output**: MP4, WebM, MP3, M4A (dengan album art!)

- **Dokumentasi**: [yt-playlist-downloader/README.md](yt-playlist-downloader/README.md)# 3. Install dependencies

pip install -r requirements.txt

---```



## 🚀 Quick Start### Launch Media Tools



### ✨ Cara Termudah (Auto-Setup!)**Windows:**

```bash

**Windows:**# Double-click or run:

```bash.\launch_media_tools.bat

# Double-click file ini:```

launch_media_tools.bat

```**Linux/macOS:**

```bash

**Linux/macOS:**chmod +x launch_media_tools.sh  # First time only

```bash./launch_media_tools.sh

# Pertama kali, buat executable:```

chmod +x launch_media_tools.sh

**Or run Python directly:**

# Kemudian jalankan:```bash

./launch_media_tools.shpython media_tools_launcher.py

``````



**Apa yang Terjadi Otomatis?**## Tools yang Tersedia

1. ✅ Membuat virtual environment

2. ✅ Install semua dependencies### 🎵 Audio Merger

3. ✅ Cek FFmpeg (optional)Program untuk menggabungkan multiple file audio menjadi satu file dengan berbagai efek transisi.

4. ✅ Launch aplikasi- **Lokasi**: `audio-merger/`

- **Fitur**: Crossfade, Gap/Jeda, GUI modern dengan Flet

**Waktu:** 2-5 menit (first run only), selanjutnya instant! ⚡- **Format**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA



---### 🎬 Media Codec Detector  

Program untuk mendeteksi format kontainer dan codec dari file media.

## 📦 Installation- **Lokasi**: `media-codec-detector/`

- **Fitur**: Analisis codec video/audio, deteksi format gambar, GUI modern

### Requirements- **Format**: Semua format media yang didukung FFmpeg

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)

  - ⚠️ Saat install, centang "Add Python to PATH"!## Struktur Folder

- **FFmpeg** (Required) - Untuk audio/video processing

```

### Install FFmpegmedia-tools/

├── media_tools_launcher.py      # 🏠 GUI Launcher Utama (RECOMMENDED)

**Windows:**├── requirements.txt             # Dependencies gabungan

```bash├── audio-merger/

# Via Chocolatey│   ├── audio_merger.py          # CLI version

choco install ffmpeg│   ├── audio_merger_gui.py      # GUI version (Flet)

│   ├── requirements.txt

# Via Winget│   └── README.md

winget install ffmpeg├── media-codec-detector/

```│   ├── media_codec_detector.py  # CLI version

│   ├── media_codec_detector_gui.py  # GUI version (Flet)

**macOS:**│   ├── requirements.txt

```bash│   └── README.md

brew install ffmpeg└── README.md                    # File ini

``````



**Linux:**## Instalasi

```bash

# Ubuntu/Debian### Setup Virtual Environment (Recommended)

sudo apt install ffmpeg```bash

# Navigasi ke folder media-tools

# Fedora/CentOScd c:\project\tools-py\media-tools

sudo dnf install ffmpeg

```# Buat virtual environment

python -m venv venv

### Manual Setup (Advanced)

# Aktifkan virtual environment

Jika auto-setup tidak bekerja, setup manual:# Windows (PowerShell)

.\venv\Scripts\Activate.ps1

```bash

# 1. Clone atau download repository# Windows (Command Prompt)

cd media-tools.\venv\Scripts\activate.bat



# 2. Buat virtual environment# Windows (Git Bash)

python -m venv venvsource venv/Scripts/activate



# 3. Aktifkan virtual environment# Linux/macOS

# Windows PowerShell:source venv/bin/activate

.\venv\Scripts\Activate.ps1```

# Windows CMD:

.\venv\Scripts\activate.bat### Install Dependencies

# Linux/macOS:```bash

source venv/bin/activate# Install semua dependencies sekaligus dari root folder

pip install -r requirements.txt

# 4. Install dependencies

pip install -r requirements.txt# Atau install individual (tidak recommended)

cd audio-merger && pip install -r requirements.txt

# 5. Jalankan launchercd ../media-codec-detector && pip install -r requirements.txt

python media_tools_launcher.py```

```

## Kebutuhan Sistem

---

### FFmpeg (Wajib untuk semua tools)

## 🎯 Cara Penggunaan**Windows:**

```bash

### 1. GUI Launcher (Recommended)choco install ffmpeg

```

**Jalankan launcher utama:**

```bash**macOS:**

# Dari folder media-tools```bash

python media_tools_launcher.pybrew install ffmpeg

``````



**Fitur Launcher:****Linux:**

- 🏠 **Dashboard**: Pilih tool yang ingin digunakan```bash

- 🎯 **Tool Cards**: Info lengkap setiap toolsudo apt install ffmpeg

- 🔙 **Navigation**: Back to home dari setiap tool```

- 📖 **Help**: Dokumentasi terintegrasi

- 🎨 **Modern UI**: Interface yang clean dan user-friendly## Cara Penggunaan



### 2. Direct CLI Launch### 🏠 Launcher GUI (All-in-One - RECOMMENDED)

```bash

**Langsung ke tool tertentu:**# Dari folder media-tools (setelah setup venv dan install requirements)

```bashpython media_tools_launcher.py

# Audio Merger```

python media_tools_launcher.py --audio-merger

**Fitur Launcher:**

# Media Codec Detector- 🎯 **Home Dashboard**: Pilih tool yang ingin digunakan

python media_tools_launcher.py --media-detector- 🔄 **Seamless Navigation**: Back to home dari setiap tool

- 📖 **Integrated Documentation**: Dokumentasi dan system requirements

# YouTube Batch Downloader- 🎨 **Unified Interface**: Konsistensi UI/UX antar tools

python media_tools_launcher.py --batch-downloader-flet

### 🛠️ Individual Tools

# YouTube Playlist Downloader

python media_tools_launcher.py --playlist-downloader-flet#### Audio Merger

``````bash

cd audio-merger

### 3. Individual Tool Launch

# GUI Version

**Jalankan tool secara standalone:**python audio_merger_gui.py

```bash

# Audio Merger# CLI Version  

cd audio-merger && python audio_merger_gui.pypython audio_merger.py



# Media Codec Detector# Via Launcher (direct)

cd media-codec-detector && python media_codec_detector_gui.pycd .. && python media_tools_launcher.py --audio-merger

```

# YouTube Batch Downloader

cd yt-batch-downloader && python batch_downloader_gui_flet.py#### Media Codec Detector

```bash

# YouTube Playlist Downloadercd media-codec-detector

cd yt-playlist-downloader && python playlist_downloader_gui_flet.py

```# GUI Version

python media_codec_detector_gui.py

---

# CLI Version

## 🌟 Fitur Unggulanpython media_codec_detector.py



### 🎨 Modern GUI# Via Launcher (direct)

- **Flet Framework**: Modern, responsive, cross-platformcd .. && python media_tools_launcher.py --media-detector

- **Drag & Drop**: Upload file dengan mudah```

- **Real-time Progress**: Monitor progress download/processing

- **Dark/Light Mode**: Sesuaikan dengan preferensi### 📋 Command Line Options

- **Intuitive Design**: User-friendly untuk semua level

```bash

### 🚀 YouTube Tools Features# Launcher options

python media_tools_launcher.py                # Launch GUI home

#### ✨ NEW! Thumbnail & Metadata Embeddingpython media_tools_launcher.py --audio-merger # Direct to Audio Merger

Semua download YouTube kini otomatis menyertakan:python media_tools_launcher.py --media-detector # Direct to Media Detector

- **🖼️ Thumbnail sebagai Cover Art**: Album art untuk MP3/M4Apython media_tools_launcher.py --cli          # Show CLI options

- **📝 Metadata Lengkap**: Title, artist (channel), date, descriptionpython media_tools_launcher.py --help         # Show help

- **🎵 Music Library Ready**: Langsung indah di music player!```



**Contoh hasil MP3:**## Fitur Unggulan

```

My Favorite Song.mp3### � Unified Launcher

├─ 🎨 YouTube thumbnail sebagai album art- **All-in-One Interface**: Akses semua tools dari satu tempat

├─ 📝 Title: "My Favorite Song"- **Seamless Navigation**: Back to home button di setiap tool

├─ 👤 Artist: "Channel Name"- **Integrated Help**: Documentation dan system requirements

└─ 📅 Date: "2025-11-21"- **Modern Design**: Dashboard yang clean dan intuitive

```

### �🎨 GUI Modern

#### Batch Downloader Features- Interface grafis dengan Flet (cross-platform)

- 📥 Download banyak video individual- Drag & drop functionality  

- ⚡ Enhanced progress (speed, ETA, statistics)- Real-time progress monitoring

- 🔄 Retry failed downloads- Responsive design

- 🗑️ Clear failed URLs- Consistent UI/UX across tools

- 🔇 Silent mode (no JS warnings)

- 📊 Real-time monitoring### 🔧 Powerful Processing

- Multi-format support

#### Playlist Downloader Features- Advanced audio effects (crossfade, gap)

- 🎵 Download full playlist otomatis- Comprehensive codec detection

- 🔢 Auto-numbering files- Batch processing capabilities

- 📁 Custom naming templates- Thread-safe background operations

- 📊 Progress tracking per video

- ⚡ Resume capability### 💻 Flexible Usage

- **GUI Launcher**: Home dashboard untuk non-teknis users

### 🎵 Audio Merger Features- **Individual GUIs**: Standalone tool interfaces

- 🎼 **Crossfade Transitions**: Smooth blending antar lagu- **CLI Support**: Terminal interface untuk automation

- ⏱️ **Gap Control**: Jeda antar audio (0-10 detik)- **Direct Launch**: Command line shortcuts ke tools

- 🎚️ **Volume Control**: Individual & master volume- **Cross-platform**: Windows, macOS, Linux

- 🔊 **Preview**: Dengar hasil sebelum save

- 📁 **Batch Processing**: Gabung banyak file sekaligus## Screenshot Launcher



### 🎬 Media Codec Detector Features![Media Tools Launcher](https://via.placeholder.com/800x600/7B1FA2/ffffff?text=Media+Tools+Launcher)

- 📊 **Codec Analysis**: Video & audio codec detection

- 📦 **Container Info**: Format, bitrate, resolution**Launcher Features:**

- 🎨 **Metadata Display**: Complete file metadata- 🏠 **Home Dashboard**: Tool selection dengan card interface

- 📸 **Image Support**: JPEG, PNG, WebP, GIF analysis- 🎯 **Tool Cards**: Informasi lengkap dan feature list

- 💾 **Export Results**: Save analysis to file- 📖 **Documentation**: Built-in help dan system requirements

- 🚀 **Quick Launch**: One-click access ke tools

---- 🔙 **Back Navigation**: Seamless return to home dari tools



## 📁 Struktur Project## License



```Free to use and modify.

media-tools/

├── 🏠 media_tools_launcher.py      # Main GUI Launcher## Author

├── 📄 README.md                     # Dokumentasi utama (file ini)

├── 📋 requirements.txt              # Dependencies gabunganKoleksi tools untuk mempermudah pemrosesan file media.
├── 🚀 launch_media_tools.bat       # Windows auto-launcher
├── 🚀 launch_media_tools.sh        # Linux/Mac auto-launcher
├── ⚙️ setup_media_tools.py         # Setup script
│
├── 🎵 audio-merger/
│   ├── audio_merger_gui.py         # GUI (Flet)
│   ├── audio_merger.py             # CLI version
│   ├── README.md                   # Dokumentasi lengkap
│   └── requirements.txt
│
├── 🎬 media-codec-detector/
│   ├── media_codec_detector_gui.py # GUI (Flet)
│   ├── media_codec_detector.py     # CLI version
│   ├── README.md                   # Dokumentasi lengkap
│   └── requirements.txt
│
├── 📥 yt-batch-downloader/
│   ├── batch_downloader_gui_flet.py  # Modern GUI
│   ├── batch_downloader.py           # Backend
│   ├── README.md                     # Dokumentasi lengkap
│   └── requirements.txt
│
└── 🎵 yt-playlist-downloader/
    ├── playlist_downloader_gui_flet.py  # Modern GUI
    ├── playlist_downloader.py           # Backend
    ├── README.md                        # Dokumentasi lengkap
    └── requirements.txt
```

---

## 🔧 Troubleshooting

### Issue: "Python not found"
**Solution:**
1. Install Python dari https://www.python.org/downloads/
2. **PENTING**: Centang "Add Python to PATH" saat install
3. Restart terminal/computer
4. Coba lagi

### Issue: "yt-dlp not found"
**Solution:**
1. Buka tool (Batch/Playlist Downloader)
2. Klik tombol "Install/Update yt-dlp" di bagian atas
3. Tunggu proses selesai
4. Coba download lagi

### Issue: "FFmpeg not found"
**Solution:**
Install FFmpeg sesuai OS Anda (lihat bagian Installation di atas).

**Note**: FFmpeg wajib untuk:
- Audio Merger (semua fitur)
- Media Codec Detector (semua fitur)
- YouTube downloaders (thumbnail embedding)

### Issue: "Failed to create virtual environment"
**Solution:**
```bash
# Hapus venv folder yang corrupt
# Windows:
rmdir /s /q venv
# Linux/macOS:
rm -rf venv

# Jalankan setup lagi
python setup_media_tools.py
```

### Issue: Import errors atau module not found
**Solution:**
```bash
# Aktifkan venv
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 💡 Tips & Best Practices

### Audio Merger
- ✅ Gunakan format yang sama untuk hasil terbaik (semua MP3 atau semua WAV)
- ✅ Preview dulu sebelum save final
- ✅ Crossfade 2-3 detik ideal untuk musik
- ✅ Export ke WAV untuk kualitas maksimal, MP3 untuk file size kecil

### YouTube Downloads
- ✅ **Gunakan audio-only untuk musik** - Lebih kecil, dapat metadata & cover art
- ✅ **Batch downloader untuk video individual** - Lebih fleksibel
- ✅ **Playlist downloader untuk album/series** - Auto-numbered, organized
- ✅ **Enable retry** jika koneksi tidak stabil
- ✅ **Check thumbnail** di music player setelah download

### Media Codec Detector
- ✅ Berguna untuk cek kompatibilitas sebelum editing
- ✅ Identifikasi codec yang tidak supported
- ✅ Cek bitrate untuk optimize file size

---

## 🎉 Changelog

### Version 2.1 (November 21, 2025)
- ✨ **NEW**: Thumbnail & metadata embedding untuk YouTube downloads
- 🎨 MP3/M4A dengan album art dari YouTube thumbnail
- 📝 Metadata lengkap (title, artist, date) otomatis
- 📱 Perfect integration dengan music players

### Version 2.0 (November 21, 2025)
- 🔇 Silent mode - no JavaScript warnings
- ⚡ Enhanced progress display dengan speed & ETA
- 🔄 Retry failed downloads (batch downloader)
- 🗑️ Clear failed URLs (batch downloader)
- 📊 Real-time statistics

### Version 1.0
- 🏠 Unified launcher dengan dashboard
- 🎵 Audio Merger dengan crossfade & effects
- 🎬 Media Codec Detector
- 📥 YouTube Batch Downloader
- 🎵 YouTube Playlist Downloader
- 🎨 Modern Flet-based GUI

---

## 📚 Documentation

**Main Documentation:**
- This README - Overview & Quick Start
- Each tool folder has detailed README.md

**Tool-Specific Docs:**
- [Audio Merger README](audio-merger/README.md) - Complete audio merging guide
- [Media Codec Detector README](media-codec-detector/README.md) - Codec detection guide
- [Batch Downloader README](yt-batch-downloader/README.md) - Batch download guide
- [Playlist Downloader README](yt-playlist-downloader/README.md) - Playlist download guide

---

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

---

## 📄 License

Free to use and modify.

---

## 👤 Author

**Media Tools Collection**
- Repository: https://github.com/zakkutsu/tools-py
- Created: 2025

---

## 🆘 Support

Jika menemui masalah:
1. Baca dokumentasi tool-specific di folder masing-masing
2. Check Troubleshooting section di atas
3. Pastikan Python & FFmpeg terinstall dengan benar
4. Coba jalankan `python media_tools_launcher.py --help` untuk CLI options

**Happy media processing! 🎉**
