# 📥 Setup Guide - Universal File Converter

Panduan lengkap untuk setup **FFmpeg** dan **Poppler** yang dibutuhkan untuk menjalankan Universal Converter.

---

## 🎯 Quick Start Checklist

- [ ] Install Python dependencies (`pip install -r requirements.txt`)
- [ ] Download dan setup FFmpeg
- [ ] Download dan setup Poppler
- [ ] Verifikasi struktur folder
- [ ] Test run aplikasi

---

## 📦 Part 1: Python Dependencies

### Install via pip

```bash
# Pastikan kamu di folder universal-converter
cd universal-converter

# Install semua dependencies
pip install -r requirements.txt
```

### Manual Installation
Jika ada masalah dengan requirements.txt:
```bash
pip install flet
pip install Pillow
pip install pdf2image
```

### Verifikasi Installation
```bash
python -c "import flet; import PIL; import pdf2image; print('✅ Semua library terinstall!')"
```

---

## 🎬 Part 2: Setup FFmpeg (Untuk Video/Audio)

### Mengapa Butuh FFmpeg?
FFmpeg adalah **mesin konversi video/audio** paling powerful. Tanpa ini, kamu tidak bisa convert file MP4, MP3, dll.

### Langkah Download & Setup

#### 1. Download FFmpeg
Kunjungi: **https://github.com/BtbN/FFmpeg-Builds/releases**

Pilih file:
- **Nama:** `ffmpeg-master-latest-win64-gpl.zip`
- **Size:** ~100MB

#### 2. Extract File
- Extract file ZIP yang sudah didownload
- Kamu akan melihat folder dengan nama panjang seperti: `ffmpeg-master-latest-win64-gpl`

#### 3. Cari file ffmpeg.exe
Masuk ke dalam folder:
```
ffmpeg-master-latest-win64-gpl/
└── bin/
    ├── ffmpeg.exe    ← AMBIL FILE INI
    ├── ffplay.exe
    └── ffprobe.exe
```

#### 4. Copy ke Folder Project
Copy **HANYA** file `ffmpeg.exe` ke:
```
C:\project\media-tools-py\universal-converter\ffmpeg.exe
```

#### 5. Test FFmpeg
Buka PowerShell di folder `universal-converter`, lalu:
```powershell
.\ffmpeg.exe -version
```

Jika muncul informasi versi FFmpeg, berarti **SUKSES!** ✅

---

## 📄 Part 3: Setup Poppler (Untuk PDF)

### Mengapa Butuh Poppler?
Poppler adalah **engine untuk render PDF**. Library Python `pdf2image` butuh ini untuk bisa convert PDF jadi gambar.

### Langkah Download & Setup

#### 1. Download Poppler
Kunjungi: **https://github.com/oschwartz10612/poppler-windows/releases/**

Pilih file terbaru:
- **Nama:** `Release-XX.XX.X-0.zip` (contoh: `Release-24.02.0-0.zip`)
- **Size:** ~30MB

#### 2. Extract File
Extract file ZIP. Kamu akan melihat folder dengan nama panjang seperti:
```
poppler-XX.XX.X/
```

#### 3. Rename Folder
**PENTING:** Rename folder ini menjadi hanya `poppler`

Sebelum:
```
poppler-24.02.0/
```

Sesudah:
```
poppler/
```

#### 4. Verifikasi Struktur
Pastikan di dalam folder `poppler` ada struktur seperti ini:
```
poppler/
└── Library/
    └── bin/
        ├── pdftoppm.exe    ← FILE PENTING
        ├── pdfinfo.exe
        ├── pdftocairo.exe
        └── (banyak file .exe lainnya)
```

#### 5. Move ke Folder Project
Pindahkan **SELURUH** folder `poppler/` ke:
```
C:\project\media-tools-py\universal-converter\poppler\
```

#### 6. Test Poppler
Buka PowerShell di folder `universal-converter`, lalu:
```powershell
.\poppler\Library\bin\pdftoppm.exe -v
```

Jika muncul informasi versi Poppler, berarti **SUKSES!** ✅

---

## ✅ Part 4: Verifikasi Final

### Cek Struktur Folder
Folder `universal-converter` harus terlihat seperti ini:

```
universal-converter/
│
├── universal_converter_gui.py   ✅ Script Python
├── requirements.txt             ✅ Dependencies list
├── README.md                    ✅ Dokumentasi
├── SETUP_GUIDE.md              ✅ File ini
│
├── ffmpeg.exe                   ✅ FFmpeg executable (100MB+)
│
└── poppler/                     ✅ Folder Poppler
    └── Library/
        └── bin/
            ├── pdftoppm.exe     ✅
            ├── pdfinfo.exe      ✅
            └── ...
```

### Test Run Aplikasi
```bash
python universal_converter_gui.py
```

Jika aplikasi terbuka dengan GUI Flet, **SETUP SELESAI!** 🎉

---

## 🔥 Quick Setup (Copy-Paste Commands)

Jika kamu sudah download FFmpeg dan Poppler, jalankan ini di PowerShell:

```powershell
# Masuk ke folder project
cd C:\project\media-tools-py\universal-converter

# Install Python dependencies
pip install -r requirements.txt

# Test FFmpeg (pastikan sudah ada ffmpeg.exe di folder ini)
.\ffmpeg.exe -version

# Test Poppler (pastikan sudah ada folder poppler/)
.\poppler\Library\bin\pdftoppm.exe -v

# Jalankan aplikasi
python universal_converter_gui.py
```

---

## 🐛 Troubleshooting

### "ffmpeg.exe is not recognized"
**Solusi:**
- Pastikan file `ffmpeg.exe` ada di folder `universal-converter/`
- Cek nama file: harus persis `ffmpeg.exe` (huruf kecil semua)
- Jangan taruh di subfolder

### "Poppler not found"
**Solusi:**
- Pastikan folder bernama `poppler` (bukan `poppler-24.02.0`)
- Cek struktur: `poppler/Library/bin/pdftoppm.exe` harus ada
- Path di kode Python: `POPPLER_BIN_PATH = os.path.join(base_dir, "poppler", "Library", "bin")`

### "Permission Denied" saat extract
**Solusi:**
- Run as Administrator
- Extract ke lokasi lain dulu, baru copy

### "Module 'pdf2image' not found"
**Solusi:**
```bash
pip install --upgrade pdf2image
```

### Download Link Tidak Bisa Dibuka
**Alternatif:**
- **FFmpeg:** https://www.gyan.dev/ffmpeg/builds/ (Pilih `ffmpeg-release-essentials.zip`)
- **Poppler:** https://blog.alivate.com.au/poppler-windows/ (Pilih versi latest)

---

## 📊 File Size Reference

| Component | Size | Notes |
|-----------|------|-------|
| `ffmpeg.exe` | ~100MB | Essential untuk video/audio |
| `poppler/` folder | ~30MB | Essential untuk PDF |
| Python libraries | ~50MB | Via pip install |

**Total Storage Needed:** ~200MB

---

## 🎓 Understanding the Architecture

### Workflow Konversi

```
User Input
    ↓
[File Picker] → Deteksi ekstensi → Cek FORMAT_MAP
    ↓
Tampilkan opsi valid
    ↓
User pilih format output
    ↓
┌─────────────────┬──────────────────┬─────────────────┐
│                 │                  │                 │
│   IMAGE         │    VIDEO/AUDIO   │      PDF        │
│  (Pillow)       │    (FFmpeg)      │   (Poppler)     │
│                 │                  │                 │
└────────┬────────┴────────┬─────────┴────────┬────────┘
         │                 │                  │
         └─────────────────┴──────────────────┘
                          ↓
                   Output File(s)
```

### Engine Mapping

| File Type | Engine | Executable Needed |
|-----------|--------|-------------------|
| JPG, PNG, WEBP, BMP | Pillow (Python) | ❌ No |
| MP4, MP3, MKV, WAV | FFmpeg | ✅ ffmpeg.exe |
| PDF | Poppler + Pillow | ✅ poppler/ folder |

---

## 🚀 Next Steps

Setelah setup selesai:

1. **Baca [README.md](README.md)** untuk panduan penggunaan
2. **Test konversi** berbagai format
3. **Report bugs** jika ada masalah

---

## 💬 Need Help?

Jika masih ada masalah:
1. Cek ulang struktur folder (paling sering error di sini)
2. Pastikan semua dependencies ter-install
3. Coba restart terminal/PowerShell
4. Check file permissions (Read/Write access)

**Happy Converting!** 🎉
