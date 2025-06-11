#!/bin/bash
# MEOW File Association Setup for macOS
# Sets up .meow files to open with Preview (or other image viewers)

set -e

echo "🐾 Setting up MEOW file associations for macOS..."

# Method 1: Using duti (recommended - install with: brew install duti)
if command -v duti &> /dev/null; then
    echo "📱 Using duti to set file associations..."
    
    # Associate .meow with Preview
    duti -s com.apple.Preview .meow all
    echo "   ✅ Associated .meow files with Preview"
    
    # Optional: Also associate with other image viewers
    # duti -s com.adobe.Photoshop .meow all
    # duti -s org.gimp.gimp-2.10 .meow all
    
    echo "🎉 MEOW files will now open with Preview by default!"
    
elif command -v /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister &> /dev/null; then
    echo "📱 Using lsregister (system method)..."
    
    # Create a simple app bundle that redirects .meow to Preview
    APP_NAME="MEOWViewer.app"
    APP_PATH="/Applications/$APP_NAME"
    
    if [ ! -d "$APP_PATH" ]; then
        echo "   📦 Creating MEOW viewer app bundle..."
        
        # Create app structure
        mkdir -p "$APP_PATH/Contents/MacOS"
        mkdir -p "$APP_PATH/Contents/Resources"
        
        # Create Info.plist
        cat > "$APP_PATH/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>MEOWViewer</string>
    <key>CFBundleIdentifier</key>
    <string>com.meowformat.viewer</string>
    <key>CFBundleName</key>
    <string>MEOW Viewer</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>meow</string>
            </array>
            <key>CFBundleTypeName</key>
            <string>MEOW Image File</string>
            <key>CFBundleTypeRole</key>
            <string>Viewer</string>
            <key>LSHandlerRank</key>
            <string>Owner</string>
        </dict>
    </array>
</dict>
</plist>
EOF
        
        # Create executable script that opens with Preview
        cat > "$APP_PATH/Contents/MacOS/MEOWViewer" << 'EOF'
#!/bin/bash
# MEOW Viewer - Opens .meow files with Preview
if [ "$#" -gt 0 ]; then
    /usr/bin/open -a Preview "$@"
else
    echo "MEOW Viewer: Opens .meow files with Preview"
fi
EOF
        
        chmod +x "$APP_PATH/Contents/MacOS/MEOWViewer"
        
        echo "   ✅ Created MEOW Viewer app bundle"
    fi
    
    # Register the app
    /System/Library/Frameworks/CoreServices.framework/Versions/A/Frameworks/LaunchServices.framework/Versions/A/Support/lsregister -f "$APP_PATH"
    
    echo "   ✅ Registered MEOW Viewer with Launch Services"
    echo "🎉 MEOW files will now open with Preview via MEOW Viewer!"
    
else
    echo "❌ Could not find duti or lsregister"
    echo "📥 Install duti with: brew install duti"
    echo "   Or manually associate .meow files in Finder:"
    echo "   1. Right-click a .meow file"
    echo "   2. Choose 'Get Info'"
    echo "   3. In 'Open with:' select Preview"
    echo "   4. Click 'Change All...'"
    exit 1
fi

# Test the association
echo ""
echo "🧪 Testing file association..."
if [ -f "test.meow" ] || [ -f "assets/sample-images/test.meow" ]; then
    TEST_FILE="test.meow"
    if [ ! -f "$TEST_FILE" ]; then
        TEST_FILE="assets/sample-images/test.meow"
    fi
    
    echo "   📄 Test file: $TEST_FILE"
    
    # Check what app is associated
    if command -v duti &> /dev/null; then
        ASSOCIATED_APP=$(duti -x .meow 2>/dev/null || echo "Unknown")
        echo "   📱 Associated app: $ASSOCIATED_APP"
    fi
    
    echo "   💡 Try: open '$TEST_FILE'"
    
else
    echo "   ⚠️  No test .meow file found"
    echo "   💡 Create one with: python meow_format.py some_image.png"
fi

echo ""
echo "✅ macOS MEOW file association setup complete!"
echo ""
echo "📱 .meow files now open as images in Preview"
echo "🤖 MEOW-aware apps can still extract AI metadata"
echo "🌟 True cross-compatibility achieved on macOS!"
