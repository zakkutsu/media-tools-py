# Media Looper Tool

**Tool untuk mengulang video/audio tanpa re-encoding (Stream Copy)**

## 🎯 Kegunaan
- Loop video/audio N kali **tanpa quality loss**
- Proses **super cepat** (detikan untuk hasil berjam-jam)
- Ideal untuk:
  - Background music loop
  - Video test pattern
  - Presentation materials
  - Content repetition

## 🧠 Computer Science Concept

### Rendering vs Stream Copy

**Cara Pemula (Re-encoding):**
```
Input → Decode → Process → Re-encode → Output
⏱️  Waktu: LAMA (tergantung CPU/GPU)
📉 Quality: BERKURANG (lossy compression)
```

**Cara Programmer (Stream Copy):**
```
Input → Binary Concatenation → Output
⏱️  Waktu: INSTANT (hanya copy data)
✅ Quality: IDENTIK (lossless)
```

### Teknik yang Digunakan
- **FFmpeg `-stream_loop`**: Manipulasi di level container, bukan pixel
- **Stream Copy (`-c copy`)**: Zero re-encoding
- **Binary Concatenation**: Menjahit data mentah tanpa processing

## 📝 Penggunaan

### Via GUI (Flet - Modern Interface) 🎨
```bash
python media_looper_gui_flet.py
```
**Features:**
- 🎯 **Tab-based UI**: Single Loop & Alternating Loop
- 📊 **Duration Calculator**: Preview output duration
- 🚀 **Quick Presets**: 10x, 20x, 30x, 60x, 120x buttons
- 📝 **Real-time Log**: Monitor processing status
- 🎨 **Modern Design**: Clean Flet interface

**Tab 1: Single Loop**
1. Select file
2. Enter loop count (or use quick presets)
3. Click Process
4. Output: `filename_looped_60x.ext`

**Tab 2: Alternating Loop** 🔥
1. Select File A and File B
2. Enter loop count (sets)
3. Click Process
4. Output: `filenameA_merged_10x.ext`

### Via CLI (Interactive Menu)
```bash
python media_looper_cli.py
```

**Mode 1: Single Loop**
- Loop 1 file berkali-kali (A-A-A...)
- Instant processing dengan stream copy

**Mode 2: Alternating Loop** 🔥
- Loop 2 file bergantian (A-B-A-B-A-B...)
- Ideal untuk:
  - Intro + Content loop (intro-video-intro-video)
  - Music + Silence pattern
  - Question + Answer repetition
- Teknik: FFmpeg Concat Demuxer

## ⚡ Contoh Kasus

### Use Case 1: Background Music 1 Jam (Single Loop)
```
Input:  lagu.mp3 (3 menit)
Loop:   20x
Output: lagu_looped_20x.mp3 (60 menit)
Waktu:  ~2 detik
```

### Use Case 2: Video Loop (Single Loop)
```
Input:  clip.mp4 (10 detik)
Loop:   360x
Output: clip_looped_360x.mp4 (1 jam)
Waktu:  ~5 detik
```

### Use Case 3: Intro + Video Pattern (Alternating Loop) ⭐
```
File A: intro.mp4 (5 detik bumper)
File B: content.mp4 (30 detik video)
Loop:   10 sets
Output: intro_merged_looped_10x.mp4 (350 detik = 5:50)
Pattern: intro → content → intro → content ... (10x)
Waktu:  ~3 detik
```

### Use Case 4: Music + Silence (Alternating Loop)
```
File A: music.mp3 (1 menit)
File B: silence.mp3 (30 detik)
Loop:   20 sets
Output: music_merged_looped_20x.mp3 (30 menit)
Pattern: Musik 1 menit, jeda 30 detik, repeat
```

## 🔧 Technical Details

### Single Loop: Stream Loop Technique
```python
# User berpikir: "60x total"
# FFmpeg menghitung: "1 original + 59 repeats"
ffmpeg_loop_count = user_input - 1

cmd = ['ffmpeg', '-stream_loop', '59', '-i', 'input.mp4', '-c', 'copy', 'output.mp4']
```

### Alternating Loop: Concat Demuxer Technique
```python
# 1. Python generates temporary list file
with open('list.txt', 'w') as f:
    for i in range(loop_count):
        f.write(f"file '{path_a}'\n")
        f.write(f"file '{path_b}'\n")

# 2. FFmpeg reads list and concatenates
cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', 'output.mp4']
```

**Kenapa Concat Demuxer?**
- Menghindari command line terlalu panjang (Windows limit: ~8000 chars)
- FFmpeg membaca file list baris per baris
- Lebih efisien untuk batch processing dalam jumlah besar
- Stream copy tetap dipakai = FAST!

### Supported Formats
- **Video**: MP4, MKV, AVI, MOV, WebM, FLV
- **Audio**: MP3, WAV, AAC, FLAC, M4A, OGG

### Compatibility Warning (Alternating Mode)
⚠️ Untuk alternating loop, kedua file **HARUS** memiliki:
- Format container yang sama (MP4-MP4, MP3-MP3)
- Codec yang identik (H.264-H.264, AAC-AAC)
- Resolusi yang sama (1080p-1080p)

Jika berbeda → gunakan re-encoding (lebih lama tapi aman)

## 📋 Requirements
- Python 3.7+
- FFmpeg (harus ada di system PATH)
- tkinterdnd2 (untuk drag & drop GUI)

## ⚠️ Catatan Penting

1. **Container Compatibility**: Input harus valid container format
2. **No Quality Loss**: Stream copy = identical quality
3. **File Size**: Output = Input × Loop Count (logical)
4. **Speed**: Processing time ≈ 1-5 detik (tidak tergantung durasi total)

## 🎓 Educational Value

### Konsep CS yang Dipelajari:

**1. Binary File Manipulation**
- Stream copy bekerja di level binary data
- Tidak ada decoding/encoding → instant processing

**2. Container vs Codec**
- Container: "Kotak" penyimpan (MP4, MKV)
- Codec: "Isi" nya (H.264, AAC)
- Stream copy = copy container tanpa decode isi

**3. Algorithm Design**
- Single loop: Direct FFmpeg flag
- Alternating: List generation algorithm

**4. Concat Demuxer Technique**
- Python generates text file dengan daftar input
- FFmpeg reads & concatenates sequentially
- Menghindari command line length limitation

**5. Performance Optimization**
- Stream copy vs Re-encoding: 100x+ faster
- Batch processing dengan temp file
- Memory-efficient (tidak load ke RAM)

**6. System Programming**
- Subprocess management
- Temporary file handling
- Path normalization (Windows/Linux compatibility)

---

**Tip Pro**: 
- **Single loop**: Gunakan `-stream_loop` untuk 1 file (simplest)
- **Alternating loop**: Gunakan concat demuxer untuk 2+ files (scalable)
- Kedua teknik menggunakan stream copy = INSTANT processing!
