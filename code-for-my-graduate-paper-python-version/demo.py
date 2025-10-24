"""
Demo script for ISDIP saliency detection
"""
import os
import time
import numpy as np
import cv2
from PIL import Image
import glob

from superpixel_utils import generate_superpixels, save_dat_file
from isdip import isdip_saliency

def main():
    # Parameters
    sp_number = 200  # superpixel number
    dataset = 'MSRA1000'
    method = 'ISDIP'
    
    # Paths
    img_root = './test/'
    sal_dir = './saliencymap/'
    sup_dir = './superpixels/'
    
    # Create directories
    os.makedirs(sup_dir, exist_ok=True)
    os.makedirs(sal_dir, exist_ok=True)
    
    # Get image files
    img_files = glob.glob(os.path.join(img_root, '*.jpg'))
    
    start_time = time.time()
    
    for i, img_path in enumerate(img_files):
        print(f"Processing image {i+1}/{len(img_files)}: {img_path}")
        
        # Read image
        img_bgr = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_in = img_rgb.astype(np.float64) / 255.0
        
        height, width, channels = img_in.shape
        
        # Save as BMP for consistency
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        bmp_path = os.path.join(os.path.dirname(img_path), base_name + '.bmp')
        cv2.imwrite(bmp_path, img_bgr)
        
        # Generate superpixels
        superpixels = generate_superpixels(img_in, n_segments=sp_number, compactness=20)
        sp_num = np.max(superpixels)
        sp_pixels = height * width / sp_num
        
        # Save superpixel labels
        sp_file = os.path.join(sup_dir, base_name + '.dat')
        save_dat_file(superpixels, sp_file)
        
        # Run ISDIP algorithm
        scanning_result, inds = isdip_saliency(sp_pixels, superpixels, sp_num, 
                                             width, height, channels, img_in)
        
        # Combine results from 4 directions
        # Method 1: multiply all 4 directions
        superpixel_saliency = (scanning_result[0] * scanning_result[1] * 
                              scanning_result[2] * scanning_result[3])
        
        # Alternative combinations (commented out):
        # superpixel_saliency = scanning_result[0]  # single direction
        # superpixel_saliency = scanning_result[0] * scanning_result[1]  # 2 directions
        # superpixel_saliency = (scanning_result[0] * scanning_result[1] * 
        #                       scanning_result[2])  # 3 directions
        
        # Assign saliency values to pixels
        sal_map = np.zeros((height, width))
        for j in range(sp_num):
            if j < len(inds) and inds[j] is not None and len(inds[j]) > 0:
                # Convert flat indices to 2D coordinates
                rows, cols = np.unravel_index(inds[j], (height, width))
                sal_map[rows, cols] = superpixel_saliency[j]
        
        # Normalize to 0-255
        if sal_map.max() > sal_map.min():
            sal_map = (sal_map - sal_map.min()) / (sal_map.max() - sal_map.min())
        sal_map = (sal_map * 255).astype(np.uint8)
        
        # Save saliency map
        out_path = os.path.join(sal_dir, base_name + '.png')
        Image.fromarray(sal_map, mode='L').save(out_path)
        
        elapsed = time.time() - start_time
        print(f"Elapsed time: {elapsed:.2f} seconds")

if __name__ == '__main__':
    main()