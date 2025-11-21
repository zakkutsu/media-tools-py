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
            "folder_input": "📁 Pilih Folder Audio",
            "folder_output": "📂 Folder Tujuan Penyimpanan",
            "file_naming": "Nama File Output",
            "effects": "Efek Transisi",
            "normal": "🔗 Gabungan Langsung (Tanpa Efek)",
            "crossfade": "🔄 Crossfade (Transisi Halus)",
            "gap": "⏸️ Gap/Jeda (Silence antar lagu)",
            "auto_numbering": "🔢 Auto Number Files",
            "start_merge": "🎵 Mulai Gabungkan Audio",
            "ready": "Siap untuk download",
        },
        "en": {
            "title": "🎵 Audio Merger",
            "description": "Merge audio files into one with transition effects",
            "folder_input": "📁 Select Audio Folder",
            "folder_output": "📂 Output Folder",
            "file_naming": "Output File Name",
            "effects": "Transition Effects",
            "normal": "🔗 Direct Merge (No Effects)",
            "crossfade": "🔄 Crossfade (Smooth Transition)",
            "gap": "⏸️ Gap/Silence (Silence between tracks)",
            "auto_numbering": "🔢 Auto Number Files",
            "start_merge": "🎵 Start Merging Audio",
            "ready": "Ready to download",
        },
        "jp": {
            "title": "🎵 オーディオマージャー",
            "description": "トランジション効果で音声ファイルを1つに結合",
            "folder_input": "📁 音声フォルダを選択",
            "folder_output": "📂 出力フォルダ",
            "file_naming": "出力ファイル名",
            "effects": "トランジション効果",
            "normal": "🔗 直接マージ（効果なし）",
            "crossfade": "🔄 クロスフェード（スムーズな遷移）",
            "gap": "⏸️ ギャップ/無音（トラック間の無音）",
            "auto_numbering": "🔢 自動番号付け",
            "start_merge": "🎵 音声マージを開始",
            "ready": "ダウンロード準備完了",
        }
    },
    
    # YouTube Downloader common translations
    "youtube_downloader": {
        "id": {
            "quality_best": "🎬 Video (Kualitas Terbaik)",
            "quality_720p": "🎬 Video (720p - Hemat Bandwidth)",
            "quality_480p": "🎬 Video (480p - Hemat Bandwidth)",
            "audio_only": "🎵 Audio Only (MP3)",
            "download_folder": "📁 Download Folder",
            "start_download": "🚀 Start Download",
            "progress": "📊 Download Progress",
            "url_management": "🔗 URL Management",
            "add_url": "Add URL",
            "load_from_file": "📄 Load from File",
            "save_to_file": "💾 Save to File",
            "clear_all": "🗑️ Clear All",
        },
        "en": {
            "quality_best": "🎬 Video (Best Quality)",
            "quality_720p": "🎬 Video (720p - Save Bandwidth)",
            "quality_480p": "🎬 Video (480p - Save Bandwidth)",
            "audio_only": "🎵 Audio Only (MP3)",
            "download_folder": "📁 Download Folder",
            "start_download": "🚀 Start Download",
            "progress": "📊 Download Progress",
            "url_management": "🔗 URL Management",
            "add_url": "Add URL",
            "load_from_file": "📄 Load from File",
            "save_to_file": "💾 Save to File",
            "clear_all": "🗑️ Clear All",
        },
        "jp": {
            "quality_best": "🎬 動画（最高品質）",
            "quality_720p": "🎬 動画（720p - 帯域幅節約）",
            "quality_480p": "🎬 動画（480p - 帯域幅節約）",
            "audio_only": "🎵 音声のみ（MP3）",
            "download_folder": "📁 ダウンロードフォルダ",
            "start_download": "🚀 ダウンロード開始",
            "progress": "📊 ダウンロード進行状況",
            "url_management": "🔗 URL管理",
            "add_url": "URL追加",
            "load_from_file": "📄 ファイルから読み込む",
            "save_to_file": "💾 ファイルに保存",
            "clear_all": "🗑️ すべてクリア",
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
