"""
Superpixel utilities
"""
import numpy as np
from skimage.segmentation import slic
import struct

def generate_superpixels(image, n_segments=200, compactness=20):
    """
    Generate superpixels using SLIC algorithm
    Args:
        image: input image (H, W, 3)
        n_segments: number of superpixels
        compactness: compactness parameter
    Returns:
        superpixel labels (H, W)
    """
    # Convert to 0-1 range if needed
    if image.max() > 1:
        image = image / 255.0
    
    # Generate superpixels (labels start from 0)
    labels = slic(image, n_segments=n_segments, compactness=compactness, 
                  start_label=1, enforce_connectivity=True)
    
    return labels

def read_dat_file(image_size, data_path):
    """
    Read superpixel labels from .dat file
    Args:
        image_size: (height, width)
        data_path: path to .dat file
    Returns:
        label matrix (height, width)
    """
    height, width = image_size
    
    with open(data_path, 'rb') as f:
        # Read uint32 values
        data = f.read(height * width * 4)  # 4 bytes per uint32
        labels = struct.unpack(f'{height * width}I', data)
    
    # Convert to numpy array and add 1 (MATLAB indexing)
    labels = np.array(labels) + 1
    
    # Reshape to image dimensions
    labels = labels.reshape(width, height).T
    
    return labels

def save_dat_file(labels, data_path):
    """
    Save superpixel labels to .dat file
    Args:
        labels: label matrix (height, width)
        data_path: output path
    """
    # Convert to 0-based indexing and flatten
    labels_flat = (labels - 1).T.flatten().astype(np.uint32)
    
    with open(data_path, 'wb') as f:
        f.write(labels_flat.tobytes())