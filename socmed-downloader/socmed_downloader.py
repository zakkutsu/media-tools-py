import yt_dlp
import os
import sys

# --- KONFIGURASI BROWSER UNTUK FB/IG ---
# Jika gagal download FB/IG karena minta login,
# ubah nilai ini menjadi nama browser yang sedang kamu pakai login.
# Pilihan: 'chrome', 'firefox', 'edge', 'brave', 'opera'
# Jika tidak butuh cookies, biarkan None.
BROWSER_COOKIES = None 
# Contoh jika pakai Chrome: BROWSER_COOKIES = 'chrome'


def progress_hook(d):
    """Fungsi untuk menampilkan status download di terminal agar tidak sepi."""
    if d['status'] == 'downloading':
        # Menampilkan persentase agar terlihat prosesnya
        percent = d.get('_percent_str', 'N/A')
        speed = d.get('_speed_str', 'N/A')
        sys.stdout.write(f"\r[Sedang Download] Progress: {percent} | Speed: {speed}")
        sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\n[Selesai] Download rampung. Sedang memproses akhir (FFmpeg)...")

def run_downloader():
    while True: # Looping agar program tidak langsung keluar setelah selesai
        print("\n" + "="*50)
        print("   SOCMED DOWNLOADER   ")
        print("   (YT, TikTok, IG, FB, Twitter/X)   ")
        print("="*50)
        url = input(">> Masukkan Link (atau ketik 'exit' untuk keluar): ").strip()
        
        if url.lower() in ['exit', 'keluar', 'q']:
            print("Sampai jumpa!")
            break
        
        if not url: continue # Skip jika input kosong

        print("\n>> Pilih Format:")
        print("1. Video")
        print("2. Audio (MP3)")
        pilihan = input(">> Pilihan (1/2): ").strip()
        
        # Quality selection for video
        quality = "best"
        if pilihan == '1':
            print("\n>> Pilih Kualitas Video:")
            print("1. Terbaik (Otomatis)")
            print("2. 1080p (Full HD)")
            print("3. 720p (HD)")
            print("4. 480p (SD)")
            quality_choice = input(">> Pilihan (1/2/3/4): ").strip()
            
            quality_map = {
                '1': 'best',
                '2': '1080',
                '3': '720',
                '4': '480'
            }
            quality = quality_map.get(quality_choice, 'best')

        # === Settingan Inti yt-dlp ===
        ydl_opts = {
            # Nama file output: Judul Asli.Ekstensi
            'outtmpl': '%(title)s.%(ext)s', 
            
            # Memanggil fungsi hook untuk tampilan progress
            'progress_hooks': [progress_hook],
            
            # Agar tidak berhenti total jika ada 1 video error di playlist
            'ignoreerrors': True, 
            
            # Agar tampilan terminal tidak terlalu penuh sampah teks
            'quiet': True, 
            'no_warnings': True,
        }
        
        # --- Logika Pilihan Format ---
        if pilihan == '2':
            # Setting Audio MP3
            print("\n[Info] Mode: Audio MP3 Selected")
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192', # Bitrate 192kbps (standar bagus)
                }],
            })
        else:
            # Setting Video dengan quality selector
            print(f"\n[Info] Mode: Video Selected (Quality: {quality})")
            if quality == 'best':
                format_str = 'bestvideo+bestaudio/best'
            elif quality == '1080':
                format_str = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            elif quality == '720':
                format_str = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            elif quality == '480':
                format_str = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            else:
                format_str = 'bestvideo+bestaudio/best'
            
            ydl_opts.update({
                'format': format_str,
            })

        # --- Logika Cookies untuk FB/IG ---
        if BROWSER_COOKIES:
             print(f"[Info] Menggunakan cookies dari browser: {BROWSER_COOKIES} (untuk bypass login FB/IG)")
             ydl_opts['cookiesfrombrowser'] = (BROWSER_COOKIES,) # Tuple format


        print("\n--- Memulai Proses ---")
        # === Eksekusi Download ===
        try:
            # Membuka yt-dlp dengan settingan di atas
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Ambil info dulu untuk memastikan link valid & menampilkan judul
                info = ydl.extract_info(url, download=False) 
                judul = info.get('title', 'Unknown Title')
                site = info.get('extractor_key', 'Unknown Site')
                
                print(f"[Target Detect] Situs: {site} | Judul: {judul}")
                print("Sedang mendownload...")
                
                # Lakukan download
                ydl.download([url])
                
            print(f"\n✅ SUKSES! File tersimpan di folder ini.")
            
        except Exception as e:
            # Menangkap error jika link tidak valid atau masalah lain
            print(f"\n❌ GAGAL: Terjadi kesalahan.")
            print(f"Error details: {e}")

# Agar skrip hanya jalan jika dieksekusi langsung, bukan di-import
if __name__ == "__main__":
    # Memastikan file tersimpan di folder tempat skrip berada
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_downloader()
