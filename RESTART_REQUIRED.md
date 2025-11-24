# 🚨 PENTING - CARA MELIHAT PERUBAHAN TRANSLATION

## Masalah yang Anda Alami:
Screenshot menunjukkan text dengan underscore seperti:
- `format_video` (seharusnya "Video (MP4)")
- `format_audio` (seharusnya "Audio (MP3)")  
- `quality_best` (seharusnya "Terbaik (Otomatis)")
- `cookies_none` (seharusnya "Tidak Pakai")

## Penyebab:
Aplikasi yang sedang berjalan menggunakan versi LAMA dari `language_config.py` 
yang di-cache oleh Python saat aplikasi pertama kali dijalankan.

## Solusi - WAJIB RESTART:

### Cara 1: Restart Lengkap (RECOMMENDED)
```bash
# 1. TUTUP aplikasi yang sedang berjalan (klik X atau Ctrl+C di terminal)
# 2. Jalankan ulang dari awal:
python media_tools_launcher.py
```

### Cara 2: Jika dijalankan dari launcher lain
```bash
# 1. Tutup semua window aplikasi media-tools
# 2. Tutup terminal/command prompt yang menjalankan
# 3. Buka terminal baru
# 4. Jalankan ulang aplikasi
```

## ✅ Verifikasi Berhasil:
Setelah restart, Anda seharusnya melihat:
- ✅ "🎬 Video (MP4)" bukan "🎬 format_video"  
- ✅ "🎵 Audio (MP3)" bukan "🎵 format_audio"
- ✅ "Terbaik (Otomatis)" bukan "quality_best"
- ✅ "Tidak Pakai" bukan "cookies_none"
- ✅ "Pilih Kualitas:" bukan "quality_label"
- ✅ "Browser Cookies (untuk IG/FB):" bukan "cookies_label"

## 🔧 Test Translation (Optional):
Jika ingin memastikan translation berfungsi sebelum menjalankan aplikasi:
```bash
python socmed-downloader\test_translation.py
```

Hasil yang benar akan menampilkan text tanpa underscore.

## 📝 Catatan Teknis:
Python meng-cache imported modules. Perubahan pada file .py tidak akan 
terlihat sampai aplikasi di-restart atau module di-reload secara manual.
File yang sudah diupdate:
- ✅ socmed-downloader/language_config.py (6 translation keys baru)
- ✅ socmed-downloader/socmed_downloader_gui.py (menggunakan translations)
- ✅ Sudah di-commit dan push ke GitHub

Translation sudah 100% berfungsi (diverifikasi dengan test script).
**ANDA HANYA PERLU RESTART APLIKASI!** 🚀
