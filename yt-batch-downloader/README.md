# YouTube Batch Downloader 🎬

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

Tool untuk mendownload **multiple individual YouTube videos** sekaligus dari daftar URL. Berbeda dengan playlist downloader, tool ini untuk download banyak video terpisah/individual dalam satu batch.Tool untuk mendownload **multiple individual YouTube videos** sekaligus dari daftar URL yang diberikan. Berbeda dengan playlist downloader, tool ini untuk download banyak video terpisah/individual dalam satu bat## 🎨 Thumbnail & Metadata Feature



## ✨ FeaturesAll downloads now automatically include:

- **🖼️ YouTube Thumbnail** embedded as cover art (audio) or thumbnail (video)

### Core Features- **📝 Rich Metadata**: Title, artist (channel), date, description

- 📥 **Batch Download** - Download banyak video individual sekaligus

- 🎬 **Multiple Quality** - Best quality, 720p, 480p (hemat kuota)**Example MP3 result:**

- 🎵 **Audio Only Mode** - Extract audio format MP3/M4A```

- 📝 **URL Management** - Add, remove, load from file, save to fileSong.mp3

- 🔢 **Auto Numbering** - Beri nomor urut pada file (opsional)├─ 🎨 YouTube thumbnail as album art

- ⚡ **Continue on Error** - Lanjutkan download meski ada yang gagal├─ 📝 Title: "Song Name"

- 📊 **Progress Tracking** - Status setiap URL (Ready/Success/Failed)├─ 👤 Artist: "Channel Name"

└─ 📅 Date: "2025-11-21"

### 🎨 NEW! Version 2.1 Features```

- 🖼️ **Embed Thumbnail** - YouTube thumbnail sebagai cover art/album art

- 📋 **Add Metadata** - Title, artist, date, description otomatisPerfect for music libraries! See [../METADATA_THUMBNAIL_FEATURE.md](../METADATA_THUMBNAIL_FEATURE.md) for details.

- 🎵 **Beautiful MP3s** - Audio files dengan album art indah dari YouTube!

## 📝 Changelog

**Contoh hasil MP3:**

```See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

My Favorite Song.mp3

├─ 🎨 YouTube thumbnail sebagai album art### Version 2.1 (November 21, 2025)

├─ 📝 Title: "My Favorite Song"- 🎨 **NEW**: Auto embed YouTube thumbnail as cover art

├─ 👤 Artist: "Channel Name"- 📋 **NEW**: Auto add metadata (title, artist, date)

└─ 📅 Date: "2025-11-21"- 🎵 MP3 files with beautiful album art!

```- 📱 Better music player integration



### ⚡ Version 2.0 Features### Version 2.0 (November 21, 2025)

- 🔇 **Silent Mode** - No JavaScript runtime warnings- ✨ Silent mode - no JS runtime warnings

- ⚡ **Enhanced Progress** - Real-time speed, ETA, detailed statistics- ⚡ Enhanced progress with speed & ETA

- 🔄 **Retry Failed** - One-click retry untuk failed URLs saja- 🔄 Retry failed downloads feature

- 🗑️ **Clear Failed** - Hapus failed downloads dari list- 🗑️ Clear failed URLs feature

- 📊 **Statistics** - Speed (videos/min), elapsed time, success/fail counters- 📊 Real-time download statistics



---### Version 1.0

- ✅ Batch download multiple individual videos

## 📋 Requirements- ✅ GUI interface with URL management

- ✅ Multiple quality options

- Python 3.8+- ✅ Audio-only mode

- yt-dlp (auto-install via GUI)- ✅ Optional auto-numbering

- FFmpeg (required untuk thumbnail embedding)- ✅ Continue on error optiones



---### Core Features

- 📥 **Batch Download Multiple Videos** - Download banyak video individual sekaligus

## 🚀 Installation- 🎬 **Multiple Video Quality** - Best quality, 720p, 480p (hemat kuota)

- 🎵 **Audio Only Mode** - Extract audio saja dalam format MP3

### Via Main Launcher (Recommended)- 📝 **URL Management** - Add, remove, load from file, save to file

```bash- 🔢 **Optional Auto Numbering** - Beri nomor urut pada file (opsional)

# Dari folder media-tools- 🖥️ **GUI Interface** - Interface grafis yang user-friendly

python media_tools_launcher.py- ⚡ **Continue on Error** - Lanjutkan download meski ada yang gagal

# Pilih "YouTube Batch Downloader"- 📊 **Progress Tracking** - Lihat status setiap URL (Ready/Success/Failed)

```

### 🆕 New in Version 2.0!

### Standalone- 🔇 **Silent Mode** - No JavaScript runtime warnings, cleaner output

```bash- ⚡ **Enhanced Progress Display** - Real-time speed, ETA, and detailed statistics

# 1. Navigate to folder- 🔄 **Retry Failed Downloads** - One-click retry for failed URLs only

cd yt-batch-downloader- 🗑️ **Clear Failed URLs** - Quickly remove failed downloads from list

- 📊 **Download Statistics** - Speed in videos/min, elapsed time, success/fail counters

# 2. Install dependencies

pip install -r requirements.txt### 🎨 New in Version 2.1!

- 🖼️ **Embed Thumbnail** - YouTube thumbnail as cover art/album art

# 3. Install FFmpeg- 📋 **Add Metadata** - Title, artist, date, description automatically added

# Windows: choco install ffmpeg- 🎵 **Beautiful MP3s** - Audio files with gorgeous album art from YouTube thumbnails!

# macOS: brew install ffmpeg

# Linux: sudo apt install ffmpeg## 📋 Requirements



# 4. Run- Python 3.7+

python batch_downloader_gui_flet.py- yt-dlp (akan diinstall otomatis)

```- FFmpeg (untuk video processing)



---## 🚀 Installation



## 🎯 Cara Penggunaan1. **Navigate to folder**

   ```bash

### GUI Interface   cd media-tools/yt-batch-downloader

   ```

**Launch:**

```bash2. **Install dependencies**

python batch_downloader_gui_flet.py   ```bash

```   pip install -r requirements.txt

   ```

**Workflow:**

1. **Install yt-dlp** (jika belum): Klik tombol "Install/Update yt-dlp"3. **Install FFmpeg** (jika belum ada)

2. **Set Folder**: Pilih folder download atau gunakan default   - **Windows**: Download dari [ffmpeg.org](https://ffmpeg.org/download.html)

3. **Add URLs**:   - **macOS**: `brew install ffmpeg`

   - Manual: Paste URL → klik "Add URL"   - **Ubuntu/Debian**: `sudo apt install ffmpeg`

   - From file: Klik "Load from File" → pilih .txt berisi URLs

4. **Configure**:## 🎯 Cara Penggunaan

   - Pilih type: Video (best/720p/480p) atau Audio (MP3)

   - Set naming template (opsional)### Method 1: GUI (Recommended)

   - Enable auto-numbering (opsional)

5. **Download**: Klik "Start Batch Download"Jalankan interface grafis:

6. **Monitor**: Lihat real-time progress, speed, ETA```bash

7. **Retry** (if needed): Klik "Retry Failed" untuk retry URLs yang gagalpython batch_downloader_gui.py

```

### CLI Interface

**Langkah-langkah:**

**Basic download:**1. Klik "Install/Update yt-dlp" jika belum terinstall

```bash2. Pilih folder download atau biarkan default

python batch_downloader.py3. **Tambahkan URL video YouTube:**

# Follow interactive prompts   - Ketik URL di input field, tekan Enter atau klik "Add URL"

```   - Atau klik "Load from File" untuk load dari file .txt

   - Atau paste multiple URLs sekaligus

---4. Kelola URL list (hapus, copy, save to file)

5. Pilih jenis download (video/audio)

## 📊 Progress Display6. ✅ Centang "Auto Number Files" jika ingin file diberi nomor urut

7. ✅ Centang "Continue on Error" untuk lanjut meski ada yang gagal

**Enhanced progress dengan statistik lengkap:**8. Klik "Start Batch Download"



```### Method 2: Command Line

📊 Download Progress

🎵 [7/20] (35.0%) - Amazing Tutorial Video.mp4Jalankan via terminal:

```bash

Speed: 3.2 videos/min  │  ETA: 04:05python batch_downloader.py

Elapsed: 02:18 | Success: 7 | Failed: 0```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 35%

```Program akan memandu Anda step-by-step:

1. Input URLs satu per satu (ketik 'done' untuk selesai)

**Informasi ditampilkan:**2. Pilih jenis download

- Current video being downloaded3. Pilih auto numbering atau tidak

- Progress: [current/total] (percentage)

- Speed dalam videos/minute### Method 3: Load URLs from File

- ETA (Estimated Time Arrival) format MM:SS

- Elapsed time sejak mulai downloadBuat file .txt dengan format:

- Success/Failed counters real-time```txt

https://www.youtube.com/watch?v=VIDEO_ID_1

---https://www.youtube.com/watch?v=VIDEO_ID_2

https://www.youtube.com/watch?v=VIDEO_ID_3

## 🔄 Retry & Clear Features```



### Retry Failed DownloadsLalu load file tersebut via GUI atau CLI.



**Kapan digunakan:**## 📂 Output Format

- Network interruption saat download

- YouTube rate limiting### Dengan Auto Numbering:

- Temporary server errors```

- Connection timeout01 - Video Title 1.mp4

02 - Video Title 2.mp4

**How it works:**03 - Video Title 3.mp4

1. Download 50 URLs```

2. 5 URLs failed (network issues)

3. Klik "🔄 Retry Failed"### Tanpa Auto Numbering:

4. System isolates 5 failed URLs```

5. Re-download hanya yang failedVideo Title 1.mp4

6. Tidak perlu download ulang yang sudah sukses!Video Title 2.mp4

Video Title 3.mp4

### Clear Failed URLs```



**Kapan digunakan:**## ⚙️ Kustomisasi

- URL video sudah dihapus

- Video private/region-blocked### Template Nama File

- URL invalid/typo

- Permanent failures yang tidak ingin di-retry| Variable | Deskripsi |

|----------|-----------|

**How it works:**| `%(title)s` | Judul video |

1. Identifikasi URLs yang permanently broken| `%(ext)s` | Ekstensi file |

2. Klik "🗑️ Clear Failed"| `%(uploader)s` | Nama channel |

3. Failed URLs dihapus dari list| `%(upload_date)s` | Tanggal upload |

4. Clean list, siap untuk batch baru| `%(duration)s` | Durasi video |



---**Contoh template:**

```

## 🎵 Download Options"%(title)s - %(uploader)s.%(ext)s"

"[%(upload_date)s] %(title)s.%(ext)s"

### Video Quality```

- **Best Quality** - Kualitas terbaik available (1080p/4K jika ada)

- **720p** - HD quality, hemat bandwidth### Kualitas Video

- **480p** - SD quality, paling hemat bandwidth

| Mode | Deskripsi |

### Audio Only (MP3)|------|-----------|

- **Format**: MP3| `best` | Kualitas terbaik yang tersedia |

- **Quality**: Best available| `720p` | Maksimal 720p (hemat bandwidth) |

- **Features**:| `480p` | Maksimal 480p (hemat bandwidth lebih) |

  - ✅ YouTube thumbnail sebagai album art

  - ✅ Metadata lengkap (title, artist, date)## 🎯 Use Cases

  - ✅ Perfect untuk music collection

  - ✅ Ukuran file lebih kecil dari video### 1. **Download Tutorial Series**

- Kumpulkan URL video tutorial dari berbagai channel

### File Naming- Download sekaligus untuk ditonton offline

**Default template:** `%(title)s.%(ext)s`

**With auto-numbering:** `01 - %(title)s.%(ext)s`### 2. **Music Collection**

- List lagu-lagu favorit dari YouTube

**Available variables:**- Download audio saja dalam format MP3

- `%(title)s` - Video title

- `%(ext)s` - File extension### 3. **Educational Content**

- `%(uploader)s` - Channel name- Video pembelajaran dari berbagai sumber

- `%(upload_date)s` - Upload date- Organize dengan auto numbering



**Examples:**### 4. **Backup Favorite Videos**

```- Backup video favorit sebelum dihapus dari YouTube

%(title)s.%(ext)s- Simpan dalam kualitas terbaik

→ Amazing Tutorial.mp4

## 🔧 Troubleshooting

%(uploader)s - %(title)s.%(ext)s

→ TechChannel - Amazing Tutorial.mp4### "yt-dlp not found"

``````bash

pip install --upgrade yt-dlp

---```



## 💡 Tips & Best Practices### Beberapa video gagal download

- Cek "Continue on Error" untuk skip video yang bermasalah

### URL Management- Video mungkin private, region-blocked, atau sudah dihapus

- ✅ Save URL lists ke file .txt untuk reuse- Cek status di URL list - yang merah adalah yang gagal

- ✅ Organize URLs by topic/category

- ✅ Validate URLs sebelum batch download besar### Download terputus

- ✅ Use descriptive filenames saat save URL list- Restart aplikasi dan jalankan lagi

- yt-dlp akan skip file yang sudah ada dan lanjut yang belum

### Download Strategy

- ✅ **Musik**: Gunakan Audio Only (MP3) untuk mendapat cover art & metadata### FFmpeg error

- ✅ **Tutorial**: 720p balance antara quality dan size- Pastikan FFmpeg sudah terinstall: `ffmpeg -version`

- ✅ **Archive**: Best quality untuk preserve original- Download dari [ffmpeg.org](https://ffmpeg.org/download.html)

- ✅ **Mobile**: 480p untuk save bandwidth dan storage

### GUI tidak responsif

### Performance- Jangan tutup aplikasi saat sedang download

- ✅ Enable "Continue on Error" untuk batch besar- Lihat progress di log output

- ✅ Monitor speed - jika <1 video/min, mungkin ada issue

- ✅ Use retry untuk temporary network issues## 📁 Struktur File

- ✅ Clear failed untuk permanent errors

```

### Network Issuesyt-batch-downloader/

- ✅ Jika many failures, check internet connection├── batch_downloader.py         # Core functionality

- ✅ YouTube rate limiting: Wait 10-15 minutes, then retry├── batch_downloader_gui.py     # GUI interface

- ✅ Use VPN jika region-blocked├── requirements.txt           # Dependencies

- ✅ Download saat network stabil (avoid peak hours)└── README.md                 # Documentation (this file)

```

---

## 🆚 Perbedaan dengan Playlist Downloader

## 🎨 Thumbnail & Metadata Embedding

| Feature | Batch Downloader | Playlist Downloader |

### Apa yang Ditambahkan?|---------|------------------|-------------------|

| **Input** | Multiple individual URLs | Single playlist URL |

**Untuk MP3/M4A:**| **Use Case** | Video dari berbagai source | Video dari satu playlist |

- 🖼️ **Cover Art**: YouTube thumbnail embedded| **URL Management** | Manual add/remove/edit | Otomatis dari playlist |

- 📝 **Title**: Video title| **Flexibility** | Sangat fleksibel | Terbatas pada playlist |

- 👤 **Artist**: Channel name

- 📅 **Date**: Upload date## 🌟 Tips & Tricks

- 💬 **Comment**: Video description

1. **Organize URLs**: Simpan URL dalam file .txt per kategori

**Untuk Video:**2. **Test Small Batch**: Coba dulu dengan 2-3 URL sebelum batch besar

- 🖼️ **Thumbnail**: Embedded dalam container3. **Check Video Info**: Pastikan URL valid sebelum download

- 📝 **Metadata**: Title, artist, date, description4. **Use Auto Numbering**: Untuk series/tutorial yang perlu urutan

5. **Save URL Lists**: Backup daftar URL untuk download ulang nanti

### Music Player Compatibility

## ⚠️ Disclaimer

**Tested & Working:**

- ✅ Windows Media PlayerTool ini hanya untuk penggunaan personal dan educational. Pastikan Anda mematuhi:

- ✅ VLC Media Player- Terms of Service YouTube

- ✅ iTunes / Apple Music- Copyright laws di negara Anda

- ✅ Spotify (local files)- Hak cipta content creator

- ✅ Foobar2000

- ✅ MusicBee## 🤝 Support

- ✅ Android Music Players

- ✅ iOS Music AppJika ada masalah atau pertanyaan:

1. Cek troubleshooting section di atas

### Before vs After2. Update yt-dlp ke versi terbaru

3. Pastikan koneksi internet stabil

**Before (tanpa thumbnail):**

```## 🎁 New Features Showcase

Music Library

├─ Song1.mp3  [Generic music icon]### Enhanced Progress Display

├─ Song2.mp3  [Generic music icon]```

└─ Song3.mp3  [Generic music icon]📊 Download Progress

```🎵 [3/10] (30.0%) - Video Title Here...



**After (dengan thumbnail):**Speed: 2.5 videos/min  │  ETA: 03:25

```Elapsed: 01:30 | Success: 3 | Failed: 0

Music Library```

├─ Song1.mp3  [🎨 Colorful YouTube thumbnail]

├─ Song2.mp3  [🎨 Colorful YouTube thumbnail]### Smart Retry System

└─ Song3.mp3  [🎨 Colorful YouTube thumbnail]When downloads fail (network issues, temporary errors):

```1. **"🔄 Retry Failed"** button automatically appears

2. Click to retry only failed URLs

---3. Successful downloads are preserved

4. Perfect for network interruptions!

## 🔧 Troubleshooting

### Quick Cleanup

### Issue: "yt-dlp not found"- **"�️ Clear Failed"** button removes permanently broken URLs

**Solution:**- Keeps your list clean and organized

1. Klik tombol "Install/Update yt-dlp" di GUI- One-click cleanup after identifying invalid URLs

2. Tunggu proses selesai

3. Status berubah menjadi "yt-dlp is available"## �📝 Changelog

4. Coba download lagi

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

### Issue: "No URLs in list"

**Solution:**### Version 2.0 (November 21, 2025)

- Add URLs manually atau- ✨ Silent mode - no JS runtime warnings

- Load from file (.txt dengan 1 URL per line)- ⚡ Enhanced progress with speed & ETA

- 🔄 Retry failed downloads feature

### Issue: "Failed to create download folder"- 🗑️ Clear failed URLs feature

**Solution:**- 📊 Real-time download statistics

- Check folder path valid

- Check write permissions### Version 1.0

- Pastikan drive ada space- ✅ Batch download multiple individual videos

- Gunakan folder di user directory (Downloads, Documents)- ✅ GUI interface with URL management

- ✅ Multiple quality options

### Issue: "Download failed" untuk semua URLs- ✅ Audio-only mode

**Solution:**- ✅ Optional auto-numbering

1. Check internet connection- ✅ Continue on error option

2. Verify URLs valid (paste di browser)- ✅ Load/save URL lists from/to files

3. Check if YouTube down/blocked- ✅ Progress tracking and status display
4. Try different quality option
5. Install/update yt-dlp ke versi terbaru

### Issue: "No thumbnail in MP3"
**Solution:**
1. Pastikan FFmpeg terinstall
2. Check FFmpeg ada di PATH
3. Update yt-dlp: `python -m pip install -U yt-dlp`
4. Re-download file

### Issue: High failure rate
**Possible causes:**
- YouTube rate limiting → Wait 10-15 minutes
- Network unstable → Check connection
- Old yt-dlp version → Update
- Invalid/deleted videos → Clear failed URLs

---

## 📊 Example Workflows

### Workflow 1: Download Music Collection
```
1. Collect URLs of music videos
2. Save URLs to "music_playlist.txt"
3. Open batch downloader
4. Load from file: music_playlist.txt
5. Select "Audio Only (MP3)"
6. Enable auto-numbering
7. Download
8. Result: MP3s with album art ready for music player!
```

### Workflow 2: Tutorial Series
```
1. Add tutorial video URLs manually
2. Select "720p" quality
3. Use template: "%(playlist_index)s - %(title)s.%(ext)s"
4. Enable continue on error
5. Download
6. Monitor progress and retry if needed
```

### Workflow 3: Archive Important Videos
```
1. Curate list of important videos
2. Select "Best Quality"
3. Save URL list for future reference
4. Download with metadata
5. Backup files with complete metadata preserved
```

---

## 🎉 Changelog

### Version 2.1 (November 21, 2025)
- ✨ **NEW**: Auto embed YouTube thumbnail as cover art
- ✨ **NEW**: Auto add metadata (title, artist, date)
- 🎵 MP3 files with beautiful album art!
- 📱 Better music player integration
- 🎨 Perfect for music collections

### Version 2.0 (November 21, 2025)
- 🔇 Silent mode - no JS runtime warnings
- ⚡ Enhanced progress with speed & ETA
- 🔄 Retry failed downloads button
- 🗑️ Clear failed URLs button
- 📊 Real-time download statistics
- ⏱️ Elapsed time tracking
- 🎯 Success/fail counters

### Version 1.0 (Initial Release)
- 📥 Batch download functionality
- 🎬 Video quality selection
- 🎵 Audio-only mode
- 📝 URL management
- 🔢 Auto-numbering
- 🖥️ Flet GUI interface
- ⚡ Continue on error

---

## 📚 Additional Resources

- **Main Documentation**: [../README.md](../README.md)
- **Playlist Downloader**: [../yt-playlist-downloader/README.md](../yt-playlist-downloader/README.md)
- **FFmpeg Download**: https://ffmpeg.org/download.html
- **yt-dlp GitHub**: https://github.com/yt-dlp/yt-dlp

---

## 🤝 Contributing

Found a bug or have a feature request? Contributions welcome!

---

## 📄 License

Free to use and modify.

---

**Happy downloading! 🎉**

---

<a name="english"></a>
## 🇺🇸 English

Tool to download multiple individual YouTube videos at once.

### ✨ Features

- **Batch Download**: Download multiple individual videos
- **Multiple Quality Options**: Best, 720p, 480p
- **Audio-Only Mode**: Extract MP3 with album art
- **URL Management**: Load/save URL lists, retry failed
- **Auto Numbering**: Optional file numbering
- **Progress Tracking**: Real-time speed, ETA, statistics
- **Thumbnail & Metadata**: Auto-embed for media files
- **Modern GUI**: Flet-based responsive interface

### 🚀 Quick Start

```bash
# 1. Navigate to folder
cd yt-batch-downloader

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run GUI
python batch_downloader_gui_flet.py
```

For detailed documentation, see the Indonesian section above.


---

<a name="japanese"></a>
## 🇯🇵 日本語

複数の個別YouTube動画を一度にダウンロードするツール。

### ✨ 機能

- **バッチダウンロード**: 複数の個別動画をダウンロード
- **複数の品質オプション**: 最高品質、720p、480p
- **音声のみモード**: アルバムアート付きMP3抽出
- **URL管理**: URLリストの読み込み/保存、失敗の再試行
- **自動番号付け**: オプションのファイル番号付け
- **進行状況追跡**: リアルタイムの速度、ETA、統計
- **サムネイルとメタデータ**: メディアファイルへの自動埋め込み
- **モダンGUI**: Fletベースのレスポンシブインターフェース

### 🚀 クイックスタート

```bash
# 1. フォルダに移動
cd yt-batch-downloader

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. GUIを実行
python batch_downloader_gui_flet.py
```

詳細なドキュメントについては、上記のインドネシア語セクションを参照してください。
