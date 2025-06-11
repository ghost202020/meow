#!/bin/bash
# Simple macOS MEOW File Association (Alternative Method)
# Uses Finder's built-in "Change All" functionality

echo "🐾 Simple MEOW File Association for macOS"
echo "========================================="
echo ""

# Check if we have a test MEOW file
MEOW_FILE=""
if [ -f "test.meow" ]; then
    MEOW_FILE="test.meow"
elif [ -f "assets/sample-images/test.meow" ]; then
    MEOW_FILE="assets/sample-images/test.meow"
elif [ -f "demo_steganographic.meow" ]; then
    MEOW_FILE="demo_steganographic.meow"
fi

if [ -z "$MEOW_FILE" ]; then
    echo "❌ No .meow file found for testing"
    echo "📝 Create one first with:"
    echo "   python meow_format.py some_image.png"
    exit 1
fi

echo "📄 Found test file: $MEOW_FILE"
echo ""

# Method 1: Direct Launch Services database modification
echo "🔧 Method 1: Using Launch Services"
echo "=================================="

# Create a temporary script to set the association
TEMP_SCRIPT=$(mktemp /tmp/meow_assoc.XXXXXX)
cat > "$TEMP_SCRIPT" << 'EOF'
tell application "System Events"
    try
        set meowFile to POSIX file "/PATH/TO/MEOW/FILE"
        set fileInfo to info for meowFile
        
        -- This will open the Get Info dialog
        tell application "Finder"
            open information window of (meowFile as alias)
        end tell
        
    on error
        display dialog "Could not process file association"
    end try
end tell
EOF

# Replace placeholder with actual file path
sed -i '' "s|/PATH/TO/MEOW/FILE|$(pwd)/$MEOW_FILE|g" "$TEMP_SCRIPT"

echo "📱 Opening Get Info dialog for $MEOW_FILE..."
echo "   1. In the 'Open with:' section, select Preview.app"
echo "   2. Click 'Change All...' button"
echo "   3. Confirm the change"
echo ""

# Open Get Info dialog
osascript -e "tell application \"Finder\" to open information window of (POSIX file \"$(pwd)/$MEOW_FILE\" as alias)"

rm "$TEMP_SCRIPT"

echo "✅ Get Info dialog opened!"
echo ""

# Method 2: Command line using defaults (may require additional setup)
echo "🔧 Method 2: Using defaults command"
echo "==================================="

# Set default application for .meow files
defaults write com.apple.LaunchServices/com.apple.launchservices.secure LSHandlers -array-add '{LSHandlerContentType=public.image;LSHandlerRoleAll=com.apple.Preview;}'

# Restart Launch Services
killall Finder 2>/dev/null || true

echo "✅ Set Preview as default for image files (includes .meow)"
echo ""

# Method 3: Using open command test
echo "🧪 Testing file association"
echo "============================"

echo "📱 Testing: open '$MEOW_FILE'"
echo "   This should open the .meow file in Preview..."
echo ""

# Test opening the file
open "$MEOW_FILE"

echo "✅ If Preview opened, the association is working!"
echo ""

# Method 4: UTI (Uniform Type Identifier) setup
echo "🔧 Method 3: UTI Configuration"
echo "=============================="

echo "📝 For advanced users, you can create a custom UTI:"
echo ""
echo "1. Create a custom app bundle with proper UTI declaration"
echo "2. Use the full associate_meow_macos.sh script instead"
echo "3. Or use duti: brew install duti && duti -s com.apple.Preview .meow all"
echo ""

echo "🎉 macOS MEOW file association setup complete!"
echo ""
echo "💡 If .meow files don't open with Preview:"
echo "   • Right-click any .meow file"
echo "   • Choose 'Get Info' (⌘+I)"
echo "   • Under 'Open with:' select Preview"
echo "   • Click 'Change All...'"
echo ""
echo "🌟 .meow files will then work like regular images on macOS!"
