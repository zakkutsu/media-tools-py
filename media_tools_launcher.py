import flet as ft
import os
import sys
from pathlib import Path
import importlib.util
import subprocess
from language_config import get_language, set_language, get_available_languages, get_all_texts

# Import the GUI classes from both tools
current_dir = Path(__file__).parent

# Add paths for imports
audio_merger_path = str(current_dir / "audio-merger")
media_detector_path = str(current_dir / "media-codec-detector")
batch_downloader_path = str(current_dir / "yt-batch-downloader")
playlist_downloader_path = str(current_dir / "yt-playlist-downloader")
socmed_downloader_path = str(current_dir / "socmed-downloader")
media_looper_path = str(current_dir / "media-looper")

# Add all tool paths to sys.path
tool_paths = [audio_merger_path, media_detector_path, batch_downloader_path, playlist_downloader_path, socmed_downloader_path, media_looper_path]
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
        'yt_dlp': 'yt-dlp'
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

class MediaToolsLauncher:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎬🎵 Media Tools Launcher"
        self.page.window_width = 800
        self.page.window_height = 600
        self.page.window_min_width = 600
        self.page.window_min_height = 500
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Language configuration
        self.current_language = get_language()
        self.translations = get_all_texts("launcher", self.current_language)
        self.common_translations = get_all_texts("common", self.current_language)
        
        # State management
        self.current_app = None
        self.home_view = None
        self.app_view = None
        
        # Initialize UI
        self.setup_home_ui()
        
    def change_language(self, e):
        """Handle language change"""
        new_lang = e.control.value
        if set_language(new_lang):
            self.current_language = new_lang
            self.translations = get_all_texts("launcher", self.current_language)
            self.common_translations = get_all_texts("common", self.current_language)
            # Refresh UI
            self.setup_home_ui()
    
    def setup_home_ui(self):
        """Setup the main home interface"""
        
        # Clear page
        self.page.controls.clear()
        
        # Language selector dropdown
        languages = get_available_languages()
        language_options = [
            ft.dropdown.Option(key=lang_code, text=f"{lang_data['flag']} {lang_data['name']}")
            for lang_code, lang_data in languages.items()
        ]
        
        language_selector = ft.Dropdown(
            value=self.current_language,
            options=language_options,
            width=250,
            on_change=self.change_language,
            border_color=ft.colors.DEEP_PURPLE,
            focused_border_color=ft.colors.DEEP_PURPLE_400,
            label=self.common_translations.get("select_language", "Pilih Bahasa"),
        )
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.BUILD_CIRCLE, size=50, color=ft.colors.DEEP_PURPLE),
                    ft.Column([
                        ft.Text(self.translations.get("title", "Media Tools"), 
                               size=32, weight=ft.FontWeight.BOLD),
                        ft.Text(self.translations.get("subtitle", "Suite"), 
                               size=24, weight=ft.FontWeight.W_300, color=ft.colors.GREY_600),
                    ], spacing=0),
                    ft.Container(expand=True),  # Spacer
                    language_selector,
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Text(self.translations.get("description", "Pilih tool yang ingin Anda gunakan"), 
                       size=16, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=15),
            padding=30,
            bgcolor=ft.colors.DEEP_PURPLE_50,
            border_radius=15,
            margin=ft.margin.only(bottom=30)
        )
        
        # Tool cards
        audio_merger_card = self.create_tool_card(
            title=self.translations.get("tool_audio_merger", "🎵 Audio Merger"),
            description=self.translations.get("audio_merger_desc", 
                "Gabungkan multiple file audio menjadi satu dengan efek transisi seperti crossfade dan gap"),
            features=[
                "✨ Crossfade & Gap effects",
                "🎚️ Multi-format support",
                "📊 Real-time progress",
                "🎨 Modern GUI interface"
            ],
            color=ft.colors.BLUE,
            on_click=self.launch_audio_merger
        )
        
        media_detector_card = self.create_tool_card(
            title=self.translations.get("tool_media_detector", "🎬 Media Codec Detector"), 
            description=self.translations.get("media_detector_desc",
                "Deteksi format kontainer dan codec dari file media (gambar, video, audio)"),
            features=[
                "🕵️ Comprehensive codec detection", 
                "📱 Image format analysis",
                "🎥 Video & audio streams",
                "🧪 Dummy file generator"
            ],
            color=ft.colors.PURPLE,
            on_click=self.launch_media_detector
        )
        
        batch_downloader_card = self.create_tool_card(
            title=self.translations.get("tool_batch_downloader", "📥 Batch Downloader"),
            description=self.translations.get("batch_downloader_desc",
                "Download multiple individual YouTube videos dengan modern Flet interface"),
            features=[
                "� Modern Flet GUI interface",
                "📝 URL management & batch loading",
                "� Quality selection options",
                "📊 Real-time progress tracking"
            ],
            color=ft.colors.RED,
            on_click=self.launch_batch_downloader
        )
        
        playlist_downloader_card = self.create_tool_card(
            title=self.translations.get("tool_playlist_downloader", "🎵 Playlist Downloader"),
            description=self.translations.get("playlist_downloader_desc",
                "Download complete YouTube playlists dengan elegant interface"),
            features=[
                "📱 Modern Flet GUI interface",
                "🎵 Full playlist downloading",
                "🎯 Flexible naming templates",
                "📊 Progress tracking per video"
            ],
            color=ft.colors.ORANGE,
            on_click=self.launch_playlist_downloader
        )
        
        socmed_downloader_card = self.create_tool_card(
            title=self.translations.get("tool_socmed_downloader", "📥 SocMed Downloader"),
            description=self.translations.get("socmed_downloader_desc",
                "Download video/audio dari YouTube, TikTok, Instagram, Facebook, Twitter/X"),
            features=[
                "🌐 Multi-platform (YT, TikTok, IG, FB, X)",
                "🎬 Video & Audio (MP3) support",
                "📦 Batch download (TXT/CSV/JSON)",
                "🎯 Quality selector (480p-1080p)"
            ],
            color=ft.colors.GREEN,
            on_click=self.launch_socmed_downloader
        )
        
        media_looper_card = self.create_tool_card(
            title=self.translations.get("tool_media_looper", "🔁 Media Looper"),
            description=self.translations.get("media_looper_desc",
                "Loop video/audio N kali tanpa re-encoding menggunakan FFmpeg stream copy"),
            features=[
                "⚡ Super cepat (stream copy, no re-encode)",
                "🎵 Audio & Video support",
                "📊 Duration calculator",
                "🎯 Zero quality loss"
            ],
            color=ft.colors.TEAL,
            on_click=self.launch_media_looper
        )
        
        # Tool selection section
        tools_section = ft.Container(
            content=ft.Column([
                ft.Text(self.translations.get("select_tool", "Pilih Tool"), 
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
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            margin=ft.margin.only(bottom=30)
        )
        
        # Additional info section
        info_section = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=ft.colors.GREY_300),
                ft.Row([
                    ft.Icon(ft.icons.INFO_OUTLINE, size=20, color=ft.colors.GREY_600),
                    ft.Text(self.translations.get("info_message", 
                           "Kedua tool memerlukan FFmpeg untuk berfungsi dengan optimal"), 
                           size=14, color=ft.colors.GREY_600),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Row([
                    ft.TextButton(self.translations.get("documentation", "📖 Dokumentasi"), 
                                 on_click=self.show_docs),
                    ft.TextButton(self.translations.get("system_requirements", "⚙️ System Requirements"), 
                                 on_click=self.show_requirements),
                    ft.TextButton(self.translations.get("exit", "❌ Exit"), 
                                 on_click=self.exit_app),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
            ], spacing=15),
            padding=20,
            margin=ft.margin.only(top=20)
        )
        
        # Main layout
        main_content = ft.Column([
            header,
            tools_section,
            info_section,
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
                    ft.Text(feature, size=12, color=ft.colors.GREY_700)
                ])
            )
        
        card = ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.PLAY_CIRCLE_FILL, color=color, size=30),
                        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, expand=True),
                    ]),
                    padding=15,
                    bgcolor=ft.colors.with_opacity(0.1, color),
                    border_radius=ft.border_radius.only(top_left=10, top_right=10)
                ),
                
                # Content
                ft.Container(
                    content=ft.Column([
                        ft.Text(description, size=14, color=ft.colors.GREY_800),
                        ft.Container(height=10),  # Spacing
                        ft.Text("Features:", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREY_700),
                        ft.Column(feature_items, spacing=5),
                        ft.Container(height=15),  # Spacing
                        ft.ElevatedButton(
                            self.translations.get("launch_tool", "Launch Tool"),
                            icon=ft.icons.ROCKET_LAUNCH,
                            bgcolor=color,
                            color=ft.colors.WHITE,
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
            border=ft.border.all(2, ft.colors.with_opacity(0.3, color)),
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=5,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2)
            )
        )
        
        return card
    
    def launch_audio_merger(self, e):
        """Launch Audio Merger tool"""
        if AudioMergerGUI is None:
            error_msg = "Audio Merger tidak tersedia.\n\nPastikan file audio_merger_gui.py ada di folder audio-merger/\n\nPeriksa juga bahwa semua dependencies sudah terinstall dengan:\npip install -r requirements.txt"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("audio_merger")
    
    def launch_media_detector(self, e):
        """Launch Media Codec Detector tool"""
        if MediaCodecDetectorGUI is None:
            error_msg = "Media Codec Detector tidak tersedia.\n\nPastikan file media_codec_detector_gui.py ada di folder media-codec-detector/\n\nPeriksa juga bahwa semua dependencies sudah terinstall dengan:\npip install -r requirements.txt"
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
            error_msg = "YouTube Batch Downloader tidak tersedia.\n\nPastikan file batch_downloader_gui_flet.py atau batch_downloader_gui.py ada di folder yt-batch-downloader/\n\nPeriksa juga bahwa yt-dlp sudah terinstall dengan:\npip install yt-dlp"
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
            error_msg = "YouTube Playlist Downloader tidak tersedia.\n\nPastikan file playlist_downloader_gui_flet.py atau playlist_downloader_gui.py ada di folder yt-playlist-downloader/\n\nPeriksa juga bahwa yt-dlp sudah terinstall dengan:\npip install yt-dlp"
            self.show_error(error_msg)
            return
    
    def launch_socmed_downloader(self, e):
        """Launch SocMed Downloader tool"""
        if SocMedDownloaderGUI is None:
            error_msg = "SocMed Downloader tidak tersedia.\n\nPastikan file socmed_downloader_gui.py ada di folder socmed-downloader/\n\nPeriksa juga bahwa yt-dlp sudah terinstall dengan:\npip install yt-dlp"
            self.show_error(error_msg)
            return
        
        self.switch_to_app("socmed_downloader")
    
    def launch_media_looper(self, e):
        """Launch Media Looper tool"""
        if MediaLooperGUI is None:
            error_msg = "Media Looper tidak tersedia.\n\nPastikan file media_looper_gui_flet.py ada di folder media-looper/\n\nPeriksa juga bahwa FFmpeg sudah terinstall dan ada di system PATH."
            self.show_error(error_msg)
            return
        
        self.switch_to_app("media_looper")
    
    def switch_to_app(self, app_name):
        """Switch to specific application"""
        self.page.controls.clear()
        
        # Create back button
        back_button = ft.Container(
            content=ft.ElevatedButton(
                self.common_translations.get("back_to_home", "🏠 Back to Home"),
                icon=ft.icons.HOME,
                on_click=self.back_to_home,
                bgcolor=ft.colors.GREY_600,
                color=ft.colors.WHITE
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
        self.show_snackbar(f"🚀 Launching {app_name.replace('_', ' ').title()}...", ft.colors.BLUE)
        
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
                    self.show_snackbar(f"✅ {app_name.replace('_', ' ').title()} launched successfully!", ft.colors.GREEN)
                self.page.run_thread_safe(show_success)
                
            except FileNotFoundError as e:
                print(f"File not found for {app_name}: {e}")
                def show_error():
                    self.show_snackbar(f"❌ {app_name.replace('_', ' ').title()} file not found", ft.colors.RED)
                self.page.run_thread_safe(show_error)
            except Exception as e:
                print(f"Unexpected error launching {app_name}: {e}")
                def show_error():
                    self.show_snackbar(f"❌ Error launching {app_name.replace('_', ' ').title()}: {str(e)}", ft.colors.RED)
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
                    ft.Text("📖 Dokumentasi Media Tools", size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    ft.Text("🎵 Audio Merger:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Gabungkan multiple file audio dengan efek transisi\n• Format: MP3, WAV, FLAC, M4A, OGG, AAC, WMA\n• Efek: Crossfade, Gap/Jeda, Gabungan langsung", size=12),
                    ft.Container(height=10),
                    ft.Text("🎬 Media Codec Detector:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Deteksi codec dan format file media\n• Support: Gambar, Video, Audio\n• Analisis stream dan container format", size=12),
                    ft.Container(height=10),
                    ft.Text("📥 YouTube Batch Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download multiple individual YouTube videos\n• Quality selection & auto-numbering\n• URL management dari file atau manual input", size=12),
                    ft.Container(height=10),
                    ft.Text("🎵 YouTube Playlist Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download entire YouTube playlists\n• Progress tracking per video\n• Flexible naming templates\n• Modern Flet interface", size=12),
                    ft.Container(height=10),
                    ft.Text("� SocMed Downloader:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Download video/audio dari YouTube, TikTok, Instagram, Facebook, Twitter/X\n• Support video & audio (MP3) download\n• Batch download dari file TXT/CSV/JSON\n• Quality selector (480p-1080p)", size=12),
                    ft.Container(height=10),
                    ft.Text("�💡 Tips:", weight=ft.FontWeight.BOLD),
                    ft.Text("• Pastikan FFmpeg sudah terinstall\n• YouTube tools memerlukan yt-dlp\n• Gunakan virtual environment untuk dependencies", size=12),
                ], spacing=5, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=450,
                padding=10
            )
            
            dialog = ft.AlertDialog(
                title=ft.Text("Dokumentasi"),
                content=docs_content,
                actions=[ft.TextButton("Tutup", on_click=lambda e: self.page.close(dialog))],
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
                    ft.Text("• Python 3.8 atau lebih baru\n• Virtual environment (recommended)", size=12),
                    ft.Container(height=10),
                    ft.Text("📦 FFmpeg (Wajib):", weight=ft.FontWeight.BOLD),
                    ft.Text("Windows: choco install ffmpeg\nmacOS: brew install ffmpeg\nLinux: sudo apt install ffmpeg", size=12),
                    ft.Container(height=10),
                    ft.Text("📚 Python Dependencies:", weight=ft.FontWeight.BOLD),
                    ft.Text("• pydub (audio processing)\n• flet (GUI framework)\n• ffmpeg-python (FFmpeg wrapper)\n• Pillow (image processing)\n• filetype (file type detection)\n• yt-dlp (YouTube downloader)", size=12),
                    ft.Container(height=10),
                    ft.Text("💾 Disk Space:", weight=ft.FontWeight.BOLD),
                    ft.Text("• ~200MB untuk dependencies\n• Space tambahan untuk file output", size=12),
                ], spacing=5, scroll=ft.ScrollMode.AUTO),
                width=500,
                height=400,
                padding=10
            )
            
            dialog = ft.AlertDialog(
                title=ft.Text("System Requirements"),
                content=req_content,
                actions=[ft.TextButton("Tutup", on_click=lambda e: self.page.close(dialog))],
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
                ft.Icon(ft.icons.ERROR, color=ft.colors.RED),
                ft.Text("Error", color=ft.colors.RED)
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
    
    def show_snackbar(self, message, color=ft.colors.BLUE):
        """Show snackbar message"""
        snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
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










