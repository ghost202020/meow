# MEOW File Association Guide

This directory contains scripts to set up file associations for `.meow` files across different operating systems, enabling them to open with standard image viewers while maintaining their AI metadata capabilities.

## Quick Setup

### Windows
```cmd
associate_meow.bat
```

### macOS  
```bash
chmod +x associate_meow_macos.sh
./associate_meow_macos.sh
```

### Linux/Unix
```bash
chmod +x associate_meow_crossplatform.sh
./associate_meow_crossplatform.sh
```

## Available Scripts

### 1. `associate_meow.bat` (Windows)
- Uses Windows `ftype` and `assoc` commands
- Associates `.meow` files with Paint or other image viewers
- Requires administrator privileges

### 2. `associate_meow_macos.sh` (macOS - Full Setup)
- Uses `duti` utility for robust file associations
- Automatically installs duti via Homebrew if available
- Creates proper Launch Services registration
- Falls back to manual Finder setup instructions

### 3. `associate_meow_simple_macos.sh` (macOS - Simple)
- Opens Get Info dialog for manual association
- Provides step-by-step instructions
- No external dependencies required
- Uses built-in macOS functionality

### 4. `associate_meow_crossplatform.sh` (Universal)
- Detects operating system automatically
- Handles macOS, Linux, and BSD systems
- Creates MIME types on Linux using `xdg-mime`
- Provides fallback instructions for unsupported systems

## How It Works

Once file associations are set up:

1. **Double-clicking** a `.meow` file opens it in your default image viewer
2. **Renaming** `.meow` to `.png` still works perfectly
3. **MEOW-aware applications** can still extract AI metadata
4. **Standard image viewers** see it as a normal PNG

## Platform-Specific Details

### macOS Methods

#### Method 1: duti (Recommended)
```bash
# Install duti
brew install duti

# Associate .meow with Preview
duti -s com.apple.Preview .meow all
```

#### Method 2: Manual Finder Setup
1. Right-click any `.meow` file
2. Select "Get Info" (⌘+I)
3. Under "Open with:" select Preview
4. Click "Change All..."

#### Method 3: Launch Services Registration
Creates a custom app bundle that redirects `.meow` files to Preview while registering the file type properly with macOS.

### Linux Methods

#### Method 1: xdg-mime (Most Distributions)
```bash
# Create MIME type
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

# Set default application
xdg-mime default eog.desktop image/x-meow
```

#### Method 2: Desktop Environment Specific
- **GNOME**: Uses Eye of GNOME (eog)
- **KDE**: Uses Gwenview
- **XFCE**: Uses Ristretto
- **Lightweight**: Uses feh or similar

## Testing the Association

After running the setup script:

1. **Create a test file:**
   ```bash
   python meow_format.py test_image.png test.meow
   ```

2. **Test opening:**
   - **Windows**: Double-click the `.meow` file
   - **macOS**: `open test.meow`
   - **Linux**: `xdg-open test.meow`

3. **Verify it opens as an image** in your default viewer

4. **Test with MEOW-aware app:**
   ```bash
   python meow_gui.py
   # Open the same .meow file to see AI metadata
   ```

## Troubleshooting

### macOS Issues
- **"duti not found"**: Install with `brew install duti`
- **Association not working**: Try the manual Finder method
- **Preview won't open**: Check file permissions

### Linux Issues  
- **"xdg-utils not found"**: Install with your package manager
- **No image viewer**: Install eog, gwenview, or feh
- **MIME not updating**: Run `update-mime-database` manually

### Windows Issues
- **"Access denied"**: Run Command Prompt as administrator
- **Association not working**: Try using Default Programs in Settings

## Advanced Configuration

### Custom Image Viewer (macOS)
```bash
# Associate with Photoshop instead of Preview
duti -s com.adobe.Photoshop .meow all

# Associate with GIMP
duti -s org.gimp.gimp-2.10 .meow all
```

### Custom Image Viewer (Linux)
```bash
# Associate with GIMP
xdg-mime default gimp.desktop image/x-meow

# Associate with Photoshop (if installed via Wine)
xdg-mime default photoshop.desktop image/x-meow
```

## Benefits of File Association

✅ **Seamless User Experience**: `.meow` files work like regular images  
✅ **No File Extension Confusion**: Users don't need to rename files  
✅ **Cross-Platform Compatibility**: Works on Windows, macOS, and Linux  
✅ **Preserved AI Metadata**: MEOW-aware apps still see the hidden data  
✅ **Backward Compatibility**: Files work even if renamed to `.png`  

This achieves the ultimate goal: **True cross-compatibility where .meow files work everywhere as images, but contain rich AI metadata for enhanced applications.**
