#ifndef SENTINEL
#define SENTINEL

#include <iostream>
#include "opencv2/opencv.hpp"
#include <opencv2/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <vector>
#include <filesystem>


std::string extract_band_name(std::string filename){
	std::vector<std::string> bandNames{"B01","B02","B03","B04","B05","B06","B07","B08","B8A","B09","B10","B11","B12","B13","AOT","SCL","TCI","WVP"};
	std::string bandName;
	int checksum = 0;
	for(int i =0; i<bandNames.size();++i){
		if (filename.find(bandNames[i]) != std::string::npos){
			++checksum;
			bandName = bandNames[i];
		}
	}
	if(checksum == 1){
		return bandName;
	}
	else{
		std::cerr<<"found "<< checksum <<" band name in " << filename<<"\n";
		return filename;
	}
	
}



class Sentinel{
	public:
		Sentinel(std::string dirPath){
			const std::filesystem::path path{dirPath};
			for (auto const& dir_entry : std::filesystem::directory_iterator{path}){
				if (dir_entry.is_directory()){
					//std::cout<<dir_entry.path().filename()<<"\n";
					for (auto const& file : std::filesystem::directory_iterator{dir_entry.path()}){
						if (file.is_regular_file() && file.path().extension() == ".jp2"){
							//std::cout<<file<<"\n";
							std::filesystem::path filePath = file.path();
							this->files.insert({extract_band_name(filePath.filename()), file.path()});
						}
						else{
							std::cerr<<"not a valid file or not a .jp2 file \n";
						}
					}
					this->resolutions.insert({dir_entry.path().filename(), files});
					this->files.clear();
				}
			}
		
		}
		
		std::map<std::string,std::map<std::string,std::string>> get_all_files() {return this->resolutions;}
		
		cv::Mat generate_MNDWI_mask(cv::Mat b03, cv::Mat infrared){
			
			if(b03.size != infrared.size){
				std::cerr<<"Bands are not the same resolution \n";
			}
			else{
				
				int y = b03.size[0];
				int x = b03.size[1];
				
				b03.convertTo(b03, CV_32FC1);
				infrared.convertTo(infrared, CV_32FC1);

				cv::Mat MNDWI = (b03 - infrared) / (b03 + infrared);

				cv::Mat mask(cv::Size(y, x), CV_8UC1, cv::Scalar(0));

				for(int row = 0; row < MNDWI.rows; ++row){
					for(int col = 0; col < MNDWI.cols; ++col){
						float pixel = MNDWI.at<float>(row, col, 0);
						if(pixel > 0){
							mask.at<uchar>(row, col) = 255;
						}
					}
				}
				return mask;
			}
			//XXX warning no return
		}
		
		cv::Mat extract_water(cv::Mat band){
			//XXX check dimention in case of colored image ?
			int y = band.size[0];
			int x = band.size[1];
			
			//access images
			auto paths = this->resolutions["R60m"];
			// https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/#units
			// scl bad is classified from 0 to 11. 6 is water.
			std::string sclPath = paths["SCL"];
			cv::Mat scl = cv::imread(sclPath, cv::IMREAD_LOAD_GDAL);
			//XXX check matrix type
			
			cv::Mat mask(cv::Size(y, x), CV_8UC1, cv::Scalar(0));
			
			for(int row = 0; row < scl.rows; ++row){
				for(int col = 0; col < scl.cols; ++col){
					if(scl.at<uchar>(row, col, 0) == 6){ 
						mask.at<uchar>(row, col) = 255;
					}
					else{
						mask.at<uchar>(row, col) = 0;
					}
				}
			}
			
			//TODO erode / dilate mask
			
			mask.convertTo(mask, CV_16UC1);
			
			cv::Mat result(cv::Size(y, x), CV_16UC1, cv::Scalar(0));
			
			cv::bitwise_and(band, mask, result);
			
			
			return result;
		}
		
	private:
		std::map<std::string,std::string> files;
		std::map<std::string,std::map<std::string,std::string>> resolutions;
};

#endif
