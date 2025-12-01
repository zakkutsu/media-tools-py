#!/usr/bin/env python3
"""
YouTube Playlist Downloader
Menggunakan yt-dlp untuk mendownload playlist YouTube dengan berbagai opsi kualitas
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
import json

class PlaylistDownloader:
    def __init__(self):
        self.download_folder = None
        self.yt_dlp_available = self._check_yt_dlp()
        self.yt_dlp_cmd = self._get_yt_dlp_command()
    
    def _check_yt_dlp(self) -> bool:
        """Check if yt-dlp is installed and available"""
        try:
            # Try yt-dlp command first
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        try:
            # Try as Python module if command not found
            result = subprocess.run([sys.executable, '-m', 'yt_dlp', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _get_yt_dlp_command(self) -> List[str]:
        """Get the correct yt-dlp command (either 'yt-dlp' or 'python -m yt_dlp')"""
        try:
            # Try yt-dlp command first
            result = subprocess.run(['yt-dlp', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                return ['yt-dlp']
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        # Fall back to Python module
        return [sys.executable, '-m', 'yt_dlp']
    
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
    
    def get_playlist_info(self, playlist_url: str) -> Optional[Dict[str, Any]]:
        """Get playlist information without downloading"""
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia. Jalankan install_or_update_yt_dlp() terlebih dahulu.")
            return None
        
        try:
            cmd = self.yt_dlp_cmd + [
                '--dump-json',
                '--flat-playlist',
                playlist_url
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                # Parse each line as JSON (yt-dlp outputs one JSON per line for playlists)
                entries = []
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        try:
                            entry = json.loads(line)
                            entries.append(entry)
                        except json.JSONDecodeError:
                            continue
                
                return {
                    'total_videos': len(entries),
                    'entries': entries
                }
            else:
                print(f"Error getting playlist info: {result.stderr}")
                return None
                
        except subprocess.TimeoutExpired:
            print("Timeout saat mengambil info playlist")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def download_video_playlist(self, playlist_url: str, quality: str = "best", 
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        """
        Download video playlist dengan kualitas terbaik
        
        Args:
            playlist_url: URL playlist YouTube
            quality: Kualitas video ("best", "720p", "480p", dll)
            output_template: Template nama file output
            auto_numbering: Enable/disable auto numbering (playlist_index)
            progress_callback: Function callback untuk update progress (current, total, percentage, title)
        """
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia. Install terlebih dahulu!")
            return False
        
        if not self.download_folder:
            print("Download folder belum di-set!")
            return False
        
        try:
            # Change to download directory
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
            # Adjust output template based on auto_numbering setting
            if not auto_numbering:
                # Remove only playlist_index from template, keep title and other variables
                output_template = output_template.replace("%(playlist_index)s - ", "")
                output_template = output_template.replace("%(playlist_index)s", "")
                # Clean up any double spaces or leading/trailing spaces
                output_template = " ".join(output_template.split())
                # Ensure we still have title in the template
                if "%(title)s" not in output_template:
                    output_template = "%(title)s.%(ext)s"
            
            # Build command based on quality
            if quality == "best":
                format_selector = "bv+ba/b"
            elif quality == "720p":
                format_selector = "bestvideo[height<=720]+bestaudio/best[height<=720]"
            elif quality == "480p":
                format_selector = "bestvideo[height<=480]+bestaudio/best[height<=480]"
            else:
                format_selector = quality
            
            cmd = self.yt_dlp_cmd + [
                '-f', format_selector,
                '-o', output_template,
                '--embed-thumbnail',  # Embed thumbnail as cover art
                '--add-metadata',     # Add metadata (title, artist, etc.)
                '--no-playlist' if 'list=' not in playlist_url else '',
                playlist_url
            ]
            
            # Remove empty string from cmd
            cmd = [arg for arg in cmd if arg]
            
            print(f"Mulai download video playlist...")
            print(f"URL: {playlist_url}")
            print(f"Kualitas: {quality}")
            print(f"Folder: {self.download_folder}")
            print("="*50)
            
            # Run the download command and show output in real-time
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            current_item = 0
            total_items = 0
            current_title = ""
            
            for line in process.stdout:
                line_stripped = line.strip()
                
                # Parse playlist info
                if "Downloading" in line and "items of" in line:
                    try:
                        # Extract total items from line like "Downloading 94 items of 94"
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "items" and i > 0:
                                total_items = int(parts[i-1])
                                break
                    except (ValueError, IndexError):
                        pass
                
                # Parse current download item
                elif "Downloading item" in line and "of" in line:
                    try:
                        # Extract current item from line like "[download] Downloading item 1 of 94"
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "item" and i < len(parts) - 2:
                                current_item = int(parts[i+1])
                                break
                    except (ValueError, IndexError):
                        pass
                
                # Parse video title being downloaded
                elif "] Extracting URL:" in line and "youtube.com/watch" in line:
                    # Reset title when starting new video
                    current_title = ""
                elif line_stripped.startswith("[youtube]") and "Downloading webpage" in line:
                    try:
                        # Extract video ID from line like "[youtube] VPK-lxmGyDk: Downloading webpage"
                        video_id = line_stripped.split("]")[1].split(":")[0].strip()
                        current_title = f"Video ID: {video_id}"
                    except (IndexError, ValueError):
                        pass
                
                # Show progress for each song
                if current_item > 0 and total_items > 0:
                    percentage = (current_item / total_items) * 100
                    progress_text = f"📥 [{current_item}/{total_items}] ({percentage:.1f}%) - {current_title}"
                    
                    # Only print progress when we have new item info
                    if "Downloading item" in line:
                        print(f"\n{progress_text}")
                        print("─" * len(progress_text))
                        
                        # Call progress callback if provided
                        if progress_callback:
                            progress_callback(current_item, total_items, percentage, current_title)
                
                # Print the original line (but filter some verbose output)
                if not any(skip in line_stripped for skip in ["Sleeping", "WARNING:", "See  https://"]):
                    print(line_stripped)
            
            process.wait()
            
            if process.returncode == 0:
                print("\n✅ Download selesai!")
                return True
            else:
                print(f"\n❌ Download gagal dengan kode error: {process.returncode}")
                return False
                
        except Exception as e:
            print(f"Error saat download: {e}")
            return False
        finally:
            # Return to original directory
            try:
                os.chdir(original_cwd)
            except:
                pass
    
    def download_audio_playlist(self, playlist_url: str, audio_format: str = "mp3",
                              audio_quality: str = "0",
                              output_template: str = "%(playlist_index)s - %(title)s.%(ext)s",
                              auto_numbering: bool = True, progress_callback=None) -> bool:
        """
        Download audio-only playlist
        
        Args:
            playlist_url: URL playlist YouTube
            audio_format: Format audio ("mp3", "m4a", "wav", dll)
            audio_quality: Kualitas audio (0=terbaik, 9=terburuk)
            output_template: Template nama file output
            auto_numbering: Enable/disable auto numbering (playlist_index)
            progress_callback: Function callback untuk update progress (current, total, percentage, title)
        """
        if not self.yt_dlp_available:
            print("yt-dlp tidak tersedia. Install terlebih dahulu!")
            return False
        
        if not self.download_folder:
            print("Download folder belum di-set!")
            return False
        
        try:
            # Change to download directory
            original_cwd = os.getcwd()
            os.chdir(self.download_folder)
            
            # Adjust output template based on auto_numbering setting
            if not auto_numbering:
                # Remove only playlist_index from template, keep title and other variables
                output_template = output_template.replace("%(playlist_index)s - ", "")
                output_template = output_template.replace("%(playlist_index)s", "")
                # Clean up any double spaces or leading/trailing spaces
                output_template = " ".join(output_template.split())
                # Ensure we still have title in the template
                if "%(title)s" not in output_template:
                    output_template = "%(title)s.%(ext)s"
            
            cmd = self.yt_dlp_cmd + [
                '-x',  # Extract audio
                '--audio-format', audio_format,
                '--audio-quality', audio_quality,
                '-o', output_template,
                '--embed-thumbnail',  # Embed thumbnail as album art (MP3 cover)
                '--add-metadata',     # Add metadata (title, artist, album, etc.)
                playlist_url
            ]
            
            print(f"Mulai download audio playlist...")
            print(f"URL: {playlist_url}")
            print(f"Format: {audio_format}")
            print(f"Kualitas: {audio_quality} (0=terbaik)")
            print(f"Folder: {self.download_folder}")
            print("="*50)
            
            # Run the download command and show output in real-time
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
                                     text=True, universal_newlines=True)
            
            current_item = 0
            total_items = 0
            current_title = ""
            
            for line in process.stdout:
                line_stripped = line.strip()
                
                # Parse playlist info
                if "Downloading" in line and "items of" in line:
                    try:
                        # Extract total items from line like "Downloading 94 items of 94"
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "items" and i > 0:
                                total_items = int(parts[i-1])
                                break
                    except (ValueError, IndexError):
                        pass
                
                # Parse current download item
                elif "Downloading item" in line and "of" in line:
                    try:
                        # Extract current item from line like "[download] Downloading item 1 of 94"
                        parts = line_stripped.split()
                        for i, part in enumerate(parts):
                            if part == "item" and i < len(parts) - 2:
                                current_item = int(parts[i+1])
                                break
                    except (ValueError, IndexError):
                        pass
                
                # Parse video title being downloaded
                elif "] Extracting URL:" in line and "youtube.com/watch" in line:
                    # Reset title when starting new video
                    current_title = ""
                elif line_stripped.startswith("[youtube]") and "Downloading webpage" in line:
                    try:
                        # Extract video ID from line like "[youtube] VPK-lxmGyDk: Downloading webpage"
                        video_id = line_stripped.split("]")[1].split(":")[0].strip()
                        current_title = f"Audio ID: {video_id}"
                    except (IndexError, ValueError):
                        pass
                
                # Show progress for each song
                if current_item > 0 and total_items > 0:
                    percentage = (current_item / total_items) * 100
                    progress_text = f"🎵 [{current_item}/{total_items}] ({percentage:.1f}%) - {current_title}"
                    
                    # Only print progress when we have new item info
                    if "Downloading item" in line:
                        print(f"\n{progress_text}")
                        print("─" * len(progress_text))
                        
                        # Call progress callback if provided
                        if progress_callback:
                            progress_callback(current_item, total_items, percentage, current_title)
                
                # Print the original line (but filter some verbose output)
                if not any(skip in line_stripped for skip in ["Sleeping", "WARNING:", "See  https://"]):
                    print(line_stripped)
            
            process.wait()
            
            if process.returncode == 0:
                print("\n✅ Download selesai!")
                return True
            else:
                print(f"\n❌ Download gagal dengan kode error: {process.returncode}")
                return False
                
        except Exception as e:
            print(f"Error saat download: {e}")
            return False
        finally:
            # Return to original directory
            try:
                os.chdir(original_cwd)
            except:
                pass


def main():
    """Command line interface untuk playlist downloader"""
    downloader = PlaylistDownloader()
    
    print("🎵 YouTube Playlist Downloader 🎵")
    print("="*40)
    
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
    
    # Get playlist URL
    while True:
        url = input("\nMasukkan URL playlist YouTube: ").strip()
        if url:
            break
        print("URL tidak boleh kosong!")
    
    # Get playlist info
    print("\n📋 Mengambil informasi playlist...")
    info = downloader.get_playlist_info(url)
    if info:
        print(f"📊 Total video: {info['total_videos']}")
    
    # Auto numbering option
    print("\n🔢 Auto File Numbering:")
    auto_numbering_choice = input("Aktifkan penomoran otomatis file? (y/n, default: y): ").strip().lower()
    auto_numbering = auto_numbering_choice != 'n'
    
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
            success = downloader.download_video_playlist(url, quality="best", auto_numbering=auto_numbering)
            break
        elif choice == "2":
            success = downloader.download_video_playlist(url, quality="720p", auto_numbering=auto_numbering)
            break
        elif choice == "3":
            success = downloader.download_video_playlist(url, quality="480p", auto_numbering=auto_numbering)
            break
        elif choice == "4":
            success = downloader.download_audio_playlist(url, auto_numbering=auto_numbering)
            break
        else:
            print("Pilihan tidak valid. Masukkan 1-4.")
    
    if success:
        print(f"\n🎉 Download berhasil! File tersimpan di: {downloader.download_folder}")
    else:
        print("\n😞 Download gagal. Cek koneksi internet atau URL playlist.")


if __name__ == "__main__":
    main()