"""
Language Configuration System for Media Tools
Stores and manages language preferences across all tools
"""

import json
from pathlib import Path

# Configuration file path
CONFIG_FILE = Path(__file__).parent / ".language_config.json"

# Default language
DEFAULT_LANGUAGE = "id"  # Indonesian

# Available languages
LANGUAGES = {
    "id": {"name": "Bahasa Indonesia", "flag": "🇮🇩"},
    "en": {"name": "English", "flag": "🇺🇸"},
    "jp": {"name": "日本語", "flag": "🇯🇵"}
}

def get_language():
    """Get current language preference"""
    try:
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                lang = config.get('language', DEFAULT_LANGUAGE)
                if lang in LANGUAGES:
                    return lang
    except Exception as e:
        print(f"Error reading language config: {e}")
    
    return DEFAULT_LANGUAGE

def set_language(lang_code):
    """Set language preference"""
    if lang_code not in LANGUAGES:
        raise ValueError(f"Invalid language code: {lang_code}")
    
    try:
        config = {}
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
        
        config['language'] = lang_code
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error saving language config: {e}")
        return False

def get_available_languages():
    """Get list of available languages"""
    return LANGUAGES

# Translation dictionaries for all tools
TRANSLATIONS = {
    # Common UI elements
    "common": {
        "id": {
            "back_to_home": "🏠 Kembali ke Beranda",
            "close": "Tutup",
            "cancel": "Batal",
            "ok": "OK",
            "yes": "Ya",
            "no": "Tidak",
            "browse": "Telusuri",
            "save": "Simpan",
            "load": "Muat",
            "delete": "Hapus",
            "clear": "Bersihkan",
            "reset": "Reset",
            "start": "Mulai",
            "stop": "Berhenti",
            "pause": "Jeda",
            "resume": "Lanjutkan",
            "install": "Install",
            "update": "Update",
            "language": "Bahasa",
            "select_language": "Pilih Bahasa",
        },
        "en": {
            "back_to_home": "🏠 Back to Home",
            "close": "Close",
            "cancel": "Cancel",
            "ok": "OK",
            "yes": "Yes",
            "no": "No",
            "browse": "Browse",
            "save": "Save",
            "load": "Load",
            "delete": "Delete",
            "clear": "Clear",
            "reset": "Reset",
            "start": "Start",
            "stop": "Stop",
            "pause": "Pause",
            "resume": "Resume",
            "install": "Install",
            "update": "Update",
            "language": "Language",
            "select_language": "Select Language",
        },
        "jp": {
            "back_to_home": "🏠 ホームに戻る",
            "close": "閉じる",
            "cancel": "キャンセル",
            "ok": "OK",
            "yes": "はい",
            "no": "いいえ",
            "browse": "参照",
            "save": "保存",
            "load": "読み込む",
            "delete": "削除",
            "clear": "クリア",
            "reset": "リセット",
            "start": "開始",
            "stop": "停止",
            "pause": "一時停止",
            "resume": "再開",
            "install": "インストール",
            "update": "更新",
            "language": "言語",
            "select_language": "言語を選択",
        }
    },
    
    # Main Launcher
    "launcher": {
        "id": {
            "title": "Media Tools",
            "subtitle": "Suite",
            "description": "Pilih tool yang ingin Anda gunakan",
            "tool_audio_merger": "🎵 Audio Merger",
            "tool_media_detector": "🎬 Media Codec Detector",
            "tool_batch_downloader": "📥 Batch Downloader",
            "tool_playlist_downloader": "🎵 Playlist Downloader",
            "audio_merger_desc": "Gabungkan multiple file audio menjadi satu dengan efek transisi seperti crossfade dan gap",
            "media_detector_desc": "Deteksi format kontainer dan codec dari file media (gambar, video, audio)",
            "batch_downloader_desc": "Download multiple individual YouTube videos dengan modern Flet interface",
            "playlist_downloader_desc": "Download complete YouTube playlists dengan elegant interface",
            "launch_tool": "Launch Tool",
            "select_tool": "Pilih Tool",
            "documentation": "📖 Dokumentasi",
            "system_requirements": "⚙️ System Requirements",
            "exit": "❌ Exit",
            "info_message": "Kedua tool memerlukan FFmpeg untuk berfungsi dengan optimal",
        },
        "en": {
            "title": "Media Tools",
            "subtitle": "Suite",
            "description": "Select the tool you want to use",
            "tool_audio_merger": "🎵 Audio Merger",
            "tool_media_detector": "🎬 Media Codec Detector",
            "tool_batch_downloader": "📥 Batch Downloader",
            "tool_playlist_downloader": "🎵 Playlist Downloader",
            "audio_merger_desc": "Merge multiple audio files into one with transition effects like crossfade and gap",
            "media_detector_desc": "Detect container format and codecs from media files (images, videos, audio)",
            "batch_downloader_desc": "Download multiple individual YouTube videos with modern Flet interface",
            "playlist_downloader_desc": "Download complete YouTube playlists with elegant interface",
            "launch_tool": "Launch Tool",
            "select_tool": "Select Tool",
            "documentation": "📖 Documentation",
            "system_requirements": "⚙️ System Requirements",
            "exit": "❌ Exit",
            "info_message": "Both tools require FFmpeg to function optimally",
        },
        "jp": {
            "title": "メディアツール",
            "subtitle": "スイート",
            "description": "使用するツールを選択してください",
            "tool_audio_merger": "🎵 オーディオマージャー",
            "tool_media_detector": "🎬 メディアコーデック検出器",
            "tool_batch_downloader": "📥 バッチダウンローダー",
            "tool_playlist_downloader": "🎵 プレイリストダウンローダー",
            "audio_merger_desc": "クロスフェードやギャップなどのトランジション効果で複数の音声ファイルを1つに結合",
            "media_detector_desc": "メディアファイル（画像、動画、音声）からコンテナ形式とコーデックを検出",
            "batch_downloader_desc": "モダンなFletインターフェースで複数の個別YouTube動画をダウンロード",
            "playlist_downloader_desc": "エレガントなインターフェースでYouTubeプレイリスト全体をダウンロード",
            "launch_tool": "ツールを起動",
            "select_tool": "ツールを選択",
            "documentation": "📖 ドキュメント",
            "system_requirements": "⚙️ システム要件",
            "exit": "❌ 終了",
            "info_message": "両方のツールは最適に機能するためにFFmpegが必要です",
        }
    },
    
    # Audio Merger specific translations
    "audio_merger": {
        "id": {
            "title": "🎵 Audio Merger",
            "description": "Gabungkan file audio menjadi satu dengan efek transisi",
            "step1": "1. Pilih Folder Audio",
            "step2": "3. Folder Tujuan Penyimpanan",
            "step4": "4. Pengaturan Output & Efek",
            "folder_not_selected": "📁 Belum ada folder dipilih",
            "select_audio_folder": "Pilih Folder Audio",
            "select_output_folder": "Pilih Folder Tujuan",
            "output_filename_label": "Nama File Output",
            "files_found_title": "2. File Audio Ditemukan",
            "effects": "Efek Transisi:",
            "effect_normal": "🔗 Gabungan Langsung (Tanpa Efek)",
            "effect_crossfade": "🔄 Crossfade (Transisi Halus)",
            "effect_gap": "⏸️ Gap/Jeda (Silence antar lagu)",
            "start_merge_btn": "🎵 Mulai Gabungkan Audio",
        },
        "en": {
            "title": "🎵 Audio Merger",
            "description": "Merge audio files into one with transition effects",
            "step1": "1. Select Audio Folder",
            "step2": "3. Output Folder Destination",
            "step4": "4. Output & Effect Settings",
            "folder_not_selected": "📁 No folder selected",
            "select_audio_folder": "Select Audio Folder",
            "select_output_folder": "Select Output Folder",
            "output_filename_label": "Output File Name",
            "files_found_title": "2. Audio Files Found",
            "effects": "Transition Effects:",
            "effect_normal": "🔗 Direct Merge (No Effects)",
            "effect_crossfade": "🔄 Crossfade (Smooth Transition)",
            "effect_gap": "⏸️ Gap/Silence (Silence between tracks)",
            "start_merge_btn": "🎵 Start Merging Audio",
        },
        "jp": {
            "title": "🎵 オーディオマージャー",
            "description": "トランジション効果で音声ファイルを1つに結合",
            "step1": "1. 音声フォルダを選択",
            "step2": "3. 出力フォルダの保存先",
            "step4": "4. 出力と効果の設定",
            "folder_not_selected": "📁 フォルダが選択されていません",
            "select_audio_folder": "音声フォルダを選択",
            "select_output_folder": "出力フォルダを選択",
            "output_filename_label": "出力ファイル名",
            "files_found_title": "2. 見つかった音声ファイル",
            "effects": "トランジション効果:",
            "effect_normal": "🔗 直接マージ（効果なし）",
            "effect_crossfade": "🔄 クロスフェード（スムーズな遷移）",
            "effect_gap": "⏸️ ギャップ/無音（トラック間の無音）",
            "start_merge_btn": "🎵 音声マージを開始",
        }
    },
    
    # Media Codec Detector specific translations
    "media_detector": {
        "id": {
            "title": "🎬 Media Codec Detector",
            "description": "Deteksi format kontainer dan codec dari file media",
            "step1": "1. Pilih Mode Analisis",
            "step2": "2. Pilih File/Folder Media",
            "mode_file": "📄 Analisis File Tunggal",
            "mode_folder": "📁 Analisis Semua File dalam Folder",
            "no_selection": "📁 Belum ada file/folder dipilih",
            "select_file": "Pilih File",
            "select_folder": "Pilih Folder",
            "files_found": "File Media Ditemukan",
            "start_analysis": "🕵️ Mulai Analisis",
            "analysis_results": "📊 Hasil Analisis",
            "container_format": "Format Kontainer",
            "video_codec": "Codec Video",
            "audio_codec": "Codec Audio",
            "image_format": "Format Gambar",
            "resolution": "Resolusi",
            "duration": "Durasi",
            "file_size": "Ukuran File",
            "no_codec": "Tidak ada codec",
            "analyzing": "⏳ Menganalisis...",
            "complete": "✅ Analisis Selesai!",
            "error": "❌ Error",
            "select_first": "Silakan pilih file atau folder terlebih dahulu!",
        },
        "en": {
            "title": "🎬 Media Codec Detector",
            "description": "Detect container format and codecs from media files",
            "step1": "1. Select Analysis Mode",
            "step2": "2. Select Media File/Folder",
            "mode_file": "📄 Single File Analysis",
            "mode_folder": "📁 Analyze All Files in Folder",
            "no_selection": "📁 No file/folder selected",
            "select_file": "Select File",
            "select_folder": "Select Folder",
            "files_found": "Media Files Found",
            "start_analysis": "🕵️ Start Analysis",
            "analysis_results": "📊 Analysis Results",
            "container_format": "Container Format",
            "video_codec": "Video Codec",
            "audio_codec": "Audio Codec",
            "image_format": "Image Format",
            "resolution": "Resolution",
            "duration": "Duration",
            "file_size": "File Size",
            "no_codec": "No codec",
            "analyzing": "⏳ Analyzing...",
            "complete": "✅ Analysis Complete!",
            "error": "❌ Error",
            "select_first": "Please select a file or folder first!",
        },
        "jp": {
            "title": "🎬 メディアコーデック検出器",
            "description": "メディアファイルからコンテナ形式とコーデックを検出",
            "step1": "1. 分析モードを選択",
            "step2": "2. メディアファイル/フォルダを選択",
            "mode_file": "📄 単一ファイル分析",
            "mode_folder": "📁 フォルダ内の全ファイルを分析",
            "no_selection": "📁 ファイル/フォルダが選択されていません",
            "select_file": "ファイルを選択",
            "select_folder": "フォルダを選択",
            "files_found": "見つかったメディアファイル",
            "start_analysis": "🕵️ 分析を開始",
            "analysis_results": "📊 分析結果",
            "container_format": "コンテナ形式",
            "video_codec": "動画コーデック",
            "audio_codec": "音声コーデック",
            "image_format": "画像形式",
            "resolution": "解像度",
            "duration": "再生時間",
            "file_size": "ファイルサイズ",
            "no_codec": "コーデックなし",
            "analyzing": "⏳ 分析中...",
            "complete": "✅ 分析完了！",
            "error": "❌ エラー",
            "select_first": "まずファイルまたはフォルダを選択してください！",
        }
    },
    
    # YouTube Downloader common translations (Batch & Playlist)
    "youtube_downloader": {
        "id": {
            "title_batch": "🎬 YouTube Batch Downloader",
            "title_playlist": "🎵 YouTube Playlist Downloader",
            "desc_batch": "Download multiple individual YouTube videos",
            "desc_playlist": "Download complete YouTube playlists",
            "quality_best": "🎬 Video (Kualitas Terbaik)",
            "quality_720p": "🎬 Video (720p - Hemat Bandwidth)",
            "quality_480p": "🎬 Video (480p - Hemat Bandwidth)",
            "audio_only": "🎵 Audio Only (MP3)",
            "download_folder": "📁 Folder Download",
            "select_folder": "Pilih Folder",
            "start_download": "🚀 Mulai Download",
            "stop_download": "⏹️ Stop Download",
            "progress": "📊 Progress Download",
            "url_management": "🔗 Manajemen URL",
            "url_list": "Daftar URL",
            "add_url": "Tambah URL",
            "load_from_file": "📄 Muat dari File",
            "save_to_file": "💾 Simpan ke File",
            "clear_all": "🗑️ Hapus Semua",
            "url_input": "Masukkan URL YouTube",
            "url_count": "URL dalam daftar",
            "output_template": "Template Nama File",
            "downloading": "⏳ Mengunduh...",
            "complete": "✅ Download Selesai!",
            "error": "❌ Error",
            "no_urls": "Belum ada URL di daftar!",
            "install_ytdlp": "� Install/Update yt-dlp",
            "ytdlp_status": "Status yt-dlp",
            "output_log": "📋 Log Output",
        },
        "en": {
            "title_batch": "🎬 YouTube Batch Downloader",
            "title_playlist": "🎵 YouTube Playlist Downloader",
            "desc_batch": "Download multiple individual YouTube videos",
            "desc_playlist": "Download complete YouTube playlists",
            "quality_best": "🎬 Video (Best Quality)",
            "quality_720p": "🎬 Video (720p - Save Bandwidth)",
            "quality_480p": "🎬 Video (480p - Save Bandwidth)",
            "audio_only": "🎵 Audio Only (MP3)",
            "download_folder": "📁 Download Folder",
            "select_folder": "Select Folder",
            "start_download": "🚀 Start Download",
            "stop_download": "⏹️ Stop Download",
            "progress": "📊 Download Progress",
            "url_management": "🔗 URL Management",
            "url_list": "URL List",
            "add_url": "Add URL",
            "load_from_file": "📄 Load from File",
            "save_to_file": "💾 Save to File",
            "clear_all": "🗑️ Clear All",
            "url_input": "Enter YouTube URL",
            "url_count": "URLs in list",
            "output_template": "File Name Template",
            "downloading": "⏳ Downloading...",
            "complete": "✅ Download Complete!",
            "error": "❌ Error",
            "no_urls": "No URLs in list!",
            "install_ytdlp": "📦 Install/Update yt-dlp",
            "ytdlp_status": "yt-dlp Status",
            "output_log": "📋 Output Log",
        },
        "jp": {
            "title_batch": "🎬 YouTubeバッチダウンローダー",
            "title_playlist": "🎵 YouTubeプレイリストダウンローダー",
            "desc_batch": "複数の個別YouTube動画をダウンロード",
            "desc_playlist": "YouTubeプレイリスト全体をダウンロード",
            "quality_best": "🎬 動画（最高品質）",
            "quality_720p": "🎬 動画（720p - 帯域幅節約）",
            "quality_480p": "🎬 動画（480p - 帯域幅節約）",
            "audio_only": "🎵 音声のみ（MP3）",
            "download_folder": "📁 ダウンロードフォルダ",
            "select_folder": "フォルダを選択",
            "start_download": "🚀 ダウンロード開始",
            "stop_download": "⏹️ ダウンロード停止",
            "progress": "📊 ダウンロード進行状況",
            "url_management": "🔗 URL管理",
            "url_list": "URLリスト",
            "add_url": "URL追加",
            "load_from_file": "📄 ファイルから読み込む",
            "save_to_file": "💾 ファイルに保存",
            "clear_all": "🗑️ すべてクリア",
            "url_input": "YouTube URLを入力",
            "url_count": "リスト内のURL",
            "output_template": "ファイル名テンプレート",
            "downloading": "⏳ ダウンロード中...",
            "complete": "✅ ダウンロード完了！",
            "error": "❌ エラー",
            "no_urls": "リストにURLがありません！",
            "install_ytdlp": "📦 yt-dlpをインストール/更新",
            "ytdlp_status": "yt-dlpステータス",
            "output_log": "📋 出力ログ",
        }
    }
}

def get_text(category, key, lang=None):
    """Get translated text for a specific key"""
    if lang is None:
        lang = get_language()
    
    try:
        return TRANSLATIONS[category][lang][key]
    except KeyError:
        # Fallback to Indonesian if translation not found
        try:
            return TRANSLATIONS[category]["id"][key]
        except KeyError:
            return key

def get_all_texts(category, lang=None):
    """Get all translations for a category"""
    if lang is None:
        lang = get_language()
    
    try:
        return TRANSLATIONS[category][lang]
    except KeyError:
        return TRANSLATIONS[category].get("id", {})
