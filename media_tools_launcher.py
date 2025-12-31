import flet as ft
import os
import sys
from pathlib import Path
import importlib.util
import subprocess

# Detect if running as PyInstaller executable
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    current_dir = Path(sys._MEIPASS)
else:
    # Running as script
    current_dir = Path(__file__).parent

# ============================================
# FFmpeg Portable Configuration
# ============================================
def setup_ffmpeg_portable():
    """Setup FFmpeg portable path for pydub and other tools"""
    ffmpeg_portable_path = current_dir / "ffmpeg-portable" / "bin"
    
    # Check if FFmpeg portable exists
    if ffmpeg_portable_path.exists():
        ffmpeg_exe = ffmpeg_portable_path / "ffmpeg.exe"
        ffprobe_exe = ffmpeg_portable_path / "ffprobe.exe"
        
        if ffmpeg_exe.exists():
            # Add to PATH environment variable (first priority)
            os.environ["PATH"] = str(ffmpeg_portable_path) + os.pathsep + os.environ.get("PATH", "")
            
            # Configure pydub specifically
            try:
                from pydub import AudioSegment
                AudioSegment.converter = str(ffmpeg_exe)
                if ffprobe_exe.exists():
                    AudioSegment.ffprobe = str(ffprobe_exe)
                print(f"✅ FFmpeg portable configured: {ffmpeg_portable_path}")
                return True
            except ImportError:
                # pydub not yet installed, will be configured after installation
                print("⚠️  pydub not yet installed, FFmpeg will be configured after dependency installation")
                return False
    else:
        print("⚠️  FFmpeg portable not found. Checking system FFmpeg...")
        # Check if system FFmpeg is available
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ System FFmpeg detected")
                return True
        except (FileNotFoundError, subprocess.TimeoutExpired):
            print("❌ FFmpeg not found! Please run launch_media_tools.bat for auto-setup")
            return False
    
    return False

# Setup FFmpeg portable on startup
setup_ffmpeg_portable()

# Add paths for imports
audio_merger_path = str(current_dir / "audio-merger")
media_detector_path = str(current_dir / "media-codec-detector")
batch_downloader_path = str(current_dir / "yt-batch-downloader")
playlist_downloader_path = str(current_dir / "yt-playlist-downloader")
socmed_downloader_path = str(current_dir / "socmed-downloader")
media_looper_path = str(current_dir / "media-looper")
universal_converter_path = str(current_dir / "universal-converter")
spotify_downloader_path = str(current_dir / "spotify-downloader")

# Add all tool paths to sys.path
tool_paths = [audio_merger_path, media_detector_path, batch_downloader_path, playlist_downloader_path, socmed_downloader_path, media_looper_path, universal_converter_path, spotify_downloader_path]
for path in tool_paths:
    if path not in sys.path:
        sys.path.insert(0, path)

# Helper function to check and install missing dependencies
def check_and_install_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    required_packages = {
        'pydub': 'pydub==0.25.1',
        'flet': 'flet>=0.25.0', 
        'ffmpeg': 'ffmpeg-python==0.2.0',
        'PIL': 'Pillow>=10.0.0',
        'filetype': 'filetype==1.2.0',
        'yt_dlp': 'yt-dlp',
        'pdf2image': 'pdf2image>=1.16.3',
        'spotdl': 'spotdl>=4.0.0'
    }
    
    for package, install_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_deps.append(install_name)
    
    return missing_deps

def install_missing_dependencies(missing_deps):
    """Install missing dependencies"""
    if not missing_deps:
        return True
    
    try:
        print(f"Installing missing dependencies: {', '.join(missing_deps)}")
        subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_deps, 
                      check=True, timeout=300)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f"Failed to install dependencies: {e}")
        return False

# Import GUI classes with more robust error handling and auto-installation
AudioMergerGUI = None
MediaCodecDetectorGUI = None
BatchDownloaderGUI = None
PlaylistDownloaderGUI = None
SocMedDownloaderGUI = None
MediaLooperGUI = None

# Check dependencies first
missing_deps = check_and_install_dependencies()
if missing_deps:
    print(f"⚠️  Missing dependencies detected: {', '.join(missing_deps)}")
    print("🔄 Attempting auto-installation...")
    if install_missing_dependencies(missing_deps):
        print("✅ Dependencies installed successfully!")
        # Re-configure FFmpeg after pydub installation
        setup_ffmpeg_portable()
    else:
        print("❌ Failed to install dependencies. Please run setup_media_tools.py")

try:
    # Try to import AudioMergerGUI
    audio_spec = importlib.util.spec_from_file_location(
        "audio_merger_gui", 
        current_dir / "audio-merger" / "audio_merger_gui.py"
    )
    if audio_spec and audio_spec.loader:
        audio_module = importlib.util.module_from_spec(audio_spec)
        audio_spec.loader.exec_module(audio_module)
        AudioMergerGUI = audio_module.AudioMergerGUI
except Exception as e:
    print(f"Failed to import AudioMergerGUI: {e}")
    AudioMergerGUI = None

try:
    # Try to import MediaCodecDetectorGUI
    detector_spec = importlib.util.spec_from_file_location(
        "media_codec_detector_gui", 
        current_dir / "media-codec-detector" / "media_codec_detector_gui.py"
    )
    if detector_spec and detector_spec.loader:
        detector_module = importlib.util.module_from_spec(detector_spec)
        detector_spec.loader.exec_module(detector_module)
        MediaCodecDetectorGUI = detector_module.MediaCodecDetectorGUI
except Exception as e:
    print(f"Failed to import MediaCodecDetectorGUI: {e}")
    MediaCodecDetectorGUI = None

# Import Flet-based YouTube Tools (New unified approach)
BatchDownloaderFletGUI = None
PlaylistDownloaderFletGUI = None

try:
    # Try to import BatchDownloaderGUI (Flet-based)
    batch_flet_spec = importlib.util.spec_from_file_location(
        "batch_downloader_gui_flet", 
        current_dir / "yt-batch-downloader" / "batch_downloader_gui_flet.py"
    )
    if batch_flet_spec and batch_flet_spec.loader:
        batch_flet_module = importlib.util.module_from_spec(batch_flet_spec)
        batch_flet_spec.loader.exec_module(batch_flet_module)
        BatchDownloaderFletGUI = batch_flet_module.BatchDownloaderGUI
except Exception as e:
    print(f"Failed to import BatchDownloaderFletGUI: {e}")
    BatchDownloaderFletGUI = None

try:
    # Try to import PlaylistDownloaderGUI (Flet-based)
    playlist_flet_spec = importlib.util.spec_from_file_location(
        "playlist_downloader_gui_flet", 
        current_dir / "yt-playlist-downloader" / "playlist_downloader_gui_flet.py"
    )
    if playlist_flet_spec and playlist_flet_spec.loader:
        playlist_flet_module = importlib.util.module_from_spec(playlist_flet_spec)
        playlist_flet_spec.loader.exec_module(playlist_flet_module)
        PlaylistDownloaderFletGUI = playlist_flet_module.PlaylistDownloaderGUI
except Exception as e:
    print(f"Failed to import PlaylistDownloaderFletGUI: {e}")
    PlaylistDownloaderFletGUI = None

# For backward compatibility, keep original Tkinter imports as fallback
BatchDownloaderGUI = None
PlaylistDownloaderGUI = None

try:
    # Try to import BatchDownloaderGUI (Tkinter-based - fallback)
    batch_spec = importlib.util.spec_from_file_location(
        "batch_downloader_gui", 
        current_dir / "yt-batch-downloader" / "batch_downloader_gui.py"
    )
    if batch_spec and batch_spec.loader:
        batch_module = importlib.util.module_from_spec(batch_spec)
        batch_spec.loader.exec_module(batch_module)
        BatchDownloaderGUI = batch_module.BatchDownloaderGUI
except Exception as e:
    print(f"Failed to import BatchDownloaderGUI (Tkinter fallback): {e}")
    BatchDownloaderGUI = None

try:
    # Try to import PlaylistDownloaderGUI (Tkinter-based - fallback)
    playlist_spec = importlib.util.spec_from_file_location(
        "playlist_downloader_gui", 
        current_dir / "yt-playlist-downloader" / "playlist_downloader_gui.py"
    )
    if playlist_spec and playlist_spec.loader:
        playlist_module = importlib.util.module_from_spec(playlist_spec)
        playlist_spec.loader.exec_module(playlist_module)
        PlaylistDownloaderGUI = playlist_module.PlaylistDownloaderGUI
except Exception as e:
    print(f"Failed to import PlaylistDownloaderGUI (Tkinter fallback): {e}")
    PlaylistDownloaderGUI = None

# Import SocMed Downloader (Flet-based)
try:
    socmed_spec = importlib.util.spec_from_file_location(
        "socmed_downloader_gui",
        current_dir / "socmed-downloader" / "socmed_downloader_gui.py"
    )
    if socmed_spec and socmed_spec.loader:
        socmed_module = importlib.util.module_from_spec(socmed_spec)
        socmed_spec.loader.exec_module(socmed_module)
        SocMedDownloaderGUI = socmed_module.SocMedDownloaderGUI
except Exception as e:
    print(f"Failed to import SocMedDownloaderGUI: {e}")
    SocMedDownloaderGUI = None

# Import Media Looper (Flet-based)
try:
    media_looper_spec = importlib.util.spec_from_file_location(
        "media_looper_gui_flet",
        current_dir / "media-looper" / "media_looper_gui_flet.py"
    )
    if media_looper_spec and media_looper_spec.loader:
        media_looper_module = importlib.util.module_from_spec(media_looper_spec)
        media_looper_spec.loader.exec_module(media_looper_module)
        MediaLooperGUI = media_looper_module.MediaLooperGUI
except Exception as e:
    print(f"Failed to import MediaLooperGUI: {e}")
    MediaLooperGUI = None

# Import Universal Converter (Flet-based)
try:
    universal_converter_spec = importlib.util.spec_from_file_location(
        "universal_converter_gui",
        current_dir / "universal-converter" / "universal_converter_gui.py"
    )
    if universal_converter_spec and universal_converter_spec.loader:
        universal_converter_module = importlib.util.module_from_spec(universal_converter_spec)
        universal_converter_spec.loader.exec_module(universal_converter_module)
        UniversalConverterGUI = universal_converter_module.main
except Exception as e:
    print(f"Failed to import UniversalConverterGUI: {e}")
    UniversalConverterGUI = None

# Import Spotify Downloader (Flet-based)
try:
    spotify_downloader_spec = importlib.util.spec_from_file_location(
        "spotify_downloader_gui_flet",
        current_dir / "spotify-downloader" / "spotify_downloader_gui_flet.py"
    )
    if spotify_downloader_spec and spotify_downloader_spec.loader:
        spotify_downloader_module = importlib.util.module_from_spec(spotify_downloader_spec)
        spotify_downloader_spec.loader.exec_module(spotify_downloader_module)
        SpotifyDownloaderGUI = spotify_downloader_module.main
except Exception as e:
    print(f"Failed to import SpotifyDownloaderGUI: {e}")
    SpotifyDownloaderGUI = None

class MediaToolsLauncher:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬🎵 Media Tools Launcher"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_min_width = 600
        self.page.window_min_height = 500
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # State management
        self.current_app = None
        self.home_view = None
        self.app_view = None
        
        # Initialize UI
        self.setup_home_ui()
    
    def setup_home_ui(self):
        """Setup the main home interface"""
        
        # Clear page
        self.page.controls.clear()
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUILD_CIRCLE, size=50, color=ft.Colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text("Media Tools", 
                               size=32, weight=ft.FontWeight.BOLD),
                        ft.Text("Suite", 
                               size=24, weight=ft.FontWeight.W_300, color=ft.Colors.GREY_600),
                    ], spacing=0),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Text("Select the tool you want to use", 
                       size=16, color=ft.Colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=30,
            bgcolor=ft.Colors.DEEP_PURPLE_50,
            border_radius=15,
            margin=ft.margin.only(bottom=30)
        )
        
        # Tool cards
        audio_merger_card = self.create_tool_card(
            title="🎵 Audio Merger",
            description="Merge multiple audio files into one with transition effects like crossfade and gap",
            features=[
                "✨ Crossfade & Gap effects",
                "🎚️ Multi-format support",
                "📊 Real-time progress",
                "🎨 Modern GUI interface"
            ],
            color=ft.Colors.BLUE,
            on_click=self.launch_audio_merger
        )
        
        media_detector_card = self.create_tool_card(
            title="🎬 Media Codec Detector", 
            description="Detect container format and codecs from media files (images, videos, audio)",
            features=[
                "🕵️ Comprehensive codec detection", 
                "📱 Image format analysis",
                "🎥 Video & audio streams",
                "🧪 Dummy file generator"
            ],
            color=ft.Colors.PURPLE,
            on_click=self.launch_media_detector
        )
        
        batch_downloader_card = self.create_tool_card(
            title="📥 Batch Downloader",
            description="Download multiple individual YouTube videos with modern Flet interface",
            features=[
                "� Modern Flet GUI interface",
                "📝 URL management & batch loading",
                "� Quality selection options",
                "📊 Real-time progress tracking"
            ],
            color=ft.Colors.RED,
            on_click=self.launch_batch_downloader
        )
        
        playlist_downloader_card = self.create_tool_card(
            title="🎵 Playlist Downloader",
            description="Download complete YouTube playlists with elegant interface",
            features=[
                "📱 Modern Flet GUI interface",
                "🎵 Full playlist downloading",
                "🎯 Flexible naming templates",
                "📊 Progress tracking per video"
            ],
            color=ft.Colors.ORANGE,
            on_click=self.launch_playlist_downloader
        )
        
        socmed_downloader_card = self.create_tool_card(
            title="🌐 SocMed Downloader",
            description="Download video/audio from YouTube, TikTok, Instagram, Facebook, Twitter/X",
            features=[
                "🌐 Multi-platform (YT, TikTok, IG, FB, X)",
                "🎬 Video & Audio (MP3) support",
                "📦 Batch download (TXT/CSV/JSON)",
                "🎯 Quality selector (480p-1080p)"
            ],
            color=ft.Colors.GREEN,
            on_click=self.launch_socmed_downloader
        )
        
        media_looper_card = self.create_tool_card(
            title="🔁 Media Looper",
            description="Loop video/audio N times without re-encoding using FFmpeg stream copy",
            features=[
                "⚡ Super cepat (stream copy, no re-encode)",
                "🎵 Audio & Video support",
                "📊 Duration calculator",
                "🎯 Zero quality loss"
            ],
            color=ft.Colors.TEAL,
            on_click=self.launch_media_looper
        )
        
        universal_converter_card = self.create_tool_card(
            title="🔄 Universal Converter",
            description="Smart file converter for images, videos, audio, and PDF with format validation",
            features=[
                "🖼️ Images (JPG, PNG, WEBP, BMP, ICO)",
                "🎬 Video & Audio (MP4, MP3, GIF, etc)",
                "📄 PDF to Image (per page)",
                "🧠 Smart format detection"
            ],
            color=ft.Colors.DEEP_PURPLE,
            on_click=self.launch_universal_converter
        )
        
        spotify_downloader_card = self.create_tool_card(
            title="🎵 Spotify Downloader",
            description="Download music from Spotify without API key using YouTube Music match",
            features=[
                "🎵 Single track & playlist support",
                "🎧 High quality MP3 output",
                "📝 Auto metadata & lyrics",
                "🚫 No API key required"
            ],
            color=ft.Colors.LIGHT_GREEN_700,
            on_click=self.launch_spotify_downloader
        )
        
        # Tool selection section
        tools_section = ft.Container(
            content=ft.Column([
                ft.Text("Select Tool", 
                       size=20, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    audio_merger_card,
                    media_detector_card,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
                ft.Container(height=10),  # Spacing
                ft.Row([
                    batch_downloader_card,
                    playlist_downloader_card,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
                ft.Container(height=10),  # Spacing
                ft.Row([
                    socmed_downloader_card,
                    media_looper_card,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
                ft.Container(height=10),  # Spacing
                ft.Row([
                    universal_converter_card,
                    spotify_downloader_card,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20, wrap=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            margin=ft.margin.only(bottom=30)
        )
        
        # Additional info section
        info_section = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.GREY_600),
                    ft.Text("These tools require FFmpeg to function optimally", 
                           size=14, color=ft.Colors.GREY_600),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.TextButton("📖 Documentation", 
                                 on_click=self.show_docs),
                    ft.TextButton("⚙️ System Requirements", 
                                 on_click=self.show_requirements),
                    ft.TextButton("❌ Exit", 
                                 on_click=self.exit_app),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=15),
            padding=20,
            margin=ft.margin.only(top=20)
        )
        
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
        
        # Main layout with footer inside scrollable content
        main_content = ft.Column([
            header,
            tools_section,
            info_section,
            footer  # Footer inside scrollable content
        ], scroll=ft.ScrollMode.AUTO, expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        
        self.home_view = main_content
        self.page.add(main_content)
        self.page.update()
    
    def create_tool_card(self, title, description, features, color, on_click):
        """Create a tool selection card"""
        
        feature_items = []
        for feature in features:
            feature_items.append(
                ft.Row([
                    ft.Container(width=10),  # Indent
                    ft.Text(feature, size=12, color=ft.Colors.GREY_700)
                ])
            )
        
        card = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.PLAY_CIRCLE_FILL, color=color, size=30),
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, expand=True),
                    ]),
                    padding=15,
                    bgcolor=ft.Colors.with_opacity(0.1, color),
                    border_radius=ft.border_radius.only(top_left=10, top_right=10)
                ),
                
                # Content
                ft.Container(
                    content=ft.Column([
                        ft.Text(description, size=14, color=ft.Colors.GREY_800),
                        ft.Container(height=10),  # Spacing
                        ft.Text("Features:", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                        ft.Column(feature_items, spacing=5),
                        ft.Container(height=15),  # Spacing
                        ft.ElevatedButton(
                            "Launch Tool",
                            icon=ft.Icons.ROCKET_LAUNCH,
                            bgcolor=color,
                            color=ft.Colors.WHITE,
                            on_click=on_click,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8),
                            )
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=8),
                    padding=15
                )
            ]),
            width=350,
            border=ft.border.all(2, ft.Colors.with_opacity(0.3, color)),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
        
        return card
    
    def launch_audio_merger(self, e):
        """Launch Audio Merger tool"""
        if AudioMergerGUI is None:
            error_msg = "Audio Merger is not available.\n\nMake sure audio_merger_gui.py exists in the audio-merger/ folder\n\nAlso check that all dependencies are installed with:\npip install -r requirements.txt"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("audio_merger")
    
    def launch_media_detector(self, e):
        """Launch Media Codec Detector tool"""
        if MediaCodecDetectorGUI is None:
            error_msg = "Media Codec Detector is not available.\n\nMake sure media_codec_detector_gui.py exists in the media-codec-detector/ folder\n\nAlso check that all dependencies are installed with:\npip install -r requirements.txt"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("media_detector")
    
    def launch_batch_downloader(self, e):
        """Launch YouTube Batch Downloader tool (Flet version preferred)"""
        if BatchDownloaderFletGUI is not None:
            # Use modern Flet version
            self.switch_to_app("batch_downloader_flet")
        elif BatchDownloaderGUI is not None:
            # Fallback to Tkinter version
            self.switch_to_app("batch_downloader_tkinter")
        else:
            error_msg = "YouTube Batch Downloader is not available.\n\nMake sure batch_downloader_gui_flet.py or batch_downloader_gui.py exists in the yt-batch-downloader/ folder\n\nAlso check that yt-dlp is installed with:\npip install yt-dlp"
            self.show_error(error_msg)
            return
    
    def launch_playlist_downloader(self, e):
        """Launch YouTube Playlist Downloader tool (Flet version preferred)"""
        if PlaylistDownloaderFletGUI is not None:
            # Use modern Flet version
            self.switch_to_app("playlist_downloader_flet")
        elif PlaylistDownloaderGUI is not None:
            # Fallback to Tkinter version
            self.switch_to_app("playlist_downloader_tkinter")
        else:
            error_msg = "YouTube Playlist Downloader is not available.\n\nMake sure playlist_downloader_gui_flet.py or playlist_downloader_gui.py exists in the yt-playlist-downloader/ folder\n\nAlso check that yt-dlp is installed with:\npip install yt-dlp"
            self.show_error(error_msg)
            return
    
    def launch_socmed_downloader(self, e):
        """Launch SocMed Downloader tool"""
        if SocMedDownloaderGUI is None:
            error_msg = "SocMed Downloader is not available.\n\nMake sure socmed_downloader_gui.py exists in the socmed-downloader/ folder\n\nAlso check that yt-dlp is installed with:\npip install yt-dlp"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("socmed_downloader")
    
    def launch_media_looper(self, e):
        """Launch Media Looper tool"""
        if MediaLooperGUI is None:
            error_msg = "Media Looper is not available.\n\nMake sure media_looper_gui_flet.py exists in the media-looper/ folder\n\nAlso check that FFmpeg is installed and in the system PATH."
            self.show_error(error_msg)
            return
        
        self.switch_to_app("media_looper")
    
    def launch_universal_converter(self, e):
        """Launch Universal Converter tool"""
        if UniversalConverterGUI is None:
            error_msg = "Universal Converter is not available.\n\nMake sure universal_converter_gui.py exists in the universal-converter/ folder\n\nAlso check that Pillow and pdf2image are installed with:\npip install Pillow pdf2image"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("universal_converter")
    
    def launch_spotify_downloader(self, e):
        """Launch Spotify Downloader tool"""
        if SpotifyDownloaderGUI is None:
            error_msg = "Spotify Downloader is not available.\n\nMake sure spotify_downloader_gui_flet.py exists in the spotify-downloader/ folder\n\nAlso check that spotdl is installed with:\npip install spotdl"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("spotify_downloader")
    
    def switch_to_app(self, app_name):
        """Switch to specific application"""
        self.page.controls.clear()
        
        # Create back button
        back_button = ft.Container(
            content=ft.ElevatedButton(
                "🏠 Back to Home",
                icon=ft.Icons.HOME,
                on_click=self.back_to_home,
                bgcolor=ft.Colors.GREY_600,
                color=ft.Colors.WHITE
            ),
            alignment=ft.alignment.top_left,
            padding=10
        )
        
        # Create app container
        app_container = ft.Container(
            expand=True,
            padding=ft.padding.only(top=10)
        )
        
        self.page.add(
            ft.Column([
                back_button,
                app_container
            ], expand=True)
        )
        
        # Initialize the selected app
        if app_name == "audio_merger":
            self.current_app = AudioMergerGUI(self.create_app_page(app_container))
        elif app_name == "media_detector":
            self.current_app = MediaCodecDetectorGUI(self.create_app_page(app_container))
        elif app_name == "batch_downloader_flet":
            # Modern Flet-based Batch Downloader
            self.current_app = BatchDownloaderFletGUI(self.create_app_page(app_container))
        elif app_name == "playlist_downloader_flet":
            # Modern Flet-based Playlist Downloader
            self.current_app = PlaylistDownloaderFletGUI(self.create_app_page(app_container))
        elif app_name == "socmed_downloader":
            # SocMed Downloader (Flet-based)
            self.current_app = SocMedDownloaderGUI(self.create_app_page(app_container))
        elif app_name == "media_looper":
            # Media Looper (Flet-based)
            self.current_app = MediaLooperGUI(self.create_app_page(app_container))
        elif app_name == "universal_converter":
            # Universal Converter (Flet-based)
            UniversalConverterGUI(self.create_app_page(app_container))
        elif app_name == "spotify_downloader":
            # Spotify Downloader (Flet-based)
            SpotifyDownloaderGUI(self.create_app_page(app_container))
        elif app_name == "batch_downloader_tkinter":
            # Fallback Tkinter-based Batch Downloader
            self.launch_tkinter_app("batch_downloader")
            return
        elif app_name == "playlist_downloader_tkinter":
            # Fallback Tkinter-based Playlist Downloader
            self.launch_tkinter_app("playlist_downloader") 
            return
        
        self.page.update()
    
    def create_app_page(self, container):
        """Create a pseudo-page for the app"""
        class AppPage:
            def __init__(self, page, container):
                self.page = page
                self.container = container
                self.title = page.title
                self.window_width = page.window_width
                self.window_height = page.window_height
                self.window_min_width = page.window_min_width
                self.window_min_height = page.window_min_height
                self.window_resizable = getattr(page, 'window_resizable', True)
                self.theme_mode = page.theme_mode
                self.controls = []
                self.overlay = page.overlay
                self.snack_bar = None
                self.dialog = None
                self.scroll = getattr(page, 'scroll', None)
                # Additional properties for compatibility
                self.padding = 0  # Default padding
                self.window = page.window if hasattr(page, 'window') else None
            
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
                """Open dialog"""
                self.page.open(dialog)
                
            def close(self, dialog):
                """Close dialog"""
                self.page.close(dialog)
        
        return AppPage(self.page, container)
    
    def launch_tkinter_app(self, app_name):
        """Launch Tkinter-based apps in separate process"""
        import subprocess
        import threading
        
        # Show immediate feedback
        self.show_snackbar(f"🚀 Launching {app_name.replace('_', ' ').title()}...", ft.Colors.BLUE)
        
        def run_tkinter_app():
            try:
                if app_name == "batch_downloader":
                    script_path = current_dir / "yt-batch-downloader" / "batch_downloader_gui.py"
                elif app_name == "playlist_downloader":
                    script_path = current_dir / "yt-playlist-downloader" / "playlist_downloader_gui.py"
                else:
                    raise ValueError(f"Unknown app: {app_name}")
                
                if not script_path.exists():
                    raise FileNotFoundError(f"Script not found: {script_path}")
                
                # Change to the tool directory before running
                original_cwd = os.getcwd()
                tool_dir = script_path.parent
                os.chdir(str(tool_dir))
                
                # Use virtual environment python if available
                venv_python = current_dir / "venv" / "Scripts" / "python.exe"
                if venv_python.exists():
                    python_exe = str(venv_python)
                else:
                    python_exe = sys.executable
                
                print(f"Launching {app_name} with: {python_exe} {script_path.name}")
                
                # Launch without waiting for completion (non-blocking)
                process = subprocess.Popen([python_exe, str(script_path.name)], 
                                         stdout=subprocess.PIPE, 
                                         stderr=subprocess.PIPE,
                                         creationflags=subprocess.CREATE_NEW_CONSOLE if os.name == 'nt' else 0)
                
                os.chdir(original_cwd)
                
                # Show success message
                def show_success():
                    self.show_snackbar(f"✅ {app_name.replace('_', ' ').title()} launched successfully!", ft.Colors.GREEN)
                self.page.run_thread_safe(show_success)
                
            except FileNotFoundError as e:
                print(f"File not found for {app_name}: {e}")
                def show_error():
                    self.show_snackbar(f"❌ {app_name.replace('_', ' ').title()} file not found", ft.Colors.RED)
                self.page.run_thread_safe(show_error)
            except Exception as e:
                print(f"Unexpected error launching {app_name}: {e}")
                def show_error():
                    self.show_snackbar(f"❌ Error launching {app_name.replace('_', ' ').title()}: {str(e)}", ft.Colors.RED)
                self.page.run_thread_safe(show_error)
        
        # Run in separate thread to avoid blocking main UI
        threading.Thread(target=run_tkinter_app, daemon=True).start()
    
    def back_to_home(self, e):
        """Return to home screen"""
        self.current_app = None
        self.setup_home_ui()
    
    def show_docs(self, e):
        """Show documentation dialog"""
        try:
            print("📖 Opening documentation dialog...")
            
            docs_content = ft.Container(
                content=ft.Column([
                    ft.Text("📖 Media Tools Documentation", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("🎵 Audio Merger:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Merge multiple audio files with transition effects\n• Formats: MP3, WAV, FLAC, M4A, OGG, AAC, WMA\n• Effects: Crossfade, Gap, Direct merge", size=12),
                    ft.Container(height=10),
                    ft.Text("🎬 Media Codec Detector:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Detect codec and media file format\n• Support: Images, Videos, Audio\n• Stream and container format analysis", size=12),
                    ft.Container(height=10),
                    ft.Text("📥 YouTube Batch Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download multiple individual YouTube videos\n• Quality selection & auto-numbering\n• URL management from file or manual input", size=12),
                    ft.Container(height=10),
                    ft.Text("🎵 YouTube Playlist Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download entire YouTube playlists\n• Progress tracking per video\n• Flexible naming templates\n• Modern Flet interface", size=12),
                    ft.Container(height=10),
                    ft.Text("🌐 SocMed Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download video/audio from YouTube, TikTok, Instagram, Facebook, Twitter/X\n• Support video & audio (MP3) download\n• Batch download from TXT/CSV/JSON files\n• Quality selector (480p-1080p)", size=12),
                    ft.Container(height=10),
                    ft.Text("💡 Tips:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Make sure FFmpeg is installed\n• YouTube tools require yt-dlp\n• Use virtual environment for dependencies", size=12),
                ], spacing=5, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=450,
                padding=10
            )
            
            dialog = ft.AlertDialog(
                title=ft.Text("Documentation"),
                content=docs_content,
                actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(dialog))],
                actions_alignment=ft.MainAxisAlignment.END,
                modal=True
            )
            
            self.page.open(dialog)
            print("✅ Documentation dialog opened successfully")
        except Exception as ex:
            print(f"❌ Error showing docs: {ex}")
            import traceback
            traceback.print_exc()
    
    def show_requirements(self, e):
        """Show system requirements dialog"""
        try:
            print("⚙️ Opening system requirements dialog...")
            
            req_content = ft.Container(
                content=ft.Column([
                    ft.Text("⚙️ System Requirements", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("🐍 Python:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Python 3.8 or newer\n• Virtual environment (recommended)", size=12),
                    ft.Container(height=10),
                    ft.Text("📦 FFmpeg (Required):", weight=ft.FontWeight.BOLD),
                    ft.Text("Windows: choco install ffmpeg\nmacOS: brew install ffmpeg\nLinux: sudo apt install ffmpeg", size=12),
                    ft.Container(height=10),
                    ft.Text("📚 Python Dependencies:", weight=ft.FontWeight.BOLD),
                    ft.Text("• pydub (audio processing)\n• flet (GUI framework)\n• ffmpeg-python (FFmpeg wrapper)\n• Pillow (image processing)\n• filetype (file type detection)\n• yt-dlp (YouTube downloader)", size=12),
                    ft.Container(height=10),
                    ft.Text("💾 Disk Space:", weight=ft.FontWeight.BOLD),
                    ft.Text("• ~200MB for dependencies\n• Additional space for output files", size=12),
                ], spacing=5, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=400,
                padding=10
            )
            
            dialog = ft.AlertDialog(
                title=ft.Text("System Requirements"),
                content=req_content,
                actions=[ft.TextButton("Close", on_click=lambda e: self.page.close(dialog))],
                actions_alignment=ft.MainAxisAlignment.END,
                modal=True
            )
            
            self.page.open(dialog)
            print("✅ System requirements dialog opened successfully")
        except Exception as ex:
            print(f"❌ Error showing requirements: {ex}")
            import traceback
            traceback.print_exc()
    
    def close_dialog(self):
        """Close current dialog"""
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()
    
    def show_error(self, message):
        """Show error dialog"""
        dialog = ft.AlertDialog(
            title=ft.Row([
                ft.Icon(ft.Icons.ERROR, color=ft.Colors.RED),
                ft.Text("Error", color=ft.Colors.RED)
            ]),
            content=ft.Container(
                content=ft.Text(message, size=14),
                width=400,
                height=200
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog()),
                ft.TextButton("Debug Info", on_click=self.show_debug_info)
            ],
            modal=True
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_debug_info(self, e):
        """Show debug information"""
        debug_info = f"""Debug Information:
        
Current Directory: {Path(__file__).parent}
Audio Merger Path: {Path(__file__).parent / "audio-merger" / "audio_merger_gui.py"}
Audio Merger Exists: {(Path(__file__).parent / "audio-merger" / "audio_merger_gui.py").exists()}
Media Detector Path: {Path(__file__).parent / "media-codec-detector" / "media_codec_detector_gui.py"}
Media Detector Exists: {(Path(__file__).parent / "media-codec-detector" / "media_codec_detector_gui.py").exists()}
Batch Downloader Path: {Path(__file__).parent / "yt-batch-downloader" / "batch_downloader_gui.py"}
Batch Downloader Exists: {(Path(__file__).parent / "yt-batch-downloader" / "batch_downloader_gui.py").exists()}
Playlist Downloader Path: {Path(__file__).parent / "yt-playlist-downloader" / "playlist_downloader_gui.py"}
Playlist Downloader Exists: {(Path(__file__).parent / "yt-playlist-downloader" / "playlist_downloader_gui.py").exists()}

Available GUIs:
AudioMergerGUI: {AudioMergerGUI is not None}
MediaCodecDetectorGUI: {MediaCodecDetectorGUI is not None}
BatchDownloaderGUI: {BatchDownloaderGUI is not None}
PlaylistDownloaderGUI: {PlaylistDownloaderGUI is not None}

Python Path:
{chr(10).join(sys.path[:5])}... (showing first 5)"""
        
        debug_dialog = ft.AlertDialog(
            title=ft.Text("Debug Information"),
            content=ft.Container(
                content=ft.Text(debug_info, size=12, font_family="monospace"),
                width=500,
                height=300,
                scroll=ft.ScrollMode.AUTO
            ),
            actions=[ft.TextButton("Close", on_click=lambda e: self.close_dialog())],
            modal=True
        )
        
        self.page.dialog = debug_dialog
        debug_dialog.open = True
        self.page.update()
    
    def show_snackbar(self, message, color=ft.Colors.BLUE):
        """Show snackbar message"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE),
            bgcolor=color,
            duration=3000
        )
        self.page.snack_bar = snack_bar
        snack_bar.open = True
        self.page.update()
    
    def exit_app(self, e):
        """Exit the application"""
        print("🚪 Closing application...")
        # Set window prevent_close to False to allow closing
        self.page.window.prevent_close = False
        # Close the window
        self.page.window.close()
        # Update to process the close
        self.page.update()

def main(page: ft.Page):
    """Main function for Flet app"""
    app = MediaToolsLauncher(page)

if __name__ == "__main__":
    # Check if running from command line with tool-specific flags
    import sys
    
    if "--audio-merger" in sys.argv:
        # Launch Audio Merger directly
        try:
            current_dir = Path(__file__).parent
            audio_path = current_dir / "audio-merger" / "audio_merger_gui.py"
            if audio_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("audio_merger_gui", audio_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                ft.app(target=module.main, view=ft.AppView.FLET_APP)
            else:
                print("❌ Audio Merger GUI file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching Audio Merger: {e}")
    elif "--media-detector" in sys.argv:
        # Launch Media Detector directly
        try:
            current_dir = Path(__file__).parent
            detector_path = current_dir / "media-codec-detector" / "media_codec_detector_gui.py"
            if detector_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("media_codec_detector_gui", detector_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                ft.app(target=module.main, view=ft.AppView.FLET_APP)
            else:
                print("❌ Media Codec Detector GUI file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching Media Codec Detector: {e}")
    elif "--batch-downloader" in sys.argv:
        # Launch YouTube Batch Downloader directly
        try:
            current_dir = Path(__file__).parent
            batch_path = current_dir / "yt-batch-downloader" / "batch_downloader_gui.py"
            if batch_path.exists():
                import os
                original_cwd = os.getcwd()
                os.chdir(str(batch_path.parent))
                import subprocess
                subprocess.run([sys.executable, "batch_downloader_gui.py"])
                os.chdir(original_cwd)
            else:
                print("❌ YouTube Batch Downloader GUI file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching YouTube Batch Downloader: {e}")
    elif "--playlist-downloader" in sys.argv:
        # Launch YouTube Playlist Downloader directly
        try:
            current_dir = Path(__file__).parent
            playlist_path = current_dir / "yt-playlist-downloader" / "playlist_downloader_gui.py"
            if playlist_path.exists():
                import os
                original_cwd = os.getcwd()
                os.chdir(str(playlist_path.parent))
                import subprocess
                subprocess.run([sys.executable, "playlist_downloader_gui.py"])
                os.chdir(original_cwd)
            else:
                print("❌ YouTube Playlist Downloader GUI file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching YouTube Playlist Downloader: {e}")
    elif "--cli" in sys.argv:
        # Show CLI options
        print("🎬🎵 Media Tools CLI Options:")
        print("--audio-merger         : Launch Audio Merger GUI")
        print("--media-detector       : Launch Media Codec Detector GUI")
        print("--batch-downloader-flet    : Launch YouTube Batch Downloader GUI (Modern Flet)")
        print("--playlist-downloader-flet : Launch YouTube Playlist Downloader GUI (Modern Flet)")
        print("--batch-downloader         : Launch YouTube Batch Downloader GUI (Legacy Tkinter)")
        print("--playlist-downloader      : Launch YouTube Playlist Downloader GUI (Legacy Tkinter)")
        print("--help                : Show this help")
        print("\nUntuk CLI tools individual:")
        print("python audio-merger/audio_merger.py")
        print("python media-codec-detector/media_codec_detector.py")
        print("python yt-batch-downloader/batch_downloader.py")
        print("python yt-playlist-downloader/playlist_downloader.py")
    elif "--batch-downloader-flet" in sys.argv:
        # Launch YouTube Batch Downloader (Flet version) directly
        try:
            current_dir = Path(__file__).parent
            batch_flet_path = current_dir / "yt-batch-downloader" / "batch_downloader_gui_flet.py"
            if batch_flet_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("batch_downloader_gui_flet", batch_flet_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                ft.app(target=module.main, view=ft.AppView.FLET_APP)
            else:
                print("❌ YouTube Batch Downloader (Flet) file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching YouTube Batch Downloader (Flet): {e}")
    elif "--playlist-downloader-flet" in sys.argv:
        # Launch YouTube Playlist Downloader (Flet version) directly
        try:
            current_dir = Path(__file__).parent
            playlist_flet_path = current_dir / "yt-playlist-downloader" / "playlist_downloader_gui_flet.py"
            if playlist_flet_path.exists():
                import importlib.util
                spec = importlib.util.spec_from_file_location("playlist_downloader_gui_flet", playlist_flet_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                ft.app(target=module.main, view=ft.AppView.FLET_APP)
            else:
                print("❌ YouTube Playlist Downloader (Flet) file tidak ditemukan")
        except Exception as e:
            print(f"❌ Error launching YouTube Playlist Downloader (Flet): {e}")
    elif "--help" in sys.argv:
        print("🎬🎵 Media Tools Launcher")
        print("Usage: python media_tools_launcher.py [options]")
        print("\nOptions:")
        print("  (no args)              : Launch GUI home/launcher")
        print("  --audio-merger         : Launch Audio Merger directly")
        print("  --media-detector       : Launch Media Detector directly")
        print("  --batch-downloader-flet    : Launch YouTube Batch Downloader (Flet) directly")
        print("  --playlist-downloader-flet : Launch YouTube Playlist Downloader (Flet) directly")
        print("  --batch-downloader         : Launch YouTube Batch Downloader (Tkinter) directly")
        print("  --playlist-downloader      : Launch YouTube Playlist Downloader (Tkinter) directly")
        print("  --cli                  : Show CLI options")
        print("  --help                 : Show this help")
    else:
        # Launch main launcher GUI
        ft.app(target=main, view=ft.AppView.FLET_APP)
















