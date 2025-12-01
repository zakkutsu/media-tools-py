#!/usr/bin/env python3
"""
GUI untuk YouTube Playlist Downloader menggunakan Flet
Interface grafis modern untuk download playlist YouTube
"""

import flet as ft
import threading
import os
import sys
from pathlib import Path
import asyncio
import time

# Add parent directory to path for language_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from language_config import get_language, get_all_texts

# Import our playlist downloader
from playlist_downloader import PlaylistDownloader


class PlaylistDownloaderGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎵 YouTube Playlist Downloader"
        self.page.window_width = 850
        self.page.window_height = 750
        self.page.window_resizable = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 10
        
        # Language configuration
        self.current_language = get_language()
        self.translations = get_all_texts("youtube_downloader", self.current_language)
        self.common_translations = get_all_texts("common", self.current_language)
        
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
        self.current_progress_bar = None
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
                    self.translations.get("title_playlist", "🎵 YouTube Playlist Downloader"),
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    self.translations.get("desc_playlist", "Download complete YouTube playlists with ease"),
                    size=14,
                    color=ft.Colors.GREY_600,
                    text_align=ft.TextAlign.CENTER
                )
            ]),
            padding=ft.padding.only(bottom=20)
        )
        main_content.controls.append(title_section)
        
        # yt-dlp Status Section
        self.ytdlp_status_text = ft.Text(self.translations.get("ytdlp_status", "Checking yt-dlp status..."), size=12)
        self.install_btn = ft.ElevatedButton(
            text=self.translations.get("install_ytdlp", "📦 Install/Update yt-dlp"),
            on_click=self.install_update_ytdlp,
            icon=ft.Icons.DOWNLOAD
        )
        
        ytdlp_status_section = ft.Container(
            content=ft.Row([
                self.ytdlp_status_text,
                self.install_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
        main_content.controls.append(ytdlp_status_section)
        
        # Download Folder Section
        self.folder_field = ft.TextField(
            label=self.translations.get("download_folder", "📁 Download Folder"),
            value=self.download_folder,
            expand=True,
            on_change=self.on_folder_change
        )
        
        browse_btn = ft.ElevatedButton(
            text=self.common_translations.get("browse", "Browse"),
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self.browse_folder
        )
        
        folder_section = ft.Container(
            content=ft.Row([self.folder_field, browse_btn]),
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(folder_section)
        
        # Playlist URL Section
        self.url_field = ft.TextField(
            label=self.translations.get("url_input", "🔗 Playlist URL"),
            hint_text=self.translations.get("url_input", "Paste YouTube playlist URL here..."),
            expand=True,
            on_change=self.on_url_change,
            on_submit=self.get_playlist_info
        )
        
        self.get_info_btn = ft.ElevatedButton(
            text="Get Info",
            icon=ft.Icons.INFO,
            on_click=self.get_playlist_info,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100)
        )
        
        url_section = ft.Container(
            content=ft.Row([self.url_field, self.get_info_btn]),
            padding=ft.padding.only(bottom=5)
        )
        main_content.controls.append(url_section)
        
        # Playlist Info Display
        self.info_text = ft.Text("", color=ft.Colors.BLUE_600, size=12, weight=ft.FontWeight.BOLD)
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
            text=self.translations.get("start_download", "🚀 Start Download"),
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_download,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_600
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
            icon=ft.Icons.REFRESH,
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
            color=ft.Colors.GREY_600
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
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
    def create_progress_section(self):
        """Create progress section"""
        self.progress_label = ft.Text("Ready to download", size=12, weight=ft.FontWeight.BOLD)
        
        # Playlist Progress (Overall)
        playlist_progress_label = ft.Text("Playlist Progress:", size=10, weight=ft.FontWeight.BOLD)
        self.overall_progress_bar = ft.ProgressBar(value=0, expand=True)
        
        # Current Item Progress
        current_progress_label = ft.Text("Current Item Progress:", size=10, weight=ft.FontWeight.BOLD)
        self.current_progress_bar = ft.ProgressBar(value=0, expand=True)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 Download Progress", size=16, weight=ft.FontWeight.BOLD),
                self.progress_label,
                ft.Container(height=10),  # Spacer
                playlist_progress_label,
                ft.Container(
                    content=self.overall_progress_bar,
                    padding=ft.padding.symmetric(vertical=3)
                ),
                ft.Container(height=5),   # Spacer
                current_progress_label,
                ft.Container(
                    content=self.current_progress_bar,
                    padding=ft.padding.symmetric(vertical=3)
                )
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_300),
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
    
    def update_ytdlp_status(self):
        """Update yt-dlp status display"""
        if self.downloader.yt_dlp_available:
            self.ytdlp_status_text.value = "✅ yt-dlp is available"
            self.ytdlp_status_text.color = ft.Colors.GREEN_600
            self.install_btn.text = "Update yt-dlp"
        else:
            self.ytdlp_status_text.value = "❌ yt-dlp not found"
            self.ytdlp_status_text.color = ft.Colors.RED_600
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
        
        # Create file picker for directory
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
        # Clear previous info when URL changes
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
                self.info_text.color = ft.Colors.GREEN_600
                self.log_output(f"✅ {info_text}")
            else:
                self.playlist_info = None
                self.info_text.value = "❌ Failed to get playlist info"
                self.info_text.color = ft.Colors.RED_600
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
        
        # Update template accordingly
        current_template = self.output_template
        
        if self.auto_numbering:
            # Enable auto numbering - add playlist_index if not present
            if "%(playlist_index)s" not in current_template:
                if current_template.startswith("%(title)s"):
                    new_template = "%(playlist_index)s - " + current_template
                else:
                    new_template = "%(playlist_index)s - %(title)s.%(ext)s"
                self.output_template = new_template
                self.template_field.value = new_template
        else:
            # Disable auto numbering - remove only playlist_index, keep title
            new_template = current_template.replace("%(playlist_index)s - ", "")
            new_template = new_template.replace("%(playlist_index)s", "")
            # Clean up any double spaces
            new_template = " ".join(new_template.split())
            # Ensure we still have title in the template
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
        # Validate inputs
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
        
        # Set download folder
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
            
            # Disable UI elements
            self.download_btn.disabled = True
            self.download_btn.text = "Downloading..."
            self.reset_progress()
            self.current_progress_bar.value = None  # Indeterminate mode
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
            
            # Re-enable UI elements
            self.current_progress_bar.value = 0  # Back to determinate mode
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
        # Update progress label
        if title:
            self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%) - {title}"
        else:
            self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%)"
        
        # Update overall progress bar
        self.overall_progress_bar.value = percentage / 100.0
        
        # Current item progress is set to indeterminate during download
        # It could be made more sophisticated with individual file progress
        
        # Update GUI
        self.page.update()
    
    def reset_progress(self):
        """Reset progress display"""
        self.progress_label.value = "Ready to download"
        self.overall_progress_bar.value = 0
        self.current_progress_bar.value = 0
        self.page.update()
    
    def log_output(self, message):
        """Add message to output log"""
        log_entry = ft.Text(
            message,
            size=10,
            selectable=True
        )
        self.output_log.controls.append(log_entry)
        
        # Keep only last 100 entries to prevent memory issues
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


def main(page: ft.Page):
    """Main function to run the Flet app"""
    app = PlaylistDownloaderGUI(page)


if __name__ == "__main__":
    ft.app(target=main)

