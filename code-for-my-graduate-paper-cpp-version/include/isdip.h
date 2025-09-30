#ifndef ISDIP_H
#define ISDIP_H

#include <opencv2/opencv.hpp>
#include <vector>

struct ISIDPResult {
    std::vector<std::vector<double>> scanning_result;
    std::vector<std::vector<int>> inds;
};

class ISDIP {
public:
    static ISIDPResult isdip_saliency(double sp_pixels, const cv::Mat& superpixels, 
                                     int sp_num, int width, int height, 
                                     int channels, const cv::Mat& image);
    
private:
    static std::vector<double> calculate_feature_vector(const cv::Vec3d& rgb, 
                                                       const cv::Vec3d& lab, 
                                                       const cv::Vec3d& xyz);
    static double calculate_color_distance(const std::vector<double>& f1, 
                                         const std::vector<double>& f2);
};

#endif // ISDIP_H