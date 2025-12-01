# Media Tools - Release Notes Template

## 📦 How to Create a GitHub Release

### Step 1: Build the Executable

```powershell
# Run from project root
python -m PyInstaller MediaToolsZakkutsu.spec --clean
```

The executable will be created in: `dist/MediaToolsZakkutsu.exe`

### Step 2: Create GitHub Release

1. Go to: https://github.com/zakkutsu/media-tools-py/releases
2. Click **"Draft a new release"**
3. Fill in the release information (see template below)
4. Upload `dist/MediaToolsZakkutsu.exe`
5. Click **"Publish release"**

---

## 📝 Release Template

Use this template when creating a new release on GitHub:

### Tag version
```
v1.0.0
```

### Release title
```
Media Tools v1.0.0 - Complete Media Processing Suite
```

### Description

```markdown
# 🎬 Media Tools v1.0.0

Koleksi lengkap tools untuk pemrosesan media dengan unified GUI launcher.

## 📥 Download

**Download file executable siap pakai (tanpa perlu install Python):**

### Windows
- **MediaToolsZakkutsu.exe** - Single file executable (~150MB)

## ⚠️ System Requirements

### Wajib Diinstall
- **FFmpeg** - Harus diinstall dan tersedia di PATH system
  - Windows: `winget install FFmpeg` atau `choco install ffmpeg`
  - Download manual: https://ffmpeg.org/download.html

### Optional (Sudah Included)
- ✅ Python dependencies (sudah included di executable)
- ✅ Flet GUI framework
- ✅ yt-dlp downloader
- ✅ pydub, Pillow, ffmpeg-python

## 🛠️ Tools yang Tersedia

1. **🎵 Audio Merger** - Menggabungkan multiple file audio dengan efek transisi
2. **🎬 Media Codec Detector** - Analisis codec dan format file media
3. **📥 YouTube Batch Downloader** - Download multiple video YouTube
4. **🎵 YouTube Playlist Downloader** - Download playlist YouTube lengkap
5. **📥 SocMed Downloader** - Download dari TikTok, Instagram, Facebook, Twitter/X
6. **🔁 Media Looper** - Loop video/audio tanpa re-encoding

## 🚀 Cara Menggunakan

### Method 1: Executable (Recommended for End Users)
1. Download `MediaToolsZakkutsu.exe`
2. Install FFmpeg jika belum (lihat System Requirements)
3. Double-click `MediaToolsZakkutsu.exe`
4. Pilih tool yang ingin digunakan

### Method 2: Source Code (For Developers)
```bash
git clone https://github.com/zakkutsu/media-tools-py.git
cd media-tools-py
python setup_media_tools.py
python media_tools_launcher.py
```

## 📋 What's New in v1.0.0

- ✨ Initial release with unified launcher
- ✅ All 6 tools integrated
- ✅ Multi-language support (ID, EN, JP)
- ✅ Auto-dependency installation
- ✅ Standalone executable distribution

## 🐛 Known Issues

- Executable file size is large (~150MB) due to included dependencies
- First launch might take a few seconds to initialize
- Some antivirus software might flag the .exe (false positive)

## 📚 Documentation

- Main README: https://github.com/zakkutsu/media-tools-py
- Individual tool docs available in each subfolder

## 💬 Support

For issues, questions, or feature requests:
- Open an issue: https://github.com/zakkutsu/media-tools-py/issues
- Discussions: https://github.com/zakkutsu/media-tools-py/discussions

---

**Full Changelog**: https://github.com/zakkutsu/media-tools-py/commits/v1.0.0
```

---

## 🔄 Update Checklist for New Releases

Before creating a new release, make sure to:

- [ ] Update version number in code files
- [ ] Test the executable on clean Windows installation
- [ ] Verify FFmpeg detection works correctly
- [ ] Test all 6 tools individually
- [ ] Update CHANGELOG.md with new features/fixes
- [ ] Build with `python -m PyInstaller MediaToolsZakkutsu.spec --clean`
- [ ] Test the built executable
- [ ] Create git tag: `git tag v1.0.0`
- [ ] Push tag: `git push origin v1.0.0`
- [ ] Create GitHub Release with the executable
- [ ] Verify download link in README works

---

## 📊 Build Information

### Current Build Configuration
- **Spec File**: `MediaToolsZakkutsu.spec`
- **Output**: `dist/MediaToolsZakkutsu.exe`
- **Mode**: `--onefile` (single executable)
- **Console**: `--noconsole` (GUI only, no console window)
- **Compression**: UPX enabled

### Build Command
```powershell
python -m PyInstaller MediaToolsZakkutsu.spec --clean
```

### Approximate File Sizes
- Source code (zipped): ~50 KB
- Executable (.exe): ~150 MB (includes all Python dependencies)

---

## 🌐 Distribution Strategy

1. **Source Code** → GitHub Repository (main branch)
2. **Executable** → GitHub Releases (for end users)
3. **Documentation** → README.md (linked in both)

### For End Users:
- Download `.exe` from Releases
- No Python installation needed
- Just need FFmpeg

### For Developers:
- Clone repository
- Use `setup_media_tools.py` for auto-setup
- Develop and contribute
