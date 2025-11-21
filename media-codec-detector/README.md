# Media Codec Detector 🎬

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

Program Python untuk mendeteksi format kontainer dan codec dari file media (gambar, video, audio). Tersedia dalam versi **GUI (Flet)** dan **Command Line**.

## Fitur

- **Deteksi Format Gambar**: PNG, JPEG, GIF, BMP, dan format lainnya
- **Analisis Video**: Mendeteksi codec video (H.264, H.265, VP9, dll) dan audio dalam kontainer
- **Analisis Audio**: Mendeteksi codec audio (MP3, AAC, FLAC, dll)
- **GUI Modern**: Interface grafis dengan Flet yang user-friendly
- **Mode Interaktif**: Menu pilihan untuk analisis file atau folder
- **Real-time Analysis**: Progress indicator dan hasil real-time
- **File Dummy**: Dapat membuat file test untuk demonstrasi

## Instalasi

### 1. Install FFmpeg (Wajib)

Program ini memerlukan FFmpeg untuk menganalisis file video/audio:

**Windows:**
1. Download FFmpeg dari [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (pilih essentials)
2. Ekstrak ke folder (misal: `C:\ffmpeg`)
3. Tambahkan `C:\ffmpeg\bin` ke PATH environment variable

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Setup Python Environment

#### Clone/Download Project
```bash
# Navigasi ke folder project
cd c:\project\tools-py\media-tools\media-codec-detector
```

#### Buat Virtual Environment
```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Windows (PowerShell)
.\venv\Scripts\Activate.ps1

# Windows (Command Prompt)
.\venv\Scripts\activate.bat

# Windows (Git Bash)
source venv/Scripts/activate

# Linux/macOS
source venv/bin/activate
```

#### Install Dependencies
```bash
# Install semua dependencies
pip install -r requirements.txt

# Atau install manual
pip install ffmpeg-python pillow filetype flet
```

#### Verifikasi Instalasi
```bash
# Test FFmpeg
ffmpeg -version

# Test Python dependencies
python -c "import ffmpeg, filetype, flet; from PIL import Image; print('Dependencies OK!')"
```

## Cara Penggunaan

### Mode GUI (Recommended) 🖥️

#### Langkah-langkah Lengkap:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder project:**
   ```bash
   cd c:\project\tools-py\media-tools\media-codec-detector
   ```
3. **Aktifkan virtual environment:**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   
   # Windows (Git Bash)
   source venv/Scripts/activate
   
   # Linux/macOS
   source venv/bin/activate
   ```
4. **Jalankan GUI:**
   ```bash
   python media_codec_detector_gui.py
   ```

#### Menggunakan GUI:

**Fitur GUI:**
- **File/Folder Picker**: Pilih file tunggal atau folder dengan file browser
- **Mode Selection**: Analisis file tunggal atau semua file dalam folder
- **Visual Results**: Hasil analisis ditampilkan dengan card yang informatif
- **Real-time Progress**: Progress bar dan status update
- **Dummy File Creator**: Buat file test untuk demonstrasi

**Langkah-langkah:**
1. **Pilih Mode**: File tunggal atau folder
2. **Pilih File/Folder**: Klik tombol untuk memilih media
3. **Lihat File**: Program akan menampilkan file media yang ditemukan (mode folder)
4. **Mulai Analisis**: Klik tombol "Mulai Analisis"
5. **Lihat Hasil**: Hasil akan ditampilkan secara real-time dalam cards

### Mode Terminal Interaktif

#### Langkah-langkah:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder:**
   ```bash
   cd c:\project\tools-py\media-tools\media-codec-detector
   ```
3. **Aktifkan virtual environment:**
   ```bash
   # Windows (PowerShell)
   .\venv\Scripts\Activate.ps1
   
   # Windows (Command Prompt)
   .\venv\Scripts\activate.bat
   
   # Windows (Git Bash)
   source venv/Scripts/activate
   
   # Linux/macOS
   source venv/bin/activate
   ```
4. **Jalankan mode terminal:**
   ```bash
   # Mode terminal langsung
   python media_codec_detector.py
   
   # Atau dari GUI dengan flag --cli
   python media_codec_detector_gui.py --cli
   ```

### Menu Pilihan (Mode Terminal)

1. **Analisis file tertentu**: Masukkan path file untuk dianalisis
2. **Analisis semua file dalam folder**: Analisis semua file dalam direktori
3. **Buat file dummy untuk testing**: Membuat file test untuk demonstrasi
4. **Keluar**: Keluar dari program

### Contoh Output

**Mode Terminal:**
```
--- 🕵️ Menganalisis: video.mp4 ---
Tipe File (MIME): video/mp4
📦 Format Kontainer: QuickTime / MOV
Aliran Data (Codecs):
  Stream #0 (VIDEO)
    ▶️  Codec: H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10
    Res: 1920x1080
  Stream #1 (AUDIO)
    ▶️  Codec: AAC (Advanced Audio Coding)
    Sample: 48000 Hz, Channels: 2
```

**Mode GUI:**
- Hasil ditampilkan dalam card dengan icon yang sesuai (gambar/video/audio)
- Status success/error dengan warna yang jelas
- Detail codec dan stream information yang mudah dibaca
- Progress real-time untuk multiple files

## Contoh Penggunaan

### 1. Persiapan File
```
Media_Folder/
├── photo.jpg       # Gambar JPEG
├── video.mp4       # Video H.264 dengan audio AAC
├── music.mp3       # Audio MP3
├── document.pdf    # Non-media (akan di-skip)
└── animation.gif   # Gambar animasi GIF
```

### 2. Setup Environment
```bash
# Navigasi ke folder
cd c:\project\tools-py\media-tools\media-codec-detector

# Aktifkan virtual environment
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
.\venv\Scripts\activate.bat

# Git Bash
source venv/Scripts/activate

# Pastikan dependencies terinstall
pip install -r requirements.txt
```

### 3. Jalankan Program

**GUI Version (Mudah):**
```bash
python media_codec_detector_gui.py
```

**Terminal Version (Advanced):**
```bash
python media_codec_detector.py
```

**CLI dari GUI:**
```bash
python media_codec_detector_gui.py --cli
```

### 4. Hasil
- **GUI**: Hasil analisis ditampilkan dalam card visual yang informatif
- **Terminal**: Output text dengan emoji dan formatting yang rapi
- **File Dummy**: File test otomatis dibuat untuk demonstrasi

## Screenshot GUI

![Media Codec Detector GUI](https://via.placeholder.com/800x600/7B1FA2/ffffff?text=Media+Codec+Detector+GUI)

**Fitur GUI:**
- 🎯 **File/Folder Browser**: Pilih file tunggal atau folder dengan mudah
- 📋 **Media File List**: Lihat semua file media yang ditemukan
- 🕵️ **Real-time Analysis**: Progress dan hasil analisis secara real-time
- 📊 **Visual Results**: Card hasil dengan icon dan status yang jelas
- 🧪 **Dummy File Creator**: Buat file test untuk demonstrasi
- 🎨 **Modern UI**: Interface yang clean dan responsif

## Perbedaan Format Kontainer vs Codec

### Format Kontainer
- **File extension**: .mp4, .mkv, .mov, .avi
- **Fungsi**: "Kotak" yang membungkus data video/audio
- **Contoh**: File .mp4 bisa berisi berbagai kombinasi codec

### Codec
- **Video Codec**: H.264, H.265/HEVC, VP9, AV1
- **Audio Codec**: AAC, MP3, FLAC, Opus
- **Fungsi**: Metode kompresi/dekompresi data aktual

### Format Gambar
- **File**: .jpg, .png, .gif, .webp
- **Codec**: Biasanya langsung menentukan metode kompresi

## Format yang Didukung

### Gambar
- PNG, JPEG, GIF, BMP, TIFF, WebP
- ICO, PSD, dan format lainnya (via Pillow)

### Video
- MP4, AVI, MOV, MKV, WebM, FLV
- 3GP, WMV, dan format lainnya (via FFmpeg)

### Audio
- MP3, AAC, FLAC, WAV, OGG
- M4A, WMA, dan format lainnya (via FFmpeg)

## Troubleshooting

### Error: "ffmpeg not found"
- Pastikan FFmpeg sudah terinstall dan ada di PATH
- Test dengan menjalankan `ffmpeg -version` di terminal

### Error: "No module named 'PIL'"
- Install Pillow: `pip install Pillow`

### Error: "No module named 'ffmpeg'"
- Install ffmpeg-python: `pip install ffmpeg-python`

### File tidak dapat dianalisis
- Pastikan file tidak corrupt
- Cek apakah format didukung
- Untuk file video/audio, pastikan FFmpeg berfungsi

## Dependencies

- **ffmpeg-python**: Wrapper Python untuk FFmpeg
- **Pillow (PIL)**: Library untuk manipulasi gambar
- **filetype**: Library untuk deteksi tipe file
- **flet**: Modern GUI framework untuk Python (cross-platform)

## Author

Program ini dibuat untuk membantu analisis codec dan format file media.

## License

Free to use and modify.

---

<a name="english"></a>
## 🇺🇸 English

Python program to detect container format and codecs from media files.

### ✨ Features

- **Image Format Detection**: PNG, JPEG, GIF, BMP, and more
- **Video Analysis**: Detect video codecs (H.264, H.265, VP9, etc.)
- **Audio Analysis**: Detect audio codecs (MP3, AAC, FLAC, etc.)
- **Modern GUI**: User-friendly interface with Flet
- **Batch Processing**: Analyze multiple files or entire folders
- **Dummy File Creator**: Generate test files for demonstration

### 🚀 Quick Start

```bash
# 1. Navigate to folder
cd media-codec-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run GUI
python media_codec_detector_gui.py
```

For detailed documentation, see the Indonesian section above.


---

<a name="japanese"></a>
## 🇯🇵 日本語

メディアファイルからコンテナ形式とコーデックを検出するPythonプログラム。

### ✨ 機能

- **画像形式検出**: PNG、JPEG、GIF、BMPなど
- **動画解析**: 動画コーデック検出（H.264、H.265、VP9など）
- **音声解析**: 音声コーデック検出（MP3、AAC、FLACなど）
- **モダンGUI**: Fletを使用したユーザーフレンドリーなインターフェース
- **バッチ処理**: 複数ファイルまたはフォルダ全体を解析
- **ダミーファイル作成**: デモンストレーション用のテストファイル生成

### 🚀 クイックスタート

```bash
# 1. フォルダに移動
cd media-codec-detector

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. GUIを実行
python media_codec_detector_gui.py
```

詳細なドキュメントについては、上記のインドネシア語セクションを参照してください。
