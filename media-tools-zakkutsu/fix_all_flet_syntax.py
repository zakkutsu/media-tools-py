#!/usr/bin/env python3
"""
Script untuk memperbaiki Flet syntax compatibility dari 0.21.x ke 0.25.x
Mengganti ft.Icons.XXX -> ft.icons.XXX dan ft.Colors.XXX -> ft.colors.XXX
"""

import os
import re
from pathlib import Path

# Files yang perlu diperbaiki
TARGET_FILES = [
    'tools/audio_merger_gui.py',
    'tools/media_codec_detector_gui.py',
    'tools/batch_downloader_gui_flet.py',
    'tools/playlist_downloader_gui_flet.py',
    'tools/socmed_downloader_gui.py',
    'main.py'
]

def fix_flet_syntax(content):
    """Fix Flet syntax from 0.21.x to 0.25.x"""
    
    # Fix ft.Icons.XXX -> ft.icons.XXX
    # Match ft.Icons.WORD_WITH_UNDERSCORES
    content = re.sub(r'\bft\.Icons\.([A-Z_]+)', r'ft.icons.\1', content)
    
    # Fix ft.Colors.XXX -> ft.colors.XXX (keep uppercase after dots)
    content = re.sub(r'\bft\.Colors\.([A-Z_0-9]+)', r'ft.colors.\1', content)
    
    # Fix specific cases
    replacements = {
        'ft.Icons.': 'ft.icons.',
        'ft.Colors.': 'ft.colors.',
        'icons.icons.': 'ft.icons.',  # Fix double replacement
        'colors.colors.': 'ft.colors.',  # Fix double replacement
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    return content

def add_shutil_import(content, filepath):
    """Add shutil import if not present"""
    if 'import shutil' in content:
        return content
    
    # Add after other standard library imports
    lines = content.split('\n')
    import_index = -1
    
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_index = i
        elif import_index >= 0 and not (line.startswith('import ') or line.startswith('from ') or line.strip() == ''):
            # Found end of imports
            lines.insert(import_index + 1, 'import shutil')
            break
    
    return '\n'.join(lines)

def fix_hardcoded_paths(content, filepath):
    """Fix hardcoded paths to use portable methods"""
    
    if 'audio_merger_gui.py' in filepath:
        # Already fixed in previous operation
        pass
    
    # Ensure Path is imported
    if 'from pathlib import Path' not in content and 'import pathlib' not in content:
        content = add_pathlib_import(content)
    
    return content

def add_pathlib_import(content):
    """Add pathlib import if not present"""
    if 'from pathlib import Path' in content or 'import pathlib' in content:
        return content
    
    lines = content.split('\n')
    import_index = -1
    
    for i, line in enumerate(lines):
        if line.startswith('import ') or line.startswith('from '):
            import_index = i
        elif import_index >= 0 and not (line.startswith('import ') or line.startswith('from ') or line.strip() == ''):
            lines.insert(import_index + 1, 'from pathlib import Path')
            break
    
    return '\n'.join(lines)

def process_file(filepath):
    """Process a single file"""
    filepath_str = str(filepath)
    print(f"Processing: {filepath_str}")
    
    try:
        with open(filepath_str, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply fixes
        content = add_shutil_import(content, filepath_str)
        content = fix_flet_syntax(content)
        content = fix_hardcoded_paths(content, filepath_str)
        
        # Only write if changed
        if content != original_content:
            # Backup original
            backup_path = filepath_str + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(original_content)
            print(f"  ✓ Backup created: {backup_path}")
            
            # Write fixed version
            with open(filepath_str, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✓ Fixed and saved")
            return True
        else:
            print(f"  - No changes needed")
            return False
    
    except Exception as e:
        print(f"  ✗ Error: {e}")
        return False

def main():
    """Main function"""
    script_dir = Path(__file__).parent
    print("=" * 60)
    print("Flet Syntax Fixer - v1.0")
    print("Fixing compatibility: Flet 0.21.x → 0.25.x")
    print("=" * 60)
    print()
    
    fixed_count = 0
    total_count = 0
    
    for target_file in TARGET_FILES:
        filepath = script_dir / target_file
        if filepath.exists():
            total_count += 1
            if process_file(filepath):
                fixed_count += 1
        else:
            print(f"Warning: File not found: {filepath}")
    
    print()
    print("=" * 60)
    print(f"Summary: Fixed {fixed_count}/{total_count} files")
    print("=" * 60)
    
    if fixed_count > 0:
        print()
        print("✓ All fixes applied successfully!")
        print("  - ft.Icons.XXX → ft.icons.XXX")
        print("  - ft.Colors.XXX → ft.colors.XXX")
        print("  - Added shutil imports where needed")
        print()
        print("Backup files created with .backup extension")
        print("Test the application before deleting backups!")
    else:
        print()
        print("No changes were needed.")

if __name__ == '__main__':
    main()
