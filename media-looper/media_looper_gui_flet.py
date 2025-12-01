"""
Media Looper - Flet GUI Version
Single Loop & Alternating Loop dengan modern interface

Author: Media Tools Suite
"""

import flet as ft
import subprocess
import os
import sys
import shutil
import threading
from pathlib import Path


class MediaLooperGUI:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Media Looper Tool"
        self.page.window_width = 900
        self.page.window_height = 700
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        
        self.processing = False
        
        # Check FFmpeg
        if not shutil.which('ffmpeg'):
            self.show_error("FFmpeg tidak ditemukan!\n\nInstall FFmpeg terlebih dahulu.")
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup main UI"""
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.LOOP, size=40, color=ft.colors.WHITE),
                    ft.Text("Media Looper Tool", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Stream Copy Looping - Instant Processing", 
                       size=14, color=ft.colors.WHITE70, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=ft.colors.TEAL_700,
            padding=20,
        )
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Single Loop",
                    icon=ft.icons.REPEAT,
                    content=self.create_single_loop_tab()
                ),
                ft.Tab(
                    text="Alternating Loop",
                    icon=ft.icons.SWAP_HORIZ,
                    content=self.create_alternating_loop_tab()
                ),
            ],
            expand=1,
        )
        
        # Main layout
        self.page.add(
            ft.Column([
                header,
                self.tabs,
            ], spacing=0, expand=True)
        )
    
    def create_single_loop_tab(self):
        """Create single loop tab"""
        # File input
        self.single_file = ft.TextField(
            label="Input File",
            hint_text="Select or drag file here",
            read_only=True,
            expand=True,
        )
        
        browse_btn = ft.ElevatedButton(
            "Browse",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.single_file),
        )
        
        # Loop count
        self.single_loop_count = ft.TextField(
            label="Loop Count",
            hint_text="e.g., 60",
            value="60",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # Presets
        presets = ft.Row([
            ft.Text("Quick:", size=12, color=ft.colors.GREY_600),
            *[ft.FilledButton(
                f"{p}x",
                on_click=lambda e, count=p: setattr(self.single_loop_count, 'value', str(count)) or self.page.update(),
                style=ft.ButtonStyle(padding=8),
            ) for p in [10, 20, 30, 60, 120]]
        ], spacing=5)
        
        # Process button
        process_btn = ft.ElevatedButton(
            "⚡ Process",
            icon=ft.icons.PLAY_ARROW,
            on_click=lambda _: self.process_single_loop(),
            bgcolor=ft.colors.TEAL_600,
            color=ft.colors.WHITE,
            height=50,
        )
        
        # Status
        self.single_status = ft.Text("Ready", size=12, color=ft.colors.GREY_600)
        self.single_log = ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Info", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "• Loop 1 file berkali-kali (A-A-A...)\n"
                            "• Stream copy = instant, zero quality loss\n"
                            "• Contoh: 3 menit MP3 × 20 = 60 menit dalam 2 detik",
                            size=12, color=ft.colors.GREY_700,
                        ),
                    ], spacing=5),
                    bgcolor=ft.colors.BLUE_50,
                    padding=15,
                    border_radius=10,
                ),
                ft.Divider(),
                ft.Text("Input File", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.single_file, browse_btn], spacing=10),
                ft.Divider(),
                ft.Text("Loop Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.single_loop_count, presets], spacing=20),
                ft.Divider(),
                process_btn,
                ft.Divider(),
                ft.Text("Status", size=14, weight=ft.FontWeight.BOLD),
                self.single_status,
                ft.Container(
                    content=self.single_log,
                    bgcolor=ft.colors.GREY_100,
                    padding=10,
                    border_radius=5,
                    expand=True,
                ),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True,
        )
    
    def create_alternating_loop_tab(self):
        """Create alternating loop tab"""
        # File inputs
        self.alt_file_a = ft.TextField(
            label="File A (First)",
            hint_text="Select first file",
            read_only=True,
            expand=True,
        )
        
        self.alt_file_b = ft.TextField(
            label="File B (Second)",
            hint_text="Select second file",
            read_only=True,
            expand=True,
        )
        
        browse_a_btn = ft.ElevatedButton(
            "Browse A",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.alt_file_a),
        )
        
        browse_b_btn = ft.ElevatedButton(
            "Browse B",
            icon=ft.icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.alt_file_b),
        )
        
        # Loop count
        self.alt_loop_count = ft.TextField(
            label="Loop Count (Sets)",
            hint_text="e.g., 10",
            value="10",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        
        # Presets
        presets = ft.Row([
            ft.Text("Quick:", size=12, color=ft.colors.GREY_600),
            *[ft.FilledButton(
                f"{p}x",
                on_click=lambda e, count=p: setattr(self.alt_loop_count, 'value', str(count)) or self.page.update(),
                style=ft.ButtonStyle(padding=8),
            ) for p in [5, 10, 20, 30, 50]]
        ], spacing=5)
        
        # Delay/Silence options
        self.alt_delay = ft.TextField(
            label="Delay After A (seconds)",
            hint_text="0 = no delay",
            value="0",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="sec",
        )
        
        delay_presets = ft.Row([
            ft.Text("Quick:", size=12, color=ft.colors.GREY_600),
            *[ft.FilledButton(
                f"{p}s",
                on_click=lambda e, delay=p: setattr(self.alt_delay, 'value', str(delay)) or self.page.update(),
                style=ft.ButtonStyle(padding=8),
            ) for p in [0, 1, 2, 3, 5]]
        ], spacing=5)
        
        # Process button
        process_btn = ft.ElevatedButton(
            "⚡ Process",
            icon=ft.icons.PLAY_ARROW,
            on_click=lambda _: self.process_alternating_loop(),
            bgcolor=ft.colors.ORANGE_600,
            color=ft.colors.WHITE,
            height=50,
        )
        
        # Status
        self.alt_status = ft.Text("Ready", size=12, color=ft.colors.GREY_600)
        self.alt_log = ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Info", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "• Loop 2 file bergantian (A-B-A-B...)\n"
                            "• Ideal: intro-content, Q&A drill, music-silence\n"
                            "• Optional delay: A → [silence] → B (for thinking time)\n"
                            "• ⚠️ Both files MUST have same format & codec!",
                            size=12, color=ft.colors.GREY_700,
                        ),
                    ], spacing=5),
                    bgcolor=ft.colors.ORANGE_50,
                    padding=15,
                    border_radius=10,
                ),
                ft.Divider(),
                ft.Text("Input Files", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.alt_file_a, browse_a_btn], spacing=10),
                ft.Row([self.alt_file_b, browse_b_btn], spacing=10),
                ft.Divider(),
                ft.Text("Loop Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.alt_loop_count, presets], spacing=20),
                ft.Row([self.alt_delay, delay_presets], spacing=20),
                ft.Text("💡 Use delay for Q&A drill: Question → [pause] → Answer", 
                       size=11, color=ft.colors.GREY_600, italic=True),
                ft.Divider(),
                process_btn,
                ft.Divider(),
                ft.Text("Status", size=14, weight=ft.FontWeight.BOLD),
                self.alt_status,
                ft.Container(
                    content=self.alt_log,
                    bgcolor=ft.colors.GREY_100,
                    padding=10,
                    border_radius=5,
                    expand=True,
                ),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True,
        )
    
    def browse_file(self, target_field):
        """Browse file dialog"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                target_field.value = e.files[0].path
                self.page.update()
        
        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.pick_files(
            dialog_title="Select Media File",
            allowed_extensions=["mp4", "mkv", "avi", "mov", "mp3", "wav", "aac", "flac", "m4a"],
        )
    
    def log_message(self, log_container, message, color=None):
        """Add log message"""
        log_container.controls.append(
            ft.Text(message, size=11, color=color or ft.colors.BLACK87)
        )
        self.page.update()
    
    def get_duration(self, file_path):
        """Get media duration"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                   '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
            return float(result.stdout.strip())
        except:
            return None
    
    def format_duration(self, seconds):
        """Format duration"""
        if not seconds:
            return "Unknown"
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"
    
    def generate_silence(self, reference_file, duration):
        """Generate silence file matching reference format"""
        try:
            # Get reference file format info
            ext = os.path.splitext(reference_file)[1]
            is_video = ext.lower() in ['.mp4', '.mkv', '.avi', '.mov', '.webm']
            
            silence_file = f"temp_silence_{duration}s{ext}"
            
            if is_video:
                # Video: black frame + silent audio
                cmd = [
                    'ffmpeg', '-f', 'lavfi', '-i', f'color=c=black:s=1920x1080:d={duration}',
                    '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo:d={duration}',
                    '-c:v', 'libx264', '-preset', 'ultrafast', '-pix_fmt', 'yuv420p',
                    '-c:a', 'aac', '-shortest', silence_file, '-y'
                ]
            else:
                # Audio: silent audio
                cmd = [
                    'ffmpeg', '-f', 'lavfi', '-i', f'anullsrc=r=48000:cl=stereo:d={duration}',
                    '-c:a', 'aac', silence_file, '-y'
                ]
            
            subprocess.run(cmd, check=True, capture_output=True, timeout=30)
            return silence_file
        except Exception as e:
            print(f"Error generating silence: {e}")
            return None
    
    def process_single_loop(self):
        """Process single loop in thread"""
        if self.processing:
            self.show_snackbar("Already processing!", ft.colors.ORANGE)
            return
        
        file_path = self.single_file.value
        if not file_path or not os.path.exists(file_path):
            self.show_error("Select a valid file!")
            return
        
        try:
            count = int(self.single_loop_count.value)
            if count < 1:
                self.show_error("Loop count must be >= 1")
                return
        except ValueError:
            self.show_error("Invalid loop count!")
            return
        
        thread = threading.Thread(target=self._process_single_worker, args=(file_path, count))
        thread.daemon = True
        thread.start()
    
    def _process_single_worker(self, file_path, count):
        """Worker thread for single loop"""
        self.processing = True
        self.single_status.value = "Processing..."
        self.single_status.color = ft.colors.BLUE
        self.single_log.controls.clear()
        self.page.update()
        
        try:
            # Duration info
            duration = self.get_duration(file_path)
            if duration:
                total = duration * count
                self.log_message(self.single_log, 
                    f"📊 Duration: {self.format_duration(duration)} → {self.format_duration(total)} ({count}x)")
            
            # Prepare output
            filename, ext = os.path.splitext(file_path)
            output_file = f"{filename}_looped_{count}x{ext}"
            
            self.log_message(self.single_log, f"Input: {os.path.basename(file_path)}")
            self.log_message(self.single_log, f"Output: {os.path.basename(output_file)}")
            self.log_message(self.single_log, "\n⚙️ FFmpeg processing...", ft.colors.BLUE)
            
            # FFmpeg command
            loop_count = count - 1
            cmd = ['ffmpeg', '-stream_loop', str(loop_count), '-i', file_path,
                   '-c', 'copy', output_file, '-y']
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            size = os.path.getsize(output_file) / (1024 * 1024)
            self.log_message(self.single_log, f"\n✅ SUCCESS!", ft.colors.GREEN)
            self.log_message(self.single_log, f"📁 {output_file}")
            self.log_message(self.single_log, f"📦 Size: {size:.2f} MB")
            
            self.single_status.value = "Completed!"
            self.single_status.color = ft.colors.GREEN
            self.show_snackbar("Processing completed!", ft.colors.GREEN)
            
        except subprocess.CalledProcessError:
            self.log_message(self.single_log, "\n❌ FFmpeg error!", ft.colors.RED)
            self.single_status.value = "Error"
            self.single_status.color = ft.colors.RED
            self.show_snackbar("Processing failed!", ft.colors.RED)
        except Exception as e:
            self.log_message(self.single_log, f"\n❌ Error: {e}", ft.colors.RED)
            self.single_status.value = "Error"
            self.single_status.color = ft.colors.RED
        finally:
            self.processing = False
            self.page.update()
    
    def process_alternating_loop(self):
        """Process alternating loop in thread"""
        if self.processing:
            self.show_snackbar("Already processing!", ft.colors.ORANGE)
            return
        
        file_a = self.alt_file_a.value
        file_b = self.alt_file_b.value
        
        if not file_a or not os.path.exists(file_a):
            self.show_error("Select File A!")
            return
        
        if not file_b or not os.path.exists(file_b):
            self.show_error("Select File B!")
            return
        
        # Check extensions
        ext_a = os.path.splitext(file_a)[1]
        ext_b = os.path.splitext(file_b)[1]
        if ext_a != ext_b:
            self.show_warning(f"Different formats: {ext_a} vs {ext_b}\nMay cause errors!")
        
        try:
            count = int(self.alt_loop_count.value)
            if count < 1:
                self.show_error("Loop count must be >= 1")
                return
        except ValueError:
            self.show_error("Invalid loop count!")
            return
        
        try:
            delay = float(self.alt_delay.value)
            if delay < 0:
                self.show_error("Delay must be >= 0")
                return
        except ValueError:
            self.show_error("Invalid delay value!")
            return
        
        thread = threading.Thread(target=self._process_alternating_worker, args=(file_a, file_b, count, delay))
        thread.daemon = True
        thread.start()
    
    def _process_alternating_worker(self, file_a, file_b, count, delay=0):
        """Worker thread for alternating loop"""
        self.processing = True
        self.alt_status.value = "Processing..."
        self.alt_status.color = ft.colors.BLUE
        self.alt_log.controls.clear()
        self.page.update()
        
        list_file = "temp_concat_list.txt"
        silence_file = None
        
        try:
            # Generate silence file if delay > 0
            if delay > 0:
                self.log_message(self.alt_log, f"⏳ Generating {delay}s silence...")
                silence_file = self.generate_silence(file_a, delay)
                if not silence_file:
                    raise Exception("Failed to generate silence file")
                self.log_message(self.alt_log, f"✓ Silence file created")
            
            # Duration info
            dur_a = self.get_duration(file_a)
            dur_b = self.get_duration(file_b)
            if dur_a and dur_b:
                pair = dur_a + dur_b + delay
                total = pair * count
                delay_str = f" + Delay: {delay}s" if delay > 0 else ""
                self.log_message(self.alt_log,
                    f"📊 A: {self.format_duration(dur_a)}{delay_str} + B: {self.format_duration(dur_b)} = {self.format_duration(pair)}")
                self.log_message(self.alt_log, f"   Total: {self.format_duration(total)} ({count} sets)")
            
            # Create concat list
            abs_a = os.path.abspath(file_a).replace(os.sep, '/')
            abs_b = os.path.abspath(file_b).replace(os.sep, '/')
            
            self.log_message(self.alt_log, f"\nFile A: {os.path.basename(file_a)}")
            self.log_message(self.alt_log, f"File B: {os.path.basename(file_b)}")
            pattern = f"A-[{delay}s]-B" if delay > 0 else "A-B"
            self.log_message(self.alt_log, f"Pattern: {pattern} × {count} sets")
            
            # Create concat list with optional silence
            with open(list_file, 'w', encoding='utf-8') as f:
                for _ in range(count):
                    f.write(f"file '{abs_a}'\n")
                    if silence_file:
                        abs_silence = os.path.abspath(silence_file).replace(os.sep, '/')
                        f.write(f"file '{abs_silence}'\n")
                    f.write(f"file '{abs_b}'\n")
            
            # Prepare output
            filename, ext = os.path.splitext(file_a)
            output_file = f"{filename}_merged_{count}x{ext}"
            
            self.log_message(self.alt_log, f"\n⚙️ FFmpeg processing...", ft.colors.BLUE)
            
            # FFmpeg command
            cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file,
                   '-c', 'copy', output_file, '-y']
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            size = os.path.getsize(output_file) / (1024 * 1024)
            self.log_message(self.alt_log, f"\n✅ SUCCESS!", ft.colors.GREEN)
            self.log_message(self.alt_log, f"📁 {output_file}")
            self.log_message(self.alt_log, f"📦 Size: {size:.2f} MB")
            
            self.alt_status.value = "Completed!"
            self.alt_status.color = ft.colors.GREEN
            self.show_snackbar("Processing completed!", ft.colors.GREEN)
            
        except subprocess.CalledProcessError:
            self.log_message(self.alt_log, "\n❌ FFmpeg error! Check codec compatibility.", ft.colors.RED)
            self.alt_status.value = "Error"
            self.alt_status.color = ft.colors.RED
            self.show_snackbar("Processing failed!", ft.colors.RED)
        except Exception as e:
            self.log_message(self.alt_log, f"\n❌ Error: {e}", ft.colors.RED)
            self.alt_status.value = "Error"
            self.alt_status.color = ft.colors.RED
        finally:
            # Cleanup temp files
            if os.path.exists(list_file):
                os.remove(list_file)
            if silence_file and os.path.exists(silence_file):
                os.remove(silence_file)
            self.processing = False
            self.page.update()
    
    def show_error(self, message):
        """Show error dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
        )
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def show_warning(self, message):
        """Show warning dialog"""
        def close_dialog(e):
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Warning"),
            content=ft.Text(message),
            actions=[ft.TextButton("OK", on_click=close_dialog)],
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
    MediaLooperGUI(page)


if __name__ == "__main__":
    ft.app(target=main)
