"""
MEOWIFF File Format Implementation
Core utilities for reading and writing MEOW image files
"""

import struct
import datetime
from typing import Tuple, Optional, Dict
from PIL import Image
import numpy as np


class MeowFormat:
    """Main class for handling MEOW file format operations"""
    
    MAGIC_NUMBER = b"MEOW"
    HEADER_SIZE = 12
    
    def __init__(self):
        self.metadata = {}
    
    def png_to_meow(self, png_path: str, meow_path: str = None) -> bool:
        """
        Convert PNG image to MEOW format
        
        Args:
            png_path: Path to input PNG file
            meow_path: Path for output MEOW file (optional)
        
        Returns:
            bool: Success status
        """
        try:
            # Open and convert image to RGBA
            img = Image.open(png_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            
            # Generate output path if not provided
            if meow_path is None:
                meow_path = png_path.rsplit('.', 1)[0] + '.meow'
            
            # Convert image to numpy array for easier manipulation
            pixel_data = np.array(img)
            
            # Write MEOW file
            with open(meow_path, 'wb') as f:
                # Write header
                f.write(self.MAGIC_NUMBER)
                f.write(struct.pack('<I', width))  # Little endian uint32
                f.write(struct.pack('<I', height))
                
                # Write pixel data (RGBA, 4 bytes per pixel)
                f.write(pixel_data.tobytes())
                
                # Write metadata
                self._write_metadata(f)
            
            print(f"Successfully converted {png_path} to {meow_path}")
            return True
            
        except Exception as e:
            print(f"Error converting {png_path} to MEOW: {e}")
            return False
    
    def meow_to_image(self, meow_path: str) -> Optional[Image.Image]:
        """
        Convert MEOW file to PIL Image object
        
        Args:
            meow_path: Path to MEOW file
        
        Returns:
            PIL.Image.Image or None if error
        """
        try:
            with open(meow_path, 'rb') as f:
                # Read and verify header
                magic = f.read(4)
                if magic != self.MAGIC_NUMBER:
                    raise ValueError(f"Invalid MEOW file: incorrect magic number")
                
                # Read dimensions
                width = struct.unpack('<I', f.read(4))[0]
                height = struct.unpack('<I', f.read(4))[0]
                
                # Read pixel data
                pixel_count = width * height
                pixel_data = f.read(pixel_count * 4)  # 4 bytes per pixel (RGBA)
                
                if len(pixel_data) != pixel_count * 4:
                    raise ValueError("Incomplete pixel data")
                
                # Convert to numpy array and then to PIL Image
                pixels = np.frombuffer(pixel_data, dtype=np.uint8)
                pixels = pixels.reshape((height, width, 4))
                
                img = Image.fromarray(pixels, 'RGBA')
                
                # Read metadata if present
                try:
                    self.metadata = self._read_metadata(f)
                except:
                    # Metadata is optional, continue without it
                    pass
                
                return img
                
        except Exception as e:
            print(f"Error reading MEOW file {meow_path}: {e}")
            return None
    
    def get_file_info(self, meow_path: str) -> Optional[Dict]:
        """
        Get information about a MEOW file without loading the full image
        
        Args:
            meow_path: Path to MEOW file
        
        Returns:
            Dict with file information or None if error
        """
        try:
            with open(meow_path, 'rb') as f:
                # Read and verify header
                magic = f.read(4)
                if magic != self.MAGIC_NUMBER:
                    return None
                
                width = struct.unpack('<I', f.read(4))[0]
                height = struct.unpack('<I', f.read(4))[0]
                
                # Calculate file size info
                expected_pixel_bytes = width * height * 4
                f.seek(0, 2)  # Seek to end
                total_size = f.tell()
                metadata_size = total_size - self.HEADER_SIZE - expected_pixel_bytes
                
                return {
                    'width': width,
                    'height': height,
                    'pixels': width * height,
                    'file_size': total_size,
                    'pixel_data_size': expected_pixel_bytes,
                    'metadata_size': max(0, metadata_size),
                    'format': 'MEOW'
                }
                
        except Exception as e:
            print(f"Error getting file info for {meow_path}: {e}")
            return None
    
    def _write_metadata(self, file_handle):
        """Write metadata to file"""
        # Add creation timestamp
        self.metadata['created'] = datetime.datetime.now().isoformat()
        self.metadata['software'] = 'MEOWIFF Python Implementation v1.0'
        
        for key, value in self.metadata.items():
            key_bytes = key.encode('utf-8')
            value_bytes = value.encode('utf-8')
            
            # Write key length, key, value length, value
            file_handle.write(struct.pack('<H', len(key_bytes)))
            file_handle.write(key_bytes)
            file_handle.write(struct.pack('<H', len(value_bytes)))
            file_handle.write(value_bytes)
    
    def _read_metadata(self, file_handle) -> Dict[str, str]:
        """Read metadata from file"""
        metadata = {}
        
        try:
            while True:
                # Try to read key length
                key_len_data = file_handle.read(2)
                if len(key_len_data) < 2:
                    break
                
                key_len = struct.unpack('<H', key_len_data)[0]
                key = file_handle.read(key_len).decode('utf-8')
                
                value_len = struct.unpack('<H', file_handle.read(2))[0]
                value = file_handle.read(value_len).decode('utf-8')
                
                metadata[key] = value
                
        except Exception:
            # End of metadata or corrupted metadata
            pass
        
        return metadata


def main():
    """Simple CLI for testing the format"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python meow_format.py <command> [args]")
        print("Commands:")
        print("  info <file.meow>     - Show file information")
        print("  convert <file.png>   - Convert PNG to MEOW")
        return
    
    meow = MeowFormat()
    command = sys.argv[1]
    
    if command == "info" and len(sys.argv) >= 3:
        info = meow.get_file_info(sys.argv[2])
        if info:
            print(f"MEOW File Information:")
            for key, value in info.items():
                print(f"  {key}: {value}")
        else:
            print("Failed to read file information")
    
    elif command == "convert" and len(sys.argv) >= 3:
        success = meow.png_to_meow(sys.argv[2])
        if not success:
            print("Conversion failed")
    
    else:
        print("Invalid command or arguments")


if __name__ == "__main__":
    main()
