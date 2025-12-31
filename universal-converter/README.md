# 🔄 Universal File Converter

**The Ultimate Smart Converter** - Convert gambar, video, audio, dan PDF dengan logika pintar yang mencegah konversi yang tidak masuk akal.

## ✨ Fitur Utama

### 🎯 Smart Format Detection
Aplikasi ini menggunakan **Dictionary Mapping Logic** untuk memastikan hanya opsi konversi yang valid yang ditampilkan:
- Pilih **foto.png** → Opsi: JPG, WEBP, PDF, ICO, BMP
- Pilih **video.mp4** → Opsi: MP3 (Audio), GIF, MKV, AVI
- Pilih **dokumen.pdf** → Opsi: JPG (Per Halaman), PNG (Per Halaman)

### 🖼️ Image Conversion
- **Format Support:** JPG, PNG, WEBP, BMP, ICO, PDF
- **Auto Transparency Handling:** Konversi PNG transparan ke JPG otomatis diberi background putih
- **Quality Preserved:** Mempertahankan kualitas gambar optimal

### 🎬 Video Conversion
- **Format Support:** MP4, MKV, AVI, MOV
- **Extract Audio:** Ambil audio dari video (MP3, WAV)
- **Create GIF:** Convert video ke animasi GIF (optimized)
- **Powered by:** FFmpeg

### 🎵 Audio Conversion
- **Format Support:** MP3, WAV, OGG, M4A, FLAC
- **Bitrate Control:** 192k bitrate untuk MP3
- **High Quality:** Preservasi kualitas audio

### 📄 PDF to Image
- **Multi-Page Support:** Setiap halaman PDF jadi file gambar terpisah
- **Smart Naming:** `dokumen_page_1.png`, `dokumen_page_2.png`
- **Output Format:** JPG atau PNG
- **Powered by:** Poppler

## 📋 Requirements

### Python Libraries
```bash
pip install flet Pillow pdf2image
```

### External Tools (Wajib)

#### 1. FFmpeg (Untuk Video/Audio)
- **Download:** [FFmpeg Windows Build](https://github.com/BtbN/FFmpeg-Builds/releases)
- Pilih: `ffmpeg-master-latest-win64-gpl.zip`
- Extract dan ambil file `ffmpeg.exe`
- Taruh `ffmpeg.exe` di folder `universal-converter/`

#### 2. Poppler (Untuk PDF)
- **Download:** [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
- Pilih: `Release-XX.XX.X-0.zip` (versi terbaru)
- Extract seluruh isi
- Rename folder menjadi `poppler`
- Taruh folder `poppler/` di folder `universal-converter/`

## 📁 Struktur Folder Final

```
universal-converter/
│
├── universal_converter_gui.py   (Script utama)
├── ffmpeg.exe                   (Download dari FFmpeg)
├── poppler/                     (Extract dari Poppler ZIP)
│   └── Library/
│       └── bin/                 (Berisi pdftoppm.exe, dll)
│           ├── pdftoppm.exe
│           ├── pdfinfo.exe
│           └── ...
│
└── README.md                    (Dokumentasi ini)
```

## 🚀 Cara Menggunakan

### Langkah 1: Setup Environment
```bash
# Dari root project media-tools-py
cd universal-converter

# Install dependencies
pip install -r requirements.txt
```

### Langkah 2: Download Tools
1. Download **FFmpeg** → Copy `ffmpeg.exe` ke folder ini
2. Download **Poppler** → Extract dan rename jadi `poppler/`, taruh di sini

### Langkah 3: Jalankan Aplikasi
```bash
python universal_converter_gui.py
```

### Langkah 4: Convert File
1. Klik **"Pilih File"**
2. Pilih file yang ingin dikonversi
3. Aplikasi otomatis menampilkan format output yang valid
4. Pilih format tujuan dari dropdown
5. Klik **"MULAI KONVERSI"**
6. File hasil akan tersimpan di folder yang sama dengan file input

## 🎨 Format Support Matrix

| Input Format | Output Options | Engine |
|-------------|----------------|--------|
| JPG/PNG | PNG, JPG, WEBP, PDF, ICO, BMP | Pillow |
| WEBP | JPG, PNG, PDF | Pillow |
| BMP | JPG, PNG, WEBP | Pillow |
| ICO | PNG, JPG | Pillow |
| PDF | JPG (Per Page), PNG (Per Page) | Poppler + Pillow |
| MP4 | MP3, WAV, MKV, GIF, AVI | FFmpeg |
| MKV | MP4, MP3, AVI | FFmpeg |
| AVI/MOV | MP4, MKV, MP3 | FFmpeg |
| MP3/WAV | WAV, MP3, OGG, M4A, FLAC | FFmpeg |
| M4A/OGG | MP3, WAV, OGG | FFmpeg |
| FLAC | MP3, WAV, OGG | FFmpeg |

## ⚙️ Fitur Khusus

### Auto-Transparency Handling
```python
# PNG dengan alpha channel → JPG
# Otomatis convert ke RGB mode (background putih)
if img.mode in ("RGBA", "P"):
    img = img.convert("RGB")
```

### Video to GIF Optimization
```python
# Otomatis resize dan optimize FPS
cmd.extend(['-vf', 'fps=10,scale=320:-1'])
```

### Audio Extraction from Video
```python
# Remove video stream, keep audio only
cmd.extend(['-vn', '-ab', '192k'])
```

### PDF Multi-Page Handling
```python
# Setiap halaman PDF jadi file terpisah
for i, img in enumerate(images):
    page_name = f"{name_only}_page_{i+1}.png"
```

## 🐛 Troubleshooting

### Error: "FFmpeg tidak ditemukan"
- Pastikan `ffmpeg.exe` ada di folder `universal-converter/`
- Test di terminal: `.\ffmpeg.exe -version`

### Error: "Poppler tidak ditemukan"
- Pastikan struktur folder benar: `poppler/Library/bin/`
- Cek apakah ada file `pdftoppm.exe` di dalam folder `bin/`

### Error: "Module not found: pdf2image"
```bash
pip install pdf2image
```

### Error: "Module not found: PIL"
```bash
pip install Pillow
```

### Konversi PDF Lambat
- Normal untuk PDF besar dengan banyak halaman
- Setiap halaman diproses satu per satu

### Video Output Tidak Ada Suara
- Pastikan video input memiliki audio track
- Cek format audio codec kompatibel

## 💡 Tips & Tricks

1. **Batch Processing:** Saat ini satu file per waktu. Untuk batch, jalankan aplikasi multiple times.
2. **Quality Control:** Untuk image, output quality mengikuti default Pillow (high quality).
3. **File Size:** GIF hasil konversi sudah di-optimize (320px width, 10fps).
4. **PDF Pages:** Nama file output akan berurutan: `_page_1`, `_page_2`, dst.

## 🔧 Technical Details

### Dependencies
- **Flet:** Modern GUI framework
- **Pillow (PIL):** Image processing
- **pdf2image:** PDF to image conversion (wrapper untuk Poppler)
- **FFmpeg:** Video/Audio processing
- **Poppler:** PDF rendering engine

### Thread Safety
Konversi berjalan di background thread untuk prevent UI freeze:
```python
t = threading.Thread(target=process_conversion, daemon=True)
t.start()
```

### Error Handling
- Try-catch untuk setiap engine (Pillow, FFmpeg, Poppler)
- User-friendly error messages
- Status updates real-time

## 📝 License

Part of **Media Tools Python** project.

## 🤝 Contributing

Contributions welcome! Format tambahan yang ingin didukung:
- [ ] TIFF support
- [ ] SVG to PNG
- [ ] HEIC to JPG
- [ ] Excel/Word to PDF

---

**Developed with ❤️ using Python + Flet**
