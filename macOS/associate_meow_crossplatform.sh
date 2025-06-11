#!/bin/bash
# Cross-Platform MEOW File Association Setup
# Works on macOS, Linux, and other Unix-like systems

set -e

OS_TYPE=$(uname -s)
echo "🐾 MEOW File Association Setup"
echo "Detected OS: $OS_TYPE"
echo "=============================="

case "$OS_TYPE" in
    "Darwin")
        echo "🍎 Setting up for macOS..."
        
        # Check for duti (preferred method)
        if command -v duti &> /dev/null; then
            echo "📱 Using duti..."
            duti -s com.apple.Preview .meow all
            echo "✅ Associated .meow with Preview via duti"
            
        # Check for Homebrew and offer to install duti
        elif command -v brew &> /dev/null; then
            echo "🍺 Homebrew detected. Installing duti..."
            brew install duti
            duti -s com.apple.Preview .meow all
            echo "✅ Installed duti and associated .meow with Preview"
            
        else
            echo "📝 Manual setup required:"
            echo "   1. Install duti: brew install duti"
            echo "   2. Or manually associate in Finder:"
            echo "      • Right-click a .meow file"
            echo "      • Get Info → Open with: Preview"
            echo "      • Click 'Change All...'"
        fi
        ;;
        
    "Linux")
        echo "🐧 Setting up for Linux..."
        
        # Check for xdg-utils (most Linux distributions)
        if command -v xdg-mime &> /dev/null; then
            # Create MIME type for MEOW files
            echo "📋 Creating MIME type for .meow files..."
            
            # Add MIME type
            cat > ~/.local/share/mime/packages/meow-image.xml << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<mime-info xmlns="http://www.freedesktop.org/standards/shared-mime-info">
    <mime-type type="image/x-meow">
        <comment>MEOW Image File</comment>
        <glob pattern="*.meow"/>
        <sub-class-of type="image/png"/>
    </mime-type>
</mime-info>
EOF
            
            # Update MIME database
            update-mime-database ~/.local/share/mime/
            
            # Set default application (try common image viewers)
            if command -v eog &> /dev/null; then
                xdg-mime default eog.desktop image/x-meow
                echo "✅ Associated .meow with Eye of GNOME (eog)"
            elif command -v gwenview &> /dev/null; then
                xdg-mime default gwenview.desktop image/x-meow
                echo "✅ Associated .meow with Gwenview"
            elif command -v feh &> /dev/null; then
                xdg-mime default feh.desktop image/x-meow
                echo "✅ Associated .meow with feh"
            else
                echo "⚠️  No common image viewer found"
                echo "   Install one: sudo apt install eog (Ubuntu/Debian)"
                echo "   Or: sudo dnf install eog (Fedora)"
            fi
            
        else
            echo "❌ xdg-utils not found"
            echo "   Install: sudo apt install xdg-utils"
        fi
        ;;
        
    "FreeBSD"|"OpenBSD"|"NetBSD")
        echo "😈 Setting up for BSD..."
        echo "📝 Manual setup required:"
        echo "   • Add MIME type to /usr/local/share/mime/"
        echo "   • Configure default application in desktop environment"
        ;;
        
    *)
        echo "❓ Unknown OS: $OS_TYPE"
        echo "📝 Manual setup required for your system"
        ;;
esac

# Test the association
echo ""
echo "🧪 Testing file association..."

# Look for test files
TEST_FILES=("test.meow" "assets/sample-images/test.meow" "demo_steganographic.meow" "test_for_gui.meow")
TEST_FILE=""

for file in "${TEST_FILES[@]}"; do
    if [ -f "$file" ]; then
        TEST_FILE="$file"
        break
    fi
done

if [ -n "$TEST_FILE" ]; then
    echo "📄 Found test file: $TEST_FILE"
    
    case "$OS_TYPE" in
        "Darwin")
            echo "💡 Test with: open '$TEST_FILE'"
            ;;
        "Linux")
            echo "💡 Test with: xdg-open '$TEST_FILE'"
            if command -v xdg-open &> /dev/null; then
                echo "🚀 Opening test file..."
                xdg-open "$TEST_FILE" &
            fi
            ;;
    esac
else
    echo "⚠️  No test .meow file found"
    echo "💡 Create one with: python meow_format.py some_image.png"
fi

echo ""
echo "✅ Cross-platform MEOW file association setup complete!"
echo ""
echo "🌟 Key Benefits:"
echo "   📱 .meow files open as images in default viewers"
echo "   🤖 MEOW-aware apps can extract AI metadata"
echo "   🔄 True cross-compatibility across platforms"
echo "   💾 Files work even when renamed to .png"
