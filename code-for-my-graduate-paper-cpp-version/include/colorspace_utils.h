#ifndef COLORSPACE_UTILS_H
#define COLORSPACE_UTILS_H

#include <opencv2/opencv.hpp>

class ColorspaceUtils {
public:
    static cv::Vec3d rgb_to_lab(const cv::Vec3d& rgb);
    static cv::Vec3d rgb_to_xyz(const cv::Vec3d& rgb);
    static cv::Mat convert_colorspace(const cv::Mat& image, const std::string& conversion);
};

#endif // COLORSPACE_UTILS_H