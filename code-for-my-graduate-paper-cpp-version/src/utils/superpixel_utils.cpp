#include "../../include/superpixel_utils.h"
#include <opencv2/ximgproc.hpp>
#include <fstream>

cv::Mat SuperpixelUtils::generate_superpixels(const cv::Mat& image, int n_segments, double compactness) {
    cv::Mat labels;
    cv::Mat img_float;
    image.convertTo(img_float, CV_32FC3);
    
    auto slic = cv::ximgproc::createSuperpixelSLIC(img_float, cv::ximgproc::SLIC, n_segments, compactness);
    slic->iterate();
    slic->getLabels(labels);
    
    labels += 1; // Convert to 1-based indexing
    return labels;
}

cv::Mat SuperpixelUtils::read_dat_file(const cv::Size& image_size, const std::string& data_path) {
    std::ifstream file(data_path, std::ios::binary);
    std::vector<uint32_t> data(image_size.width * image_size.height);
    file.read(reinterpret_cast<char*>(data.data()), data.size() * sizeof(uint32_t));
    
    cv::Mat labels(image_size.height, image_size.width, CV_32S);
    for (int i = 0; i < image_size.height; i++) {
        for (int j = 0; j < image_size.width; j++) {
            labels.at<int>(i, j) = data[j * image_size.height + i] + 1;
        }
    }
    return labels;
}

void SuperpixelUtils::save_dat_file(const cv::Mat& labels, const std::string& data_path) {
    std::ofstream file(data_path, std::ios::binary);
    for (int j = 0; j < labels.cols; j++) {
        for (int i = 0; i < labels.rows; i++) {
            uint32_t val = labels.at<int>(i, j) - 1;
            file.write(reinterpret_cast<const char*>(&val), sizeof(uint32_t));
        }
    }
}