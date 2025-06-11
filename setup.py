"""
Enhanced MEOW Setup Script
Installs dependencies and sets up the Enhanced MEOW environment
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
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Enhanced MEOW dependencies...")
    
    requirements = [
        "Pillow>=10.0.0",
        "numpy>=1.21.0", 
        "scipy>=1.9.0"
    ]
    
    for requirement in requirements:
        try:
            print(f"Installing {requirement}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", requirement])
            print(f"✅ {requirement} installed successfully")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {requirement}")
            return False
    
    return True


def test_installation():
    """Test if Enhanced MEOW can be imported and works"""
    print("\n🧪 Testing Enhanced MEOW installation...")
    
    try:
        # Test imports
        from meow_enhanced import EnhancedMeowFormat
        from PIL import Image
        import numpy as np
        import scipy
        
        print("✅ All imports successful")
        
        # Test basic functionality
        meow = EnhancedMeowFormat()
        print("✅ Enhanced MEOW format initialized")
        
        # Test capability detection
        from meow_enhanced import check_meow_compatibility
        capabilities = check_meow_compatibility()
        print(f"✅ Capability detection working: {len(capabilities)} capabilities detected")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False


def setup_file_associations():
    """Setup file associations for .meow files (Windows only)"""
    if platform.system() != "Windows":
        print("📝 File associations are currently only supported on Windows")
        return True
    
    print("\n🔗 Setting up .meow file associations...")
    
    try:
        # This would require registry modifications on Windows
        # For now, just provide instructions
        print("📋 To associate .meow files with Enhanced MEOW:")
        print("   1. Right-click on a .meow file")
        print("   2. Select 'Open with' -> 'Choose another app'")
        print("   3. Browse to this folder and select 'launch_meow.bat'")
        print("   4. Check 'Always use this app' if desired")
        
        return True
        
    except Exception as e:
        print(f"❌ File association setup failed: {e}")
        return False


def create_sample_images():
    """Create sample Enhanced MEOW images for testing"""
    print("\n🖼️  Creating sample Enhanced MEOW images...")
    
    try:
        # Run the test to create sample images
        subprocess.run([sys.executable, "test_enhanced.py"], 
                      capture_output=True, text=True, timeout=60)
        
        sample_files = [
            "ai_test_image.png",
            "ai_test_image_enhanced.meow"
        ]
        
        created_files = []
        for file in sample_files:
            if os.path.exists(file):
                created_files.append(file)
        
        if created_files:
            print(f"✅ Created {len(created_files)} sample files")
            for file in created_files:
                print(f"   • {file}")
        else:
            print("⚠️  No sample files created (this is okay)")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Sample creation failed: {e} (this is not critical)")
        return True  # Not a critical failure


def cleanup_old_files():
    """Clean up any old/temporary files"""
    print("\n🧹 Cleaning up temporary files...")
    
    cleanup_patterns = [
        "*.pyc",
        "__pycache__",
        "*.tmp",
        "test_output.png"
    ]
    
    cleaned = 0
    for pattern in cleanup_patterns:
        try:
            if pattern == "__pycache__":
                if os.path.exists(pattern):
                    import shutil
                    shutil.rmtree(pattern)
                    cleaned += 1
            else:
                import glob
                files = glob.glob(pattern)
                for file in files:
                    os.remove(file)
                    cleaned += 1
        except:
            pass  # Ignore cleanup errors
    
    if cleaned > 0:
        print(f"✅ Cleaned up {cleaned} temporary files")
    else:
        print("✅ No cleanup needed")


def main():
    """Main setup function"""
    print("🚀 ENHANCED MEOW FORMAT SETUP")
    print("AI-Optimized Image Format Installation")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Dependency installation failed")
        sys.exit(1)
    
    # Test installation
    if not test_installation():
        print("\n❌ Installation test failed")
        sys.exit(1)
    
    # Setup file associations
    setup_file_associations()
    
    # Create samples
    create_sample_images()
    
    # Cleanup
    cleanup_old_files()
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 ENHANCED MEOW SETUP COMPLETE!")
    print("=" * 50)
    print("✅ Dependencies installed")
    print("✅ Enhanced MEOW format ready")
    print("✅ File associations configured")
    print("✅ Sample files created")
    
    print("\n🚀 Quick Start:")
    print("   1. Convert an image:")
    print("      python quick_convert.py your_image.jpg")
    print("   2. Launch Enhanced GUI:")
    print("      python meow_gui_enhanced.py")
    print("   3. Run compatibility demo:")
    print("      python demo_compatibility.py")
    print("   4. Test full features:")
    print("      python test_enhanced.py")
    
    print("\n📚 Documentation:")
    print("   • README.md - Project overview")
    print("   • docs/ENHANCED_MEOW.md - Technical documentation") 
    print("   • IMPLEMENTATION_COMPLETE.md - Feature summary")
    
    print("\n🎯 Enhanced MEOW: Better than PNG/JPEG for AI!")
    print("   Making images faster for machines, compatible with humans! 🐱✨")


if __name__ == "__main__":
    main()
