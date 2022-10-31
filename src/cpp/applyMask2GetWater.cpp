#include "SENTINEL.hpp"

std::string type2str(int type) {
  std::string r;

  uchar depth = type & CV_MAT_DEPTH_MASK;
  uchar chans = 1 + (type >> CV_CN_SHIFT);

  switch ( depth ) {
    case CV_8U:  r = "8U"; break;
    case CV_8S:  r = "8S"; break;
    case CV_16U: r = "16U"; break;
    case CV_16S: r = "16S"; break;
    case CV_32S: r = "32S"; break;
    case CV_32F: r = "32F"; break;
    case CV_64F: r = "64F"; break;
    default:     r = "User"; break;
  }

  r += "C";
  r += (chans+'0');

  return r;
}

void get_pixel_value(int action, int x, int y, int flags, void *userdata){
	
	if( action == cv::EVENT_LBUTTONDOWN ){
		cv::Mat*img = (cv::Mat*)userdata;
		std::cout<< x << " " << y <<"\n";
		int val = img->at<uchar>(y, x);
		std::cout<<val<<"\n";
		
	}
	
}


int main(int argc, const char* argv[]) {
    
    if (argc < 2) {
		std::cerr << "usage: ./getWater dirPath\n";
		std::cerr << "the directory must contain all directories of the different resolution\n";
		return -1;
	}
	
	std::string dirPath = argv[1];
	Sentinel sentinel(dirPath);
	auto resolutions = sentinel.get_all_files();
	
	
	//access images
	auto paths = resolutions["R60m"];
	std::string b04Path = paths["B04"];
	
	cv::Mat b04 = cv::imread(b04Path, cv::IMREAD_LOAD_GDAL);
	
	cv::Mat water = sentinel.extract_water(b04);
	
	
	// should not have to do this but at the moment i do...
	// https://answers.opencv.org/question/209252/imshow-data-types/
	water.convertTo(water, CV_8UC1);
	
	cv::resize(water, water, cv::Size(915, 915), cv::INTER_LINEAR);
	cv::imshow( "water" , water );
	//cv::setMouseCallback("mask", get_pixel_value, &mask);
	
	cv::resize(b04, b04, cv::Size(915, 915), cv::INTER_LINEAR);
	cv::imshow( "b04" , b04 );
	
	
	// Press  ESC on keyboard to exit
	char c=(char)cv::waitKey(0);
	if(c==27) cv::destroyAllWindows();
	
    return 0;
	
}
