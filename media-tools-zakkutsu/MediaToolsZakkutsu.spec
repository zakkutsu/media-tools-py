# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

# Collect all flet dependencies
flet_datas, flet_binaries, flet_hiddenimports = collect_all('flet')

# Hidden imports
hiddenimports = [
    # Flet
    'flet',
    'flet_core',
    'flet_runtime',
    # Media processing
    'pydub',
    'pydub.effects',
    'pydub.silence',
    'pydub.utils',
    'PIL',
    'PIL.Image',
    'filetype',
    'ffmpeg',
    # Downloaders
    'yt_dlp',
    'yt_dlp.extractor',
    # All tool modules
    'audio_merger',
    'audio_merger_gui',
    'media_codec_detector',
    'media_codec_detector_gui',
    'batch_downloader',
    'batch_downloader_gui_flet',
    'playlist_downloader',
    'playlist_downloader_gui_flet',
    'socmed_downloader',
    'socmed_downloader_gui',
    'batch_reader',
    'media_looper_cli',
    'media_looper_gui_flet',
    'language_config',
]

hiddenimports.extend(flet_hiddenimports)

# Data files
datas = [
    ('language_config.py', '.'),
    ('tools/*.py', 'tools'),
]

datas.extend(flet_datas)

a = Analysis(
    ['main.py'],
    pathex=['tools'],
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
