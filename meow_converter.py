"""
MEOW File Converter - Command line utility for converting images to/from MEOW format
"""

import sys
import os
from pathlib import Path
from meow_format import MeowFormat


def print_usage():
    """Print usage information"""
    print("MEOW File Converter")
    print("===================")
    print()
    print("Usage:")
    print("  python meow_converter.py compile <input.png> [output.meow]")
    print("  python meow_converter.py extract <input.meow> [output.png]")
    print("  python meow_converter.py info <file.meow>")
    print()
    print("Commands:")
    print("  compile  - Convert PNG to MEOW format")
    print("  extract  - Convert MEOW to PNG format")
    print("  info     - Display MEOW file information")
    print()
    print("Examples:")
    print("  python meow_converter.py compile image.png")
    print("  python meow_converter.py compile image.png custom.meow")
    print("  python meow_converter.py extract image.meow")
    print("  python meow_converter.py info image.meow")


def compile_to_meow(input_path: str, output_path: str = None):
    """Convert PNG to MEOW format"""
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found")
        return False
    
    if not input_path.lower().endswith('.png'):
        print("Error: Input file must be a PNG image")
        return False
    
    meow = MeowFormat()
    
    if output_path is None:
        output_path = str(Path(input_path).with_suffix('.meow'))
    
    print(f"Converting '{input_path}' to '{output_path}'...")
    
    success = meow.png_to_meow(input_path, output_path)
    
    if success:
        # Show file size comparison
        input_size = os.path.getsize(input_path)
        output_size = os.path.getsize(output_path)
        ratio = output_size / input_size if input_size > 0 else 0
        
        print(f"Conversion successful!")
        print(f"Original PNG size: {input_size:,} bytes")
        print(f"MEOW file size: {output_size:,} bytes")
        print(f"Size ratio: {ratio:.2f}x")
        
        if ratio > 2:
            print("Note: MEOW files are larger because they're uncompressed")
            print("This format prioritizes simplicity and transparency support")
    
    return success


def extract_from_meow(input_path: str, output_path: str = None):
    """Convert MEOW to PNG format"""
    if not os.path.exists(input_path):
        print(f"Error: Input file '{input_path}' not found")
        return False
    
    if not input_path.lower().endswith('.meow'):
        print("Error: Input file must be a MEOW image")
        return False
    
    meow = MeowFormat()
    
    if output_path is None:
        output_path = str(Path(input_path).with_suffix('.png'))
    
    print(f"Converting '{input_path}' to '{output_path}'...")
    
    try:
        img = meow.meow_to_image(input_path)
        if img is None:
            print("Error: Failed to load MEOW image")
            return False
        
        img.save(output_path, 'PNG')
        print(f"Conversion successful!")
        
        # Show metadata if available
        if meow.metadata:
            print("\nMetadata:")
            for key, value in meow.metadata.items():
                print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"Error during conversion: {e}")
        return False


def show_file_info(file_path: str):
    """Display information about a MEOW file"""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found")
        return False
    
    meow = MeowFormat()
    info = meow.get_file_info(file_path)
    
    if info is None:
        print("Error: Not a valid MEOW file")
        return False
    
    print(f"MEOW File Information: {file_path}")
    print("=" * (23 + len(file_path)))
    print(f"Format: {info['format']}")
    print(f"Dimensions: {info['width']} x {info['height']} pixels")
    print(f"Total pixels: {info['pixels']:,}")
    print(f"File size: {info['file_size']:,} bytes")
    print(f"Pixel data: {info['pixel_data_size']:,} bytes")
    print(f"Metadata: {info['metadata_size']:,} bytes")
    
    # Try to load metadata
    img = meow.meow_to_image(file_path)
    if img and meow.metadata:
        print("\nMetadata:")
        for key, value in meow.metadata.items():
            print(f"  {key}: {value}")
    
    return True


def main():
    """Main entry point for the converter"""
    if len(sys.argv) < 2:
        print_usage()
        return
    
    command = sys.argv[1].lower()
    
    if command == "compile":
        if len(sys.argv) < 3:
            print("Error: Input file path required for compile command")
            print_usage()
            return
        
        input_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        compile_to_meow(input_path, output_path)
    
    elif command == "extract":
        if len(sys.argv) < 3:
            print("Error: Input file path required for extract command")
            print_usage()
            return
        
        input_path = sys.argv[2]
        output_path = sys.argv[3] if len(sys.argv) > 3 else None
        
        extract_from_meow(input_path, output_path)
    
    elif command == "info":
        if len(sys.argv) < 3:
            print("Error: File path required for info command")
            print_usage()
            return
        
        file_path = sys.argv[2]
        show_file_info(file_path)
    
    else:
        print(f"Error: Unknown command '{command}'")
        print_usage()


if __name__ == "__main__":
    main()
