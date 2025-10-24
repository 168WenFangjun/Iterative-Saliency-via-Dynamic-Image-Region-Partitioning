#!/usr/bin/env python3
"""
Main program for ISDIP saliency detection
"""
import os
import glob
import numpy as np
import cv2
from PIL import Image

from superpixel_utils import generate_superpixels, save_dat_file
from isdip import isdip_saliency

def main():
    # Parameters
    sp_number = 200
    img_root = "./test/"
    sal_dir = "./saliencymap/"
    sup_dir = "./superpixels/"
    
    # Create directories
    os.makedirs(sal_dir, exist_ok=True)
    os.makedirs(sup_dir, exist_ok=True)
    
    # Get image files
    img_files = glob.glob(os.path.join(img_root, "*.jpg"))
    
    for img_path in img_files:
        print(f"Processing: {os.path.basename(img_path)}")
        
        # Read image
        img_bgr = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        img_in = img_rgb.astype(np.float64) / 255.0
        
        height, width, channels = img_in.shape
        
        # Generate superpixels
        superpixels = generate_superpixels(img_in, n_segments=sp_number, compactness=20.0)
        sp_num = np.max(superpixels)
        sp_pixels = (height * width) / sp_num
        
        # Save superpixel labels
        base_name = os.path.splitext(os.path.basename(img_path))[0]
        sp_file = os.path.join(sup_dir, base_name + ".dat")
        save_dat_file(superpixels, sp_file)
        
        # Run ISDIP algorithm
        scanning_result, inds = isdip_saliency(sp_pixels, superpixels, sp_num, 
                                             width, height, channels, img_in)
        
        # Combine results from 4 directions
        superpixel_saliency = np.ones(sp_num)
        for i in range(4):
            superpixel_saliency *= scanning_result[i]
        
        # Assign saliency values to pixels
        sal_map = np.zeros((height, width))
        for i in range(sp_num):
            if i < len(inds) and len(inds[i]) > 0:
                for idx in inds[i]:
                    y = idx // width
                    x = idx % width
                    if y < height and x < width:
                        sal_map[y, x] = superpixel_saliency[i]
        
        # Normalize to 0-255
        if sal_map.max() > sal_map.min():
            sal_map = (sal_map - sal_map.min()) / (sal_map.max() - sal_map.min())
        sal_map = (sal_map * 255).astype(np.uint8)
        
        # Save saliency map
        out_path = os.path.join(sal_dir, base_name + ".png")
        cv2.imwrite(out_path, sal_map)

if __name__ == "__main__":
    main()