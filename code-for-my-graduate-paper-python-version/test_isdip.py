"""
Test script for ISDIP implementation
"""
import os
import sys
import numpy as np
import cv2
from PIL import Image

# Add current directory to path
sys.path.append(os.path.dirname(__file__))

from superpixel_utils import generate_superpixels
from isdip import isdip_saliency

def test_single_image(image_path):
    """Test ISDIP on a single image"""
    print(f"Testing ISDIP on: {image_path}")
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return False
    
    try:
        # Read image
        img_bgr = cv2.imread(image_path)
        if img_bgr is None:
            print(f"Failed to read image: {image_path}")
            return False
            
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_in = img_rgb.astype(np.float64) / 255.0
        
        height, width, channels = img_in.shape
        print(f"Image size: {width}x{height}x{channels}")
        
        # Generate superpixels
        print("Generating superpixels...")
        superpixels = generate_superpixels(img_in, n_segments=200, compactness=20)
        sp_num = np.max(superpixels)
        sp_pixels = height * width / sp_num
        print(f"Generated {sp_num} superpixels, avg {sp_pixels:.1f} pixels per superpixel")
        
        # Run ISDIP algorithm
        print("Running ISDIP algorithm...")
        scanning_result, inds = isdip_saliency(sp_pixels, superpixels, sp_num, 
                                             width, height, channels, img_in)
        
        # Combine results from 4 directions
        superpixel_saliency = (scanning_result[0] * scanning_result[1] * 
                              scanning_result[2] * scanning_result[3])
        
        # Assign saliency values to pixels
        print("Generating saliency map...")
        sal_map = np.zeros((height, width))
        for j in range(sp_num):
            if j < len(inds) and inds[j] is not None and len(inds[j]) > 0:
                rows, cols = np.unravel_index(inds[j], (height, width))
                sal_map[rows, cols] = superpixel_saliency[j]
        
        # Normalize to 0-255
        if sal_map.max() > sal_map.min():
            sal_map = (sal_map - sal_map.min()) / (sal_map.max() - sal_map.min())
        sal_map = (sal_map * 255).astype(np.uint8)
        
        # Save result
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"{base_name}_saliency.png"
        Image.fromarray(sal_map, mode='L').save(output_path)
        print(f"Saliency map saved to: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

def main():
    """Main test function"""
    # Test with available images
    test_images = [
        "../test/3_95_95850.jpg",
        "../test/3_95_95850.bmp"
    ]
    
    success_count = 0
    for img_path in test_images:
        if test_single_image(img_path):
            success_count += 1
        print("-" * 50)
    
    print(f"Successfully processed {success_count}/{len(test_images)} images")

if __name__ == '__main__':
    main()