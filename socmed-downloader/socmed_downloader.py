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

def batch_download():
    """Download multiple videos from a batch file"""
    print("\n" + "="*50)
    print("   BATCH DOWNLOAD MODE   ")
    print("="*50)
    print("\nSupported file formats:")
    print("  - TXT: 1 link per line")
    print("  - CSV: url,quality,format")
    print("  - JSON: Array of {url, quality, format}")
    print("  - Excel (.xlsx): Columns A,B,C")
    print("  - Word (.docx): Links in paragraphs")
    
    file_path = input("\n>> Masukkan path file batch: ").strip().strip('"').strip("'")
    
    if not file_path:
        print("❌ Path file kosong!")
        return
    
    try:
        from batch_reader import read_batch_file
        
        print("\n[Info] Membaca file batch...")
        links = read_batch_file(file_path)
        
        if not links:
            print("❌ Tidak ada link ditemukan dalam file!")
            return
        
        print(f"✅ Ditemukan {len(links)} link untuk didownload")
        
        # Ask for default format and quality
        print("\n>> Pilih Format Default:")
        print("1. Video")
        print("2. Audio (MP3)")
        format_choice = input(">> Pilihan (1/2): ").strip()
        
        default_format = 'video' if format_choice == '1' else 'audio'
        
        default_quality = 'best'
        if format_choice == '1':
            print("\n>> Pilih Kualitas Video Default:")
            print("1. Terbaik (Otomatis)")
            print("2. 1080p (Full HD)")
            print("3. 720p (HD)")
            print("4. 480p (SD)")
            quality_choice = input(">> Pilihan (1/2/3/4): ").strip()
            
            quality_map = {'1': 'best', '2': '1080', '3': '720', '4': '480'}
            default_quality = quality_map.get(quality_choice, 'best')
        
        # Process each link
        success_count = 0
        failed_count = 0
        
        for i, link_data in enumerate(links, 1):
            url = link_data['url']
            quality = link_data.get('quality', default_quality)
            format_type = link_data.get('format', default_format)
            
            print(f"\n{'='*50}")
            print(f"[{i}/{len(links)}] Processing: {url}")
            print(f"{'='*50}")
            
            try:
                # Base options
                ydl_opts = {
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [progress_hook],
                    'ignoreerrors': True,
                    'quiet': True,
                    'no_warnings': True,
                }
                
                # Format selection
                if format_type == 'audio':
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': '192',
                        }],
                    })
                else:
                    # Video with quality
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
                    
                    ydl_opts['format'] = format_str
                
                # Add cookies if configured
                if BROWSER_COOKIES:
                    ydl_opts['cookiesfrombrowser'] = (BROWSER_COOKIES,)
                
                # Download
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    title = info.get('title', 'Unknown')
                    print(f"[Downloading] {title}")
                    ydl.download([url])
                
                print(f"✅ [{i}/{len(links)}] Sukses!")
                success_count += 1
                
            except Exception as e:
                print(f"❌ [{i}/{len(links)}] Gagal: {e}")
                failed_count += 1
        
        # Summary
        print(f"\n{'='*50}")
        print(f"   BATCH DOWNLOAD SELESAI   ")
        print(f"{'='*50}")
        print(f"Total: {len(links)} | Sukses: {success_count} | Gagal: {failed_count}")
        
    except Exception as e:
        print(f"\n❌ Error membaca file: {e}")

def run_downloader():
    while True: # Looping agar program tidak langsung keluar setelah selesai
        print("\n" + "="*50)
        print("   SOCMED DOWNLOADER   ")
        print("   (YT, TikTok, IG, FB, Twitter/X)   ")
        print("="*50)
        print("\n>> Pilih Mode:")
        print("1. Single Download (1 link)")
        print("2. Batch Download (dari file)")
        print("3. Exit")
        mode = input(">> Pilihan (1/2/3): ").strip()
        
        if mode == '3' or mode.lower() in ['exit', 'keluar', 'q']:
            print("Sampai jumpa!")
            break
        
        if mode == '2':
            # Batch download mode
            batch_download()
            continue
        
        # Single download mode
        url = input("\n>> Masukkan Link: ").strip()
        
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
