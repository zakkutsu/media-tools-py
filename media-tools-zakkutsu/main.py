#!/usr/bin/env python3
"""
Media Tools Zakkutsu - All-in-One Executable Version
Unified version for building single .exe file
"""

import flet as ft
import os
import sys
from pathlib import Path

# Detect if running as PyInstaller executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    BASE_DIR = Path(sys._MEIPASS)
    TOOLS_DIR = BASE_DIR / "tools"
else:
    # Running as script
    BASE_DIR = Path(__file__).parent
    TOOLS_DIR = BASE_DIR / "tools"

# Add both BASE_DIR and TOOLS_DIR to path
for path_dir in [str(BASE_DIR), str(TOOLS_DIR)]:
    if path_dir not in sys.path:
        sys.path.insert(0, path_dir)

# Import language config
try:
    from language_config import get_language, set_language, get_available_languages, get_all_texts
except ImportError:
    def get_language(): return "id"
    def set_language(lang): return True
    def get_available_languages(): return {"id": {"name": "Bahasa Indonesia", "flag": "🇮🇩"}}
    def get_all_texts(section, lang): return {}

# Import all tool GUIs
try:
    from audio_merger_gui import AudioMergerGUI
except ImportError as e:
    print(f"Warning: Could not import AudioMergerGUI: {e}")
    AudioMergerGUI = None

try:
    from media_codec_detector_gui import MediaCodecDetectorGUI
except ImportError as e:
    print(f"Warning: Could not import MediaCodecDetectorGUI: {e}")
    MediaCodecDetectorGUI = None

try:
    from batch_downloader_gui_flet import BatchDownloaderGUI as BatchDownloaderFletGUI
except ImportError as e:
    print(f"Warning: Could not import BatchDownloaderFletGUI: {e}")
    BatchDownloaderFletGUI = None

try:
    from playlist_downloader_gui_flet import PlaylistDownloaderGUI as PlaylistDownloaderFletGUI
except ImportError as e:
    print(f"Warning: Could not import PlaylistDownloaderFletGUI: {e}")
    PlaylistDownloaderFletGUI = None

try:
    from socmed_downloader_gui import SocMedDownloaderGUI
except ImportError as e:
    print(f"Warning: Could not import SocMedDownloaderGUI: {e}")
    SocMedDownloaderGUI = None

try:
    from media_looper_gui_flet import MediaLooperGUI
except ImportError as e:
    print(f"Warning: Could not import MediaLooperGUI: {e}")
    MediaLooperGUI = None


class MediaToolsZakkutsu:
    """Main launcher for all media tools"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬 Media Tools Zakkutsu"
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.window_min_width = 700
        self.page.window_min_height = 600
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        
        # Language setup
        self.current_language = get_language()
        self.translations = get_all_texts("launcher", self.current_language)
        
        # Tool definitions
        self.tools = {
            "audio_merger": {
                "name": "🎵 Audio Merger",
                "desc": "Merge multiple audio files with crossfade & gap effects",
                "color": ft.colors.BLUE,
                "gui_class": AudioMergerGUI,
                "icon": ft.icons.AUDIO_FILE
            },
            "codec_detector": {
                "name": "🎬 Media Codec Detector",
                "desc": "Detect format and codec from media files",
                "color": ft.colors.PURPLE,
                "gui_class": MediaCodecDetectorGUI,
                "icon": ft.icons.INFO
            },
            "youtube_batch": {
                "name": "📥 YouTube Batch Downloader",
                "desc": "Download multiple individual YouTube videos",
                "color": ft.colors.RED,
                "gui_class": BatchDownloaderFletGUI,
                "icon": ft.icons.DOWNLOAD
            },
            "youtube_playlist": {
                "name": "🎵 YouTube Playlist Downloader",
                "desc": "Download complete YouTube playlists",
                "color": ft.colors.ORANGE,
                "gui_class": PlaylistDownloaderFletGUI,
                "icon": ft.icons.PLAYLIST_PLAY
            },
            "socmed": {
                "name": "📥 SocMed Downloader",
                "desc": "Download from TikTok, Instagram, Facebook, Twitter/X",
                "color": ft.colors.GREEN,
                "gui_class": SocMedDownloaderGUI,
                "icon": ft.icons.DOWNLOAD_FOR_OFFLINE
            },
            "media_looper": {
                "name": "🔁 Media Looper",
                "desc": "Loop video/audio without re-encoding",
                "color": ft.colors.TEAL,
                "gui_class": MediaLooperGUI,
                "icon": ft.icons.REPEAT
            }
        }
        
        self.setup_ui()
    
    def create_tool_card(self, tool_id, tool_info):
        """Create a card for each tool"""
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(tool_info["icon"], size=40, color=tool_info["color"]),
                    ft.Column([
                        ft.Text(tool_info["name"], size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(tool_info["desc"], size=12, color=ft.colors.GREY_700),
                    ], expand=True, spacing=5),
                ], spacing=15),
                ft.ElevatedButton(
                    "Launch Tool",
                    icon=ft.icons.ROCKET_LAUNCH,
                    on_click=lambda e, tid=tool_id: self.launch_tool(tid),
                    style=ft.ButtonStyle(
                        bgcolor=tool_info["color"],
                        color=ft.colors.WHITE,
                    ),
                    disabled=tool_info["gui_class"] is None
                )
            ], spacing=15),
            padding=20,
            border=ft.border.all(2, tool_info["color"]),
            border_radius=10,
            bgcolor=ft.colors.with_opacity(0.05, tool_info["color"]),
        )
    
    def launch_tool(self, tool_id):
        """Launch the selected tool"""
        tool_info = self.tools.get(tool_id)
        if not tool_info or not tool_info["gui_class"]:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Tool not available"), bgcolor=ft.colors.RED)
            )
            return
        
        # Clear page and launch tool
        self.page.controls.clear()
        
        # Add back button
        back_btn = ft.ElevatedButton(
            "← Back to Home",
            icon=ft.icons.HOME,
            on_click=lambda e: self.setup_ui()
        )
        
        try:
            # Create tool instance
            tool_instance = tool_info["gui_class"](self.page)
            
            # Add controls
            self.page.add(
                ft.Container(padding=10, content=back_btn),
                ft.Divider(),
            )
            
            self.page.update()
            
        except Exception as e:
            self.page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Error launching tool: {str(e)}"),
                    bgcolor=ft.colors.RED
                )
            )
            self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI"""
        self.page.controls.clear()
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.VIDEO_LIBRARY, size=60, color=ft.colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text(
                            "Media Tools Zakkutsu",
                            size=36,
                            weight=ft.FontWeight.BOLD,
                            color=ft.colors.DEEP_PURPLE
                        ),
                        ft.Text(
                            "All-in-One Media Processing Suite",
                            size=16,
                            color=ft.colors.GREY_600
                        ),
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Text(
                    "Select a tool to get started",
                    size=14,
                    color=ft.colors.GREY_700,
                    text_align=ft.TextAlign.CENTER
                ),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
            padding=30,
            bgcolor=ft.colors.DEEP_PURPLE_50,
            border_radius=15,
        )
        
        # Tool cards in grid
        tools_grid = ft.GridView(
            expand=True,
            runs_count=2,
            max_extent=400,
            child_aspect_ratio=1.5,
            spacing=15,
            run_spacing=15,
        )
        
        for tool_id, tool_info in self.tools.items():
            tools_grid.controls.append(self.create_tool_card(tool_id, tool_info))
        
        # Footer
        footer = ft.Container(
            content=ft.Row([
                ft.Icon(ft.icons.INFO_OUTLINE, size=16, color=ft.colors.GREY_600),
                ft.Text(
                    "v1.0.0 | FFmpeg required | github.com/zakkutsu/media-tools-py",
                    size=12,
                    color=ft.colors.GREY_600
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
            padding=10,
        )
        
        # Add all components
        self.page.add(
            header,
            ft.Container(height=20),
            tools_grid,
            footer,
        )
        
        self.page.update()


def main(page: ft.Page):
    """Main entry point"""
    MediaToolsZakkutsu(page)


if __name__ == "__main__":
    ft.app(target=main)
