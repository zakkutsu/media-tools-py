#!/usr/bin/env python3
"""
Media Tools Setup Script
Script untuk setup otomatis semua dependencies dan environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class MediaToolsSetup:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.venv_path = self.project_root / "venv"
        self.requirements_file = self.project_root / "requirements.txt"
        
    def print_status(self, message, status="INFO"):
        """Print status message with emoji"""
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "WARNING": "⚠️",
            "ERROR": "❌",
            "PROGRESS": "🔄"
        }
        print(f"{emoji_map.get(status, 'ℹ️')} {message}")
    
    def check_python_version(self):
        """Check if Python version is compatible"""
        self.print_status("Checking Python version...", "PROGRESS")
        
        version = sys.version_info
        if version.major < 3 or (version.major == 3 and version.minor < 8):
            self.print_status(f"Python {version.major}.{version.minor} detected. Need Python 3.8+", "ERROR")
            return False
        
        self.print_status(f"Python {version.major}.{version.minor}.{version.micro} - Compatible ✓", "SUCCESS")
        return True
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available"""
        self.print_status("Checking FFmpeg availability...", "PROGRESS")
        
        try:
            result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                self.print_status("FFmpeg is available ✓", "SUCCESS")
                return True
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass
        
        self.print_status("FFmpeg not found - Required for media processing", "WARNING")
        self.print_ffmpeg_install_instructions()
        return False
    
    def print_ffmpeg_install_instructions(self):
        """Print FFmpeg installation instructions"""
        system = platform.system().lower()
        
        print("\n📦 FFmpeg Installation Instructions:")
        if system == "windows":
            print("   • Option 1: choco install ffmpeg")
            print("   • Option 2: Download from https://ffmpeg.org/download.html")
            print("   • Option 3: winget install ffmpeg")
        elif system == "darwin":  # macOS
            print("   • brew install ffmpeg")
        else:  # Linux
            print("   • Ubuntu/Debian: sudo apt install ffmpeg")
            print("   • CentOS/RHEL: sudo yum install ffmpeg")
            print("   • Arch: sudo pacman -S ffmpeg")
        print()
    
    def create_virtual_environment(self):
        """Create virtual environment if not exists"""
        if self.venv_path.exists():
            self.print_status("Virtual environment already exists", "INFO")
            return True
        
        self.print_status("Creating virtual environment...", "PROGRESS")
        try:
            subprocess.run([sys.executable, '-m', 'venv', str(self.venv_path)], 
                          check=True, timeout=120)
            self.print_status("Virtual environment created successfully", "SUCCESS")
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            self.print_status(f"Failed to create virtual environment: {e}", "ERROR")
            return False
    
    def get_venv_python(self):
        """Get path to virtual environment Python executable"""
        if platform.system().lower() == "windows":
            return self.venv_path / "Scripts" / "python.exe"
        else:
            return self.venv_path / "bin" / "python"
    
    def get_venv_pip(self):
        """Get path to virtual environment pip executable"""
        if platform.system().lower() == "windows":
            return self.venv_path / "Scripts" / "pip.exe"
        else:
            return self.venv_path / "bin" / "pip"
    
    def install_dependencies(self):
        """Install all required dependencies"""
        if not self.requirements_file.exists():
            self.print_status("requirements.txt not found", "ERROR")
            return False
        
        self.print_status("Installing dependencies...", "PROGRESS")
        
        venv_pip = self.get_venv_pip()
        
        try:
            # Upgrade pip first (use venv python instead of venv pip for Windows compatibility)
            venv_python = self.get_venv_python()
            try:
                subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'pip'], 
                              check=True, timeout=120)
                self.print_status("Pip upgraded successfully", "SUCCESS")
            except subprocess.CalledProcessError:
                self.print_status("Pip upgrade failed, continuing with existing version", "WARNING")
            
            # Install requirements
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '-r', str(self.requirements_file)], 
                          check=True, timeout=300)
            
            # Install yt-dlp for YouTube tools
            subprocess.run([str(venv_python), '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], 
                          check=True, timeout=120)
            
            self.print_status("All dependencies installed successfully", "SUCCESS")
            return True
            
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
            self.print_status(f"Failed to install dependencies: {e}", "ERROR")
            return False
    
    def verify_installation(self):
        """Verify that all packages are properly installed"""
        self.print_status("Verifying installation...", "PROGRESS")
        
        venv_python = self.get_venv_python()
        
        required_packages = [
            'pydub', 'flet', 'ffmpeg', 'PIL', 'filetype', 'yt_dlp'
        ]
        
        failed_packages = []
        
        for package in required_packages:
            try:
                result = subprocess.run([str(venv_python), '-c', f'import {package}'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    self.print_status(f"✓ {package}", "SUCCESS")
                else:
                    failed_packages.append(package)
                    self.print_status(f"✗ {package} - {result.stderr.strip()}", "ERROR")
            except subprocess.TimeoutExpired:
                # For flet, timeout might be normal due to initialization
                if package == 'flet':
                    self.print_status(f"⚠ {package} (slow import, likely OK)", "WARNING")
                else:
                    failed_packages.append(package)
                    self.print_status(f"✗ {package} (timeout)", "ERROR")
        
        if failed_packages:
            self.print_status(f"Failed packages: {', '.join(failed_packages)}", "ERROR")
            return False
        
        self.print_status("All packages verified successfully", "SUCCESS")
        return True
    
    def create_launcher_scripts(self):
        """Create convenient launcher scripts"""
        self.print_status("Creating launcher scripts...", "PROGRESS")
        
        venv_python = self.get_venv_python()
        
        # Windows batch file
        if platform.system().lower() == "windows":
            bat_content = f"""@echo off
cd /d "{self.project_root}"
"{venv_python}" media_tools_launcher.py %*
pause
"""
            bat_path = self.project_root / "launch_media_tools.bat"
            with open(bat_path, 'w', encoding='utf-8') as f:
                f.write(bat_content)
            self.print_status(f"Created: {bat_path.name}", "SUCCESS")
        
        # Cross-platform shell script
        sh_content = f"""#!/bin/bash
cd "{self.project_root}"
"{venv_python}" media_tools_launcher.py "$@"
"""
        sh_path = self.project_root / "launch_media_tools.sh"
        with open(sh_path, 'w', encoding='utf-8') as f:
            f.write(sh_content)
        
        # Make shell script executable on Unix systems
        if platform.system().lower() != "windows":
            os.chmod(sh_path, 0o755)
        
        self.print_status(f"Created: {sh_path.name}", "SUCCESS")
    
    def run_setup(self):
        """Run complete setup process"""
        print("🎬🎵 MEDIA TOOLS SETUP 🎵🎬")
        print("=" * 50)
        
        # Step 1: Check Python version
        if not self.check_python_version():
            return False
        
        # Step 2: Check FFmpeg (warning only, not blocking)
        self.check_ffmpeg()
        
        # Step 3: Create virtual environment
        if not self.create_virtual_environment():
            return False
        
        # Step 4: Install dependencies
        if not self.install_dependencies():
            return False
        
        # Step 5: Verify installation
        if not self.verify_installation():
            return False
        
        # Step 6: Create launcher scripts
        self.create_launcher_scripts()
        
        print("\n" + "=" * 50)
        self.print_status("SETUP COMPLETED SUCCESSFULLY!", "SUCCESS")
        print("\n🚀 How to run:")
        
        if platform.system().lower() == "windows":
            print(f"   • Double-click: launch_media_tools.bat")
            print(f"   • Command line: .\\launch_media_tools.bat")
            print(f"   • PowerShell: .\\venv\\Scripts\\Activate.ps1; python media_tools_launcher.py")
        else:
            print(f"   • Command line: ./launch_media_tools.sh")
            print(f"   • Or: source venv/bin/activate && python media_tools_launcher.py")
        
        print("\n📋 Command line options:")
        print("   • --audio-merger     : Launch Audio Merger directly")
        print("   • --media-detector   : Launch Media Codec Detector directly")
        print("   • --help            : Show help")
        
        return True


def main():
    """Main setup function"""
    setup = MediaToolsSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h']:
        print("🎬🎵 Media Tools Setup Script")
        print("\nUsage: python setup_media_tools.py")
        print("\nThis script will:")
        print("  1. Check Python version compatibility")
        print("  2. Check FFmpeg availability")
        print("  3. Create virtual environment")
        print("  4. Install all required dependencies")
        print("  5. Verify installation")
        print("  6. Create convenient launcher scripts")
        return
    
    try:
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()