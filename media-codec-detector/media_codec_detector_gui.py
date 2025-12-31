import flet as ft
import os
import glob
import threading
import filetype
import ffmpeg
from PIL import Image
from pathlib import Path
import sys

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
                    ft.Icon(ft.Icons.MOVIE, size=40, color=ft.Colors.PURPLE),
                    ft.Text("🎬 Media Codec Detector", 
                           size=28, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Detect container format and codecs from media files", 
                       size=14, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            bgcolor=ft.Colors.PURPLE_50,
            border_radius=10,
            margin=ft.margin.only(bottom=20)
        )
        
        # Mode selection
        self.mode_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="file", label="📄 Single File Analysis"),
                ft.Radio(value="folder", label="📁 Analyze All Files in Folder"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            value="file",
            on_change=self.on_mode_change
        )
        
        mode_section = ft.Container(
            content=ft.Column([
                ft.Text("1. Select Analysis Mode", 
                       size=16, weight=ft.FontWeight.BOLD),
                self.mode_radio,
            ]),
            padding=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=15)
        )
        
        # File/Folder selection
        self.path_text = ft.Text("📁 No file/folder selected", size=14)
        self.select_button = ft.ElevatedButton(
            "Select File",
            icon=ft.Icons.FILE_OPEN,
            on_click=self.pick_file_dialog,
            bgcolor=ft.Colors.PURPLE,
            color=ft.Colors.WHITE
        )
        
        selection_section = ft.Container(
            content=ft.Column([
                ft.Text("2. Select Media File/Folder", 
                       size=16, weight=ft.FontWeight.BOLD),
                ft.Row([self.select_button, self.path_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
            padding=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=15)
        )
        
        # File list (for folder mode)
        self.files_list = ft.Column([], scroll=ft.ScrollMode.AUTO, height=120)
        self.files_section_title = ft.Text("Media Files Found", 
                                           size=16, weight=ft.FontWeight.BOLD)
        self.files_section = ft.Container(
            content=ft.Column([
                self.files_section_title,
                ft.Container(
                    content=self.files_list,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.Colors.GREY_50
                )
            ]),
            visible=False,
            margin=ft.margin.only(bottom=15)
        )
        
        # Analysis button
        self.analyze_button = ft.ElevatedButton(
            "🕵️ Start Analysis",
            icon=ft.Icons.SEARCH,
            on_click=self.start_analysis,
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.all(15)
            ),
            expand=True
        )
        
        # Progress
        self.progress_bar = ft.ProgressBar(visible=False)
        self.status_text = ft.Text("", size=12, color=ft.Colors.GREY_700)
        
        action_section = ft.Column([
            self.progress_bar,
            self.status_text,
            ft.Row([self.analyze_button], alignment=ft.MainAxisAlignment.CENTER),
        ])
        
        # Results section
        self.results_list = ft.Column([], scroll=ft.ScrollMode.AUTO)
        self.results_section_title = ft.Text("📊 Analysis Results", 
                                             size=16, weight=ft.FontWeight.BOLD)
        self.results_section = ft.Container(
            content=ft.Column([
                self.results_section_title,
                ft.Container(
                    content=self.results_list,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.Colors.GREY_50,
                    height=200
                )
            ]),
            visible=False,
            margin=ft.margin.only(top=20)
        )
        
        # Main layout
        # Footer
        footer = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.FACEBOOK,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Facebook"
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CAMERA_ALT,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Instagram"
                        ),
                        ft.IconButton(
                            icon=ft.Icons.EMAIL,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Email"
                        ),
                        ft.IconButton(
                            icon=ft.Icons.PHONE,
                            icon_color=ft.Colors.WHITE70,
                            icon_size=20,
                            tooltip="Phone"
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                ft.Text(
                    "© 2025 Media Tools Suite. All rights reserved.",
                    size=11,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.GREY_900,  # Dark grey for light theme
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
        )
        
        main_content = ft.Column([
            header,
            mode_section,
            selection_section,
            self.files_section,
            action_section,
            self.results_section,
            footer  # Footer inside scrollable content
        ], scroll=ft.ScrollMode.AUTO, expand=True)
        
        self.page.add(main_content)
        self.page.update()
    
    def on_mode_change(self, e):
        """Handle mode selection change"""
        self.analysis_mode = e.control.value
        
        if self.analysis_mode == "file":
            self.select_button.text = "Select File"
            self.select_button.icon = ft.Icons.FILE_OPEN
            self.files_section.visible = False
        else:
            self.select_button.text = "Select Folder"
            self.select_button.icon = ft.Icons.FOLDER_OPEN
            self.files_section.visible = True
        
        # Reset selection
        self.selected_path = ""
        self.media_files = []
        self.path_text.value = "📁 No file/folder selected"
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
                dialog_title="Select Media File",
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
        image_formats = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp', 'ico', 'svg', 'psd', 'raw', 'heic']
        video_formats = ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', '3gp', 'wmv', 'm4v', 'ts', 'mts', 'vob']
        audio_formats = ['mp3', 'aac', 'flac', 'wav', 'ogg', 'm4a', 'wma']
        document_formats = ['pdf', 'doc', 'docx', 'txt', 'xlsx']
        
        all_formats = image_formats + video_formats + audio_formats + document_formats
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
                    icon = ft.Icons.IMAGE
                    color = ft.Colors.BLUE
                elif file_ext in video_formats:
                    icon = ft.Icons.VIDEO_FILE
                    color = ft.Colors.RED
                elif file_ext in audio_formats:
                    icon = ft.Icons.AUDIO_FILE
                    color = ft.Colors.GREEN
                else:
                    icon = ft.Icons.INSERT_DRIVE_FILE
                    color = ft.Colors.GREY
                
                self.files_list.controls.append(
                    ft.Row([
                        ft.Icon(icon, size=16, color=color),
                        ft.Text(f"{i}. {filename}", size=12, expand=True),
                    ])
                )
        else:
            self.files_list.controls.append(
                ft.Text("❌ No media files found", color=ft.Colors.RED)
            )
        
        self.page.update()
    
    def start_analysis(self, e):
        """Start the media analysis process"""
        if not self.media_files:
            self.show_snackbar("❌ Please select a file or folder containing media first!", ft.Colors.RED)
            return
        
        if self.is_processing:
            return
        
        # Start analysis in background thread
        self.is_processing = True
        self.analyze_button.disabled = True
        self.progress_bar.visible = True
        self.status_text.value = "🔄 Starting media analysis..."
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
                progress = (i / total_files) * 100
                self.update_status(f"🕵️ Analyzing ({progress:.0f}%): {filename}")
                self.update_progress(progress / 100)
                
                result = self.analyze_single_file(file_path)
                self.analysis_results.append(result)
                
                # Update results in real-time
                self.add_result_to_ui(result)
            
            self.update_status(f"✅ Analysis Complete! Successfully analyzed {total_files} file(s).")
            self.show_snackbar_safe(f"🎉 Analysis complete for {total_files} files!", ft.Colors.GREEN)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.update_status(error_msg)
            self.show_snackbar_safe(f"❌ Failed to analyze media: {str(e)}", ft.Colors.RED)
        
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
                result['error'] = "File not found"
                return result
            
            # Detect file type
            kind = filetype.guess(file_path)
            if kind is None:
                result['error'] = "Cannot determine file type"
                return result
            
            result['mime_type'] = kind.mime
            result['file_type'] = kind.extension
            
            # Handle different media types
            if 'image' in result['mime_type']:
                result['details'] = self.analyze_image(file_path)
            elif 'video' in result['mime_type'] or 'audio' in result['mime_type']:
                result['details'] = self.analyze_video_audio(file_path)
            else:
                result['details'] = {'type': 'Not a standard media file'}
        
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def get_codec_description(self, codec_name):
        """Get user-friendly description of codec"""
        descriptions = {
            'h264': 'H.264/AVC - Most common video codec, excellent compression',
            'h265': 'H.265/HEVC - Advanced codec, better compression than H.264',
            'vp9': 'VP9 - Google\'s royalty-free codec, used in YouTube',
            'av1': 'AV1 - Next-gen codec, superior compression',
            'mpeg4': 'MPEG-4 - Older codec, still widely supported',
            'aac': 'AAC - Advanced Audio Coding, high quality',
            'mp3': 'MP3 - Universal audio format',
            'opus': 'Opus - Modern codec, excellent for voice',
            'vorbis': 'Vorbis - Open-source audio codec',
            'flac': 'FLAC - Lossless audio, perfect quality',
            'pcm': 'PCM - Uncompressed raw audio',
        }
        codec_lower = codec_name.lower()
        for key, desc in descriptions.items():
            if key in codec_lower:
                return desc
        return 'Unknown codec'
    
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
            details['error'] = f"Cannot read image details: {e}"
        
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
                    codec_name = stream.get('codec_long_name', stream.get('codec_name', 'N/A'))
                    stream_info = {
                        'index': i,
                        'type': stream.get('codec_type', 'unknown'),
                        'codec': codec_name
                    }
                    
                    # Add codec description
                    if codec_name != 'N/A':
                        codec_desc = self.get_codec_description(codec_name)
                        stream_info['codec'] = f"{codec_name}\n   └ {codec_desc}"
                    
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
                        ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED, size=20),
                        ft.Text(filename, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Text("❌ Error", color=ft.Colors.RED)
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.RED_50,
                    border_radius=ft.border_radius.only(top_left=5, top_right=5)
                )
                
                content = ft.Column([
                    header,
                    ft.Container(
                        content=ft.Text(f"Error: {result['error']}", color=ft.Colors.RED, size=12),
                        padding=10
                    )
                ])
            else:
                # Success - show detailed info
                mime_type = result['mime_type']
                details = result['details']
                
                # Choose icon and color based on type
                if 'image' in mime_type:
                    icon = ft.Icons.IMAGE
                    color = ft.Colors.BLUE
                elif 'video' in mime_type:
                    icon = ft.Icons.VIDEO_FILE
                    color = ft.Colors.RED
                elif 'audio' in mime_type:
                    icon = ft.Icons.AUDIO_FILE
                    color = ft.Colors.GREEN
                else:
                    icon = ft.Icons.INSERT_DRIVE_FILE
                    color = ft.Colors.GREY
                
                header = ft.Container(
                    content=ft.Row([
                        ft.Icon(icon, color=color, size=20),
                        ft.Text(filename, weight=ft.FontWeight.BOLD, expand=True),
                        ft.Text("✅ OK", color=ft.Colors.GREEN)
                    ]),
                    padding=10,
                    bgcolor=ft.Colors.GREEN_50,
                    border_radius=ft.border_radius.only(top_left=5, top_right=5)
                )
                
                # Build details content
                details_content = [
                    ft.Text(f"MIME Type: {mime_type}", size=12, weight=ft.FontWeight.BOLD),
                ]
                
                if details.get('type') == 'image':
                    details_content.extend([
                        ft.Text(f"🖼️ Format: {details.get('format', 'N/A')}", size=12),
                        ft.Text(f"📐 Size: {details.get('size', 'N/A')}", size=12),
                        ft.Text(f"🎨 Color Mode: {details.get('mode', 'N/A')}", size=12),
                    ])
                
                elif details.get('type') == 'video_audio':
                    details_content.append(
                        ft.Text(f"📦 Container: {details.get('container', 'N/A')}", size=12)
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
                    details_content.append(ft.Text(f"❌ {details['error']}", color=ft.Colors.RED, size=12))
                
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
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=5,
                margin=ft.margin.only(bottom=10)
            )
            
            self.results_list.controls.append(result_card)
            self.page.update()
        
        self.page.run_thread_safe(update_ui)
    
    def update_progress(self, value):
        """Update progress bar (thread-safe)"""
        def update():
            self.progress_bar.value = value
            self.page.update()
        
        self.page.run_thread_safe(update)
    
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




