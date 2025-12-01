# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all, collect_submodules

# Collect all flet dependencies
flet_datas, flet_binaries, flet_hiddenimports = collect_all('flet')

# Collect all submodules for critical packages
hiddenimports = [
    'flet',
    'flet.core',
    'flet.utils',
    'flet_core',
    'flet_runtime',
    'pydub',
    'pydub.effects',
    'pydub.silence',
    'pydub.utils',
    'PIL',
    'PIL.Image',
    'filetype',
    'yt_dlp',
    'yt_dlp.extractor',
    'ffmpeg',
]

# Add all tool modules
tool_modules = [
    'audio_merger_gui',
    'audio_merger',
    'media_codec_detector_gui',
    'media_codec_detector',
    'batch_downloader_gui_flet',
    'batch_downloader_gui',
    'batch_downloader',
    'playlist_downloader_gui_flet',
    'playlist_downloader_gui',
    'playlist_downloader',
    'socmed_downloader_gui',
    'socmed_downloader',
    'batch_reader',
    'media_looper_gui_flet',
    'media_looper_cli',
    'language_config',
]

hiddenimports.extend(tool_modules)
hiddenimports.extend(flet_hiddenimports)

# Data files to include
datas = [
    ('language_config.py', '.'),
    ('audio-merger/*.py', 'audio-merger'),
    ('media-codec-detector/*.py', 'media-codec-detector'),
    ('yt-batch-downloader/*.py', 'yt-batch-downloader'),
    ('yt-playlist-downloader/*.py', 'yt-playlist-downloader'),
    ('socmed-downloader/*.py', 'socmed-downloader'),
    ('media-looper/*.py', 'media-looper'),
    ('media-looper/bg/*.png', 'media-looper/bg'),
]
datas.extend(flet_datas)

a = Analysis(
    ['media_tools_launcher.py'],
    pathex=['audio-merger', 'media-codec-detector', 'yt-batch-downloader', 
            'yt-playlist-downloader', 'socmed-downloader', 'media-looper'],
    binaries=flet_binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='MediaToolsZakkutsu',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
