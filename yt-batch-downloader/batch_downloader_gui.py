#!/usr/bin/env python3
"""
GUI untuk YouTube Batch Downloader
Interface grafis untuk download multiple video individual YouTube
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path
import queue

# Import our batch downloader
from batch_downloader import BatchDownloader


class BatchDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Batch Downloader")
        self.root.geometry("900x750")
        self.root.resizable(True, True)
        
        # Initialize downloader
        self.downloader = BatchDownloader()
        
        # Queue for thread communication
        self.output_queue = queue.Queue()
        
        # Variables
        self.download_folder = tk.StringVar()
        self.download_type = tk.StringVar(value="video_best")
        self.output_template = tk.StringVar(value="%(title)s.%(ext)s")
        self.auto_numbering = tk.BooleanVar(value=False)
        self.continue_on_error = tk.BooleanVar(value=True)
        
        # Set default download folder
        self.download_folder.set(os.path.join(os.path.expanduser("~"), "Downloads", "YouTube_Batch"))
        
        self.setup_ui()
        self.check_output_queue()
        self.update_url_count()
    
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
        title_label = ttk.Label(main_frame, text="🎬 YouTube Batch Downloader", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Download multiple individual YouTube videos", 
                                  font=("Arial", 10), foreground="gray")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 20))
        
        # yt-dlp status
        self.ytdlp_status_frame = ttk.Frame(main_frame)
        self.ytdlp_status_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.ytdlp_status_label = ttk.Label(self.ytdlp_status_frame, text="Checking yt-dlp status...")
        self.ytdlp_status_label.pack(side=tk.LEFT)
        
        self.install_update_btn = ttk.Button(self.ytdlp_status_frame, text="Install/Update yt-dlp",
                                           command=self.install_update_ytdlp)
        self.install_update_btn.pack(side=tk.RIGHT)
        
        # Update yt-dlp status
        self.update_ytdlp_status()
        
        # Download folder section
        ttk.Label(main_frame, text="📁 Download Folder:").grid(row=3, column=0, sticky=tk.W, pady=(10, 5))
        
        folder_frame = ttk.Frame(main_frame)
        folder_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        folder_frame.columnconfigure(0, weight=1)
        
        self.folder_entry = ttk.Entry(folder_frame, textvariable=self.download_folder, width=60)
        self.folder_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        ttk.Button(folder_frame, text="Browse", command=self.browse_folder).grid(row=0, column=1)
        
        # URL Management section
        url_frame = ttk.LabelFrame(main_frame, text="🔗 URL Management", padding="10")
        url_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        url_frame.columnconfigure(0, weight=1)
        
        # URL input
        url_input_frame = ttk.Frame(url_frame)
        url_input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        url_input_frame.columnconfigure(0, weight=1)
        
        self.url_entry = tk.Entry(url_input_frame, width=60, font=("Arial", 10))
        self.url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.url_entry.bind('<Return>', lambda e: self.add_url())
        
        ttk.Button(url_input_frame, text="Add URL", command=self.add_url).grid(row=0, column=1)
        
        # URL management buttons
        url_btn_frame = ttk.Frame(url_frame)
        url_btn_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(url_btn_frame, text="📄 Load from File", command=self.load_urls_from_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(url_btn_frame, text="💾 Save to File", command=self.save_urls_to_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(url_btn_frame, text="🗑️ Clear All", command=self.clear_all_urls).pack(side=tk.LEFT, padx=(0, 5))
        
        self.url_count_label = ttk.Label(url_btn_frame, text="URLs: 0", font=("Arial", 10, "bold"))
        self.url_count_label.pack(side=tk.RIGHT)
        
        # URL List display
        ttk.Label(url_frame, text="URL List:").grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        # Create Treeview for URL list
        self.url_tree = ttk.Treeview(url_frame, columns=('URL', 'Status'), show='tree headings', height=8)
        self.url_tree.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Configure columns
        self.url_tree.heading('#0', text='#')
        self.url_tree.heading('URL', text='YouTube URL')
        self.url_tree.heading('Status', text='Status')
        
        self.url_tree.column('#0', width=50, minwidth=40)
        self.url_tree.column('URL', width=500, minwidth=300)
        self.url_tree.column('Status', width=100, minwidth=80)
        
        # URL list scrollbar
        url_scrollbar = ttk.Scrollbar(url_frame, orient="vertical", command=self.url_tree.yview)
        url_scrollbar.grid(row=3, column=2, sticky=(tk.N, tk.S))
        self.url_tree.configure(yscrollcommand=url_scrollbar.set)
        
        # URL list context menu
        self.url_tree.bind("<Button-3>", self.show_url_context_menu)
        
        # Download options section
        options_frame = ttk.LabelFrame(main_frame, text="⚙️ Download Options", padding="10")
        options_frame.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
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
        
        # Options checkboxes
        options_check_frame = ttk.Frame(options_frame)
        options_check_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.auto_numbering_checkbox = ttk.Checkbutton(options_check_frame, 
                                                      text="🔢 Auto Number Files (01 - Title.ext)", 
                                                      variable=self.auto_numbering,
                                                      command=self.on_auto_numbering_change)
        self.auto_numbering_checkbox.pack(anchor=tk.W)
        
        self.continue_on_error_checkbox = ttk.Checkbutton(options_check_frame, 
                                                         text="🔄 Continue on Error", 
                                                         variable=self.continue_on_error)
        self.continue_on_error_checkbox.pack(anchor=tk.W)
        
        # Help text
        help_text = "Template variables: %(title)s (title), %(ext)s (extension), %(uploader)s (channel)"
        ttk.Label(options_frame, text=help_text, font=("Arial", 8), foreground="gray").grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        
        # Download button
        self.download_btn = ttk.Button(main_frame, text="🚀 Start Batch Download", 
                                     command=self.start_download, style="Accent.TButton")
        self.download_btn.grid(row=7, column=0, columnspan=3, pady=20)
        
        # Download progress section
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        self.progress_frame.columnconfigure(0, weight=1)
        
        # Progress label
        self.progress_label = ttk.Label(self.progress_frame, text="Ready to download", 
                                       font=("Arial", 10))
        self.progress_label.grid(row=0, column=0, pady=(0, 5))
        
        # Overall progress bar (for batch progress)
        self.overall_progress = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.overall_progress.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # General progress bar (old one for compatibility)
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Output text area
        output_frame = ttk.LabelFrame(main_frame, text="📋 Download Log", padding="5")
        output_frame.grid(row=10, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        output_frame.columnconfigure(0, weight=1)
        output_frame.rowconfigure(0, weight=1)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=12, width=90)
        self.output_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure main frame row weights
        main_frame.rowconfigure(10, weight=1)
        
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
            self.progress.start()
            self.install_update_btn.config(state="disabled")
            
            success = self.downloader.install_or_update_yt_dlp()
            
            self.progress.stop()
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
    
    def add_url(self):
        """Add URL to the list"""
        url = self.url_entry.get().strip()
        if not url:
            return
        
        if self.downloader.add_url(url):
            # Add to treeview
            item_id = self.url_tree.insert('', 'end', text=str(len(self.downloader.url_list)), 
                                          values=(url, 'Ready'))
            
            self.url_entry.delete(0, tk.END)
            self.update_url_count()
            self.log_output(f"✅ URL added: {url}")
        else:
            messagebox.showwarning("Warning", "URL already exists or invalid!")
    
    def load_urls_from_file(self):
        """Load URLs from a text file"""
        file_path = filedialog.askopenfilename(
            title="Select URL file",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            added_count = self.downloader.add_urls_from_file(file_path)
            if added_count > 0:
                self.refresh_url_tree()
                self.log_output(f"✅ Loaded {added_count} URLs from file")
            else:
                messagebox.showwarning("Warning", "No valid URLs found in file!")
    
    def save_urls_to_file(self):
        """Save current URLs to a text file"""
        if not self.downloader.url_list:
            messagebox.showwarning("Warning", "No URLs to save!")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save URLs to file",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in self.downloader.url_list:
                        f.write(url + '\n')
                self.log_output(f"✅ URLs saved to: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
    
    def clear_all_urls(self):
        """Clear all URLs"""
        if self.downloader.url_list:
            result = messagebox.askyesno("Confirm", "Are you sure you want to clear all URLs?")
            if result:
                self.downloader.clear_url_list()
                self.refresh_url_tree()
                self.log_output("🗑️ All URLs cleared")
    
    def refresh_url_tree(self):
        """Refresh the URL tree display"""
        # Clear existing items
        for item in self.url_tree.get_children():
            self.url_tree.delete(item)
        
        # Add current URLs
        for i, url in enumerate(self.downloader.url_list, 1):
            status = 'Ready'
            if url in self.downloader.successful_downloads:
                status = 'Success'
            elif url in self.downloader.failed_downloads:
                status = 'Failed'
            
            self.url_tree.insert('', 'end', text=str(i), values=(url, status))
        
        self.update_url_count()
    
    def show_url_context_menu(self, event):
        """Show context menu for URL tree"""
        item = self.url_tree.selection()[0] if self.url_tree.selection() else None
        if item:
            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Remove URL", 
                                   command=lambda: self.remove_selected_url(item))
            context_menu.add_command(label="Copy URL", 
                                   command=lambda: self.copy_selected_url(item))
            
            try:
                context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                context_menu.grab_release()
    
    def remove_selected_url(self, item):
        """Remove selected URL from list"""
        values = self.url_tree.item(item, 'values')
        if values:
            url = values[0]
            if url in self.downloader.url_list:
                self.downloader.url_list.remove(url)
                self.refresh_url_tree()
                self.log_output(f"🗑️ URL removed: {url}")
    
    def copy_selected_url(self, item):
        """Copy selected URL to clipboard"""
        values = self.url_tree.item(item, 'values')
        if values:
            url = values[0]
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            self.log_output(f"📋 URL copied to clipboard: {url}")
    
    def update_url_count(self):
        """Update URL count display"""
        count = len(self.downloader.url_list)
        self.url_count_label.config(text=f"URLs: {count}")
    
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
            self.overall_progress.config(value=0)
        
        self.root.after(0, reset_ui)
    
    def reset_template(self):
        """Reset output template to default"""
        if self.auto_numbering.get():
            self.output_template.set("%(title)s.%(ext)s")  # Will be modified by auto_numbering
        else:
            self.output_template.set("%(title)s.%(ext)s")
    
    def on_auto_numbering_change(self):
        """Handle auto numbering checkbox change"""
        # The numbering will be handled in the download functions
        pass
    
    def start_download(self):
        """Start batch download process"""
        # Validate inputs
        if not self.downloader.yt_dlp_available:
            messagebox.showerror("Error", "yt-dlp is not available. Please install it first!")
            return
        
        if not self.downloader.url_list:
            messagebox.showwarning("Warning", "Please add some YouTube URLs first!")
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
            self.log_output("="*70)
            self.log_output("🚀 Starting batch download...")
            self.log_output(f"Total URLs: {len(self.downloader.url_list)}")
            self.log_output(f"Type: {self.download_type.get()}")
            self.log_output(f"Folder: {folder}")
            self.log_output(f"Auto Numbering: {'Enabled' if self.auto_numbering.get() else 'Disabled'}")
            self.log_output("="*70)
            
            # Disable UI elements
            self.root.after(0, lambda: self.download_btn.config(state="disabled", text="Downloading..."))
            self.root.after(0, lambda: self.progress.start())
            self.root.after(0, lambda: self.reset_progress())
            
            download_type = self.download_type.get()
            template = self.output_template.get() or "%(title)s.%(ext)s"
            auto_numbering = self.auto_numbering.get()
            continue_on_error = self.continue_on_error.get()
            
            try:
                if download_type == "video_best":
                    result = self.downloader.batch_download_videos(
                        quality="best", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        progress_callback=self.update_progress)
                elif download_type == "video_720p":
                    result = self.downloader.batch_download_videos(
                        quality="720p", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        progress_callback=self.update_progress)
                elif download_type == "video_480p":
                    result = self.downloader.batch_download_videos(
                        quality="480p", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        progress_callback=self.update_progress)
                elif download_type == "audio_mp3":
                    result = self.downloader.batch_download_audio(
                        audio_format="mp3", output_template=template, 
                        auto_numbering=auto_numbering, continue_on_error=continue_on_error,
                        progress_callback=self.update_progress)
                
                # Update UI with results
                self.root.after(0, self.refresh_url_tree)
                
            except Exception as e:
                self.log_output(f"❌ Error during batch download: {e}")
                result = {"success": 0, "failed": len(self.downloader.url_list)}
            
            # Re-enable UI elements
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.download_btn.config(state="normal", text="🚀 Start Batch Download"))
            
            # Show completion message
            if result["success"] > 0:
                self.log_output("="*70)
                self.log_output("🎉 Batch download completed!")
                self.log_output(f"✅ Successful: {result['success']}")
                self.log_output(f"❌ Failed: {result['failed']}")
                self.log_output(f"📁 Files saved to: {folder}")
                self.log_output("="*70)
                
                self.root.after(0, lambda: messagebox.showinfo("Success", 
                    f"Batch download completed!\n\n"
                    f"✅ Successful: {result['success']}\n"
                    f"❌ Failed: {result['failed']}\n\n"
                    f"Files saved to:\n{folder}"))
            else:
                self.log_output("="*70)
                self.log_output("😞 Batch download failed!")
                self.log_output("Please check URLs and internet connection.")
                self.log_output("="*70)
                
                self.root.after(0, lambda: messagebox.showerror("Error", 
                    f"Batch download failed!\n\n"
                    f"All {result['failed']} downloads failed.\n\n"
                    f"Please check:\n"
                    f"- Internet connection\n"
                    f"- YouTube URLs validity\n"
                    f"- Download folder permissions"))
        
        threading.Thread(target=download_thread, daemon=True).start()
    
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
    
    app = BatchDownloaderGUI(root)
    
    # Center the window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()


if __name__ == "__main__":
    main()