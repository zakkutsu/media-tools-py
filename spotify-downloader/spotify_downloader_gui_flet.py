import flet as ft
import subprocess
import os
import threading
import re
import sys

def check_spotdl_installed():
    """Mengecek apakah spotdl sudah terinstall."""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', 'spotdl'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def install_spotdl():
    """Menginstall spotdl via pip."""
    try:
        subprocess.run(
            [sys.executable, '-m', 'pip', 'install', 'spotdl>=4.0.0'],
            check=True
        )
        return True
    except Exception as e:
        return False

def main(page: ft.Page):
    page.title = "🎵 Spotify Downloader Pro (SpotDL)"
    page.window_width = 750
    page.window_height = 750
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 20
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#1a1a2e"

    # Cek apakah spotdl terinstall
    spotdl_installed = check_spotdl_installed()

    # --- ALERT SPOTDL NOT INSTALLED ---
    def on_install_spotdl(e):
        install_btn.disabled = True
        install_btn.text = "⏳ Installing..."
        install_status.value = "📦 Sedang menginstall spotdl..."
        install_status.color = ft.Colors.BLUE_400
        page.update()
        
        def install_thread():
            success = install_spotdl()
            if success:
                install_status.value = "✅ spotdl berhasil diinstall! Silakan restart aplikasi."
                install_status.color = ft.Colors.GREEN_400
                install_btn.text = "✅ Installed"
            else:
                install_status.value = "❌ Gagal install. Coba manual: pip install spotdl"
                install_status.color = ft.Colors.RED_400
                install_btn.disabled = False
                install_btn.text = "🔄 Coba Lagi"
            page.update()
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    install_btn = ft.Button(
        "📦 Install spotdl Sekarang",
        icon=ft.Icons.DOWNLOAD,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        on_click=on_install_spotdl,
        width=250,
        height=45
    )
    
    install_status = ft.Text(
        value="⚠️ Library 'spotdl' belum terinstall. Klik tombol di atas untuk install.",
        color=ft.Colors.ORANGE_400,
        size=13,
        weight=ft.FontWeight.BOLD
    )
    
    spotdl_alert = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.ORANGE_400, size=48),
            ft.Text(
                "spotdl Belum Terinstall",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            ),
            install_status,
            ft.Divider(height=10, color="transparent"),
            install_btn,
            ft.Divider(height=10, color="transparent"),
            ft.Text(
                "Atau install manual via terminal:\npip install spotdl",
                size=11,
                color=ft.Colors.GREY_400,
                text_align=ft.TextAlign.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.ORANGE_400),
        border=ft.Border.all(2, ft.Colors.ORANGE_700),
        border_radius=10,
        padding=30,
        visible=not spotdl_installed
    )

    # --- KOMPONEN UI ---
    url_input = ft.TextField(
        label="🔗 Link Spotify (Lagu/Album/Playlist)",
        width=600,
        border_color=ft.Colors.GREEN_400,
        focused_border_color=ft.Colors.GREEN_200,
        text_size=14,
        disabled=not spotdl_installed
    )
    
    bitrate_options = ["128k", "192k", "256k", "320k"]
    bitrate_dropdown = ft.Dropdown(
        label="🎧 Bitrate",
        width=120,
        options=[ft.dropdown.Option(opt) for opt in bitrate_options],
        value="320k",
        border_color=ft.Colors.BLUE_400,
        disabled=not spotdl_installed
    )

    # Output folder
    default_output_folder = os.path.join(os.path.expanduser("~"), "Downloads", "Music_Downloads")
    output_folder_field = ft.TextField(
        label="📁 Folder Output (Bisa diedit manual)",
        value=default_output_folder,
        width=520,
        text_size=12,
        border_color=ft.Colors.ORANGE_400,
        disabled=not spotdl_installed,
        hint_text="Edit path atau gunakan default"
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
        border=ft.Border.all(1, ft.Colors.GREY_700),
        border_radius=10,
        heading_row_color=ft.Colors.with_opacity(0.1, ft.Colors.WHITE),
        data_row_max_height=45,
        visible=True
    )
    
    # Footer untuk tabel
    table_footer = ft.Container(
        content=ft.Row([
            ft.Text("✨ Total: ", size=12, color=ft.Colors.GREY_400),
            ft.Text("0", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400, key="footer_total"),
            ft.Text(" lagu | ", size=12, color=ft.Colors.GREY_400),
            ft.Text("✅ Selesai: ", size=12, color=ft.Colors.GREY_400),
            ft.Text("0", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.CYAN_400, key="footer_done"),
            ft.Text(" | ❌ Error: ", size=12, color=ft.Colors.GREY_400),
            ft.Text("0", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.RED_400, key="footer_error"),
        ], alignment=ft.MainAxisAlignment.CENTER),
        padding=10,
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLUE_900),
        border=ft.border.only(top=ft.BorderSide(1, ft.Colors.GREY_600)),
        border_radius=ft.border_radius.only(bottom_left=10, bottom_right=10)
    )
    
    # ListView untuk tabel yang bisa discroll dengan smooth
    table_listview = ft.ListView(
        controls=[song_table],
        spacing=0,
        padding=10,
        auto_scroll=True,  # Auto scroll ke bawah saat ada item baru
        expand=True
    )
    
    # Container scrollable untuk tabel dengan footer
    table_container = ft.Container(
        content=ft.Column([
            ft.Container(
                content=table_listview,
                height=300,
                border=ft.border.only(
                    left=ft.BorderSide(1, ft.Colors.GREY_600),
                    right=ft.BorderSide(1, ft.Colors.GREY_600),
                    top=ft.BorderSide(1, ft.Colors.GREY_600)
                ),
                border_radius=ft.border_radius.only(top_left=10, top_right=10),
                bgcolor=ft.Colors.with_opacity(0.05, ft.Colors.WHITE)
            ),
            table_footer
        ], spacing=0),
        border_radius=10,
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

        # Set environment untuk UTF-8 encoding (fix Unicode error di Windows)
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'

        try:
            process = subprocess.Popen(
                dl_cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                encoding='utf-8',
                errors='replace',  # Replace karakter yang tidak bisa di-encode
                startupinfo=startupinfo,
                env=env,
                bufsize=1
            )

            song_index = 0
            completed_count = 0
            error_count = 0
            current_song = ""
            total_songs = 0
            
            # Fungsi untuk update footer
            def update_footer():
                # Cari text controls di footer
                for control in table_footer.content.controls:
                    if hasattr(control, 'key'):
                        if control.key == "footer_total":
                            control.value = str(total_songs)
                        elif control.key == "footer_done":
                            control.value = str(completed_count)
                        elif control.key == "footer_error":
                            control.value = str(error_count)
            
            for line in process.stdout:
                line = line.strip()
                if not line:
                    continue
                
                # Print untuk debugging (bisa dilihat di console)
                print(f"DEBUG: {line}")
                
                # Deteksi jumlah total lagu
                if "Found" in line and ("song" in line.lower() or "track" in line.lower()):
                    status_text.value = f"📋 {line}"
                    # Extract jumlah lagu
                    import re
                    match = re.search(r'Found (\d+)', line)
                    if match:
                        total_songs = int(match.group(1))
                    update_footer()
                    page.update()
                
                # Deteksi lagu yang berhasil didownload
                # Format: Downloaded "Artist - Title": URL
                if line.startswith("Downloaded") and '"' in line:
                    # Extract nama lagu dari dalam quotes
                    match = re.search(r'Downloaded "(.*?)"', line)
                    if match:
                        song_info = match.group(1)
                        
                        if " - " in song_info:
                            song_index += 1
                            completed_count += 1
                            
                            # Pisahkan Artis dan Judul
                            parts = song_info.split(" - ", 1)
                            artist = parts[0].strip()
                            title = parts[1].strip()
                            
                            row_obj = ft.DataRow(cells=[
                                ft.DataCell(ft.Text(str(song_index), color=ft.Colors.GREY_300)),
                                ft.DataCell(ft.Text(artist[:25] + "..." if len(artist) > 25 else artist, color=ft.Colors.CYAN_200, size=12)),
                                ft.DataCell(ft.Text(title[:35] + "..." if len(title) > 35 else title, color=ft.Colors.WHITE, size=12)),
                                ft.DataCell(ft.Text("-", color=ft.Colors.GREY_400, size=12)),
                                ft.DataCell(get_status_icon("done")),
                            ])
                            song_table.rows.append(row_obj)
                            
                            # Update status dan footer
                            if total_songs > 0:
                                status_text.value = f"🔄 Downloading: {title[:30]}... ({completed_count}/{total_songs})"
                            else:
                                status_text.value = f"🔄 Downloading: {title[:40]}..."
                            
                            update_footer()
                            progress_label.value = f"✅ {completed_count} lagu selesai"
                            
                            # Scroll ke bawah otomatis
                            try:
                                table_listview.scroll_to(offset=-1, duration=100)
                            except:
                                pass
                            
                            page.update()
                
                # Deteksi error
                if "Error" in line and "Provider" in line:
                    error_count += 1
                    # Bisa juga tambahkan row untuk error jika mau
                    status_text.value = f"⚠️ {completed_count} berhasil, {error_count} error"
                    status_text.color = ft.Colors.ORANGE_400
                    update_footer()
                    page.update()
                
                # Update progress bar jika ada info progress
                if "complete" in line.lower() and "/" in line:
                    match = re.search(r'(\d+)/(\d+)', line)
                    if match:
                        current = int(match.group(1))
                        total = int(match.group(2))
                        progress_label.value = f"📊 Progress: {current}/{total}"
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
    btn_download = ft.Button(
        "🚀 Mulai Download",
        bgcolor=ft.Colors.GREEN_700,
        color=ft.Colors.WHITE,
        on_click=on_click_download,
        width=200,
        height=45,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        disabled=not spotdl_installed
    )

    # --- FOOTER ---
    def create_footer():
        """Create footer with social media icons and copyright"""
        return ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=ft.Colors.GREY_800),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.FACEBOOK,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Facebook",
                            on_click=lambda _: None
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CAMERA_ALT,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Instagram",
                            on_click=lambda _: None
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EMAIL,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Email",
                            on_click=lambda _: None
                        ),
                        ft.IconButton(
                            icon=ft.Icons.PHONE,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Phone",
                            on_click=lambda _: None
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                ft.Text(
                    "© 2025 Media Tools Suite. All rights reserved.",
                    size=11,
                    color=ft.Colors.GREY_500,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor="#0f0f1e",  # Darker purple-black matching page bgcolor
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
        )
    
    footer = create_footer()

    # --- LAYOUT ---
    page.add(
        ft.Column(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text("🎵 Spotify Downloader Pro", size=28, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                            ft.Text("Download lagu dari Spotify via YouTube Music", size=12, color=ft.Colors.GREY_400),
                            ft.Divider(height=20, color=ft.Colors.GREY_700),
                            
                            # Alert jika spotdl belum terinstall
                            spotdl_alert,
                            ft.Divider(height=10, color="transparent", visible=not spotdl_installed),
                            
                            url_input,
                            ft.Row([
                                bitrate_dropdown,
                                output_folder_field
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            
                            ft.Divider(height=15, color="transparent"),
                            ft.Row([btn_download], alignment=ft.MainAxisAlignment.CENTER),
                            ft.Divider(height=15, color="transparent"),
                            
                            ft.Row([status_text, progress_label], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            progress_bar,
                            
                            ft.Divider(height=10, color="transparent"),
                            ft.Text("📋 Daftar Lagu:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            table_container
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True
                    ),
                    padding=10,
                    expand=True
                ),
                footer
            ],
            spacing=0,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.run(main)
