import os
import glob
import argparse
from pathlib import Path

# Konfigurasi FFmpeg path sebelum import pydub
FFMPEG_PATH = r"C:\Users\nonion\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
FFPROBE_PATH = r"C:\Users\nonion\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0-essentials_build\bin\ffprobe.exe"

# Set environment untuk pydub agar menemukan ffmpeg
if os.path.exists(FFMPEG_PATH):
    os.environ["PATH"] = os.path.dirname(FFMPEG_PATH) + os.pathsep + os.environ.get("PATH", "")

from pydub import AudioSegment

def get_audio_files(folder_path, formats=None):
    """
    Mencari semua file audio dalam folder dengan format yang ditentukan
    """
    if formats is None:
        formats = ['mp3', 'wav', 'flac', 'm4a', 'ogg', 'aac', 'wma']
    
    audio_files = []
    for format_ext in formats:
        pattern = os.path.join(folder_path, f"*.{format_ext}")
        files = glob.glob(pattern, recursive=False)
        audio_files.extend(files)
    
    # Urutkan berdasarkan nama file
    audio_files.sort()
    return audio_files

def merge_audio_files(input_folder, output_file, crossfade_duration=0, gap_duration=0, formats=None):
    """
    Menggabungkan file audio dalam folder menjadi satu file
    
    Args:
        input_folder: Path folder yang berisi file audio
        output_file: Nama file output hasil gabungan
        crossfade_duration: Durasi crossfade dalam milidetik (0 = no crossfade)
        gap_duration: Durasi jeda antar lagu dalam milidetik (0 = no gap)
        formats: List format file yang akan dicari
    """
    
    # Cari semua file audio
    audio_files = get_audio_files(input_folder, formats)
    
    if not audio_files:
        print(f"❌ Tidak ada file audio yang ditemukan di folder '{input_folder}'")
        return False
    
    print(f"🎵 Ditemukan {len(audio_files)} file audio:")
    for i, file in enumerate(audio_files, 1):
        print(f"   {i}. {os.path.basename(file)}")
    
    print(f"\n🔄 Memulai proses penggabungan...")
    
    try:
        # Muat file pertama sebagai audio dasar
        combined_audio = AudioSegment.from_file(audio_files[0])
        print(f"   ✅ Memuat: {os.path.basename(audio_files[0])}")
        
        # Gabungkan file-file selanjutnya
        for i, audio_file in enumerate(audio_files[1:], 2):
            print(f"   🔗 Menggabungkan: {os.path.basename(audio_file)} ({i}/{len(audio_files)})")
            next_audio = AudioSegment.from_file(audio_file)
            
            # Terapkan crossfade atau gap sesuai konfigurasi
            if crossfade_duration > 0:
                # Crossfade: suara lagu pertama fade out saat lagu kedua fade in
                combined_audio = combined_audio.append(next_audio, crossfade=crossfade_duration)
            elif gap_duration > 0:
                # Gap: tambahkan jeda/silent antar lagu
                silence = AudioSegment.silent(duration=gap_duration)
                combined_audio = combined_audio + silence + next_audio
            else:
                # Gabungan langsung tanpa efek
                combined_audio += next_audio
        
        # Ekspor hasil akhir
        print(f"\n💾 Mengekspor hasil ke: {output_file}...")
        
        # Deteksi format output dari ekstensi file
        output_format = output_file.split('.')[-1].lower()
        if output_format not in ['mp3', 'wav', 'flac', 'm4a', 'ogg', 'aac']:
            output_format = 'mp3'  # Default ke MP3
            
        combined_audio.export(output_file, format=output_format)
        
        # Tampilkan informasi hasil
        duration_seconds = len(combined_audio) / 1000
        minutes = int(duration_seconds // 60)
        seconds = int(duration_seconds % 60)
        
        print(f"✅ Selesai! File berhasil digabungkan.")
        print(f"📊 Informasi hasil:")
        print(f"   • Total durasi: {minutes}:{seconds:02d}")
        print(f"   • Format output: {output_format.upper()}")
        print(f"   • Ukuran file: {os.path.getsize(output_file) / (1024*1024):.1f} MB")
        
        return True
        
    except Exception as e:
        print(f"❌ Terjadi error: {e}")
        print("💡 Pastikan:")
        print("   • FFmpeg sudah terinstal dan ada di PATH")
        print("   • File audio tidak corrupt")
        print("   • Anda memiliki permission untuk menulis file output")
        return False

def interactive_mode():
    """
    Mode interaktif untuk pengguna
    """
    print("🎵 AUDIO MERGER 🎵")
    print("Program untuk menggabungkan file audio menjadi satu file")
    print("Mendukung: MP3, WAV, FLAC, M4A, OGG, AAC, WMA")
    print("=" * 60)
    
    while True:
        print("\nPilihan:")
        print("1. Gabungkan audio dari folder")
        print("2. Gabungkan audio dengan crossfade")
        print("3. Gabungkan audio dengan jeda antar lagu")
        print("4. Info tentang crossfade dan gap")
        print("5. Keluar")
        
        choice = input("\nMasukkan pilihan (1-5): ").strip()
        
        if choice == '1':
            # Mode gabungan biasa
            folder = input("Masukkan path folder audio: ").strip().strip('"')
            if not os.path.exists(folder):
                print("❌ Folder tidak ditemukan!")
                continue
                
            output = input("Nama file output (misal: hasil.mp3): ").strip()
            if not output:
                output = "hasil_gabungan.mp3"
                
            merge_audio_files(folder, output)
            
        elif choice == '2':
            # Mode dengan crossfade
            folder = input("Masukkan path folder audio: ").strip().strip('"')
            if not os.path.exists(folder):
                print("❌ Folder tidak ditemukan!")
                continue
                
            try:
                crossfade = int(input("Durasi crossfade (detik, contoh: 2): ")) * 1000
            except ValueError:
                crossfade = 2000  # Default 2 detik
                
            output = input("Nama file output (misal: hasil_crossfade.mp3): ").strip()
            if not output:
                output = "hasil_crossfade.mp3"
                
            merge_audio_files(folder, output, crossfade_duration=crossfade)
            
        elif choice == '3':
            # Mode dengan gap/jeda
            folder = input("Masukkan path folder audio: ").strip().strip('"')
            if not os.path.exists(folder):
                print("❌ Folder tidak ditemukan!")
                continue
                
            try:
                gap = int(input("Durasi jeda antar lagu (detik, contoh: 1): ")) * 1000
            except ValueError:
                gap = 1000  # Default 1 detik
                
            output = input("Nama file output (misal: hasil_gap.mp3): ").strip()
            if not output:
                output = "hasil_gap.mp3"
                
            merge_audio_files(folder, output, gap_duration=gap)
            
        elif choice == '4':
            # Info tentang efek
            print("\n📚 INFORMASI EFEK:")
            print("\n🔄 CROSSFADE:")
            print("   • Lagu pertama pelan-pelan fade out")
            print("   • Lagu kedua pelan-pelan fade in")
            print("   • Kedua lagu overlap sejenak untuk transisi halus")
            print("   • Durasi total berkurang karena overlap")
            
            print("\n⏸️  GAP/JEDA:")
            print("   • Menambahkan silence/hening antar lagu")
            print("   • Berguna untuk memberi jeda nafas")
            print("   • Durasi total bertambah sesuai jeda")
            
            print("\n🔗 GABUNGAN LANGSUNG:")
            print("   • Lagu disambung langsung tanpa efek")
            print("   • Cepat dan sederhana")
            print("   • Mungkin terdengar 'kasar' antar transisi")
            
        elif choice == '5':
            print("Terima kasih! 👋")
            break
            
        else:
            print("❌ Pilihan tidak valid!")

def main():
    """
    Fungsi utama dengan support command line dan interactive mode
    """
    parser = argparse.ArgumentParser(description='Audio Merger - Gabungkan file audio menjadi satu')
    parser.add_argument('--folder', '-f', type=str, help='Path folder yang berisi file audio')
    parser.add_argument('--output', '-o', type=str, help='Nama file output')
    parser.add_argument('--crossfade', '-c', type=int, default=0, help='Durasi crossfade dalam detik')
    parser.add_argument('--gap', '-g', type=int, default=0, help='Durasi jeda antar lagu dalam detik')
    parser.add_argument('--formats', type=str, nargs='+', help='Format file yang dicari (default: semua format)')
    
    args = parser.parse_args()
    
    # Jika tidak ada argumen, jalankan mode interaktif
    if not args.folder:
        interactive_mode()
        return
    
    # Mode command line
    if not os.path.exists(args.folder):
        print(f"❌ Error: Folder '{args.folder}' tidak ditemukan!")
        return
    
    output_file = args.output if args.output else "hasil_gabungan.mp3"
    crossfade_ms = args.crossfade * 1000 if args.crossfade > 0 else 0
    gap_ms = args.gap * 1000 if args.gap > 0 else 0
    
    success = merge_audio_files(
        args.folder, 
        output_file, 
        crossfade_duration=crossfade_ms,
        gap_duration=gap_ms,
        formats=args.formats
    )
    
    if not success:
        exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna. Sampai jumpa! 👋")
    except Exception as e:
        print(f"\n❌ Terjadi error tidak terduga: {e}")