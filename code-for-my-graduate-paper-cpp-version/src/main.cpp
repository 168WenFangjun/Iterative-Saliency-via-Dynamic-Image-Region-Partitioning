#include "../include/isdip.h"
#include "../include/superpixel_utils.h"
#include <opencv2/opencv.hpp>
#include <filesystem>
#include <iostream>

int main() {
    const int sp_number = 200;
    const std::string img_root = "../test/";
    const std::string sal_dir = "../saliencymap/";
    const std::string sup_dir = "../superpixels/";
    
    std::filesystem::create_directories(sal_dir);
    std::filesystem::create_directories(sup_dir);
    
    for (const auto& entry : std::filesystem::directory_iterator(img_root)) {
        if (entry.path().extension() == ".jpg") {
            std::cout << "Processing: " << entry.path().filename() << std::endl;
            
            cv::Mat img_bgr = cv::imread(entry.path().string());
            cv::Mat img_rgb;
            cv::cvtColor(img_bgr, img_rgb, cv::COLOR_BGR2RGB);
            
            cv::Mat img_in;
            img_rgb.convertTo(img_in, CV_64FC3, 1.0/255.0);
            
            int height = img_in.rows, width = img_in.cols, channels = img_in.channels();
            
            // Generate superpixels
            cv::Mat superpixels = SuperpixelUtils::generate_superpixels(img_in, sp_number, 20.0);
            int sp_num = 0;
            cv::minMaxLoc(superpixels, nullptr, reinterpret_cast<double*>(&sp_num));
            double sp_pixels = (double)(height * width) / sp_num;
            
            // Save superpixel labels
            std::string base_name = entry.path().stem().string();
            std::string sp_file = sup_dir + base_name + ".dat";
            SuperpixelUtils::save_dat_file(superpixels, sp_file);
            
            // Run ISDIP algorithm
            auto result = ISDIP::isdip_saliency(sp_pixels, superpixels, sp_num, width, height, channels, img_in);
            
            // Combine results from 4 directions
            std::vector<double> superpixel_saliency(sp_num);
            for (int i = 0; i < sp_num; i++) {
                superpixel_saliency[i] = result.scanning_result[0][i] * result.scanning_result[1][i] * 
                                       result.scanning_result[2][i] * result.scanning_result[3][i];
            }
            
            // Assign saliency values to pixels
            cv::Mat sal_map = cv::Mat::zeros(height, width, CV_64F);
            for (int i = 0; i < sp_num; i++) {
                for (int idx : result.inds[i]) {
                    int y = idx / width;
                    int x = idx % width;
                    if (y < height && x < width) {
                        sal_map.at<double>(y, x) = superpixel_saliency[i];
                    }
                }
            }
            
            // Normalize to 0-255
            double min_val, max_val;
            cv::minMaxLoc(sal_map, &min_val, &max_val);
            if (max_val > min_val) {
                sal_map = (sal_map - min_val) / (max_val - min_val);
            }
            sal_map *= 255;
            
            cv::Mat sal_map_uint8;
            sal_map.convertTo(sal_map_uint8, CV_8U);
            
            std::string out_path = sal_dir + base_name + ".png";
            cv::imwrite(out_path, sal_map_uint8);
        }
    }
    
    return 0;
}