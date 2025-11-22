import flet as ft
import yt_dlp
import os
import sys
import threading
from pathlib import Path
from language_config import get_text, LANGUAGES

class SocMedDownloaderGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "SocMed Downloader"
        self.page.window_width = 800
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        
        # State
        self.current_lang = 'id'
        self.download_folder = str(Path.home() / "Downloads")
        self.download_mode = 'single'  # 'single' or 'batch'
        self.batch_file_path = None
        
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
        
        # Language selector
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
        
        # Language section (top right)
        lang_section = ft.Container(
            content=ft.Row([self.lang_dropdown], alignment=ft.MainAxisAlignment.END),
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(lang_section)
        
        # Title Section (centered like yt downloader)
        title_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    get_text(self.current_lang, 'app_title'),
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    get_text(self.current_lang, 'subtitle'),
                    size=14,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    get_text(self.current_lang, 'platform_support'),
                    size=12,
                    color=ft.Colors.BLUE_600,
                    weight=ft.FontWeight.W_500,
                    text_align=ft.TextAlign.CENTER
                )
            ]),
            padding=ft.padding.only(bottom=20)
        )
        main_content.controls.append(title_section)
        
        # Input Management Section (like yt downloader)
        input_section = self.create_input_management_section()
        main_content.controls.append(input_section)
        
        # Format selector
        self.format_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="video", label=get_text(self.current_lang, 'format_video')),
                ft.Radio(value="audio", label=get_text(self.current_lang, 'format_audio')),
            ]),
            value="video",
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
            size=11,
            color=ft.Colors.GREY_600,
            italic=True,
        )
        
        # Platform support info
        self.platform_info = ft.Text(
            get_text(self.current_lang, 'platform_support'),
            size=12,
            color=ft.Colors.BLUE_600,
            weight=ft.FontWeight.W_500,
        )
        
        # Progress bar
        self.progress_bar = ft.ProgressBar(width=700, visible=False)
        
        # Status text
        self.status_text = ft.Text(
            get_text(self.current_lang, 'status_ready'),
            size=13,
            color=ft.Colors.GREY_700,
        )
        
        # Info container (for platform and title detection)
        self.info_container = ft.Container(
            content=ft.Column([]),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=10,
            padding=10,
            visible=False,
        )
        
        # Buttons
        self.download_btn = ft.ElevatedButton(
            text=get_text(self.current_lang, 'download_button'),
            icon=ft.Icons.DOWNLOAD,
            on_click=self.start_download,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )
        
        self.clear_btn = ft.OutlinedButton(
            text=get_text(self.current_lang, 'clear_button'),
            icon=ft.Icons.CLEAR,
            on_click=self.clear_form,
        )
        
        # Download Options Section
        options_section = self.create_download_options_section()
        main_content.controls.append(options_section)
        
        # Download Buttons Section
        buttons_section = self.create_buttons_section()
        main_content.controls.append(buttons_section)
        
        # Progress Section
        progress_section = self.create_progress_section()
        main_content.controls.append(progress_section)
        
        # Add file picker to overlay
        self.page.overlay.append(self.file_picker)
        
        # Add main content to page
        self.page.add(main_content)
    
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
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    get_text(self.current_lang, 'mode_label'), 
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
                    size=14,
                    weight=ft.FontWeight.W_500
                ),
                self.url_input,
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(15),
            margin=ft.margin.only(bottom=10)
        )
    
    def create_download_options_section(self):
        """Create download options section similar to yt downloader"""
        # Format selector
        self.format_radio = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="video", label=get_text(self.current_lang, 'format_video')),
                ft.Radio(value="audio", label=get_text(self.current_lang, 'format_audio')),
            ]),
            value="video",
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
            size=11,
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
                ft.Container(height=5),
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
        # Buttons
        self.download_btn = ft.ElevatedButton(
            text=get_text(self.current_lang, 'download_button'),
            icon=ft.Icons.DOWNLOAD,
            on_click=self.start_download,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_700,
            ),
        )
        
        self.clear_btn = ft.OutlinedButton(
            text=get_text(self.current_lang, 'clear_button'),
            icon=ft.Icons.CLEAR,
            on_click=self.clear_form,
            width=140,
            height=50,
        )
        
        return ft.Container(
            content=ft.Row([
                self.download_btn,
                self.clear_btn,
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=15),
            padding=ft.padding.symmetric(vertical=20)
        )
    
    def create_progress_section(self):
        """Create progress section similar to yt downloader"""
        # Progress bar
        self.progress_bar = ft.ProgressBar(expand=True, visible=False)
        
        # Status text
        self.status_text = ft.Text(
            get_text(self.current_lang, 'status_ready'),
            size=13,
            color=ft.Colors.GREY_700,
        )
        
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
                self.info_container,
                ft.Container(height=10),
                self.progress_bar,
                ft.Container(height=5),
                self.status_text,
            ]),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(15),
            margin=ft.margin.only(top=10)
        )
        

    
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
            # Show batch file picker, hide URL input
            self.url_input.visible = False
            self.batch_file_btn.visible = True
            self.batch_file_info.visible = True
        else:
            # Show URL input, hide batch file picker
            self.url_input.visible = True
            self.batch_file_btn.visible = False
            self.batch_file_info.visible = False
            self.selected_file_text.visible = False
            self.batch_file_path = None
        
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
    
    def clear_form(self, e):
        """Clear the form"""
        self.url_input.value = ""
        self.format_radio.value = "video"
        self.quality_dropdown.value = "best"
        self.cookies_dropdown.value = "none"
        self.progress_bar.visible = False
        self.info_container.visible = False
        self.status_text.value = get_text(self.current_lang, 'status_ready')
        self.status_text.color = ft.Colors.GREY_700
        self.download_btn.disabled = False
        self.page.update()
    
    def update_status(self, message, color=ft.Colors.GREY_700):
        """Update status text"""
        self.status_text.value = message
        self.status_text.color = color
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
    
    def progress_hook(self, d):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            self.update_status(
                get_text(self.current_lang, 'progress_downloading', percent=percent, speed=speed),
                ft.Colors.BLUE_700
            )
            if not self.progress_bar.visible:
                self.progress_bar.visible = True
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
                # Audio MP3
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
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
            self.progress_bar.visible = False
            self.update_status(
                get_text(self.current_lang, 'status_success') + "\n" + 
                get_text(self.current_lang, 'output_folder', folder=self.download_folder),
                ft.Colors.GREEN_700
            )
            
        except Exception as e:
            self.progress_bar.visible = False
            error_msg = str(e)
            if 'Unsupported URL' in error_msg:
                error_msg = get_text(self.current_lang, 'error_invalid_url')
            self.update_status(
                get_text(self.current_lang, 'status_error', error=error_msg),
                ft.Colors.RED_700
            )
        
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
                        ydl_opts.update({
                            'format': 'bestaudio/best',
                            'postprocessors': [{
                                'key': 'FFmpegExtractAudio',
                                'preferredcodec': 'mp3',
                                'preferredquality': '192',
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
        self.download_btn.disabled = True
        self.info_container.visible = False
        self.page.update()
        
        # Run in thread to keep UI responsive
        thread = threading.Thread(target=self.download_video, daemon=True)
        thread.start()

def main(page: ft.Page):
    SocMedDownloaderGUI(page)

if __name__ == "__main__":
    ft.app(target=main)

