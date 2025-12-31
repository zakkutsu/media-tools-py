import flet as ft
import os
import subprocess
import threading
from PIL import Image
from pdf2image import convert_from_path  # Library untuk PDF

def main(page: ft.Page):
    page.title = "Universal Converter V2 (+PDF Support)"
    page.window_width = 650
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # --- KONFIGURASI PATH ---
    # Python akan mencari folder 'poppler' di sebelah script ini
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Path spesifik ke folder 'bin' milik poppler
    POPPLER_BIN_PATH = os.path.join(base_dir, "poppler", "Library", "bin")

    # --- OTAK PINTAR (MAPPING FORMAT) ---
    FORMAT_MAP = {
        # Gambar
        '.jpg':  ['png', 'webp', 'pdf', 'ico', 'bmp'],
        '.jpeg': ['png', 'webp', 'pdf', 'ico', 'bmp'],
        '.png':  ['jpg', 'webp', 'pdf', 'ico', 'bmp'],
        '.webp': ['jpg', 'png', 'pdf'],
        '.bmp':  ['jpg', 'png', 'webp'],
        '.ico':  ['png', 'jpg'],
        
        # PDF (Fitur Baru)
        '.pdf':  ['jpg (Setiap Halaman)', 'png (Setiap Halaman)'],

        # Video
        '.mp4':  ['mp3 (Audio Only)', 'wav (Audio Only)', 'mkv', 'gif (Animasi)', 'avi'],
        '.mkv':  ['mp4', 'mp3 (Audio Only)', 'avi'],
        '.mov':  ['mp4', 'mp3 (Audio Only)'],
        '.avi':  ['mp4', 'mkv', 'mp3 (Audio Only)'],
        
        # Audio
        '.mp3':  ['wav', 'ogg', 'm4a', 'flac'],
        '.wav':  ['mp3', 'ogg', 'm4a', 'flac'],
        '.m4a':  ['mp3', 'wav', 'ogg'],
        '.ogg':  ['mp3', 'wav'],
        '.flac': ['mp3', 'wav', 'ogg'],
    }

    # --- UI COMPONENTS ---
    selected_file = ft.Text("Belum ada file...", italic=True, color=ft.Colors.GREY)
    status_text = ft.Text("Menunggu...", size=16, weight="bold")
    progress_ring = ft.ProgressRing(visible=False)

    def update_status(msg, is_error=False):
        status_text.value = msg
        status_text.color = ft.Colors.RED if is_error else ft.Colors.GREEN
        page.update()

    # --- LOGIC UTAMA ---
    def process_conversion(input_path, target_fmt_raw):
        output_dir = os.path.dirname(input_path)
        filename = os.path.basename(input_path)
        name_only, ext_old = os.path.splitext(filename)
        ext_old = ext_old.lower()

        # Bersihkan nama format target
        clean_ext = target_fmt_raw.split(" ")[0].lower()
        if not clean_ext.startswith("."): 
            clean_ext = "." + clean_ext

        try:
            # === 1. PDF TO IMAGE ===
            if ext_old == '.pdf':
                if not os.path.exists(POPPLER_BIN_PATH):
                    update_status("❌ Error: Folder 'poppler' tidak ditemukan! Lihat README untuk download.", True)
                    return

                update_status("📄 Membaca halaman PDF...", False)
                
                # Convert PDF ke List Gambar
                images = convert_from_path(input_path, poppler_path=POPPLER_BIN_PATH)
                
                total_pages = len(images)
                update_status(f"📄 Menyimpan {total_pages} halaman...", False)

                # Loop untuk menyimpan setiap halaman
                for i, img in enumerate(images):
                    # Nama file: dokumen_page_1.png
                    page_name = f"{name_only}_page_{i+1}{clean_ext}"
                    save_path = os.path.join(output_dir, page_name)
                    
                    # Jika user minta JPG, buang alpha channel
                    if clean_ext in ['.jpg', '.jpeg']:
                        img = img.convert("RGB")
                        
                    img.save(save_path)
                
                update_status(f"✅ Selesai! {total_pages} gambar tersimpan.", False)

            # === 2. GAMBAR KE GAMBAR/PDF ===
            elif ext_old in ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.ico']:
                output_path = os.path.join(output_dir, f"{name_only}_converted{clean_ext}")
                update_status(f"🖼️ Memproses Gambar ke {clean_ext}...", False)
                
                img = Image.open(input_path)

                if clean_ext == '.pdf':
                    # Convert gambar ke PDF
                    if img.mode in ("RGBA", "P"): 
                        img = img.convert("RGB")
                    img.save(output_path, "PDF", resolution=100.0)
                else:
                    # Gambar ke Gambar lain
                    if clean_ext in ['.jpg', '.jpeg'] and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    img.save(output_path)
                
                update_status(f"✅ Gambar tersimpan: {os.path.basename(output_path)}", False)

            # === 3. VIDEO/AUDIO (FFMPEG) ===
            elif ext_old in ['.mp4', '.mkv', '.avi', '.mov', '.mp3', '.wav', '.m4a', '.ogg', '.flac']:
                output_path = os.path.join(output_dir, f"{name_only}_converted{clean_ext}")
                update_status(f"🎬 Memproses Media ke {clean_ext}...", False)
                
                cmd = ['ffmpeg', '-i', input_path]
                
                # Logic tambahan untuk konversi khusus
                if clean_ext == '.mp3':
                    cmd.extend(['-vn', '-ab', '192k'])  # Buang video, bitrate audio 192k
                elif clean_ext == '.gif':
                    cmd.extend(['-vf', 'fps=10,scale=320:-1'])  # Optimasi GIF biar ringan
                elif clean_ext in ['.wav', '.ogg', '.m4a', '.flac']:
                    cmd.extend(['-vn'])  # Hanya ambil audio
                
                cmd.extend([output_path, '-y'])
                
                # Hide CMD window di Windows
                startupinfo = None
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                
                result = subprocess.run(cmd, check=True, startupinfo=startupinfo, 
                                       capture_output=True, text=True)
                
                update_status(f"✅ Media tersimpan: {os.path.basename(output_path)}", False)

            else:
                update_status("❌ Format input belum didukung engine.", True)

        except FileNotFoundError as e:
            if "ffmpeg" in str(e).lower():
                update_status("❌ FFmpeg tidak ditemukan! Download dulu (lihat README).", True)
            else:
                update_status(f"❌ File tidak ditemukan: {str(e)}", True)
        except subprocess.CalledProcessError as e:
            update_status(f"❌ FFmpeg Error: Proses konversi gagal.", True)
        except Exception as e:
            update_status(f"❌ Error: {str(e)}", True)
        
        finally:
            btn_convert.disabled = False
            progress_ring.visible = False
            page.update()

    # --- THREADING ---
    def on_convert_click(e):
        if not selected_file.value or not format_dropdown.value: 
            return
        if selected_file.value == "Belum ada file...":
            return
            
        btn_convert.disabled = True
        progress_ring.visible = True
        
        # Jalankan di background thread
        t = threading.Thread(target=process_conversion, 
                           args=(selected_file.value, format_dropdown.value), 
                           daemon=True)
        t.start()

    # --- FILE PICKER ---
    def on_file_picked(e: ft.FilePickerResultEvent):
        if e.files:
            path = e.files[0].path
            selected_file.value = path
            _, ext = os.path.splitext(path)
            ext = ext.lower()

            if ext in FORMAT_MAP:
                format_dropdown.options = [ft.dropdown.Option(o) for o in FORMAT_MAP[ext]]
                format_dropdown.value = FORMAT_MAP[ext][0]
                format_dropdown.disabled = False
                btn_convert.disabled = False
                update_status("✓ File OK. Pilih format output.", False)
            else:
                format_dropdown.options = []
                format_dropdown.value = None
                format_dropdown.disabled = True
                btn_convert.disabled = True
                update_status(f"⚠️ Format '{ext}' belum didukung.", True)
            
            page.update()

    # --- LAYOUT SETUP ---
    file_picker = ft.FilePicker(on_result=on_file_picked)
    page.overlay.append(file_picker)

    btn_pick = ft.ElevatedButton(
        "Pilih File", 
        icon=ft.Icons.FOLDER_OPEN, 
        on_click=lambda _: file_picker.pick_files(),
        width=200,
        height=45
    )
    
    format_dropdown = ft.Dropdown(
        label="Convert ke format...", 
        width=400, 
        disabled=True,
        hint_text="Pilih file input terlebih dahulu"
    )
    
    btn_convert = ft.ElevatedButton(
        "MULAI KONVERSI", 
        icon=ft.Icons.PLAY_ARROW, 
        disabled=True, 
        on_click=on_convert_click,
        bgcolor=ft.Colors.BLUE_600,
        color=ft.Colors.WHITE,
        width=200,
        height=50
    )

    # Container dengan styling
    container = ft.Container(
        content=ft.Column([
            ft.Icon(ft.Icons.SWAP_HORIZONTAL_CIRCLE, size=70, color=ft.Colors.BLUE_400),
            ft.Text("Universal File Converter", size=28, weight="bold"),
            ft.Text("Support: PDF, Gambar, Audio, Video", size=13, color="grey"),
            ft.Divider(height=30),
            btn_pick,
            ft.Container(selected_file, padding=10),
            ft.Divider(height=20, color="transparent"),
            format_dropdown,
            ft.Divider(height=20, color="transparent"),
            btn_convert,
            ft.Divider(height=20, color="transparent"),
            progress_ring,
            status_text
        ], 
        alignment=ft.MainAxisAlignment.CENTER, 
        horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=40,
        border_radius=15,
        bgcolor=ft.Colors.GREY_900,
        width=580,
        border=ft.border.all(1, ft.Colors.GREY_800)
    )

    page.add(ft.Container(
        content=container,
        alignment=ft.alignment.center,
        expand=True
    ))

if __name__ == "__main__":
    ft.app(target=main)
