#include "SENTINEL.hpp"


int main(int argc, const char* argv[]) {
    
    if (argc < 2) {
		std::cerr << "usage: ./visualize dirPath\n";
		std::cerr << "the directory must contain all directories of the different resolution\n";
		return -1;
	}
	
	std::string dirPath = argv[1];
	Sentinel sentinel(dirPath);
	auto resolutions = sentinel.get_all_files();
	
	// visualize all images
	
	for(auto &res : resolutions){
		std::map imgs = res.second;
		for(auto &imgPath : imgs){
			std::string image = imgPath.second;
			std::cout<<image<<"\n";
			
			cv::Mat img = cv::imread(image);
			std::cout<<img.size()<<"\n";
			
			cv::resize(img, img, cv::Size(915, 915), cv::INTER_LINEAR);

			cv::imshow( res.first + "/" + imgPath.first , img );
			// Press  ESC on keyboard to exit
			char c=(char)cv::waitKey(0);
			if(c==27) cv::destroyAllWindows();
			
		}
	}
	
	/*
	//access one image
	auto paths = resolutions["R60m"];
	auto imgpath = paths["TCI"];
	std::cout<<imgpath<<"\n";
	cv::Mat img = cv::imread(imgpath);
	cv::resize(img, img, cv::Size(915, 915), cv::INTER_LINEAR);
	cv::imshow( "img" , img );
	// Press  ESC on keyboard to exit
	char c=(char)cv::waitKey(0);
	if(c==27) cv::destroyAllWindows();
	*/
	
	
    return 0;
	
}
