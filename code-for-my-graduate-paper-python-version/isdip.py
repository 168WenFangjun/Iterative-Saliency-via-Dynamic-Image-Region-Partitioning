"""
ISDIP (Image Saliency Detection using Iterative Scanning and Directional Propagation)
"""
import numpy as np
from colorspace_utils import rgb_to_lab, rgb_to_xyz

def calculate_color_distance(f1, f2):
    """Calculate Euclidean distance between two feature vectors"""
    diff = np.array(f1) - np.array(f2)
    return np.sqrt(np.sum(diff * diff))

def isdip_saliency(sp_pixels, superpixels, sp_num, width, height, channels, image):
    """
    ISDIP saliency detection algorithm
    Args:
        sp_pixels: average pixels per superpixel
        superpixels: superpixel label matrix (H, W)
        sp_num: number of superpixels
        width, height, channels: image dimensions
        image: input image (H, W, C)
    Returns:
        scanning_result: list of 4 saliency maps from different directions
        inds: list of pixel indices for each superpixel
    """
    # Initialize arrays
    rgb_vals = np.zeros((sp_num, 3))
    inds = [[] for _ in range(sp_num)]
    
    # Calculate mean color for each superpixel
    for i in range(sp_num):
        mask = (superpixels == i + 1)  # 1-based indexing
        y_coords, x_coords = np.where(mask)
        if len(y_coords) > 0:
            # Store pixel indices
            pixel_indices = y_coords * width + x_coords
            inds[i] = pixel_indices.tolist()
            
            # Calculate mean RGB values
            pixel_values = image[y_coords, x_coords]
            rgb_vals[i] = np.mean(pixel_values, axis=0)
    
    # Color space conversions
    lab_vals = np.zeros((sp_num, 3))
    xyz_vals = np.zeros((sp_num, 3))
    
    for i in range(sp_num):
        lab_vals[i] = rgb_to_lab(rgb_vals[i].reshape(1, 1, 3)).flatten()
        xyz_vals[i] = rgb_to_xyz(rgb_vals[i].reshape(1, 1, 3)).flatten()
    
    # Construct feature vectors (RGB + XYZ + LAB)
    features = []
    for i in range(sp_num):
        feature = np.concatenate([
            rgb_vals[i],
            xyz_vals[i], 
            lab_vals[i]
        ])
        features.append(feature)
    

    
    # Scanning parameters
    scanning_gap = max(1, int(np.sqrt(sp_pixels)) - 1)
    scanning_result = [np.zeros(sp_num) for _ in range(4)]
    
    # Four direction scanning
    for scanning_label in range(4):
        if scanning_label < 2:  # horizontal scanning
            loops_count = width
        else:  # vertical scanning
            loops_count = height
            
        # Generate background seeds for each position
        bg_seeds = {}
        for i in range(0, loops_count, scanning_gap):
            unique_labels = set()
            
            if scanning_label == 0:  # left to right
                for y in range(height):
                    for x in range(min(i + 1, width)):
                        unique_labels.add(superpixels[y, x])
            elif scanning_label == 1:  # right to left
                for y in range(height):
                    for x in range(loops_count - i - 1, width):
                        unique_labels.add(superpixels[y, x])
            elif scanning_label == 2:  # top to bottom
                for y in range(min(i + 1, height)):
                    for x in range(width):
                        unique_labels.add(superpixels[y, x])
            else:  # bottom to top
                for y in range(loops_count - i - 1, height):
                    for x in range(width):
                        unique_labels.add(superpixels[y, x])
            
            bg_seeds[i] = list(unique_labels)
        
        # Weight matrix construction
        weight_matrix = {}
        for i in range(0, loops_count, scanning_gap):
            weight_matrix[i] = np.zeros(sp_num)
        
        # Iterate through scanning positions
        loops_count = loops_count // 2
        
        for loop_count in range(0, loops_count, scanning_gap):
            if loop_count not in bg_seeds:
                continue
                
            current_bg_seeds = bg_seeds[loop_count]
            
            # Calculate average background feature
            sum_bg_feature = np.zeros(9)  # RGB + XYZ + LAB = 9 dimensions
            bg_count = 0
            
            for label in current_bg_seeds:
                if label > 0 and label <= sp_num:
                    sum_bg_feature += features[label - 1]  # Convert to 0-based
                    bg_count += 1
            
            if bg_count == 0:
                continue
                
            avg_bg_feature = sum_bg_feature / bg_count
            
            # Inherit previous weights
            if loop_count >= scanning_gap and (loop_count - scanning_gap) in weight_matrix:
                weight_matrix[loop_count] = weight_matrix[loop_count - scanning_gap].copy()
            
            # Calculate color differences for center seeds
            for i in range(sp_num):
                label = i + 1  # Convert to 1-based
                if label not in current_bg_seeds:
                    color_diff = calculate_color_distance(features[i], avg_bg_feature)
                    weight_matrix[loop_count][i] += color_diff
        
        # Store final result
        if loop_count - scanning_gap >= 0 and (loop_count - scanning_gap) in weight_matrix:
            scanning_result[scanning_label] = weight_matrix[loop_count - scanning_gap]
        elif loop_count in weight_matrix:
            scanning_result[scanning_label] = weight_matrix[loop_count]
    
    return scanning_result, inds