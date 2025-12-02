#!/usr/bin/env python3
"""
YouTube Batch Downloader
Download multiple individual YouTube videos from a list of URLs
Berbeda dengan playlist downloader, ini untuk download banyak             cmd = [
                sys.executable, '-m', 'yt_dlp',  # Use python -m yt_dlp instead of yt-dlp command
                '-f', format_selector,
                '-o', output_template,
                '--no-playlist',
                url
            ]
            
            print(f"📹 Downloading: {url}")ividual sekaligus
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
import json
import time

class BatchDownloader:
    def __init__(self):
        self.download_folder = None
        self.yt_dlp_available = self._check_yt_dlp()
        self.url_list = []
        self.failed_downloads = []
        self.successful_downloads = []
    
    def _check_yt_dlp(self) -> bool:
        """Check if yt-dlp is installed and available"""
        try:
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install_or_update_yt_dlp(self) -> bool:
        """Install or update yt-dlp to the latest version"""
        try:
            print("Installing/Updating yt-dlp...")
            result = subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                print("yt-dlp berhasil diinstall/update!")
                self.yt_dlp_available = True
                return True
            else:
                print(f"Error installing yt-dlp: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print("Timeout saat install yt-dlp")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def set_download_folder(self, folder_path: str) -> bool:
        """Set and create download folder if it doesn't exist"""
        try:
            self.download_folder = Path(folder_path)
            self.download_folder.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            print(f"Error creating folder: {e}")
            return False
    
    def add_url(self, url: str) -> bool:
        """Add a YouTube URL to the download list"""
        url = url.strip()
        if not url:
            return False
        
        # Basic YouTube URL validation
        if not ('youtube.com/watch' in url or 'youtu.be/' in url):
            print(f"⚠️  URL mungkin bukan video YouTube: {url}")
        
        if url not in self.url_list:
            self.url_list.append(url)
            return True
        else:
            print(f"⚠️  URL sudah ada dalam list: {url}")
            return False
    
    def add_urls_from_list(self, urls: List[str]) -> int:
        """Add multiple URLs to the download list"""
        added_count = 0
        for url in urls:
            if self.add_url(url):
                added_count += 1
        return added_count
    
    def add_urls_from_file(self, file_path: str) -> int:
        """Add URLs from a text file (one URL per line)"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                urls = [line.strip() for line in f.readlines() if line.strip()]
            return self.add_urls_from_list(urls)
        except Exception as e:
            print(f"Error reading file: {e}")
            return 0
    
    def clear_url_list(self):
        """Clear the URL list"""
        self.url_list.clear()
        self.failed_downloads.clear()
        self.successful_downloads.clear()
    
    def get_video_info(self, url: str) -> Optional[Dict[str, Any]]:
        """Get video information without downloading"""
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia.")
            return None
        
        try:
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '--dump-json',
                '--no-playlist',
                '--extractor-args', 'youtube:player_client=default',  # Suppress JS runtime warning
                url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                try:
                    info = json.loads(result.stdout.strip())
                    return {
                        'title': info.get('title', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'uploader': info.get('uploader', 'Unknown'),
                        'view_count': info.get('view_count', 0)
                    }
                except json.JSONDecodeError:
                    return None
            else:
                return None
                
        except subprocess.TimeoutExpired:
            return None
        except Exception as e:
            return None
    
    def download_single_video(self, url: str, quality: str = "best", 
                             output_template: str = "%(title)s.%(ext)s",
                             auto_numbering: bool = False,
                             embed_thumbnail: bool = True,
                             embed_metadata: bool = True) -> bool:
        """
        Download a single video
        
        Args:
            url: YouTube video URL
            quality: Video quality ("best", "720p", "480p", etc.)
            output_template: Output filename template
            auto_numbering: Add number prefix to filename
            embed_thumbnail: Embed YouTube thumbnail (disable for faster download)
            embed_metadata: Add metadata like title, artist, date (disable for faster download)
        """
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia!")
            return False
        
        if not self.download_folder:
            print("Download folder belum di-set!")
            return False
        
        try:
            # Change to download directory
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
            # Add numbering if requested
            if auto_numbering:
                current_number = len(self.successful_downloads) + 1
                if "%(title)s" in output_template:
                    output_template = output_template.replace("%(title)s", f"{current_number:02d} - %(title)s")
                else:
                    output_template = f"{current_number:02d} - " + output_template
            
            # Build command based on quality
            if quality == "best":
                format_selector = "bv+ba/b"
            elif quality == "720p":
                format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif quality == "480p":
                format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            else:
                format_selector = quality
            
            cmd = [
                sys.executable, '-m', 'yt_dlp',
                '-f', format_selector,
                '-o', output_template,
                '--no-playlist',
                '--extractor-args', 'youtube:player_client=default',  # Suppress JS runtime warning
            ]
            
            # Add optional features (can be disabled for faster/lighter downloads)
            if embed_thumbnail:
                cmd.append('--embed-thumbnail')  # Embed thumbnail as cover art
            if embed_metadata:
                cmd.append('--add-metadata')     # Add metadata (title, artist, etc.)
            
            cmd.append(url)
            
            print(f"📥 Downloading: {url}")
            
            # Run the download command
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            for line in process.stdout:
                print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.successful_downloads.append(url)
                return True
            else:
                self.failed_downloads.append(url)
                return False
                
        except Exception as e:
            print(f"Error downloading {url}: {e}")
            self.failed_downloads.append(url)
            return False
        finally:
            # Return to original directory
            try:
                os.chdir(original_cwd)
            except:
                pass
    
    def download_single_audio(self, url: str, audio_format: str = "mp3",
                             audio_quality: str = "0",
                             output_template: str = "%(title)s.%(ext)s",
                             auto_numbering: bool = False,
                             embed_thumbnail: bool = True,
                             embed_metadata: bool = True) -> bool:
        """
        Download audio only from a single video
        
        Args:
            url: YouTube video URL
            audio_format: Audio format ("mp3", "m4a", "wav", etc.)
            audio_quality: Audio quality (0=best, 9=worst)
            output_template: Output filename template
            auto_numbering: Add number prefix to filename
            embed_thumbnail: Embed YouTube thumbnail as album art (disable for faster download)
            embed_metadata: Add metadata like title, artist, date (disable for faster download)
        """
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia!")
            return False
        
        if not self.download_folder:
            print("Download folder belum di-set!")
            return False
        
        try:
            # Change to download directory
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
            # Add numbering if requested
            if auto_numbering:
                current_number = len(self.successful_downloads) + 1
                if "%(title)s" in output_template:
                    output_template = output_template.replace("%(title)s", f"{current_number:02d} - %(title)s")
                else:
                    output_template = f"{current_number:02d} - " + output_template
            
            cmd = [
                sys.executable, '-m', 'yt_dlp',  # Use python -m yt_dlp instead of yt-dlp command
                '-x',  # Extract audio
                '--audio-format', audio_format,
                '--audio-quality', audio_quality,
                '-o', output_template,
                '--no-playlist',
                '--extractor-args', 'youtube:player_client=default',  # Suppress JS runtime warning
            ]
            
            # Add optional features (can be disabled for faster/lighter downloads)
            if embed_thumbnail:
                cmd.append('--embed-thumbnail')  # Embed thumbnail as album art (MP3 cover)
            if embed_metadata:
                cmd.append('--add-metadata')     # Add metadata (title, artist, album, etc.)
            
            cmd.append(url)
            
            print(f"🎵 Downloading audio: {url}")
            
            # Run the download command
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            for line in process.stdout:
                print(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.successful_downloads.append(url)
                return True
            else:
                self.failed_downloads.append(url)
                return False
                
        except Exception as e:
            print(f"Error downloading audio from {url}: {e}")
            self.failed_downloads.append(url)
            return False
        finally:
            # Return to original directory
            try:
                os.chdir(original_cwd)
            except:
                pass
    
    def batch_download_videos(self, quality: str = "best", 
                             output_template: str = "%(title)s.%(ext)s",
                             auto_numbering: bool = False,
                             continue_on_error: bool = True,
                             embed_thumbnail: bool = True,
                             embed_metadata: bool = True,
                             progress_callback=None) -> Dict[str, int]:
        """
        Download all videos in the URL list
        
        Args:
            quality: Video quality
            output_template: Output filename template
            auto_numbering: Add number prefix to filenames
            continue_on_error: Continue downloading other videos if one fails
            embed_thumbnail: Embed YouTube thumbnail (disable for faster download)
            embed_metadata: Add metadata like title, artist, date (disable for faster download)
            progress_callback: Function callback untuk update progress (current, total, percentage, title)
        
        Returns:
            Dict with success and failure counts
        """
        if not self.url_list:
            print("Tidak ada URL dalam list!")
            return {"success": 0, "failed": 0}
        
        print(f"🚀 Memulai batch download {len(self.url_list)} video...")
        print("=" * 60)
        
        self.successful_downloads.clear()
        self.failed_downloads.clear()
        
        for i, url in enumerate(self.url_list, 1):
            print(f"\n📹 [{i}/{len(self.url_list)}] Processing: {url}")
            
            # Update progress if callback provided
            if progress_callback:
                percentage = (i / len(self.url_list)) * 100
                progress_callback(i, len(self.url_list), percentage, f"Processing: {url[:50]}...")
            
            success = self.download_single_video(url, quality, output_template, auto_numbering, 
                                                embed_thumbnail, embed_metadata)
            
            if success:
                print(f"✅ [{i}/{len(self.url_list)}] Download berhasil!")
            else:
                print(f"❌ [{i}/{len(self.url_list)}] Download gagal!")
                if not continue_on_error:
                    print("⏹️  Menghentikan batch download karena ada error.")
                    break
            
            # Small delay between downloads
            if i < len(self.url_list):
                time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"📊 Batch Download Selesai!")
        print(f"✅ Berhasil: {len(self.successful_downloads)}")
        print(f"❌ Gagal: {len(self.failed_downloads)}")
        
        if self.failed_downloads:
            print("\n❌ URL yang gagal:")
            for url in self.failed_downloads:
                print(f"  - {url}")
        
        return {
            "success": len(self.successful_downloads),
            "failed": len(self.failed_downloads)
        }
    
    def batch_download_audio(self, audio_format: str = "mp3", audio_quality: str = "0",
                            output_template: str = "%(title)s.%(ext)s",
                            auto_numbering: bool = False,
                            continue_on_error: bool = True,
                            embed_thumbnail: bool = True,
                            embed_metadata: bool = True,
                            progress_callback=None) -> Dict[str, int]:
        """
        Download audio only from all videos in the URL list
        
        Args:
            audio_format: Audio format ("mp3", "m4a", etc.)
            audio_quality: Audio quality (0=best, 9=worst)
            output_template: Output filename template
            auto_numbering: Add number prefix to filenames
            continue_on_error: Continue downloading other videos if one fails
            embed_thumbnail: Embed YouTube thumbnail as album art (disable for faster download)
            embed_metadata: Add metadata like title, artist, date (disable for faster download)
            progress_callback: Function callback untuk update progress (current, total, percentage, title)
        
        Returns:
            Dict with success and failure counts
        """
        if not self.url_list:
            print("Tidak ada URL dalam list!")
            return {"success": 0, "failed": 0}
        
        print(f"🎵 Memulai batch download audio {len(self.url_list)} video...")
        print("=" * 60)
        
        self.successful_downloads.clear()
        self.failed_downloads.clear()
        
        for i, url in enumerate(self.url_list, 1):
            print(f"\n🎵 [{i}/{len(self.url_list)}] Processing: {url}")
            
            # Update progress if callback provided
            if progress_callback:
                percentage = (i / len(self.url_list)) * 100
                progress_callback(i, len(self.url_list), percentage, f"Processing: {url[:50]}...")
            
            success = self.download_single_audio(url, audio_format, audio_quality, output_template, 
                                                auto_numbering, embed_thumbnail, embed_metadata)
            
            if success:
                print(f"✅ [{i}/{len(self.url_list)}] Download berhasil!")
            else:
                print(f"❌ [{i}/{len(self.url_list)}] Download gagal!")
                if not continue_on_error:
                    print("⏹️  Menghentikan batch download karena ada error.")
                    break
            
            # Small delay between downloads
            if i < len(self.url_list):
                time.sleep(2)
        
        print("\n" + "=" * 60)
        print(f"📊 Batch Download Audio Selesai!")
        print(f"✅ Berhasil: {len(self.successful_downloads)}")
        print(f"❌ Gagal: {len(self.failed_downloads)}")
        
        if self.failed_downloads:
            print("\n❌ URL yang gagal:")
            for url in self.failed_downloads:
                print(f"  - {url}")
        
        return {
            "success": len(self.successful_downloads),
            "failed": len(self.failed_downloads)
        }


def main():
    """Command line interface untuk batch downloader"""
    downloader = BatchDownloader()
    
    print("🎬 YouTube Batch Downloader 🎬")
    print("="*40)
    print("Download multiple individual YouTube videos")
    print()
    
    # Check yt-dlp
    if not downloader.yt_dlp_available:
        print("yt-dlp belum terinstall atau perlu diupdate.")
        install = input("Install/Update yt-dlp sekarang? (y/n): ").lower().strip()
        if install == 'y':
            if not downloader.install_or_update_yt_dlp():
                print("Gagal install yt-dlp. Keluar...")
                return
        else:
            print("yt-dlp diperlukan untuk menjalankan program ini.")
            return
    
    # Set download folder
    while True:
        folder = input("\nMasukkan path folder download (atau tekan Enter untuk folder saat ini): ").strip()
        if not folder:
            folder = os.getcwd()
        
        if downloader.set_download_folder(folder):
            print(f"✅ Download folder: {downloader.download_folder}")
            break
        else:
            print("❌ Gagal membuat folder. Coba lagi...")
    
    # Add URLs
    print("\n📝 Tambahkan URL YouTube (ketik 'done' untuk selesai):")
    while True:
        url = input("URL YouTube: ").strip()
        if url.lower() == 'done':
            break
        elif url:
            if downloader.add_url(url):
                print(f"✅ URL ditambahkan. Total: {len(downloader.url_list)}")
            else:
                print("❌ Gagal menambahkan URL atau URL sudah ada.")
    
    if not downloader.url_list:
        print("❌ Tidak ada URL yang ditambahkan. Keluar...")
        return
    
    print(f"\n📋 Total URL: {len(downloader.url_list)}")
    
    # Auto numbering option
    print("\n🔢 Auto File Numbering:")
    auto_numbering_choice = input("Aktifkan penomoran otomatis file? (y/n, default: n): ").strip().lower()
    auto_numbering = auto_numbering_choice == 'y'
    
    if auto_numbering:
        print("✅ File akan diberi nomor urut: 01 - Title.ext, 02 - Title.ext, ...")
    else:
        print("❌ File tanpa nomor urut: Title.ext")
    
    # Choose download type
    print("\n🎯 Pilih jenis download:")
    print("1. Video (kualitas terbaik)")
    print("2. Video (720p - hemat kuota)")
    print("3. Video (480p - hemat kuota)")
    print("4. Audio saja (MP3)")
    
    while True:
        choice = input("Pilihan (1-4): ").strip()
        
        if choice == "1":
            result = downloader.batch_download_videos(quality="best", auto_numbering=auto_numbering)
            break
        elif choice == "2":
            result = downloader.batch_download_videos(quality="720p", auto_numbering=auto_numbering)
            break
        elif choice == "3":
            result = downloader.batch_download_videos(quality="480p", auto_numbering=auto_numbering)
            break
        elif choice == "4":
            result = downloader.batch_download_audio(auto_numbering=auto_numbering)
            break
        else:
            print("Pilihan tidak valid. Masukkan 1-4.")
    
    print(f"\n🎉 Batch download selesai!")
    print(f"📁 File tersimpan di: {downloader.download_folder}")
    print(f"✅ Berhasil: {result['success']}")
    print(f"❌ Gagal: {result['failed']}")


if __name__ == "__main__":
    main()