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
Version: 1.0 All-in-One
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
        self.yt_dlp_cmd = self._get_yt_dlp_command()
    
    def _check_yt_dlp(self) -> bool:
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True
        except:
            pass
        
        try:
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _get_yt_dlp_command(self) -> List[str]:
        try:
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return ['yt-dlp']
        except:
            pass
        return [sys.executable, '-m', 'yt_dlp']
    
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
            cmd = self.yt_dlp_cmd + ['--dump-json', '--flat-playlist', playlist_url]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                entries = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            entries.append(json.loads(line))
                        except:
                            continue
                return {'total_videos': len(entries), 'entries': entries}
            return None
        except:
            return None
    
    def download_video_playlist(self, playlist_url: str, quality: str = "best", 
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        if not self.yt_dlp_available or not self.download_folder:
            return False
        
        try:
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
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
            
            cmd = self.yt_dlp_cmd + ['-f', format_selector, '-o', output_template, 
                                    '--embed-thumbnail', '--add-metadata', playlist_url]
            cmd = [arg for arg in cmd if arg]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            current_item = 0
            total_items = 0
            
            for line in process.stdout:
                line_stripped = line.strip()
                
                if "Downloading" in line and "items of" in line:
                    try:
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "items" and i > 0:
                                total_items = int(parts[i-1])
                                break
                    except:
                        pass
                
                elif "Downloading item" in line and "of" in line:
                    try:
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "item" and i < len(parts) - 2:
                                current_item = int(parts[i+1])
                                break
                    except:
                        pass
                
                if current_item > 0 and total_items > 0 and progress_callback:
                    percentage = (current_item / total_items) * 100
                    if "Downloading item" in line:
                        progress_callback(current_item, total_items, percentage, "")
            
            process.wait()
            return process.returncode == 0
        except:
            return False
        finally:
            try:
                os.chdir(original_cwd)
            except:
                pass
    
    def download_audio_playlist(self, playlist_url: str, audio_format: str = "mp3",
                              audio_quality: str = "0",
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        if not self.yt_dlp_available or not self.download_folder:
            return False
        
        try:
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
            if not auto_numbering:
                output_template = output_template.replace("%(playlist_index)s - ", "").replace("%(playlist_index)s", "")
                output_template = " ".join(output_template.split())
                if "%(title)s" not in output_template:
                    output_template = "%(title)s.%(ext)s"
            
            cmd = self.yt_dlp_cmd + ['-x', '--audio-format', audio_format, '--audio-quality', audio_quality,
                                    '-o', output_template, '--embed-thumbnail', '--add-metadata', playlist_url]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            current_item = 0
            total_items = 0
            
            for line in process.stdout:
                line_stripped = line.strip()
                
                if "Downloading" in line and "items of" in line:
                    try:
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "items" and i > 0:
                                total_items = int(parts[i-1])
                                break
                    except:
                        pass
                
                elif "Downloading item" in line and "of" in line:
                    try:
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "item" and i < len(parts) - 2:
                                current_item = int(parts[i+1])
                                break
                    except:
                        pass
                
                if current_item > 0 and total_items > 0 and progress_callback:
                    percentage = (current_item / total_items) * 100
                    if "Downloading item" in line:
                        progress_callback(current_item, total_items, percentage, "")
            
            process.wait()
            return process.returncode == 0
        except:
            return False
        finally:
            try:
                os.chdir(original_cwd)
            except:
                pass


# ============================================================================
# PLAYLIST DOWNLOADER GUI
# ============================================================================

class PlaylistDownloaderGUI:
    """GUI for YouTube Playlist Downloader"""
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎵 YouTube Playlist Downloader"
        self.downloader = PlaylistDownloader()
        self.download_folder = os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Downloads")
        self.setup_simple_ui()
    
    def setup_simple_ui(self):
        """Setup simplified UI"""
        self.page.controls.clear()
        
        # Title
        title = ft.Text("🎵 YouTube Playlist Downloader", size=24, weight=ft.FontWeight.BOLD)
        
        # URL Input
        self.url_field = ft.TextField(label="🔗 Playlist URL", expand=True)
        
        # Download Type
        self.type_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="video_best", label="🎬 Video (Best Quality)"),
                ft.Radio(value="audio_mp3", label="🎵 Audio Only (MP3)"),
            ]),
            value="video_best"
        )
        
        # Progress
        self.progress_label = ft.Text("Ready", size=12)
        self.progress_bar = ft.ProgressBar(value=0, expand=True)
        
        # Download Button
        download_btn = ft.ElevatedButton(
            "🚀 Start Download",
            on_click=self.start_download,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
            width=200
        )
        
        # Layout
        content = ft.Column([
            title,
            ft.Container(height=20),
            self.url_field,
            ft.Container(height=10),
            ft.Text("Download Type:", weight=ft.FontWeight.BOLD),
            self.type_radio,
            ft.Container(height=20),
            download_btn,
            ft.Container(height=20),
            self.progress_label,
            self.progress_bar,
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
        
        self.page.add(content)
        self.page.update()
    
    def start_download(self, e):
        """Start download"""
        url = self.url_field.value.strip() if self.url_field.value else ""
        if not url:
            self.progress_label.value = "❌ Please enter URL!"
            self.page.update()
            return
        
        def download_thread():
            self.progress_label.value = "🔄 Downloading..."
            self.page.update()
            
            self.downloader.set_download_folder(self.download_folder)
            
            download_type = self.type_radio.value
            
            if download_type == "audio_mp3":
                success = self.downloader.download_audio_playlist(url, progress_callback=self.update_progress)
            else:
                success = self.downloader.download_video_playlist(url, progress_callback=self.update_progress)
            
            if success:
                self.progress_label.value = f"✅ Download complete! Saved to: {self.download_folder}"
            else:
                self.progress_label.value = "❌ Download failed!"
            
            self.page.update()
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def update_progress(self, current, total, percentage, title):
        """Update progress"""
        self.progress_label.value = f"📥 [{current}/{total}] ({percentage:.1f}%)"
        self.progress_bar.value = percentage / 100.0
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
            bgcolor=ft.Colors.TEAL,
            color=ft.Colors.WHITE
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
            
            loop_count = count - 1
            cmd = ['ffmpeg', '-stream_loop', str(loop_count), '-i', file_path,
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
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE
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
        subtitle = ft.Text("YouTube, TikTok, Instagram, Facebook, Twitter/X", size=14, color=ft.Colors.GREY_600)
        
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
            bgcolor=ft.Colors.GREEN,
            color=ft.Colors.WHITE,
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
                    ft.Icon(ft.Icons.APPS, size=50, color=ft.Colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text("Media Tools Zakkutsu", size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("All-in-One Standalone Edition", size=16, color=ft.Colors.GREY_600),
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
            ft.Text("Select a Tool", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(height=10),
            ft.Row([
                self.create_card("🎵 YT Playlist\nDownloader", ft.Colors.RED, lambda e: self.launch_tool("playlist")),
                self.create_card("🔁 Media\nLooper", ft.Colors.TEAL, lambda e: self.launch_tool("looper")),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ft.Container(height=20),
            ft.Row([
                self.create_card("🎵 Audio\nMerger", ft.Colors.BLUE, lambda e: self.launch_tool("merger")),
                self.create_card("🌐 SocMed\nDownloader", ft.Colors.GREEN, lambda e: self.launch_tool("socmed")),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        # Info
        info = ft.Container(
            content=ft.Column([
                ft.Divider(height=1),
                ft.Text("💡 FFmpeg required for optimal functionality", size=12, color=ft.Colors.GREY_600),
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
                    icon=ft.Icons.ROCKET_LAUNCH,
                    bgcolor=color,
                    color=ft.Colors.WHITE,
                    on_click=on_click,
                )
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            width=350,
            height=150,
            border=ft.border.all(2, color),
            border_radius=10,
            padding=20,
            bgcolor=ft.Colors.WHITE,
        )
    
    def launch_tool(self, tool_name):
        """Launch selected tool"""
        self.page.controls.clear()
        
        # Back button
        back_btn = ft.ElevatedButton(
            "🏠 Back to Home",
            on_click=lambda e: self.setup_home(),
            bgcolor=ft.Colors.GREY_600,
            color=ft.Colors.WHITE
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
        print("✅ FFmpeg: OK")
    else:
        print("❌ FFmpeg: Not Found")
        print("   Install: winget install FFmpeg")
    
    # Check yt-dlp
    if check_ytdlp():
        print("✅ yt-dlp: OK")
    else:
        print("⚠️  yt-dlp: Not Found (will auto-install)")
    
    print()
    print("🚀 Launching GUI...")
    print("="*70)
    print()
    
    # Launch Flet app
    ft.app(target=main, view=ft.AppView.FLET_APP)
