"""
Steganographic MEOW Format - True Cross-Compatibility with .meow Extension
Hides MEOW data in PNG pixels, allowing .meow files that work everywhere
"""

import struct
import json
import zlib
import os
from typing import Optional, Dict, Tuple
from PIL import Image
import numpy as np


class SteganographicMeowFormat:
    """
    Creates .meow files that are actually PNGs with hidden data
    Solves the cross-compatibility problem while keeping .meow extension
    """
    
    MAGIC_HEADER = b"MEOW_STEG_V1"  # 12 bytes
    
    def create_steganographic_meow(self, image_path: str, output_path: str = None,
                                 ai_annotations: Dict = None) -> bool:
        """
        Create a .meow file that's actually a PNG with hidden MEOW data
        
        Args:
            image_path: Input image path
            output_path: Output .meow file path
            ai_annotations: AI metadata to embed
            
        Returns:
            bool: Success status
        """
        try:
            # Load and prepare image
            img = Image.open(image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            if output_path is None:
                output_path = image_path.rsplit('.', 1)[0] + '.meow'
            
            # Ensure .meow extension
            if not output_path.lower().endswith('.meow'):
                output_path = output_path.rsplit('.', 1)[0] + '.meow'
            
            # Prepare MEOW data for hiding
            meow_data = self._prepare_meow_data(img, ai_annotations)
            
            # Hide data in image using steganography
            stego_img = self._hide_data_in_image(img, meow_data)
            
            # Save as PNG but with .meow extension
            stego_img.save(output_path, format='PNG', optimize=True)
            
            print(f"✅ Created steganographic MEOW file: {output_path}")
            print(f"📱 File opens as PNG in ANY viewer despite .meow extension")
            print(f"🤖 MEOW data hidden in pixel LSBs")
            print(f"📊 Hidden data size: {len(meow_data)} bytes")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating steganographic MEOW: {e}")
            return False
    
    def _prepare_meow_data(self, img: Image.Image, ai_annotations: Dict = None) -> bytes:
        """Prepare all MEOW data for hiding"""
        
        # Generate AI features
        features = self._generate_features(img)
        attention = self._generate_attention_maps(img)
        
        # Combine all data
        meow_data = {
            'format': 'Steganographic MEOW v1.0',
            'features': features,
            'attention': attention,
            'ai_annotations': ai_annotations or {},
            'image_stats': {
                'width': img.size[0],
                'height': img.size[1],
                'mode': img.mode
            }
        }
        
        # Serialize and compress
        json_data = json.dumps(meow_data).encode('utf-8')
        compressed = zlib.compress(json_data)
        
        # Add header and length
        data_length = len(compressed)
        header = self.MAGIC_HEADER + struct.pack('<I', data_length)
        
        return header + compressed
    
    def _hide_data_in_image(self, img: Image.Image, data: bytes) -> Image.Image:
        """Hide data in image using LSB steganography"""
        
        # Convert image to numpy array
        img_array = np.array(img)
        height, width, channels = img_array.shape
        
        # Calculate capacity (2 bits per channel, skip alpha)
        capacity = height * width * 3 * 2 // 8  # 2 bits per RGB channel
        
        if len(data) > capacity:
            raise ValueError(f"Data too large: {len(data)} bytes, capacity: {capacity} bytes")
        
        # Convert data to bits
        data_bits = ''.join([format(byte, '08b') for byte in data])
        
        # Pad with zeros if needed
        total_bits_needed = len(data_bits)
        if total_bits_needed % 2 != 0:
            data_bits += '0'
            total_bits_needed += 1
        
        # Hide data in LSBs (2 bits per channel)
        flat_img = img_array.reshape(-1, channels)
        bit_index = 0
        
        for pixel_idx in range(len(flat_img)):
            if bit_index >= len(data_bits):
                break
                
            pixel = flat_img[pixel_idx]
            
            # Modify RGB channels (skip alpha)
            for channel in range(3):  # R, G, B only
                if bit_index + 1 < len(data_bits):
                    # Get 2 bits
                    bits = data_bits[bit_index:bit_index + 2]
                    bit_index += 2
                    
                    # Clear 2 LSBs and set new ones
                    pixel[channel] = (pixel[channel] & 0xFC) | int(bits, 2)
        
        # Reshape back and return
        result_array = flat_img.reshape(height, width, channels)
        return Image.fromarray(result_array, 'RGBA')
    
    def _generate_features(self, img: Image.Image) -> Dict:
        """Generate AI features"""
        gray = np.array(img.convert('L'))
        
        # Edge detection
        edges_x = np.abs(np.diff(gray.astype(np.float32), axis=1))
        edges_y = np.abs(np.diff(gray.astype(np.float32), axis=0))
        
        return {
            'edge_density': float(np.mean(edges_x) + np.mean(edges_y)),
            'brightness': float(np.mean(gray)),
            'contrast': float(np.std(gray)),
            'complexity': float(np.var(gray))
        }
    
    def _generate_attention_maps(self, img: Image.Image) -> Dict:
        """Generate attention data"""
        gray = np.array(img.convert('L'))
        
        # Simple gradient-based saliency
        grad_x = np.abs(np.diff(gray.astype(np.float32), axis=1))
        grad_y = np.abs(np.diff(gray.astype(np.float32), axis=0))
        
        # Pad to original size
        grad_x = np.pad(grad_x, ((0, 0), (0, 1)), mode='edge')
        grad_y = np.pad(grad_y, ((0, 1), (0, 0)), mode='edge')
        
        saliency = np.sqrt(grad_x**2 + grad_y**2)
        
        return {
            'max_saliency': float(np.max(saliency)),
            'mean_saliency': float(np.mean(saliency)),
            'attention_points': self._find_attention_points(saliency)
        }
    
    def _find_attention_points(self, saliency: np.ndarray) -> list:
        """Find key attention points"""
        threshold = np.percentile(saliency, 95)
        points = np.where(saliency > threshold)
        return list(zip(points[1].tolist(), points[0].tolist()))[:10]
    
    def load_steganographic_meow(self, file_path: str, 
                               extract_meow_data: bool = True) -> Tuple[Image.Image, Optional[Dict]]:
        """
        Load steganographic MEOW file
        
        Returns:
            tuple: (PIL Image, MEOW data dict or None)
        """
        try:
            # Load as standard PNG (always works)
            img = Image.open(file_path)
            
            if not extract_meow_data:
                return img, None
            
            # Extract hidden MEOW data
            meow_data = self._extract_hidden_data(img)
            
            return img, meow_data
            
        except Exception as e:
            print(f"Error loading steganographic MEOW: {e}")
            return None, None
    
    def _extract_hidden_data(self, img: Image.Image) -> Optional[Dict]:
        """Extract hidden data from image"""
        try:
            # Convert to numpy array
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            img_array = np.array(img)
            height, width, channels = img_array.shape
            
            # Extract bits from LSBs
            flat_img = img_array.reshape(-1, channels)
            extracted_bits = []
            
            # Read header first (16 bytes = 128 bits = 64 pixels)
            header_bits = []
            for pixel_idx in range(min(64, len(flat_img))):
                pixel = flat_img[pixel_idx]
                for channel in range(3):  # RGB only
                    # Extract 2 LSBs
                    bits = format(pixel[channel] & 0x03, '02b')
                    header_bits.append(bits)
                    if len(header_bits) * 2 >= 128:  # 16 bytes * 8 bits
                        break
                if len(header_bits) * 2 >= 128:
                    break
            
            # Convert header bits to bytes
            header_bit_string = ''.join(header_bits)[:128]
            header_bytes = bytes([int(header_bit_string[i:i+8], 2) 
                                for i in range(0, 128, 8)])
            
            # Check magic header
            magic = header_bytes[:12]
            if magic != self.MAGIC_HEADER:
                return None
            
            # Get data length
            data_length = struct.unpack('<I', header_bytes[12:16])[0]
            
            # Extract data bits
            total_bits_needed = (16 + data_length) * 8  # header + data
            pixels_needed = (total_bits_needed + 5) // 6  # 6 bits per pixel (2 per RGB)
            
            if pixels_needed > len(flat_img):
                return None
            
            all_bits = []
            for pixel_idx in range(pixels_needed):
                pixel = flat_img[pixel_idx]
                for channel in range(3):  # RGB only
                    bits = format(pixel[channel] & 0x03, '02b')
                    all_bits.append(bits)
            
            # Convert to bytes
            all_bit_string = ''.join(all_bits)
            data_bit_string = all_bit_string[128:128 + data_length * 8]  # Skip header
            
            data_bytes = bytes([int(data_bit_string[i:i+8], 2) 
                              for i in range(0, len(data_bit_string), 8)])
            
            # Decompress and parse JSON
            decompressed = zlib.decompress(data_bytes)
            meow_data = json.loads(decompressed.decode('utf-8'))
            
            return meow_data
            
        except Exception as e:
            print(f"Error extracting hidden data: {e}")
            return None


def create_file_association_script():
    """Create a script to associate .meow files with standard image viewers"""
    
    # Windows registry script
    reg_content = '''Windows Registry Editor Version 5.00

; Associate .meow files with default image viewer
[HKEY_CLASSES_ROOT\.meow]
@="MEOW_Image"
"Content Type"="image/png"

[HKEY_CLASSES_ROOT\MEOW_Image]
@="MEOW Enhanced Image"

[HKEY_CLASSES_ROOT\MEOW_Image\DefaultIcon]
@="imageres.dll,70"

[HKEY_CLASSES_ROOT\MEOW_Image\shell\open\command]
@="\\"C:\\\\Windows\\\\System32\\\\rundll32.exe\\" \\"C:\\\\Windows\\\\System32\\\\shimgvw.dll\\", ImageView_Fullscreen %1"

; Alternative: Use default PNG viewer
[HKEY_CLASSES_ROOT\MEOW_Image\shell\open]
@="Open with Image Viewer"

[HKEY_CLASSES_ROOT\MEOW_Image\shell\open\command]
@="cmd /c copy \\"%1\\" \\"%TEMP%\\\\temp_meow.png\\" && start \\"%TEMP%\\\\temp_meow.png\\""
'''
    
    with open('associate_meow_files.reg', 'w') as f:
        f.write(reg_content)
    
    print("✅ Created associate_meow_files.reg")
    print("📝 Run as administrator to associate .meow files with image viewers")


def main():
    """Demo the steganographic format"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python steganographic_meow.py <image_path> [output_path]")
        print("       python steganographic_meow.py --create-association")
        return
    
    if sys.argv[1] == '--create-association':
        create_file_association_script()
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create steganographic MEOW
    stego_meow = SteganographicMeowFormat()
    
    ai_annotations = {
        'object_classes': ['cat', 'dog', 'person'],
        'model_params': {
            'input_size': [224, 224],
            'mean_rgb': [0.485, 0.456, 0.406]
        },
        'training_hints': {
            'focus_regions': 'center',
            'augmentation': 'rotation,flip'
        }
    }
    
    success = stego_meow.create_steganographic_meow(input_path, output_path, ai_annotations)
    
    if success:
        # Test loading
        final_path = output_path or (input_path.rsplit('.', 1)[0] + '.meow')
        
        print(f"\n🧪 Testing compatibility:")
        print(f"📁 File: {final_path}")
        
        # Test file size
        original_size = os.path.getsize(input_path)
        meow_size = os.path.getsize(final_path)
        print(f"📊 Size: {original_size:,} → {meow_size:,} bytes ({meow_size/original_size:.2f}x)")
        
        # Load as standard image
        img, _ = stego_meow.load_steganographic_meow(final_path, extract_meow_data=False)
        print(f"📱 Standard PNG load: {'✅ Success' if img else '❌ Failed'}")
        
        # Load with MEOW data
        img, meow_data = stego_meow.load_steganographic_meow(final_path, extract_meow_data=True)
        print(f"🤖 MEOW enhanced load: {'✅ Success' if meow_data else '❌ Failed'}")
        
        if meow_data:
            print(f"🎯 AI features extracted:")
            for key in meow_data.keys():
                if key != 'ai_annotations':
                    print(f"   - {key}")
        
        print(f"\n💡 To enable .meow file association:")
        print(f"   Run: python steganographic_meow.py --create-association")
        print(f"   Then: Run associate_meow_files.reg as administrator")


if __name__ == "__main__":
    main()
