#!/usr/bin/env python3
"""
Media Tools Zakkutsu Launcher
Simple launcher untuk semua tools

Author: Zakkutsu
Version: 1.0
"""

import flet as ft
import os
import sys
from pathlib import Path
import subprocess
import importlib.util

# Current directory
current_dir = Path(__file__).parent

# Check dependencies
def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_ytdlp():
    """Check if yt-dlp is installed"""
    try:
        import yt_dlp
        return True
    except ImportError:
        return False


class MediaToolsLauncher:
    """Launcher for Zakkutsu Media Tools"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬 Media Tools Zakkutsu"
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
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
                    ft.Icon(ft.Icons.APPS, size=50, color=ft.Colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text("Media Tools Zakkutsu", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Collection by Zakkutsu", size=16, color=ft.Colors.GREY_600),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.CENTER),
            ]),
            padding=30,
            bgcolor=ft.Colors.DEEP_PURPLE_50,
            border_radius=15,
            margin=ft.margin.only(bottom=20)
        )
        
        # System status
        status = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if ffmpeg_ok else ft.Icons.ERROR,
                    color=ft.Colors.GREEN if ffmpeg_ok else ft.Colors.RED,
                    size=20
                ),
                ft.Text(
                    "FFmpeg: " + ("OK" if ffmpeg_ok else "Not Found"),
                    color=ft.Colors.GREEN if ffmpeg_ok else ft.Colors.RED
                ),
                ft.Container(width=20),
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if ytdlp_ok else ft.Icons.ERROR,
                    color=ft.Colors.GREEN if ytdlp_ok else ft.Colors.RED,
                    size=20
                ),
                ft.Text(
                    "yt-dlp: " + ("OK" if ytdlp_ok else "Not Found"),
                    color=ft.Colors.GREEN if ytdlp_ok else ft.Colors.RED
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=10,
            bgcolor=ft.Colors.BLUE_50,
            border_radius=8,
            margin=ft.margin.only(bottom=20)
        )
        
        # Tool cards
        cards = ft.Column([
            ft.Text("Select a Tool", size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
            ft.Container(height=10),
            ft.Row([
                self.create_card(
                    "🎵 YT Playlist Downloader",
                    "Download YouTube playlists",
                    ft.Colors.RED,
                    lambda e: self.launch_tool("yt-playlist-downloader", "playlist_downloader_gui_flet.py")
                ),
                self.create_card(
                    "🔁 Media Looper",
                    "Loop media files instantly",
                    ft.Colors.TEAL,
                    lambda e: self.launch_tool("media-looper", "media_looper_gui_flet.py")
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),
            ft.Row([
                self.create_card(
                    "🎵 Audio Merger",
                    "Merge audio with effects",
                    ft.Colors.BLUE,
                    lambda e: self.launch_tool("audio-merger", "audio_merger_gui.py")
                ),
                self.create_card(
                    "🌐 SocMed Downloader",
                    "Download from social media",
                    ft.Colors.GREEN,
                    lambda e: self.launch_tool("socmed-downloader", "socmed_downloader_gui.py")
                ),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Info
        info = ft.Container(
            content=ft.Column([
                ft.Divider(height=1),
                ft.Row([
                    ft.TextButton("📖 Help", on_click=self.show_help),
                    ft.TextButton("⚙️ Install Dependencies", on_click=self.install_deps),
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
    
    def create_card(self, title, description, color, on_click):
        """Create tool card"""
        return ft.Container(
            content=ft.Column([
                ft.Text(title, size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Container(height=5),
                ft.Text(description, size=12, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
                ft.Container(height=15),
                ft.ElevatedButton(
                    "Launch",
                    icon=ft.Icons.ROCKET_LAUNCH,
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    on_click=on_click,
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=350,
            height=180,
            border=ft.border.all(2, color),
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.WHITE,
        )
    
    def launch_tool(self, folder, script):
        """Launch a tool"""
        tool_path = current_dir / folder / script
        
        if not tool_path.exists():
            self.show_error(f"Tool not found: {folder}/{script}")
            return
        
        try:
            # Run in separate process
            subprocess.Popen(
                [sys.executable, str(tool_path)],
                cwd=str(tool_path.parent),
                creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0
            )
            self.show_snackbar(f"✅ Launched {folder}", ft.Colors.GREEN)
        except Exception as e:
            self.show_error(f"Failed to launch: {e}")
    
    def install_deps(self, e):
        """Install dependencies"""
        self.show_snackbar("📦 Installing dependencies...", ft.Colors.BLUE)
        
        def install():
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-r', str(current_dir / 'requirements.txt')],
                    check=True,
                    timeout=300
                )
                self.page.run_thread_safe(lambda: self.show_snackbar("✅ Installed successfully!", ft.Colors.GREEN))
            except Exception as ex:
                self.page.run_thread_safe(lambda: self.show_snackbar(f"❌ Installation failed: {ex}", ft.Colors.RED))
        
        import threading
        threading.Thread(target=install, daemon=True).start()
    
    def show_help(self, e):
        """Show help dialog"""
        content = ft.Container(
            content=ft.Column([
                ft.Text("📖 Help", size=20, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("Quick Start:", weight=ft.FontWeight.BOLD),
                ft.Text("1. Install FFmpeg (required):\n   Windows: winget install FFmpeg", size=12),
                ft.Text("2. Install dependencies:\n   pip install -r requirements.txt", size=12),
                ft.Text("3. Click Launch on any tool", size=12),
                ft.Container(height=10),
                ft.Text("Tools:", weight=ft.FontWeight.BOLD),
                ft.Text("• YT Playlist: Download YouTube playlists\n• Media Looper: Loop videos/audio\n• Audio Merger: Merge with effects\n• SocMed: TikTok, IG, FB, Twitter/X", size=12),
            ], scroll=ft.ScrollMode.AUTO),
            width=500,
            height=400,
            padding=10
        )
        
        dialog = ft.AlertDialog(
            title=ft.Text("Help"),
            content=content,
            actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(dialog))],
        )
        
        self.page.open(dialog)
    
    def show_error(self, message):
        """Show error"""
        dialog = ft.AlertDialog(
            title=ft.Row([ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED), ft.Text("Error")]),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=lambda e: self.page.close(dialog))],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_snackbar(self, message, color):
        """Show snackbar"""
        self.page.snack_bar = ft.SnackBar(ft.Text(message), bgcolor=color)
        self.page.snack_bar.open = True
        self.page.update()


def main(page: ft.Page):
    """Main entry point"""
    MediaToolsLauncher(page)


if __name__ == "__main__":
    if "--help" in sys.argv:
        print("🎬 Media Tools Zakkutsu Launcher")
        print("Usage: python media_tools_launcher.py")
        print("\nLaunches GUI to select and run tools")
    else:
        ft.app(target=main, view=ft.AppView.FLET_APP)
