# 📦 Panduan Upload ke GitHub Releases

## Langkah-langkah Singkat

### 1️⃣ Build Executable
```powershell
# Dari root project
python -m PyInstaller MediaToolsZakkutsu.spec --clean
```

**Output:** `dist/MediaToolsZakkutsu.exe` (~150MB)

### 2️⃣ Test Executable
- Jalankan `dist/MediaToolsZakkutsu.exe`
- Test semua 6 tools
- Pastikan tidak ada error

### 3️⃣ Commit & Push Code
```bash
git add .
git commit -m "Release v1.0.0"
git push origin main
```

### 4️⃣ Create Git Tag
```bash
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

### 5️⃣ Create GitHub Release

1. **Buka GitHub Repository**
   - https://github.com/zakkutsu/media-tools-py

2. **Klik "Releases"** (di sidebar kanan)

3. **Klik "Draft a new release"**

4. **Isi Form Release:**

   **Choose a tag:** 
   - Pilih `v1.0.0` (tag yang baru dibuat)

   **Release title:**
   ```
   Media Tools v1.0.0 - Complete Media Processing Suite
   ```

   **Description:** (Copy dari RELEASE_NOTES.md atau custom)
   ```markdown
   # 🎬 Media Tools v1.0.0

   Download versi siap pakai tanpa perlu install Python!

   ## 📥 Download
   
   **Windows:** MediaToolsZakkutsu.exe (~150MB)
   
   ## ⚠️ System Requirements
   - **FFmpeg** wajib diinstall: `winget install FFmpeg`
   
   ## 🛠️ 6 Tools Included
   - Audio Merger
   - Media Codec Detector  
   - YouTube Batch Downloader
   - YouTube Playlist Downloader
   - SocMed Downloader (TikTok, IG, FB, Twitter/X)
   - Media Looper
   
   ## 🚀 Cara Pakai
   1. Download MediaToolsZakkutsu.exe
   2. Install FFmpeg
   3. Double-click dan jalankan!
   ```

5. **Upload File:**
   - Drag & drop `dist/MediaToolsZakkutsu.exe`
   - Atau klik "Attach binaries" dan pilih file

6. **Klik "Publish release"** ✅

### 6️⃣ Verify

1. Cek link download: `https://github.com/zakkutsu/media-tools-py/releases/latest`
2. Test download file executable
3. Pastikan README link ke releases sudah benar

---

## ✅ Checklist Upload

- [ ] Code sudah di-commit dan di-push
- [ ] Executable sudah di-build dan di-test
- [ ] Git tag sudah dibuat dan di-push
- [ ] GitHub Release sudah dibuat
- [ ] File .exe sudah di-upload ke Release
- [ ] README.md sudah ada link ke Releases
- [ ] Link download di-test dan berfungsi

---

## 🔄 Update Release (Edit)

Jika perlu edit release yang sudah ada:

1. Buka: https://github.com/zakkutsu/media-tools-py/releases
2. Klik "Edit" pada release yang mau diubah
3. Update description atau upload file baru
4. Klik "Update release"

---

## 🗑️ Delete Release (Jika Perlu)

1. Buka release yang mau dihapus
2. Klik "Delete"
3. Konfirmasi deletion

**Note:** Menghapus release tidak menghapus git tag. Untuk hapus tag:
```bash
git tag -d v1.0.0                    # hapus local
git push origin --delete v1.0.0      # hapus remote
```

---

## 📊 Tips & Best Practices

### Naming Convention
- **Tag:** `v1.0.0`, `v1.1.0`, `v2.0.0`
- **Title:** `Media Tools v1.0.0 - Short Description`
- **File:** `MediaToolsZakkutsu.exe` (consistent name)

### File Size
- Current: ~150MB (karena include semua dependencies)
- Future optimization: bisa dikurangi dengan exclude unused modules

### Changelog
- Selalu include changelog di description
- Jelaskan fitur baru, bug fixes, breaking changes

### Testing
- Test executable di clean Windows installation
- Test di Windows Defender (cek false positive)
- Verify semua tools berfungsi

### Communication
- Update README dengan link release
- Announce di Discussions (jika ada)
- Share di social media (optional)

---

## 🐛 Troubleshooting

### "Release draft not found"
- Pastikan sudah login ke GitHub
- Pastikan punya write access ke repository

### "Tag already exists"
- Gunakan tag version baru: `v1.0.1`, `v1.1.0`, dst
- Atau hapus tag lama terlebih dahulu

### "File too large"
- GitHub limit: 2GB per file
- MediaToolsZakkutsu.exe (~150MB) masih aman

### "Download link not working"
- Pastikan release sudah "Published" (bukan Draft)
- Link format: `https://github.com/{owner}/{repo}/releases/latest`

---

## 📝 Template Cepat

Copy-paste ini ke Release description:

```markdown
# 🎬 Media Tools v1.0.0

Download versi siap pakai (tanpa install Python)!

## 📥 Download
**Windows:** MediaToolsZakkutsu.exe

## ⚠️ Requirements
- FFmpeg: `winget install FFmpeg`

## 🛠️ 6 Tools
Audio Merger | Codec Detector | YouTube Batch | YouTube Playlist | SocMed Downloader | Media Looper

## 🚀 Quick Start
1. Download .exe
2. Install FFmpeg
3. Double-click & run!

**Docs:** https://github.com/zakkutsu/media-tools-py
```

---

Selamat! Executable siap didistribusikan ke pengguna! 🎉
