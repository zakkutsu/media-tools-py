"""
Advanced Media Looper - CLI Version
Support single loop dan alternating loop (A-B-A-B) menggunakan FFmpeg concat demuxer

Author: Media Tools Suite
Educational Purpose: Demonstrating concat demuxer technique
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


def clean_path(path):
    """Membersihkan path dari tanda kutip (efek drag & drop di terminal)"""
    return path.strip().replace('"', '').replace("'", '')


def get_ffmpeg_path_format(path):
    """
    FFmpeg concat demuxer butuh format path khusus.
    Di Windows, backslash (\) harus diganti slash (/) atau di-escape.
    """
    abs_path = os.path.abspath(path)
    # Escape single quotes for FFmpeg concat format
    return abs_path.replace(os.sep, '/').replace("'", "'\\''")


def get_media_duration(file_path):
    """Get media file duration using FFprobe"""
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


def process_single_loop(input_file, loop_count):
    """
    MODE 1: Looping 1 File (A -> A -> A ...)
    Menggunakan stream_loop FFmpeg (paling efisien)
    """
    
    # Validate input
    is_valid, msg = validate_media_file(input_file)
    if not is_valid:
        print(f"❌ Error: {msg}")
        return None
    
    filename, ext = os.path.splitext(input_file)
    output_file = f"{filename}_looped_{loop_count}x{ext}"
    
    # Get duration info
    duration = get_media_duration(input_file)
    if duration:
        total_duration = duration * int(loop_count)
        print(f"\n📊 Info:")
        print(f"   Original: {format_duration(duration)}")
        print(f"   Total: {format_duration(total_duration)} ({loop_count}x)")
    
    print(f"\n--- MODE 1: Single Loop ---")
    print(f"Input: {os.path.basename(input_file)}")
    print(f"Loop: {loop_count}x")
    print(f"Output: {os.path.basename(output_file)}")
    
    # FFmpeg logic: stream_loop N menghitung N sebagai tambahan loop
    ffmpeg_loop_count = int(loop_count) - 1

    cmd = [
        'ffmpeg',
        '-stream_loop', str(ffmpeg_loop_count), 
        '-i', input_file,
        '-c', 'copy',  # Stream copy untuk kecepatan maksimal
        output_file,
        '-y'
    ]
    
    print(f"\n⚙️ Processing...")
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        output_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✅ SUKSES!")
        print(f"📁 Output: {output_file}")
        print(f"📦 Size: {output_size:.2f} MB")
        return output_file
    except subprocess.CalledProcessError:
        print("❌ Error saat processing.")
        return None


def process_alternating_loop(file_a, file_b, loop_count):
    """
    MODE 2: Alternating Loop (A -> B -> A -> B ...)
    Menggunakan concat demuxer technique
    """
    
    # 1. Validasi Files
    is_valid_a, msg_a = validate_media_file(file_a)
    is_valid_b, msg_b = validate_media_file(file_b)
    
    if not is_valid_a:
        print(f"❌ File A Error: {msg_a}")
        return None
    if not is_valid_b:
        print(f"❌ File B Error: {msg_b}")
        return None
    
    # 2. Validasi Ekstensi (Warning untuk compatibility)
    ext_a = os.path.splitext(file_a)[1].lower()
    ext_b = os.path.splitext(file_b)[1].lower()
    
    if ext_a != ext_b:
        print("\n⚠️  PERINGATAN: Ekstensi file berbeda!")
        print(f"   File A: {ext_a}")
        print(f"   File B: {ext_b}")
        print("\n   Stream Copy mungkin error atau menghasilkan file corrupt.")
        print("   Saran: Pastikan resolusi, codec, dan format kedua file identik.")
        proceed = input("\n   Tetap lanjutkan? (y/n): ")
        if proceed.lower() != 'y': 
            print("❌ Dibatalkan.")
            return None

    # 3. Get duration info
    duration_a = get_media_duration(file_a)
    duration_b = get_media_duration(file_b)
    
    if duration_a and duration_b:
        single_pair_duration = duration_a + duration_b
        total_duration = single_pair_duration * int(loop_count)
        print(f"\n📊 Info:")
        print(f"   File A: {format_duration(duration_a)}")
        print(f"   File B: {format_duration(duration_b)}")
        print(f"   Per Set: {format_duration(single_pair_duration)}")
        print(f"   Total: {format_duration(total_duration)} ({loop_count} sets)")

    # 4. Membuat List File Sementara (Concat Demuxer Algorithm)
    list_filename = "temp_concat_list.txt"
    
    path_a = get_ffmpeg_path_format(file_a)
    path_b = get_ffmpeg_path_format(file_b)

    print(f"\n--- MODE 2: Alternating Loop ---")
    print(f"File A: {os.path.basename(file_a)}")
    print(f"File B: {os.path.basename(file_b)}")
    print(f"Pattern: A-B-A-B... ({loop_count} sets)")
    print(f"\n⚙️ Generating concat list...")

    try:
        with open(list_filename, 'w', encoding='utf-8') as f:
            for i in range(int(loop_count)):
                f.write(f"file '{path_a}'\n")
                f.write(f"file '{path_b}'\n")
        
        print(f"✅ List created: {int(loop_count) * 2} entries")

        # 5. Prepare output filename
        filename_out, ext_out = os.path.splitext(file_a)
        output_file = f"{filename_out}_merged_looped_{loop_count}x{ext_out}"

        # 6. Eksekusi FFmpeg dengan Concat Demuxer
        cmd = [
            'ffmpeg',
            '-f', 'concat',       # Format concat demuxer
            '-safe', '0',         # Izinkan absolute path
            '-i', list_filename,  # Input dari file text
            '-c', 'copy',         # Stream copy (FAST!)
            output_file,
            '-y'
        ]

        print(f"\n⚙️ FFmpeg processing...")
        subprocess.run(cmd, check=True, capture_output=True)
        
        output_size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"\n✅ SUKSES!")
        print(f"📁 Output: {output_file}")
        print(f"📦 Size: {output_size:.2f} MB")
        
        return output_file
        
    except subprocess.CalledProcessError:
        print("❌ Error saat penggabungan.")
        print("\n💡 Tips:")
        print("   - Pastikan kedua file memiliki codec yang sama")
        print("   - Untuk file berbeda resolusi, gunakan re-encoding (lebih lama)")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None
    finally:
        # Cleanup temporary file
        if os.path.exists(list_filename):
            os.remove(list_filename)
            print("🧹 Temporary file cleaned")


def main():
    """Main CLI interface dengan menu"""
    
    print("=" * 60)
    print("  ADVANCED MEDIA LOOPER - Stream Copy Edition")
    print("  Single Loop & Alternating Loop (A-B Pattern)")
    print("=" * 60)
    
    # Check FFmpeg
    if not check_ffmpeg():
        input("\nTekan Enter untuk keluar...")
        return
    
    while True:
        print("\n" + "=" * 60)
        print("MENU:")
        print("=" * 60)
        print("1. Single Loop       (A → A → A ... N kali)")
        print("2. Alternating Loop  (A → B → A → B ... N set)")
        print("3. Keluar")
        print("=" * 60)
        
        pilihan = input("\n>> Pilih Menu (1/2/3): ").strip()

        if pilihan == '3':
            print("\n👋 Terima kasih!")
            break

        elif pilihan == '1':
            print("\n--- SINGLE LOOP MODE ---")
            print("💡 Tip: Drag & drop file ke terminal")
            
            path = input("\n📂 Path file: ")
            path = clean_path(path)
            
            if not os.path.exists(path):
                print("❌ File tidak ditemukan!")
                continue
            
            try:
                qty = input("🔁 Ulang berapa kali? (contoh: 60): ")
                qty_int = int(qty)
                
                if qty_int < 1:
                    print("❌ Minimal 1x loop")
                    continue
                
                if qty_int > 1000:
                    confirm = input(f"⚠️  Loop {qty_int}x akan menghasilkan file besar. Lanjut? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                
                process_single_loop(path, qty)
                
            except ValueError:
                print("❌ Masukkan angka yang valid!")
                continue

        elif pilihan == '2':
            print("\n--- ALTERNATING LOOP MODE ---")
            print("💡 Pattern: A-B-A-B-A-B...")
            print("⚠️  Kedua file harus memiliki format/codec yang sama!")
            
            path_a = input("\n📂 File PERTAMA (A): ")
            path_a = clean_path(path_a)
            
            path_b = input("📂 File KEDUA (B): ")
            path_b = clean_path(path_b)
            
            if not os.path.exists(path_a):
                print("❌ File A tidak ditemukan!")
                continue
            
            if not os.path.exists(path_b):
                print("❌ File B tidak ditemukan!")
                continue
            
            try:
                qty = input("\n🔁 Ulang berapa set (A+B)? (contoh: 10): ")
                qty_int = int(qty)
                
                if qty_int < 1:
                    print("❌ Minimal 1 set")
                    continue
                
                if qty_int > 500:
                    confirm = input(f"⚠️  {qty_int} sets akan membuat file sangat besar. Lanjut? (y/n): ")
                    if confirm.lower() != 'y':
                        continue
                
                process_alternating_loop(path_a, path_b, qty)
                
            except ValueError:
                print("❌ Masukkan angka yang valid!")
                continue
            
        else:
            print("❌ Pilihan tidak valid. Gunakan 1, 2, atau 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program dihentikan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal Error: {e}")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
