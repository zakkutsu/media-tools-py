# 🎵 YouTube Playlist Downloader# 🎵 YouTube Playlist Downloader



Tool untuk mendownload **full playlist YouTube** dengan mudah dan otomatis. Mendukung download video dan audio dengan berbagai kualitas, auto-numbering, dan metadata lengkap.Tool untuk mendownload playlist YouTube dengan mudah dan otomatis menggunakan `yt-dlp`. Mendukung download video dan audio dengan berbagai kualitas.



## ✨ Features## ✨ Features



### Core Features- 📥 **Batch Download Playlist** - Download seluruh playlist sekaligus

- 📥 **Full Playlist Download** - Download seluruh playlist sekaligus- 🎬 **Multiple Video Quality** - Best quality, 720p, 480p (hemat kuota)

- 🎬 **Multiple Quality** - Best quality, 720p, 480p (hemat kuota)- 🎵 **Audio Only Mode** - Extract audio saja dalam format MP3

- 🎵 **Audio Only Mode** - Extract audio format MP3/M4A- 📝 **Auto Numbering** - File otomatis diberi nomor urut sesuai playlist

- 📝 **Auto Numbering** - File otomatis diberi nomor urut sesuai playlist- 🖥️ **GUI Interface** - Interface grafis yang user-friendly

- 📁 **Custom Naming** - Atur format nama file dengan template- ⚡ **Resume Download** - Lanjutkan download yang terputus

- 🖥️ **GUI Interface** - Interface grafis modern dengan Flet- 📁 **Custom Output** - Atur folder dan format nama file

- ⚡ **Resume Download** - Lanjutkan download yang terputus- 📊 **Progress Display** - Tampilkan persentase dan progress tiap lagu/video

- 📊 **Progress Display** - Progress per video dan overall- 🎨 **Embed Thumbnail** - YouTube thumbnail sebagai cover art/album art (NEW!)

- 📋 **Add Metadata** - Title, artist, date, description otomatis (NEW!)

### 🎨 NEW! Version 1.1 Features

- 🖼️ **Embed Thumbnail** - YouTube/Playlist thumbnail sebagai album art## 📋 Requirements

- 📋 **Add Metadata** - Title, artist, date, description otomatis

- 🎵 **Beautiful Music Files** - Audio dengan album art indah!- Python 3.7+

- yt-dlp (akan diinstall otomatis)

**Contoh hasil MP3:**- FFmpeg (untuk video processing)

```

01 - First Song.mp3## 🚀 Installation

├─ 🎨 Playlist thumbnail sebagai album art

├─ 📝 Title: "First Song"1. **Clone atau copy folder ini**

├─ 👤 Artist: "Channel Name"   ```bash

├─ 💿 Album: "Playlist Name"   cd media-tools/playlist-downloader

└─ 📅 Date: "2025-11-21"   ```

```

2. **Install dependencies**

---   ```bash

   pip install -r requirements.txt

## 📋 Requirements   ```



- Python 3.8+3. **Install FFmpeg** (jika belum ada)

- yt-dlp (auto-install via GUI)   - **Windows**: Download dari [ffmpeg.org](https://ffmpeg.org/download.html)

- FFmpeg (required untuk thumbnail embedding)   - **macOS**: `brew install ffmpeg`

   - **Ubuntu/Debian**: `sudo apt install ffmpeg`

---

## 🎯 Cara Penggunaan

## 🚀 Installation

### Method 1: GUI (Recommended)

### Via Main Launcher (Recommended)

```bashJalankan interface grafis:

# Dari folder media-tools```bash

python media_tools_launcher.pypython playlist_downloader_gui.py

# Pilih "YouTube Playlist Downloader"```

```

**Langkah-langkah:**

### Standalone1. Klik "Install/Update yt-dlp" jika belum terinstall

```bash2. Pilih folder download atau biarkan default

# 1. Navigate to folder3. Paste URL playlist YouTube

cd yt-playlist-downloader4. Klik "Get Info" untuk melihat jumlah video

5. Pilih jenis download (video/audio)

# 2. Install dependencies6. Klik "Start Download"

pip install -r requirements.txt

### Method 2: Command Line

# 3. Install FFmpeg

# Windows: choco install ffmpegJalankan via terminal:

# macOS: brew install ffmpeg```bash

# Linux: sudo apt install ffmpegpython playlist_downloader.py

```

# 4. Run

python playlist_downloader_gui_flet.pyProgram akan memandu Anda step-by-step.

```

### Method 3: Manual yt-dlp Commands

---

Berikut command manual yang bisa digunakan langsung:

## 🎯 Cara Penggunaan

#### Download Video (Kualitas Terbaik)

### GUI Interface```bash

yt-dlp -f "bv+ba/b" -o "%(playlist_index)s - %(title)s.%(ext)s" "URL_PLAYLIST"

**Launch:**```

```bash

python playlist_downloader_gui_flet.py#### Download Video (720p - Hemat Kuota)

``````bash

yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" -o "%(playlist_index)s - %(title)s.%(ext)s" "URL_PLAYLIST"

**Workflow:**```

1. **Install yt-dlp** (jika belum): Klik "Install/Update yt-dlp"

2. **Set Folder**: Pilih folder download atau gunakan default#### Download Audio Saja (MP3)

3. **Paste URL**: Masukkan URL playlist YouTube```bash

4. **Get Info**: Klik "Get Info" untuk lihat jumlah video di playlistyt-dlp -x --audio-format mp3 --audio-quality 0 -o "%(playlist_index)s - %(title)s.%(ext)s" "URL_PLAYLIST"

5. **Configure**:```

   - Pilih type: Video (best/720p/480p) atau Audio (MP3)

   - Set naming template (default sudah bagus)## � Progress Display

   - Enable/disable auto-numbering

6. **Download**: Klik "Start Download"Saat download playlist, Anda akan melihat progress yang jelas:

7. **Monitor**: Lihat progress overall dan per video

### **Video Download:**

### CLI Interface```

📥 [3/10] (30.0%) - Video ID: abc123

**Interactive mode:**──────────────────────────────────────────────────

```bash[download] Downloading item 3 of 10

python playlist_downloader.py[youtube] abc123: Downloading webpage

# Follow prompts step-by-step[info] abc123: Downloading 1 format(s): 401+251

```[download] 100% of 15.2MiB in 00:06

✅ Downloaded: Tutorial Python #3 - Functions

### Manual yt-dlp Commands```



**Video (Best Quality):**### **Audio Download:**

```bash```

yt-dlp -f "bv+ba/b" -o "%(playlist_index)s - %(title)s.%(ext)s" --embed-thumbnail --add-metadata "PLAYLIST_URL"🎵 [2/5] (40.0%) - Audio ID: song002

```─────────────────────────────────────────────

[download] Downloading item 2 of 5

**Video (720p):**[ExtractAudio] Destination: Song Title.mp3

```bash✅ Extracted: Song Title - Artist Name

yt-dlp -f "bestvideo[height<=720]+bestaudio/best[height<=720]" -o "%(playlist_index)s - %(title)s.%(ext)s" --embed-thumbnail --add-metadata "PLAYLIST_URL"```

```

**Progress Features:**

**Audio (MP3):**- 📊 **Clear Percentage** - `(30.0%)` untuk setiap item

```bash- 🔢 **Item Counter** - `[3/10]` current/total

yt-dlp -x --audio-format mp3 --audio-quality 0 -o "%(playlist_index)s - %(title)s.%(ext)s" --embed-thumbnail --add-metadata "PLAYLIST_URL"- 🎯 **Video/Audio ID** - Identifikasi file yang sedang didownload

```- 🧹 **Clean Output** - Filter warning dan verbose messages



---## �📂 Output Format



## 📊 Progress DisplayFile akan tersimpan dengan format:

```

**Playlist progress dengan detail lengkap:**01 - Judul Video Pertama.mp4

02 - Judul Video Kedua.mp4

```03 - Judul Video Ketiga.mp4

📊 Download Progress...

🎵 [3/10] (30.0%) - Amazing Song Title```



Playlist Progress:## ⚙️ Kustomisasi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 30%

### Template Nama File

Current Item Progress:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ (downloading...)Anda bisa mengubah format nama file dengan template berikut:

```

| Variable | Deskripsi |

**Informasi ditampilkan:**|----------|-----------|

- Current video/audio being downloaded| `%(playlist_index)s` | Nomor urut dalam playlist |

- Progress: [current/total] (percentage)| `%(title)s` | Judul video |

- Overall playlist progress bar| `%(ext)s` | Ekstensi file |

- Individual item progress| `%(uploader)s` | Nama channel |

- Status updates in log| `%(upload_date)s` | Tanggal upload |



---**Contoh template:**

```

## 🎵 Download Options"[%(playlist_index)s] %(title)s - %(uploader)s.%(ext)s"

```

### Video Quality

- **Best Quality** - Kualitas terbaik (1080p/4K jika tersedia)### Kualitas Video

- **720p** - HD quality, balance size & quality

- **480p** - SD quality, hemat bandwidth| Mode | Deskripsi |

|------|-----------|

### Audio Only (MP3)| `best` | Kualitas terbaik yang tersedia |

- **Format**: MP3| `720p` | Maksimal 720p (hemat bandwidth) |

- **Quality**: Best available| `480p` | Maksimal 480p (hemat bandwidth lebih) |

- **Features**:

  - ✅ Playlist thumbnail sebagai album art untuk semua lagu## 🔧 Troubleshooting

  - ✅ Metadata lengkap per lagu

  - ✅ Unified album look (semua lagu punya thumbnail sama)### "yt-dlp not found"

  - ✅ Perfect untuk music playlists```bash

pip install --upgrade yt-dlp

### File Naming Templates```



**Default (dengan auto-numbering):**### Download terputus/error

```- Jalankan command yang sama lagi, yt-dlp akan skip file yang sudah selesai

%(playlist_index)s - %(title)s.%(ext)s- Pastikan koneksi internet stabil

→ 01 - First Song.mp3- Coba update yt-dlp ke versi terbaru

→ 02 - Second Song.mp3

→ 03 - Third Song.mp3### Video tidak bisa didownload

```- Cek apakah playlist public/tidak private

- Beberapa video mungkin region-blocked

**Without auto-numbering:**- Update yt-dlp untuk bypass YouTube changes

```

%(title)s.%(ext)s### FFmpeg error

→ First Song.mp3- Pastikan FFmpeg sudah terinstall dan ada di PATH

→ Second Song.mp3- Test dengan: `ffmpeg -version`

→ Third Song.mp3

```## 📁 Struktur File



**Custom dengan uploader:**```

```playlist-downloader/

%(playlist_index)s - %(uploader)s - %(title)s.%(ext)s├── playlist_downloader.py      # Core functionality

→ 01 - ChannelName - First Song.mp3├── playlist_downloader_gui.py  # GUI interface

→ 02 - ChannelName - Second Song.mp3├── requirements.txt           # Dependencies

```└── README.md                 # Documentation (this file)

```

**Available variables:**

- `%(playlist_index)s` - Nomor urut dalam playlist## 🌟 Tips & Tricks

- `%(title)s` - Video/song title

- `%(ext)s` - File extension1. **Hemat Kuota**: Gunakan mode 720p atau 480p untuk menghemat bandwidth

- `%(uploader)s` - Channel name2. **Resume Download**: Jika download terputus, jalankan command yang sama - akan otomatis lanjut

- `%(upload_date)s` - Upload date3. **Batch Multiple Playlists**: Buat script untuk loop multiple URLs

- `%(playlist)s` - Playlist name4. **Folder Organization**: Buat folder terpisah untuk setiap playlist

- `%(playlist_id)s` - Playlist ID

## ⚠️ Disclaimer

---

Tool ini hanya untuk penggunaan personal dan educational. Pastikan Anda mematuhi:

## 💡 Tips & Best Practices- Terms of Service YouTube

- Copyright laws di negara Anda

### For Music Playlists- Hak cipta content creator

- ✅ **Use Audio Only (MP3)** untuk music playlists

- ✅ **Enable auto-numbering** untuk maintain track order## 🤝 Support

- ✅ Semua songs akan dapat **same playlist thumbnail** sebagai album art

- ✅ Perfect untuk compilation albums atau curated playlistsJika ada masalah atau pertanyaan:

- ✅ File size jauh lebih kecil dari video1. Cek troubleshooting section di atas

2. Update yt-dlp ke versi terbaru

### For Video Playlists3. Pastikan koneksi internet stabil

- ✅ **720p recommended** untuk tutorial series - good balance

- ✅ **Best quality** untuk archiving important playlists## 🎨 New Feature: Thumbnail & Metadata Embedding

- ✅ **480p** untuk mobile viewing atau slow internet

- ✅ Enable auto-numbering untuk episode orderSemua download sekarang otomatis menyertakan:

- **🖼️ Thumbnail Embedding**: YouTube thumbnail sebagai cover art (untuk audio) atau embedded thumbnail (untuk video)

### Naming Strategy- **📝 Metadata**: Title, artist (channel name), date, description otomatis ditambahkan

- ✅ Keep default template `%(playlist_index)s - %(title)s.%(ext)s`

- ✅ Auto-numbering ensures correct order**Contoh hasil MP3:**

- ✅ Titles are cleaned automatically (invalid chars removed)```

- ✅ For long titles, yt-dlp auto-truncatesSong.mp3

├─ 🎨 Cover art dari thumbnail YouTube

### Performance├─ 📝 Title: "Song Name"

- ✅ Large playlists (50+ videos): Monitor progress, can take hours├─ � Artist: "Channel Name"

- ✅ Download saat network stabil└─ 📅 Date: "2025-11-21"

- ✅ Resume functionality: Re-run command akan skip yang sudah downloaded```

- ✅ Check disk space before downloading large playlists

Lihat dokumentasi lengkap di [METADATA_THUMBNAIL_FEATURE.md](../METADATA_THUMBNAIL_FEATURE.md)

---

## �📝 Changelog

## 🎨 Playlist Thumbnail & Metadata

### Version 1.1 (November 21, 2025)

### What Gets Added?- ✨ **NEW**: Auto embed YouTube thumbnail as cover art

- ✨ **NEW**: Auto add metadata (title, artist, date, description)

**For Audio Files (MP3/M4A):**- 🎵 MP3 files now have beautiful album art!

- 🖼️ **Album Art**: Playlist thumbnail (semua lagu dapat thumbnail yang sama!)- 📱 Better integration with music players

- 📝 **Title**: Song title

- 👤 **Artist**: Channel name### Version 1.0

- 💿 **Album**: Playlist name- ✅ Basic playlist download functionality

- 📅 **Date**: Upload date- ✅ GUI interface with tkinter

- 🔢 **Track Number**: Playlist index- ✅ Multiple quality options

- 💬 **Comment**: Video description- ✅ Audio-only mode

- ✅ Auto-numbering files

**For Video Files:**- ✅ Resume capability
- 🖼️ **Thumbnail**: Embedded in container
- 📝 **Metadata**: Title, artist, date, description
- 🏷️ **Tags**: Playlist info preserved

### Unified Album Look

**Music Playlist Download Result:**
```
My Music Playlist/
├── 01 - Song One.mp3    [🎨 Playlist thumbnail]
├── 02 - Song Two.mp3    [🎨 Same thumbnail]
├── 03 - Song Three.mp3  [🎨 Same thumbnail]
├── 04 - Song Four.mp3   [🎨 Same thumbnail]
└── ...

Music Player View:
┌─────────────────────────────────┐
│  My Music Playlist              │
│  ┌───────────────┐              │
│  │  📀 Playlist  │              │
│  │   Thumbnail   │              │
│  └───────────────┘              │
│  ▶ 01 - Song One                │
│  ▶ 02 - Song Two                │
│  ▶ 03 - Song Three              │
│  ▶ 04 - Song Four               │
└─────────────────────────────────┘
```

### Music Player Compatibility
- ✅ Windows Media Player
- ✅ VLC Media Player
- ✅ iTunes / Apple Music
- ✅ Spotify (local files)
- ✅ Foobar2000
- ✅ MusicBee
- ✅ AIMP
- ✅ Android Music Players
- ✅ iOS Music App
- ✅ Plex / Jellyfin

---

## 🔧 Troubleshooting

### Issue: "yt-dlp not found"
**Solution:**
1. Klik "Install/Update yt-dlp" di GUI
2. Tunggu proses selesai
3. Coba download lagi

### Issue: "Failed to get playlist info"
**Solution:**
- Check playlist URL valid (paste di browser)
- Pastikan playlist public (not private)
- Check internet connection
- Update yt-dlp

### Issue: "Some videos skipped"
**Possible reasons:**
- Private/deleted videos in playlist (normal)
- Age-restricted videos
- Region-blocked videos
- Check log untuk detail

### Issue: "No thumbnail in MP3s"
**Solution:**
1. Install FFmpeg: https://ffmpeg.org/download.html
2. Pastikan FFmpeg di PATH
3. Update yt-dlp: `python -m pip install -U yt-dlp`
4. Re-download playlist

### Issue: "Download very slow"
**Possible causes:**
- Large playlist (many videos)
- High quality selected (large files)
- Internet connection slow
- YouTube throttling

**Solutions:**
- Select lower quality (720p atau 480p)
- Download during off-peak hours
- Check internet speed
- Resume later if interrupted

### Issue: "Incomplete playlist download"
**Solution:**
1. Re-run same command
2. yt-dlp automatically skips already downloaded files
3. Only downloads remaining videos
4. Check failed videos in log

---

## 📊 Example Workflows

### Workflow 1: Music Album/Compilation
```
Goal: Download music playlist sebagai MP3 album

1. Find music playlist URL
2. Open Playlist Downloader GUI
3. Paste URL → Get Info (verify video count)
4. Select "Audio Only (MP3)"
5. Keep auto-numbering enabled
6. Download
7. Result: Complete album dengan:
   - Unified album art (playlist thumbnail)
   - Track numbers (01, 02, 03...)
   - All metadata included
   - Ready untuk music player!
```

### Workflow 2: Tutorial/Course Series
```
Goal: Download tutorial playlist untuk offline viewing

1. Get playlist URL dari course
2. Open Playlist Downloader
3. Paste URL → Get Info
4. Select "720p" (good balance)
5. Use template: %(playlist_index)s - %(title)s.%(ext)s
6. Download
7. Result: Numbered tutorial videos, easy to follow in order
```

### Workflow 3: Podcast Series
```
Goal: Download podcast playlist sebagai audio

1. Find podcast playlist
2. Playlist Downloader → Audio Only
3. Auto-numbering enabled
4. Download
5. Result: Episodic audio files with episode art
```

---

## 🎉 Changelog

### Version 1.1 (November 21, 2025)
- ✨ **NEW**: Auto embed playlist thumbnail as album art
- ✨ **NEW**: Auto add comprehensive metadata
- 🎵 Unified album look untuk music playlists!
- 💿 Track numbers and album info included
- 📱 Perfect music player integration

### Version 1.0 (Initial Release)
- 📥 Full playlist download
- 🎬 Multiple quality options
- 🎵 Audio-only mode
- 📝 Auto-numbering
- 📁 Custom naming templates
- 🖥️ Flet GUI interface
- ⚡ Resume capability
- 📊 Progress tracking

---

## 📚 Additional Resources

- **Main Documentation**: [../README.md](../README.md)
- **Batch Downloader**: [../yt-batch-downloader/README.md](../yt-batch-downloader/README.md)
- **FFmpeg Download**: https://ffmpeg.org/download.html
- **yt-dlp GitHub**: https://github.com/yt-dlp/yt-dlp

---

## 🤝 Contributing

Found a bug or have a feature request? Contributions welcome!

---

## 📄 License

Free to use and modify.

---

**Happy playlist downloading! 🎉**
