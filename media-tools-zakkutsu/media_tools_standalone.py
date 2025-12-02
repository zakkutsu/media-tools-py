#!/usr/bin/env python3
"""
=============================================================================
MEDIA TOOLS ZAKKUTSU - ALL-IN-ONE STANDALONE
=============================================================================
Complete media processing suite in a single file.
No external folders needed - everything is embedded!

Tools Included:
1. YT Playlist Downloader - Download YouTube playlists
2. Media Looper - Loop video/audio instantly
3. Audio Merger - Merge audio files with effects
4. SocMed Downloader - Download from TikTok, IG, FB, Twitter/X

Author: Zakkutsu
Version: 1.0.1
Date: December 2025
License: MIT

Dependencies:
- flet >= 0.25.0
- yt-dlp >= 2024.11.0
- pydub == 0.25.1
- ffmpeg-python == 0.2.0

System Requirements:
- Python 3.8+
- FFmpeg (must be installed separately)

Usage:
    python media_tools_standalone.py

=============================================================================
"""

import flet as ft
from flet import icons, colors
import os
import sys
import subprocess
import threading
import time
import glob
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_ffmpeg_path():
    """Get FFmpeg executable path (bundled, portable, or system)"""
    # For PyInstaller bundled executable
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = sys._MEIPASS  # PyInstaller temp folder
        bundled_ffmpeg = os.path.join(app_dir, 'ffmpeg-portable', 'bin', 'ffmpeg.exe')
        if os.path.exists(bundled_ffmpeg):
            return bundled_ffmpeg
    
    # For running as script
    app_dir = os.path.dirname(os.path.abspath(__file__))
    portable_ffmpeg = os.path.join(app_dir, 'ffmpeg-portable', 'bin', 'ffmpeg.exe')
    
    # Check portable version
    if os.path.exists(portable_ffmpeg):
        return portable_ffmpeg
    
    # Check system PATH
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        if result.returncode == 0:
            return 'ffmpeg'  # System FFmpeg
    except:
        pass
    
    return None

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    return get_ffmpeg_path() is not None

def download_ffmpeg_portable(page=None, progress_callback=None):
    """Download and extract FFmpeg portable version"""
    import urllib.request
    import zipfile
    import shutil
    
    app_dir = os.path.dirname(os.path.abspath(__file__))
    ffmpeg_dir = os.path.join(app_dir, 'ffmpeg-portable')
    
    # FFmpeg portable download URL (Windows 64-bit)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    zip_path = os.path.join(app_dir, 'ffmpeg-temp.zip')
    
    try:
        if progress_callback:
            progress_callback("Downloading FFmpeg portable (~100 MB)...", 0)
        
        # Download with progress
        def reporthook(block_num, block_size, total_size):
            if progress_callback and total_size > 0:
                downloaded = block_num * block_size
                percent = min(int((downloaded / total_size) * 50), 50)  # 0-50%
                progress_callback(f"Downloading: {downloaded//1024//1024}MB / {total_size//1024//1024}MB", percent)
        
        urllib.request.urlretrieve(ffmpeg_url, zip_path, reporthook=reporthook)
        
        if progress_callback:
            progress_callback("Extracting FFmpeg...", 60)
        
        # Extract ZIP
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            # Get root folder name in ZIP
            zip_contents = zip_ref.namelist()
            root_folder = zip_contents[0].split('/')[0]
            
            # Extract to temp location
            temp_extract = os.path.join(app_dir, 'ffmpeg-temp-extract')
            zip_ref.extractall(temp_extract)
            
            # Move bin folder to ffmpeg-portable
            extracted_bin = os.path.join(temp_extract, root_folder, 'bin')
            if os.path.exists(extracted_bin):
                if os.path.exists(ffmpeg_dir):
                    shutil.rmtree(ffmpeg_dir)
                os.makedirs(ffmpeg_dir, exist_ok=True)
                shutil.move(extracted_bin, os.path.join(ffmpeg_dir, 'bin'))
            
            # Cleanup temp
            shutil.rmtree(temp_extract)
        
        # Remove ZIP
        os.remove(zip_path)
        
        if progress_callback:
            progress_callback("FFmpeg installed successfully!", 100)
        
        return True
        
    except Exception as e:
        if progress_callback:
            progress_callback(f"Error: {str(e)}", -1)
        # Cleanup on error
        for path in [zip_path, os.path.join(app_dir, 'ffmpeg-temp-extract')]:
            if os.path.exists(path):
                try:
                    if os.path.isfile(path):
                        os.remove(path)
                    else:
                        shutil.rmtree(path)
                except:
                    pass
        return False

def check_ytdlp():
    """Check if yt-dlp is installed"""
    try:
        import yt_dlp
        # Try to verify it's working by checking version
        version = yt_dlp.version.__version__
        return True
    except (ImportError, AttributeError):
        return False

def install_dependencies():
    """Install missing dependencies"""
    missing = []
    try:
        import flet
    except ImportError:
        missing.append('flet>=0.25.0')
    
    try:
        import yt_dlp
    except ImportError:
        missing.append('yt-dlp>=2024.11.0')
    
    try:
        import pydub
    except ImportError:
        missing.append('pydub==0.25.1')
    
    if missing:
        print(f"Installing missing dependencies: {', '.join(missing)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
        print("Dependencies installed successfully!")
        return True
    return False


# ============================================================================
# PLAYLIST DOWNLOADER CLASS
# ============================================================================

class PlaylistDownloader:
    """YouTube Playlist Downloader"""
    
    def __init__(self):
        self.download_folder = None
        self.yt_dlp_available = self._check_yt_dlp()
    
    def _check_yt_dlp(self) -> bool:
        try:
            import yt_dlp
            return True
        except ImportError:
            return False
    
    def install_or_update_yt_dlp(self) -> bool:
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                                  capture_output=True, text=True, timeout=120)
            if result.returncode == 0:
                self.yt_dlp_available = True
                return True
            return False
        except:
            return False
    
    def set_download_folder(self, folder_path: str) -> bool:
        try:
            self.download_folder = Path(folder_path)
            self.download_folder.mkdir(parents=True, exist_ok=True)
            return True
        except:
            return False
    
    def get_playlist_info(self, playlist_url: str) -> Optional[Dict[str, Any]]:
        if not self.yt_dlp_available:
            return None
        
        try:
            import yt_dlp
            
            ydl_opts = {
                'quiet': True,
                'extract_flat': True,
                'force_generic_extractor': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                if 'entries' in info:
                    return {
                        'total_videos': len(info['entries']),
                        'entries': info['entries']
                    }
                return None
        except Exception as e:
            print(f"Error getting playlist info: {e}")
            return None
    
    def download_video_playlist(self, playlist_url: str, quality: str = "best", 
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        if not self.yt_dlp_available or not self.download_folder:
            return False
        
        try:
            import yt_dlp
            
            if not auto_numbering:
                output_template = output_template.replace("%(playlist_index)s - ", "").replace("%(playlist_index)s", "")
                output_template = " ".join(output_template.split())
                if "%(title)s" not in output_template:
                    output_template = "%(title)s.%(ext)s"
            
            if quality == "best":
                format_selector = "bv+ba/b"
            elif quality == "720p":
                format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif quality == "480p":
                format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            else:
                format_selector = quality
            
            # Progress hook
            current_item = [0]  # Track current item
            
            def progress_hook(d):
                if not progress_callback:
                    return
                
                try:
                    status = d.get('status', '')
                    playlist_index = d.get('playlist_index', 0)
                    playlist_count = d.get('playlist_count', 0)
                    
                    if playlist_index > 0 and playlist_count > 0:
                        # Update tracker when starting new item
                        if status == 'downloading' and playlist_index != current_item[0]:
                            current_item[0] = playlist_index
                            info_dict = d.get('info_dict', {})
                            title = info_dict.get('title', '')
                            percentage = (playlist_index / playlist_count) * 100
                            progress_callback(playlist_index, playlist_count, percentage, title)
                        
                        # Update on completion
                        elif status == 'finished':
                            info_dict = d.get('info_dict', {})
                            title = info_dict.get('title', '')
                            percentage = (playlist_index / playlist_count) * 100
                            progress_callback(playlist_index, playlist_count, percentage, f"✓ {title}")
                
                except Exception as e:
                    pass
            
            ydl_opts = {
                'format': format_selector,
                'outtmpl': str(self.download_folder / output_template),
                'writethumbnail': True,
                'embedthumbnail': True,
                'addmetadata': True,
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([playlist_url])
            
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False
    
    def download_audio_playlist(self, playlist_url: str, audio_format: str = "mp3",
                              audio_quality: str = "0",
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        if not self.yt_dlp_available or not self.download_folder:
            return False
        
        try:
            import yt_dlp
            
            if not auto_numbering:
                output_template = output_template.replace("%(playlist_index)s - ", "").replace("%(playlist_index)s", "")
                output_template = " ".join(output_template.split())
                if "%(title)s" not in output_template:
                    output_template = "%(title)s.%(ext)s"
            
            # Progress hook
            current_item = [0]  # Track current item
            
            def progress_hook(d):
                if not progress_callback:
                    return
                
                try:
                    status = d.get('status', '')
                    playlist_index = d.get('playlist_index', 0)
                    playlist_count = d.get('playlist_count', 0)
                    
                    if playlist_index > 0 and playlist_count > 0:
                        # Update tracker when starting new item
                        if status == 'downloading' and playlist_index != current_item[0]:
                            current_item[0] = playlist_index
                            info_dict = d.get('info_dict', {})
                            title = info_dict.get('title', '')
                            percentage = (playlist_index / playlist_count) * 100
                            progress_callback(playlist_index, playlist_count, percentage, title)
                        
                        # Update on completion
                        elif status == 'finished':
                            info_dict = d.get('info_dict', {})
                            title = info_dict.get('title', '')
                            percentage = (playlist_index / playlist_count) * 100
                            progress_callback(playlist_index, playlist_count, percentage, f"✓ {title}")
                
                except Exception as e:
                    pass
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.download_folder / output_template),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': audio_format,
                    'preferredquality': audio_quality,
                }],
                'writethumbnail': True,
                'embedthumbnail': True,
                'addmetadata': True,
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([playlist_url])
            
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False


# ============================================================================
# PLAYLIST DOWNLOADER GUI
# ============================================================================

class PlaylistDownloaderGUI:
    """GUI for YouTube Playlist Downloader"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎵 YouTube Playlist Downloader"
        
        # Initialize downloader
        self.downloader = PlaylistDownloader()
        
        # Variables
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Downloads")
        self.playlist_url = ""
        self.download_type = "video_best"
        self.output_template = "%(playlist_index)s - %(title)s.%(ext)s"
        self.auto_numbering = True
        self.playlist_info = None
        
        # UI Components
        self.folder_field = None
        self.url_field = None
        self.template_field = None
        self.info_text = None
        self.overall_progress_bar = None
        self.overall_progress_text = None
        self.current_progress_bar = None
        self.current_progress_text = None
        self.progress_label = None
        self.output_log = None
        self.download_btn = None
        self.get_info_btn = None
        self.ytdlp_status_text = None
        self.install_btn = None
        
        # Setup UI
        self.setup_ui()
        self.update_ytdlp_status()
    
    def setup_ui(self):
        """Setup the user interface"""
        self.page.controls.clear()
        
        # Create scrollable column for main content
        main_content = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10
        )
        
        # Title Section
        title_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "🎵 YouTube Playlist Downloader",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Download complete YouTube playlists with ease",
                    size=14,
                    color=colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ]),
            padding=ft.padding.only(bottom=20)
        )
        main_content.controls.append(title_section)
        
        # yt-dlp Status Section
        self.ytdlp_status_text = ft.Text("Checking yt-dlp status...", size=12)
        self.install_btn = ft.ElevatedButton(
            text="📦 Install/Update yt-dlp",
            on_click=self.install_update_ytdlp,
            icon=icons.DOWNLOAD
        )
        
        ytdlp_status_section = ft.Container(
            content=ft.Row([
                self.ytdlp_status_text,
                self.install_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(10),
            border=ft.border.all(1, colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
        main_content.controls.append(ytdlp_status_section)
        
        # Download Folder Section
        self.folder_field = ft.TextField(
            label="📁 Download Folder",
            value=self.download_folder,
            expand=True,
            on_change=self.on_folder_change
        )
        
        browse_btn = ft.ElevatedButton(
            text="Browse",
            icon=icons.FOLDER_OPEN,
            on_click=self.browse_folder
        )
        
        folder_section = ft.Container(
            content=ft.Row([self.folder_field, browse_btn]),
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(folder_section)
        
        # Playlist URL Section
        self.url_field = ft.TextField(
            label="🔗 Playlist URL",
            hint_text="Paste YouTube playlist URL here...",
            expand=True,
            on_change=self.on_url_change,
            on_submit=self.get_playlist_info
        )
        
        self.get_info_btn = ft.ElevatedButton(
            text="Get Info",
            icon=icons.INFO,
            on_click=self.get_playlist_info,
            style=ft.ButtonStyle(bgcolor=colors.BLUE_100)
        )
        
        url_section = ft.Container(
            content=ft.Row([self.url_field, self.get_info_btn]),
            padding=ft.padding.only(bottom=5)
        )
        main_content.controls.append(url_section)
        
        # Playlist Info Display
        self.info_text = ft.Text("", color=colors.BLUE_600, size=12, weight=ft.FontWeight.BOLD)
        info_section = ft.Container(
            content=self.info_text,
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(info_section)
        
        # Download Options Section
        options_section = self.create_download_options_section()
        main_content.controls.append(options_section)
        
        # Download Button
        self.download_btn = ft.ElevatedButton(
            text="🚀 Start Download",
            icon=icons.PLAY_ARROW,
            on_click=self.start_download,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=colors.WHITE,
                bgcolor=colors.BLUE_600
            )
        )
        
        download_section = ft.Container(
            content=ft.Row([self.download_btn], alignment=ft.MainAxisAlignment.CENTER),
            padding=ft.padding.symmetric(vertical=20)
        )
        main_content.controls.append(download_section)
        
        # Progress Section
        progress_section = self.create_progress_section()
        main_content.controls.append(progress_section)
        
        # Output Log Section
        output_section = self.create_output_section()
        main_content.controls.append(output_section)
        
        # Add main content to page
        self.page.add(main_content)
    
    def create_download_options_section(self):
        """Create download options section"""
        # Download Type Radio Buttons
        download_type_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="video_best", label="🎬 Video (Best Quality)"),
                ft.Radio(value="video_720p", label="🎬 Video (720p - Save Bandwidth)"),
                ft.Radio(value="video_480p", label="🎬 Video (480p - Save Bandwidth)"),
                ft.Radio(value="audio_mp3", label="🎵 Audio Only (MP3)")
            ]),
            value="video_best",
            on_change=self.on_download_type_change
        )
        
        # Output Template
        self.template_field = ft.TextField(
            label="File Naming Template",
            value=self.output_template,
            expand=True,
            on_change=self.on_template_change
        )
        
        reset_template_btn = ft.ElevatedButton(
            text="Reset",
            icon=icons.REFRESH,
            on_click=self.reset_template
        )
        
        template_row = ft.Row([self.template_field, reset_template_btn])
        
        # Auto Numbering Checkbox
        auto_numbering_checkbox = ft.Checkbox(
            label="🔢 Enable Auto File Numbering (01 - Title.ext)",
            value=self.auto_numbering,
            on_change=self.on_auto_numbering_change
        )
        
        # Help Text
        help_text = ft.Text(
            "Template variables: %(playlist_index)s (number), %(title)s (title), %(ext)s (extension)",
            size=10,
            color=colors.GREY_600
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("⚙️ Download Options", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("Download Type:", size=12, weight=ft.FontWeight.BOLD),
                download_type_group,
                ft.Text("File Naming Template:", size=12, weight=ft.FontWeight.BOLD),
                template_row,
                auto_numbering_checkbox,
                help_text
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
    def create_progress_section(self):
        """Create progress section"""
        self.progress_label = ft.Text("Ready to download", size=12, weight=ft.FontWeight.BOLD)
        
        # Playlist Progress (Overall)
        playlist_progress_label = ft.Text("Playlist Progress:", size=10, weight=ft.FontWeight.BOLD)
        self.overall_progress_bar = ft.ProgressBar(value=0, expand=True)
        self.overall_progress_text = ft.Text("0%", size=11, weight=ft.FontWeight.BOLD, width=50, text_align=ft.TextAlign.RIGHT)
        
        # Current Item Progress
        current_progress_label = ft.Text("Current Item Progress:", size=10, weight=ft.FontWeight.BOLD)
        self.current_progress_bar = ft.ProgressBar(value=0, expand=True)
        self.current_progress_text = ft.Text("0%", size=11, weight=ft.FontWeight.BOLD, width=50, text_align=ft.TextAlign.RIGHT)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 Download Progress", size=16, weight=ft.FontWeight.BOLD),
                self.progress_label,
                ft.Container(height=10),
                playlist_progress_label,
                ft.Row([
                    ft.Container(
                        content=self.overall_progress_bar,
                        padding=ft.padding.symmetric(vertical=3),
                        expand=True
                    ),
                    self.overall_progress_text
                ], spacing=10),
                ft.Container(height=5),
                current_progress_label,
                ft.Row([
                    ft.Container(
                        content=self.current_progress_bar,
                        padding=ft.padding.symmetric(vertical=3),
                        expand=True
                    ),
                    self.current_progress_text
                ], spacing=10)
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
    def create_output_section(self):
        """Create output log section"""
        self.output_log = ft.ListView(
            height=250,
            spacing=2,
            padding=ft.padding.all(10),
            auto_scroll=True
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📋 Output Log", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=self.output_log,
                    border=ft.border.all(1, colors.GREY_300),
                    border_radius=8,
                    bgcolor=colors.GREY_50
                )
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
    def update_ytdlp_status(self):
        """Update yt-dlp status display"""
        if self.downloader.yt_dlp_available:
            self.ytdlp_status_text.value = "✅ yt-dlp is available"
            self.ytdlp_status_text.color = colors.GREEN_600
            self.install_btn.text = "Update yt-dlp"
        else:
            self.ytdlp_status_text.value = "❌ yt-dlp not found"
            self.ytdlp_status_text.color = colors.RED_600
            self.install_btn.text = "Install yt-dlp"
        self.page.update()
    
    def install_update_ytdlp(self, e):
        """Install or update yt-dlp in a separate thread"""
        def install_thread():
            self.log_output("Installing/Updating yt-dlp...")
            self.install_btn.disabled = True
            self.page.update()
            
            success = self.downloader.install_or_update_yt_dlp()
            
            self.install_btn.disabled = False
            
            if success:
                self.log_output("✅ yt-dlp installed/updated successfully!")
                self.update_ytdlp_status()
            else:
                self.log_output("❌ Failed to install/update yt-dlp")
            
            self.page.update()
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def browse_folder(self, e):
        """Browse for download folder"""
        def get_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.download_folder = e.path
                self.folder_field.value = e.path
                self.page.update()
        
        get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
        self.page.overlay.append(get_directory_dialog)
        self.page.update()
        
        get_directory_dialog.get_directory_path(
            dialog_title="Select Download Folder",
            initial_directory=self.download_folder
        )
    
    def on_folder_change(self, e):
        """Handle folder field change"""
        self.download_folder = e.control.value
    
    def on_url_change(self, e):
        """Handle URL field change"""
        self.playlist_url = e.control.value
        self.info_text.value = ""
        self.page.update()
    
    def get_playlist_info(self, e):
        """Get playlist information in a separate thread"""
        url = self.url_field.value.strip() if self.url_field.value else ""
        if not url:
            self.show_dialog("Warning", "Please enter a playlist URL first!")
            return
        
        def info_thread():
            self.log_output(f"Getting playlist info for: {url}")
            self.get_info_btn.disabled = True
            self.get_info_btn.text = "Getting Info..."
            self.page.update()
            
            info = self.downloader.get_playlist_info(url)
            
            self.get_info_btn.disabled = False
            self.get_info_btn.text = "Get Info"
            
            if info:
                self.playlist_info = info
                info_text = f"📊 Found {info['total_videos']} videos in playlist"
                self.info_text.value = info_text
                self.info_text.color = colors.GREEN_600
                self.log_output(f"✅ {info_text}")
            else:
                self.playlist_info = None
                self.info_text.value = "❌ Failed to get playlist info"
                self.info_text.color = colors.RED_600
                self.log_output("❌ Failed to get playlist info. Check URL and internet connection.")
            
            self.page.update()
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def on_download_type_change(self, e):
        """Handle download type change"""
        self.download_type = e.control.value
    
    def on_template_change(self, e):
        """Handle template change"""
        self.output_template = e.control.value
    
    def on_auto_numbering_change(self, e):
        """Handle auto numbering checkbox change"""
        self.auto_numbering = e.control.value
        
        current_template = self.output_template
        
        if self.auto_numbering:
            if "%(playlist_index)s" not in current_template:
                if current_template.startswith("%(title)s"):
                    new_template = "%(playlist_index)s - " + current_template
                else:
                    new_template = "%(playlist_index)s - %(title)s.%(ext)s"
                self.output_template = new_template
                self.template_field.value = new_template
        else:
            new_template = current_template.replace("%(playlist_index)s - ", "")
            new_template = new_template.replace("%(playlist_index)s", "")
            new_template = " ".join(new_template.split())
            if "%(title)s" not in new_template or not new_template or new_template == ".%(ext)s":
                new_template = "%(title)s.%(ext)s"
            self.output_template = new_template
            self.template_field.value = new_template
        
        self.page.update()
    
    def reset_template(self, e):
        """Reset output template to default"""
        if self.auto_numbering:
            self.output_template = "%(playlist_index)s - %(title)s.%(ext)s"
        else:
            self.output_template = "%(title)s.%(ext)s"
        
        self.template_field.value = self.output_template
        self.page.update()
    
    def start_download(self, e):
        """Start download process in a separate thread"""
        if not self.downloader.yt_dlp_available:
            self.show_dialog("Error", "yt-dlp is not available. Please install it first!")
            return
        
        url = self.url_field.value.strip() if self.url_field.value else ""
        if not url:
            self.show_dialog("Warning", "Please enter a playlist URL!")
            return
        
        folder = self.download_folder.strip()
        if not folder:
            self.show_dialog("Warning", "Please select a download folder!")
            return
        
        if not self.downloader.set_download_folder(folder):
            self.show_dialog("Error", f"Failed to create download folder: {folder}")
            return
        
        def download_thread():
            self.log_output("="*60)
            self.log_output("🚀 Starting download...")
            self.log_output(f"URL: {url}")
            self.log_output(f"Type: {self.download_type}")
            self.log_output(f"Folder: {folder}")
            self.log_output(f"Auto Numbering: {'Enabled' if self.auto_numbering else 'Disabled'}")
            self.log_output("="*60)
            
            self.download_btn.disabled = True
            self.download_btn.text = "Downloading..."
            self.reset_progress()
            self.current_progress_bar.value = None
            self.page.update()
            
            success = False
            download_type = self.download_type
            template = self.output_template or "%(playlist_index)s - %(title)s.%(ext)s"
            auto_numbering = self.auto_numbering
            
            try:
                if download_type == "video_best":
                    success = self.downloader.download_video_playlist(
                        url, quality="best", output_template=template, 
                        auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "video_720p":
                    success = self.downloader.download_video_playlist(
                        url, quality="720p", output_template=template, 
                        auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "video_480p":
                    success = self.downloader.download_video_playlist(
                        url, quality="480p", output_template=template, 
                        auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "audio_mp3":
                    success = self.downloader.download_audio_playlist(
                        url, audio_format="mp3", output_template=template, 
                        auto_numbering=auto_numbering, progress_callback=self.update_progress)
            except Exception as ex:
                self.log_output(f"❌ Error during download: {ex}")
                success = False
            
            self.current_progress_bar.value = 0
            self.download_btn.disabled = False
            self.download_btn.text = "🚀 Start Download"
            self.page.update()
            
            if success:
                self.log_output("="*60)
                self.log_output("🎉 Download completed successfully!")
                self.log_output(f"📁 Files saved to: {folder}")
                self.log_output("="*60)
                self.show_dialog("Success", 
                    f"Download completed!\n\nFiles saved to:\n{folder}")
            else:
                self.log_output("="*60)
                self.log_output("😞 Download failed!")
                self.log_output("Please check your internet connection and playlist URL.")
                self.log_output("="*60)
                self.show_dialog("Error", 
                    "Download failed!\n\nPlease check:\n- Internet connection\n- Playlist URL\n- Download folder permissions")
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def update_progress(self, current, total, percentage, title=""):
        """Update progress display"""
        if title:
            self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%) - {title}"
        else:
            self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%)"
        
        self.overall_progress_bar.value = percentage / 100.0
        self.overall_progress_text.value = f"{percentage:.1f}%"
        self.page.update()
    
    def reset_progress(self):
        """Reset progress display"""
        self.progress_label.value = "Ready to download"
        self.overall_progress_bar.value = 0
        self.overall_progress_text.value = "0%"
        self.current_progress_bar.value = 0
        self.current_progress_text.value = "0%"
        self.page.update()
    
    def log_output(self, message):
        """Add message to output log"""
        log_entry = ft.Text(
            message,
            size=10,
            selectable=True
        )
        self.output_log.controls.append(log_entry)
        
        if len(self.output_log.controls) > 100:
            self.output_log.controls.pop(0)
        
        self.page.update()
    
    def show_dialog(self, title, message):
        """Show dialog message"""
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()
        
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()


# ============================================================================
# MEDIA LOOPER - Core Logic
# ============================================================================

def get_media_duration(file_path):
    """Get media duration using FFprobe"""
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
               '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return None

def format_duration(seconds):
    """Format seconds to HH:MM:SS"""
    if not seconds:
        return "Unknown"
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"


# ============================================================================
# MEDIA LOOPER GUI
# ============================================================================

class MediaLooperGUI:
    """Simple Media Looper GUI"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🔁 Media Looper"
        self.processing = False
        self.setup_simple_ui()
    
    def setup_simple_ui(self):
        """Setup simplified UI"""
        self.page.controls.clear()
        
        # Title
        title = ft.Text("🔁 Media Looper", size=24, weight=ft.FontWeight.BOLD)
        
        # File Input
        self.file_field = ft.TextField(label="📂 Input File", read_only=True, expand=True)
        browse_btn = ft.ElevatedButton("Browse", on_click=self.browse_file)
        
        # Loop Count
        self.loop_field = ft.TextField(label="🔁 Loop Count", value="60", width=150)
        
        # Status
        self.status_text = ft.Text("Ready", size=12)
        
        # Process Button
        process_btn = ft.ElevatedButton(
            "⚡ Process",
            on_click=self.process_loop,
            bgcolor=colors.TEAL,
            color=colors.WHITE
        )
        
        # Layout
        content = ft.Column([
            title,
            ft.Container(height=20),
            ft.Row([self.file_field, browse_btn]),
            ft.Container(height=10),
            self.loop_field,
            ft.Container(height=20),
            process_btn,
            ft.Container(height=20),
            self.status_text,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.add(content)
        self.page.update()
    
    def browse_file(self, e):
        """Browse file"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                self.file_field.value = e.files[0].path
                self.page.update()
        
        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.pick_files(allowed_extensions=["mp4", "mkv", "mp3", "wav"])
    
    def process_loop(self, e):
        """Process looping"""
        file_path = self.file_field.value
        if not file_path or not os.path.exists(file_path):
            self.status_text.value = "❌ Select a valid file!"
            self.page.update()
            return
        
        try:
            count = int(self.loop_field.value)
            if count < 1:
                self.status_text.value = "❌ Loop count must be >= 1"
                self.page.update()
                return
        except:
            self.status_text.value = "❌ Invalid loop count!"
            self.page.update()
            return
        
        def process_thread():
            self.status_text.value = "⚙️ Processing..."
            self.page.update()
            
            filename, ext = os.path.splitext(file_path)
            output_file = f"{filename}_looped_{count}x{ext}"
            
            # Get FFmpeg path (system or portable)
            ffmpeg_exe = get_ffmpeg_path()
            if not ffmpeg_exe:
                self.status_text.value = "❌ FFmpeg not found!"
                self.page.update()
                return
            
            loop_count = count - 1
            cmd = [ffmpeg_exe, '-stream_loop', str(loop_count), '-i', file_path,
                   '-c', 'copy', output_file, '-y']
            
            try:
                subprocess.run(cmd, check=True, capture_output=True)
                self.status_text.value = f"✅ Success! Saved: {os.path.basename(output_file)}"
            except:
                self.status_text.value = "❌ Processing failed!"
            
            self.page.update()
        
        threading.Thread(target=process_thread, daemon=True).start()


# ============================================================================
# AUDIO MERGER - Core Logic
# ============================================================================

def get_audio_files(folder_path):
    """Get audio files from folder"""
    formats = ['mp3', 'wav', 'flac', 'm4a', 'ogg', 'aac', 'wma']
    audio_files = []
    for fmt in formats:
        pattern = os.path.join(folder_path, f"*.{fmt}")
        audio_files.extend(glob.glob(pattern))
    audio_files.sort()
    return audio_files


# ============================================================================
# AUDIO MERGER GUI
# ============================================================================

class AudioMergerGUI:
    """Simple Audio Merger GUI"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎵 Audio Merger"
        self.selected_folder = ""
        self.audio_files = []
        self.setup_simple_ui()
    
    def setup_simple_ui(self):
        """Setup simplified UI"""
        self.page.controls.clear()
        
        # Title
        title = ft.Text("🎵 Audio Merger", size=24, weight=ft.FontWeight.BOLD)
        
        # Folder Input
        self.folder_field = ft.TextField(label="📁 Audio Folder", read_only=True, expand=True)
        browse_btn = ft.ElevatedButton("Browse Folder", on_click=self.browse_folder)
        
        # Files List
        self.files_text = ft.Text("No folder selected", size=12)
        
        # Effect Selection
        self.effect_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="normal", label="🔗 Direct Merge (No Effects)"),
                ft.Radio(value="crossfade", label="🔄 Crossfade (2s)"),
                ft.Radio(value="gap", label="⏸️ Gap/Silence (1s)"),
            ]),
            value="normal"
        )
        
        # Status
        self.status_text = ft.Text("Ready", size=12)
        
        # Merge Button
        merge_btn = ft.ElevatedButton(
            "🎵 Merge Audio",
            on_click=self.start_merge,
            bgcolor=colors.BLUE,
            color=colors.WHITE
        )
        
        # Layout
        content = ft.Column([
            title,
            ft.Container(height=20),
            ft.Row([self.folder_field, browse_btn]),
            ft.Container(height=10),
            self.files_text,
            ft.Container(height=10),
            ft.Text("Effects:", weight=ft.FontWeight.BOLD),
            self.effect_radio,
            ft.Container(height=20),
            merge_btn,
            ft.Container(height=20),
            self.status_text,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.add(content)
        self.page.update()
    
    def browse_folder(self, e):
        """Browse folder"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.selected_folder = e.path
                self.folder_field.value = e.path
                self.scan_files()
                self.page.update()
        
        picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(picker)
        self.page.update()
        picker.get_directory_path()
    
    def scan_files(self):
        """Scan audio files"""
        self.audio_files = get_audio_files(self.selected_folder)
        if self.audio_files:
            self.files_text.value = f"✅ Found {len(self.audio_files)} audio files"
        else:
            self.files_text.value = "❌ No audio files found"
    
    def start_merge(self, e):
        """Start merging"""
        if not self.audio_files:
            self.status_text.value = "❌ Select a folder with audio files!"
            self.page.update()
            return
        
        def merge_thread():
            self.status_text.value = "🔄 Merging audio files..."
            self.page.update()
            
            try:
                from pydub import AudioSegment
                
                # Configure pydub to use portable FFmpeg if available
                ffmpeg_exe = get_ffmpeg_path()
                if ffmpeg_exe and ffmpeg_exe != 'ffmpeg':
                    AudioSegment.converter = ffmpeg_exe
                    AudioSegment.ffmpeg = ffmpeg_exe
                    AudioSegment.ffprobe = ffmpeg_exe.replace('ffmpeg.exe', 'ffprobe.exe')
                
                # Load first file
                combined = AudioSegment.from_file(self.audio_files[0])
                
                effect = self.effect_radio.value
                
                # Merge remaining files
                for audio_file in self.audio_files[1:]:
                    next_audio = AudioSegment.from_file(audio_file)
                    
                    if effect == "crossfade":
                        combined = combined.append(next_audio, crossfade=2000)
                    elif effect == "gap":
                        silence = AudioSegment.silent(duration=1000)
                        combined = combined + silence + next_audio
                    else:
                        combined += next_audio
                
                # Export
                output_file = os.path.join(self.selected_folder, "merged_output.mp3")
                combined.export(output_file, format="mp3")
                
                self.status_text.value = f"✅ Merged! Saved: {output_file}"
            except Exception as ex:
                self.status_text.value = f"❌ Error: {str(ex)}"
            
            self.page.update()
        
        threading.Thread(target=merge_thread, daemon=True).start()


# ============================================================================
# SOCMED DOWNLOADER GUI (Simplified)
# ============================================================================

class SocMedDownloaderGUI:
    """Simple SocMed Downloader GUI"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🌐 SocMed Downloader"
        self.download_folder = str(Path.home() / "Downloads" / "SocMed_Downloads")
        self.setup_simple_ui()
    
    def setup_simple_ui(self):
        """Setup simplified UI"""
        self.page.controls.clear()
        
        # Title
        title = ft.Text("🌐 SocMed Downloader", size=24, weight=ft.FontWeight.BOLD)
        subtitle = ft.Text("YouTube, TikTok, Instagram, Facebook, Twitter/X", size=14, color=colors.GREY_600)
        
        # URL Input
        self.url_field = ft.TextField(label="🔗 URL", expand=True)
        
        # Format Selection
        self.format_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="video", label="🎬 Video"),
                ft.Radio(value="audio", label="🎵 Audio (MP3)"),
            ]),
            value="video"
        )
        
        # Progress
        self.progress_text = ft.Text("Ready", size=12)
        self.progress_bar = ft.ProgressBar(value=0, expand=True)
        
        # Download Button
        download_btn = ft.ElevatedButton(
            "🚀 Download",
            on_click=self.start_download,
            bgcolor=colors.GREEN,
            color=colors.WHITE,
            width=200
        )
        
        # Layout
        content = ft.Column([
            title,
            subtitle,
            ft.Container(height=20),
            self.url_field,
            ft.Container(height=10),
            ft.Text("Format:", weight=ft.FontWeight.BOLD),
            self.format_radio,
            ft.Container(height=20),
            download_btn,
            ft.Container(height=20),
            self.progress_text,
            self.progress_bar,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.add(content)
        self.page.update()
    
    def start_download(self, e):
        """Start download"""
        url = self.url_field.value.strip() if self.url_field.value else ""
        if not url:
            self.progress_text.value = "❌ Please enter URL!"
            self.page.update()
            return
        
        def download_thread():
            self.progress_text.value = "🔄 Downloading..."
            self.page.update()
            
            try:
                import yt_dlp
                
                os.makedirs(self.download_folder, exist_ok=True)
                os.chdir(self.download_folder)
                
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'quiet': True,
                    'no_warnings': True,
                }
                
                if self.format_radio.value == "audio":
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    ydl_opts['format'] = 'bestvideo+bestaudio/best'
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                
                self.progress_text.value = f"✅ Download complete! Saved to: {self.download_folder}"
                self.progress_bar.value = 1.0
            except Exception as ex:
                self.progress_text.value = f"❌ Error: {str(ex)}"
                self.progress_bar.value = 0
            
            self.page.update()
        
        threading.Thread(target=download_thread, daemon=True).start()


# ============================================================================
# MAIN LAUNCHER
# ============================================================================

class MediaToolsLauncher:
    """Main launcher for all tools"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬 Media Tools Zakkutsu"
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        self.current_tool = None
        self.setup_home()
    
    def setup_home(self):
        """Setup home screen"""
        self.page.controls.clear()
        
        # Check system status
        ffmpeg_ok = check_ffmpeg()
        ytdlp_ok = check_ytdlp()
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icons.APPS, size=50, color=colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text("Media Tools Zakkutsu", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("All-in-One Standalone Edition", size=16, color=colors.GREY_600),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=30,
            bgcolor=colors.DEEP_PURPLE_50,
            border_radius=15,
            margin=ft.margin.only(bottom=20)
        )
        
        # System status
        status_row = [
            ft.Icon(
                icons.CHECK_CIRCLE if ffmpeg_ok else icons.ERROR,
                color=colors.GREEN if ffmpeg_ok else colors.RED,
                size=20
            ),
            ft.Text(
                "FFmpeg: " + ("OK" if ffmpeg_ok else "Not Found"),
                color=colors.GREEN if ffmpeg_ok else colors.RED
            ),
        ]
        
        # Add download button if FFmpeg not found
        if not ffmpeg_ok:
            status_row.append(
                ft.TextButton(
                    "Download",
                    icon=icons.DOWNLOAD,
                    on_click=lambda e: self.show_ffmpeg_download_dialog()
                )
            )
        
        status_row.extend([
            ft.Container(width=20),
            ft.Icon(
                icons.CHECK_CIRCLE if ytdlp_ok else icons.ERROR,
                color=colors.GREEN if ytdlp_ok else colors.RED,
                size=20
            ),
            ft.Text(
                "yt-dlp: " + ("OK" if ytdlp_ok else "Not Found"),
                color=colors.GREEN if ytdlp_ok else colors.RED
            ),
        ])
        
        status = ft.Container(
            content=ft.Row(
                status_row,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            padding=10,
            bgcolor=colors.BLUE_50,
            border_radius=8,
            margin=ft.margin.only(bottom=20)
        )
        
        # Tool cards
        cards = ft.Column([
            ft.Text("Select a Tool", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Row([
                self.create_card("🎵 YT Playlist\nDownloader", colors.RED, lambda e: self.launch_tool("playlist")),
                self.create_card("🔁 Media\nLooper", colors.TEAL, lambda e: self.launch_tool("looper")),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),
            ft.Row([
                self.create_card("🎵 Audio\nMerger", colors.BLUE, lambda e: self.launch_tool("merger")),
                self.create_card("🌐 SocMed\nDownloader", colors.GREEN, lambda e: self.launch_tool("socmed")),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Info
        info = ft.Container(
            content=ft.Column([
                ft.Divider(height=1),
                ft.Text("💡 FFmpeg required for optimal functionality", size=12, color=colors.GREY_600),
                ft.Row([
                    ft.TextButton("❌ Exit", on_click=lambda e: self.page.window.close()),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=20
        )
        
        # Main content
        content = ft.Column([
            header,
            status,
            cards,
            info,
        ], scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.page.add(content)
        self.page.update()
    
    def create_card(self, title, color, on_click):
        """Create tool card"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=15),
                ft.ElevatedButton(
                    "Launch",
                    icon=icons.ROCKET_LAUNCH,
                    bgcolor=color,
                    color=colors.WHITE,
                    on_click=on_click,
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=350,
            height=150,
            border=ft.border.all(2, color),
            border_radius=10,
            padding=20,
            bgcolor=colors.WHITE,
        )
    
    def launch_tool(self, tool_name):
        """Launch selected tool"""
        self.page.controls.clear()
        
        # Back button
        back_btn = ft.ElevatedButton(
            "🏠 Back to Home",
            on_click=lambda e: self.setup_home(),
            bgcolor=colors.GREY_600,
            color=colors.WHITE
        )
        
        # Tool container
        tool_container = ft.Container(expand=True, padding=10)
        
        self.page.add(ft.Column([
            ft.Container(content=back_btn, padding=10),
            tool_container
        ], expand=True))
        
        # Initialize tool
        app_page = self.create_pseudo_page(tool_container)
        
        if tool_name == "playlist":
            self.current_tool = PlaylistDownloaderGUI(app_page)
        elif tool_name == "looper":
            self.current_tool = MediaLooperGUI(app_page)
        elif tool_name == "merger":
            self.current_tool = AudioMergerGUI(app_page)
        elif tool_name == "socmed":
            self.current_tool = SocMedDownloaderGUI(app_page)
        
        self.page.update()
    
    def show_ffmpeg_download_dialog(self):
        """Show FFmpeg download dialog"""
        progress_bar = ft.ProgressBar(width=400, value=0)
        status_text = ft.Text("Ready to download FFmpeg portable...", size=14)
        
        def update_progress(message, percent):
            status_text.value = message
            if percent >= 0:
                progress_bar.value = percent / 100.0
            self.page.update()
        
        def start_download(e):
            download_btn.disabled = True
            close_btn.disabled = True
            self.page.update()
            
            # Run download in thread
            import threading
            def download_thread():
                success = download_ffmpeg_portable(self.page, update_progress)
                if success:
                    status_text.value = "✅ FFmpeg installed successfully! Restart the app."
                    status_text.color = colors.GREEN
                    close_btn.disabled = False
                    # Refresh home screen after 2 seconds
                    import time
                    time.sleep(2)
                    self.page.close(dialog)
                    self.setup_home()
                else:
                    status_text.value = "❌ Download failed. Try manual installation."
                    status_text.color = colors.RED
                    download_btn.disabled = False
                    close_btn.disabled = False
                self.page.update()
            
            threading.Thread(target=download_thread, daemon=True).start()
        
        download_btn = ft.ElevatedButton(
            "Download FFmpeg (~100 MB)",
            icon=icons.DOWNLOAD,
            on_click=start_download,
            bgcolor=colors.BLUE
        )
        
        close_btn = ft.TextButton("Close", on_click=lambda e: self.page.close(dialog))
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Download FFmpeg Portable"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text(
                        "FFmpeg is required for media processing.\n"
                        "Download portable version (~100 MB)?",
                        size=14
                    ),
                    ft.Container(height=10),
                    ft.Text("Source: github.com/BtbN/FFmpeg-Builds", size=12, color=colors.GREY_600),
                    ft.Container(height=20),
                    progress_bar,
                    ft.Container(height=10),
                    status_text,
                ], tight=True),
                width=450,
                height=200
            ),
            actions=[
                download_btn,
                close_btn,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dialog)
        dialog.open = True
        self.page.update()
    
    def create_pseudo_page(self, container):
        """Create pseudo page for tools"""
        class PseudoPage:
            def __init__(self, page, container):
                self.page = page
                self.container = container
                self.title = page.title
                self.window_width = page.window_width
                self.window_height = page.window_height
                self.theme_mode = page.theme_mode
                self.controls = []
                self.overlay = page.overlay
                self.snack_bar = None
                self.dialog = None
            
            def add(self, *controls):
                for control in controls:
                    self.controls.append(control)
                    self.container.content = ft.Column(self.controls, expand=True, scroll=ft.ScrollMode.AUTO)
                self.update()
            
            def update(self):
                self.page.update()
            
            def run_thread_safe(self, func):
                self.page.run_thread_safe(func)
            
            def open(self, dialog):
                self.page.dialog = dialog
                dialog.open = True
                self.page.update()
            
            def close(self, dialog):
                dialog.open = False
                self.page.update()
        
        return PseudoPage(self.page, container)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main(page: ft.Page):
    """Main entry point"""
    MediaToolsLauncher(page)


if __name__ == "__main__":
    print("="*70)
    print("  MEDIA TOOLS ZAKKUTSU - ALL-IN-ONE STANDALONE")
    print("="*70)
    print()
    print("Tools Included:")
    print("  1. YT Playlist Downloader")
    print("  2. Media Looper")
    print("  3. Audio Merger")
    print("  4. SocMed Downloader")
    print()
    print("Checking dependencies...")
    print()
    
    # Check FFmpeg
    if check_ffmpeg():
        print("[OK] FFmpeg: OK")
    else:
        print("[!] FFmpeg: Not Found")
        print("    Install: winget install FFmpeg")
        print("    Or use auto-download feature in the app")
    
    # Check yt-dlp
    if check_ytdlp():
        print("[OK] yt-dlp: OK")
    else:
        print("[INFO] yt-dlp: Not Found (will auto-install)")
    
    print()
    print("[LAUNCH] Starting GUI...")
    print("="*70)
    print()
    
    # Launch Flet app
    ft.app(target=main, view=ft.AppView.FLET_APP)
