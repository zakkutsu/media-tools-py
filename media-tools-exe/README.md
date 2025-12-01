# Media Tools - Executable Version 📦

> **For Distribution** - Build single .exe file

## 🎯 Tujuan Folder Ini

Folder ini **khusus untuk build executable** yang siap didistribusikan:
- ✅ Single file .exe (~80MB)
- ✅ Tidak butuh Python installed
- ✅ Siap upload ke GitHub Releases
- ✅ End-user friendly

## 🚀 Build Executable

### Quick Build
```bash
cd media-tools-exe
build.bat
```

### Manual Build
```bash
python -m PyInstaller MediaToolsZakkutsu.spec --clean
```

**Output:** `dist/MediaToolsZakkutsu.exe`

## 📦 Distribusi

1. **Build** executable dengan `build.bat`
2. **Test** executable di `dist/MediaToolsZakkutsu.exe`
3. **Upload** ke GitHub Releases
4. **Share** link download dengan users

## 📋 Files

```
media-tools-exe/
├── MediaToolsZakkutsu.spec  # PyInstaller config
├── build.bat                # Build script
├── main.py
├── requirements.txt
├── tools/                   # All tool modules
│   └── (... semua tools)
└── dist/                    # Output folder
    └── MediaToolsZakkutsu.exe
```

## ⚙️ Configuration

### Build Settings (MediaToolsZakkutsu.spec)
- `--onefile`: Single executable
- `--noconsole`: No console window
- `upx=True`: Compression enabled
- All dependencies bundled

### Requirements
- PyInstaller
- All Python dependencies
- ~2-3 minutes build time

## 🔧 Maintenance

### Update dari Script Version

Setelah development selesai di `../media-tools-script/`:

```bash
# 1. Copy updated files
cp ../media-tools-script/tools/audio_merger.py tools/
cp ../media-tools-script/main.py .

# 2. Rebuild
build.bat

# 3. Test
dist\MediaToolsZakkutsu.exe
```

### Testing Checklist

- [ ] Build berhasil tanpa error
- [ ] Executable bisa dijalankan
- [ ] Semua 6 tools bisa dibuka
- [ ] FFmpeg detection works
- [ ] File size reasonable (~80MB)

## 📤 GitHub Release

1. **Tag version:**
   ```bash
   git tag -a v1.0.0 -m "Release v1.0.0"
   git push origin v1.0.0
   ```

2. **Create release** di GitHub

3. **Upload** `dist/MediaToolsZakkutsu.exe`

4. **Update** README link

## 🐛 Troubleshooting

### Build Failed
```bash
# Clean and retry
Remove-Item -Recurse -Force build, dist
python -m PyInstaller MediaToolsZakkutsu.spec --clean
```

### Exe Not Working
- Test di clean Windows installation
- Check FFmpeg in PATH
- Verify all dependencies bundled

### Large File Size
- Normal ~80MB with all dependencies
- Can't reduce much without breaking tools

## 💡 Tips

- **Always test** executable before distributing
- **Keep script version** in sync
- **Document changes** in CHANGELOG
- **Test on different** Windows versions

## 🆚 vs Script Version

| | Exe Version | Script Version |
|---|---|---|
| **Build time** | ⏱️ 2-3 menit | ⚡ Instant |
| **Distribution** | ✅ Easy | ❌ Need Python |
| **Debugging** | ❌ Sulit | ✅ Mudah |
| **File size** | 📦 ~80 MB | 📄 Few KB |
| **Use case** | 📤 End users | 🔧 Developers |

---

**Distribution → Pakai folder ini**  
**Development → Pakai `../media-tools-script/`**
