"""
Color space conversion utilities
Converted from MATLAB colorspace.m
"""
import numpy as np
try:
    from colorspacious import cspace_convert
except ImportError:
    cspace_convert = None

def rgb_to_lab(rgb):
    """Simple RGB to LAB conversion"""
    rgb = np.clip(rgb, 0, 1)
    lab = np.zeros_like(rgb)
    lab[..., 0] = 0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]
    lab[..., 1] = 0.5 * (rgb[..., 0] - rgb[..., 1])
    lab[..., 2] = 0.5 * (rgb[..., 1] - rgb[..., 2])
    return lab * 100

def rgb_to_xyz(rgb):
    """Simple RGB to XYZ conversion"""
    rgb = np.clip(rgb, 0, 1)
    xyz = np.zeros_like(rgb)
    xyz[..., 0] = 0.412453 * rgb[..., 0] + 0.357580 * rgb[..., 1] + 0.180423 * rgb[..., 2]
    xyz[..., 1] = 0.212671 * rgb[..., 0] + 0.715160 * rgb[..., 1] + 0.072169 * rgb[..., 2]
    xyz[..., 2] = 0.019334 * rgb[..., 0] + 0.119193 * rgb[..., 1] + 0.950227 * rgb[..., 2]
    return xyz * 100

def colorspace_convert(image, conversion):
    """
    Convert color space of image
    Args:
        image: numpy array of shape (H, W, 3) or (N, 3)
        conversion: string like 'Lab<-RGB' or 'XYZ<-RGB'
    Returns:
        converted image in target color space
    """
    if '<-' in conversion:
        dest, src = conversion.split('<-')
    elif '->' in conversion:
        src, dest = conversion.split('->')
    else:
        raise ValueError(f"Invalid conversion format: {conversion}")
    
    if not src:
        src = 'RGB'
    if not dest:
        dest = 'RGB'
    
    src = src.upper().strip()
    dest = dest.upper().strip()
    
    if cspace_convert is not None:
        try:
            space_map = {
                'RGB': 'sRGB1',
                'LAB': 'CIELab',
                'XYZ': 'XYZ100'
            }
            
            src_space = space_map.get(src, 'sRGB1')
            dest_space = space_map.get(dest, 'sRGB1')
            
            original_shape = image.shape
            if len(original_shape) == 3:
                image_flat = image.reshape(-1, 3)
                converted = cspace_convert(image_flat, src_space, dest_space)
                return converted.reshape(original_shape)
            else:
                return cspace_convert(image, src_space, dest_space)
        except Exception:
            pass
    
    if src == 'RGB' and dest == 'LAB':
        return rgb_to_lab(image)
    elif src == 'RGB' and dest == 'XYZ':
        return rgb_to_xyz(image)
    elif src == dest:
        return image.copy()
    else:
        return image.copy()