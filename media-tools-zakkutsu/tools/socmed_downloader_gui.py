import flet as ft
import yt_dlp
import os
import sys
import threading
import time
from pathlib import Path

# Ensure language_config can be imported from current directory
_current_file_dir = Path(__file__).parent.resolve()
_lang_config_path = _current_file_dir / "language_config.py"

# Import language_config from THIS folder specifically
import importlib.util
spec = importlib.util.spec_from_file_location("socmed_language_config", _lang_config_path)
if spec and spec.loader:
    socmed_lang_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(socmed_lang_module)
    get_text = socmed_lang_module.get_text
    LANGUAGES = socmed_lang_module.LANGUAGES
else:
    # Fallback
    def get_text(lang, key, **kwargs):
        return key
    LANGUAGES = {}

class SocMedDownloaderGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🌐 SocMed Downloader"
        self.page.window_width = 900
        self.page.window_height = 800
        self.page.window_resizable = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 10
        
        # State
        self.current_lang = 'id'
        self.download_folder = str(Path.home() / "Downloads" / "SocMed_Downloads")
        self.download_mode = 'single'  # 'single' or 'batch'
        self.batch_file_path = None
        
        # Statistics tracking
        self.start_time = None
        self.download_count = 0
        
        # File picker
        self.file_picker = ft.FilePicker(on_result=self.file_picker_result)
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the main user interface"""
        
        # Create scrollable column for main content
        main_content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10
        )
        
        # Language selector section (top right)
        self.lang_dropdown = ft.Dropdown(
            label=get_text(self.current_lang, 'language_label'),
            width=200,
            options=[
                ft.dropdown.Option("id", "🇮🇩 Bahasa Indonesia"),
                ft.dropdown.Option("en", "🇺🇸 English"),
                ft.dropdown.Option("jp", "🇯🇵 日本語"),
            ],
            value=self.current_lang,
            on_change=self.change_language,
        )
        
        lang_section = ft.Container(
            content=ft.Row([self.lang_dropdown], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(lang_section)
        
        # Title Section (centered)
        title_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    get_text(self.current_lang, 'app_title'),
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    get_text(self.current_lang, 'subtitle'),
                    size=14,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Container(height=5),
                ft.Container(
                    content=ft.Text(
                        "🌐 " + get_text(self.current_lang, 'platform_support'),
                        size=13,
                        color=ft.Colors.WHITE,
                        weight=ft.FontWeight.W_500,
                        text_align=ft.TextAlign.CENTER
                    ),
                    bgcolor=ft.Colors.BLUE_600,
                    border_radius=20,
                    padding=ft.padding.symmetric(horizontal=20, vertical=8),
                )
            ]),
            padding=ft.padding.only(bottom=20)
        )
        main_content.controls.append(title_section)
        
        # Download Folder Section
        folder_section = self.create_folder_section()
        main_content.controls.append(folder_section)
        
        # Input Management Section
        input_section = self.create_input_management_section()
        main_content.controls.append(input_section)
        
        # Download Options Section
        options_section = self.create_download_options_section()
        main_content.controls.append(options_section)
        
        # Download Buttons Section
        buttons_section = self.create_buttons_section()
        main_content.controls.append(buttons_section)
        
        # Progress Section
        progress_section = self.create_progress_section()
        main_content.controls.append(progress_section)
        
        # Output Log Section
        output_section = self.create_output_section()
        main_content.controls.append(output_section)
        
        # Add file picker to overlay
        self.page.overlay.append(self.file_picker)
        
        # Add main content to page
        self.page.add(main_content)
    
    def create_folder_section(self):
        """Create download folder section"""
        self.folder_field = ft.TextField(
            label=get_text(self.current_lang, 'download_folder_label'),
            value=self.download_folder,
            expand=True,
            on_change=self.on_folder_change
        )
        
        browse_btn = ft.ElevatedButton(
            text=get_text(self.current_lang, 'batch_file_button') or "Browse",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self.browse_folder
        )
        
        return ft.Container(
            content=ft.Row([self.folder_field, browse_btn]),
            padding=ft.padding.only(bottom=10)
        )
    
    def create_input_management_section(self):
        """Create input management section similar to yt downloader"""
        # Download Mode selector
        self.mode_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="single", label=get_text(self.current_lang, 'mode_single')),
                ft.Radio(value="batch", label=get_text(self.current_lang, 'mode_batch')),
            ]),
            value="single",
            on_change=self.change_mode,
        )
        
        # Batch file picker button
        self.batch_file_btn = ft.ElevatedButton(
            text=get_text(self.current_lang, 'batch_file_button'),
            icon=ft.Icons.FILE_OPEN,
            on_click=lambda _: self.file_picker.pick_files(
                allowed_extensions=['txt', 'csv', 'json'],
                dialog_title=get_text(self.current_lang, 'batch_file_label'),
            ),
            visible=False,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100)
        )
        
        # Batch file info
        self.batch_file_info = ft.Text(
            get_text(self.current_lang, 'batch_supported'),
            size=11,
            color=ft.Colors.GREY_600,
            italic=True,
            visible=False,
        )
        
        # Selected file display
        self.selected_file_text = ft.Text(
            "",
            size=12,
            color=ft.Colors.BLUE_700,
            weight=ft.FontWeight.W_500,
            visible=False,
        )
        
        # URL Input
        self.url_input = ft.TextField(
            label=get_text(self.current_lang, 'url_label'),
            hint_text=get_text(self.current_lang, 'url_hint'),
            expand=True,
            multiline=False,
            autocorrect=False,
            on_submit=self.on_url_submit
        )
        
        # Add URL button
        add_url_btn = ft.ElevatedButton(
            text="Add URL",
            icon=ft.Icons.ADD,
            on_click=self.on_url_submit,
            visible=False  # Will be shown in batch mode
        )
        
        # URL input row
        url_input_row = ft.Row([self.url_input, add_url_btn])
        
        # URL list for batch mode
        self.url_list = ft.ListView(
            height=150,
            spacing=5,
            padding=ft.padding.all(10)
        )
        
        self.url_list_container = ft.Container(
            content=self.url_list,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            bgcolor=ft.Colors.GREY_50,
            visible=False
        )
        
        # URL count display
        self.url_count_text = ft.Text(
            "URLs: 0", 
            weight=ft.FontWeight.BOLD, 
            size=12,
            visible=False
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "🔗 " + get_text(self.current_lang, 'mode_label'), 
                    size=16, 
                    weight=ft.FontWeight.BOLD
                ),
                self.mode_radio,
                ft.Container(height=10),
                self.batch_file_btn,
                self.batch_file_info,
                self.selected_file_text,
                ft.Container(height=10),
                ft.Text(
                    get_text(self.current_lang, 'url_label'),
                    size=12,
                    weight=ft.FontWeight.BOLD
                ),
                url_input_row,
                ft.Container(height=5),
                # Platform badges - Social Media Focus
                ft.Row([
                    ft.Container(
                        content=ft.Text("TikTok", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLACK,
                        border_radius=5,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                    ft.Container(
                        content=ft.Text("Instagram", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.PINK_600,
                        border_radius=5,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                    ft.Container(
                        content=ft.Text("Facebook", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLUE_700,
                        border_radius=5,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                    ft.Container(
                        content=ft.Text("X/Twitter", size=10, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLUE_900,
                        border_radius=5,
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    ),
                ], wrap=True, spacing=5),
                ft.Container(height=5),
                self.url_count_text,
                self.url_list_container,
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(15),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_download_options_section(self):
        """Create download options section similar to yt downloader"""
        # Format selector with radio group
        self.format_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="video", label="🎬 " + get_text(self.current_lang, 'format_video')),
                ft.Radio(value="audio", label="🎵 " + get_text(self.current_lang, 'format_audio')),
            ]),
            value="video",
            on_change=self.on_format_change,
        )
        
        # Quality selector
        self.quality_dropdown = ft.Dropdown(
            label=get_text(self.current_lang, 'quality_label'),
            width=300,
            options=[
                ft.dropdown.Option("best", get_text(self.current_lang, 'quality_best')),
                ft.dropdown.Option("1080", get_text(self.current_lang, 'quality_1080p')),
                ft.dropdown.Option("720", get_text(self.current_lang, 'quality_720p')),
                ft.dropdown.Option("480", get_text(self.current_lang, 'quality_480p')),
            ],
            value="best",
        )
        
        # Cookies selector
        self.cookies_dropdown = ft.Dropdown(
            label=get_text(self.current_lang, 'cookies_label'),
            width=300,
            options=[
                ft.dropdown.Option("none", get_text(self.current_lang, 'cookies_none')),
                ft.dropdown.Option("chrome", get_text(self.current_lang, 'cookies_chrome')),
                ft.dropdown.Option("edge", get_text(self.current_lang, 'cookies_edge')),
                ft.dropdown.Option("firefox", get_text(self.current_lang, 'cookies_firefox')),
                ft.dropdown.Option("brave", get_text(self.current_lang, 'cookies_brave')),
            ],
            value="none",
        )
        
        # Help text for cookies
        self.cookies_help = ft.Text(
            get_text(self.current_lang, 'help_cookies'),
            size=10,
            color=ft.Colors.GREY_600,
            italic=True,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "⚙️ " + get_text(self.current_lang, 'format_label'), 
                    size=16, 
                    weight=ft.FontWeight.BOLD
                ),
                self.format_radio,
                ft.Container(height=10),
                ft.Row([
                    self.quality_dropdown,
                    ft.Container(width=20),
                    self.cookies_dropdown,
                ]),
                ft.Container(height=5),
                self.cookies_help,
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(15),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_buttons_section(self):
        """Create buttons section similar to yt downloader"""
        # Main download button
        self.download_btn = ft.ElevatedButton(
            text="🚀 " + get_text(self.current_lang, 'download_button'),
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_download,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_600,
            ),
        )
        
        # Clear button
        self.clear_btn = ft.OutlinedButton(
            text="🗑️ " + get_text(self.current_lang, 'clear_button'),
            icon=ft.Icons.CLEAR,
            on_click=self.clear_form,
            width=140,
            height=50,
        )
        
        # Retry failed button (for batch mode)
        self.retry_failed_btn = ft.ElevatedButton(
            text="🔄 Retry Failed",
            icon=ft.Icons.REFRESH,
            on_click=self.retry_failed_downloads,
            width=150,
            height=50,
            disabled=True,
            visible=False,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.ORANGE_600
            )
        )
        
        return ft.Container(
            content=ft.Row([
                self.download_btn,
                self.retry_failed_btn,
                self.clear_btn,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=ft.padding.symmetric(vertical=20)
        )
    
    def create_progress_section(self):
        """Create progress section with enhanced details"""
        # Progress label and bar
        self.progress_label = ft.Text(
            get_text(self.current_lang, 'status_ready'), 
            size=12, 
            weight=ft.FontWeight.BOLD
        )
        self.progress_bar = ft.ProgressBar(value=0, expand=True)
        
        # Enhanced progress info
        self.speed_label = ft.Text(get_text(self.current_lang, 'speed_label') + ": -- MB/s", size=11, color=ft.Colors.BLUE_600)
        self.eta_label = ft.Text(get_text(self.current_lang, 'eta_label') + ": --:--", size=11, color=ft.Colors.GREEN_600)
        self.stats_text = ft.Text("", size=11, color=ft.Colors.GREY_700)
        
        # Info container (for platform and title detection)
        self.info_container = ft.Container(
            content=ft.Column([]),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=10,
            visible=False,
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 " + get_text(self.current_lang, 'progress_section_title'), size=16, weight=ft.FontWeight.BOLD),
                self.info_container,
                ft.Container(height=5),
                self.progress_label,
                ft.Container(
                    content=self.progress_bar,
                    padding=ft.padding.symmetric(vertical=5)
                ),
                ft.Row([
                    self.speed_label,
                    ft.Text("│", color=ft.Colors.GREY_400),
                    self.eta_label,
                ], spacing=10),
                self.stats_text,
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(10),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_output_section(self):
        """Create output log section"""
        self.output_log = ft.ListView(
            height=200,
            spacing=2,
            padding=ft.padding.all(10),
            auto_scroll=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📋 " + get_text(self.current_lang, 'log_section_title'), size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.output_log,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    bgcolor=ft.Colors.GREY_50
                )
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )

    
    def on_folder_change(self, e):
        """Handle folder field change"""
        self.download_folder = e.control.value
    
    def browse_folder(self, e):
        """Browse for download folder"""
        def get_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.download_folder = e.path
                self.folder_field.value = e.path
                self.page.update()
        
        # Create file picker for directory
        get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
        self.page.overlay.append(get_directory_dialog)
        self.page.update()
        
        get_directory_dialog.get_directory_path(
            dialog_title="Select Download Folder",
            initial_directory=self.download_folder
        )
    
    def on_url_submit(self, e):
        """Handle URL input submit"""
        # For single mode, this is just submit
        # For batch mode, this adds URL to list
        if self.download_mode == 'batch':
            self.add_url_to_list()
    
    def add_url_to_list(self):
        """Add URL to batch list"""
        url = self.url_input.value.strip() if self.url_input.value else ""
        if not url:
            return
        
        # Add to UI list
        url_item = ft.ListTile(
            title=ft.Text(url, size=12),
            subtitle=ft.Text(get_text(self.current_lang, 'ready_status'), color=ft.Colors.BLUE_600),
            trailing=ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color=ft.Colors.RED_400,
                tooltip="Remove URL",
                on_click=lambda e, url=url: self.remove_url_from_list(url)
            )
        )
        self.url_list.controls.append(url_item)
        
        self.url_input.value = ""
        self.update_url_count()
        self.log_output(f"✅ URL added: {url}")
        self.page.update()
    
    def remove_url_from_list(self, url):
        """Remove URL from batch list"""
        for i, control in enumerate(self.url_list.controls):
            if hasattr(control, 'title') and control.title.value == url:
                self.url_list.controls.pop(i)
                break
        
        self.update_url_count()
        self.log_output(f"🗑️ URL removed: {url}")
        self.page.update()
    
    def update_url_count(self):
        """Update URL count display"""
        count = len(self.url_list.controls)
        self.url_count_text.value = f"URLs: {count}"
        if count > 0:
            self.url_count_text.visible = True
        self.page.update()
    
    def retry_failed_downloads(self, e):
        """Retry failed downloads - placeholder for now"""
        self.log_output("🔄 Retry functionality not implemented yet")
    
    def log_output(self, message):
        """Add message to output log"""
        try:
            log_entry = ft.Text(
                message,
                size=10,
                selectable=True
            )
            self.output_log.controls.append(log_entry)
            
            # Keep only last 100 entries
            if len(self.output_log.controls) > 100:
                self.output_log.controls.pop(0)
            
            self.page.update()
        except Exception as e:
            pass
    
    def change_language(self, e):
        """Change the interface language"""
        self.current_lang = e.control.value
        # Rebuild UI with new language
        self.page.controls.clear()
        self.page.overlay.clear()
        self.page.overlay.append(self.file_picker)
        self.build_ui()
        self.page.update()
    
    def change_mode(self, e):
        """Change download mode between single and batch"""
        self.download_mode = e.control.value
        
        if self.download_mode == 'batch':
            # Show batch elements
            self.batch_file_btn.visible = True
            self.batch_file_info.visible = True
            self.url_list_container.visible = True
            self.retry_failed_btn.visible = True
            # Change URL input label
            self.url_input.label = "🔗 Add URL to Batch List"
        else:
            # Hide batch elements
            self.batch_file_btn.visible = False
            self.batch_file_info.visible = False
            self.selected_file_text.visible = False
            self.url_list_container.visible = False
            self.url_count_text.visible = False
            self.retry_failed_btn.visible = False
            self.batch_file_path = None
            # Reset URL input label
            self.url_input.label = get_text(self.current_lang, 'url_label')
        
        self.page.update()
    
    def file_picker_result(self, e: ft.FilePickerResultEvent):
        """Handle file picker result"""
        if e.files:
            file = e.files[0]
            self.batch_file_path = file.path
            filename = Path(file.path).name
            self.selected_file_text.value = get_text(
                self.current_lang, 
                'batch_file_selected', 
                filename=filename
            )
            self.selected_file_text.visible = True
            self.page.update()
    
    def on_format_change(self, e):
        """Update quality options when format changes"""
        if self.format_radio.value == "audio":
            # Change to audio quality options
            self.quality_dropdown.options = [
                ft.dropdown.Option("best", get_text(self.current_lang, 'quality_audio_best')),
                ft.dropdown.Option("320", get_text(self.current_lang, 'quality_audio_320')),
                ft.dropdown.Option("192", get_text(self.current_lang, 'quality_audio_192')),
                ft.dropdown.Option("128", get_text(self.current_lang, 'quality_audio_128')),
            ]
        else:
            # Change to video quality options
            self.quality_dropdown.options = [
                ft.dropdown.Option("best", get_text(self.current_lang, 'quality_best')),
                ft.dropdown.Option("1080", get_text(self.current_lang, 'quality_1080p')),
                ft.dropdown.Option("720", get_text(self.current_lang, 'quality_720p')),
                ft.dropdown.Option("480", get_text(self.current_lang, 'quality_480p')),
            ]
        
        # Reset to best quality when switching
        self.quality_dropdown.value = "best"
        self.page.update()
    
    def clear_form(self, e):
        """Clear the form"""
        self.url_input.value = ""
        self.format_radio.value = "video"
        self.quality_dropdown.value = "best"
        self.cookies_dropdown.value = "none"
        self.info_container.visible = False
        self.download_btn.disabled = False
        
        # Clear batch list if in batch mode
        if self.download_mode == 'batch':
            self.url_list.controls.clear()
            self.update_url_count()
        
        # Clear output log
        self.output_log.controls.clear()
        
        # Reset progress
        self.reset_progress()
        
        self.page.update()
    
    def update_status(self, message, color=ft.Colors.GREY_700):
        """Update status text"""
        self.progress_label.value = message
        self.progress_label.color = color
        self.page.update()
    
    def show_info(self, platform, title):
        """Show platform and title info"""
        self.info_container.content = ft.Column([
            ft.Text(
                get_text(self.current_lang, 'detected_platform', platform=platform),
                size=12,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_900,
            ),
            ft.Text(
                get_text(self.current_lang, 'detected_title', title=title),
                size=12,
                color=ft.Colors.BLUE_800,
            ),
        ])
        self.info_container.visible = True
        self.page.update()
    
    def update_progress(self, current, total, percentage, title="", speed="", eta=""):
        """Update progress display with enhanced statistics"""
        try:
            # Update progress label
            if title:
                self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%) - {title}"
            else:
                self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%)"
            
            # Update progress bar
            self.progress_bar.value = percentage / 100.0
            
            # Update speed and ETA
            if speed:
                self.speed_label.value = f"{get_text(self.current_lang, 'speed_label')}: {speed}"
            if eta:
                self.eta_label.value = f"{get_text(self.current_lang, 'eta_label')}: {eta}"
            
            # Update statistics
            if self.start_time:
                elapsed = time.time() - self.start_time
                elapsed_mins = int(elapsed // 60)
                elapsed_secs = int(elapsed % 60)
                self.stats_text.value = f"Elapsed: {elapsed_mins:02d}:{elapsed_secs:02d} | Downloaded: {current}"
            
            # Update GUI
            self.page.update()
        except Exception as e:
            pass
    
    def reset_progress(self):
        """Reset progress display"""
        self.progress_label.value = get_text(self.current_lang, 'status_ready')
        self.progress_bar.value = 0
        self.speed_label.value = get_text(self.current_lang, 'speed_label') + ": -- MB/s"
        self.eta_label.value = get_text(self.current_lang, 'eta_label') + ": --:--"
        self.stats_text.value = ""
        self.start_time = None
        self.page.update()
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', 'N/A')
            speed_str = d.get('_speed_str', 'N/A')
            
            # Parse percentage for progress bar
            try:
                percent_num = float(percent_str.replace('%', '')) if percent_str != 'N/A' else 0
            except:
                percent_num = 0
            
            self.progress_label.value = get_text(self.current_lang, 'progress_downloading', percent=percent_str, speed=speed_str)
            self.progress_label.color = ft.Colors.BLUE_700
            self.progress_bar.value = percent_num / 100.0
            
            # Update speed display
            if speed_str != 'N/A':
                self.speed_label.value = f"{get_text(self.current_lang, 'speed_label')}: {speed_str}"
            
            self.page.update()
            
        elif d['status'] == 'finished':
            self.update_status(
                get_text(self.current_lang, 'status_processing'),
                ft.Colors.ORANGE_700
            )
    
    def download_video(self):
        """Download video/audio in background thread"""
        try:
            # Check download mode
            if self.download_mode == 'batch':
                self.download_batch()
                return
            
            # Single download mode
            url = self.url_input.value.strip()
            
            if not url:
                self.update_status(
                    get_text(self.current_lang, 'error_empty_url'),
                    ft.Colors.RED_700
                )
                self.download_btn.disabled = False
                self.page.update()
                return
            
            # Change to download folder
            os.chdir(self.download_folder)
            
            # Base options
            ydl_opts = {
                'outtmpl': '%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'ignoreerrors': True,
                'quiet': True,
                'no_warnings': True,
            }
            
            # Format selection based on user choice
            format_choice = self.format_radio.value
            quality_choice = self.quality_dropdown.value
            
            if format_choice == 'audio':
                # Audio MP3 with quality selection
                audio_quality = '192'  # default
                if quality_choice == '320':
                    audio_quality = '320'
                elif quality_choice == '192':
                    audio_quality = '192'
                elif quality_choice == '128':
                    audio_quality = '128'
                elif quality_choice == 'best':
                    audio_quality = '320'  # best quality = 320 kbps
                
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality,
                    }],
                })
            else:
                # Video with quality selection
                if quality_choice == 'best':
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                elif quality_choice == '1080':
                    ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                elif quality_choice == '720':
                    ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                elif quality_choice == '480':
                    ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            
            # Cookies if selected
            cookies_choice = self.cookies_dropdown.value
            if cookies_choice != 'none':
                ydl_opts['cookiesfrombrowser'] = (cookies_choice,)
            
            # Extract info first
            self.update_status(
                get_text(self.current_lang, 'status_validating'),
                ft.Colors.BLUE_700
            )
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                platform = info.get('extractor_key', 'Unknown')
                title = info.get('title', 'Unknown Title')
                
                # Show info
                self.show_info(platform, title)
                
                # Start download
                self.update_status(
                    get_text(self.current_lang, 'status_downloading'),
                    ft.Colors.BLUE_700
                )
                ydl.download([url])
            
            # Success
            self.progress_bar.value = 1.0
            self.update_status(
                get_text(self.current_lang, 'status_success'),
                ft.Colors.GREEN_700
            )
            self.log_output("✅ " + get_text(self.current_lang, 'status_success'))
            self.log_output("📁 " + get_text(self.current_lang, 'output_folder', folder=self.download_folder))
            
        except Exception as e:
            self.progress_bar.value = 0
            error_msg = str(e)
            if 'Unsupported URL' in error_msg:
                error_msg = get_text(self.current_lang, 'error_invalid_url')
            self.update_status(
                get_text(self.current_lang, 'status_error', error=error_msg),
                ft.Colors.RED_700
            )
            self.log_output("❌ " + get_text(self.current_lang, 'status_error', error=error_msg))
        
        finally:
            self.download_btn.disabled = False
            self.page.update()
    
    def download_batch(self):
        """Download multiple videos from batch file"""
        try:
            # Check if file is selected
            if not self.batch_file_path:
                self.update_status(
                    get_text(self.current_lang, 'batch_no_file'),
                    ft.Colors.RED_700
                )
                self.download_btn.disabled = False
                self.page.update()
                return
            
            # Import batch reader
            from batch_reader import read_batch_file
            
            # Read links from file
            self.update_status(
                get_text(self.current_lang, 'status_validating'),
                ft.Colors.BLUE_700
            )
            
            try:
                links = read_batch_file(self.batch_file_path)
            except Exception as e:
                self.update_status(
                    get_text(self.current_lang, 'batch_error_read', error=str(e)),
                    ft.Colors.RED_700
                )
                self.download_btn.disabled = False
                self.page.update()
                return
            
            if not links:
                self.update_status(
                    get_text(self.current_lang, 'batch_no_links'),
                    ft.Colors.RED_700
                )
                self.download_btn.disabled = False
                self.page.update()
                return
            
            # Change to download folder
            os.chdir(self.download_folder)
            
            # Process each link
            total = len(links)
            success_count = 0
            failed_count = 0
            
            for i, link_data in enumerate(links, 1):
                url = link_data['url']
                quality = link_data.get('quality', self.quality_dropdown.value)
                format_type = link_data.get('format', self.format_radio.value)
                
                # Update status
                self.update_status(
                    get_text(self.current_lang, 'batch_processing', current=i, total=total),
                    ft.Colors.BLUE_700
                )
                self.progress_bar.visible = True
                self.page.update()
                
                try:
                    # Base options
                    ydl_opts = {
                        'outtmpl': '%(title)s.%(ext)s',
                        'progress_hooks': [self.progress_hook],
                        'ignoreerrors': True,
                        'quiet': True,
                        'no_warnings': True,
                    }
                    
                    # Format selection
                    if format_type == 'audio':
                        # Audio quality mapping
                        audio_quality = '192'  # default
                        if quality == '320':
                            audio_quality = '320'
                        elif quality == '192':
                            audio_quality = '192'
                        elif quality == '128':
                            audio_quality = '128'
                        elif quality == 'best':
                            audio_quality = '320'
                        
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': audio_quality,
                            }],
                        })
                    else:
                        # Video with quality selection
                        if quality == 'best':
                            ydl_opts['format'] = 'bestvideo+bestaudio/best'
                        elif quality == '1080':
                            ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
                        elif quality == '720':
                            ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
                        elif quality == '480':
                            ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
                    
                    # Cookies if selected
                    cookies_choice = self.cookies_dropdown.value
                    if cookies_choice != 'none':
                        ydl_opts['cookiesfrombrowser'] = (cookies_choice,)
                    
                    # Download
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    success_count += 1
                    
                except Exception as e:
                    failed_count += 1
                    print(f"Error downloading {url}: {e}")
            
            # Show completion status
            self.progress_bar.visible = False
            self.update_status(
                get_text(
                    self.current_lang, 
                    'batch_complete', 
                    total=total, 
                    success=success_count, 
                    failed=failed_count
                ) + "\n" + get_text(self.current_lang, 'output_folder', folder=self.download_folder),
                ft.Colors.GREEN_700 if failed_count == 0 else ft.Colors.ORANGE_700
            )
            
        except Exception as e:
            self.progress_bar.visible = False
            self.update_status(
                get_text(self.current_lang, 'status_error', error=str(e)),
                ft.Colors.RED_700
            )
        
        finally:
            self.download_btn.disabled = False
            self.page.update()
    
    def start_download(self, e):
        """Start download in background thread"""
        # Validation
        if self.download_mode == 'single':
            url = self.url_input.value.strip()
            if not url:
                self.log_output("❌ " + get_text(self.current_lang, 'error_empty_url'))
                return
        elif self.download_mode == 'batch':
            if not self.batch_file_path and len(self.url_list.controls) == 0:
                self.log_output("⚠️ No URLs in batch list and no file selected!")
                return
        
        # Ensure download folder exists
        os.makedirs(self.download_folder, exist_ok=True)
        
        # Start timer and reset progress
        self.start_time = time.time()
        self.download_btn.disabled = True
        self.download_btn.text = "Downloading..."
        self.info_container.visible = False
        self.reset_progress()
        
        # Log start
        self.log_output("="*50)
        self.log_output("🚀 Starting download...")
        self.log_output(f"📁 Folder: {self.download_folder}")
        self.log_output(f"🎵 Format: {self.format_radio.value}")
        self.log_output(f"🎯 Quality: {self.quality_dropdown.value}")
        self.log_output("="*50)
        
        self.page.update()
        
        # Run in thread to keep UI responsive
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

def main(page: ft.Page):
    SocMedDownloaderGUI(page)

if __name__ == "__main__":
    ft.app(target=main)




