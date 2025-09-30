#include "../include/isdip.h"
#include "../include/colorspace_utils.h"
#include <cmath>
#include <algorithm>
#include <set>

ISIDPResult ISDIP::isdip_saliency(double sp_pixels, const cv::Mat& superpixels, 
                                 int sp_num, int width, int height, 
                                 int channels, const cv::Mat& image) {
    
    std::vector<cv::Vec3d> rgb_vals(sp_num);
    std::vector<std::vector<int>> inds(sp_num);
    
    // Calculate mean color for each superpixel
    for (int i = 0; i < sp_num; i++) {
        cv::Vec3d sum(0, 0, 0);
        int count = 0;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                if (superpixels.at<int>(y, x) == i + 1) {
                    inds[i].push_back(y * width + x);
                    cv::Vec3d pixel = image.at<cv::Vec3d>(y, x);
                    sum += pixel;
                    count++;
                }
            }
        }
        if (count > 0) rgb_vals[i] = sum / count;
    }
    
    // Color space conversions
    std::vector<cv::Vec3d> lab_vals(sp_num), xyz_vals(sp_num);
    for (int i = 0; i < sp_num; i++) {
        lab_vals[i] = ColorspaceUtils::rgb_to_lab(rgb_vals[i]);
        xyz_vals[i] = ColorspaceUtils::rgb_to_xyz(rgb_vals[i]);
    }
    
    // Construct feature vectors
    std::vector<std::vector<double>> features(sp_num);
    for (int i = 0; i < sp_num; i++) {
        features[i] = {rgb_vals[i][0], rgb_vals[i][1], rgb_vals[i][2],
                      xyz_vals[i][0], xyz_vals[i][1], xyz_vals[i][2],
                      lab_vals[i][0], lab_vals[i][1], lab_vals[i][2]};
    }
    
    int scanning_gap = std::max(1, (int)std::sqrt(sp_pixels) - 1);
    std::vector<std::vector<double>> scanning_result(4, std::vector<double>(sp_num, 0));
    
    // Four direction scanning
    for (int scanning_label = 0; scanning_label < 4; scanning_label++) {
        int loops_count = (scanning_label < 2) ? width : height;
        std::vector<std::vector<int>> bg_seeds(loops_count);
        
        // Generate background seeds for each position
        for (int i = 0; i < loops_count; i += scanning_gap) {
            std::set<int> unique_labels;
            
            if (scanning_label == 0) { // left to right
                for (int y = 0; y < height; y++) {
                    for (int x = 0; x <= i && x < width; x++) {
                        unique_labels.insert(superpixels.at<int>(y, x));
                    }
                }
            } else if (scanning_label == 1) { // right to left
                for (int y = 0; y < height; y++) {
                    for (int x = loops_count - i - 1; x < width; x++) {
                        unique_labels.insert(superpixels.at<int>(y, x));
                    }
                }
            } else if (scanning_label == 2) { // top to bottom
                for (int y = 0; y <= i && y < height; y++) {
                    for (int x = 0; x < width; x++) {
                        unique_labels.insert(superpixels.at<int>(y, x));
                    }
                }
            } else { // bottom to top
                for (int y = loops_count - i - 1; y < height; y++) {
                    for (int x = 0; x < width; x++) {
                        unique_labels.insert(superpixels.at<int>(y, x));
                    }
                }
            }
            
            bg_seeds[i] = std::vector<int>(unique_labels.begin(), unique_labels.end());
        }
        
        std::vector<std::vector<double>> weight_matrix(loops_count, std::vector<double>(sp_num, 0));
        loops_count /= 2;
        
        for (int loop_count = 0; loop_count < loops_count; loop_count += scanning_gap) {
            if (loop_count >= bg_seeds.size()) break;
            
            auto& current_bg_seeds = bg_seeds[loop_count];
            
            // Calculate average background feature
            std::vector<double> sum_bg_feature(9, 0);
            int bg_count = 0;
            for (int label : current_bg_seeds) {
                if (label > 0 && label <= sp_num) {
                    for (int j = 0; j < 9; j++) {
                        sum_bg_feature[j] += features[label - 1][j];
                    }
                    bg_count++;
                }
            }
            
            if (bg_count == 0) continue;
            
            for (int j = 0; j < 9; j++) {
                sum_bg_feature[j] /= bg_count;
            }
            
            // Inherit previous weights
            if (loop_count >= scanning_gap) {
                weight_matrix[loop_count] = weight_matrix[loop_count - scanning_gap];
            }
            
            // Calculate color differences for center seeds
            for (int i = 0; i < sp_num; i++) {
                bool is_bg = std::find(current_bg_seeds.begin(), current_bg_seeds.end(), i + 1) != current_bg_seeds.end();
                if (!is_bg) {
                    double color_diff = calculate_color_distance(features[i], sum_bg_feature);
                    weight_matrix[loop_count][i] += color_diff;
                }
            }
        }
        
        if (loop_count - scanning_gap >= 0 && loop_count - scanning_gap < weight_matrix.size()) {
            scanning_result[scanning_label] = weight_matrix[loop_count - scanning_gap];
        }
    }
    
    return {scanning_result, inds};
}

double ISDIP::calculate_color_distance(const std::vector<double>& f1, const std::vector<double>& f2) {
    double sum = 0;
    for (size_t i = 0; i < f1.size(); i++) {
        double diff = f1[i] - f2[i];
        sum += diff * diff;
    }
    return std::sqrt(sum);
}