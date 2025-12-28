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

# Compatibility layer for different Flet versions
# Flet 0.21.x uses ft.Icons/ft.Colors (uppercase)
# Flet 0.25.x uses ft.Icons/ft.Colors (lowercase)
try:
    # Try new style (0.25.x)
    _ = ft.Icons.LOOP
    icons = ft.Icons
    colors = ft.Colors
except AttributeError:
    # Fallback to old style (0.21.x)
    icons = ft.Icons
    colors = ft.Colors


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
                    ft.Icon(icons.LOOP, size=40, color=colors.WHITE),
                    ft.Text("Media Looper Tool", size=28, weight=ft.FontWeight.BOLD, color=colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Text("Stream Copy Looping - Instant Processing", 
                       size=14, color=colors.WHITE70, text_align=ft.TextAlign.CENTER),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            bgcolor=colors.TEAL_700,
            padding=20,
        )
        
        # Tabs
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Single Loop",
                    icon=icons.REPEAT,
                    content=self.create_single_loop_tab()
                ),
                ft.Tab(
                    text="Alternating Loop",
                    icon=icons.SWAP_HORIZ,
                    content=self.create_alternating_loop_tab()
                ),
            ],
            expand=1,
        )
        
        # Footer (will be added to each tab's content)
        self.footer = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=colors.TEAL_700),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=icons.FACEBOOK,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Facebook"
                        ),
                        ft.IconButton(
                            icon=icons.CAMERA_ALT,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Instagram"
                        ),
                        ft.IconButton(
                            icon=icons.EMAIL,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Email"
                        ),
                        ft.IconButton(
                            icon=icons.PHONE,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Phone"
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                ft.Text(
                    "© 2025 Media Tools Suite. All rights reserved.",
                    size=11,
                    color=colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=colors.TEAL_800,  # Darker teal for light theme
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
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
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.single_file),
        )
        
        # Output folder
        self.single_output_folder = ft.TextField(
            label="Output Folder",
            hint_text="Same as input folder",
            read_only=True,
            expand=True,
        )
        
        browse_output_btn = ft.ElevatedButton(
            "Browse",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_folder(self.single_output_folder),
        )
        
        # Output filename
        self.single_output_name = ft.TextField(
            label="Output Filename (without extension)",
            hint_text="Auto: input_looped_NNx",
            expand=True,
        )
        
        # Output format
        self.single_output_format = ft.Dropdown(
            label="Output Format",
            hint_text="Auto (same as input)",
            options=[
                ft.dropdown.Option("auto", "Auto (same as input)"),
                ft.dropdown.Option("video", "Video (.mp4)"),
                ft.dropdown.Option("audio", "Audio (.mp3)"),
            ],
            value="auto",
            width=200,
        )
        
        # Background image for audio->video
        self.single_bg_image = ft.TextField(
            label="Background Image (for audio→video)",
            hint_text="Default: bg/bg.png",
            read_only=True,
            expand=True,
        )
        
        browse_bg_btn = ft.ElevatedButton(
            "Browse",
            icon=icons.IMAGE,
            on_click=lambda _: self.browse_image(self.single_bg_image),
        )
        
        use_default_bg_btn = ft.TextButton(
            "Use Default BG",
            on_click=lambda _: self.set_default_bg(self.single_bg_image),
        )
        
        # Duration display
        self.single_duration_display = ft.Container(
            content=ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("No file selected", size=11, color=colors.GREY_600),
            ], spacing=2),
            bgcolor=colors.GREY_50,
            padding=10,
            border_radius=5,
        )
        
        # Loop count
        self.single_loop_count = ft.TextField(
            label="Loop Count",
            hint_text="e.g., 60",
            value="60",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda _: self.update_single_duration(),
        )
        
        # Presets
        presets = ft.Row([
            ft.Text("Quick:", size=12, color=colors.GREY_600),
            *[ft.FilledButton(
                f"{p}x",
                on_click=lambda e, count=p: (setattr(self.single_loop_count, 'value', str(count)), self.update_single_duration(), self.page.update())[-1],
                style=ft.ButtonStyle(padding=8),
            ) for p in [10, 20, 30, 60, 120]]
        ], spacing=5)
        
        # Process button
        process_btn = ft.ElevatedButton(
            "⚡ Process",
            icon=icons.PLAY_ARROW,
            on_click=lambda _: self.process_single_loop(),
            bgcolor=colors.TEAL_600,
            color=colors.WHITE,
            height=50,
        )
        
        # Status
        self.single_status = ft.Text("Ready", size=12, color=colors.GREY_600)
        self.single_progress = ft.ProgressBar(width=400, value=0, visible=False)
        self.single_progress_text = ft.Text("", size=11, color=colors.BLUE_700, visible=False)
        self.single_log = ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        
        # Create footer for this tab
        footer = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=colors.TEAL_700),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=icons.FACEBOOK,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Facebook"
                        ),
                        ft.IconButton(
                            icon=icons.CAMERA_ALT,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Instagram"
                        ),
                        ft.IconButton(
                            icon=icons.EMAIL,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Email"
                        ),
                        ft.IconButton(
                            icon=icons.PHONE,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Phone"
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                ft.Text(
                    "© 2025 Media Tools Suite. All rights reserved.",
                    size=11,
                    color=colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=colors.TEAL_800,
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Text("📝 Info", size=14, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            "• Loop 1 file berkali-kali (A-A-A...)\n"
                            "• Stream copy = instant, zero quality loss\n"
                            "• Contoh: 3 menit MP3 × 20 = 60 menit dalam 2 detik",
                            size=12, color=colors.GREY_700,
                        ),
                    ], spacing=5),
                    bgcolor=colors.BLUE_50,
                    padding=15,
                    border_radius=10,
                ),
                ft.Divider(),
                ft.Text("Input File", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.single_file, browse_btn], spacing=10),
                self.single_duration_display,
                ft.Divider(),
                ft.Text("Loop Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.single_loop_count, presets], spacing=20),
                ft.Divider(),
                ft.Text("Output Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.single_output_folder, browse_output_btn], spacing=10),
                self.single_output_name,
                ft.Row([self.single_output_format], spacing=10),
                ft.Row([self.single_bg_image, browse_bg_btn, use_default_bg_btn], spacing=10),
                ft.Divider(),
                process_btn,
                ft.Divider(),
                ft.Text("Status", size=14, weight=ft.FontWeight.BOLD),
                self.single_status,
                self.single_progress,
                self.single_progress_text,
                ft.Container(
                    content=self.single_log,
                    bgcolor=colors.GREY_100,
                    padding=10,
                    border_radius=5,
                    expand=True,
                ),
                footer,  # Footer inside scrollable content
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
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.alt_file_a),
        )
        
        browse_b_btn = ft.ElevatedButton(
            "Browse B",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_file(self.alt_file_b),
        )
        
        # Output folder
        self.alt_output_folder = ft.TextField(
            label="Output Folder",
            hint_text="Same as File A folder",
            read_only=True,
            expand=True,
        )
        
        browse_alt_output_btn = ft.ElevatedButton(
            "Browse",
            icon=icons.FOLDER_OPEN,
            on_click=lambda _: self.browse_folder(self.alt_output_folder),
        )
        
        # Output filename
        self.alt_output_name = ft.TextField(
            label="Output Filename (without extension)",
            hint_text="Auto: fileA_fileB_alt_NNx",
            expand=True,
        )
        
        # Output format
        self.alt_output_format = ft.Dropdown(
            label="Output Format",
            hint_text="Auto (same as input)",
            options=[
                ft.dropdown.Option("auto", "Auto (same as input)"),
                ft.dropdown.Option("video", "Video (.mp4)"),
                ft.dropdown.Option("audio", "Audio (.mp3)"),
            ],
            value="auto",
            width=200,
        )
        
        # Background image
        self.alt_bg_image = ft.TextField(
            label="Background Image (for audio→video)",
            hint_text="Default: bg/bg.png",
            read_only=True,
            expand=True,
        )
        
        browse_alt_bg_btn = ft.ElevatedButton(
            "Browse",
            icon=icons.IMAGE,
            on_click=lambda _: self.browse_image(self.alt_bg_image),
        )
        
        use_default_alt_bg_btn = ft.TextButton(
            "Use Default BG",
            on_click=lambda _: self.set_default_bg(self.alt_bg_image),
        )
        
        # Duration display
        self.alt_duration_display = ft.Container(
            content=ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("No files selected", size=11, color=colors.GREY_600),
            ], spacing=2),
            bgcolor=colors.GREY_50,
            padding=10,
            border_radius=5,
        )
        
        # Loop count
        self.alt_loop_count = ft.TextField(
            label="Loop Count (Sets)",
            hint_text="e.g., 10",
            value="10",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            on_change=lambda _: self.update_alt_duration(),
        )
        
        # Presets
        presets = ft.Row([
            ft.Text("Quick:", size=12, color=colors.GREY_600),
            *[ft.FilledButton(
                f"{p}x",
                on_click=lambda e, count=p: (setattr(self.alt_loop_count, 'value', str(count)), self.update_alt_duration(), self.page.update())[-1],
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
            on_change=lambda _: self.update_alt_duration(),
        )
        
        delay_presets = ft.Row([
            ft.Text("Quick:", size=12, color=colors.GREY_600),
            *[ft.FilledButton(
                f"{p}s",
                on_click=lambda e, delay=p: (setattr(self.alt_delay, 'value', str(delay)), self.update_alt_duration(), self.page.update())[-1],
                style=ft.ButtonStyle(padding=8),
            ) for p in [0, 1, 2, 3, 5]]
        ], spacing=5)
        
        # Process button
        process_btn = ft.ElevatedButton(
            "⚡ Process",
            icon=icons.PLAY_ARROW,
            on_click=lambda _: self.process_alternating_loop(),
            bgcolor=colors.ORANGE_600,
            color=colors.WHITE,
            height=50,
        )
        
        # Status
        self.alt_status = ft.Text("Ready", size=12, color=colors.GREY_600)
        self.alt_progress = ft.ProgressBar(width=400, value=0, visible=False)
        self.alt_progress_text = ft.Text("", size=11, color=colors.BLUE_700, visible=False)
        self.alt_log = ft.Column([], scroll=ft.ScrollMode.AUTO, expand=True, spacing=5)
        
        # Create footer for this tab
        footer = ft.Container(
            content=ft.Column([
                ft.Divider(height=1, color=colors.TEAL_700),
                ft.Container(
                    content=ft.Row([
                        ft.IconButton(
                            icon=icons.FACEBOOK,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Facebook"
                        ),
                        ft.IconButton(
                            icon=icons.CAMERA_ALT,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Instagram"
                        ),
                        ft.IconButton(
                            icon=icons.EMAIL,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Email"
                        ),
                        ft.IconButton(
                            icon=icons.PHONE,
                            icon_color=colors.WHITE70,
                            icon_size=20,
                            tooltip="Phone"
                        ),
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    padding=ft.padding.only(top=10, bottom=5)
                ),
                ft.Text(
                    "© 2025 Media Tools Suite. All rights reserved.",
                    size=11,
                    color=colors.GREY_400,
                    text_align=ft.TextAlign.CENTER
                ),
            ], spacing=5, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=colors.TEAL_800,
            padding=ft.padding.only(top=10, bottom=10, left=20, right=20),
        )
        
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
                            size=12, color=colors.GREY_700,
                        ),
                    ], spacing=5),
                    bgcolor=colors.ORANGE_50,
                    padding=15,
                    border_radius=10,
                ),
                ft.Divider(),
                ft.Text("Input Files", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.alt_file_a, browse_a_btn], spacing=10),
                ft.Row([self.alt_file_b, browse_b_btn], spacing=10),
                self.alt_duration_display,
                ft.Divider(),
                ft.Text("Loop Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.alt_loop_count, presets], spacing=20),
                ft.Row([self.alt_delay, delay_presets], spacing=20),
                ft.Text("💡 Use delay for Q&A drill: Question → [pause] → Answer", 
                       size=11, color=colors.GREY_600, italic=True),
                ft.Divider(),
                ft.Text("Output Settings", size=14, weight=ft.FontWeight.BOLD),
                ft.Row([self.alt_output_folder, browse_alt_output_btn], spacing=10),
                self.alt_output_name,
                ft.Row([self.alt_output_format], spacing=10),
                ft.Row([self.alt_bg_image, browse_alt_bg_btn, use_default_alt_bg_btn], spacing=10),
                ft.Divider(),
                process_btn,
                ft.Divider(),
                ft.Text("Status", size=14, weight=ft.FontWeight.BOLD),
                self.alt_status,
                self.alt_progress,
                self.alt_progress_text,
                ft.Container(
                    content=self.alt_log,
                    bgcolor=colors.GREY_100,
                    padding=10,
                    border_radius=5,
                    expand=True,
                ),
                footer,  # Footer inside scrollable content
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            padding=20,
            expand=True,
        )
    
    def browse_file(self, target_field):
        """Browse file dialog"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                target_field.value = e.files[0].path
                # Update duration display after file selection
                if target_field == self.single_file:
                    self.update_single_duration()
                elif target_field == self.alt_file_a or target_field == self.alt_file_b:
                    self.update_alt_duration()
                self.page.update()
        
        file_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(file_picker)
        self.page.update()
        
        file_picker.pick_files(
            dialog_title="Select Media File",
            allowed_extensions=["mp4", "mkv", "avi", "mov", "mp3", "wav", "aac", "flac", "m4a"],
        )
    
    def browse_folder(self, target_field):
        """Browse folder dialog"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.path:
                target_field.value = e.path
                self.page.update()
        
        folder_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(folder_picker)
        self.page.update()
        
        folder_picker.get_directory_path(dialog_title="Select Output Folder")
    
    def browse_image(self, target_field):
        """Browse image file dialog"""
        def on_result(e: ft.FilePickerResultEvent):
            if e.files:
                target_field.value = e.files[0].path
                self.page.update()
        
        image_picker = ft.FilePicker(on_result=on_result)
        self.page.overlay.append(image_picker)
        self.page.update()
        
        image_picker.pick_files(
            dialog_title="Select Background Image",
            allowed_extensions=["jpg", "jpeg", "png", "bmp", "webp"],
        )
    
    def set_default_bg(self, target_field):
        """Set default background image"""
        default_bg = os.path.join(os.path.dirname(__file__), "bg", "bg.png")
        if os.path.exists(default_bg):
            target_field.value = default_bg
            self.show_snackbar("Default BG set!", colors.GREEN)
        else:
            self.show_snackbar("Default BG not found!", colors.RED)
        self.page.update()
    
    def update_single_duration(self):
        """Update single loop duration display"""
        file_path = self.single_file.value
        if not file_path or not os.path.exists(file_path):
            self.single_duration_display.content = ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("No file selected", size=11, color=colors.GREY_600),
            ], spacing=2)
            self.page.update()
            return
        
        duration = self.get_duration(file_path)
        if duration:
            try:
                count = int(self.single_loop_count.value) if self.single_loop_count.value else 1
                total_duration = duration * count
                
                self.single_duration_display.content = ft.Column([
                    ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"File: {self.format_duration(duration)}", size=11, color=colors.BLUE_700),
                    ft.Text(f"Loop: {count}x", size=11, color=colors.BLUE_700),
                    ft.Text(f"Total: {self.format_duration(total_duration)}", size=13, weight=ft.FontWeight.BOLD, color=colors.GREEN_700),
                ], spacing=2)
            except:
                self.single_duration_display.content = ft.Column([
                    ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"File: {self.format_duration(duration)}", size=11, color=colors.BLUE_700),
                ], spacing=2)
        else:
            self.single_duration_display.content = ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("Could not read duration", size=11, color=colors.ORANGE_600),
            ], spacing=2)
        
        self.page.update()
    
    def update_alt_duration(self):
        """Update alternating loop duration display"""
        file_a = self.alt_file_a.value
        file_b = self.alt_file_b.value
        
        if not file_a or not os.path.exists(file_a) or not file_b or not os.path.exists(file_b):
            self.alt_duration_display.content = ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("Select both files", size=11, color=colors.GREY_600),
            ], spacing=2)
            self.page.update()
            return
        
        dur_a = self.get_duration(file_a)
        dur_b = self.get_duration(file_b)
        
        if dur_a and dur_b:
            try:
                count = int(self.alt_loop_count.value) if self.alt_loop_count.value else 1
                delay = float(self.alt_delay.value) if self.alt_delay.value else 0
                pair_duration = dur_a + dur_b + delay
                total_duration = pair_duration * count
                
                delay_str = f" + Delay: {delay}s" if delay > 0 else ""
                
                self.alt_duration_display.content = ft.Column([
                    ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"File A: {self.format_duration(dur_a)}", size=11, color=colors.BLUE_700),
                    ft.Text(f"File B: {self.format_duration(dur_b)}{delay_str}", size=11, color=colors.BLUE_700),
                    ft.Text(f"Per Set: {self.format_duration(pair_duration)}", size=11, color=colors.BLUE_700),
                    ft.Text(f"Loop: {count}x sets", size=11, color=colors.BLUE_700),
                    ft.Text(f"Total: {self.format_duration(total_duration)}", size=13, weight=ft.FontWeight.BOLD, color=colors.GREEN_700),
                ], spacing=2)
            except:
                self.alt_duration_display.content = ft.Column([
                    ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"File A: {self.format_duration(dur_a)}", size=11, color=colors.BLUE_700),
                    ft.Text(f"File B: {self.format_duration(dur_b)}", size=11, color=colors.BLUE_700),
                ], spacing=2)
        else:
            self.alt_duration_display.content = ft.Column([
                ft.Text("Duration Calculation:", size=12, weight=ft.FontWeight.BOLD),
                ft.Text("Could not read duration", size=11, color=colors.ORANGE_600),
            ], spacing=2)
        
        self.page.update()
    
    def log_message(self, log_container, message, color=None):
        """Add log message"""
        log_container.controls.append(
            ft.Text(message, size=11, color=color or colors.BLACK87)
        )
        self.page.update()
    
    def update_progress(self, progress_bar, progress_text, percentage, step_text):
        """Update progress bar and text"""
        progress_bar.value = percentage / 100
        progress_bar.visible = True
        progress_text.value = f"{step_text} - {percentage}%"
        progress_text.visible = True
        self.page.update()
    
    def hide_progress(self, progress_bar, progress_text):
        """Hide progress bar"""
        progress_bar.visible = False
        progress_text.visible = False
        self.page.update()
    
    def run_ffmpeg_with_progress(self, cmd, total_duration, progress_bar, progress_text, step_text):
        """Run FFmpeg with progress tracking"""
        import re
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',  # Replace invalid characters instead of failing
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        
        stderr_output = []
        for line in process.stderr:
            stderr_output.append(line)
            # Parse FFmpeg progress from stderr
            # Example: time=00:01:23.45
            time_match = re.search(r'time=(\d+):(\d+):(\d+\.\d+)', line)
            if time_match and total_duration and total_duration > 0:
                hours = int(time_match.group(1))
                minutes = int(time_match.group(2))
                seconds = float(time_match.group(3))
                current_time = hours * 3600 + minutes * 60 + seconds
                
                percentage = min(int((current_time / total_duration) * 100), 99)
                self.update_progress(progress_bar, progress_text, percentage, step_text)
        
        process.wait()
        
        if process.returncode != 0:
            error_msg = ''.join(stderr_output[-20:])  # Last 20 lines
            raise subprocess.CalledProcessError(process.returncode, cmd, stderr=error_msg)
        
        # Set to 100% when done
        self.update_progress(progress_bar, progress_text, 100, step_text)
        return process
    
    def get_duration(self, file_path):
        """Get media duration"""
        try:
            cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
                   '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', 
                                  errors='replace', check=True, timeout=10)
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
            
            subprocess.run(cmd, check=True, capture_output=True, text=True, 
                          encoding='utf-8', errors='replace', timeout=30)
            return silence_file
        except Exception as e:
            print(f"Error generating silence: {e}")
            return None
    
    def process_single_loop(self):
        """Process single loop in thread"""
        if self.processing:
            self.show_snackbar("Already processing!", colors.ORANGE)
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
        self.single_status.color = colors.BLUE
        self.single_log.controls.clear()
        self.page.update()
        
        temp_files = []
        
        try:
            # Duration info
            duration = self.get_duration(file_path)
            if duration:
                total = duration * count
                self.log_message(self.single_log, 
                    f"📊 Input Duration: {self.format_duration(duration)}")
                self.log_message(self.single_log, 
                    f"📊 Loop Count: {count}x")
                self.log_message(self.single_log, 
                    f"📊 Total Duration: {self.format_duration(total)}", colors.GREEN)
            
            # Determine output format and extension
            output_format = self.single_output_format.value or "auto"
            input_ext = os.path.splitext(file_path)[1].lower()
            is_input_video = input_ext in ['.mp4', '.mkv', '.avi', '.mov', '.webm']
            
            if output_format == "video":
                output_ext = ".mp4"
                needs_conversion = not is_input_video
            elif output_format == "audio":
                output_ext = ".mp3"
                needs_conversion = is_input_video
            else:  # auto
                output_ext = input_ext
                needs_conversion = False
            
            # Determine output folder
            if self.single_output_folder.value:
                output_folder = self.single_output_folder.value
            else:
                output_folder = os.path.dirname(file_path)
            
            # Determine output filename
            if self.single_output_name.value and self.single_output_name.value.strip():
                filename = self.single_output_name.value.strip()
            else:
                filename = os.path.splitext(os.path.basename(file_path))[0]
                filename = f"{filename}_looped_{count}x"
            
            output_file = os.path.join(output_folder, f"{filename}{output_ext}")
            
            self.log_message(self.single_log, f"\nInput: {os.path.basename(file_path)}")
            self.log_message(self.single_log, f"Output: {os.path.basename(output_file)}")
            
            # Step 1: Loop the file
            self.log_message(self.single_log, "\n⚙️ Step 1: Looping...", colors.BLUE)
            temp_looped = f"temp_looped_{count}x{input_ext}"
            temp_files.append(temp_looped)
            
            loop_count = count - 1
            cmd = ['ffmpeg', '-stream_loop', str(loop_count), '-i', file_path,
                   '-c', 'copy', '-progress', 'pipe:2', temp_looped, '-y']
            
            # Use progress tracking for looping (stream copy is instant, so this is mostly for show)
            total_dur = duration * count if duration else None
            self.run_ffmpeg_with_progress(cmd, total_dur, self.single_progress, 
                                         self.single_progress_text, "Looping")
            self.log_message(self.single_log, "✓ Looping complete", colors.GREEN)
            
            # Step 2: Convert if needed
            if needs_conversion:
                self.log_message(self.single_log, "\n⚙️ Step 2: Converting format...", colors.BLUE)
                
                if output_format == "video" and not is_input_video:
                    # Audio to Video - need background image
                    bg_image = self.single_bg_image.value
                    if not bg_image:
                        bg_image = os.path.join(os.path.dirname(__file__), "bg", "bg.png")
                    
                    if not os.path.exists(bg_image):
                        raise Exception("Background image not found! Please select a background image.")
                    
                    self.log_message(self.single_log, f"Using BG: {os.path.basename(bg_image)}")
                    
                    cmd = ['ffmpeg', '-loop', '1', '-i', bg_image, '-i', temp_looped,
                           '-c:v', 'libx264', '-tune', 'stillimage', '-c:a', 'aac',
                           '-b:a', '192k', '-pix_fmt', 'yuv420p', '-shortest',
                           '-progress', 'pipe:2', output_file, '-y']
                else:
                    # Video to Audio
                    cmd = ['ffmpeg', '-i', temp_looped, '-vn', '-c:a', 'libmp3lame',
                           '-b:a', '192k', '-progress', 'pipe:2', output_file, '-y']
                
                # Use progress tracking for conversion
                total_dur = duration * count if duration else None
                self.run_ffmpeg_with_progress(cmd, total_dur, self.single_progress,
                                             self.single_progress_text, "Converting")
                self.log_message(self.single_log, "✓ Conversion complete", colors.GREEN)
            else:
                # No conversion needed, just move
                import shutil
                shutil.move(temp_looped, output_file)
                temp_files.remove(temp_looped)
            
            # Hide progress bar
            self.hide_progress(self.single_progress, self.single_progress_text)
            
            size = os.path.getsize(output_file) / (1024 * 1024)
            self.log_message(self.single_log, f"\n✅ SUCCESS!", colors.GREEN)
            self.log_message(self.single_log, f"📁 {output_file}")
            self.log_message(self.single_log, f"📦 Size: {size:.2f} MB")
            
            self.single_status.value = "Completed!"
            self.single_status.color = colors.GREEN
            self.show_snackbar("Processing completed!", colors.GREEN)
            
        except subprocess.CalledProcessError as e:
            self.hide_progress(self.single_progress, self.single_progress_text)
            self.log_message(self.single_log, "\n❌ FFmpeg error!", colors.RED)
            error_msg = "Unknown error"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg = str(e.stderr)
            elif hasattr(e, 'output') and e.output:
                error_msg = str(e.output)
            self.log_message(self.single_log, error_msg, colors.RED)
            self.single_status.value = "Error"
            self.single_status.color = colors.RED
            self.show_snackbar("Processing failed! Check FFmpeg installation.", colors.RED)
        except Exception as e:
            self.hide_progress(self.single_progress, self.single_progress_text)
            self.log_message(self.single_log, f"\n❌ Error: {e}", colors.RED)
            self.single_status.value = "Error"
            self.single_status.color = colors.RED
        finally:
            # Cleanup temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    try:
                        os.remove(temp_file)
                    except:
                        pass
            self.hide_progress(self.single_progress, self.single_progress_text)
            self.processing = False
            self.page.update()
    
    def process_alternating_loop(self):
        """Process alternating loop in thread"""
        if self.processing:
            self.show_snackbar("Already processing!", colors.ORANGE)
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
        self.alt_status.color = colors.BLUE
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
            with open(list_file, 'w', encoding='utf-8', newline='') as f:
                for _ in range(count):
                    f.write(f"file '{abs_a}'\n")
                    if silence_file:
                        abs_silence = os.path.abspath(silence_file).replace(os.sep, '/')
                        f.write(f"file '{abs_silence}'\n")
                    f.write(f"file '{abs_b}'\n")
            
            # Prepare output
            ext = os.path.splitext(file_a)[1]
            
            # Determine output folder
            if self.alt_output_folder.value:
                output_folder = self.alt_output_folder.value
            else:
                output_folder = os.path.dirname(file_a)
            
            # Determine output filename
            if self.alt_output_name.value and self.alt_output_name.value.strip():
                filename = self.alt_output_name.value.strip()
            else:
                name_a = os.path.splitext(os.path.basename(file_a))[0]
                name_b = os.path.splitext(os.path.basename(file_b))[0]
                filename = f"{name_a}_{name_b}_alt_{count}x"
            
            output_file = os.path.join(output_folder, f"{filename}{ext}")
            
            self.log_message(self.alt_log, f"Output: {os.path.basename(output_file)}")
            self.log_message(self.alt_log, f"\n⚙️ FFmpeg processing...", colors.BLUE)
            
            # FFmpeg command with progress
            cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file,
                   '-c', 'copy', '-progress', 'pipe:2', output_file, '-y']
            
            # Calculate total duration for progress tracking
            total_dur = (dur_a + dur_b + delay) * count if dur_a and dur_b else None
            self.run_ffmpeg_with_progress(cmd, total_dur, self.alt_progress,
                                         self.alt_progress_text, "Merging")
            
            # Hide progress bar
            self.hide_progress(self.alt_progress, self.alt_progress_text)
            
            size = os.path.getsize(output_file) / (1024 * 1024)
            self.log_message(self.alt_log, f"\n✅ SUCCESS!", colors.GREEN)
            self.log_message(self.alt_log, f"📁 {output_file}")
            self.log_message(self.alt_log, f"📦 Size: {size:.2f} MB")
            
            self.alt_status.value = "Completed!"
            self.alt_status.color = colors.GREEN
            self.show_snackbar("Processing completed!", colors.GREEN)
            
        except subprocess.CalledProcessError as e:
            self.hide_progress(self.alt_progress, self.alt_progress_text)
            self.log_message(self.alt_log, "\n❌ FFmpeg error! Check codec compatibility.", colors.RED)
            error_msg = "Unknown error"
            if hasattr(e, 'stderr') and e.stderr:
                error_msg = str(e.stderr)
            elif hasattr(e, 'output') and e.output:
                error_msg = str(e.output)
            self.log_message(self.alt_log, f"Error details: {error_msg}", colors.RED)
            self.alt_status.value = "Error"
            self.alt_status.color = colors.RED
            self.show_snackbar("Processing failed! Check codec compatibility.", colors.RED)
        except Exception as e:
            self.hide_progress(self.alt_progress, self.alt_progress_text)
            self.log_message(self.alt_log, f"\n❌ Error: {e}", colors.RED)
            self.alt_status.value = "Error"
            self.alt_status.color = colors.RED
        finally:
            # Cleanup temp files
            if os.path.exists(list_file):
                os.remove(list_file)
            if silence_file and os.path.exists(silence_file):
                os.remove(silence_file)
            self.hide_progress(self.alt_progress, self.alt_progress_text)
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





