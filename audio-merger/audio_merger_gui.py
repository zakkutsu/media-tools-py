import flet as ft
import os
import glob
import threading
from pathlib import Path
import sys

# Add parent directory to path for language_config
sys.path.insert(0, str(Path(__file__).parent.parent))
from language_config import get_language, get_all_texts

# Konfigurasi FFmpeg path sebelum import pydub
FFMPEG_PATH = r"C:\Users\nonion\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\Users\nonion\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-essentials_build\bin\ffprobe.exe"

# Set environment untuk pydub agar menemukan ffmpeg
if os.path.exists(FFMPEG_PATH):
    os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment

class AudioMergerGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "🎵 Audio Merger"
        self.page.window_width = 750
        self.page.window_height = 700
        self.page.window_min_width = 700
        self.page.window_min_height = 650
        self.page.window_resizable = True
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.scroll = ft.ScrollMode.AUTO
        self.page.padding = 10
        
        # Language configuration
        self.current_language = get_language()
        self.translations = get_all_texts("audio_merger", self.current_language)
        self.common_translations = get_all_texts("common", self.current_language)
        
        # State variables
        self.selected_folder = ""
        self.output_folder = r"C:\Users\nonion\Music"  # Default folder tujuan penyimpanan
        self.audio_files = []
        self.output_filename = "merger_output"
        self.crossfade_duration = 0
        self.gap_duration = 0
        self.is_processing = False
        
        # Initialize UI
        self.setup_ui()
        
    def setup_ui(self):
        """Setup user interface"""
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.AUDIOTRACK, size=40, color=ft.colors.BLUE),
                    ft.Text(self.translations.get("title", "🎵 Audio Merger"), 
                           size=28, weight=ft.FontWeight.BOLD),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text(self.translations.get("description", 
                       "Gabungkan file audio menjadi satu dengan efek transisi"), 
                       size=14, color=ft.colors.GREY_700, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            margin=ft.margin.only(bottom=10)
        )
        
        # Folder selection
        self.folder_text = ft.Text(self.translations.get("folder_not_selected", "📁 Belum ada folder dipilih"), size=14)
        folder_button = ft.ElevatedButton(
            self.translations.get("select_audio_folder", "Pilih Folder Audio"),
            icon=ft.icons.FOLDER_OPEN,
            on_click=self.pick_folder_dialog,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE
        )
        
        folder_section = ft.Container(
            content=ft.Column([
                ft.Text(self.translations.get("step1", "1. Pilih Folder Audio"), size=16, weight=ft.FontWeight.BOLD),
                ft.Row([folder_button, self.folder_text], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=8)
        )
        
        # File list (reduced height to show more content below)
        self.files_list = ft.Column([], scroll=ft.ScrollMode.AUTO, height=120)
        self.files_section_title = ft.Text(self.translations.get("files_found_title", "2. File Audio Ditemukan"), size=16, weight=ft.FontWeight.BOLD)
        files_section = ft.Container(
            content=ft.Column([
                self.files_section_title,
                ft.Container(
                    content=self.files_list,
                    border=ft.border.all(1, ft.colors.GREY_300),
                    border_radius=5,
                    padding=10,
                    bgcolor=ft.colors.GREY_50
                )
            ]),
            margin=ft.margin.only(bottom=8)
        )
        
        # Output folder selection
        self.output_folder_text = ft.Text("📂 C:\\Users\\nonion\\Music", size=12, expand=True)
        output_folder_button = ft.ElevatedButton(
            self.translations.get("select_output_folder", "Pilih Folder Tujuan"),
            icon=ft.icons.SAVE,
            on_click=self.pick_output_folder_dialog,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            width=150
        )
        
        # Reset output folder button
        reset_output_button = ft.ElevatedButton(
            self.common_translations.get("reset", "Reset"),
            icon=ft.icons.REFRESH,
            on_click=self.reset_output_folder,
            bgcolor=ft.colors.GREY,
            color=ft.colors.WHITE,
            width=80
        )
        
        # Output settings (compact)
        self.output_field = ft.TextField(
            label=self.translations.get("output_filename_label", "Nama File Output"),
            value=self.output_filename,
            suffix_text=".mp3",
            on_change=self.on_output_change,
            width=300
        )
        
        # Effect settings
        self.effect_radio = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="normal", label=self.translations.get("effect_normal", "🔗 Gabungan Langsung (Tanpa Efek)")),
                ft.Radio(value="crossfade", label=self.translations.get("effect_crossfade", "🔄 Crossfade (Transisi Halus)")),
                ft.Radio(value="gap", label=self.translations.get("effect_gap", "⏸️ Gap/Jeda (Silence antar lagu)")),
            ]),
            value="normal",
            on_change=self.on_effect_change
        )
        
        self.crossfade_slider = ft.Slider(
            min=0, max=10, divisions=20, value=2,
            label="Crossfade: {value} detik",
            visible=False,
            on_change=self.on_crossfade_change
        )
        
        self.gap_slider = ft.Slider(
            min=0, max=5, divisions=10, value=1,
            label="Gap: {value} detik",
            visible=False,
            on_change=self.on_gap_change
        )
        
        # Output folder section
        output_folder_section = ft.Container(
            content=ft.Column([
                ft.Text(self.translations.get("step2", "3. Folder Tujuan Penyimpanan"), size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    output_folder_button,
                    reset_output_button,
                    self.output_folder_text
                ], alignment=ft.MainAxisAlignment.START, spacing=10),
            ]),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=8)
        )

        # Combined settings section
        settings_section = ft.Container(
            content=ft.Column([
                ft.Text(self.translations.get("step4", "4. Pengaturan Output & Efek"), size=16, weight=ft.FontWeight.BOLD),
                ft.Row([
                    ft.Column([
                        ft.Text(self.translations.get("output_filename_label", "Nama File:"), size=12, weight=ft.FontWeight.BOLD),
                        self.output_field,
                    ], spacing=5),
                    ft.Column([
                        ft.Text(self.translations.get("effects", "Efek Transisi:"), size=12, weight=ft.FontWeight.BOLD),
                        self.effect_radio,
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.crossfade_slider, self.gap_slider], alignment=ft.MainAxisAlignment.CENTER),
            ], spacing=8),
            padding=10,
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            margin=ft.margin.only(bottom=10)
        )
        
        # Progress and merge button
        self.progress_bar = ft.ProgressBar(value=0, visible=False, width=400, height=10)
        self.progress_text = ft.Text("", size=12, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)
        self.status_text = ft.Text("", size=12, color=ft.colors.GREY_700)
        
        self.merge_button = ft.ElevatedButton(
            self.translations.get("start_merge_btn", "🎵 Mulai Gabungkan Audio"),
            icon=ft.icons.PLAY_ARROW,
            on_click=self.start_merge,
            bgcolor=ft.colors.GREEN,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.padding.all(15)
            ),
            expand=True,
            height=50
        )
        
        # Progress section with better styling
        progress_section = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("Progress:", size=14, weight=ft.FontWeight.BOLD),
                    self.progress_text,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.progress_bar,
                ft.Container(height=5),  # Spacer
                self.status_text,
            ]),
            padding=15,
            bgcolor=ft.colors.BLUE_50,
            border_radius=8,
            border=ft.border.all(1, ft.colors.BLUE_200),
            visible=False
        )
        
        action_section = ft.Column([
            progress_section,
            ft.Container(height=10),  # Spacer
            ft.Row([self.merge_button], alignment=ft.MainAxisAlignment.CENTER),
        ])
        
        # Store reference to progress container for visibility control
        self.progress_container = progress_section
        
        # Main layout
        main_content = ft.Column([
            header,
            folder_section,
            files_section,
            output_folder_section,
            settings_section,
            action_section,
        ], scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        
        self.page.add(main_content)
        self.page.update()
    
    def pick_folder_dialog(self, e):
        """Open folder picker dialog"""
        def get_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.selected_folder = e.path
                self.folder_text.value = f"📁 {os.path.basename(e.path)}"
                self.scan_audio_files()
                self.page.update()
        
        get_directory_dialog = ft.FilePicker(on_result=get_directory_result)
        self.page.overlay.append(get_directory_dialog)
        self.page.update()
        get_directory_dialog.get_directory_path()
    
    def pick_output_folder_dialog(self, e):
        """Open output folder picker dialog"""
        def get_output_directory_result(e: ft.FilePickerResultEvent):
            if e.path:
                self.output_folder = e.path
                folder_name = os.path.basename(e.path)
                self.output_folder_text.value = f"📂 {folder_name}"
                self.output_folder_text.color = ft.colors.GREEN_700
                self.page.update()
        
        get_output_dialog = ft.FilePicker(on_result=get_output_directory_result)
        self.page.overlay.append(get_output_dialog)
        self.page.update()
        get_output_dialog.get_directory_path()
    
    def reset_output_folder(self, e):
        """Reset output folder to default Music folder"""
        self.output_folder = r"C:\Users\nonion\Music"
        self.output_folder_text.value = "📂 C:\\Users\\nonion\\Music"
        self.output_folder_text.color = ft.colors.GREY_700
        self.page.update()
    
    def scan_audio_files(self):
        """Scan folder for audio files"""
        if not self.selected_folder:
            return
            
        formats = ['mp3', 'wav', 'flac', 'm4a', 'ogg', 'aac', 'wma']
        self.audio_files = []
        
        for format_ext in formats:
            pattern = os.path.join(self.selected_folder, f"*.{format_ext}")
            files = glob.glob(pattern)
            self.audio_files.extend(files)
        
        self.audio_files.sort()
        
        # Update UI
        self.files_list.controls.clear()
        
        if self.audio_files:
            total_size = 0
            for i, file_path in enumerate(self.audio_files, 1):
                filename = os.path.basename(file_path)
                try:
                    file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                    total_size += file_size
                    size_text = f"({file_size:.1f} MB)"
                except:
                    size_text = ""
                
                self.files_list.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.icons.MUSIC_NOTE, size=16, color=ft.colors.BLUE),
                            ft.Column([
                                ft.Text(f"{i}. {filename}", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text(size_text, size=10, color=ft.colors.GREY_600),
                            ], spacing=2, expand=True),
                        ]),
                        padding=5,
                        border_radius=5,
                        bgcolor=ft.colors.WHITE if i % 2 == 0 else ft.colors.GREY_100,
                    )
                )
            
            # Add total info
            self.files_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.INFO, size=16, color=ft.colors.GREEN),
                        ft.Text(f"Total: {len(self.audio_files)} file • {total_size:.1f} MB", 
                               size=12, weight=ft.FontWeight.BOLD, color=ft.colors.GREEN),
                    ]),
                    padding=8,
                    bgcolor=ft.colors.GREEN_50,
                    border_radius=5,
                    margin=ft.margin.only(top=5)
                )
            )
        else:
            self.files_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.icons.ERROR, color=ft.colors.RED),
                        ft.Text("❌ Tidak ada file audio ditemukan", color=ft.colors.RED),
                    ]),
                    padding=10,
                    bgcolor=ft.colors.RED_50,
                    border_radius=5,
                    border=ft.border.all(1, ft.colors.RED_200)
                )
            )
        
        self.page.update()
    
    def on_output_change(self, e):
        """Handle output filename change"""
        self.output_filename = e.control.value if e.control.value else "merger_output"
    
    def on_effect_change(self, e):
        """Handle effect selection change"""
        effect = e.control.value
        
        self.crossfade_slider.visible = (effect == "crossfade")
        self.gap_slider.visible = (effect == "gap")
        
        if effect == "crossfade":
            self.crossfade_duration = int(self.crossfade_slider.value * 1000)
            self.gap_duration = 0
        elif effect == "gap":
            self.gap_duration = int(self.gap_slider.value * 1000)
            self.crossfade_duration = 0
        else:
            self.crossfade_duration = 0
            self.gap_duration = 0
        
        self.page.update()
    
    def on_crossfade_change(self, e):
        """Handle crossfade slider change"""
        self.crossfade_duration = int(e.control.value * 1000)
    
    def on_gap_change(self, e):
        """Handle gap slider change"""
        self.gap_duration = int(e.control.value * 1000)
    
    def start_merge(self, e):
        """Start the audio merging process"""
        if not self.audio_files:
            self.show_snackbar("❌ Pilih folder yang berisi file audio terlebih dahulu!", ft.colors.RED)
            return
        
        if self.is_processing:
            return
        
        # Start merging in background thread
        self.is_processing = True
        self.merge_button.text = "⏳ Sedang Memproses..."
        self.merge_button.icon = ft.icons.HOURGLASS_EMPTY
        self.merge_button.bgcolor = ft.colors.ORANGE
        self.merge_button.disabled = True
        self.progress_container.visible = True
        self.progress_bar.value = 0
        self.progress_text.value = "0%"
        self.status_text.value = f"🔄 Memulai penggabungan {len(self.audio_files)} file audio..."
        self.page.update()
        
        # Run merge in thread to avoid blocking UI
        threading.Thread(target=self.merge_audio_files_wrapper, daemon=True).start()
    
    def merge_audio_files_wrapper(self):
        """Wrapper for merge_audio_files with better error handling"""
        try:
            self.merge_audio_files()
        except Exception as e:
            print(f"Error in merge process: {e}")
            # Reset UI on error
            try:
                self.is_processing = False
                self.merge_button.text = "🎵 Mulai Gabungkan Audio"
                self.merge_button.icon = ft.icons.PLAY_ARROW
                self.merge_button.bgcolor = ft.colors.GREEN
                self.merge_button.disabled = False
                self.progress_container.visible = False
                self.status_text.value = f"❌ Error: {str(e)}"
                self.page.update()
            except:
                pass
    
    def merge_audio_files(self):
        """Merge audio files (runs in background thread)"""
        try:
            # Determine output filename with extension
            output_filename = self.output_filename
            if not output_filename.endswith(('.mp3', '.wav', '.flac', '.m4a', '.ogg')):
                output_filename += '.mp3'
            
            # Determine output path based on selected output folder
            if self.output_folder:
                # Use selected output folder
                output_path = os.path.join(self.output_folder, output_filename)
            else:
                # Use input folder as default
                output_path = os.path.join(self.selected_folder, output_filename) if self.selected_folder else output_filename
            
            total_files = len(self.audio_files)
            
            # Step 1: Loading first file (10% progress)
            self.update_progress(5, f"📂 Memuat file pertama: {os.path.basename(self.audio_files[0])}")
            combined_audio = AudioSegment.from_file(self.audio_files[0])
            self.update_progress(10, f"✅ File pertama dimuat: {os.path.basename(self.audio_files[0])}")
            
            # Step 2: Merge remaining files (10% - 80% progress)
            if total_files > 1:
                merge_progress_per_file = 70 / (total_files - 1)  # 70% for merging phase
                
                for i, audio_file in enumerate(self.audio_files[1:], 2):
                    progress = 10 + (i-1) * merge_progress_per_file
                    filename = os.path.basename(audio_file)
                    
                    self.update_progress(progress, f"🔗 Memuat file {i}/{total_files}: {filename}")
                    next_audio = AudioSegment.from_file(audio_file)
                    
                    self.update_progress(progress + merge_progress_per_file/2, f"🔀 Menggabungkan file {i}/{total_files}: {filename}")
                    
                    if self.crossfade_duration > 0:
                        combined_audio = combined_audio.append(next_audio, crossfade=self.crossfade_duration)
                    elif self.gap_duration > 0:
                        silence = AudioSegment.silent(duration=self.gap_duration)
                        combined_audio = combined_audio + silence + next_audio
                    else:
                        combined_audio += next_audio
                    
                    self.update_progress(progress + merge_progress_per_file, f"✅ File {i}/{total_files} berhasil digabungkan")
            
            # Step 3: Export result (80% - 100% progress)
            self.update_progress(85, f"💾 Memulai ekspor ke: {os.path.basename(output_path)}")
            
            output_format = output_filename.split('.')[-1].lower()
            if output_format not in ['mp3', 'wav', 'flac', 'm4a', 'ogg']:
                output_format = 'mp3'
            
            # Export with progress simulation
            self.update_progress(90, f"📤 Mengekspor audio dalam format {output_format.upper()}...")
            combined_audio.export(output_path, format=output_format)
            self.update_progress(95, "🔍 Memverifikasi file hasil...")
            
            # Calculate stats
            duration_seconds = len(combined_audio) / 1000
            minutes = int(duration_seconds // 60)
            seconds = int(duration_seconds % 60)
            file_size = os.path.getsize(output_path) / (1024*1024)
            
            # Show path info in success message
            folder_info = f"📁 {os.path.dirname(output_path)}" if self.output_folder else "📁 Folder input"
            self.update_progress(100, f"🎉 Selesai! Durasi: {minutes}:{seconds:02d}, Ukuran: {file_size:.1f} MB")
            
            # Update status with full path info
            self.update_status(f"✅ File tersimpan: {output_path}")
            self.show_snackbar_safe("🎉 Audio berhasil digabungkan!", ft.colors.GREEN)
            
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            self.update_status(error_msg)
            self.show_snackbar_safe(f"❌ Gagal menggabungkan audio: {str(e)}", ft.colors.RED)
        
        finally:
            # Reset UI state after 3 seconds to show final result
            import time
            time.sleep(3)
            
            try:
                self.is_processing = False
                self.merge_button.text = "🎵 Mulai Gabungkan Audio"
                self.merge_button.icon = ft.icons.PLAY_ARROW
                self.merge_button.bgcolor = ft.colors.GREEN
                self.merge_button.disabled = False
                self.progress_container.visible = False
                self.page.update()
            except Exception as e:
                print(f"Error resetting UI: {e}")
    
    def update_status(self, message):
        """Update status text (thread-safe)"""
        try:
            self.status_text.value = message
            self.page.update()
        except Exception as e:
            print(f"Error updating status: {e}")
    
    def update_progress(self, percentage, message):
        """Update progress bar and status (thread-safe)"""
        try:
            self.progress_bar.value = percentage / 100
            self.progress_text.value = f"{int(percentage)}%"
            self.status_text.value = message
            self.page.update()
        except Exception as e:
            print(f"Error updating progress: {e}")
        
        # Small delay to make progress visible
        import time
        time.sleep(0.1)
    
    def show_snackbar(self, message, color):
        """Show snackbar notification"""
        snackbar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=color,
            duration=3000
        )
        self.page.snack_bar = snackbar
        snackbar.open = True
        self.page.update()
    
    def show_snackbar_safe(self, message, color):
        """Thread-safe snackbar"""
        try:
            self.show_snackbar(message, color)
        except Exception as e:
            print(f"Error showing snackbar: {e}")

def main(page: ft.Page):
    """Main function for Flet app"""
    app = AudioMergerGUI(page)

if __name__ == "__main__":
    # Check if running from command line with --cli flag
    import sys
    if "--cli" in sys.argv:
        # Import and run CLI version
        from audio_merger import main as cli_main
        cli_main()
    else:
        # Run GUI version
        ft.app(target=main, view=ft.AppView.FLET_APP)