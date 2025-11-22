# SocMed Downloader 📥

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

Program Python untuk mendownload video dan audio dari berbagai platform social media menggunakan yt-dlp dan FFmpeg. Tersedia dalam versi **GUI (Flet)** dan **Command Line**.

## Fitur

- **Multi-Platform Support**: YouTube, TikTok, Instagram, Facebook, Twitter/X
- **Dual Format**: Video (MP4) dan Audio (MP3 192kbps)
- **Quality Selector**: Pilih kualitas 480p, 720p, 1080p, atau Terbaik (otomatis)
- **TikTok Watermark Removal**: Download TikTok tanpa watermark
- **Cookie Support**: Browser cookies untuk bypass login Instagram/Facebook
- **GUI Modern**: Interface grafis multi-bahasa (ID/EN/JP) dengan Flet
- **CLI Mode**: Terminal interaktif dengan looping
- **Real-time Progress**: Progress bar dan speed indicator
- **Auto Quality**: Download kualitas terbaik yang tersedia
- **FFmpeg Integration**: Otomatis convert audio dan merge video HD

## Platform yang Didukung

| Platform | Video | Audio | Notes |
|----------|-------|-------|-------|
| YouTube | ✅ | ✅ | Playlist, Shorts, 8K support |
| TikTok | ✅ | ✅ | Tanpa watermark otomatis |
| Instagram | ✅ | ✅ | Butuh cookies browser |
| Facebook | ✅ | ✅ | Butuh cookies browser |
| Twitter/X | ✅ | ✅ | Video & GIF support |

## Instalasi

### 1. Install FFmpeg (Wajib)

Program ini memerlukan FFmpeg untuk memproses media:

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
cd c:\project\media-tools-py\socmed-downloader
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
pip install yt-dlp flet
```

#### Verifikasi Instalasi
```bash
# Test FFmpeg
ffmpeg -version

# Test Python dependencies
python -c "import yt_dlp, flet; print('Dependencies OK!')"
```

## Cara Penggunaan

### Mode GUI (Recommended) 🖥️

#### Langkah-langkah Lengkap:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder project:**
   ```bash
   cd c:\project\media-tools-py\socmed-downloader
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
   python socmed_downloader_gui.py
   ```
   
   **Atau double-click file `launch_downloader.bat` (Windows)**

#### Menggunakan GUI:

**Fitur GUI:**
- **Multi-Language**: Pilih bahasa Indonesia, English, atau 日本語
- **URL Input**: Paste link dari platform apapun
- **Format Selector**: Pilih Video atau Audio (MP3)
- **Quality Selector**: Pilih kualitas video (480p/720p/1080p/Terbaik)
- **Cookie Selector**: Pilih browser untuk bypass login (Chrome/Edge/Firefox/Brave)
- **Real-time Progress**: Progress bar dan speed monitoring
- **Platform Detection**: Otomatis detect platform dan judul video
- **Modern UI**: Interface yang clean dan user-friendly

**Langkah-langkah:**
1. **Pilih Bahasa**: Dropdown bahasa di kanan atas
2. **Paste URL**: Copy link dari YouTube/TikTok/IG/FB/Twitter
3. **Pilih Format**: Video atau Audio
4. **Pilih Kualitas**: Untuk video, pilih 480p/720p/1080p atau Terbaik
5. **Pilih Cookies**: Jika download IG/FB, pilih browser yang sedang login
6. **Download**: Klik tombol "Mulai Download"
7. **Selesai**: File tersimpan di folder Downloads

### Mode Terminal (CLI)

#### Langkah-langkah:

1. **Buka Terminal/Command Prompt**
2. **Navigasi ke folder:**
   ```bash
   cd c:\project\media-tools-py\socmed-downloader
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
4. **Jalankan CLI:**
   ```bash
   python socmed_downloader.py
   ```

Program akan menampilkan menu dengan pilihan:
- Paste URL video/audio
- Pilih format (Video/Audio)
- Pilih kualitas (untuk video)
- Download otomatis dengan progress
- Looping - download lagi atau ketik 'exit'

## Contoh Penggunaan

### 1. Download YouTube Video (1080p)
```bash
# GUI: Paste URL → Pilih Video → Pilih 1080p → Download
# CLI: Run script → Paste URL → Pilih 1 (Video) → Pilih 2 (1080p)
```

### 2. Download YouTube Audio (MP3)
```bash
# GUI: Paste URL → Pilih Audio (MP3) → Download
# CLI: Run script → Paste URL → Pilih 2 (Audio)
```

### 3. Download TikTok (Tanpa Watermark)
```bash
# GUI: Paste TikTok URL → Pilih Video → Download
# CLI: Run script → Paste TikTok URL → Pilih 1
# Result: Video tanpa watermark TikTok!
```

### 4. Download Instagram Reels (Dengan Cookies)
```bash
# Persiapan: Login Instagram di browser Chrome
# GUI: Pilih Cookies "Google Chrome" → Paste IG URL → Download
# CLI: Edit socmed_downloader.py → Set BROWSER_COOKIES = 'chrome' → Run
```

### 5. Download Facebook Video (Dengan Cookies)
```bash
# Persiapan: Login Facebook di browser
# GUI: Pilih Cookies browser → Paste FB URL → Download
# CLI: Edit socmed_downloader.py → Set BROWSER_COOKIES = 'chrome' → Run
```

## Kualitas Video

### Quality Options:
- **Terbaik (Otomatis)**: Download kualitas tertinggi yang tersedia (bisa 4K/8K dari YouTube)
- **1080p (Full HD)**: Maksimal 1920x1080, ukuran file sedang
- **720p (HD)**: Maksimal 1280x720, ukuran file kecil, cepat download
- **480p (SD)**: Maksimal 854x480, ukuran file sangat kecil, untuk koneksi lambat

### Rekomendasi:
- **YouTube 4K/8K**: Pilih "Terbaik" (file besar)
- **Normal viewing**: 1080p atau 720p (balanced)
- **Mobile/WhatsApp**: 480p atau 720p (hemat kuota)
- **Archive/Collection**: Terbaik (kualitas maksimal)

## Cookie Setup untuk Instagram & Facebook

### Kenapa Butuh Cookies?
Instagram dan Facebook sering memblokir akses anonim dengan error:
- ❌ "Login required"
- ❌ "Sign in to view"  
- ❌ "This content isn't available"

**Solusi**: Gunakan cookies dari browser yang sedang login.

### Cara Setup (GUI Version):
1. **Login** Instagram/Facebook di browser (Chrome/Edge/Firefox/Brave)
2. **Jangan logout** dari browser
3. **Buka GUI** SocMed Downloader
4. **Pilih browser** di dropdown "Browser Cookies"
5. **Download** seperti biasa

### Cara Setup (CLI Version):
1. **Login** Instagram/Facebook di browser Chrome
2. **Edit** file `socmed_downloader.py`
3. **Ubah baris 10**:
   ```python
   BROWSER_COOKIES = 'chrome'  # Ganti sesuai browser: chrome/edge/firefox/brave
   ```
4. **Save** file
5. **Run** script seperti biasa

**Note**: Cookies akan otomatis diambil dari browser yang sedang login, jadi tetap aman.

## Troubleshooting

### Error: "ffmpeg not found"
- Pastikan FFmpeg terinstall: `ffmpeg -version`
- Tambahkan FFmpeg ke PATH environment variable
- Restart terminal setelah install FFmpeg

### Error: "Login required" (Instagram/Facebook)
- Aktifkan cookie support (lihat "Cookie Setup" di atas)
- Pastikan sudah login di browser yang dipilih
- Coba restart browser setelah login

### Error: "No module named 'flet'"
- Pastikan virtual environment aktif: `.\venv\Scripts\Activate.ps1`
- Install dependencies: `pip install -r requirements.txt`
- Atau manual: `pip install flet`

### Error: "Unsupported URL"
- Cek URL sudah benar dan lengkap
- Pastikan platform didukung (YT/TikTok/IG/FB/Twitter)
- Update yt-dlp: `pip install --upgrade yt-dlp`

### TikTok masih ada watermark
- Update yt-dlp ke versi terbaru: `pip install --upgrade yt-dlp`
- Coba download ulang

### GUI tidak muncul
- Pastikan flet terinstall: `pip install flet`
- Test: `python -c "import flet; print('OK')"`
- Gunakan CLI sebagai alternatif

### Video tidak bisa diputar
- Pastikan FFmpeg terinstall dengan benar
- Coba player lain (VLC, MPV)
- Coba download ulang dengan format berbeda

## Tips Penggunaan

### 1. Update Berkala
```bash
# Update yt-dlp setiap 1-2 bulan untuk support algoritma terbaru
pip install --upgrade yt-dlp
```

### 2. Pilih Kualitas Sesuai Kebutuhan
- **Collection/Archive**: Terbaik (4K/8K)
- **Daily viewing**: 1080p atau 720p
- **Mobile/Share**: 720p atau 480p

### 3. Gunakan GUI untuk Kemudahan
- Multi-language support
- Visual quality selector
- Easy cookie management
- Real-time progress

### 4. Looping Feature (CLI)
CLI support looping untuk download multiple video tanpa restart:
```
>> Download video 1 → Selesai
>> Download video 2 → Selesai
>> Download video 3 → Selesai
>> Ketik 'exit' → Keluar
```

### 5. Organize Downloaded Files
```
Downloads/
├── YouTube/
├── TikTok/
├── Instagram/
└── Others/
```

## Dependencies

- **yt-dlp**: Library download untuk berbagai platform
- **flet**: Modern GUI framework (cross-platform)
- **FFmpeg**: Audio/video processor (sistem requirement)

## File Structure

```
socmed-downloader/
├── socmed_downloader_gui.py    # GUI version (Flet) dengan multi-language
├── socmed_downloader.py        # CLI version dengan quality selector
├── language_config.py          # Multi-language configuration (ID/EN/JP)
├── requirements.txt            # Python dependencies
├── launch_downloader.bat       # Windows quick launcher (GUI)
├── README.md                   # Dokumentasi lengkap
└── venv/                       # Virtual environment (setelah setup)
```

## Author

Program untuk memudahkan download konten dari berbagai platform social media dengan kualitas terbaik.

## License

Free to use and modify untuk penggunaan personal dan educational purposes.

## Disclaimer

⚠️ **Penting:**
- Tool ini untuk **personal use** dan **educational purposes** saja
- Hormati hak cipta dan privasi orang lain
- Jangan download konten yang dilindungi hak cipta tanpa izin
- Jangan gunakan untuk tujuan komersial tanpa izin
- Untuk konten privat (IG/FB), pastikan punya izin dari pemilik

---

<a name="english"></a>
## 🇺🇸 English

Python program to download videos and audio from various social media platforms using yt-dlp and FFmpeg.

### ✨ Features

- **Multi-Platform Support**: YouTube, TikTok, Instagram, Facebook, Twitter/X
- **Dual Format**: Video (MP4) and Audio (MP3 192kbps)
- **Quality Selector**: Choose 480p, 720p, 1080p, or Best (automatic)
- **TikTok Watermark Removal**: Download TikTok without watermark
- **Cookie Support**: Browser cookies to bypass Instagram/Facebook login
- **Modern GUI**: Multi-language interface (ID/EN/JP) with Flet
- **CLI Mode**: Interactive terminal with looping
- **Real-time Progress**: Progress bar and speed indicator
- **Auto Quality**: Download best quality available
- **FFmpeg Integration**: Automatic audio conversion and HD video merging

### 🚀 Quick Start

```bash
# 1. Navigate to folder
cd socmed-downloader

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run GUI
python socmed_downloader_gui.py

# Or run CLI
python socmed_downloader.py
```

### 📥 Supported Platforms

| Platform | Video | Audio | Notes |
|----------|-------|-------|-------|
| YouTube | ✅ | ✅ | Playlists, Shorts, 8K support |
| TikTok | ✅ | ✅ | Automatic watermark removal |
| Instagram | ✅ | ✅ | Requires browser cookies |
| Facebook | ✅ | ✅ | Requires browser cookies |
| Twitter/X | ✅ | ✅ | Video & GIF support |

### 🎯 Usage Examples

**Download YouTube Video (1080p):**
- GUI: Paste URL → Select Video → Choose 1080p → Download
- CLI: Run script → Paste URL → Select 1 (Video) → Choose 2 (1080p)

**Download TikTok (No Watermark):**
- Paste TikTok URL → Select Video → Download
- Result: Video without TikTok watermark!

**Download Instagram/Facebook (With Cookies):**
- Preparation: Login to IG/FB in Chrome browser
- GUI: Select "Google Chrome" in Cookies dropdown → Paste URL → Download
- CLI: Edit `BROWSER_COOKIES = 'chrome'` in socmed_downloader.py → Run

For detailed documentation, see the Indonesian section above.

---

<a name="japanese"></a>
## 🇯🇵 日本語

yt-dlpとFFmpegを使用して、様々なソーシャルメディアプラットフォームから動画と音声をダウンロードするPythonプログラム。

### ✨ 機能

- **マルチプラットフォーム対応**: YouTube, TikTok, Instagram, Facebook, Twitter/X
- **デュアルフォーマット**: ビデオ（MP4）とオーディオ（MP3 192kbps）
- **品質セレクター**: 480p、720p、1080p、または最高（自動）を選択
- **TikTok透かし除去**: TikTokを透かしなしでダウンロード
- **Cookie対応**: Instagram/Facebookログインをバイパスするブラウザクッキー
- **モダンGUI**: 多言語インターフェース（ID/EN/JP）とFlet
- **CLIモード**: ループ機能付きインタラクティブターミナル
- **リアルタイム進行状況**: プログレスバーと速度インジケーター
- **自動品質**: 利用可能な最高品質をダウンロード
- **FFmpeg統合**: 自動音声変換とHDビデオマージ

### 🚀 クイックスタート

```bash
# 1. フォルダに移動
cd socmed-downloader

# 2. 仮想環境を作成
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows PowerShell

# 3. 依存関係をインストール
pip install -r requirements.txt

# 4. GUIを実行
python socmed_downloader_gui.py

# またはCLIを実行
python socmed_downloader.py
```

### 📥 対応プラットフォーム

| プラットフォーム | ビデオ | オーディオ | 備考 |
|----------|-------|-------|-------|
| YouTube | ✅ | ✅ | プレイリスト、ショート、8K対応 |
| TikTok | ✅ | ✅ | 自動透かし除去 |
| Instagram | ✅ | ✅ | ブラウザCookie必要 |
| Facebook | ✅ | ✅ | ブラウザCookie必要 |
| Twitter/X | ✅ | ✅ | ビデオ&GIF対応 |

### 🎯 使用例

**YouTubeビデオをダウンロード（1080p）:**
- GUI: URLを貼り付け → ビデオを選択 → 1080pを選択 → ダウンロード
- CLI: スクリプトを実行 → URLを貼り付け → 1を選択（ビデオ） → 2を選択（1080p）

**TikTokをダウンロード（透かしなし）:**
- TikTok URLを貼り付け → ビデオを選択 → ダウンロード
- 結果: TikTok透かしなしのビデオ！

**Instagram/Facebookをダウンロード（Cookieあり）:**
- 準備: ChromeブラウザでIG/FBにログイン
- GUI: Cookie ドロップダウンで「Google Chrome」を選択 → URLを貼り付け → ダウンロード
- CLI: socmed_downloader.pyで`BROWSER_COOKIES = 'chrome'`を編集 → 実行

詳細なドキュメントについては、上記のインドネシア語セクションを参照してください。
