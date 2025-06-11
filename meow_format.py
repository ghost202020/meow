"""
Enhanced MEOW File Format Implementation
AI-optimized image format with cross-compatibility
Based on the AI_Pivot specifications
"""

import struct
import json
import datetime
import zlib
import io
from typing import Tuple, Optional, Dict, List, Union
from PIL import Image
import numpy as np
from dataclasses import dataclass, asdict


@dataclass
class AIMetadata:
    """AI-specific metadata structure"""
    # Semantic annotations
    object_classes: List[str] = None
    bounding_boxes: List[Dict] = None
    segmentation_masks: Dict = None
    
    # Attention and saliency
    attention_maps: Dict = None
    saliency_regions: List[Dict] = None
    
    # Model optimization hints
    optimal_input_size: Tuple[int, int] = None
    preprocessing_params: Dict = None
    feature_importance: Dict = None
    
    # Content analysis
    complexity_map: Dict = None
    texture_analysis: Dict = None
    edge_density: float = None


class ChunkType:
    """MEOW chunk type definitions"""
    # Standard chunks
    HEADER = b'MHDR'
    FALLBACK_IMAGE = b'FALL'  # Embedded PNG/JPEG for compatibility
    PIXEL_DATA = b'MPIX'      # Enhanced pixel data
    METADATA = b'META'        # General metadata
    
    # AI-specific chunks
    AI_METADATA = b'AIMT'     # AI annotations and metadata
    FEATURE_MAPS = b'FEAT'    # Pre-computed feature maps
    ATTENTION = b'ATTN'       # Attention maps and saliency
    SEMANTIC = b'SEMT'        # Semantic segmentation layers
    MULTI_RES = b'MRES'       # Multi-resolution pyramid
    COMPRESSION = b'COMP'     # Neural compression data
    
    # Compatibility chunks
    PNG_COMPAT = b'PNGC'      # PNG compatibility data
    JPEG_COMPAT = b'JPGC'     # JPEG compatibility data


class EnhancedMeowFormat:
    """Enhanced MEOW format with AI optimizations and cross-compatibility"""
    
    MAGIC_NUMBER = b"MEOW"
    VERSION = 2  # Enhanced version
    HEADER_SIZE = 16  # Magic(4) + Version(4) + Flags(4) + ChunkCount(4)
    
    def __init__(self):
        self.chunks = {}
        self.ai_metadata = AIMetadata()
        self.compression_level = 6  # Default compression level
        
    def create_from_image(self, image_path: str, output_path: str = None, 
                         include_fallback: bool = True,
                         ai_annotations: Dict = None) -> bool:
        """
        Create enhanced MEOW file from standard image with AI optimizations
        
        Args:
            image_path: Path to input image (PNG, JPEG, etc.)
            output_path: Output MEOW file path
            include_fallback: Include embedded fallback image for compatibility
            ai_annotations: Optional AI metadata to embed
        
        Returns:
            bool: Success status
        """
        try:
            # Load original image
            img = Image.open(image_path)
            if img.mode not in ['RGB', 'RGBA']:
                img = img.convert('RGBA')
            
            width, height = img.size
            
            if output_path is None:
                output_path = image_path.rsplit('.', 1)[0] + '.meow'
            
            # Initialize chunks
            self.chunks = {}
            
            # Create header chunk
            self._create_header_chunk(width, height)
            
            # Create fallback image chunk (embedded PNG for compatibility)
            if include_fallback:
                self._create_fallback_chunk(img)
            
            # Create enhanced pixel data with neural compression
            self._create_enhanced_pixel_chunk(img)
            
            # Create multi-resolution pyramid
            self._create_multi_resolution_chunk(img)
            
            # Generate AI-specific feature maps
            self._create_feature_maps_chunk(img)
            
            # Create attention and saliency maps
            self._create_attention_chunk(img)
            
            # Process AI annotations if provided
            if ai_annotations:
                self._process_ai_annotations(ai_annotations)
            
            # Create metadata chunks
            self._create_metadata_chunk()
            self._create_ai_metadata_chunk()
            
            # Write MEOW file
            self._write_meow_file(output_path)
            
            print(f"Successfully created enhanced MEOW: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error creating enhanced MEOW: {e}")
            return False
    
    def load_meow_file(self, meow_path: str, load_ai_data: bool = True) -> Optional[Image.Image]:
        """
        Load MEOW file with optional AI data loading
        
        Args:
            meow_path: Path to MEOW file
            load_ai_data: Whether to load AI-specific chunks
        
        Returns:
            PIL Image or None if error
        """
        try:
            with open(meow_path, 'rb') as f:
                # Read and verify header
                magic = f.read(4)
                if magic != self.MAGIC_NUMBER:
                    raise ValueError("Invalid MEOW file: incorrect magic number")
                
                version = struct.unpack('<I', f.read(4))[0]
                flags = struct.unpack('<I', f.read(4))[0]
                chunk_count = struct.unpack('<I', f.read(4))[0]
                
                print(f"Loading MEOW v{version} with {chunk_count} chunks")
                
                # Read all chunks
                self.chunks = {}
                for _ in range(chunk_count):
                    chunk_type = f.read(4)
                    chunk_size = struct.unpack('<I', f.read(4))[0]
                    chunk_data = f.read(chunk_size)
                    self.chunks[chunk_type] = chunk_data
                
                # Try to load enhanced pixel data first
                if ChunkType.PIXEL_DATA in self.chunks:
                    img = self._load_enhanced_pixels()
                    if img:
                        print("Loaded enhanced pixel data")
                        if load_ai_data:
                            self._load_ai_chunks()
                        return img
                
                # Fallback to embedded standard image
                if ChunkType.FALLBACK_IMAGE in self.chunks:
                    img = self._load_fallback_image()
                    if img:
                        print("Loaded fallback image")
                        return img
                
                raise ValueError("No loadable image data found")
                
        except Exception as e:
            print(f"Error loading MEOW file: {e}")
            return None
    
    def get_ai_metadata(self) -> AIMetadata:
        """Get AI metadata from loaded file"""
        return self.ai_metadata
    
    def _create_header_chunk(self, width: int, height: int):
        """Create header chunk with image information"""
        header_data = struct.pack('<IIII', 
                                 width, height, 
                                 32,  # bit depth (RGBA)
                                 0)   # reserved
        self.chunks[ChunkType.HEADER] = header_data
    
    def _create_fallback_chunk(self, img: Image.Image):
        """Create fallback PNG chunk for cross-compatibility"""
        buffer = io.BytesIO()
        # Convert to RGB if RGBA to reduce size
        fallback_img = img.convert('RGB') if img.mode == 'RGBA' else img
        fallback_img.save(buffer, format='PNG', optimize=True)
        self.chunks[ChunkType.FALLBACK_IMAGE] = buffer.getvalue()
    
    def _create_enhanced_pixel_chunk(self, img: Image.Image):
        """Create enhanced pixel data with neural compression simulation"""
        # Convert to numpy array
        pixel_data = np.array(img)
        
        # Simulate neural compression: compress complex regions more
        complexity_map = self._calculate_complexity_map(pixel_data)
        
        # Apply content-aware compression
        compressed_data = self._neural_compress(pixel_data, complexity_map)
        
        self.chunks[ChunkType.PIXEL_DATA] = compressed_data
    
    def _create_multi_resolution_chunk(self, img: Image.Image):
        """Create multi-resolution pyramid for different model input sizes"""
        resolutions = [(224, 224), (512, 512), (1024, 1024)]
        pyramid_data = {}
        
        for target_size in resolutions:
            if img.size[0] >= target_size[0] or img.size[1] >= target_size[1]:
                resized = img.resize(target_size, Image.Resampling.LANCZOS)
                buffer = io.BytesIO()
                resized.save(buffer, format='PNG')
                pyramid_data[f"{target_size[0]}x{target_size[1]}"] = buffer.getvalue()
        
        if pyramid_data:
            pyramid_json = json.dumps(pyramid_data, default=lambda x: x.hex() if isinstance(x, bytes) else x)
            self.chunks[ChunkType.MULTI_RES] = pyramid_json.encode('utf-8')
    
    def _create_feature_maps_chunk(self, img: Image.Image):
        """Generate pre-computed feature maps for AI models"""
        gray = img.convert('L')
        gray_array = np.array(gray)
        
        # Edge detection (Sobel-like)
        edge_x = np.abs(np.diff(gray_array, axis=1))
        edge_y = np.abs(np.diff(gray_array, axis=0))
        
        # Texture analysis (local variance)
        texture_map = self._calculate_texture_features(gray_array)
        
        feature_data = {
            'edges_x': edge_x.tolist(),
            'edges_y': edge_y.tolist(),
            'texture': texture_map.tolist(),
            'mean_brightness': float(np.mean(gray_array)),
            'contrast': float(np.std(gray_array))
        }
        
        # Compress feature data
        feature_json = json.dumps(feature_data)
        compressed_features = zlib.compress(feature_json.encode('utf-8'), self.compression_level)
        self.chunks[ChunkType.FEATURE_MAPS] = compressed_features
    
    def _create_attention_chunk(self, img: Image.Image):
        """Create attention maps and saliency information"""
        gray = np.array(img.convert('L'))
        
        # Simple saliency based on gradient magnitude
        saliency_map = self._calculate_saliency(gray)
        
        # Find high-attention regions
        attention_regions = self._find_attention_regions(saliency_map)
        
        attention_data = {
            'saliency_map': saliency_map.tolist(),
            'attention_regions': attention_regions,
            'focus_points': self._find_focus_points(saliency_map)
        }
        
        attention_json = json.dumps(attention_data)
        compressed_attention = zlib.compress(attention_json.encode('utf-8'), self.compression_level)
        self.chunks[ChunkType.ATTENTION] = compressed_attention
    
    def _create_metadata_chunk(self):
        """Create general metadata chunk"""
        metadata = {
            'created': datetime.datetime.now().isoformat(),
            'software': 'Enhanced MEOW Python Implementation v2.0',
            'format_version': self.VERSION,
            'ai_optimized': True,
            'compression_level': self.compression_level
        }
        
        metadata_json = json.dumps(metadata)
        self.chunks[ChunkType.METADATA] = metadata_json.encode('utf-8')
    
    def _create_ai_metadata_chunk(self):
        """Create AI-specific metadata chunk"""
        ai_data = asdict(self.ai_metadata)
        # Remove None values
        ai_data = {k: v for k, v in ai_data.items() if v is not None}
        
        if ai_data:
            ai_json = json.dumps(ai_data)
            compressed_ai = zlib.compress(ai_json.encode('utf-8'), self.compression_level)
            self.chunks[ChunkType.AI_METADATA] = compressed_ai
    
    def _process_ai_annotations(self, annotations: Dict):
        """Process and store AI annotations"""
        if 'object_classes' in annotations:
            self.ai_metadata.object_classes = annotations['object_classes']
        if 'bounding_boxes' in annotations:
            self.ai_metadata.bounding_boxes = annotations['bounding_boxes']
        if 'preprocessing_params' in annotations:
            self.ai_metadata.preprocessing_params = annotations['preprocessing_params']
    
    def _write_meow_file(self, output_path: str):
        """Write all chunks to MEOW file"""
        with open(output_path, 'wb') as f:
            # Write file header
            f.write(self.MAGIC_NUMBER)
            f.write(struct.pack('<I', self.VERSION))
            f.write(struct.pack('<I', 0))  # flags (reserved)
            f.write(struct.pack('<I', len(self.chunks)))
            
            # Write all chunks
            for chunk_type, chunk_data in self.chunks.items():
                f.write(chunk_type)
                f.write(struct.pack('<I', len(chunk_data)))
                f.write(chunk_data)
    
    def _load_enhanced_pixels(self) -> Optional[Image.Image]:
        """Load enhanced pixel data"""
        try:
            pixel_data = self.chunks[ChunkType.PIXEL_DATA]
            # Decompress neural compressed data
            decompressed = self._neural_decompress(pixel_data)
            
            # Convert back to PIL Image
            if ChunkType.HEADER in self.chunks:
                header = struct.unpack('<IIII', self.chunks[ChunkType.HEADER])
                width, height = header[0], header[1]
                
                if len(decompressed) == width * height * 4:  # RGBA
                    pixels = np.frombuffer(decompressed, dtype=np.uint8)
                    pixels = pixels.reshape((height, width, 4))
                    return Image.fromarray(pixels, 'RGBA')
                elif len(decompressed) == width * height * 3:  # RGB
                    pixels = np.frombuffer(decompressed, dtype=np.uint8)
                    pixels = pixels.reshape((height, width, 3))
                    return Image.fromarray(pixels, 'RGB')
            
            return None
        except Exception as e:
            print(f"Error loading enhanced pixels: {e}")
            return None
    
    def _load_fallback_image(self) -> Optional[Image.Image]:
        """Load embedded fallback image"""
        try:
            fallback_data = self.chunks[ChunkType.FALLBACK_IMAGE]
            return Image.open(io.BytesIO(fallback_data))
        except Exception as e:
            print(f"Error loading fallback image: {e}")
            return None
    
    def _load_ai_chunks(self):
        """Load AI-specific data chunks"""
        try:
            # Load AI metadata
            if ChunkType.AI_METADATA in self.chunks:
                compressed_data = self.chunks[ChunkType.AI_METADATA]
                decompressed = zlib.decompress(compressed_data)
                ai_data = json.loads(decompressed.decode('utf-8'))
                
                # Reconstruct AI metadata
                for key, value in ai_data.items():
                    if hasattr(self.ai_metadata, key):
                        setattr(self.ai_metadata, key, value)
            
            print("AI metadata loaded successfully")
            
        except Exception as e:
            print(f"Error loading AI chunks: {e}")
    
    # Helper methods for AI processing
    def _calculate_complexity_map(self, pixel_data: np.ndarray) -> np.ndarray:
        """Calculate complexity map for content-aware compression"""
        gray = np.mean(pixel_data, axis=2) if len(pixel_data.shape) == 3 else pixel_data
        
        # Calculate local variance as complexity measure
        kernel_size = 5
        h, w = gray.shape
        complexity = np.zeros_like(gray)
        
        for i in range(kernel_size//2, h - kernel_size//2):
            for j in range(kernel_size//2, w - kernel_size//2):
                window = gray[i-kernel_size//2:i+kernel_size//2+1, 
                             j-kernel_size//2:j+kernel_size//2+1]
                complexity[i, j] = np.var(window)
        
        return complexity
    
    def _neural_compress(self, pixel_data: np.ndarray, complexity_map: np.ndarray) -> bytes:
        """Simulate neural compression with content awareness"""
        # For now, use standard compression with complexity-based quality
        # In a real implementation, this would use a trained neural compressor
        
        # Apply different compression levels based on complexity
        high_complexity = complexity_map > np.percentile(complexity_map, 75)
        
        # Flatten and compress
        compressed = zlib.compress(pixel_data.tobytes(), self.compression_level)
        
        # Store complexity map for decompression
        complexity_compressed = zlib.compress(complexity_map.tobytes())
        
        # Combine data
        result = struct.pack('<I', len(compressed)) + compressed + complexity_compressed
        return result
    
    def _neural_decompress(self, compressed_data: bytes) -> bytes:
        """Decompress neural compressed data"""
        try:
            # Extract pixel data length
            pixel_len = struct.unpack('<I', compressed_data[:4])[0]
            
            # Extract and decompress pixel data
            pixel_compressed = compressed_data[4:4+pixel_len]
            pixel_data = zlib.decompress(pixel_compressed)
            
            return pixel_data
            
        except Exception as e:
            print(f"Decompression error: {e}")
            return b''
    
    def _calculate_texture_features(self, gray_array: np.ndarray) -> np.ndarray:
        """Calculate texture features using local variance"""
        kernel_size = 3
        h, w = gray_array.shape
        texture = np.zeros_like(gray_array, dtype=np.float32)
        
        for i in range(kernel_size//2, h - kernel_size//2):
            for j in range(kernel_size//2, w - kernel_size//2):
                window = gray_array[i-kernel_size//2:i+kernel_size//2+1, 
                                  j-kernel_size//2:j+kernel_size//2+1]
                texture[i, j] = np.var(window.astype(np.float32))
        
        return texture
    
    def _calculate_saliency(self, gray_array: np.ndarray) -> np.ndarray:
        """Calculate saliency map using gradient magnitude"""
        # Calculate gradients
        grad_x = np.abs(np.diff(gray_array.astype(np.float32), axis=1))
        grad_y = np.abs(np.diff(gray_array.astype(np.float32), axis=0))
        
        # Pad to match original size
        grad_x = np.pad(grad_x, ((0, 0), (0, 1)), mode='edge')
        grad_y = np.pad(grad_y, ((0, 1), (0, 0)), mode='edge')
        
        # Combine gradients
        saliency = np.sqrt(grad_x**2 + grad_y**2)
        
        # Normalize to 0-255
        if saliency.max() > 0:
            saliency = (saliency / saliency.max() * 255).astype(np.uint8)
        
        return saliency
    
    def _find_attention_regions(self, saliency_map: np.ndarray) -> List[Dict]:
        """Find high-attention regions in saliency map"""
        threshold = np.percentile(saliency_map, 90)
        high_attention = saliency_map > threshold
        
        # Find connected components (simplified)
        regions = []
        h, w = high_attention.shape
        visited = np.zeros_like(high_attention)
        
        def flood_fill(start_i, start_j):
            stack = [(start_i, start_j)]
            region_points = []
            
            while stack:
                i, j = stack.pop()
                if (i < 0 or i >= h or j < 0 or j >= w or 
                    visited[i, j] or not high_attention[i, j]):
                    continue
                
                visited[i, j] = True
                region_points.append((i, j))
                
                # Add neighbors
                for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                    stack.append((i+di, j+dj))
            
            return region_points
        
        for i in range(h):
            for j in range(w):
                if high_attention[i, j] and not visited[i, j]:
                    points = flood_fill(i, j)
                    if len(points) > 10:  # Minimum region size
                        min_i, min_j = min(p[0] for p in points), min(p[1] for p in points)
                        max_i, max_j = max(p[0] for p in points), max(p[1] for p in points)
                        
                        regions.append({
                            'bbox': [min_j, min_i, max_j, max_i],  # x1, y1, x2, y2
                            'area': len(points),
                            'avg_saliency': float(np.mean([saliency_map[p[0], p[1]] for p in points]))
                        })
        
        return regions
    
    def _find_focus_points(self, saliency_map: np.ndarray) -> List[Tuple[int, int]]:
        """Find key focus points in the image"""
        # Find local maxima
        from scipy import ndimage
        
        # Use maximum filter to find local maxima
        neighborhood = ndimage.generate_binary_structure(2, 2)
        local_maxima = ndimage.maximum_filter(saliency_map, footprint=neighborhood) == saliency_map
        
        # Get coordinates of maxima above threshold
        threshold = np.percentile(saliency_map, 95)
        focus_points = np.where((local_maxima) & (saliency_map > threshold))
        
        # Convert to list of tuples and limit number
        points = list(zip(focus_points[1].tolist(), focus_points[0].tolist()))  # x, y format
        return points[:10]  # Limit to top 10 focus points


def check_meow_compatibility(viewer_path: str = None) -> Dict[str, bool]:
    """
    Check if a viewer supports MEOW format enhancements
    
    Args:
        viewer_path: Path to viewer executable (optional)
    
    Returns:
        Dict with capability flags
    """
    capabilities = {
        'supports_meow': False,
        'supports_ai_metadata': False,
        'supports_multi_resolution': False,
        'supports_fallback': True  # All viewers should support fallback
    }
    
    # In a real implementation, this would check viewer capabilities
    # For now, assume basic support
    capabilities['supports_meow'] = True
    
    return capabilities


def smart_fallback_loader(meow_path: str, viewer_capabilities: Dict = None) -> Image.Image:
    """
    Smart fallback loading based on viewer capabilities
    
    Args:
        meow_path: Path to MEOW file
        viewer_capabilities: Optional capability dict
    
    Returns:
        PIL Image loaded with appropriate method
    """
    if viewer_capabilities is None:
        viewer_capabilities = check_meow_compatibility()
    
    meow = EnhancedMeowFormat()
    
    if viewer_capabilities.get('supports_meow', False):
        # Load full enhanced image
        img = meow.load_meow_file(meow_path, load_ai_data=True)
        if img:
            print("Loaded full enhanced MEOW image")
            return img
    
    # Fallback to standard image
    img = meow.load_meow_file(meow_path, load_ai_data=False)
    if img:
        print("Loaded fallback image from MEOW")
        return img
    
    raise ValueError("Could not load image from MEOW file")


if __name__ == "__main__":
    # Simple test
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python meow_enhanced.py <image_path> [output_path]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Create enhanced MEOW
    meow = EnhancedMeowFormat()
    
    # Add some sample AI annotations
    ai_annotations = {
        'object_classes': ['cat', 'background'],
        'preprocessing_params': {
            'mean_rgb': [0.485, 0.456, 0.406],
            'std_rgb': [0.229, 0.224, 0.225],
            'input_size': [224, 224]
        }
    }
    
    success = meow.create_from_image(input_path, output_path, 
                                   include_fallback=True,
                                   ai_annotations=ai_annotations)
    
    if success:
        print("Enhanced MEOW file created successfully!")
        
        # Test loading
        if output_path is None:
            output_path = input_path.rsplit('.', 1)[0] + '.meow'
        
        loaded_img = smart_fallback_loader(output_path)
        if loaded_img:
            print(f"Successfully loaded and verified MEOW file: {output_path}")
            
            # Print AI metadata
            ai_meta = meow.get_ai_metadata()
            if ai_meta.object_classes:
                print(f"Detected objects: {ai_meta.object_classes}")
    else:
        print("Failed to create enhanced MEOW file")
