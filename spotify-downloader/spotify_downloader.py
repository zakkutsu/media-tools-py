import subprocess
import os
import sys

def check_spotdl_installed():
    """Mengecek apakah spotdl sudah terinstall di sistem."""
    try:
        subprocess.run(["spotdl", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def run_spotify_downloader():
    print("\n" + "="*45)
    print("   SPOTIFY DOWNLOADER (via YouTube Match)   ")
    print("   Powered by: spotdl")
    print("="*45)
    
    if not check_spotdl_installed():
        print("❌ Error: Library 'spotdl' belum terinstall.")
        print(">> Silakan ketik: pip install spotdl")
        return

    # Input Link
    url = input(">> Masukkan Link (Lagu/Album/Playlist Spotify): ").strip()
    
    if not url:
        print("Input kosong.")
        return

    # Folder Output
    output_folder = "Music_Downloads"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        
    print(f"\n📂 File akan disimpan di folder: /{output_folder}")
    print("🚀 Sedang mencari dan mencocokkan lagu...")
    print("(Proses ini tidak butuh login, tapi butuh koneksi stabil)\n")

    # Command spotdl
    cmd = [
        'spotdl',
        url,
        '--output', output_folder,
        '--format', 'mp3',
        '--bitrate', '320k',
        '--lyrics',
        '--m3u'
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Selesai! Cek folder '{output_folder}'.")
        
    except subprocess.CalledProcessError:
        print("\n❌ Terjadi kesalahan saat download.")
        print("Tips: Pastikan link valid dan internet stabil.")
    except KeyboardInterrupt:
        print("\n⛔ Dibatalkan oleh user.")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_spotify_downloader()
