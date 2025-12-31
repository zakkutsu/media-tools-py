#!/usr/bin/env python3
"""
GUI untuk YouTube Batch Downloader menggunakan Flet
Interface grafis modern untuk download multiple video individual YouTube
"""

import flet as ft
import threading
import os
import sys
from pathlib import Path
import asyncio
import time

# Import our batch downloader
from batch_downloader import BatchDownloader


class BatchDownloaderGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬 YouTube Batch Downloader"
        self.page.window_width = 900
        self.page.window_height = 800
        self.page.window_resizable = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 10
        
        # Initialize downloader
        self.downloader = BatchDownloader()
        
        # Variables
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Batch")
        self.download_type = "video_best"
        self.output_template = "%(title)s.%(ext)s"
        self.auto_numbering = False
        self.continue_on_error = True
        self.embed_thumbnail = True  # NEW: Optional thumbnail embedding
        self.embed_metadata = True   # NEW: Optional metadata embedding
        
        # Statistics tracking
        self.start_time = None
        self.total_downloaded_size = 0
        self.current_video_title = ""
        
        # UI Components
        self.folder_field = None
        self.url_field = None
        self.url_list = None
        self.url_count_text = None
        self.template_field = None
        self.progress_bar = None
        self.progress_label = None
        self.output_log = None
        self.download_btn = None
        self.ytdlp_status_text = None
        self.install_btn = None
        
        # Enhanced progress components
        self.speed_label = None
        self.eta_label = None
        self.stats_text = None
        
        # Setup UI
        self.setup_ui()
        self.update_ytdlp_status()
        self.update_url_count()
    
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
                    "🎬 YouTube Batch Downloader",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                ft.Text(
                    "Download multiple individual YouTube videos",
                    size=14,
                    color=ft.Colors.GREY_600,
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
            icon=ft.Icons.DOWNLOAD
        )
        
        ytdlp_status_section = ft.Container(
            content=ft.Row([
                self.ytdlp_status_text,
                self.install_btn
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            padding=ft.padding.all(10),
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
            icon=ft.Icons.FOLDER_OPEN,
            on_click=self.browse_folder
        )
        
        folder_section = ft.Container(
            content=ft.Row([self.folder_field, browse_btn]),
            padding=ft.padding.only(bottom=10)
        )
        main_content.controls.append(folder_section)
        
        # URL Management Section
        url_management = self.create_url_management_section()
        main_content.controls.append(url_management)
        
        # Download Options Section
        options_section = self.create_download_options_section()
        main_content.controls.append(options_section)
        
        # Download Buttons
        self.download_btn = ft.ElevatedButton(
            text="🚀 Start Download",
            icon=ft.Icons.PLAY_ARROW,
            on_click=self.start_download,
            width=200,
            height=50,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.BLUE_600
            )
        )
        
        self.retry_failed_btn = ft.ElevatedButton(
            text="🔄 Retry Failed",
            icon=ft.Icons.REFRESH,
            on_click=self.retry_failed_downloads,
            width=150,
            height=50,
            disabled=True,
            style=ft.ButtonStyle(
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.ORANGE_600
            )
        )
        
        self.clear_failed_btn = ft.OutlinedButton(
            text="🗑️ Clear Failed",
            icon=ft.Icons.DELETE_OUTLINE,
            on_click=self.clear_failed_urls,
            width=140,
            height=50,
            disabled=True,
            style=ft.ButtonStyle(
                color=ft.Colors.RED_600,
            )
        )
        
        download_section = ft.Container(
            content=ft.Row([
                self.download_btn,
                self.retry_failed_btn,
                self.clear_failed_btn
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=ft.padding.symmetric(vertical=20)
        )
        main_content.controls.append(download_section)
        
        # Progress Section
        progress_section = self.create_progress_section()
        main_content.controls.append(progress_section)
        
        # Output Log Section
        output_section = self.create_output_section()
        main_content.controls.append(output_section)
        
        # Footer (inside scrollable content)
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
        main_content.controls.append(footer)
        
        # Add main content to page
        self.page.add(main_content)
    
    def create_url_management_section(self):
        """Create URL management section"""
        # URL Input
        self.url_field = ft.TextField(
            label="Enter YouTube URL",
            hint_text="Paste YouTube video URL here...",
            expand=True,
            on_submit=self.add_url
        )
        
        add_btn = ft.ElevatedButton(
            text="Add URL",
            icon=ft.Icons.ADD,
            on_click=self.add_url
        )
        
        url_input_row = ft.Row([self.url_field, add_btn])
        
        # URL Management Buttons
        load_btn = ft.ElevatedButton(
            text="📄 Load from File",
            icon=ft.Icons.FILE_OPEN,
            on_click=self.load_urls_from_file,
            style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_100)
        )
        
        save_btn = ft.ElevatedButton(
            text="💾 Save to File",
            icon=ft.Icons.SAVE,
            on_click=self.save_urls_to_file,
            style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_100)
        )
        
        clear_btn = ft.ElevatedButton(
            text="🗑️ Clear All",
            icon=ft.Icons.CLEAR,
            on_click=self.clear_all_urls,
            style=ft.ButtonStyle(bgcolor=ft.Colors.RED_100)
        )
        
        self.url_count_text = ft.Text("URLs: 0", weight=ft.FontWeight.BOLD, size=14)
        
        button_row = ft.Row([
            load_btn, save_btn, clear_btn,
            ft.Container(expand=True),  # Spacer
            self.url_count_text
        ])
        
        # URL List
        self.url_list = ft.ListView(
            height=200,
            spacing=5,
            padding=ft.padding.all(10)
        )
        
        url_list_container = ft.Container(
            content=self.url_list,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            bgcolor=ft.Colors.GREY_50
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Text("🔗 URL Management", size=16, weight=ft.FontWeight.BOLD),
                url_input_row,
                button_row,
                ft.Text("URL List:", size=12, weight=ft.FontWeight.BOLD),
                url_list_container
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
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
        
        # Options Checkboxes
        auto_numbering_checkbox = ft.Checkbox(
            label="🔢 Auto Number Files (01 - Title.ext)",
            value=self.auto_numbering,
            on_change=self.on_auto_numbering_change
        )
        
        continue_on_error_checkbox = ft.Checkbox(
            label="🔄 Continue on Error",
            value=self.continue_on_error,
            on_change=self.on_continue_on_error_change
        )
        
        # Embed Thumbnail Checkbox (NEW)
        embed_thumbnail_checkbox = ft.Checkbox(
            label="🖼️ Embed Thumbnail (album art/cover) - Disable for faster download",
            value=self.embed_thumbnail,
            on_change=self.on_embed_thumbnail_change,
            tooltip="Embeds YouTube thumbnail as album art. Disable if you have slow internet."
        )
        
        # Embed Metadata Checkbox (NEW)
        embed_metadata_checkbox = ft.Checkbox(
            label="📋 Add Metadata (title, artist, date) - Disable for faster download",
            value=self.embed_metadata,
            on_change=self.on_embed_metadata_change,
            tooltip="Adds metadata to downloaded files. Disable if you have slow internet."
        )
        
        # Help Text
        help_text = ft.Text(
            "Template variables: %(title)s (title), %(ext)s (extension), %(uploader)s (channel)",
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
                continue_on_error_checkbox,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Text("🎨 Quality & Metadata Options:", size=12, weight=ft.FontWeight.BOLD),
                embed_thumbnail_checkbox,
                embed_metadata_checkbox,
                ft.Text("💡 Tip: Disable thumbnail & metadata for faster downloads on slow internet", 
                       size=10, color=ft.Colors.BLUE_600, italic=True),
                help_text
            ]),
            padding=ft.padding.all(10),
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
    
    def create_progress_section(self):
        """Create progress section with enhanced details"""
        self.progress_label = ft.Text("Ready to download", size=12, weight=ft.FontWeight.BOLD)
        self.progress_bar = ft.ProgressBar(value=0, expand=True)
        
        # Enhanced progress info
        self.speed_label = ft.Text("Speed: -- MB/s", size=11, color=ft.Colors.BLUE_600)
        self.eta_label = ft.Text("ETA: --:--", size=11, color=ft.Colors.GREEN_600)
        self.stats_text = ft.Text("", size=11, color=ft.Colors.GREY_700)
        
        return ft.Container(
            content=ft.Column([
                ft.Text("📊 Download Progress", size=16, weight=ft.FontWeight.BOLD),
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
                ft.Text("📋 Download Log", size=16, weight=ft.FontWeight.BOLD),
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
    
    def add_url(self, e):
        """Add URL to the list"""
        url = self.url_field.value.strip() if self.url_field.value else ""
        if not url:
            return
        
        if self.downloader.add_url(url):
            # Add to UI list
            url_item = ft.ListTile(
                title=ft.Text(url, size=12),
                subtitle=ft.Text("Ready", color=ft.Colors.BLUE_600),
                trailing=ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Remove URL",
                    on_click=lambda e, url=url: self.remove_url(url)
                )
            )
            self.url_list.controls.append(url_item)
            
            self.url_field.value = ""
            self.update_url_count()
            self.log_output(f"✅ URL added: {url}")
            self.page.update()
        else:
            self.show_dialog("Warning", "URL already exists or invalid!")
    
    def remove_url(self, url):
        """Remove URL from list"""
        if url in self.downloader.url_list:
            self.downloader.url_list.remove(url)
            self.refresh_url_list()
            self.log_output(f"🗑️ URL removed: {url}")
    
    def load_urls_from_file(self, e):
        """Load URLs from a text file"""
        def pick_files_result(e: ft.FilePickerResultEvent):
            if e.files:
                file_path = e.files[0].path
                added_count = self.downloader.add_urls_from_file(file_path)
                if added_count > 0:
                    self.refresh_url_list()
                    self.log_output(f"✅ Loaded {added_count} URLs from file")
                else:
                    self.show_dialog("Warning", "No valid URLs found in file!")
        
        pick_files_dialog = ft.FilePicker(on_result=pick_files_result)
        self.page.overlay.append(pick_files_dialog)
        self.page.update()
        
        pick_files_dialog.pick_files(
            dialog_title="Select URL file",
            allowed_extensions=["txt"],
            allow_multiple=False
        )
    
    def save_urls_to_file(self, e):
        """Save current URLs to a text file"""
        if not self.downloader.url_list:
            self.show_dialog("Warning", "No URLs to save!")
            return
        
        def save_file_result(e: ft.FilePickerResultEvent):
            if e.path:
                try:
                    with open(e.path, 'w', encoding='utf-8') as f:
                        for url in self.downloader.url_list:
                            f.write(url + '\n')
                    self.log_output(f"✅ URLs saved to: {e.path}")
                except Exception as ex:
                    self.show_dialog("Error", f"Failed to save file: {ex}")
        
        save_file_dialog = ft.FilePicker(on_result=save_file_result)
        self.page.overlay.append(save_file_dialog)
        self.page.update()
        
        save_file_dialog.save_file(
            dialog_title="Save URLs to file",
            file_name="youtube_urls.txt",
            file_type=ft.FilePickerFileType.CUSTOM,
            allowed_extensions=["txt"]
        )
    
    def clear_all_urls(self, e):
        """Clear all URLs"""
        if self.downloader.url_list:
            def close_dlg(e):
                dlg_modal.open = False
                self.page.update()
            
            def confirm_clear(e):
                self.downloader.clear_url_list()
                self.refresh_url_list()
                self.log_output("🗑️ All URLs cleared")
                close_dlg(e)
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm"),
                content=ft.Text("Are you sure you want to clear all URLs?"),
                actions=[
                    ft.TextButton("Cancel", on_click=close_dlg),
                    ft.TextButton("Clear All", on_click=confirm_clear),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            
            self.page.dialog = dlg_modal
            dlg_modal.open = True
            self.page.update()
    
    def refresh_url_list(self):
        """Refresh the URL list display"""
        self.url_list.controls.clear()
        
        for i, url in enumerate(self.downloader.url_list, 1):
            status = 'Ready'
            status_color = ft.Colors.BLUE_600
            
            if url in self.downloader.successful_downloads:
                status = 'Success'
                status_color = ft.Colors.GREEN_600
            elif url in self.downloader.failed_downloads:
                status = 'Failed'
                status_color = ft.Colors.RED_600
            
            url_item = ft.ListTile(
                title=ft.Text(f"{i}. {url}", size=12),
                subtitle=ft.Text(status, color=status_color),
                trailing=ft.IconButton(
                    icon=ft.Icons.DELETE,
                    icon_color=ft.Colors.RED_400,
                    tooltip="Remove URL",
                    on_click=lambda e, url=url: self.remove_url(url)
                )
            )
            self.url_list.controls.append(url_item)
        
        self.update_url_count()
        self.page.update()
    
    def update_url_count(self):
        """Update URL count display"""
        count = len(self.downloader.url_list)
        self.url_count_text.value = f"URLs: {count}"
        self.page.update()
    
    def on_download_type_change(self, e):
        """Handle download type change"""
        self.download_type = e.control.value
    
    def on_template_change(self, e):
        """Handle template change"""
        self.output_template = e.control.value
    
    def on_auto_numbering_change(self, e):
        """Handle auto numbering checkbox change"""
        self.auto_numbering = e.control.value
    
    def on_continue_on_error_change(self, e):
        """Handle continue on error checkbox change"""
        self.continue_on_error = e.control.value
    
    def on_embed_thumbnail_change(self, e):
        """Handle embed thumbnail checkbox change"""
        self.embed_thumbnail = e.control.value
    
    def on_embed_metadata_change(self, e):
        """Handle embed metadata checkbox change"""
        self.embed_metadata = e.control.value
        self.continue_on_error = e.control.value
    
    def reset_template(self, e):
        """Reset output template to default"""
        if self.auto_numbering:
            self.output_template = "%(title)s.%(ext)s"  # Will be modified by auto_numbering
        else:
            self.output_template = "%(title)s.%(ext)s"
        
        self.template_field.value = self.output_template
        self.page.update()
    
    def start_download(self, e):
        """Start batch download process"""
        # Validate inputs with detailed logging
        self.log_output("🔍 Validating download requirements...")
        
        if not self.downloader.yt_dlp_available:
            error_msg = "❌ yt-dlp is not available. Please install it first using the 'Install/Update yt-dlp' button above!"
            self.log_output(error_msg)
            self.show_dialog("Error - yt-dlp Not Found", 
                "yt-dlp is required for downloading YouTube videos.\n\n"
                "Please click the 'Install/Update yt-dlp' button at the top of the window to install it.\n\n"
                "After installation, try downloading again.")
            return
        
        if not self.downloader.url_list:
            error_msg = "⚠️ No URLs in the download list. Please add some YouTube URLs first!"
            self.log_output(error_msg)
            self.show_dialog("Warning - No URLs", 
                "Please add some YouTube URLs before starting the download.\n\n"
                "You can:\n"
                "• Paste a URL and click 'Add URL'\n"
                "• Load URLs from a text file\n"
                "• Add multiple URLs one by one")
            return
        
        folder = self.download_folder.strip()
        if not folder:
            error_msg = "⚠️ Download folder not specified!"
            self.log_output(error_msg)
            self.show_dialog("Warning - No Folder", 
                "Please select a download folder first!\n\n"
                "Click the 'Browse' button to choose where files should be saved.")
            return
        
        # Set download folder
        self.log_output(f"📁 Setting download folder: {folder}")
        if not self.downloader.set_download_folder(folder):
            error_msg = f"❌ Failed to create download folder: {folder}"
            self.log_output(error_msg)
            self.show_dialog("Error - Folder Creation Failed", 
                f"Could not create or access the download folder:\n{folder}\n\n"
                f"Please check:\n"
                f"• Folder path is valid\n"
                f"• You have write permissions\n"
                f"• Drive has enough space")
            return
        
        self.log_output(f"✅ Validation passed! Ready to download {len(self.downloader.url_list)} URLs")
        
        def download_thread():
            self.log_output("="*70)
            self.log_output("🚀 Starting batch download...")
            self.log_output(f"Total URLs: {len(self.downloader.url_list)}")
            self.log_output(f"Type: {self.download_type}")
            self.log_output(f"Folder: {folder}")
            self.log_output(f"Auto Numbering: {'Enabled' if self.auto_numbering else 'Disabled'}")
            self.log_output(f"Embed Thumbnail: {'Enabled' if self.embed_thumbnail else 'Disabled'}")
            self.log_output(f"Embed Metadata: {'Enabled' if self.embed_metadata else 'Disabled'}")
            self.log_output("="*70)
            
            # Start timer for statistics
            self.start_time = time.time()
            
            # Disable UI elements
            try:
                self.download_btn.disabled = True
                self.download_btn.text = "Downloading..."
                self.reset_progress()
                self.page.update()
            except:
                pass
            
            download_type = self.download_type
            template = self.output_template or "%(title)s.%(ext)s"
            auto_numbering = self.auto_numbering
            continue_on_error = self.continue_on_error
            embed_thumbnail = self.embed_thumbnail
            embed_metadata = self.embed_metadata
            
            try:
                if download_type == "video_best":
                    result = self.downloader.batch_download_videos(
                        quality="best", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        embed_thumbnail=embed_thumbnail, embed_metadata=embed_metadata,
                        progress_callback=self.update_progress)
                elif download_type == "video_720p":
                    result = self.downloader.batch_download_videos(
                        quality="720p", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        embed_thumbnail=embed_thumbnail, embed_metadata=embed_metadata,
                        progress_callback=self.update_progress)
                elif download_type == "video_480p":
                    result = self.downloader.batch_download_videos(
                        quality="480p", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        embed_thumbnail=embed_thumbnail, embed_metadata=embed_metadata,
                        progress_callback=self.update_progress)
                elif download_type == "audio_mp3":
                    result = self.downloader.batch_download_audio(
                        audio_format="mp3", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        embed_thumbnail=embed_thumbnail, embed_metadata=embed_metadata,
                        progress_callback=self.update_progress)
                
                # Update UI with results
                try:
                    self.refresh_url_list()
                except:
                    pass
                
            except Exception as ex:
                self.log_output(f"❌ Error during batch download: {ex}")
                result = {"success": 0, "failed": len(self.downloader.url_list)}
            
            # Re-enable UI elements
            try:
                self.download_btn.disabled = False
                self.download_btn.text = "🚀 Start Download"
                
                # Enable retry/clear buttons if there are failed downloads
                if len(self.downloader.failed_downloads) > 0:
                    self.retry_failed_btn.disabled = False
                    self.clear_failed_btn.disabled = False
                
                self.page.update()
            except:
                pass
            
            # Show completion message
            if result["success"] > 0:
                self.log_output("="*70)
                self.log_output("🎉 Batch download completed!")
                self.log_output(f"✅ Successful: {result['success']}")
                self.log_output(f"❌ Failed: {result['failed']}")
                self.log_output(f"📁 Files saved to: {folder}")
                self.log_output("="*70)
                
                self.show_dialog("Success", 
                    f"Batch download completed!\n\n"
                    f"✅ Successful: {result['success']}\n"
                    f"❌ Failed: {result['failed']}\n\n"
                    f"Files saved to:\n{folder}")
            else:
                self.log_output("="*70)
                self.log_output("😞 Batch download failed!")
                self.log_output("Please check URLs and internet connection.")
                self.log_output("="*70)
                
                self.show_dialog("Error", 
                    f"Batch download failed!\n\n"
                    f"All {result['failed']} downloads failed.\n\n"
                    f"Please check:\n"
                    f"- Internet connection\n"
                    f"- YouTube URLs validity\n"
                    f"- Download folder permissions")
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def update_progress(self, current, total, percentage, title=""):
        """Update progress display with enhanced statistics"""
        try:
            # Update progress label
            if title:
                self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%) - {title}"
            else:
                self.progress_label.value = f"🎵 [{current}/{total}] ({percentage:.1f}%)"
            
            # Update progress bar
            self.progress_bar.value = percentage / 100.0
            
            # Calculate elapsed time and speed
            if self.start_time:
                elapsed = time.time() - self.start_time
                if elapsed > 0:
                    speed = current / elapsed  # videos per second
                    remaining = total - current
                    eta_seconds = remaining / speed if speed > 0 else 0
                    
                    # Update speed (converted to videos/minute for readability)
                    videos_per_min = speed * 60
                    self.speed_label.value = f"Speed: {videos_per_min:.1f} videos/min"
                    
                    # Update ETA
                    eta_mins = int(eta_seconds // 60)
                    eta_secs = int(eta_seconds % 60)
                    self.eta_label.value = f"ETA: {eta_mins:02d}:{eta_secs:02d}"
                    
                    # Update statistics
                    elapsed_mins = int(elapsed // 60)
                    elapsed_secs = int(elapsed % 60)
                    self.stats_text.value = f"Elapsed: {elapsed_mins:02d}:{elapsed_secs:02d} | Success: {len(self.downloader.successful_downloads)} | Failed: {len(self.downloader.failed_downloads)}"
            
            # Update GUI
            self.page.update()
        except Exception as e:
            # Silently ignore UI update errors in background thread
            pass
    
    def reset_progress(self):
        """Reset progress display"""
        self.progress_label.value = "Ready to download"
        self.progress_bar.value = 0
        self.speed_label.value = "Speed: -- MB/s"
        self.eta_label.value = "ETA: --:--"
        self.stats_text.value = ""
        self.start_time = None
        self.page.update()
    
    def log_output(self, message):
        """Add message to output log"""
        try:
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
        except Exception as e:
            # Silently ignore UI update errors in background thread
            pass
    
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
    
    def retry_failed_downloads(self, e):
        """Retry only the failed downloads"""
        if not self.downloader.failed_downloads:
            self.show_dialog("Info", "No failed downloads to retry!")
            return
        
        failed_count = len(self.downloader.failed_downloads)
        self.log_output(f"🔄 Retrying {failed_count} failed downloads...")
        
        # Create new URL list with only failed URLs
        failed_urls = self.downloader.failed_downloads.copy()
        
        # Clear current lists
        self.downloader.clear_url_list()
        
        # Add failed URLs back
        for url in failed_urls:
            self.downloader.add_url(url)
        
        # Refresh UI
        self.refresh_url_list()
        
        # Disable retry/clear buttons
        self.retry_failed_btn.disabled = True
        self.clear_failed_btn.disabled = True
        self.page.update()
        
        self.log_output(f"✅ Ready to retry {failed_count} URLs. Click 'Start Batch Download' to begin.")
    
    def clear_failed_urls(self, e):
        """Clear failed URLs from the list"""
        if not self.downloader.failed_downloads:
            self.show_dialog("Info", "No failed downloads to clear!")
            return
        
        failed_count = len(self.downloader.failed_downloads)
        
        # Remove failed URLs from downloader's list
        for url in self.downloader.failed_downloads:
            if url in self.downloader.url_list:
                self.downloader.url_list.remove(url)
        
        # Clear failed list
        self.downloader.failed_downloads.clear()
        
        # Refresh UI
        self.refresh_url_list()
        
        # Disable retry/clear buttons
        self.retry_failed_btn.disabled = True
        self.clear_failed_btn.disabled = True
        self.page.update()
        
        self.log_output(f"🗑️ Cleared {failed_count} failed URLs from the list")


def main(page: ft.Page):
    """Main function to run the Flet app"""
    app = BatchDownloaderGUI(page)


if __name__ == "__main__":
    ft.app(target=main)




