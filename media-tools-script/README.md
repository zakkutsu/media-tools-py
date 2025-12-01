# Media Tools - Script Version 🔧

> **For Development & Debugging** - Jalankan sebagai Python script

## 🎯 Tujuan Folder Ini

Folder ini **khusus untuk development dan debugging**:
- ✅ Test perubahan code secara real-time
- ✅ Debug dengan mudah menggunakan print/debugger
- ✅ Lihat error messages lengkap
- ✅ Tidak perlu rebuild executable

## 🚀 Cara Menggunakan

### 1. Install Dependencies
```bash
cd media-tools-script
pip install -r requirements.txt
```

### 2. Jalankan
```bash
python main.py
```

## 🔧 Development Workflow

1. **Edit** → Ubah file di `tools/` atau `main.py`
2. **Save** → Simpan perubahan
3. **Run** → `python main.py` 
4. **Test** → Langsung test tanpa rebuild!

## 📂 Struktur

```
media-tools-script/
├── main.py              # Launcher utama
├── language_config.py
├── requirements.txt
├── tools/              # Semua tool modules
│   ├── audio_merger.py
│   ├── audio_merger_gui.py
│   └── (... semua tools lainnya)
└── assets/
```

## 🐛 Debugging

- Tambahkan `print()` statements dimana saja
- Gunakan VS Code debugger
- Error stack traces lengkap muncul di console
- Hot-reload: Edit → Save → Restart

## 🔄 Sync ke Exe Version

Setelah testing OK, copy changes ke exe version:

```bash
# Copy file yang diubah
cp tools/audio_merger.py ../media-tools-exe/tools/

# Rebuild executable
cd ../media-tools-exe
build.bat
```

## 🆚 Perbedaan dengan Exe Version

| | Script Version | Exe Version |
|---|---|---|
| **Kecepatan test** | ⚡ Instant | ⏱️ 2-3 menit |
| **Debugging** | ✅ Mudah | ❌ Sulit |
| **Distribusi** | ❌ Butuh Python | ✅ Standalone |
| **Use case** | 🔧 Development | 📤 Distribution |

---

**Development → Pakai folder ini**  
**Distribution → Pakai `../media-tools-exe/`**
