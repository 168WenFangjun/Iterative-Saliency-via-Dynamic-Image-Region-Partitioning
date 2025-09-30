#include "../../include/colorspace_utils.h"
#include <algorithm>
#include <cmath>

cv::Vec3d ColorspaceUtils::rgb_to_lab(const cv::Vec3d& rgb) {
    cv::Vec3d lab;
    lab[0] = 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2];
    lab[1] = 0.5 * (rgb[0] - rgb[1]);
    lab[2] = 0.5 * (rgb[1] - rgb[2]);
    return lab * 100.0;
}

cv::Vec3d ColorspaceUtils::rgb_to_xyz(const cv::Vec3d& rgb) {
    cv::Vec3d xyz;
    xyz[0] = 0.412453 * rgb[0] + 0.357580 * rgb[1] + 0.180423 * rgb[2];
    xyz[1] = 0.212671 * rgb[0] + 0.715160 * rgb[1] + 0.072169 * rgb[2];
    xyz[2] = 0.019334 * rgb[0] + 0.119193 * rgb[1] + 0.950227 * rgb[2];
    return xyz * 100.0;
}

cv::Mat ColorspaceUtils::convert_colorspace(const cv::Mat& image, const std::string& conversion) {
    cv::Mat result = image.clone();
    
    if (conversion == "Lab<-RGB" || conversion == "RGB->Lab") {
        for (int i = 0; i < image.rows; i++) {
            for (int j = 0; j < image.cols; j++) {
                cv::Vec3d rgb = image.at<cv::Vec3d>(i, j);
                cv::Vec3d lab = rgb_to_lab(rgb);
                result.at<cv::Vec3d>(i, j) = lab;
            }
        }
    } else if (conversion == "XYZ<-RGB" || conversion == "RGB->XYZ") {
        for (int i = 0; i < image.rows; i++) {
            for (int j = 0; j < image.cols; j++) {
                cv::Vec3d rgb = image.at<cv::Vec3d>(i, j);
                cv::Vec3d xyz = rgb_to_xyz(rgb);
                result.at<cv::Vec3d>(i, j) = xyz;
            }
        }
    }
    
    return result;
}