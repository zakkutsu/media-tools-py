"""
Media Looper - CLI Version
Loop video/audio files using FFmpeg stream copy (no re-encoding)

Author: Media Tools Suite
Educational Purpose: Demonstrating binary concatenation vs pixel processing
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path


def check_ffmpeg():
    """Check if FFmpeg is installed and accessible"""
    if not shutil.which('ffmpeg'):
        print("\n❌ ERROR: FFmpeg tidak ditemukan!")
        print("   Pastikan FFmpeg sudah terinstall dan ada di system PATH.")
        print("   Download: https://ffmpeg.org/download.html")
        return False
    return True


def get_media_duration(file_path):
    """Get media file duration using FFprobe (optional, for info only)"""
    try:
        cmd = [
            'ffprobe', 
            '-v', 'quiet',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            file_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        duration = float(result.stdout.strip())
        return duration
    except:
        return None


def format_duration(seconds):
    """Convert seconds to HH:MM:SS format"""
    if seconds is None:
        return "Unknown"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes}:{secs:02d}"


def validate_media_file(file_path):
    """Validate if file exists and is a supported media format"""
    if not os.path.exists(file_path):
        return False, "File tidak ditemukan"
    
    # Supported extensions
    video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv', '.m4v']
    audio_exts = ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.opus', '.wma']
    
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext not in video_exts + audio_exts:
        return False, f"Format {ext} mungkin tidak didukung"
    
    return True, "OK"


def process_loop(input_file, loop_count, output_file=None):
    """
    Main processing function - Loop media using FFmpeg stream copy
    
    Args:
        input_file: Path to input media file
        loop_count: Number of times to loop (total duration)
        output_file: Optional custom output path
    
    Technical Note:
        FFmpeg's -stream_loop counts "extra" loops.
        If user wants 60x total, we need: 1 original + 59 loops
    """
    
    # 1. Validate input file
    is_valid, msg = validate_media_file(input_file)
    if not is_valid:
        print(f"❌ Error: {msg}")
        return False
    
    # 2. Prepare output filename
    if output_file is None:
        filename, ext = os.path.splitext(input_file)
        output_file = f"{filename}_looped_{loop_count}x{ext}"
    
    # 3. Calculate FFmpeg loop parameter
    # User: "60x total" → FFmpeg: "59 extra loops"
    ffmpeg_loop_count = int(loop_count) - 1
    
    # 4. Get duration info (optional, for user feedback)
    original_duration = get_media_duration(input_file)
    if original_duration:
        total_duration = original_duration * loop_count
        print(f"\n📊 Info:")
        print(f"   Original Duration: {format_duration(original_duration)}")
        print(f"   Total Duration:    {format_duration(total_duration)} ({loop_count}x)")
    
    print(f"\n--- Processing: {os.path.basename(input_file)} ---")
    print(f"Target: {loop_count}x repetitions")
    print("Mode: Stream Copy (Zero Re-encoding, Maximum Speed)")
    print(f"Output: {os.path.basename(output_file)}")
    print("\n⚙️  FFmpeg sedang bekerja...")
    
    # 5. Build FFmpeg command
    # Key flags:
    # -stream_loop N : Repeat input N times (N = extra loops)
    # -c copy        : Stream copy - no decoding/encoding (INSTANT)
    # -y             : Overwrite output if exists
    cmd = [
        'ffmpeg',
        '-stream_loop', str(ffmpeg_loop_count),
        '-i', input_file,
        '-c', 'copy',  # 🔑 KEY: Stream copy for instant processing
        output_file,
        '-y'
    ]
    
    try:
        # Run FFmpeg with progress output
        subprocess.run(cmd, check=True)
        
        # Show success message
        output_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
        print(f"\n✅ SUKSES!")
        print(f"📁 File tersimpan: {output_file}")
        print(f"📦 Size: {output_size:.2f} MB")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Gagal memproses file.")
        print(f"   Kemungkinan penyebab:")
        print(f"   - File korup atau tidak valid")
        print(f"   - Format tidak didukung untuk stream copy")
        print(f"   - Disk space tidak cukup")
        return False
    except Exception as e:
        print(f"\n❌ Error tidak terduga: {e}")
        return False


def main():
    """Main CLI interface"""
    print("=" * 60)
    print("  MEDIA LOOPER TOOL - Stream Copy Edition")
    print("  Loop Video/Audio tanpa Re-encoding")
    print("=" * 60)
    
    # Check FFmpeg availability
    if not check_ffmpeg():
        input("\nTekan Enter untuk keluar...")
        return
    
    print("\n💡 Tip: Drag & drop file ke terminal untuk auto-paste path")
    print("=" * 60)
    
    # Get input file path
    file_path = input("\n📂 Path file (atau drag & drop): ").strip()
    
    # Clean quotes (Windows auto-adds quotes when dragging files)
    file_path = file_path.replace('"', '').replace("'", '')
    
    # Validate file exists
    if not os.path.exists(file_path):
        print(f"\n❌ Error: File tidak ditemukan!")
        print(f"   Path: {file_path}")
        input("\nTekan Enter untuk keluar...")
        return
    
    # Get loop count
    try:
        loop_input = input("\n🔁 Jumlah loop (contoh: 60): ").strip()
        loop_count = int(loop_input)
        
        if loop_count < 1:
            print("❌ Jumlah loop minimal 1")
            input("\nTekan Enter untuk keluar...")
            return
        
        if loop_count > 1000:
            confirm = input(f"\n⚠️  Loop {loop_count}x akan menghasilkan file sangat besar. Lanjut? (y/n): ")
            if confirm.lower() != 'y':
                print("Dibatalkan.")
                return
                
    except ValueError:
        print("❌ Masukkan angka yang valid!")
        input("\nTekan Enter untuk keluar...")
        return
    
    # Process the file
    print("\n" + "=" * 60)
    success = process_loop(file_path, loop_count)
    print("=" * 60)
    
    if success:
        print("\n🎉 Proses selesai!")
    else:
        print("\n⚠️  Proses gagal. Cek error di atas.")
    
    input("\nTekan Enter untuk keluar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Proses dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
