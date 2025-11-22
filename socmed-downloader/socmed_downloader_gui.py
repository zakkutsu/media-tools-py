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
        
        # Build UI
        self.build_ui()
    
    def build_ui(self):
        """Build the main user interface"""
        
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
        
        # Title
        self.title_text = ft.Text(
            get_text(self.current_lang, 'app_title'),
            size=32,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_700,
        )
        
        self.subtitle_text = ft.Text(
            get_text(self.current_lang, 'subtitle'),
            size=14,
            color=ft.colors.GREY_700,
        )
        
        # URL Input
        self.url_input = ft.TextField(
            label=get_text(self.current_lang, 'url_label'),
            hint_text=get_text(self.current_lang, 'url_hint'),
            width=700,
            multiline=False,
            autocorrect=False,
        )
        
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
            color=ft.colors.GREY_600,
            italic=True,
        )
        
        # Platform support info
        self.platform_info = ft.Text(
            get_text(self.current_lang, 'platform_support'),
            size=12,
            color=ft.colors.BLUE_600,
            weight=ft.FontWeight.W_500,
        )
        
        # Progress bar
        self.progress_bar = ft.ProgressBar(width=700, visible=False)
        
        # Status text
        self.status_text = ft.Text(
            get_text(self.current_lang, 'status_ready'),
            size=13,
            color=ft.colors.GREY_700,
        )
        
        # Info container (for platform and title detection)
        self.info_container = ft.Container(
            content=ft.Column([]),
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            padding=10,
            visible=False,
        )
        
        # Buttons
        self.download_btn = ft.ElevatedButton(
            text=get_text(self.current_lang, 'download_button'),
            icon=ft.icons.DOWNLOAD,
            on_click=self.start_download,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_700,
            ),
        )
        
        self.clear_btn = ft.OutlinedButton(
            text=get_text(self.current_lang, 'clear_button'),
            icon=ft.icons.CLEAR,
            on_click=self.clear_form,
        )
        
        # Layout
        self.page.add(
            ft.Container(height=10),
            ft.Row([self.lang_dropdown], alignment=ft.MainAxisAlignment.END),
            ft.Container(height=10),
            self.title_text,
            self.subtitle_text,
            ft.Container(height=10),
            self.platform_info,
            ft.Divider(height=20),
            self.url_input,
            ft.Container(height=10),
            ft.Text(get_text(self.current_lang, 'format_label'), size=14, weight=ft.FontWeight.W_500),
            self.format_radio,
            ft.Container(height=10),
            ft.Row([
                self.quality_dropdown,
                ft.Container(width=20),
                self.cookies_dropdown,
            ]),
            self.cookies_help,
            ft.Container(height=20),
            self.info_container,
            self.progress_bar,
            self.status_text,
            ft.Container(height=20),
            ft.Row([
                self.download_btn,
                ft.Container(width=10),
                self.clear_btn,
            ]),
        )
    
    def change_language(self, e):
        """Change the interface language"""
        self.current_lang = e.control.value
        # Rebuild UI with new language
        self.page.controls.clear()
        self.build_ui()
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
        self.status_text.color = ft.colors.GREY_700
        self.download_btn.disabled = False
        self.page.update()
    
    def update_status(self, message, color=ft.colors.GREY_700):
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
                color=ft.colors.BLUE_900,
            ),
            ft.Text(
                get_text(self.current_lang, 'detected_title', title=title),
                size=12,
                color=ft.colors.BLUE_800,
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
                ft.colors.BLUE_700
            )
            if not self.progress_bar.visible:
                self.progress_bar.visible = True
                self.page.update()
        elif d['status'] == 'finished':
            self.update_status(
                get_text(self.current_lang, 'status_processing'),
                ft.colors.ORANGE_700
            )
    
    def download_video(self):
        """Download video/audio in background thread"""
        try:
            url = self.url_input.value.strip()
            
            if not url:
                self.update_status(
                    get_text(self.current_lang, 'error_empty_url'),
                    ft.colors.RED_700
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
                ft.colors.BLUE_700
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
                    ft.colors.BLUE_700
                )
                ydl.download([url])
            
            # Success
            self.progress_bar.visible = False
            self.update_status(
                get_text(self.current_lang, 'status_success') + "\n" + 
                get_text(self.current_lang, 'output_folder', folder=self.download_folder),
                ft.colors.GREEN_700
            )
            
        except Exception as e:
            self.progress_bar.visible = False
            error_msg = str(e)
            if 'Unsupported URL' in error_msg:
                error_msg = get_text(self.current_lang, 'error_invalid_url')
            self.update_status(
                get_text(self.current_lang, 'status_error', error=error_msg),
                ft.colors.RED_700
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
