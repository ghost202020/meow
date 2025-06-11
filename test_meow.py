"""
Test script for MEOW file format
Creates a simple test image and demonstrates conversion
"""

import os
from PIL import Image, ImageDraw
import numpy as np
from meow_format import MeowFormat


def create_test_image(filename="test_image.png", size=(200, 150)):
    """Create a simple test image with various colors and transparency"""
    
    # Create RGBA image
    img = Image.new('RGBA', size, (255, 255, 255, 0))  # Transparent background
    draw = ImageDraw.Draw(img)
    
    # Draw some shapes with different colors and transparency
    # Red rectangle
    draw.rectangle([10, 10, 80, 60], fill=(255, 0, 0, 255))
    
    # Green circle (semi-transparent)
    draw.ellipse([100, 20, 180, 100], fill=(0, 255, 0, 128))
    
    # Blue triangle
    draw.polygon([(50, 80), (100, 130), (150, 80)], fill=(0, 0, 255, 255))
    
    # Some text
    try:
        from PIL import ImageFont
        # Try to use a default font, fall back to basic if not available
        font = ImageFont.load_default()
        draw.text((10, 120), "MEOW!", fill=(128, 0, 128, 255), font=font)
    except:
        draw.text((10, 120), "MEOW!", fill=(128, 0, 128, 255))
    
    # Save the test image
    img.save(filename, 'PNG')
    print(f"Created test image: {filename}")
    return filename


def run_tests():
    """Run a series of tests on the MEOW format"""
    
    print("MEOW File Format Test Suite")
    print("=" * 40)
    
    # Create test image
    test_png = create_test_image()
    
    # Initialize MEOW format handler
    meow = MeowFormat()
    
    # Test 1: Convert PNG to MEOW
    print("\nTest 1: Converting PNG to MEOW...")
    test_meow = "test_image.meow"
    success = meow.png_to_meow(test_png, test_meow)
    
    if success:
        print("✓ PNG to MEOW conversion successful")
        
        # Compare file sizes
        png_size = os.path.getsize(test_png)
        meow_size = os.path.getsize(test_meow)
        ratio = meow_size / png_size
        
        print(f"  PNG size: {png_size:,} bytes")
        print(f"  MEOW size: {meow_size:,} bytes")
        print(f"  Size ratio: {ratio:.2f}x")
    else:
        print("✗ PNG to MEOW conversion failed")
        return
    
    # Test 2: Get file info
    print("\nTest 2: Reading MEOW file information...")
    info = meow.get_file_info(test_meow)
    
    if info:
        print("✓ File info retrieved successfully")
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print("✗ Failed to get file info")
    
    # Test 3: Convert MEOW back to image
    print("\nTest 3: Converting MEOW back to image...")
    img = meow.meow_to_image(test_meow)
    
    if img:
        print("✓ MEOW to image conversion successful")
        output_png = "test_output.png"
        img.save(output_png, 'PNG')
        print(f"  Saved as: {output_png}")
        
        # Verify dimensions match
        original_img = Image.open(test_png)
        if img.size == original_img.size:
            print("✓ Dimensions match original")
        else:
            print("✗ Dimension mismatch")
            
    else:
        print("✗ MEOW to image conversion failed")
    
    # Test 4: Check metadata
    print("\nTest 4: Checking metadata...")
    if meow.metadata:
        print("✓ Metadata found:")
        for key, value in meow.metadata.items():
            print(f"  {key}: {value}")
    else:
        print("! No metadata found (this is okay)")
    
    print("\nTest Summary:")
    print("=" * 40)
    print("All core functionality tests completed!")
    print("\nGenerated files:")
    print(f"- {test_png} (original test image)")
    print(f"- {test_meow} (MEOW format)")
    print(f"- test_output.png (converted back from MEOW)")
    
    print("\nTo test the GUI applications:")
    print("1. Run: python meow_gui.py")
    print("2. Run: python meow_viewer.py test_image.meow")
    print("3. Run: python meow_converter.py info test_image.meow")


if __name__ == "__main__":
    # Change to the script directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_tests()
