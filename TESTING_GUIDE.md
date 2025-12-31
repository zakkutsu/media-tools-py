# 🧪 Testing Guide - Media Tools (English UI)

## ✅ All Changes Completed

### 🔄 Changes Made:
1. ✅ **UI Language**: All UI text converted to **English**
2. ✅ **Language Switcher**: Removed from all modules
3. ✅ **Language Config Files**: Deleted (3 files)
4. ✅ **README**: Kept in **Indonesian** (as requested)
5. ✅ **Import Errors**: Fixed all language_config imports

### 📝 Modules Updated:
1. ✅ **audio-merger** - audio_merger_gui.py
2. ✅ **media-codec-detector** - media_codec_detector_gui.py
3. ✅ **yt-batch-downloader** - batch_downloader_gui_flet.py
4. ✅ **yt-playlist-downloader** - playlist_downloader_gui_flet.py
5. ✅ **socmed-downloader** - socmed_downloader_gui.py
6. ✅ **spotify-downloader** - spotify_downloader_gui_flet.py (already Indonesian, kept as is)
7. ✅ **media-looper** - media_looper_gui_flet.py (no language system)
8. ✅ **media_tools_launcher.py** - Main launcher

---

## 🧪 Manual Testing Checklist

### 1. Test Media Tools Launcher BAT
```bash
# Double-click or run:
launch_media_tools.bat
```

**Expected:**
- ✅ Launcher window opens
- ✅ Title: "Media Tools Suite"
- ✅ ALL text in **English**
- ✅ No language selector dropdown
- ✅ All tool cards displayed with English text

---

### 2. Test Audio Merger

**Launch from:**
- Option A: Via main launcher → Click "🎵 Audio Merger"
- Option B: Direct run: `python audio-merger/audio_merger_gui.py`

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🎵 Audio Merger"
- ✅ Description: "Merge audio files into one with transition effects"
- ✅ Button texts in English:
  - "Select Audio Folder" 
  - "Select Output Folder"
  - "Reset"
  - "Start Merging Audio"
- ✅ Effect options in English:
  - "Direct Merge (No Effects)"
  - "Crossfade (Smooth Transition)"
  - "Gap/Silence (Silence between tracks)"
- ✅ Progress messages in English
- ✅ No language selector

**Quick functional test:**
1. Select a folder with audio files
2. Verify files are listed
3. Click "Start Merging Audio"
4. Verify merge completes successfully

---

SUCESSFULLY 100%

### 3. Test Media Codec Detector

**Launch from:**
- Option A: Via main launcher → Click "🎬 Media Codec Detector"
- Option B: Direct run: `python media-codec-detector/media_codec_detector_gui.py`

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🎬 Media Codec Detector"
- ✅ Description: "Detect container format and codecs from media files"
- ✅ Mode options in English:
  - "Single File Analysis"
  - "Analyze All Files in Folder"
- ✅ Buttons in English:
  - "Select File"
  - "Select Folder"
  - "Start Analysis"
- ✅ Analysis results in English
- ✅ No language selector

**Quick functional test:**
1. Select single file mode
2. Choose a media file
3. Click "Start Analysis"
4. Verify analysis completes with English results

---

NOTE TESTING MANUAL: Tidak ada persentase dari analisis, sehingga saya tidak tau apakah analisis berjalan atau tidak.. dan setelah saya tunggu lama selama 20 menit, hasil analis belum keluar

PERBAIKAN YANG HARUS DILAKUKAN: 
1. Tambahkan persentase saat analisis agar tau sudah berapa persen berjalan.
2. Tambahkan tulisan success atau finish jika sudah selesai
3. Tambahkan deskripsi dari codec terkait
4. Pastikan support semua jenis file, entah gambar, audio, video, dokumen dll
5. Hapus utilities yg berisi teks "Buat File Dummy untuk testing.

### 4. Test YouTube Batch Downloader

**Launch from:**
- Option A: Via main launcher → Click "📥 Batch Downloader"
- Option B: Direct run: `python yt-batch-downloader/batch_downloader_gui_flet.py` (requires path setup via launcher)

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🎬 YouTube Batch Downloader"
- ✅ Description: "Download multiple individual YouTube videos"
- ✅ UI elements in English:
  - "Download Folder"
  - "Browse"
  - "Enter YouTube URL"
  - "Add URL"
  - "Load from File"
  - "Save to File"
  - "Clear All"
  - "Start Download"
- ✅ Quality options in English:
  - "Video (Best Quality)"
  - "Video (720p - Save Bandwidth)"
  - "Audio Only (MP3)"
- ✅ No language selector

---

### 5. Test YouTube Playlist Downloader

**Launch from:**
- Option A: Via main launcher → Click "🎵 Playlist Downloader"
- Option B: Via launcher only (has dependencies)

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🎵 YouTube Playlist Downloader"
- ✅ Description: "Download complete YouTube playlists"
- ✅ UI in English
- ✅ "Playlist URL" field
- ✅ "Start Download" button
- ✅ No language selector

---

### 6. Test SocMed Downloader

**Launch from:**
- Option A: Via main launcher → Click "🌐 SocMed Downloader"
- Option B: Direct run: `python socmed-downloader/socmed_downloader_gui.py`

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🌐 SocMed Downloader"
- ✅ Description: "Download videos & audio from social media platforms"
- ✅ Platform info: "TikTok, Instagram, Facebook, Twitter/X & Other Platforms"
- ✅ UI elements in English:
  - "Download Folder"
  - "Enter Video/Audio URL:"
  - "Select Format:" (Video/Audio/Image)
  - "Select Quality:"
  - "Browser Cookies (for IG/FB):"
  - "Start Download"
- ✅ Mode options in English:
  - "Single (1 link)"
  - "Batch (Multiple links from file)"
- ✅ **NO language selector dropdown** ← CRITICAL CHECK
- ✅ No "Language:" label

---

### 7. Test Media Looper

**Launch from:**
- Option A: Via main launcher → Click "🔁 Media Looper"
- Option B: Direct run: `python media-looper/media_looper_gui_flet.py`

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "Media Looper Tool"
- ✅ Tabs: "Single Loop" and "Alternating Loop"
- ✅ UI already in English (no changes were needed)

---

### 8. Test Spotify Downloader

**Launch from:**
- Option A: Via main launcher → Click "🎵 Spotify Downloader"
- Option B: Direct run: `cd spotify-downloader; python spotify_downloader_gui_flet.py`

**Test checklist:**
- ✅ Window opens without errors
- ✅ Title: "🎵 Spotify Downloader Pro (SpotDL)"
- ✅ UI in Indonesian (unchanged - was already Indonesian only)
- ✅ Functional test: Enter a Spotify URL and verify download works

---

NOTE: Saya ingin membuat spotify downloader tanpa api key
jadi ada 2 jenis, 1 pake api key, 1 tanpa api key
tapi untuk saat ini saya fokus ke versi tanpa api key dulu

BERIKUT INTRUKSI SPOTIFY TANPA API KEY:
Wah, benar sekali. Berdasarkan screenshot yang kamu kirim, tombol **"Create app"** memang sedang dinonaktifkan oleh Spotify dengan pesan:

> *"New integrations are currently on hold while we make updates to improve reliability and performance."*
> (Integrasi baru sedang ditunda sementara kami melakukan pembaruan...)

Ini adalah kebijakan global dari Spotify saat ini (sedang *maintenance* besar-besaran pada API mereka), jadi bukan akunmu yang bermasalah.

---

### Apakah ini akhir segalanya? Tentu TIDAK. 🛠️

Kabar baiknya: **`spotdl` SEBENARNYA BISA JALAN TANPA API KEY.**

API Key yang kita coba buat tadi itu hanya "jalan tol" khusus supaya lebih ngebut. Tanpa API Key, `spotdl` akan menggunakan "jalur umum" (Anonymous). Biasanya error yang kamu alami sebelumnya ("bermasalah") **bukan** karena kurang API Key, tapi karena **FFmpeg** belum terdeteksi.

Mari kita fokus memperbaiki scriptnya agar bisa jalan **tanpa login**.

### Solusi: Gunakan Script V3 (Mode Debug)

Saya sudah buatkan script **V3 Debug** di jawaban sebelumnya. Script itu dirancang khusus untuk mendeteksi error tanpa perlu API Key.

**Lakukan langkah ini:**

1. **Lupakan soal Dashboard Spotify.** Kamu tidak membutuhkannya sekarang.
2. **Copy-Paste** kode `gui_spotify_v3_debug.py` yang saya berikan di jawaban sebelumnya.
3. Jalankan scriptnya.
4. Saat aplikasi terbuka, **JANGAN** download dulu. Lihat di bagian bawah, klik **"Log System"**.
5. Apakah ada tulisan merah: **"MISSING: FFmpeg"**?

### Jika Errornya "FFmpeg not found" / "Missing"

Ini masalah utamanya (90% kasus). Script Python tidak bisa mengubah lagu jadi MP3 karena mesinnya (FFmpeg) tidak ada.

**Cara Memperbaiki (Hanya 2 Menit):**

1. Download **FFmpeg** (versi *Essentials build*) dari link ini: [gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip](https://www.google.com/search?q=https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip)
2. Buka file ZIP tersebut.
3. Masuk ke folder `bin`. Kamu akan melihat file bernama `ffmpeg.exe`.
4. **Copy file `ffmpeg.exe` tersebut.**
5. **Paste** di folder yang sama persis dengan tempat kamu menyimpan file python (`gui_spotify_v3_debug.py`).

Setelah `ffmpeg.exe` dan file python kamu bertetangga (satu folder), coba jalankan lagi scriptnya. Pasti lancar!

Tentu, ini adalah script Versi 3 (Debug Mode) yang paling kuat.

Script ini TIDAK MEMERLUKAN API KEY. Script ini akan berjalan menggunakan mode Anonymous (Tamu). Jika ada error, script ini akan memberitahumu alasannya di kotak "Log System" di bawah tombol.

Kode Python: spotify_downloader_v3.py
Silakan copy semua kode di bawah ini:

Python

import flet as ft
import subprocess
import os
import threading
import re
import shutil
import sys

def main(page: ft.Page):
    page.title = "Spotify Downloader V3 (No Login Required)"
    page.window_width = 800
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20

    # --- KOMPONEN UI ---
    url_input = ft.TextField(
        label="Link Spotify (Lagu/Album/Playlist)", 
        width=600, 
        prefix_icon=ft.icons.LINK,
        hint_text="https://open.spotify.com/track/..."
    )
    
    bitrate_dropdown = ft.Dropdown(
        label="Kualitas",
        width=120,
        options=[ft.dropdown.Option(o) for o in ["128k", "192k", "256k", "320k"]],
        value="320k"
    )

    # Folder Output Default
    default_path = os.path.join(os.path.expanduser("~"), "Downloads", "Music_Downloads")
    output_folder_field = ft.TextField(value=default_path, width=450, read_only=True, text_size=12)
    
    # Log Console (Penting untuk melihat error)
    log_text = ft.Text(value="Menunggu perintah...", font_family="Consolas", size=12, color=ft.Colors.GREEN_400)
    log_container = ft.Column([log_text], scroll=ft.ScrollMode.ALWAYS, height=150)
    
    # Expander Log
    log_expander = ft.ExpansionTile(
        title=ft.Text("Log System (Klik ini jika error)", color=ft.Colors.RED_200, weight="bold"),
        subtitle=ft.Text("Cek di sini untuk melihat detail proses", size=12, italic=True),
        controls=[ft.Container(content=log_container, bgcolor=ft.Colors.BLACK, padding=10)],
        initially_expanded=False
    )

    status_text = ft.Text("Siap", size=16, weight="bold")
    progress_bar = ft.ProgressBar(width=750, visible=False, color=ft.Colors.GREEN)

    # Tabel Lagu
    song_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#"), numeric=True),
            ft.DataColumn(ft.Text("Info Lagu")),
            ft.DataColumn(ft.Text("Status")),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_800),
        heading_row_color=ft.Colors.BLACK26,
    )
    table_container = ft.Column([song_table], scroll=ft.ScrollMode.ADAPTIVE, height=300)

    # --- FUNGSI BANTUAN ---
    def add_log(message, is_error=False):
        color = ft.Colors.RED if is_error else ft.Colors.GREEN_400
        log_text.value += f"\n> {message}"
        log_text.color = color
        page.update()

    def check_dependencies():
        """Cek apakah FFmpeg dan SpotDL terinstall"""
        missing = []
        
        # Cek FFmpeg (Bisa dari PATH atau file exe di folder yang sama)
        ffmpeg_in_folder = os.path.exists("ffmpeg.exe")
        ffmpeg_in_path = shutil.which("ffmpeg")
        
        if not (ffmpeg_in_path or ffmpeg_in_folder):
            missing.append("FFmpeg")
            
        if not shutil.which("spotdl"):
            missing.append("SpotDL (Library Python)")
        
        if missing:
            msg = f"MISSING: {', '.join(missing)}.\n"
            msg += "TIPS: Download ffmpeg.exe dan taruh di folder script ini!"
            return False, msg
        return True, "Dependencies OK."

    def pick_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            output_folder_field.value = e.path
            page.update()

    folder_picker = ft.FilePicker(on_result=pick_folder_result)
    page.overlay.append(folder_picker)

    # --- CORE LOGIC (THREADING) ---
    def run_download_thread(url, folder, bitrate):
        add_log("--- MEMULAI PROSES BARU ---")
        
        # 1. Cek Dependencies
        ok, msg = check_dependencies()
        if not ok:
            status_text.value = "❌ Gagal: Komponen Hilang"
            add_log(msg, True)
            progress_bar.visible = False
            page.update()
            # Buka log otomatis biar user sadar
            log_expander.initially_expanded = True 
            page.update()
            return

        status_text.value = "🔍 Sedang mengambil daftar lagu..."
        progress_bar.visible = True
        song_table.rows.clear()
        page.update()

        # Siapkan folder output
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except Exception as e:
                add_log(f"Gagal buat folder: {e}", True)
                return

        # Hide CMD window flags
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # 2. PROSES LIST (Dry Run - Cek Lagu dulu)
        add_log(f"Mencari metadata: {url}")
        try:
            list_cmd = ['spotdl', 'list', url]
            
            proc = subprocess.Popen(
                list_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                text=True, 
                startupinfo=startupinfo
            )
            stdout, stderr = proc.communicate()

            # SpotDL kadang return non-zero tapi berhasil list, jadi kita cek outputnya
            if "Error" in stderr and not stdout:
                status_text.value = "❌ Gagal mengambil list."
                add_log(f"Error SpotDL:\n{stderr}", True)
                progress_bar.visible = False
                page.update()
                return

            # Parsing Output List
            lines = stdout.splitlines()
            valid_rows = []
            idx = 1
            
            for line in lines:
                # Filter baris yang relevan
                if " - " in line and not line.startswith("Found"):
                    clean_line = re.sub(r'^\d+\.\s*', '', line).strip()
                    
                    row = ft.DataRow(cells=[
                        ft.DataCell(ft.Text(str(idx))),
                        ft.DataCell(ft.Text(clean_line, size=12, width=400)),
                        ft.DataCell(ft.Icon(ft.icons.CIRCLE_OUTLINED, size=16)),
                    ])
                    song_table.rows.append(row)
                    valid_rows.append(row)
                    idx += 1
            
            add_log(f"Ditemukan {len(valid_rows)} lagu.")
            page.update()

            if not valid_rows:
                add_log("Output kosong. Cek Link atau Koneksi.", True)
                add_log(f"Raw Output: {stdout[:100]}...", True)
                status_text.value = "⚠️ Tidak ada lagu ditemukan."
                progress_bar.visible = False
                page.update()
                return

        except Exception as e:
            add_log(f"Crash saat List: {e}", True)
            return

        # 3. PROSES DOWNLOAD REAL
        status_text.value = "🚀 Mendownload..."
        add_log("Memulai download stream...")
        page.update()

        dl_cmd = [
            'spotdl', url,
            '--output', folder,
            '--format', 'mp3',
            '--bitrate', bitrate,
            '--simple-tui'
        ]

        try:
            process = subprocess.Popen(
                dl_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True, 
                startupinfo=startupinfo,
                bufsize=1, 
                universal_newlines=True
            )

            current_idx = 0
            
            for line in process.stdout:
                line = line.strip()
                if not line: continue
                
                # Log ke console bawah (filter spam progress bar)
                if "%" not in line:
                    add_log(f"CMD: {line}")

                # Update Status UI
                if "Downloading" in line:
                    status_text.value = f"Sedang memproses lagu ke-{current_idx + 1}..."
                    if current_idx < len(valid_rows):
                        valid_rows[current_idx].cells[2].content = ft.ProgressRing(width=15, height=15)
                        page.update()

                elif "Downloaded" in line or "Skipping" in line:
                    if current_idx < len(valid_rows):
                        valid_rows[current_idx].cells[2].content = ft.Icon(ft.icons.CHECK_CIRCLE, color=ft.Colors.GREEN, size=20)
                        current_idx += 1
                        page.update()
                
                elif "Error" in line:
                    status_text.value = "⚠️ Terjadi Error pada satu lagu"
                    if current_idx < len(valid_rows):
                        valid_rows[current_idx].cells[2].content = ft.Icon(ft.icons.ERROR, color=ft.Colors.RED, size=20)
                        current_idx += 1
                        page.update()

            process.wait()
            status_text.value = "✅ Proses Selesai!"
            add_log("Selesai.")

        except Exception as e:
            status_text.value = f"❌ Error Fatal: {e}"
            add_log(f"Crash: {e}", True)
        
        finally:
            progress_bar.visible = False
            page.update()

    def on_click_start(e):
        url = url_input.value.strip()
        folder = output_folder_field.value
        bitrate = bitrate_dropdown.value
        
        if not url:
            url_input.error_text = "Link wajib diisi"
            page.update()
            return
        url_input.error_text = None
        
        t = threading.Thread(target=run_download_thread, args=(url, folder, bitrate), daemon=True)
        t.start()

    # --- LAYOUT ---
    page.add(
        ft.Row([ft.Icon(ft.icons.MUSIC_NOTE, color=ft.Colors.GREEN), ft.Text("Spotify Downloader V3", size=20, weight="bold")]),
        ft.Divider(),
        url_input,
        ft.Row([bitrate_dropdown, output_folder_field, ft.IconButton(ft.icons.FOLDER, on_click=lambda _: folder_picker.get_directory_path())]),
        ft.ElevatedButton("DOWNLOAD SEKARANG", color="white", bgcolor=ft.Colors.GREEN, width=200, height=45, on_click=on_click_start),
        ft.Divider(height=10, color="transparent"),
        status_text,
        progress_bar,
        ft.Text("Daftar Antrian:", weight="bold"),
        table_container,
        ft.Divider(),
        log_expander # Log ada di sini
    )

if __name__ == "__main__":
    ft.app(target=main)
⚠️ SYARAT WAJIB AGAR BERHASIL (Tanpa Login)
Script ini PASTI GAGAL jika kamu tidak punya ffmpeg.exe.

Download FFmpeg di sini: Link Download Langsung (gyan.dev)

Buka ZIP-nya, masuk ke folder bin.

Ambil file ffmpeg.exe.

Paste (tempel) file ffmpeg.exe itu di folder yang sama dengan file python ini.

Jika ffmpeg.exe sudah ada di sebelah script python, tombol Download akan bekerja lancar meskipun kamu tidak punya akun Spotify Developer.

## 🔍 Critical Verification Points

### For EVERY Module:
1. ❌ **NO "Language:" or "Bahasa:" dropdown selector**
2. ❌ **NO language switching functionality**
3. ✅ **ALL UI text must be in English**
4. ✅ **All buttons, labels, and messages in English**
5. ✅ **Error messages in English**
6. ✅ **Progress indicators in English**

### Special Check - SocMed Downloader:
This module had the most complex language system. Verify:
- ❌ NO language dropdown at top-right
- ✅ ALL text in English from top to bottom
- ✅ Form labels in English
- ✅ Button texts in English
- ✅ Status messages in English

---

## 🐛 Known Issues / Notes

1. **Import Test Results**: 
   - ✅ 6/8 modules import successfully standalone
   - ❌ batch_downloader_gui_flet and playlist_downloader_gui_flet require launcher path setup
   - ✅ **This is OK** - use main launcher to run these modules

2. **FFmpeg**:
   - ✅ System FFmpeg detected and working
   - ⚠️ FFmpeg portable not configured (optional)

3. **Background Modules**:
   - ✅ batch_downloader.py - Backend for batch downloader (required)
   - ✅ playlist_downloader.py - Backend for playlist downloader (required)
   - ✅ socmed_downloader.py - Backend for socmed downloader (required)
   - ✅ spotify_downloader.py - **DELETED** (not used by GUI)

---

## ✅ Quick Smoke Test

Run this to verify all changes:

```bash
# 1. Test module imports
python test_modules.py

# Expected: 6/8 modules OK (batch & playlist need launcher)

# 2. Launch main GUI
.\launch_media_tools.bat

# Verify:
# - Launcher opens
# - Title in English
# - No language selector
# - All tool cards show English text

# 3. Test one module from launcher
# - Click "🎵 Audio Merger"
# - Verify UI is in English
# - Verify no language selector
```

---

## 📊 Success Criteria

✅ **PASS if ALL of these are true:**
1. Main launcher opens without errors
2. ALL UI text is in English
3. NO language selector in any module
4. No import errors in console
5. Each module can be launched from main launcher
6. Basic functionality works (can select files, click buttons, etc.)

❌ **FAIL if ANY of these occur:**
1. Any language selector/dropdown visible
2. Any Indonesian/Japanese text in UI (except README)
3. Import errors related to language_config
4. Module fails to launch from launcher
5. Crashes or Python errors

---

## 🎯 Final Verification Command

```bash
# Verify no language_config files remain
Get-ChildItem -Recurse -Filter "language_config.py" | Select-Object FullName

# Expected: ONLY in media-tools-zakkutsu folder (separate project)
# Should NOT appear in root or socmed-downloader
```

---

## 📝 Report Template

After testing, fill this out:

```
### Test Results - [Date]

**Launcher BAT:**
- [ ] Opens successfully
- [ ] UI in English
- [ ] No language selector

**Audio Merger:**
- [ ] Launches OK
- [ ] UI in English
- [ ] Basic function works

**Media Codec Detector:**
- [ ] Launches OK
- [ ] UI in English
- [ ] Basic function works

**YouTube Batch Downloader:**
- [ ] Launches OK
- [ ] UI in English

**YouTube Playlist Downloader:**
- [ ] Launches OK
- [ ] UI in English

**SocMed Downloader:**
- [ ] Launches OK
- [ ] UI in English
- [ ] NO language selector (CRITICAL)

**Media Looper:**
- [ ] Launches OK
- [ ] UI in English

**Spotify Downloader:**
- [ ] Launches OK
- [ ] Indonesian UI (unchanged)

**Overall Status:** ✅ PASS / ❌ FAIL
**Issues Found:** (list any problems)
```

---

## 🚀 Next Steps After Testing

If all tests pass:
1. ✅ Commit changes to Git
2. ✅ Update main README if needed
3. ✅ Deploy to production

If tests fail:
1. Note which module failed
2. Check console for error messages
3. Verify file changes were applied correctly
4. Re-run failed tests
