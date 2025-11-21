#!/usr/bin/env python3
"""
Script to add multilingual support to all README files
Adds language selector at top and English/Japanese translations
"""

import os
from pathlib import Path

# Language selector template
LANG_SELECTOR = """# {title}

<!-- Language Selection -->
**Languages:** [🇮🇩 Bahasa Indonesia](#indonesian) | [🇺🇸 English](#english) | [🇯🇵 日本語](#japanese)

---

<a name="indonesian"></a>
## 🇮🇩 Bahasa Indonesia

"""

# Translations for each tool
TRANSLATIONS = {
    "audio-merger": {
        "title": "Audio Merger 🎵",
        "description_id": "Program Python untuk menggabungkan multiple file audio menjadi satu file menggunakan pydub dan FFmpeg.",
        "description_en": "Python program to merge multiple audio files into one using pydub and FFmpeg.",
        "description_jp": "pydubとFFmpegを使用して複数の音声ファイルを1つに結合するPythonプログラム。",
        "features_en": [
            "**Multi-format Support**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA",
            "**Crossfade Effect**: Smooth transitions between songs",
            "**Gap/Silence**: Add silence between tracks",
            "**Modern GUI**: User-friendly graphical interface (Flet)",
            "**CLI Mode**: Command line support for automation",
            "**Auto-sorting**: Files automatically sorted by name",
            "**Real-time Progress**: Detailed progress indicators"
        ],
        "features_jp": [
            "**マルチフォーマット対応**: MP3, WAV, FLAC, M4A, OGG, AAC, WMA",
            "**クロスフェード効果**: 曲間のスムーズな遷移",
            "**ギャップ/無音**: トラック間に無音を追加",
            "**モダンGUI**: ユーザーフレンドリーなグラフィカルインターフェース（Flet）",
            "**CLIモード**: 自動化のためのコマンドラインサポート",
            "**自動ソート**: ファイル名で自動的にソート",
            "**リアルタイム進行状況**: 詳細な進行状況インジケーター"
        ]
    },
    "media-codec-detector": {
        "title": "Media Codec Detector 🎬",
        "description_id": "Program Python untuk mendeteksi format kontainer dan codec dari file media.",
        "description_en": "Python program to detect container format and codecs from media files.",
        "description_jp": "メディアファイルからコンテナ形式とコーデックを検出するPythonプログラム。",
        "features_en": [
            "**Image Format Detection**: PNG, JPEG, GIF, BMP, and more",
            "**Video Analysis**: Detect video codecs (H.264, H.265, VP9, etc.)",
            "**Audio Analysis**: Detect audio codecs (MP3, AAC, FLAC, etc.)",
            "**Modern GUI**: User-friendly interface with Flet",
            "**Batch Processing**: Analyze multiple files or entire folders",
            "**Dummy File Creator**: Generate test files for demonstration"
        ],
        "features_jp": [
            "**画像形式検出**: PNG、JPEG、GIF、BMPなど",
            "**動画解析**: 動画コーデック検出（H.264、H.265、VP9など）",
            "**音声解析**: 音声コーデック検出（MP3、AAC、FLACなど）",
            "**モダンGUI**: Fletを使用したユーザーフレンドリーなインターフェース",
            "**バッチ処理**: 複数ファイルまたはフォルダ全体を解析",
            "**ダミーファイル作成**: デモンストレーション用のテストファイル生成"
        ]
    },
    "yt-batch-downloader": {
        "title": "YouTube Batch Downloader 🎬",
        "description_id": "Tool untuk mendownload multiple video YouTube individual sekaligus.",
        "description_en": "Tool to download multiple individual YouTube videos at once.",
        "description_jp": "複数の個別YouTube動画を一度にダウンロードするツール。",
        "features_en": [
            "**Batch Download**: Download multiple individual videos",
            "**Multiple Quality Options**: Best, 720p, 480p",
            "**Audio-Only Mode**: Extract MP3 with album art",
            "**URL Management**: Load/save URL lists, retry failed",
            "**Auto Numbering**: Optional file numbering",
            "**Progress Tracking**: Real-time speed, ETA, statistics",
            "**Thumbnail & Metadata**: Auto-embed for media files",
            "**Modern GUI**: Flet-based responsive interface"
        ],
        "features_jp": [
            "**バッチダウンロード**: 複数の個別動画をダウンロード",
            "**複数の品質オプション**: 最高品質、720p、480p",
            "**音声のみモード**: アルバムアート付きMP3抽出",
            "**URL管理**: URLリストの読み込み/保存、失敗の再試行",
            "**自動番号付け**: オプションのファイル番号付け",
            "**進行状況追跡**: リアルタイムの速度、ETA、統計",
            "**サムネイルとメタデータ**: メディアファイルへの自動埋め込み",
            "**モダンGUI**: Fletベースのレスポンシブインターフェース"
        ]
    },
    "yt-playlist-downloader": {
        "title": "YouTube Playlist Downloader 🎵",
        "description_id": "Tool untuk mendownload playlist YouTube lengkap dengan auto-numbering.",
        "description_en": "Tool to download complete YouTube playlists with auto-numbering.",
        "description_jp": "自動番号付けでYouTubeプレイリスト全体をダウンロードするツール。",
        "features_en": [
            "**Full Playlist Download**: Download entire playlist at once",
            "**Multiple Quality Options**: Best, 720p, 480p",
            "**Audio-Only Mode**: Extract MP3 with unified album art",
            "**Auto Numbering**: Files numbered by playlist order",
            "**Progress Tracking**: Per-video and overall progress",
            "**Resume Capability**: Continue interrupted downloads",
            "**Thumbnail & Metadata**: Auto-embed for all files",
            "**Modern GUI**: Flet-based interface"
        ],
        "features_jp": [
            "**プレイリスト全体ダウンロード**: プレイリスト全体を一度にダウンロード",
            "**複数の品質オプション**: 最高品質、720p、480p",
            "**音声のみモード**: 統一アルバムアート付きMP3抽出",
            "**自動番号付け**: プレイリスト順でファイル番号付け",
            "**進行状況追跡**: 動画ごとおよび全体の進行状況",
            "**再開機能**: 中断されたダウンロードを続行",
            "**サムネイルとメタデータ**: すべてのファイルに自動埋め込み",
            "**モダンGUI**: Fletベースのインターフェース"
        ]
    }
}

def add_language_sections(readme_path, tool_key):
    """Add language selector and translations to README"""
    
    if tool_key not in TRANSLATIONS:
        print(f"No translation data for {tool_key}")
        return
    
    trans = TRANSLATIONS[tool_key]
    
    # Read original content (Indonesian)
    with open(readme_path, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Remove old title if it exists
    lines = original_content.split('\n')
    if lines and lines[0].startswith('# '):
        original_content = '\n'.join(lines[1:]).strip()
    
    # Build English section
    english_section = f"""

---

<a name="english"></a>
## 🇺🇸 English

{trans['description_en']}

### ✨ Features

"""
    for feature in trans['features_en']:
        english_section += f"- {feature}\n"
    
    english_section += """
### 🚀 Quick Start

```bash
# 1. Navigate to folder
cd """ + tool_key + """

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run GUI
python """ + (f"{tool_key.replace('-', '_')}_gui.py" if tool_key != "yt-batch-downloader" and tool_key != "yt-playlist-downloader" else f"{tool_key.replace('yt-', '').replace('-', '_')}_gui_flet.py") + """
```

For detailed documentation, see the Indonesian section above.
"""
    
    # Build Japanese section
    japanese_section = f"""

---

<a name="japanese"></a>
## 🇯🇵 日本語

{trans['description_jp']}

### ✨ 機能

"""
    for feature in trans['features_jp']:
        japanese_section += f"- {feature}\n"
    
    japanese_section += """
### 🚀 クイックスタート

```bash
# 1. フォルダに移動
cd """ + tool_key + """

# 2. 依存関係をインストール
pip install -r requirements.txt

# 3. GUIを実行
python """ + (f"{tool_key.replace('-', '_')}_gui.py" if tool_key != "yt-batch-downloader" and tool_key != "yt-playlist-downloader" else f"{tool_key.replace('yt-', '').replace('-', '_')}_gui_flet.py") + """
```

詳細なドキュメントについては、上記のインドネシア語セクションを参照してください。
"""
    
    # Combine all sections
    new_content = LANG_SELECTOR.format(title=trans['title'])
    new_content += original_content
    new_content += english_section
    new_content += japanese_section
    
    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"✅ Updated {readme_path}")

def main():
    """Main function to process all READMEs"""
    
    base_dir = Path(__file__).parent
    
    tools = {
        "audio-merger": base_dir / "audio-merger" / "README.md",
        "media-codec-detector": base_dir / "media-codec-detector" / "README.md",
        "yt-batch-downloader": base_dir / "yt-batch-downloader" / "README.md",
        "yt-playlist-downloader": base_dir / "yt-playlist-downloader" / "README.md"
    }
    
    for tool_key, readme_path in tools.items():
        if readme_path.exists():
            print(f"\n📝 Processing {tool_key}...")
            add_language_sections(readme_path, tool_key)
        else:
            print(f"⚠️  README not found: {readme_path}")
    
    print("\n✨ All READMEs updated successfully!")

if __name__ == "__main__":
    main()
