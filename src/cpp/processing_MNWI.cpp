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

int main(int argc, const char* argv[]) {
    
    if (argc < 2) {
		std::cerr << "usage: ./process dirPath\n";
		std::cerr << "the directory must contain all directories of the different resolution\n";
		return -1;
	}
	
	std::string dirPath = argv[1];
	Sentinel sentinel(dirPath);
	auto resolutions = sentinel.get_all_files();
	
	
	//access one image
	auto paths = resolutions["R60m"];
	auto b03Path = paths["B03"];
	auto b12Path = paths["B12"];
	
	cv::Mat b03 = cv::imread(b03Path, 0);
	cv::Mat b12 = cv::imread(b12Path, 0);
	
	
	cv::Mat mask = sentinel.generate_MNDWI_mask(b03, b12);
	
	cv::resize(mask, mask, cv::Size(915, 915), cv::INTER_LINEAR);
	cv::imshow( "mask" , mask );
	// Press  ESC on keyboard to exit
	char c=(char)cv::waitKey(0);
	if(c==27) cv::destroyAllWindows();

    return 0;
	
}
