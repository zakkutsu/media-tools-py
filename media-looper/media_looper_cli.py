"""
Media Looper - Unified CLI Version
Single Loop & Alternating Loop dengan FFmpeg stream copy

Author: Media Tools Suite
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path


def check_ffmpeg():
    """Check if FFmpeg is installed"""
    if not shutil.which('ffmpeg'):
        print("\n❌ ERROR: FFmpeg tidak ditemukan!")
        print("   Install FFmpeg: https://ffmpeg.org/download.html")
        return False
    return True


def clean_path(path):
    """Clean path dari quotes (drag & drop effect)"""
    return path.strip().replace('"', '').replace("'", '')


def get_ffmpeg_path_format(path):
    """Convert path untuk FFmpeg concat demuxer"""
    abs_path = os.path.abspath(path)
    return abs_path.replace(os.sep, '/').replace("'", "'\\''")


def get_media_duration(file_path):
    """Get media duration menggunakan FFprobe"""
    try:
        cmd = ['ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
               '-of', 'default=noprint_wrappers=1:nokey=1', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(result.stdout.strip())
    except:
        return None


def format_duration(seconds):
    """Format seconds ke HH:MM:SS"""
    if seconds is None:
        return "Unknown"
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours}:{minutes:02d}:{secs:02d}" if hours > 0 else f"{minutes}:{secs:02d}"


def validate_media_file(file_path):
    """Validate file existence dan format"""
    if not os.path.exists(file_path):
        return False, "File tidak ditemukan"
    
    video_exts = ['.mp4', '.mkv', '.avi', '.mov', '.webm', '.flv', '.wmv', '.m4v']
    audio_exts = ['.mp3', '.wav', '.aac', '.flac', '.m4a', '.ogg', '.opus', '.wma']
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext not in video_exts + audio_exts:
        return False, f"Format {ext} tidak didukung"
    return True, "OK"


def process_single_loop(input_file, loop_count):
    """MODE 1: Single Loop (A-A-A...)"""
    is_valid, msg = validate_media_file(input_file)
    if not is_valid:
        print(f"❌ Error: {msg}")
        return None
    
    filename, ext = os.path.splitext(input_file)
    output_file = f"{filename}_looped_{loop_count}x{ext}"
    
    duration = get_media_duration(input_file)
    if duration:
        total = duration * int(loop_count)
        print(f"\n📊 Duration: {format_duration(duration)} → {format_duration(total)} ({loop_count}x)")
    
    print(f"\n🔁 Single Loop Mode")
    print(f"Input:  {os.path.basename(input_file)}")
    print(f"Output: {os.path.basename(output_file)}")
    
    ffmpeg_loop_count = int(loop_count) - 1
    cmd = ['ffmpeg', '-stream_loop', str(ffmpeg_loop_count), '-i', input_file,
           '-c', 'copy', output_file, '-y']
    
    print(f"\n⚙️  Processing...")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"✅ Success! {output_file} ({size:.2f} MB)")
        return output_file
    except subprocess.CalledProcessError:
        print("❌ FFmpeg error")
        return None


def process_alternating_loop(file_a, file_b, loop_count):
    """MODE 2: Alternating Loop (A-B-A-B...)"""
    for f, name in [(file_a, 'A'), (file_b, 'B')]:
        is_valid, msg = validate_media_file(f)
        if not is_valid:
            print(f"❌ File {name} Error: {msg}")
            return None
    
    ext_a = os.path.splitext(file_a)[1].lower()
    ext_b = os.path.splitext(file_b)[1].lower()
    
    if ext_a != ext_b:
        print(f"\n⚠️  WARNING: Format berbeda ({ext_a} vs {ext_b})")
        print("Stream copy mungkin gagal. Pastikan codec sama!")
        if input("Lanjut? (y/n): ").lower() != 'y':
            return None
    
    duration_a = get_media_duration(file_a)
    duration_b = get_media_duration(file_b)
    if duration_a and duration_b:
        pair = duration_a + duration_b
        total = pair * int(loop_count)
        print(f"\n📊 Duration: {format_duration(duration_a)} + {format_duration(duration_b)} = {format_duration(pair)}")
        print(f"   Total: {format_duration(total)} ({loop_count} sets)")
    
    print(f"\n🔁 Alternating Loop Mode (A-B pattern)")
    print(f"File A: {os.path.basename(file_a)}")
    print(f"File B: {os.path.basename(file_b)}")
    
    list_file = "temp_concat_list.txt"
    path_a = get_ffmpeg_path_format(file_a)
    path_b = get_ffmpeg_path_format(file_b)
    
    try:
        with open(list_file, 'w', encoding='utf-8') as f:
            for _ in range(int(loop_count)):
                f.write(f"file '{path_a}'\n")
                f.write(f"file '{path_b}'\n")
        
        filename_out, ext_out = os.path.splitext(file_a)
        output_file = f"{filename_out}_merged_{loop_count}x{ext_out}"
        
        cmd = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', list_file,
               '-c', 'copy', output_file, '-y']
        
        print(f"⚙️  Processing...")
        subprocess.run(cmd, check=True, capture_output=True)
        
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"✅ Success! {output_file} ({size:.2f} MB)")
        return output_file
    except subprocess.CalledProcessError:
        print("❌ FFmpeg error. Cek codec compatibility!")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        if os.path.exists(list_file):
            os.remove(list_file)


def main():
    """Main CLI dengan menu"""
    print("=" * 60)
    print("  MEDIA LOOPER TOOL")
    print("  Single Loop & Alternating Loop (A-B Pattern)")
    print("=" * 60)
    
    if not check_ffmpeg():
        input("\nPress Enter to exit...")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("MENU:")
        print("1. Single Loop       (A-A-A... N times)")
        print("2. Alternating Loop  (A-B-A-B... N sets)")
        print("3. Exit")
        print("=" * 60)
        
        choice = input("\nChoice (1/2/3): ").strip()
        
        if choice == '3':
            print("Bye! 👋")
            break
        
        elif choice == '1':
            print("\n--- SINGLE LOOP MODE ---")
            path = clean_path(input("📂 File path: "))
            
            if not os.path.exists(path):
                print("❌ File not found!")
                continue
            
            try:
                count = int(input("🔁 Loop count (e.g., 60): "))
                if count < 1:
                    print("❌ Min 1x")
                    continue
                if count > 1000:
                    if input(f"⚠️  {count}x = large file. Continue? (y/n): ").lower() != 'y':
                        continue
                process_single_loop(path, count)
            except ValueError:
                print("❌ Invalid number!")
        
        elif choice == '2':
            print("\n--- ALTERNATING LOOP MODE ---")
            print("⚠️  Both files must have same format/codec!")
            
            path_a = clean_path(input("📂 File A: "))
            path_b = clean_path(input("📂 File B: "))
            
            if not os.path.exists(path_a) or not os.path.exists(path_b):
                print("❌ File(s) not found!")
                continue
            
            try:
                count = int(input("🔁 Loop count (sets): "))
                if count < 1:
                    print("❌ Min 1 set")
                    continue
                if count > 500:
                    if input(f"⚠️  {count} sets = large file. Continue? (y/n): ").lower() != 'y':
                        continue
                process_alternating_loop(path_a, path_b, count)
            except ValueError:
                print("❌ Invalid number!")
        
        else:
            print("❌ Invalid choice (1/2/3)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
