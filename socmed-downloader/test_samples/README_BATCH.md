# 📦 Panduan Batch Download - SocMed Downloader

## 🎯 Apa itu Batch Download?

Batch Download memungkinkan kamu download **banyak video/audio sekaligus** dari **1 file** yang berisi daftar link!

**Keuntungan:**
- ⚡ Hemat waktu - tidak perlu paste link satu-satu
- 📝 Terorganisir - simpan daftar link sebagai arsip
- 🔄 Reusable - bisa download ulang kapan saja
- 🎛️ Flexible - set quality & format berbeda per link (CSV/JSON)

---

## 📋 Format File yang Didukung

### 1️⃣ TXT (Paling Simple!)

**Format:** 1 link per baris, komentar dimulai dengan `#`

**Contoh: `links.txt`**
```text
# Daftar Video Tutorial
https://www.youtube.com/watch?v=dQw4w9WgXcQ
https://www.youtube.com/watch?v=jNQXAC9IVRw

# TikTok videos
https://www.tiktok.com/@user/video/123
```

**Kapan pakai TXT?**
- ✅ Cuma butuh download simple (semua pakai quality sama)
- ✅ Link dari berbagai platform tercampur
- ✅ Paling cepat bikin manual

---

### 2️⃣ CSV (Dengan Metadata!)

**Format:** CSV dengan header `url,quality,format`

**Contoh: `links.csv`**
```csv
url,quality,format
https://www.youtube.com/watch?v=abc,1080,video
https://www.youtube.com/watch?v=def,720,video
https://www.youtube.com/watch?v=ghi,best,audio
```

**Kolom:**
- `url` - Link video/audio (WAJIB)
- `quality` - `best`/`1080`/`720`/`480` (optional, default: `best`)
- `format` - `video`/`audio` (optional, default: `video`)

**Kapan pakai CSV?**
- ✅ Butuh quality berbeda per link
- ✅ Mix video + audio downloads
- ✅ Bisa edit pakai Excel/Google Sheets

**Tips:**
- Buat di Excel → Save As → CSV
- Header `url,quality,format` harus ada baris pertama
- Kalau cuma ada kolom `url` saja, juga bisa (auto quality: best)

---

### 3️⃣ JSON (Structured Data)

**Format:** JSON object/array dengan metadata lengkap

**Contoh 1: Object dengan array `links`**
```json
{
  "links": [
    {
      "url": "https://youtube.com/watch?v=abc",
      "quality": "1080",
      "format": "video"
    },
    {
      "url": "https://tiktok.com/@user/video/123",
      "quality": "best"
    }
  ]
}
```

**Contoh 2: Simple array**
```json
[
  "https://youtube.com/watch?v=abc",
  "https://youtube.com/watch?v=def",
  "https://tiktok.com/@user/video/123"
]
```

**Kapan pakai JSON?**
- ✅ Generated otomatis dari script/API
- ✅ Butuh structure data kompleks
- ✅ Integration dengan tools lain

---

## 🚀 Cara Menggunakan

### Via GUI (Recommended)

1. **Buka GUI:**
   ```bash
   python socmed_downloader_gui.py
   ```
   Atau double-click: `launch_downloader.bat`

2. **Pilih Mode "Batch"** di radio button

3. **Klik "Pilih File"** → Select file TXT/CSV/JSON

4. **Set Quality & Format default** (untuk link yang tidak punya metadata)

5. **Klik "Download"** → Tunggu sampai selesai!

6. **Lihat Progress:**
   - Status akan update per link
   - Ada counter: "Processing 3/10"
   - Summary di akhir: "9 sukses, 1 gagal dari 10 file"

---

### Via CLI

1. **Jalankan CLI:**
   ```bash
   python socmed_downloader.py
   ```

2. **Pilih Option 2: Batch Download**

3. **Masukkan path file** (bisa drag-drop file ke terminal):
   ```
   >> Masukkan path file batch: C:\Downloads\links.txt
   ```

4. **Pilih format default:** Video (1) atau Audio (2)

5. **Pilih quality default** (untuk video):
   - 1: Terbaik (auto)
   - 2: 1080p
   - 3: 720p
   - 4: 480p

6. **Tunggu proses selesai!**
   - Progress ditampilkan per link
   - Summary di akhir

---

## 📝 Tips & Best Practices

### 1. Test dengan File Kecil Dulu
```text
# test_3links.txt
https://www.youtube.com/watch?v=abc
https://www.youtube.com/watch?v=def
https://www.youtube.com/watch?v=ghi
```
Download 3-5 link dulu untuk test sebelum batch ratusan link!

---

### 2. Pisahkan per Platform
```text
# youtube_videos.txt (YouTube aja)
# tiktok_videos.txt (TikTok aja)
# instagram_reels.txt (Instagram aja)
```
Lebih mudah troubleshoot kalau ada masalah!

---

### 3. Gunakan Quality 720p untuk Batch Besar
- 1080p/Best → File besar, lama download
- 720p → Balance (HD tapi ukuran wajar)
- 480p → File kecil, cepat (cocok untuk mobile)

**Rekomendasi:**
- Archive/Collection → Best
- Daily viewing → 720p
- Batch besar (>50 links) → 720p atau 480p

---

### 4. Check Disk Space!
Estimasi:
- 480p video: ~50-100 MB per video
- 720p video: ~150-300 MB per video
- 1080p video: ~300-600 MB per video
- Audio MP3: ~5-10 MB per file

Contoh: 100 video @720p = ~20-30 GB!

---

### 5. Backup File Batch
Simpan file TXT/CSV/JSON sebagai backup!
```
my_downloads/
  ├── batch_001_youtube.txt
  ├── batch_002_tiktok.csv
  └── batch_003_mixed.json
```

---

### 6. Gunakan CSV untuk Mixed Downloads
```csv
url,quality,format
https://youtube.com/music1,best,audio
https://youtube.com/music2,best,audio
https://youtube.com/tutorial,1080,video
https://tiktok.com/dance,720,video
```
Audio + Video dalam 1 batch!

---

## ❗ Troubleshooting

### "Tidak ada link valid ditemukan"
- Check format file (TXT/CSV/JSON)
- Pastikan URL lengkap dengan `https://`
- Pastikan tidak ada typo di URL

### "Error membaca file"
- CSV: Check ada header `url,quality,format`
- JSON: Validate syntax di https://jsonlint.com
- TXT: Check encoding UTF-8

### Beberapa Link Gagal
Normal! Mungkin:
- Link expired/dihapus
- Private video (butuh cookies)
- Platform restrict download
- Internet terputus sementara

Check summary di akhir untuk lihat mana yang gagal.

### Download Lambat
- Gunakan quality lebih rendah (720p/480p)
- Check internet connection
- Download di jam sepi (malam hari)

---

## 📊 Contoh Use Cases

### Use Case 1: Backup Channel Favorit
```text
# backup_channel_x.txt
https://youtube.com/watch?v=video1
https://youtube.com/watch?v=video2
https://youtube.com/watch?v=video3
# ... (200 videos)
```

### Use Case 2: Tutorial Series
```csv
url,quality,format
https://youtube.com/tutorial1,720,video
https://youtube.com/tutorial2,720,video
https://youtube.com/tutorial3,720,video
```

### Use Case 3: Music Collection
```csv
url,quality,format
https://youtube.com/song1,best,audio
https://youtube.com/song2,best,audio
https://youtube.com/song3,best,audio
```

### Use Case 4: Mixed Content dari API
```json
{
  "links": [
    {"url": "https://youtube.com/...", "quality": "1080"},
    {"url": "https://tiktok.com/...", "quality": "best"},
    {"url": "https://instagram.com/...", "quality": "720"}
  ]
}
```

---

## 🔗 Sample Files

Lihat folder `test_samples/` untuk contoh lengkap:
- **`links.txt`** - Simple text list dengan comments
- **`links.csv`** - CSV dengan metadata lengkap
- **`links.json`** - JSON structured data

Copy & edit sesuai kebutuhan!

---

## 📞 Support

Ada masalah? Check:
1. README.md utama untuk troubleshooting umum
2. File sample di `test_samples/`
3. Pastikan format file sesuai contoh

Happy Batch Downloading! 🎉
