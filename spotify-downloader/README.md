# 🎵 Spotify Downloader Pro

Download lagu dari Spotify via YouTube Music match menggunakan **spotdl**.

> **⚠️ CLONE DI DEVICE BARU? BACA INI!**  
> Jika Anda clone repo ini via Git di device lain dan aplikasi error dengan pesan **"Tidak ada lagu yang didownload"**, itu karena dependencies belum terinstall.  
> **Quick Fix:** Double-click `launch_spotify_downloader.bat` dan tunggu setup selesai (2-3 menit pertama kali).

## ✨ Features

- 🎵 Download lagu individual, album, atau playlist dari Spotify
- 🎧 Pilih bitrate audio (128k - 320k)
- 📋 Tampilan real-time daftar lagu yang sedang didownload
- 💾 Pilih folder output custom
- 🎨 Modern GUI dengan Flet framework
- ⚡ Auto-detect & install spotdl jika belum terinstall

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** harus sudah terinstall dan ada di PATH
2. **FFmpeg** harus sudah terinstall dan ada di PATH
3. **Koneksi internet** untuk download lagu

### Installation

#### 🎯 Recommended - Launcher BAT (Windows)

**Cara paling mudah di Windows:**

```bash
# 1. Clone repository
git clone https://github.com/zakkutsu/media-tools-py.git
cd media-tools-py\spotify-downloader

# 2. Double-click file ini:
launch_spotify_downloader.bat
```

**Launcher akan otomatis:**
- ✅ Membuat virtual environment
- ✅ Install semua dependencies (flet, spotdl, dll)
- ✅ Verifikasi spotdl terinstall
- ✅ Jalankan aplikasi

> **💡 Tips:** Jika clone di device baru, cukup double-click `launch_spotify_downloader.bat` dan tunggu setup selesai!

#### 🔧 Alternative - Manual Installation

Jika ingin manual atau pakai macOS/Linux:

```bash
# 1. Clone repository
git clone https://github.com/zakkutsu/media-tools-py.git
cd media-tools-py

# 2. Install dependencies (WAJIB!)
pip install -r requirements.txt

# 3. Jalankan Spotify Downloader
cd spotify-downloader
python spotify_downloader_gui_flet.py
```

#### Via Launcher Utama

```bash
# Dari root folder media-tools-py
python media_tools_launcher.py
# Pilih: Spotify Downloader
```

### First Run

Saat pertama kali dibuka, jika **spotdl belum terinstall**, aplikasi akan menampilkan:

```
⚠️ spotdl Belum Terinstall
📦 Install spotdl Sekarang
```

**Klik tombol "Install spotdl Sekarang"** dan tunggu proses instalasi selesai.

Atau install manual via terminal:

```bash
pip install spotdl
```

## 📖 Usage

1. **Masukkan Link Spotify:**
   - Link lagu individual: `https://open.spotify.com/track/...`
   - Link album: `https://open.spotify.com/album/...`
   - Link playlist: `https://open.spotify.com/playlist/...`

2. **Pilih Bitrate:**
   - 128k (ekonomis)
   - 192k (standar)
   - 256k (high quality)
   - 320k (highest quality) - **Default**

3. **Pilih Folder Output:**
   - Default: `~/Downloads/Music_Downloads`
   - Klik "Pilih Folder" untuk custom location

4. **Klik "Mulai Download"**
   - Progress akan ditampilkan real-time
   - Tabel akan menunjukkan status setiap lagu:
     - ⚪ Waiting
     - 🔵 Downloading
     - ✅ Done
     - ❌ Error

## ❓ Troubleshooting

### 🚨 Flow Chart Troubleshooting

```
Clone Repo di Device Baru
        ↓
Double-click launch_spotify_downloader.bat
        ↓
    Setup Otomatis Running
        ↓
    ┌─────────────────┐
    │ Apakah berhasil?│
    └────┬────────┬───┘
         │        │
    [YES]│        │[NO - Error Python]
         │        └→ Install Python 3.8+
         │           → Tambahkan ke PATH
         │           → Restart launcher
         │
    [GUI Terbuka]
         ↓
    ┌─────────────────────────┐
    │ Muncul alert spotdl?    │
    └────┬────────────────┬───┘
         │                │
    [YES]│                │[NO - Ready to use]
         │                └→ Masukkan link Spotify
         │                   → Download!
         │
    [Klik "Install spotdl Sekarang"]
         │
    ┌─────────────────┐
    │ Install sukses? │
    └────┬────────┬───┘
         │        │
    [YES]│        │[NO]
         │        └→ Cek koneksi internet
         │           → Manual: pip install spotdl
         │           → Restart app
         │
    [Restart Aplikasi]
         ↓
    [Ready to Download! ✅]
```

### Error: "Tidak ada lagu yang didownload"

**Penyebab umum:**

1. **spotdl belum terinstall** ⚠️ **PALING SERING**
   - ✅ **Via GUI:** Klik tombol "Install spotdl Sekarang"
   - ✅ **Via Terminal:** `pip install spotdl`
   - ✅ **Via Launcher:** Restart `launch_spotify_downloader.bat`

2. **Link Spotify tidak valid**
   - ✅ Pastikan link berformat: `https://open.spotify.com/track/...`
   - ✅ Atau: `https://open.spotify.com/album/...`
   - ✅ Atau: `https://open.spotify.com/playlist/...`

3. **FFmpeg belum terinstall**
   - ✅ Windows: `choco install ffmpeg` atau download dari [ffmpeg.org](https://ffmpeg.org)
   - ✅ macOS: `brew install ffmpeg`
   - ✅ Linux: `sudo apt install ffmpeg`
   - ✅ Verifikasi: `ffmpeg -version` di terminal

4. **Koneksi internet bermasalah**
   - ✅ Pastikan koneksi stabil (spotdl matching lagu via YouTube Music)
   - ✅ Cek firewall tidak block Python

### Error: "Module 'spotdl' not found"

```bash
# Install spotdl
pip install spotdl>=4.0.0

# Atau via requirements
pip install -r requirements.txt
```

### Clone dari Git - Device Baru

Jika aplikasi error setelah clone di device lain:

#### Via BAT Launcher (Recommended)

```bash
# Hapus folder venv lama (jika ada)
rmdir /s /q venv

# Double-click launcher lagi
launch_spotify_downloader.bat
```

Launcher akan re-setup dari awal dengan clean environment.

#### Manual Troubleshooting

```bash
# 1. Pastikan virtual environment aktif (jika pakai)
.\venv\Scripts\Activate.ps1  # Windows
source venv/bin/activate      # Linux/macOS

# 2. Install SEMUA dependencies
pip install -r requirements.txt

# 3. Verifikasi spotdl terinstall
python -m pip show spotdl

# Jika spotdl tidak ada, install manual:
pip install spotdl>=4.0.0

# 4. Jalankan aplikasi
python spotify_downloader_gui_flet.py
```

### Error: Launcher BAT Langsung Close

Jika window CMD langsung close setelah double-click:

1. **Buka CMD/PowerShell manual**
2. **Navigate ke folder:**
   ```bash
   cd C:\path\to\media-tools-py\spotify-downloader
   ```
3. **Jalankan bat file di terminal:**
   ```bash
   launch_spotify_downloader.bat
   ```
4. **Lihat error message** yang muncul
5. **Kemungkinan error:**
   - Python tidak ditemukan → Install Python 3.8+
   - pip error → Cek koneksi internet
   - FFmpeg missing → Install FFmpeg

## 🔧 Technical Details

- **Backend:** spotdl (Spotify + YouTube Music matching)
- **GUI Framework:** Flet
- **Audio Format:** MP3
- **Bitrate Range:** 128k - 320k
- **Metadata:** Auto-embedded (artist, title, album, etc.)

## 📝 Notes

- Aplikasi **TIDAK login ke Spotify**, hanya matching metadata via YouTube Music
- Kualitas audio tergantung source dari YouTube Music
- Download speed tergantung koneksi internet Anda
- Proses download berjalan di background thread (UI tetap responsive)

## 🆘 Support

Jika masih ada error, cek:
1. ✅ Python 3.8+ terinstall: `python --version`
2. ✅ FFmpeg terinstall: `ffmpeg -version`
3. ✅ spotdl terinstall: `python -m pip show spotdl`
4. ✅ Dependencies terinstall: `pip install -r requirements.txt`

## 📋 Quick Reference Card

### ✅ Checklist Setup Device Baru

```
☐ Python 3.8+ terinstall → python --version
☐ Python ada di PATH
☐ FFmpeg terinstall → ffmpeg -version
☐ Koneksi internet aktif
☐ Clone repo → git clone ...
☐ Double-click launch_spotify_downloader.bat
☐ Tunggu setup selesai (2-5 menit)
☐ Jika alert spotdl → Klik "Install spotdl Sekarang"
☐ Restart app
☐ Ready! ✨
```

### 🎯 Command Cheat Sheet

```bash
# Cek Prerequisites
python --version          # Harus 3.8+
ffmpeg -version          # Harus ada output
pip --version            # Cek pip tersedia

# Install Manual
pip install spotdl>=4.0.0
pip install flet>=0.28.0

# Verifikasi Install
python -m pip show spotdl
python -m pip show flet

# Clean Install (Jika error)
cd spotify-downloader
rmdir /s /q venv                    # Windows
rm -rf venv                         # Linux/macOS
launch_spotify_downloader.bat       # Restart setup

# Test spotdl
python -m spotdl --version
```

### 🆘 Still Having Issues?

1. **Buka terminal/CMD**
2. **Navigate ke folder:**
   ```bash
   cd C:\project\media-tools-py\spotify-downloader
   ```
3. **Jalankan manual untuk lihat error:**
   ```bash
   python spotify_downloader_gui_flet.py
   ```
4. **Copy error message** dan cek di Google atau buat issue di GitHub

## 📜 License

Part of Media Tools Suite
