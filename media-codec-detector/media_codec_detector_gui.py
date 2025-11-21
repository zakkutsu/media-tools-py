import flet as ft
import os
import glob
import threading
import filetype
import ffmpeg
from PIL import Image
from pathlib import Path

class MediaCodecDetectorGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬 Media Codec Detector"
        self.page.window_width = 800
        self.page.window_height = 700
        self.page.window_min_width = 700
        self.page.window_min_height = 600
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # State variables
        self.selected_path = ""
        self.media_files = []
        self.analysis_results = []
        self.is_processing = False
        self.analysis_mode = "file"  # "file" or "folder"
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface"""
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.MOVIE, size=40, color=ft.colors.PURPLE),
                    ft.Text("Media Codec Detector", size=28, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Deteksi format kontainer dan codec dari file media", 
                       size=14, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.colors.PURPLE_50,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
        
        # Mode selection
        self.mode_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="file", label="📄 Analisis File Tunggal"),
                ft.Radio(value="folder", label="📁 Analisis Semua File dalam Folder"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            value="file",
            on_change=self.on_mode_change
        )
        
        mode_section = ft.Container(
            content=ft.Column([
                ft.Text("1. Pilih Mode Analisis", size=16, weight=ft.FontWeight.BOLD),
                self.mode_radio,
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=15)
        )
        
        # File/Folder selection
        self.path_text = ft.Text("📁 Belum ada file/folder dipilih", size=14)
        self.select_button = ft.ElevatedButton(
            "Pilih File",
            icon=ft.icons.FILE_OPEN,
            on_click=self.pick_file_dialog,
            bgcolor=ft.colors.PURPLE,
            color=ft.colors.WHITE
        )
        
        selection_section = ft.Container(
            content=ft.Column([
                ft.Text("2. Pilih File/Folder Media", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.select_button, self.path_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=15)
        )
        
        # File list (for folder mode)
        self.files_list = ft.Column([], scroll=ft.ScrollMode.AUTO, height=120)
        self.files_section = ft.Container(
            content=ft.Column([
                ft.Text("File Media Ditemukan", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.files_list,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.colors.GREY_50
                )
            ]),
            visible=False,
            margin=ft.margin.only(bottom=15)
        )
        
        # Analysis button
        self.analyze_button = ft.ElevatedButton(
            "🕵️ Mulai Analisis",
            icon=ft.icons.SEARCH,
            on_click=self.start_analysis,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.all(15)
            ),
            expand=True
        )
        
        # Progress
        self.progress_bar = ft.ProgressBar(visible=False)
        self.status_text = ft.Text("", size=12, color=ft.colors.GREY_700)
        
        action_section = ft.Column([
            self.progress_bar,
            self.status_text,
            ft.Row([self.analyze_button], alignment=ft.MainAxisAlignment.CENTER),
        ])
        
        # Results section
        self.results_list = ft.Column([], scroll=ft.ScrollMode.AUTO)
        self.results_section = ft.Container(
            content=ft.Column([
                ft.Text("📊 Hasil Analisis", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.results_list,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.colors.GREY_50,
                    height=200
                )
            ]),
            visible=False,
            margin=ft.margin.only(top=20)
        )
        
        # Create dummy files section
        self.dummy_button = ft.ElevatedButton(
            "🧪 Buat File Dummy untuk Testing",
            icon=ft.icons.SCIENCE,
            on_click=self.create_dummy_files,
            bgcolor=ft.colors.ORANGE,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.all(10)
            )
        )
        
        dummy_section = ft.Container(
            content=ft.Column([
                ft.Text("🧪 Utilities", size=16, weight=ft.FontWeight.BOLD),
                self.dummy_button,
                ft.Text("Buat file test untuk demonstrasi analisis", size=12, color=ft.colors.GREY_600)
            ]),
            padding=15,
            border=ft.border.all(1, ft.colors.ORANGE_200),
            border_radius=8,
            margin=ft.margin.only(top=20)
        )
        
        # Main layout
        main_content = ft.Column([
            header,
            mode_section,
            selection_section,
            self.files_section,
            action_section,
            self.results_section,
            dummy_section,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.page.add(main_content)
        self.page.update()
    
    def on_mode_change(self, e):
        """Handle mode selection change"""
        self.analysis_mode = e.control.value
        
        if self.analysis_mode == "file":
            self.select_button.text = "Pilih File"
            self.select_button.icon = ft.icons.FILE_OPEN
            self.files_section.visible = False
        else:
            self.select_button.text = "Pilih Folder"
            self.select_button.icon = ft.icons.FOLDER_OPEN
            self.files_section.visible = True
        
        # Reset selection
        self.selected_path = ""
        self.media_files = []
        self.path_text.value = "📁 Belum ada file/folder dipilih"
        self.files_list.controls.clear()
        self.results_list.controls.clear()
        self.results_section.visible = False
        
        self.page.update()
    
    def pick_file_dialog(self, e):
        """Open file/folder picker dialog"""
        if self.analysis_mode == "file":
            def get_file_result(e: ft.FilePickerResultEvent):
                if e.files:
                    file_path = e.files[0].path
                    self.selected_path = file_path
                    self.path_text.value = f"📄 {os.path.basename(file_path)}"
                    self.media_files = [file_path]
                    self.page.update()
            
            get_file_dialog = ft.FilePicker(on_result=get_file_result)
            self.page.overlay.append(get_file_dialog)
            self.page.update()
            get_file_dialog.pick_files(
                dialog_title="Pilih File Media",
                allow_multiple=False,
                allowed_extensions=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "webp", "ico", 
                                   "mp4", "avi", "mov", "mkv", "webm", "flv", "3gp", "wmv",
                                   "mp3", "aac", "flac", "wav", "ogg", "m4a", "wma"]
            )
        else:
            def get_directory_result(e: ft.FilePickerResultEvent):
                if e.path:
                    self.selected_path = e.path
                    self.path_text.value = f"📁 {os.path.basename(e.path)}"
                    self.scan_media_files()
                    self.page.update()
            
            get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
            self.page.overlay.append(get_directory_dialog)
            self.page.update()
            get_directory_dialog.get_directory_path()
    
    def scan_media_files(self):
        """Scan folder for media files"""
        if not self.selected_path or self.analysis_mode != "folder":
            return
            
        # Define supported media formats
        image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico']
        video_formats = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', '3gp', 'wmv']
        audio_formats = ['mp3', 'aac', 'flac', 'wav', 'ogg', 'm4a', 'wma']
        
        all_formats = image_formats + video_formats + audio_formats
        self.media_files = []
        
        for format_ext in all_formats:
            pattern = os.path.join(self.selected_path, f"*.{format_ext}")
            files = glob.glob(pattern, recursive=False)
            self.media_files.extend(files)
        
        # Also scan for uppercase extensions
        for format_ext in all_formats:
            pattern = os.path.join(self.selected_path, f"*.{format_ext.upper()}")
            files = glob.glob(pattern, recursive=False)
            self.media_files.extend(files)
        
        # Remove duplicates and sort
        self.media_files = list(set(self.media_files))
        self.media_files.sort()
        
        # Update UI
        self.files_list.controls.clear()
        
        if self.media_files:
            for i, file_path in enumerate(self.media_files, 1):
                filename = os.path.basename(file_path)
                file_ext = filename.split('.')[-1].lower()
                
                # Choose icon based on file type
                if file_ext in image_formats:
                    icon = ft.icons.IMAGE
                    color = ft.colors.BLUE
                elif file_ext in video_formats:
                    icon = ft.icons.VIDEO_FILE
                    color = ft.colors.RED
                elif file_ext in audio_formats:
                    icon = ft.icons.AUDIO_FILE
                    color = ft.colors.GREEN
                else:
                    icon = ft.icons.INSERT_DRIVE_FILE
                    color = ft.colors.GREY
                
                self.files_list.controls.append(
                    ft.Row([
                        ft.Icon(icon, size=16, color=color),
                        ft.Text(f"{i}. {filename}", size=12, expand=True),
                    ])
                )
        else:
            self.files_list.controls.append(
                ft.Text("❌ Tidak ada file media ditemukan", color=ft.colors.RED)
            )
        
        self.page.update()
    
    def start_analysis(self, e):
        """Start the media analysis process"""
        if not self.media_files:
            self.show_snackbar("❌ Pilih file atau folder yang berisi media terlebih dahulu!", ft.colors.RED)
            return
        
        if self.is_processing:
            return
        
        # Start analysis in background thread
        self.is_processing = True
        self.analyze_button.disabled = True
        self.progress_bar.visible = True
        self.status_text.value = "🔄 Memulai analisis media..."
        self.results_list.controls.clear()
        self.results_section.visible = True
        self.page.update()
        
        # Run analysis in thread to avoid blocking UI
        threading.Thread(target=self.analyze_media_files, daemon=True).start()
    
    def analyze_media_files(self):
        """Analyze media files (runs in background thread)"""
        try:
            self.analysis_results = []
            total_files = len(self.media_files)
            
            for i, file_path in enumerate(self.media_files, 1):
                filename = os.path.basename(file_path)
                self.update_status(f"🕵️ Menganalisis file {i}/{total_files}: {filename}")
                
                result = self.analyze_single_file(file_path)
                self.analysis_results.append(result)
                
                # Update results in real-time
                self.add_result_to_ui(result)
            
            self.update_status(f"✅ Analisis selesai! {total_files} file dianalisis.")
            self.show_snackbar_safe(f"🎉 Analisis selesai untuk {total_files} file!", ft.colors.GREEN)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.update_status(error_msg)
            self.show_snackbar_safe(f"❌ Gagal menganalisis media: {str(e)}", ft.colors.RED)
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.analyze_button.disabled = False
            self.progress_bar.visible = False
            self.page.update()
    
    def analyze_single_file(self, file_path):
        """Analyze a single media file"""
        result = {
            'file_path': file_path,
            'filename': os.path.basename(file_path),
            'error': None,
            'mime_type': None,
            'file_type': None,
            'details': {}
        }
        
        try:
            if not os.path.exists(file_path):
                result['error'] = "File tidak ditemukan"
                return result
            
            # Detect file type
            kind = filetype.guess(file_path)
            if kind is None:
                result['error'] = "Tidak dapat menentukan tipe file"
                return result
            
            result['mime_type'] = kind.mime
            result['file_type'] = kind.extension
            
            # Handle different media types
            if 'image' in result['mime_type']:
                result['details'] = self.analyze_image(file_path)
            elif 'video' in result['mime_type'] or 'audio' in result['mime_type']:
                result['details'] = self.analyze_video_audio(file_path)
            else:
                result['details'] = {'type': 'Bukan file media standar'}
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def analyze_image(self, file_path):
        """Analyze image file"""
        details = {}
        try:
            with Image.open(file_path) as img:
                details['format'] = img.format
                details['mode'] = img.mode
                details['size'] = f"{img.width}x{img.height}"
                details['type'] = 'image'
        except Exception as e:
            details['error'] = f"Tidak dapat membaca detail gambar: {e}"
        
        return details
    
    def analyze_video_audio(self, file_path):
        """Analyze video/audio file using ffmpeg"""
        details = {}
        try:
            probe = ffmpeg.probe(file_path)
            
            # Get container format
            container_format = probe.get('format', {}).get('format_long_name', 'N/A')
            details['container'] = container_format
            details['streams'] = []
            
            # Analyze streams
            if 'streams' in probe:
                for i, stream in enumerate(probe['streams']):
                    stream_info = {
                        'index': i,
                        'type': stream.get('codec_type', 'unknown'),
                        'codec': stream.get('codec_long_name', stream.get('codec_name', 'N/A'))
                    }
                    
                    # Add extra details
                    if stream_info['type'] == 'video':
                        stream_info['resolution'] = f"{stream.get('width', 'N/A')}x{stream.get('height', 'N/A')}"
                        stream_info['fps'] = stream.get('r_frame_rate', 'N/A')
                    elif stream_info['type'] == 'audio':
                        stream_info['sample_rate'] = f"{stream.get('sample_rate', 'N/A')} Hz"
                        stream_info['channels'] = stream.get('channels', 'N/A')
                    
                    details['streams'].append(stream_info)
            
            details['type'] = 'video_audio'
        
        except ffmpeg.Error as e:
            details['error'] = f"FFmpeg error: {e.stderr.decode('utf-8') if e.stderr else str(e)}"
        except Exception as e:
            details['error'] = f"Error: {str(e)}"
        
        return details
    
    def add_result_to_ui(self, result):
        """Add analysis result to UI (thread-safe)"""
        def update_ui():
            # Create result card
            filename = result['filename']
            
            # Header with filename and status
            if result['error']:
                header = ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.ERROR, color=ft.colors.RED, size=20),
                        ft.Text(filename, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Text("❌ Error", color=ft.colors.RED)
                    ]),
                    padding=10,
                    bgcolor=ft.colors.RED_50,
                    border_radius=ft.border_radius.only(top_left=5, top_right=5)
                )
                
                content = ft.Column([
                    header,
                    ft.Container(
                        content=ft.Text(f"Error: {result['error']}", color=ft.colors.RED, size=12),
                        padding=10
                    )
                ])
            else:
                # Success - show detailed info
                mime_type = result['mime_type']
                details = result['details']
                
                # Choose icon and color based on type
                if 'image' in mime_type:
                    icon = ft.icons.IMAGE
                    color = ft.colors.BLUE
                elif 'video' in mime_type:
                    icon = ft.icons.VIDEO_FILE
                    color = ft.colors.RED
                elif 'audio' in mime_type:
                    icon = ft.icons.AUDIO_FILE
                    color = ft.colors.GREEN
                else:
                    icon = ft.icons.INSERT_DRIVE_FILE
                    color = ft.colors.GREY
                
                header = ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=color, size=20),
                        ft.Text(filename, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Text("✅ OK", color=ft.colors.GREEN)
                    ]),
                    padding=10,
                    bgcolor=ft.colors.GREEN_50,
                    border_radius=ft.border_radius.only(top_left=5, top_right=5)
                )
                
                # Build details content
                details_content = [
                    ft.Text(f"MIME Type: {mime_type}", size=12, weight=ft.FontWeight.BOLD),
                ]
                
                if details.get('type') == 'image':
                    details_content.extend([
                        ft.Text(f"🖼️ Format: {details.get('format', 'N/A')}", size=12),
                        ft.Text(f"📐 Ukuran: {details.get('size', 'N/A')}", size=12),
                        ft.Text(f"🎨 Mode Warna: {details.get('mode', 'N/A')}", size=12),
                    ])
                
                elif details.get('type') == 'video_audio':
                    details_content.append(
                        ft.Text(f"📦 Kontainer: {details.get('container', 'N/A')}", size=12)
                    )
                    
                    if details.get('streams'):
                        details_content.append(ft.Text("Streams:", size=12, weight=ft.FontWeight.BOLD))
                        for stream in details['streams']:
                            stream_type = stream['type'].upper()
                            codec = stream['codec']
                            
                            stream_text = f"  Stream #{stream['index']} ({stream_type}): {codec}"
                            
                            if stream['type'] == 'video' and 'resolution' in stream:
                                stream_text += f" - {stream['resolution']}"
                            elif stream['type'] == 'audio' and 'sample_rate' in stream:
                                stream_text += f" - {stream['sample_rate']}, {stream['channels']} ch"
                            
                            details_content.append(ft.Text(stream_text, size=11))
                
                elif details.get('error'):
                    details_content.append(ft.Text(f"❌ {details['error']}", color=ft.colors.RED, size=12))
                
                content = ft.Column([
                    header,
                    ft.Container(
                        content=ft.Column(details_content),
                        padding=10
                    )
                ])
            
            # Add result card
            result_card = ft.Container(
                content=content,
                border=ft.border.all(1, ft.colors.GREY_300),
                border_radius=5,
                margin=ft.margin.only(bottom=10)
            )
            
            self.results_list.controls.append(result_card)
            self.page.update()
        
        self.page.run_thread_safe(update_ui)
    
    def create_dummy_files(self, e):
        """Create dummy files for testing"""
        if self.is_processing:
            return
        
        self.is_processing = True
        self.dummy_button.disabled = True
        self.progress_bar.visible = True
        self.status_text.value = "🧪 Membuat file dummy..."
        self.page.update()
        
        # Run in thread
        threading.Thread(target=self.create_dummy_files_thread, daemon=True).start()
    
    def create_dummy_files_thread(self):
        """Create dummy files (runs in background thread)"""
        try:
            dummy_files = []
            
            # Create dummy images
            self.update_status("🖼️ Membuat file gambar dummy...")
            try:
                img = Image.new('RGB', (200, 100), color='red')
                img.save('test_image.png', 'PNG')
                img.save('test_image.jpg', 'JPEG')
                dummy_files.extend(['test_image.png', 'test_image.jpg'])
                self.update_status("✅ File gambar dummy berhasil dibuat")
            except Exception as e:
                self.update_status(f"❌ Gagal membuat file gambar: {e}")
            
            # Create dummy video and audio using ffmpeg
            self.update_status("🎬 Membuat file media dummy...")
            try:
                # Video: H.264 + AAC dalam .mp4
                (
                    ffmpeg
                    .input('lavfi:testsrc=size=192x108:rate=1:duration=1', format='lavfi')
                    .input('lavfi:sine=frequency=1000:duration=1', format='lavfi')
                    .output('test_video.mp4', vcodec='libx264', acodec='aac', shortest=None, loglevel='quiet')
                    .overwrite_output()
                    .run()
                )
                
                # Audio: MP3
                (
                    ffmpeg
                    .input('lavfi:sine=frequency=440:duration=2', format='lavfi')
                    .output('test_audio.mp3', acodec='libmp3lame', loglevel='quiet')
                    .overwrite_output()
                    .run()
                )
                dummy_files.extend(['test_video.mp4', 'test_audio.mp3'])
                self.update_status("✅ File media dummy berhasil dibuat")
                
            except FileNotFoundError:
                self.update_status("⚠️ FFmpeg tidak ditemukan, melewatkan file media dummy")
            except Exception as e:
                self.update_status(f"❌ Gagal membuat file media: {e}")
            
            if dummy_files:
                self.update_status(f"🎉 {len(dummy_files)} file dummy berhasil dibuat!")
                self.show_snackbar_safe(f"✅ {len(dummy_files)} file dummy siap untuk dianalisis!", ft.colors.GREEN)
                
                # Auto-select current directory if no path selected
                if not self.selected_path:
                    current_dir = os.getcwd()
                    self.selected_path = current_dir
                    self.path_text.value = f"📁 {os.path.basename(current_dir)} (auto-selected)"
                    if self.analysis_mode == "folder":
                        self.scan_media_files()
                    else:
                        # Switch to folder mode for convenience
                        self.analysis_mode = "folder"
                        self.mode_radio.value = "folder"
                        self.select_button.text = "Pilih Folder"
                        self.select_button.icon = ft.icons.FOLDER_OPEN
                        self.files_section.visible = True
                        self.scan_media_files()
                    
                    self.page.update()
            else:
                self.update_status("❌ Tidak ada file dummy yang berhasil dibuat")
                self.show_snackbar_safe("❌ Gagal membuat file dummy", ft.colors.RED)
        
        except Exception as e:
            self.update_status(f"❌ Error membuat dummy files: {e}")
            self.show_snackbar_safe(f"❌ Error: {str(e)}", ft.colors.RED)
        
        finally:
            # Reset UI state
            self.is_processing = False
            self.dummy_button.disabled = False
            self.progress_bar.visible = False
            self.page.update()
    
    def update_status(self, message):
        """Update status text (thread-safe)"""
        def update():
            self.status_text.value = message
            self.page.update()
        
        self.page.run_thread_safe(update)
    
    def show_snackbar(self, message, color):
        """Show snackbar notification"""
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=3000
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()
    
    def show_snackbar_safe(self, message, color):
        """Thread-safe snackbar"""
        def show():
            self.show_snackbar(message, color)
        
        self.page.run_thread_safe(show)

def main(page: ft.Page):
    """Main function for Flet app"""
    app = MediaCodecDetectorGUI(page)

if __name__ == "__main__":
    # Check if running from command line with --cli flag
    import sys
    if "--cli" in sys.argv:
        # Import and run CLI version
        from media_codec_detector import analyze_files_from_input
        analyze_files_from_input()
    else:
        # Run GUI version
        ft.app(target=main, view=ft.AppView.FLET_APP)