#!/usr/bin/env python3
"""
GUI untuk YouTube Playlist Downloader
Interface grafis menggunakan tkinter untuk memudahkan penggunaan
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import queue

# Import our playlist downloader
from playlist_downloader import PlaylistDownloader


class PlaylistDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 YouTube Playlist Downloader")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize downloader
        self.downloader = PlaylistDownloader()
        
        # Queue for thread communication
        self.output_queue = queue.Queue()
        
        # Variables
        self.download_folder = tk.StringVar()
        self.playlist_url = tk.StringVar()
        self.download_type = tk.StringVar(value="video_best")
        self.output_template = tk.StringVar(value="%(playlist_index)s - %(title)s.%(ext)s")
        self.auto_numbering = tk.BooleanVar(value=True)
        
        # Set default download folder
        self.download_folder.set(os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Downloads"))
        
        self.setup_ui()
        self.check_output_queue()
    
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame with scrollbar
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack scrollbar and canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main content frame
        main_frame = ttk.Frame(scrollable_frame, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Configure grid weights
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="🎵 YouTube Playlist Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # yt-dlp status
        self.ytdlp_status_frame = ttk.Frame(main_frame)
        self.ytdlp_status_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.ytdlp_status_label = ttk.Label(self.ytdlp_status_frame, text="Checking yt-dlp status...")
        self.ytdlp_status_label.pack(side=tk.LEFT)
        
        self.install_update_btn = ttk.Button(self.ytdlp_status_frame, text="Install/Update yt-dlp",
                                           command=self.install_update_ytdlp)
        self.install_update_btn.pack(side=tk.RIGHT)
        
        # Update yt-dlp status
        self.update_ytdlp_status()
        
        # Download folder section
        ttk.Label(main_frame, text="📁 Download Folder:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.download_folder, width=50)
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1)
        
        # Playlist URL section
        ttk.Label(main_frame, text="🔗 Playlist URL:").grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        
        url_frame = ttk.Frame(main_frame)
        url_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        url_frame.columnconfigure(0, weight=1)
        
        self.url_entry = ttk.Entry(url_frame, textvariable=self.playlist_url, width=50)
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(url_frame, text="Get Info", command=self.get_playlist_info).grid(row=0, column=1)
        
        # Playlist info display
        self.info_label = ttk.Label(main_frame, text="", foreground="blue")
        self.info_label.grid(row=6, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        
        # Download options section
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Download Options", padding="10")
        options_frame.grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        options_frame.columnconfigure(0, weight=1)
        
        # Download type
        ttk.Label(options_frame, text="Download Type:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        type_frame = ttk.Frame(options_frame)
        type_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Radiobutton(type_frame, text="🎬 Video (Best Quality)", 
                       variable=self.download_type, value="video_best").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="🎬 Video (720p - Save Bandwidth)", 
                       variable=self.download_type, value="video_720p").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="🎬 Video (480p - Save Bandwidth)", 
                       variable=self.download_type, value="video_480p").pack(anchor=tk.W)
        ttk.Radiobutton(type_frame, text="🎵 Audio Only (MP3)", 
                       variable=self.download_type, value="audio_mp3").pack(anchor=tk.W)
        
        # Output template
        ttk.Label(options_frame, text="File Naming Template:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        template_frame = ttk.Frame(options_frame)
        template_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        template_frame.columnconfigure(0, weight=1)
        
        self.template_entry = ttk.Entry(template_frame, textvariable=self.output_template)
        self.template_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(template_frame, text="Reset", command=self.reset_template).grid(row=0, column=1)
        
        # Help text for template
        help_text = "Template variables: %(playlist_index)s (number), %(title)s (title), %(ext)s (extension)"
        ttk.Label(options_frame, text=help_text, font=("Arial", 8), foreground="gray").grid(row=4, column=0, sticky=tk.W)
        
        # Auto numbering option
        auto_numbering_frame = ttk.Frame(options_frame)
        auto_numbering_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.auto_numbering_checkbox = ttk.Checkbutton(auto_numbering_frame, 
                                                      text="🔢 Enable Auto File Numbering (01 - Title.ext)", 
                                                      variable=self.auto_numbering,
                                                      command=self.on_auto_numbering_change)
        self.auto_numbering_checkbox.pack(anchor=tk.W)
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="🚀 Start Download", 
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=8, column=0, columnspan=3, pady=20)
        
        # Download progress section
        progress_section = ttk.LabelFrame(main_frame, text="📊 Download Progress", padding="10")
        progress_section.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        progress_section.columnconfigure(0, weight=1)
        
        # Progress label
        self.progress_label = ttk.Label(progress_section, text="Ready to download", 
                                       font=("Arial", 10, "bold"))
        self.progress_label.grid(row=0, column=0, pady=(0, 8))
        
        # Main progress bar (for playlist progress) - more prominent
        ttk.Label(progress_section, text="Playlist Progress:", font=("Arial", 9)).grid(row=1, column=0, sticky=tk.W, pady=(0, 2))
        self.overall_progress = ttk.Progressbar(progress_section, mode='determinate', length=400)
        self.overall_progress.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Current item progress bar (for individual song progress)
        ttk.Label(progress_section, text="Current Item Progress:", font=("Arial", 9)).grid(row=3, column=0, sticky=tk.W, pady=(0, 2))
        self.download_progress = ttk.Progressbar(progress_section, mode='indeterminate', length=400)
        self.download_progress.grid(row=4, column=0, sticky=(tk.W, tk.E))
        
        # General progress bar (old one for compatibility) - hidden by default
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress.grid_remove()  # Hide by default, only show during operations
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="📋 Output Log", padding="5")
        output_frame.grid(row=11, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=15, width=80)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame row weights
        main_frame.rowconfigure(11, weight=1)
        
        # Bind mouse wheel to canvas
        self.bind_mousewheel(canvas)
    
    def bind_mousewheel(self, canvas):
        """Bind mouse wheel to canvas for scrolling"""
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def _bind_to_mousewheel(event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        def _unbind_from_mousewheel(event):
            canvas.unbind_all("<MouseWheel>")
        
        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    def update_ytdlp_status(self):
        """Update yt-dlp status display"""
        if self.downloader.yt_dlp_available:
            self.ytdlp_status_label.config(text="✅ yt-dlp is available", foreground="green")
            self.install_update_btn.config(text="Update yt-dlp")
        else:
            self.ytdlp_status_label.config(text="❌ yt-dlp not found", foreground="red")
            self.install_update_btn.config(text="Install yt-dlp")
    
    def install_update_ytdlp(self):
        """Install or update yt-dlp in a separate thread"""
        def install_thread():
            self.log_output("Installing/Updating yt-dlp...")
            self.progress.grid()  # Show the general progress bar
            self.progress.start()
            self.install_update_btn.config(state="disabled")
            
            success = self.downloader.install_or_update_yt_dlp()
            
            self.progress.stop()
            self.progress.grid_remove()  # Hide again
            self.install_update_btn.config(state="normal")
            
            if success:
                self.log_output("✅ yt-dlp installed/updated successfully!")
                self.root.after(0, self.update_ytdlp_status)
            else:
                self.log_output("❌ Failed to install/update yt-dlp")
        
        threading.Thread(target=install_thread, daemon=True).start()
    
    def browse_folder(self):
        """Browse for download folder"""
        folder = filedialog.askdirectory(initialdir=self.download_folder.get())
        if folder:
            self.download_folder.set(folder)
    
    def reset_template(self):
        """Reset output template to default"""
        if self.auto_numbering.get():
            self.output_template.set("%(playlist_index)s - %(title)s.%(ext)s")
        else:
            self.output_template.set("%(title)s.%(ext)s")
    
    def on_auto_numbering_change(self):
        """Handle auto numbering checkbox change"""
        current_template = self.output_template.get()
        
        if self.auto_numbering.get():
            # Enable auto numbering - add playlist_index if not present
            if "%(playlist_index)s" not in current_template:
                if current_template.startswith("%(title)s"):
                    new_template = "%(playlist_index)s - " + current_template
                else:
                    new_template = "%(playlist_index)s - %(title)s.%(ext)s"
                self.output_template.set(new_template)
        else:
            # Disable auto numbering - remove only playlist_index, keep title
            new_template = current_template.replace("%(playlist_index)s - ", "")
            new_template = new_template.replace("%(playlist_index)s", "")
            # Clean up any double spaces
            new_template = " ".join(new_template.split())
            # Ensure we still have title in the template
            if "%(title)s" not in new_template or not new_template or new_template == ".%(ext)s":
                new_template = "%(title)s.%(ext)s"
            self.output_template.set(new_template)
    
    def get_playlist_info(self):
        """Get playlist information in a separate thread"""
        url = self.playlist_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a playlist URL first!")
            return
        
        def info_thread():
            self.log_output(f"Getting playlist info for: {url}")
            self.progress.grid()  # Show the general progress bar
            self.progress.start()
            
            info = self.downloader.get_playlist_info(url)
            
            self.progress.stop()
            self.progress.grid_remove()  # Hide again
            
            if info:
                info_text = f"📊 Found {info['total_videos']} videos in playlist"
                self.root.after(0, lambda: self.info_label.config(text=info_text))
                self.log_output(f"✅ {info_text}")
            else:
                self.root.after(0, lambda: self.info_label.config(text="❌ Failed to get playlist info"))
                self.log_output("❌ Failed to get playlist info. Check URL and internet connection.")
        
        threading.Thread(target=info_thread, daemon=True).start()
    
    def start_download(self):
        """Start download process in a separate thread"""
        # Validate inputs
        if not self.downloader.yt_dlp_available:
            messagebox.showerror("Error", "yt-dlp is not available. Please install it first!")
            return
        
        url = self.playlist_url.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a playlist URL!")
            return
        
        folder = self.download_folder.get().strip()
        if not folder:
            messagebox.showwarning("Warning", "Please select a download folder!")
            return
        
        # Set download folder
        if not self.downloader.set_download_folder(folder):
            messagebox.showerror("Error", f"Failed to create download folder: {folder}")
            return
        
        def download_thread():
            self.log_output("="*60)
            self.log_output("🚀 Starting download...")
            self.log_output(f"URL: {url}")
            self.log_output(f"Type: {self.download_type.get()}")
            self.log_output(f"Folder: {folder}")
            self.log_output("="*60)
            
            # Disable UI elements
            self.root.after(0, lambda: self.download_btn.config(state="disabled", text="Downloading..."))
            self.root.after(0, lambda: self.download_progress.start())  # Start current item progress animation
            self.root.after(0, lambda: self.reset_progress())
            
            success = False
            download_type = self.download_type.get()
            template = self.output_template.get() or "%(playlist_index)s - %(title)s.%(ext)s"
            auto_numbering = self.auto_numbering.get()
            
            self.log_output(f"Auto Numbering: {'Enabled' if auto_numbering else 'Disabled'}")
            
            try:
                if download_type == "video_best":
                    success = self.downloader.download_video_playlist(url, quality="best", output_template=template, auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "video_720p":
                    success = self.downloader.download_video_playlist(url, quality="720p", output_template=template, auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "video_480p":
                    success = self.downloader.download_video_playlist(url, quality="480p", output_template=template, auto_numbering=auto_numbering, progress_callback=self.update_progress)
                elif download_type == "audio_mp3":
                    success = self.downloader.download_audio_playlist(url, audio_format="mp3", output_template=template, auto_numbering=auto_numbering, progress_callback=self.update_progress)
            except Exception as e:
                self.log_output(f"❌ Error during download: {e}")
                success = False
            
            # Re-enable UI elements
            self.root.after(0, lambda: self.download_progress.stop())
            self.root.after(0, lambda: self.download_btn.config(state="normal", text="🚀 Start Download"))
            
            if success:
                self.log_output("="*60)
                self.log_output("🎉 Download completed successfully!")
                self.log_output(f"📁 Files saved to: {folder}")
                self.log_output("="*60)
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Download completed!\n\nFiles saved to:\n{folder}"))
            else:
                self.log_output("="*60)
                self.log_output("😞 Download failed!")
                self.log_output("Please check your internet connection and playlist URL.")
                self.log_output("="*60)
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    "Download failed!\n\nPlease check:\n- Internet connection\n- Playlist URL\n- Download folder permissions"))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def update_progress(self, current, total, percentage, title=""):
        """Update progress display"""
        def update_ui():
            # Update progress label
            if title:
                self.progress_label.config(text=f"🎵 [{current}/{total}] ({percentage:.1f}%) - {title}")
            else:
                self.progress_label.config(text=f"🎵 [{current}/{total}] ({percentage:.1f}%)")
            
            # Update overall progress bar
            self.overall_progress.config(value=percentage)
            
            # Update GUI
            self.root.update_idletasks()
        
        self.root.after(0, update_ui)
    
    def reset_progress(self):
        """Reset progress display"""
        def reset_ui():
            self.progress_label.config(text="Ready to download")
            self.download_progress.config(value=0)
            self.overall_progress.config(value=0)
        
        self.root.after(0, reset_ui)
    
    def log_output(self, message):
        """Add message to output log"""
        self.root.after(0, lambda: self._log_to_text(message))
    
    def _log_to_text(self, message):
        """Add message to text widget (must run in main thread)"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update_idletasks()
    
    def check_output_queue(self):
        """Check for messages from background threads"""
        try:
            while True:
                message = self.output_queue.get_nowait()
                self._log_to_text(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_output_queue)


def main():
    """Run the GUI application"""
    root = tk.Tk()
    
    # Set icon and styling
    try:
        # Try to set a nice style
        style = ttk.Style()
        style.theme_use('winnative' if sys.platform.startswith('win') else 'clam')
    except:
        pass
    
    app = PlaylistDownloaderGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()
