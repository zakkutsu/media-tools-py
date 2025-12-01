# 📁 Folder Structure Guide

## 🗂️ Project Organization

Project ini terbagi dengan tujuan yang jelas:

### 1. **Tools Folders** (Original) 🔧 FOR DEVELOPMENT

Folder-folder asli untuk masing-masing tool:

```
├── audio-merger/
├── media-codec-detector/
├── yt-batch-downloader/
├── yt-playlist-downloader/
├── socmed-downloader/
├── media-looper/
├── media_tools_launcher.py      # Main launcher
└── launch_media_tools.bat       # Quick run script
```

**Tujuan:** 
- ✅ **Development utama** - Edit & test code di sini
- ✅ Repository untuk source code
- ✅ Dokumentasi individual per tool
- ✅ Structure terpisah (easy version control)

**Cara pakai:**
```bash
# Jalankan launcher terpadu
launch_media_tools.bat

# Atau individual tool
cd audio-merger
python audio_merger_gui.py
```

---

### 2. **media-tools-zakkutsu/** 📦 FOR DISTRIBUTION

Folder khusus **untuk build executable SAJA**:

```
media-tools-zakkutsu/
├── tools/                      # All tools (flat structure)
│   ├── audio_merger.py
│   ├── audio_merger_gui.py
│   ├── media_codec_detector.py
│   ├── ...all other .py files
├── main.py                     # Unified launcher
├── MediaToolsZakkutsu.spec     # PyInstaller config
├── build.bat                   # Build script
├── requirements.txt
└── dist/
    └── MediaToolsZakkutsu.exe  # Output (~75 MB)
```

**Tujuan:**
- ✅ Build single .exe file
- ✅ Distribution to end users
- ✅ GitHub Releases
- ✅ No Python needed

**Cara pakai:**
```bash
cd media-tools-exe
build.bat
# Test: dist\MediaToolsZakkutsu.exe
```

**Tujuan:**
- 📦 **Build executable untuk distribusi**
- ⚠️ JANGAN edit code di sini (edit di original folders)
- 🔄 Copy updated files dari original folders
- 🚀 Build & upload ke GitHub Releases

**Cara pakai:**
```bash
# Build executable
cd media-tools-zakkutsu
build.bat

# Output: dist\MediaToolsZakkutsu.exe
```

---

## 🔄 Workflow

### Step by Step

1. **Development** di original folders:
   ```bash
   # Edit di folder tool asli
   # Misalnya: audio-merger/audio_merger_gui.py
   
   # Test dengan launcher
   launch_media_tools.bat
   ```

2. **Sync ke media-tools-zakkutsu**:
   ```bash
   # Copy file yang diupdate ke tools/
   copy audio-merger\audio_merger_gui.py media-tools-zakkutsu\tools\
   ```

3. **Build executable**:
   ```bash
   cd media-tools-zakkutsu
   build.bat
   ```

4. **Distribute**:
   ```bash
   # Upload dist\MediaToolsZakkutsu.exe ke GitHub Releases
   ```

---

## 🎯 Kapan Pakai Yang Mana?

### Pakai Original Folders kalau:
- 🔧 Sedang development/coding
- 🐛 Debugging error
- ⚡ Test dengan `launch_media_tools.bat`
- 📝 Edit dan track changes di Git
- 💡 Experimenting fitur baru

### Pakai `media-tools-zakkutsu/` kalau:
- 📦 Siap distribusi
- 🚀 Build release version
- 📤 Upload to GitHub Releases
- 👥 Share dengan end users (no Python needed)

---

## 📊 Comparison Table

| Feature | Original Folders | media-tools-zakkutsu |
|---------|------------------|----------------------|
| **Purpose** | Development | Distribution |
| **Structure** | Separated folders | Flat tools/ folder |
| **Run method** | .bat launcher | Build to .exe |
| **Debug** | ✅ Easy | ❌ Hard |
| **Build time** | Instant | 2-3 min |
| **Distribution** | ❌ Source only | ✅ Standalone exe |
| **Edit code** | ✅ YES | ❌ NO (sync from original) |
| **Best for** | Coding & Testing | End users |

---

## 🗺️ Quick Reference

```bash
# Development - Test with launcher
launch_media_tools.bat

# Development - Individual tool
cd audio-merger
python audio_merger_gui.py

# Distribution - Build exe
cd media-tools-zakkutsu
build.bat

# Distribution - Output
media-tools-zakkutsu\dist\MediaToolsZakkutsu.exe
```

---

## 💡 Tips

1. **Always develop in original folders** (audio-merger/, etc.)
2. **Sync to media-tools-zakkutsu** before building
3. **Build from media-tools-zakkutsu** for releases
4. **Never edit code in media-tools-zakkutsu** - sync from original

---

## ⚠️ Important

**media-tools-zakkutsu = EXE BUILD ONLY**  
Edit di original folders → Copy ke zakkutsu → Build exe
- Test exe before distributing
- Original folders = source of truth

---

**Happy Coding! 🎉**
