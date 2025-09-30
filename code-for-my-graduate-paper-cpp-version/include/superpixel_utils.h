#ifndef SUPERPIXEL_UTILS_H
#define SUPERPIXEL_UTILS_H

#include <opencv2/opencv.hpp>
#include <string>

class SuperpixelUtils {
public:
    static cv::Mat generate_superpixels(const cv::Mat& image, int n_segments = 200, 
                                       double compactness = 20.0);
    static cv::Mat read_dat_file(const cv::Size& image_size, const std::string& data_path);
    static void save_dat_file(const cv::Mat& labels, const std::string& data_path);
};

#endif // SUPERPIXEL_UTILS_H