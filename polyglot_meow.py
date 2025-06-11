"""
Polyglot MEOW Format - True Cross-Compatibility Implementation
Creates files that are simultaneously valid PNG and MEOW files
"""

import struct
import json
import zlib
import io
from typing import Optional, Dict
from PIL import Image
import numpy as np


class PolyglotMeowFormat:
    """
    Creates polyglot files that are valid PNG files with embedded MEOW data
    Standard viewers see PNG, MEOW-aware software sees enhanced features
    """
    
    # PNG chunk types for MEOW data (lowercase = ancillary, safe to ignore)
    MEOW_AI_CHUNK = b'mAId'      # AI metadata
    MEOW_FEAT_CHUNK = b'mFEt'    # Feature maps  
    MEOW_ATTN_CHUNK = b'mATn'    # Attention maps
    MEOW_META_CHUNK = b'mMEt'    # MEOW metadata
    
    def create_polyglot_file(self, image_path: str, output_path: str = None, 
                           ai_annotations: Dict = None) -> bool:
        """
        Create a file that's simultaneously a valid PNG and enhanced MEOW
        
        Args:
            image_path: Input image path
            output_path: Output file path (will have .png extension)
            ai_annotations: AI metadata to embed
            
        Returns:
            bool: Success status
        """
        try:
            # Load and prepare image
            img = Image.open(image_path)
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGBA')
            
            if output_path is None:
                output_path = image_path.rsplit('.', 1)[0] + '_polyglot.png'
            
            # Ensure .png extension for compatibility
            if not output_path.lower().endswith('.png'):
                output_path += '.png'
            
            # Create base PNG in memory
            png_buffer = io.BytesIO()
            img.save(png_buffer, format='PNG', optimize=True)
            png_data = png_buffer.getvalue()
            
            # Parse PNG structure to inject MEOW chunks
            enhanced_png = self._inject_meow_chunks(png_data, img, ai_annotations)
            
            # Write the polyglot file
            with open(output_path, 'wb') as f:
                f.write(enhanced_png)
            
            print(f"✅ Created polyglot PNG/MEOW file: {output_path}")
            print(f"📱 Standard viewers: Will see normal PNG image")
            print(f"🤖 MEOW viewers: Will see AI-enhanced features")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating polyglot file: {e}")
            return False
    
    def _inject_meow_chunks(self, png_data: bytes, img: Image.Image, 
                           ai_annotations: Dict = None) -> bytes:
        """Inject MEOW chunks into PNG file structure"""
        
        # Parse PNG chunks
        chunks = self._parse_png_chunks(png_data)
        
        # Generate MEOW data
        meow_chunks = []
        
        # Add AI metadata chunk
        if ai_annotations:
            ai_data = json.dumps(ai_annotations).encode('utf-8')
            compressed_ai = zlib.compress(ai_data)
            meow_chunks.append((self.MEOW_AI_CHUNK, compressed_ai))
        
        # Add feature maps
        feature_data = self._generate_feature_maps(img)
        if feature_data:
            compressed_features = zlib.compress(feature_data)
            meow_chunks.append((self.MEOW_FEAT_CHUNK, compressed_features))
        
        # Add attention maps  
        attention_data = self._generate_attention_maps(img)
        if attention_data:
            compressed_attention = zlib.compress(attention_data)
            meow_chunks.append((self.MEOW_ATTN_CHUNK, compressed_attention))
        
        # Add MEOW metadata
        meow_meta = {
            'format': 'Polyglot PNG/MEOW',
            'version': '1.0',
            'ai_enhanced': True,
            'chunk_count': len(meow_chunks)
        }
        meta_data = json.dumps(meow_meta).encode('utf-8')
        meow_chunks.append((self.MEOW_META_CHUNK, meta_data))
        
        # Rebuild PNG with MEOW chunks inserted before IEND
        return self._rebuild_png_with_meow_chunks(chunks, meow_chunks)
    
    def _parse_png_chunks(self, png_data: bytes) -> list:
        """Parse PNG file into chunks"""
        chunks = []
        offset = 8  # Skip PNG signature
        
        while offset < len(png_data):
            # Read chunk header
            length = struct.unpack('>I', png_data[offset:offset+4])[0]
            chunk_type = png_data[offset+4:offset+8]
            chunk_data = png_data[offset+8:offset+8+length]
            crc = png_data[offset+8+length:offset+12+length]
            
            chunks.append({
                'type': chunk_type,
                'data': chunk_data,
                'crc': crc
            })
            
            offset += 12 + length
            
            # Stop at IEND chunk
            if chunk_type == b'IEND':
                break
        
        return chunks
    
    def _rebuild_png_with_meow_chunks(self, original_chunks: list, 
                                    meow_chunks: list) -> bytes:
        """Rebuild PNG with MEOW chunks inserted"""
        result = b'\x89PNG\r\n\x1a\n'  # PNG signature
        
        # Add all original chunks except IEND
        for chunk in original_chunks:
            if chunk['type'] != b'IEND':
                result += self._write_png_chunk(chunk['type'], chunk['data'])
        
        # Insert MEOW chunks before IEND
        for chunk_type, chunk_data in meow_chunks:
            result += self._write_png_chunk(chunk_type, chunk_data)
        
        # Add IEND chunk
        result += self._write_png_chunk(b'IEND', b'')
        
        return result
    
    def _write_png_chunk(self, chunk_type: bytes, chunk_data: bytes) -> bytes:
        """Write a PNG chunk with proper CRC"""
        import binascii
        
        length = len(chunk_data)
        crc_data = chunk_type + chunk_data
        crc = binascii.crc32(crc_data) & 0xffffffff
        
        return (struct.pack('>I', length) + 
                chunk_type + 
                chunk_data + 
                struct.pack('>I', crc))
    
    def _generate_feature_maps(self, img: Image.Image) -> bytes:
        """Generate feature maps for AI"""
        gray = np.array(img.convert('L'))
        
        # Simple edge detection
        edges_x = np.abs(np.diff(gray.astype(np.float32), axis=1))
        edges_y = np.abs(np.diff(gray.astype(np.float32), axis=0))
        
        feature_data = {
            'edges_x': edges_x.tolist(),
            'edges_y': edges_y.tolist(),
            'mean_brightness': float(np.mean(gray)),
            'contrast': float(np.std(gray))
        }
        
        return json.dumps(feature_data).encode('utf-8')
    
    def _generate_attention_maps(self, img: Image.Image) -> bytes:
        """Generate attention/saliency maps"""
        gray = np.array(img.convert('L'))
        
        # Simple gradient-based saliency
        grad_x = np.abs(np.diff(gray.astype(np.float32), axis=1))
        grad_y = np.abs(np.diff(gray.astype(np.float32), axis=0))
        
        # Pad to original size
        grad_x = np.pad(grad_x, ((0, 0), (0, 1)), mode='edge')
        grad_y = np.pad(grad_y, ((0, 1), (0, 0)), mode='edge')
        
        saliency = np.sqrt(grad_x**2 + grad_y**2)
        
        attention_data = {
            'saliency_map': saliency.tolist(),
            'max_attention': float(np.max(saliency)),
            'attention_points': self._find_attention_points(saliency)
        }
        
        return json.dumps(attention_data).encode('utf-8')
    
    def _find_attention_points(self, saliency: np.ndarray) -> list:
        """Find key attention points"""
        threshold = np.percentile(saliency, 95)
        points = np.where(saliency > threshold)
        return list(zip(points[1].tolist(), points[0].tolist()))[:10]
    
    def load_polyglot_file(self, file_path: str, 
                          load_meow_data: bool = True) -> tuple:
        """
        Load polyglot file as both PNG and MEOW data
        
        Returns:
            tuple: (PIL Image, MEOW data dict or None)
        """
        try:
            # Load as standard PNG (always works)
            img = Image.open(file_path)
            
            if not load_meow_data:
                return img, None
            
            # Extract MEOW data from PNG chunks
            meow_data = self._extract_meow_data(file_path)
            
            return img, meow_data
            
        except Exception as e:
            print(f"Error loading polyglot file: {e}")
            return None, None
    
    def _extract_meow_data(self, file_path: str) -> Dict:
        """Extract MEOW data from PNG chunks"""
        meow_data = {}
        
        with open(file_path, 'rb') as f:
            png_data = f.read()
        
        chunks = self._parse_png_chunks(png_data)
        
        for chunk in chunks:
            chunk_type = chunk['type']
            
            if chunk_type == self.MEOW_AI_CHUNK:
                data = zlib.decompress(chunk['data'])
                meow_data['ai_metadata'] = json.loads(data.decode('utf-8'))
                
            elif chunk_type == self.MEOW_FEAT_CHUNK:
                data = zlib.decompress(chunk['data'])
                meow_data['features'] = json.loads(data.decode('utf-8'))
                
            elif chunk_type == self.MEOW_ATTN_CHUNK:
                data = zlib.decompress(chunk['data'])
                meow_data['attention'] = json.loads(data.decode('utf-8'))
                
            elif chunk_type == self.MEOW_META_CHUNK:
                meow_data['metadata'] = json.loads(chunk['data'].decode('utf-8'))
        
        return meow_data if meow_data else None


def main():
    """Demo the polyglot format"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python polyglot_meow.py <image_path> [output_path]")
        return
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create polyglot file
    polyglot = PolyglotMeowFormat()
    
    ai_annotations = {
        'object_classes': ['cat', 'dog', 'person'],
        'model_params': {
            'input_size': [224, 224],
            'mean_rgb': [0.485, 0.456, 0.406]
        }
    }
    
    success = polyglot.create_polyglot_file(input_path, output_path, ai_annotations)
    
    if success:
        # Test loading
        final_path = output_path or (input_path.rsplit('.', 1)[0] + '_polyglot.png')
        
        print(f"\n🧪 Testing compatibility:")
        print(f"📁 File: {final_path}")
        
        # Load as standard image
        img, _ = polyglot.load_polyglot_file(final_path, load_meow_data=False)
        print(f"📱 Standard PNG load: {'✅ Success' if img else '❌ Failed'}")
        
        # Load with MEOW data
        img, meow_data = polyglot.load_polyglot_file(final_path, load_meow_data=True)
        print(f"🤖 MEOW enhanced load: {'✅ Success' if meow_data else '❌ Failed'}")
        
        if meow_data:
            print(f"🎯 AI features detected:")
            for key in meow_data.keys():
                print(f"   - {key}")


if __name__ == "__main__":
    main()
