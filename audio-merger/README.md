# Audio Merger 🎵

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

Program Python untuk menggabungkan multiple file audio menjadi satu file menggunakan pydub dan FFmpeg. Tersedia dalam versi **GUI (Flet)** dan **Command Line**.

## Fitur

- **Multi-format Support**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA
- **Crossfade Effect**: Transisi halus antar lagu dengan fade in/out
- **Gap/Jeda**: Menambahkan silence antar lagu
- **GUI Modern**: Interface grafis dengan ### 5. Folder Output
- **Default**: File hasil disimpan di C:\Users\nonion\Music
- **Custom**: Klik "Pilih Folder Tujuan" untuk menyimpan di lokasi lain  
- **Reset**: Klik "Reset" untuk kembali ke folder default (C:\Users\nonion\Music)
- **Persistensi**: Folder tujuan akan terus digunakan sampai diresetyang user-friendly dengan folder output selection
- **Mode Interaktif**: Interface menu terminal
- **Command Line**: Support argumen untuk automasi
- **Auto-sorting**: File diurutkan otomatis berdasarkan nama
- **Real-time Progress**: Indikator progress untuk proses penggabungan dengan detail step-by-step

## Instalasi

### 1. Install FFmpeg (Wajib)

Program ini memerlukan FFmpeg untuk memproses audio:

**Windows:**
```bash
# Menggunakan Chocolatey
choco install ffmpeg

# Atau download manual dari https://ffmpeg.org/download.html
# Ekstrak dan tambahkan ke PATH
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

### 2. Setup Python Environment

#### Clone/Download Project
```bash
# Navigasi ke folder project
cd c:\project\tools-py\media-tools\audio-merger
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
pip install pydub flet pyaudioop
```

#### Verifikasi Instalasi
```bash
# Test FFmpeg
ffmpeg -version

# Test Python dependencies
python -c "import pydub, flet; print('Dependencies OK!')"
```

## Cara Penggunaan

### Mode GUI (Recommended) 🖥️

#### Langkah-langkah Lengkap:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder project:**
   ```bash
   cd c:\project\tools-py\media-tools\audio-merger
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
   python audio_merger_gui.py
   ```

#### Menggunakan GUI:

**Fitur GUI:**
- **Folder Input Browser**: Pilih folder sumber file audio
- **Folder Output Browser**: Pilih folder tujuan penyimpanan hasil (opsional)
- **Visual File List**: Melihat semua file audio yang ditemukan dengan ukuran
- **Slider Controls**: Pengaturan crossfade dan gap dengan slider
- **Real-time Progress**: Progress bar dan status update detail
- **Modern UI**: Interface yang clean dan mudah digunakan

**Langkah-langkah:**
1. **Pilih Folder Input**: Klik tombol "Pilih Folder Audio"
2. **Lihat File**: Program akan menampilkan semua file audio yang ditemukan
3. **Pilih Folder Tujuan**: Klik "Pilih Folder Tujuan" atau biarkan default (C:\Users\nonion\Music)
4. **Atur Output**: Masukkan nama file hasil
5. **Pilih Efek**: Normal, Crossfade, atau Gap/Jeda
6. **Gabungkan**: Klik tombol "Gabungkan Audio"
7. **Selesai**: File hasil akan tersimpan di folder tujuan yang dipilih

### Mode Terminal Interaktif

#### Langkah-langkah:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder:**
   ```bash
   cd c:\project\tools-py\media-tools\audio-merger
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
   python audio_merger.py
   ```

Program akan menampilkan menu dengan pilihan:
1. **Analisis file tertentu** - Masukkan path file untuk dianalisis
2. **Analisis semua file dalam folder** - Analisis semua file dalam direktori
3. **Buat file dummy untuk testing** - Membuat file test untuk demonstrasi
4. **Keluar** - Keluar dari program

```bash
python audio_merger.py
```

Program akan menampilkan menu dengan pilihan:
1. **Gabungkan audio dari folder** - Penggabungan normal
2. **Gabungkan audio dengan crossfade** - Transisi halus
3. **Gabungkan audio dengan jeda** - Tambahkan silence
4. **Info tentang efek** - Penjelasan crossfade dan gap
5. **Keluar**

### Mode Command Line

```bash
# Pastikan virtual environment aktif terlebih dahulu
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt  
.\venv\Scripts\activate.bat

# Git Bash
source venv/Scripts/activate

# Gunakan flag --cli untuk mode command line
python audio_merger_gui.py --cli

# Atau langsung gunakan versi CLI
python audio_merger.py --folder "C:\Music\Album" --output "album_complete.mp3"

# Dengan crossfade 3 detik
python audio_merger.py --folder "C:\Music\Album" --output "album_crossfade.mp3" --crossfade 3

# Dengan jeda 2 detik antar lagu
python audio_merger.py --folder "C:\Music\Album" --output "album_gap.mp3" --gap 2

# Hanya format tertentu
python audio_merger.py --folder "C:\Music" --formats mp3 wav --output "result.mp3"
```

### Parameter Command Line

- `--folder, -f`: Path folder yang berisi file audio
- `--output, -o`: Nama file output (default: hasil_gabungan.mp3)
- `--crossfade, -c`: Durasi crossfade dalam detik (default: 0)
- `--gap, -g`: Durasi jeda antar lagu dalam detik (default: 0)
- `--formats`: Format file yang dicari (default: semua format)

## Contoh Penggunaan

### 1. Persiapan File
```
Music_Folder/
├── 01_intro.mp3
├── 02_verse.wav
├── 03_chorus.flac
├── 04_bridge.m4a
└── 05_outro.ogg
```

### 2. Setup Environment
```bash
# Navigasi ke folder
cd c:\project\tools-py\media-tools\audio-merger

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
python audio_merger_gui.py
```

**Terminal Version (Advanced):**
```bash
python audio_merger.py
```

**Command Line (Automation):**
```bash
python audio_merger.py --folder "C:\Music_Folder" --output "album.mp3" --crossfade 2
```

### 4. Hasil
```
album.mp3  # File output yang berisi semua lagu digabung
```

## Screenshot GUI

![Audio Merger GUI](https://via.placeholder.com/600x400/4285f4/ffffff?text=Audio+Merger+GUI)

**Fitur GUI:**
- 🎯 **Input Folder Browser**: Pilih folder sumber audio dengan mudah
- 💾 **Output Folder Browser**: Pilih folder tujuan penyimpanan (opsional)
- 📋 **File List**: Lihat semua file yang akan digabung dengan info ukuran
- 🎚️ **Slider Controls**: Atur crossfade dan gap dengan presisi
- 📊 **Progress Bar**: Monitor proses real-time dengan detail
- 🎨 **Modern UI**: Interface yang clean dan responsif

## Jenis Efek

### 🔗 Gabungan Langsung
- Lagu disambung langsung tanpa efek
- Cepat dan sederhana
- Durasi = total durasi semua lagu

### 🔄 Crossfade
- Lagu pertama fade out saat lagu kedua fade in
- Transisi halus dan natural
- Durasi sedikit berkurang karena overlap
- **Contoh**: 2 detik crossfade = overlap 2 detik

### ⏸️ Gap/Jeda
- Menambahkan silence antar lagu
- Memberikan jeda nafas
- Durasi bertambah sesuai jeda
- **Contoh**: 1 detik gap = tambah 1 detik silence

## Format yang Didukung

### Input (dapat dicampur)
- **Lossless**: WAV, FLAC
- **Lossy**: MP3, M4A, OGG, AAC
- **Lainnya**: WMA

### Output
- MP3 (default)
- WAV, FLAC, M4A, OGG, AAC
- Format ditentukan dari ekstensi file output

## Troubleshooting

### Error: "ffmpeg not found"
- Pastikan FFmpeg terinstall dan ada di PATH
- Test dengan: `ffmpeg -version`

### Error: "No module named 'audioop'" atau "No module named 'pyaudioop'"
**Penyebab**: Python 3.13+ telah menghapus modul `audioop` dari standard library

**Solusi 1 - Install pyaudioop (Recommended):**
```bash
# Aktifkan virtual environment terlebih dahulu
source venv/Scripts/activate  # Git Bash
# atau
.\venv\Scripts\Activate.ps1   # PowerShell

# Install pyaudioop
pip install pyaudioop
```

**Solusi 2 - Downgrade Python (jika perlu):**
```bash
# Gunakan Python 3.12 atau lebih lama
python3.12 -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

**Solusi 3 - Update requirements.txt:**
Tambahkan `pyaudioop` ke requirements.txt untuk mengatasi masalah ini secara permanen.

### Error: "No module named 'pydub'" atau "No module named 'flet'"
- Pastikan virtual environment aktif: `.\venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`

### Error: "cannot activate virtual environment"
**Windows PowerShell:**
```bash
# Ubah execution policy jika perlu
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Lalu aktifkan venv
.\venv\Scripts\Activate.ps1
```

**Alternative untuk Windows:**
```bash
# Command Prompt
.\venv\Scripts\activate.bat

# Git Bash  
source venv/Scripts/activate
```

### Virtual environment tidak ada
```bash
# Buat virtual environment baru
python -m venv venv

# Aktifkan sesuai terminal yang digunakan
# PowerShell
.\venv\Scripts\Activate.ps1

# Command Prompt
.\venv\Scripts\activate.bat

# Git Bash
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

### File tidak dapat dibaca
- Pastikan file audio tidak corrupt
- Cek format file didukung
- Pastikan permission read file

### Output file kosong atau error
- Cek permission write di folder output
- Pastikan ada space disk yang cukup
- Coba format output yang berbeda

### GUI tidak muncul
- Pastikan flet terinstall: `pip install flet`
- Coba jalankan: `python -c "import flet; print('Flet OK!')"`
- Gunakan mode CLI sebagai alternatif: `python audio_merger.py`

## Tips Penggunaan

### 1. Penamaan File
Gunakan prefix angka untuk urutan yang benar:
```
01_song.mp3
02_song.mp3
10_song.mp3  # Bukan 1_song.mp3
```

### 2. Kualitas Audio
- Input lossless (WAV/FLAC) → Output lossy (MP3) = kualitas turun
- Input lossy → Output lossy = kualitas turun lebih
- Gunakan format yang sama untuk hasil terbaik

### 3. Crossfade Optimal
- **Lagu musik**: 2-4 detik
- **Podcast/speech**: 0.5-1 detik
- **DJ mix**: 4-8 detik

### 4. Folder Output
- **Default**: File hasil disimpan di folder yang sama dengan input
- **Custom**: Klik "Pilih Folder Tujuan" untuk menyimpan di lokasi lain
- **Reset**: Klik "Reset" untuk kembali ke folder input
- **Persistensi**: Folder tujuan akan terus digunakan sampai direset

### 5. Performance
- File besar membutuhkan RAM lebih
- Proses di chunk jika memory terbatas
- SSD lebih cepat untuk I/O

## Dependencies

- **pydub**: Library audio processing untuk Python
- **flet**: Modern GUI framework untuk Python (cross-platform)
- **FFmpeg**: Audio/video processor (sistem requirement)
- **threading**: Built-in Python library untuk background processing
- **pathlib**: Built-in Python library untuk path management

## File Structure

```
audio-merger/
├── audio_merger.py          # CLI version dengan interactive menu
├── audio_merger_gui.py      # GUI version dengan folder output selection
├── requirements.txt         # Python dependencies
├── README.md               # Dokumentasi lengkap
└── venv/                   # Virtual environment (setelah setup)
```

## Author

Program untuk memudahkan penggabungan file audio dengan berbagai efek transisi.

## License

Free to use and modify.

---

<a name="english"></a>
## 🇺🇸 English

Python program to merge multiple audio files into one using pydub and FFmpeg.

### ✨ Features

- **Multi-format Support**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA
- **Crossfade Effect**: Smooth transitions between songs
- **Gap/Silence**: Add silence between tracks
- **Modern GUI**: User-friendly graphical interface (Flet)
- **CLI Mode**: Command line support for automation
- **Auto-sorting**: Files automatically sorted by name
- **Real-time Progress**: Detailed progress indicators

### 🚀 Quick Start

```bash
# 1. Navigate to folder
cd audio-merger

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run GUI
python audio_merger_gui.py
```

For detailed documentation, see the Indonesian section above.


---

<a name="japanese"></a>
## 🇯🇵 日本語

pydubとFFmpegを使用して複数の音声ファイルを1つに結合するPythonプログラム。

### ✨ 機能

- **マルチフォーマット対応**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA
- **クロスフェード効果**: 曲間のスムーズな遷移
- **ギャップ/無音**: トラック間に無音を追加
- **モダンGUI**: ユーザーフレンドリーなグラフィカルインターフェース（Flet）
- **CLIモード**: 自動化のためのコマンドラインサポート
- **自動ソート**: ファイル名で自動的にソート
- **リアルタイム進行状況**: 詳細な進行状況インジケーター

### 🚀 クイックスタート

```bash
# 1. フォルダに移動
cd audio-merger

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. GUIを実行
python audio_merger_gui.py
```

詳細なドキュメントについては、上記のインドネシア語セクションを参照してください。
