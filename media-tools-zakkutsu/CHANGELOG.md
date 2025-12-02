# Changelog

All notable changes to Media Tools Zakkutsu will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2025-12-02

### 🎉 Added
- **FFmpeg Bundled in EXE** - No separate FFmpeg installation needed
- **True Standalone Distribution** - Single 273 MB EXE with everything included
- **Percentage Display** - Progress bars now show exact percentage (e.g., "45.2%")
- **Checkmark on Completion** - Visual indicator (✓) when items finish downloading
- **Enhanced Progress Tracking** - Accurate item-by-item progress without duplicates

### 🔧 Changed
- **yt-dlp Integration** - Switched from subprocess to Python API for better EXE compatibility
- **FFmpeg Detection** - Now checks bundled resources first, then system PATH
- **Progress Hook Logic** - Improved to track 'downloading' and 'finished' states separately
- **Build Process** - Updated PyInstaller config to bundle FFmpeg portable

### 🐛 Fixed
- Fixed yt-dlp not found error when running compiled EXE
- Fixed progress tracking showing inaccurate percentages
- Fixed Flet icons import error (`ft.Icons` → `icons`)
- Fixed console encoding errors with emoji characters
- Fixed missing percentage text next to progress bars
- Fixed duplicate progress updates during downloads

### 📦 Technical
- EXE size increased from 75 MB → 273 MB (due to bundled FFmpeg)
- Added `sys._MEIPASS` support for PyInstaller bundled resources
- Updated `get_ffmpeg_path()` to detect bundled FFmpeg
- Improved Windows console UTF-8 encoding handling

---

## [1.0.0] - 2025-12-01

### 🎉 Added
- **Initial Release** - All-in-One Standalone Edition
- **4 Media Tools** in single file:
  - YouTube Playlist Downloader
  - Media Looper
  - Audio Merger
  - Social Media Downloader
- **Unified Launcher** - Home screen to access all tools
- **Windows EXE Build** - PyInstaller compilation support
- **FFmpeg Auto-Download** - Automatic portable FFmpeg download (v1.0 only)
- **Progress Tracking** - Real-time download progress display
- **Batch Processing** - Support for multiple files/URLs

### 🛠️ Features (v1.0)

#### YouTube Playlist Downloader
- Download entire playlists (video or audio)
- Quality selection (best, 1080p, 720p, 480p, 360p)
- MP3 audio extraction with 192kbps
- Custom file naming templates
- Auto-numbering support
- yt-dlp version checker and updater

#### Media Looper
- Loop video/audio files instantly
- FFmpeg stream copy (no re-encoding)
- Custom loop count
- Zero quality loss

#### Audio Merger
- Merge unlimited audio files
- Crossfade effects (2 seconds)
- Silence gaps (1 second)
- Format conversion support
- Professional audio mixing

#### Social Media Downloader
- Platform support: TikTok, Instagram, Facebook, Twitter/X
- Batch download from TXT, CSV, JSON files
- Auto-detect platform from URL
- Original quality preservation

### 📦 Distribution (v1.0)
- Single Python file: `media_tools_standalone.py` (~1700 lines)
- Windows EXE: `MediaToolsZakkutsu.exe` (75 MB)
- FFmpeg: Separate download required (v1.0 limitation)

---

## [Unreleased]

### 🎯 Planned Features
- macOS and Linux builds
- Built-in video player preview
- Download queue management
- Custom FFmpeg parameters
- Subtitle download support
- Video editing tools
- Thumbnail extraction
- Metadata editor

---

## Version History Summary

| Version | Release Date | Key Feature | EXE Size |
|---------|-------------|-------------|----------|
| 1.0.1   | 2025-12-02  | FFmpeg Bundled | 273 MB |
| 1.0.0   | 2025-12-01  | Initial Release | 75 MB |

---

## Migration Guide

### v1.0.0 → v1.0.1

**No breaking changes!** Simply download the new EXE and replace the old one.

**Benefits of upgrading:**
- ✅ No FFmpeg installation hassle
- ✅ Accurate progress tracking
- ✅ Better EXE reliability
- ✅ Enhanced UI feedback

**Steps:**
1. Download `MediaToolsZakkutsu.exe` v1.0.1
2. Delete old v1.0.0 EXE (optional)
3. Run new version - done!

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

MIT License - See [LICENSE](LICENSE) for details
