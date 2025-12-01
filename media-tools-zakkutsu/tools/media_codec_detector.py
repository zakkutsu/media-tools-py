import os
import filetype
import ffmpeg  # Membutuhkan ffmpeg-python
from PIL import Image # Membutuhkan Pillow

def get_media_info(file_path):
    """
    Menganalisis file media (gambar, audio, video) dan mencetak
    format serta codec-nya.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: File tidak ditemukan di '{file_path}'")
        return

    print(f"\n--- 🕵️ Menganalisis: {file_path} ---")

    try:
        # 1. Tebak tipe file dasar
        kind = filetype.guess(file_path)
        if kind is None:
            print("Tidak dapat menentukan tipe file.")
            return

        mime_type = kind.mime
        print(f"Tipe File (MIME): {mime_type}")

        # --- Penanganan untuk Gambar ---
        if 'image' in mime_type:
            try:
                with Image.open(file_path) as img:
                    print(f"🖼️  Format Gambar: {img.format}")
                    print(f"    Mode Warna: {img.mode}")
                    print(f"    Ukuran: {img.size}")
            except Exception as e:
                print(f"Tidak dapat membaca detail gambar dengan Pillow: {e}")

        # --- Penanganan untuk Video atau Audio ---
        elif 'video' in mime_type or 'audio' in mime_type:
            try:
                # 2. Gunakan ffprobe untuk "mengintip" isi file
                # ffmpeg.probe() akan mengembalikan dictionary besar berisi semua metadata
                probe = ffmpeg.probe(file_path)
                
                # 3. Dapatkan format kontainer
                container_format = probe.get('format', {}).get('format_long_name', 'N/A')
                print(f"📦 Format Kontainer: {container_format}")
                
                # 4. Loop melalui semua stream (aliran data) di dalam kontainer
                print("Aliran Data (Codecs):")
                if 'streams' in probe:
                    for i, stream in enumerate(probe['streams']):
                        codec_type = stream.get('codec_type', 'unknown')
                        codec_name = stream.get('codec_long_name', stream.get('codec_name', 'N/A'))
                        
                        print(f"  Stream #{i} ({codec_type.upper()})")
                        print(f"    ▶️  Codec: {codec_name}")
                        
                        # Tambahkan detail ekstra jika ada
                        if codec_type == 'video':
                            width = stream.get('width', 'N/A')
                            height = stream.get('height', 'N/A')
                            print(f"    Res: {width}x{height}")
                        elif codec_type == 'audio':
                            sample_rate = stream.get('sample_rate', 'N/A')
                            channels = stream.get('channels', 'N/A')
                            print(f"    Sample: {sample_rate} Hz, Channels: {channels}")
                            
            except ffmpeg.Error as e:
                # Menangkap error jika ffmpeg gagal membaca file
                print(f"❌ Error FFmpeg: {e.stderr.decode('utf-8')}")
            except Exception as e:
                print(f"Terjadi error saat probe ffmpeg: {e}")

        # --- Penanganan untuk Tipe Lain ---
        else:
            print(f"📁 Ini bukan file media standar (gambar/audio/video).")

    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
    
    print("-" * 30)


def analyze_files_from_input():
    """
    Fungsi untuk menganalisis file berdasarkan input pengguna
    """
    print("🎬 MEDIA CODEC DETECTOR 🎬")
    print("Program untuk mendeteksi format dan codec file media")
    print("Mendukung: Gambar (PNG, JPG, etc), Video (MP4, AVI, etc), Audio (MP3, WAV, etc)")
    print("=" * 60)
    
    while True:
        print("\nPilihan:")
        print("1. Analisis file tertentu")
        print("2. Analisis semua file dalam folder")
        print("3. Buat file dummy untuk testing")
        print("4. Keluar")
        
        choice = input("\nMasukkan pilihan (1-4): ").strip()
        
        if choice == '1':
            file_path = input("Masukkan path file: ").strip().strip('"')
            get_media_info(file_path)
            
        elif choice == '2':
            folder_path = input("Masukkan path folder: ").strip().strip('"')
            if not os.path.exists(folder_path):
                print(f"❌ Folder tidak ditemukan: {folder_path}")
                continue
                
            files = []
            for file in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file)
                if os.path.isfile(file_path):
                    files.append(file_path)
            
            if not files:
                print("❌ Tidak ada file dalam folder tersebut")
                continue
                
            print(f"\nDitemukan {len(files)} file. Menganalisis...")
            for file_path in files:
                get_media_info(file_path)
                
        elif choice == '3':
            create_dummy_files()
            
        elif choice == '4':
            print("Terima kasih! 👋")
            break
            
        else:
            print("❌ Pilihan tidak valid!")


def create_dummy_files():
    """
    Membuat file dummy untuk testing
    """
    print("\nMembuat file dummy untuk pengujian...")
    dummy_files = []
    
    # a. Dummy Gambar (PNG & JPG)
    try:
        img = Image.new('RGB', (200, 100), color = 'red')
        img.save('test_image.png', 'PNG')
        img.save('test_image.jpg', 'JPEG')
        dummy_files.extend(['test_image.png', 'test_image.jpg'])
        print("✅ File gambar dummy berhasil dibuat")
    except Exception as e:
        print(f"❌ Gagal membuat file gambar: {e}")

    # b. Dummy Video (MP4) dan Audio (MP3)
    # Ini memerlukan program ffmpeg sudah terinstal di sistem Anda
    try:
        # Video: H.264 + AAC dalam .mp4
        (
            ffmpeg
            .input('lavfi:testsrc=size=192x108:rate=1:duration=1', format='lavfi') # Sumber video tes
            .input('lavfi:sine=frequency=1000:duration=1', format='lavfi') # Sumber audio tes
            .output('test_video.mp4', vcodec='libx264', acodec='aac', shortest=None, loglevel='quiet')
            .overwrite_output()
            .run()
        )
        
        # Audio: MP3
        (
            ffmpeg
            .input('lavfi:sine=frequency=440:duration=2', format='lavfi')
            .output('test_audio.mp3', acodec='libmp3lame', loglevel='quiet')
            .overwrite_output()
            .run()
        )
        dummy_files.extend(['test_video.mp4', 'test_audio.mp3'])
        print("✅ File media dummy berhasil dibuat")
        
    except FileNotFoundError:
         print("\n⚠️ PERINGATAN: Program 'ffmpeg' tidak ditemukan.")
         print("Silakan instal ffmpeg di sistem Anda untuk menganalisis file video/audio.")
         print("Melewatkan pembuatan file media dummy.\n")
    except Exception as e:
        print(f"❌ Gagal membuat file media: {e}")

    # Analisis file dummy yang berhasil dibuat
    if dummy_files:
        print(f"\n📊 Menganalisis {len(dummy_files)} file dummy...")
        for f in dummy_files:
            get_media_info(f)
            
        # Tanya apakah ingin menghapus file dummy
        delete = input("\nHapus file dummy? (y/n): ").strip().lower()
        if delete in ['y', 'yes']:
            for f in dummy_files:
                if os.path.exists(f):
                    os.remove(f)
            print("✅ File dummy berhasil dihapus")


# --- Bagian Utama untuk Menjalankan Contoh ---
if __name__ == "__main__":
    try:
        analyze_files_from_input()
    except KeyboardInterrupt:
        print("\n\nProgram dihentikan oleh pengguna. Sampai jumpa! 👋")
    except Exception as e:
        print(f"\n❌ Terjadi error tidak terduga: {e}")