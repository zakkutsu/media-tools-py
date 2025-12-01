"""
Media Looper - GUI Version
Loop video/audio files using FFmpeg stream copy with graphical interface

Author: Media Tools Suite
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import os
import sys
import shutil
import threading
from pathlib import Path

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False
    print("Warning: tkinterdnd2 not available. Drag & drop disabled.")


class MediaLooperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Looper Tool")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Variables
        self.input_file = tk.StringVar()
        self.loop_count = tk.StringVar(value="60")
        self.processing = False
        
        # Check FFmpeg
        if not self.check_ffmpeg():
            messagebox.showerror(
                "FFmpeg Not Found",
                "FFmpeg tidak ditemukan!\n\n"
                "Pastikan FFmpeg sudah terinstall dan ada di system PATH.\n"
                "Download: https://ffmpeg.org/download.html"
            )
        
        self.setup_ui()
        
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        return shutil.which('ffmpeg') is not None
    
    def setup_ui(self):
        """Setup the GUI interface"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="🔁 Media Looper Tool",
            font=("Segoe UI", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Loop Video/Audio tanpa Re-encoding (Stream Copy)",
            font=("Segoe UI", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Info box
        info_frame = tk.LabelFrame(main_frame, text="ℹ️ Cara Kerja", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = (
            "• Stream Copy: Menjahit data binary tanpa re-encoding\n"
            "• Proses INSTANT: Detikan untuk hasil berjam-jam\n"
            "• Quality IDENTIK: Zero quality loss\n"
            "• Contoh: MP3 3 menit × 20 loop = 60 menit dalam ~2 detik"
        )
        info_label = tk.Label(info_frame, text=info_text, font=("Segoe UI", 9), justify=tk.LEFT, fg="#34495e")
        info_label.pack()
        
        # Input file section
        input_frame = tk.LabelFrame(main_frame, text="📂 Input File", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_entry_frame = tk.Frame(input_frame)
        file_entry_frame.pack(fill=tk.X)
        
        self.file_entry = tk.Entry(
            file_entry_frame,
            textvariable=self.input_file,
            font=("Segoe UI", 10),
            state="readonly",
            bg="white"
        )
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        browse_btn = tk.Button(
            file_entry_frame,
            text="Browse",
            command=self.browse_file,
            font=("Segoe UI", 9),
            bg="#3498db",
            fg="white",
            cursor="hand2",
            width=10
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Drag & drop hint
        if DND_AVAILABLE:
            dnd_label = tk.Label(
                input_frame,
                text="💡 Atau drag & drop file ke sini",
                font=("Segoe UI", 9, "italic"),
                fg="#7f8c8d"
            )
            dnd_label.pack(pady=(5, 0))
            
            # Enable drag & drop
            self.file_entry.drop_target_register(DND_FILES)
            self.file_entry.dnd_bind('<<Drop>>', self.on_drop)
        
        # Loop count section
        loop_frame = tk.LabelFrame(main_frame, text="🔁 Pengaturan Loop", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        loop_frame.pack(fill=tk.X, pady=(0, 10))
        
        loop_input_frame = tk.Frame(loop_frame)
        loop_input_frame.pack(fill=tk.X)
        
        loop_label = tk.Label(loop_input_frame, text="Jumlah loop:", font=("Segoe UI", 10))
        loop_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.loop_entry = tk.Entry(
            loop_input_frame,
            textvariable=self.loop_count,
            font=("Segoe UI", 10),
            width=10
        )
        self.loop_entry.pack(side=tk.LEFT)
        
        loop_hint = tk.Label(
            loop_input_frame,
            text="(Total durasi = Durasi asli × Jumlah loop)",
            font=("Segoe UI", 9, "italic"),
            fg="#7f8c8d"
        )
        loop_hint.pack(side=tk.LEFT, padx=(10, 0))
        
        # Quick presets
        preset_frame = tk.Frame(loop_frame)
        preset_frame.pack(fill=tk.X, pady=(5, 0))
        
        preset_label = tk.Label(preset_frame, text="Preset:", font=("Segoe UI", 9))
        preset_label.pack(side=tk.LEFT, padx=(0, 5))
        
        for preset in [10, 20, 30, 60, 120]:
            btn = tk.Button(
                preset_frame,
                text=f"{preset}x",
                command=lambda p=preset: self.loop_count.set(str(p)),
                font=("Segoe UI", 8),
                width=5
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Process button
        self.process_btn = tk.Button(
            main_frame,
            text="⚡ Process",
            command=self.process_file,
            font=("Segoe UI", 12, "bold"),
            bg="#27ae60",
            fg="white",
            cursor="hand2",
            height=2
        )
        self.process_btn.pack(fill=tk.X, pady=(10, 10))
        
        # Progress section
        progress_frame = tk.LabelFrame(main_frame, text="📊 Status", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
        progress_frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_text = tk.Text(
            progress_frame,
            font=("Consolas", 9),
            height=8,
            bg="#ecf0f1",
            state="disabled",
            wrap=tk.WORD
        )
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        # Add initial message
        self.log_status("Ready. Pilih file dan klik Process untuk memulai.")
    
    def browse_file(self):
        """Browse for media file"""
        filetypes = [
            ("Media Files", "*.mp4 *.mkv *.avi *.mov *.mp3 *.wav *.aac *.flac *.m4a"),
            ("Video Files", "*.mp4 *.mkv *.avi *.mov *.webm *.flv"),
            ("Audio Files", "*.mp3 *.wav *.aac *.flac *.m4a *.ogg"),
            ("All Files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Pilih File Media",
            filetypes=filetypes
        )
        
        if filename:
            self.input_file.set(filename)
            self.log_status(f"File dipilih: {os.path.basename(filename)}")
    
    def on_drop(self, event):
        """Handle drag & drop"""
        files = self.root.tk.splitlist(event.data)
        if files:
            file_path = files[0].strip('{}')
            self.input_file.set(file_path)
            self.log_status(f"File di-drop: {os.path.basename(file_path)}")
    
    def log_status(self, message):
        """Add message to status text"""
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state="disabled")
        self.root.update()
    
    def clear_status(self):
        """Clear status text"""
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state="disabled")
    
    def validate_inputs(self):
        """Validate user inputs"""
        # Check file
        file_path = self.input_file.get()
        if not file_path:
            messagebox.showerror("Error", "Pilih file terlebih dahulu!")
            return False
        
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "File tidak ditemukan!")
            return False
        
        # Check loop count
        try:
            count = int(self.loop_count.get())
            if count < 1:
                messagebox.showerror("Error", "Jumlah loop minimal 1!")
                return False
            if count > 1000:
                if not messagebox.askyesno(
                    "Konfirmasi",
                    f"Loop {count}x akan menghasilkan file sangat besar.\n\nLanjutkan?"
                ):
                    return False
        except ValueError:
            messagebox.showerror("Error", "Masukkan angka yang valid untuk jumlah loop!")
            return False
        
        return True
    
    def get_duration(self, file_path):
        """Get media duration using FFprobe"""
        try:
            cmd = [
                'ffprobe',
                '-v', 'quiet',
                '-show_entries', 'format=duration',
                '-of', 'default=noprint_wrappers=1:nokey=1',
                file_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
            return float(result.stdout.strip())
        except:
            return None
    
    def format_duration(self, seconds):
        """Format seconds to HH:MM:SS"""
        if seconds is None:
            return "Unknown"
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        if hours > 0:
            return f"{hours}:{minutes:02d}:{secs:02d}"
        return f"{minutes}:{secs:02d}"
    
    def process_file(self):
        """Process the file in a separate thread"""
        if self.processing:
            messagebox.showwarning("Warning", "Proses sedang berjalan!")
            return
        
        if not self.validate_inputs():
            return
        
        # Run in thread to prevent UI freeze
        thread = threading.Thread(target=self.process_worker)
        thread.daemon = True
        thread.start()
    
    def process_worker(self):
        """Worker thread for processing"""
        self.processing = True
        self.process_btn.config(state="disabled", bg="#95a5a6")
        self.clear_status()
        
        input_file = self.input_file.get()
        loop_count = int(self.loop_count.get())
        
        # Prepare output path
        filename, ext = os.path.splitext(input_file)
        output_file = f"{filename}_looped_{loop_count}x{ext}"
        
        try:
            # Get duration info
            self.log_status("📊 Analyzing file...")
            duration = self.get_duration(input_file)
            if duration:
                total_duration = duration * loop_count
                self.log_status(f"Original: {self.format_duration(duration)}")
                self.log_status(f"Total: {self.format_duration(total_duration)} ({loop_count}x)")
            
            self.log_status(f"\n⚙️ Processing: {os.path.basename(input_file)}")
            self.log_status(f"Mode: Stream Copy (No Re-encoding)")
            self.log_status(f"Output: {os.path.basename(output_file)}")
            self.log_status("\n⏳ FFmpeg working...")
            
            # Build FFmpeg command
            ffmpeg_loop_count = loop_count - 1
            cmd = [
                'ffmpeg',
                '-stream_loop', str(ffmpeg_loop_count),
                '-i', input_file,
                '-c', 'copy',
                output_file,
                '-y'
            ]
            
            # Run FFmpeg
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Success
            output_size = os.path.getsize(output_file) / (1024 * 1024)
            self.log_status(f"\n✅ SUKSES!")
            self.log_status(f"📁 Output: {output_file}")
            self.log_status(f"📦 Size: {output_size:.2f} MB")
            
            messagebox.showinfo(
                "Success",
                f"File berhasil diproses!\n\n"
                f"Output: {os.path.basename(output_file)}\n"
                f"Size: {output_size:.2f} MB"
            )
            
        except subprocess.CalledProcessError as e:
            self.log_status(f"\n❌ Error: Processing failed")
            self.log_status("Possible causes:")
            self.log_status("- Corrupt file")
            self.log_status("- Unsupported format")
            self.log_status("- Insufficient disk space")
            messagebox.showerror("Error", "Gagal memproses file!\n\nCek log untuk detail.")
            
        except Exception as e:
            self.log_status(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error: {str(e)}")
        
        finally:
            self.processing = False
            self.process_btn.config(state="normal", bg="#27ae60")


def main():
    """Main entry point"""
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    
    app = MediaLooperGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
