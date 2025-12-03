import flet as ft
import subprocess
import os
import threading
import re

def main(page: ft.Page):
    page.title = "🎵 Spotify Downloader Pro (SpotDL)"
    page.window_width = 750
    page.window_height = 700
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a2e"

    # --- KOMPONEN UI ---
    url_input = ft.TextField(
        label="🔗 Link Spotify (Lagu/Album/Playlist)",
        width=600,
        border_color=ft.Colors.GREEN_400,
        focused_border_color=ft.Colors.GREEN_200,
        text_size=14
    )
    
    bitrate_options = ["128k", "192k", "256k", "320k"]
    bitrate_dropdown = ft.Dropdown(
        label="🎧 Bitrate",
        width=120,
        options=[ft.dropdown.Option(opt) for opt in bitrate_options],
        value="320k",
        border_color=ft.Colors.BLUE_400
    )

    # Output folder
    default_output_folder = os.path.join(os.path.expanduser("~"), "Downloads", "Music_Downloads")
    output_folder_field = ft.TextField(
        label="📁 Folder Output",
        value=default_output_folder,
        width=400,
        read_only=True,
        text_size=12,
        border_color=ft.Colors.ORANGE_400
    )
    
    def pick_folder_result(e: ft.FilePickerResultEvent):
        if e.path:
            output_folder_field.value = e.path
            page.update()

    folder_picker = ft.FilePicker(on_result=pick_folder_result)
    page.overlay.append(folder_picker)

    pick_folder_btn = ft.ElevatedButton(
        "Pilih Folder",
        icon=ft.Icons.FOLDER_OPEN,
        bgcolor=ft.Colors.ORANGE_700,
        color=ft.Colors.WHITE,
        on_click=lambda _: folder_picker.get_directory_path()
    )

    # Status & Progress
    status_text = ft.Text(value="✨ Siap Download", color=ft.Colors.CYAN_200, size=14, weight=ft.FontWeight.BOLD)
    progress_bar = ft.ProgressBar(width=600, visible=False, color=ft.Colors.GREEN_400, bgcolor=ft.Colors.GREY_800)
    progress_label = ft.Text(value="", size=12, color=ft.Colors.GREEN_200)

    # Tabel Lagu dengan kolom lengkap
    song_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("#", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Artis", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Judul", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Durasi", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
            ft.DataColumn(ft.Text("Status", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
        ],
        rows=[],
        border=ft.border.all(1, ft.Colors.GREY_700),
        border_radius=10,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        data_row_max_height=45
    )
    
    # Container scrollable untuk tabel
    table_container = ft.Container(
        content=ft.Column([song_table], scroll=ft.ScrollMode.ADAPTIVE),
        height=350,
        border=ft.border.all(1, ft.Colors.GREY_600),
        border_radius=10,
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
    )

    # --- ICON STATUS ---
    def get_status_icon(status):
        if status == "waiting":
            return ft.Icon(ft.Icons.RADIO_BUTTON_UNCHECKED, color=ft.Colors.GREY_400, size=18)
        elif status == "downloading":
            return ft.ProgressRing(width=16, height=16, stroke_width=2, color=ft.Colors.BLUE_400)
        elif status == "done":
            return ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN_400, size=18)
        elif status == "error":
            return ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED_400, size=18)
        return ft.Icon(ft.Icons.HELP_OUTLINE, color=ft.Colors.GREY_400, size=18)

    # --- LOGIC DOWNLOAD (THREADING) ---
    def run_download_process(url, output_folder, bitrate):
        """Fungsi ini berjalan di background thread"""
        
        # Update UI: Mulai
        status_text.value = "🚀 Memulai download..."
        status_text.color = ft.Colors.YELLOW_200
        progress_bar.visible = True
        song_table.rows.clear()
        page.update()

        # Flags untuk menyembunyikan window CMD (khusus Windows)
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Langsung Download (tanpa list dulu)
        # Gunakan python -m spotdl untuk menghindari masalah PATH
        import sys
        dl_cmd = [
            sys.executable, '-m', 'spotdl', 'download', url,
            '--output', output_folder,
            '--format', 'mp3',
            '--bitrate', bitrate,
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

            song_index = 0
            completed_count = 0
            error_count = 0
            current_song = ""
            
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                
                # Deteksi lagu baru yang sedang diproses
                if "Processing" in line or "Searching" in line:
                    # Parsing nama lagu dari output
                    if " - " in line:
                        parts = line.split(":")
                        if len(parts) > 1:
                            song_info = parts[-1].strip()
                        else:
                            song_info = line
                        
                        # Bersihkan nama lagu
                        song_info = re.sub(r'^(Processing|Searching)\s*:?\s*', '', song_info).strip()
                        
                        if song_info and " - " in song_info:
                            song_index += 1
                            current_song = song_info
                            
                            # Pisahkan Artis dan Judul
                            parts = song_info.split(" - ", 1)
                            artist = parts[0].strip() if len(parts) > 1 else "-"
                            title = parts[1].strip() if len(parts) > 1 else song_info
                            
                            row_obj = ft.DataRow(cells=[
                                ft.DataCell(ft.Text(str(song_index), color=ft.Colors.GREY_300)),
                                ft.DataCell(ft.Text(artist[:25] + "..." if len(artist) > 25 else artist, color=ft.Colors.CYAN_200, size=12)),
                                ft.DataCell(ft.Text(title[:35] + "..." if len(title) > 35 else title, color=ft.Colors.WHITE, size=12)),
                                ft.DataCell(ft.Text("-", color=ft.Colors.GREY_400, size=12)),
                                ft.DataCell(get_status_icon("downloading")),
                            ])
                            song_table.rows.append(row_obj)
                            status_text.value = f"🔄 Downloading: {title[:40]}..."
                            page.update()
                
                # Deteksi download selesai
                elif "Downloaded" in line or "Skipping" in line or "already exists" in line.lower():
                    if song_table.rows:
                        song_table.rows[-1].cells[4].content = get_status_icon("done")
                        completed_count += 1
                        progress_label.value = f"✅ {completed_count} lagu selesai"
                        page.update()
                
                # Deteksi error
                elif "error" in line.lower() or "failed" in line.lower() or "no results" in line.lower():
                    if song_table.rows:
                        song_table.rows[-1].cells[4].content = get_status_icon("error")
                        error_count += 1
                        page.update()
                
                # Update status text untuk info lain
                elif "Found" in line:
                    status_text.value = f"📋 {line}"
                    page.update()

            process.wait()
            
            if completed_count > 0:
                status_text.value = f"🎉 Selesai! {completed_count} lagu berhasil didownload."
                status_text.color = ft.Colors.GREEN_400
            elif error_count > 0:
                status_text.value = f"⚠️ Download selesai dengan {error_count} error."
                status_text.color = ft.Colors.ORANGE_400
            else:
                status_text.value = "⚠️ Tidak ada lagu yang didownload. Cek link atau koneksi."
                status_text.color = ft.Colors.ORANGE_400
        
        except Exception as e:
            status_text.value = f"❌ Error: {str(e)}"
            status_text.color = ft.Colors.RED_400
        
        finally:
            progress_bar.visible = False
            page.update()

    def on_click_download(e):
        url = url_input.value.strip()
        folder = output_folder_field.value
        bitrate = bitrate_dropdown.value

        if not url:
            url_input.error_text = "Link tidak boleh kosong!"
            page.update()
            return
        else:
            url_input.error_text = None

        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                status_text.value = "❌ Folder tidak valid."
                status_text.color = ft.Colors.RED_400
                page.update()
                return

        # Jalankan di thread terpisah
        t = threading.Thread(target=run_download_process, args=(url, folder, bitrate), daemon=True)
        t.start()

    # --- TOMBOL DOWNLOAD ---
    btn_download = ft.ElevatedButton(
        "🚀 Mulai Download",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=on_click_download,
        width=200,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        )
    )

    # --- LAYOUT ---
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🎵 Spotify Downloader Pro", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                ft.Text("Download lagu dari Spotify via YouTube Music", size=12, color=ft.Colors.GREY_400),
                ft.Divider(height=20, color=ft.Colors.GREY_700),
                
                url_input,
                ft.Row([
                    bitrate_dropdown,
                    output_folder_field,
                    pick_folder_btn
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                
                ft.Divider(height=15, color="transparent"),
                ft.Row([btn_download], alignment=ft.MainAxisAlignment.CENTER),
                ft.Divider(height=15, color="transparent"),
                
                ft.Row([status_text, progress_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                progress_bar,
                
                ft.Divider(height=10, color="transparent"),
                ft.Text("📋 Daftar Lagu:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                table_container
            ]),
            padding=10
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
