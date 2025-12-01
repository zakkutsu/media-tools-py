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

### Via GUI
```bash
python media_looper_gui.py
```
1. Pilih file (atau drag & drop)
2. Masukkan jumlah loop (contoh: 60)
3. Klik "Process"
4. File output: `filename_looped_60x.ext`

### Via CLI
```bash
python loop_media.py
```
- Interaktif: masukkan path dan jumlah loop
- Output otomatis di folder yang sama

## ⚡ Contoh Kasus

### Background Music 1 Jam
```
Input:  lagu.mp3 (3 menit)
Loop:   20x
Output: lagu_looped_20x.mp3 (60 menit)
Waktu:  ~2 detik
```

### Video Loop
```
Input:  clip.mp4 (10 detik)
Loop:   360x
Output: clip_looped_360x.mp4 (1 jam)
Waktu:  ~5 detik
```

## 🔧 Technical Details

### FFmpeg Loop Logic
```python
# User berpikir: "60x total"
# FFmpeg menghitung: "1 original + 59 repeats"
ffmpeg_loop_count = user_input - 1
```

### Supported Formats
- **Video**: MP4, MKV, AVI, MOV, WebM, FLV
- **Audio**: MP3, WAV, AAC, FLAC, M4A, OGG

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

Konsep yang dipelajari:
- Binary file manipulation
- Container vs Codec
- Subprocess management
- System automation
- Performance optimization

---

**Tip Pro**: Tool ini menggunakan `-stream_loop` (FFmpeg flag), bukan Python loop. Ini jauh lebih efisien karena bekerja di level binary, bukan pixel-by-pixel processing.
