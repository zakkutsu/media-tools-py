# Media Tools 🎬🎵

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

Koleksi tools untuk pemrosesan dan analisis file media (audio, video, gambar) dengan **GUI Launcher terpadu**.

### 📋 Tools yang Tersedia

1. **🎵 Audio Merger** - Menggabungkan multiple file audio dengan efek transisi
2. **🎬 Media Codec Detector** - Analisis codec dan format file media
3. **📥 YouTube Batch Downloader** - Download multiple video YouTube individual
4. **🎵 YouTube Playlist Downloader** - Download playlist YouTube lengkap
5. **📥 SocMed Downloader** - Download video/audio dari YouTube, TikTok, Instagram, Facebook, Twitter/X (dengan batch download TXT/CSV/JSON)
6. **🔁 Media Looper** - Loop video/audio tanpa re-encoding (stream copy untuk kecepatan maksimal)

### 🚀 Quick Start (Recommended)

#### 💿 DOWNLOAD EXECUTABLE (No Python Required!)

**Download versi siap pakai tanpa perlu install Python:**

📥 **[Download dari GitHub Releases](https://github.com/zakkutsu/media-tools-py/releases/latest)**

- ✅ Single file executable (.exe)
- ✅ Tidak perlu install Python
- ✅ Tidak perlu install dependencies
- ✅ Double-click dan langsung jalan!

**Catatan:** Executable sudah include semua dependencies Python, tapi **FFmpeg masih harus diinstall secara terpisah** (lihat [System Requirements](#system-requirements)).

---

#### ⚡ ALTERNATIVE - One-Click Auto Setup (For Developers)

**Untuk pengguna Windows**, cukup double-click file ini:
```
launch_media_tools.bat
```

Launcher akan **otomatis** melakukan:
- ✅ Membuat virtual environment
- ✅ Install semua dependencies
- ✅ **Download FFmpeg portable (jika belum ada)** 🆕
- ✅ **Auto-configure FFmpeg untuk semua tools** 🆕
- ✅ Langsung menjalankan aplikasi

**Tampilan terminal saat first-time setup:**
```
========================================
First Time Setup - Auto Installation
========================================

This is your first time running Media Tools.
Setting up environment automatically...

Please wait, this may take a few minutes...

[1/3] Creating virtual environment...
      Done!

[2/3] Installing dependencies...
      This may take 2-5 minutes depending on your internet speed...
      [Installing packages...]
      Done!

[3/3] Checking FFmpeg...
      FFmpeg not found. Downloading portable version...
      Downloading FFmpeg...
      Extracting FFmpeg...
      FFmpeg ready!

========================================
Setup Complete!
========================================

Starting Media Tools Launcher...
✅ FFmpeg portable configured: C:\...\ffmpeg-portable\bin
```

Dependencies yang dibutuhkan (seperti `yt-dlp`) akan **auto-install** saat pertama kali tools dibuka!

#### 🔧 Manual Setup (Alternative)

Jika ingin setup manual:

```bash
# Navigate to folder
cd media-tools

# Run automatic setup
python setup_media_tools.py
```

Atau cara manual:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
.\venv\Scripts\activate.bat   # Windows CMD
# OR
source venv/bin/activate      # Linux/macOS

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Install FFmpeg (required!)
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

#### 🎯 Launch Tools

**Option 1: GUI Launcher (Recommended)**
```bash
python media_tools_launcher.py
```

**Option 2: Launch Scripts**
```bash
# Windows
launch_media_tools.bat

# Linux/macOS
chmod +x launch_media_tools.sh
./launch_media_tools.sh
```

**Option 3: Individual Tools**
```bash
# Audio Merger
cd audio-merger
python audio_merger_gui.py

# Media Codec Detector
cd media-codec-detector
python media_codec_detector_gui.py

# YouTube Batch Downloader
cd yt-batch-downloader
python batch_downloader_gui_flet.py

# YouTube Playlist Downloader
cd yt-playlist-downloader
python playlist_downloader_gui_flet.py
```

### 📦 Dependencies

- Python 3.8+
- FFmpeg (system requirement)
- yt-dlp (auto-install)
- Flet (GUI framework)
- pydub, Pillow, ffmpeg-python

### 🌟 Fitur Unggulan

- ✅ **Unified Launcher** - Akses semua tools dari satu interface
- ✅ **Modern GUI** - Interface dengan Flet yang responsif
- ✅ **Auto Setup** - Instalasi dependencies otomatis
- ✅ **Cross-Platform** - Windows, macOS, Linux
- ✅ **Thumbnail & Metadata** - Auto embed untuk media files

### 📚 Dokumentasi Lengkap

- [Audio Merger](audio-merger/README.md)
- [Media Codec Detector](media-codec-detector/README.md)
- [YouTube Batch Downloader](yt-batch-downloader/README.md)
- [YouTube Playlist Downloader](yt-playlist-downloader/README.md)
- [SocMed Downloader](socmed-downloader/README.md)
- [Media Looper](media-looper/README.md) ⭐ **NEW!**

### 🔧 Troubleshooting

**Issue: "Couldn't find ffmpeg or avconv" (RuntimeWarning)**

Ini adalah **warning normal** dan tidak akan muncul lagi setelah FFmpeg terkonfigurasi. Solusi:

```bash
# Option 1: Gunakan launch_media_tools.bat (RECOMMENDED)
# - Otomatis download FFmpeg portable (~100-150 MB)
# - FFmpeg tersimpan di folder ffmpeg-portable/
# - Tidak perlu install ke system

# Option 2: Install FFmpeg ke system
# Windows
choco install ffmpeg
# atau
winget install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

**Catatan:** FFmpeg portable akan **auto-configured** untuk semua tools saat launcher pertama kali dijalankan!

---

**Issue: "FFmpeg not found"**
```bash
# Jalankan launcher batch untuk auto-setup
launch_media_tools.bat

# Atau install manual (lihat di atas)
```

**Issue: "No module named 'flet'"**
```bash
pip install -r requirements.txt
```

---

<a name="english"></a>
## 🇺🇸 English

A collection of tools for media file processing and analysis (audio, video, images) with **unified GUI Launcher**.

### 📋 Available Tools

1. **🎵 Audio Merger** - Merge multiple audio files with transition effects
2. **🎬 Media Codec Detector** - Analyze codec and media file formats
3. **📥 YouTube Batch Downloader** - Download multiple individual YouTube videos
4. **🎵 YouTube Playlist Downloader** - Download complete YouTube playlists
5. **📥 SocMed Downloader** - Download video/audio from YouTube, TikTok, Instagram, Facebook, Twitter/X (with batch download TXT/CSV/JSON)
6. **🔁 Media Looper** - Loop video/audio without re-encoding (stream copy for maximum speed)

### 🚀 Quick Start (Recommended)

#### 💿 DOWNLOAD EXECUTABLE (No Python Required!)

**Download ready-to-use version without Python installation:**

📥 **[Download from GitHub Releases](https://github.com/zakkutsu/media-tools-py/releases/latest)**

- ✅ Single file executable (.exe)
- ✅ No Python installation needed
- ✅ No dependency installation needed
- ✅ Double-click and run!

**Note:** The executable includes all Python dependencies, but **FFmpeg must still be installed separately** (see [System Requirements](#system-requirements)).

---

#### ⚡ ALTERNATIVE - One-Click Auto Setup (For Developers)

**For Windows users**, just double-click this file:
```
launch_media_tools.bat
```

The launcher will **automatically**:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Setup FFmpeg
- ✅ Launch the application

**Terminal output during first-time setup:**
```
========================================
First Time Setup - Auto Installation
========================================

This is your first time running Media Tools.
Setting up environment automatically...

Please wait, this may take a few minutes...

[1/3] Creating virtual environment...
      Done!

[2/3] Installing dependencies...
      This may take 2-5 minutes depending on your internet speed...
      [Installing packages...]
      Done!

[3/3] Checking FFmpeg...
      FFmpeg is available!

========================================
Setup Complete!
========================================

Starting Media Tools Launcher...
```

Required dependencies (like `yt-dlp`) will **auto-install** when you first open each tool!

#### 🔧 Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Navigate to folder
cd media-tools

# Run automatic setup
python setup_media_tools.py
```

Or manually:

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# OR
.\venv\Scripts\activate.bat   # Windows CMD
# OR
source venv/bin/activate      # Linux/macOS

# 3. Install all dependencies
pip install -r requirements.txt

# 4. Install FFmpeg (required!)
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

#### 🎯 Launch Tools

**Option 1: GUI Launcher (Recommended)**
```bash
python media_tools_launcher.py
```

**Option 2: Launch Scripts**
```bash
# Windows
launch_media_tools.bat

# Linux/macOS
chmod +x launch_media_tools.sh
./launch_media_tools.sh
```

**Option 3: Individual Tools**
```bash
# Audio Merger
cd audio-merger
python audio_merger_gui.py

# Media Codec Detector
cd media-codec-detector
python media_codec_detector_gui.py

# YouTube Batch Downloader
cd yt-batch-downloader
python batch_downloader_gui_flet.py

# YouTube Playlist Downloader
cd yt-playlist-downloader
python playlist_downloader_gui_flet.py
```

### 📦 Dependencies

- Python 3.8+
- FFmpeg (system requirement)
- yt-dlp (auto-install)
- Flet (GUI framework)
- pydub, Pillow, ffmpeg-python

### 🌟 Key Features

- ✅ **Unified Launcher** - Access all tools from one interface
- ✅ **Modern GUI** - Responsive Flet-based interface
- ✅ **Auto Setup** - Automatic dependency installation
- ✅ **Cross-Platform** - Windows, macOS, Linux
- ✅ **Thumbnail & Metadata** - Auto embed for media files

### 📚 Complete Documentation

- [Audio Merger](audio-merger/README.md)
- [Media Codec Detector](media-codec-detector/README.md)
- [YouTube Batch Downloader](yt-batch-downloader/README.md)
- [YouTube Playlist Downloader](yt-playlist-downloader/README.md)
- [SocMed Downloader](socmed-downloader/README.md)
- [Media Looper](media-looper/README.md) ⭐ **NEW!**

### 🔧 Troubleshooting

**Issue: "Couldn't find ffmpeg or avconv" (RuntimeWarning)**

This is a **normal warning** and will not appear after FFmpeg is configured. Solutions:

```bash
# Option 1: Use launch_media_tools.bat (RECOMMENDED)
# - Automatically downloads FFmpeg portable (~100-150 MB)
# - FFmpeg stored in ffmpeg-portable/ folder
# - No system installation needed

# Option 2: Install FFmpeg to system
# Windows
choco install ffmpeg
# or
winget install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

**Note:** FFmpeg portable will be **auto-configured** for all tools when launcher runs for the first time!

---

**Issue: "FFmpeg not found"**
```bash
# Run batch launcher for auto-setup
launch_media_tools.bat

# Or install manually (see above)
```

**Issue: "No module named 'flet'"**
```bash
pip install -r requirements.txt
```

---

<a name="japanese"></a>
## 🇯🇵 日本語

**統合GUIランチャー**を備えた、メディアファイル処理・分析ツール集（音声、動画、画像）。

### 📋 利用可能なツール

1. **🎵 Audio Merger** - トランジション効果付きで複数の音声ファイルを結合
2. **🎬 Media Codec Detector** - コーデックとメディアファイル形式を分析
3. **📥 YouTube Batch Downloader** - 複数のYouTube動画を個別にダウンロード
4. **🎵 YouTube Playlist Downloader** - YouTubeプレイリスト全体をダウンロード
5. **📥 SocMed Downloader** - YouTube、TikTok、Instagram、Facebook、Twitter/Xから動画/音声をダウンロード（TXT/CSV/JSONバッチダウンロード対応）
6. **🔁 Media Looper** - 再エンコードなしで動画/音声をループ（最高速度のストリームコピー）

### 🚀 クイックスタート（推奨）

#### 💿 実行可能ファイルをダウンロード（Pythonは不要！）

**Pythonのインストール不要ですぐに使える版をダウンロード：**

📥 **[GitHub Releasesからダウンロード](https://github.com/zakkutsu/media-tools-py/releases/latest)**

- ✅ 単一の実行可能ファイル（.exe）
- ✅ Pythonのインストール不要
- ✅ 依存関係のインストール不要
- ✅ ダブルクリックで即起動！

**注意：** 実行可能ファイルにはすべてのPython依存関係が含まれていますが、**FFmpegは別途インストールが必要です**（[システム要件](#system-requirements)を参照）。

---

#### ⚡ 代替方法 - ワンクリック自動セットアップ（開発者向け）

**Windowsユーザーの場合**、このファイルをダブルクリックするだけ：
```
launch_media_tools.bat
```

ランチャーが**自動的に**：
- ✅ 仮想環境を作成
- ✅ すべての依存関係をインストール
- ✅ FFmpegをセットアップ
- ✅ アプリケーションを起動

**初回セットアップ時のターミナル出力：**
```
========================================
First Time Setup - Auto Installation
========================================

This is your first time running Media Tools.
Setting up environment automatically...

Please wait, this may take a few minutes...

[1/3] Creating virtual environment...
      Done!

[2/3] Installing dependencies...
      This may take 2-5 minutes depending on your internet speed...
      [Installing packages...]
      Done!

[3/3] Checking FFmpeg...
      FFmpeg is available!

========================================
Setup Complete!
========================================

Starting Media Tools Launcher...
```

必要な依存関係（`yt-dlp`など）は、各ツールを初めて開いたときに**自動インストール**されます！

#### 🔧 手動セットアップ（代替方法）

手動セットアップを希望する場合：

```bash
# フォルダに移動
cd media-tools

# 自動セットアップを実行
python setup_media_tools.py
```

または手動で：

```bash
# 1. 仮想環境を作成
python -m venv venv

# 2. 有効化
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# または
.\venv\Scripts\activate.bat   # Windows CMD
# または
source venv/bin/activate      # Linux/macOS

# 3. すべての依存関係をインストール
pip install -r requirements.txt

# 4. FFmpegをインストール（必須！）
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt install ffmpeg
```

#### 🎯 ツールの起動

**オプション1：GUIランチャー（推奨）**
```bash
python media_tools_launcher.py
```

**オプション2：起動スクリプト**
```bash
# Windows
launch_media_tools.bat

# Linux/macOS
chmod +x launch_media_tools.sh
./launch_media_tools.sh
```

**オプション3：個別ツール**
```bash
# Audio Merger
cd audio-merger
python audio_merger_gui.py

# Media Codec Detector
cd media-codec-detector
python media_codec_detector_gui.py

# YouTube Batch Downloader
cd yt-batch-downloader
python batch_downloader_gui_flet.py

# YouTube Playlist Downloader
cd yt-playlist-downloader
python playlist_downloader_gui_flet.py

# Media Looper
cd media-looper
python media_looper_gui.py
```

### 📦 依存関係

- Python 3.8+
- FFmpeg（システム要件）
- yt-dlp（自動インストール）
- Flet（GUIフレームワーク）
- pydub、Pillow、ffmpeg-python

### 🌟 主な機能

- ✅ **統合ランチャー** - 1つのインターフェースからすべてのツールにアクセス
- ✅ **モダンGUI** - レスポンシブなFletベースのインターフェース
- ✅ **自動セットアップ** - 依存関係の自動インストール
- ✅ **クロスプラットフォーム** - Windows、macOS、Linux
- ✅ **サムネイルとメタデータ** - メディアファイルへの自動埋め込み

### 📚 完全なドキュメント

- [Audio Merger](audio-merger/README.md)
- [Media Codec Detector](media-codec-detector/README.md)
- [YouTube Batch Downloader](yt-batch-downloader/README.md)
- [YouTube Playlist Downloader](yt-playlist-downloader/README.md)
- [SocMed Downloader](socmed-downloader/README.md)
- [Media Looper](media-looper/README.md) ⭐ **NEW!**

### 🔧 トラブルシューティング

**問題：「FFmpeg not found」**
```bash
# Windows
choco install ffmpeg

# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

**問題：「No module named 'flet'」**
```bash
pip install -r requirements.txt
```

---

## 📄 License

Free to use and modify.

## 🤝 Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

---

**Made with ❤️ for media enthusiasts**
