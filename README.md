# MEOW
**M**arvelously **e**fficient **o**ptimized **w**onderful Image File Format.

Also known as MEOWIFF or MEOW.

A Python implementation inspired by the BRUHIFF format, but with actual practical features!

## Features
- Cross-platform compatibility (Windows, Linux, macOS)
- Efficient binary storage (much smaller than BRUH format)
- RGBA support with transparency
- Metadata support
- Fast rendering with PIL/Pillow
- GUI viewer with tkinter
- Both CLI and GUI modes

## How to Use

### Setup
1. Navigate to the Meow-Format directory
2. Install dependencies: `pip install -r requirements.txt`

### Convert Images to MEOW Format
```bash
python meow_converter.py compile path/to/image.png
```

### View MEOW Images
```bash
python meow_viewer.py path/to/image.meow
```

### GUI Mode
```bash
python meow_gui.py
```

## File Format Specification

### Header (12 bytes)
- Bytes 0-3: Magic number "MEOW" (4 bytes ASCII)
- Bytes 4-7: Width (uint32, little endian)
- Bytes 8-11: Height (uint32, little endian)

### Pixel Data
- Each pixel: 4 bytes (RGBA)
- Row-major order (left to right, top to bottom)
- Uncompressed for simplicity (could add compression later)

### Metadata (Optional)
- Length-prefixed strings for metadata
- Currently supports: creation date, software name

## Advantages over BRUH Format
- 33% smaller file size (4 bytes/pixel vs 6 bytes/pixel)
- Binary storage instead of text
- RGBA support with transparency
- Cross-platform compatibility
- Better error handling
- Metadata support
- Faster I/O operations
