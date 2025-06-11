"""
MEOW Format Setup Script
Installs dependencies and sets up file associations
"""

import sys
import subprocess
import os
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required Python packages"""
    print("\nInstalling dependencies...")
    
    try:
        # Install packages
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False


def test_installation():
    """Test if the installation works"""
    print("\nTesting installation...")
    
    try:
        # Test imports
        from meow_format import MeowFormat
        from PIL import Image
        import numpy as np
        
        print("✓ All modules imported successfully")
        
        # Test basic functionality
        meow = MeowFormat()
        print("✓ MeowFormat class initialized")
        
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


def create_desktop_shortcuts():
    """Create desktop shortcuts (Windows only)"""
    if platform.system() != "Windows":
        print("Desktop shortcuts only supported on Windows")
        return
    
    print("\nCreating desktop shortcuts...")
    
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        script_dir = Path(__file__).parent.absolute()
        
        # Create shortcut for GUI
        shortcut = Dispatch('WScript.Shell').CreateShortCut(
            os.path.join(desktop, "MEOW Format Manager.lnk")
        )
        shortcut.Targetpath = sys.executable
        shortcut.Arguments = f'"{script_dir / "meow_gui.py"}"'
        shortcut.WorkingDirectory = str(script_dir)
        shortcut.IconLocation = sys.executable
        shortcut.save()
        
        print("✓ Desktop shortcut created")
        
    except ImportError:
        print("! Could not create desktop shortcuts (winshell not available)")
    except Exception as e:
        print(f"! Could not create desktop shortcuts: {e}")


def setup_file_associations():
    """Setup file associations for .meow files (Windows only)"""
    if platform.system() != "Windows":
        print("File associations only supported on Windows")
        return
    
    print("\nSetting up file associations...")
    print("Note: This requires administrator privileges")
    
    script_dir = Path(__file__).parent.absolute()
    viewer_path = script_dir / "meow_viewer.py"
    
    # Create registry entries
    reg_commands = [
        f'reg add "HKEY_CLASSES_ROOT\\.meow" /ve /d "MEOWImageFile" /f',
        f'reg add "HKEY_CLASSES_ROOT\\MEOWImageFile" /ve /d "MEOW Image File" /f',
        f'reg add "HKEY_CLASSES_ROOT\\MEOWImageFile\\shell\\open\\command" /ve /d "\\"{sys.executable}\\" \\"{viewer_path}\\" \\"%1\\"" /f'
    ]
    
    try:
        for cmd in reg_commands:
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print("✓ File associations created")
    except subprocess.CalledProcessError:
        print("! Could not create file associations (requires admin privileges)")
        print("  You can manually associate .meow files with meow_viewer.py")


def main():
    """Main setup function"""
    print("MEOW File Format Setup")
    print("=" * 30)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        sys.exit(1)
    
    # Optional setup steps
    response = input("\nDo you want to create desktop shortcuts? (y/n): ")
    if response.lower() in ['y', 'yes']:
        create_desktop_shortcuts()
    
    response = input("\nDo you want to set up file associations for .meow files? (y/n): ")
    if response.lower() in ['y', 'yes']:
        setup_file_associations()
    
    print("\n" + "=" * 30)
    print("Setup completed successfully!")
    print("\nYou can now use:")
    print("- python meow_gui.py (Complete GUI)")
    print("- python meow_viewer.py <file.meow> (Simple viewer)")
    print("- python meow_converter.py (Command line tools)")
    print("- launch_meow.bat (Windows launcher)")
    
    print("\nTo test the installation:")
    print("- python test_meow.py")


if __name__ == "__main__":
    # Change to script directory
    os.chdir(Path(__file__).parent)
    main()
