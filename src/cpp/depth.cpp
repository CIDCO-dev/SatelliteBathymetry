#include "SENTINEL.hpp"

#include <cmath>

#include <fstream>
#include <sstream>

#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/kdtree/kdtree_flann.h>

//#include "../MBES-lib/src/math/CoordinateTransform.hpp"
//#include "../MBES-lib/src/Position.hpp"

void readFileXYZ(std::string filename, pcl::PointCloud<pcl::PointXYZ>::Ptr &cloud){

	std::ifstream myfile (filename);
	
	std::string line;
	double x,y,z;
	Eigen::Vector3d positionEcef;
	Position positionGeographic(0,0,0,0);
	
	if (myfile.is_open()){
		while ( getline (myfile,line) ) {
			std::istringstream ss(line);
			ss >> x >> y >> z;
			
			//std::cout<<x <<" "<<y <<" "<< z<<"\n";
			/*
			positionEcef(0) = x;
			positionEcef(1) = y;
			positionEcef(2) = z;
			*/
			//CoordinateTransform::convertECEFToLongitudeLatitudeElevation(positionEcef, positionGeographic);
			
			//Eigen::Vector3d vectorGeographic = positionGeographic.getVector();
			
			// lat lon depth
			cloud->push_back(pcl::PointXYZ(x, y, z));
		}
	}
}


int main(int argc, const char* argv[]) {
    
    if (argc < 2) {
		std::cerr << "usage: ./depth dirPath\n";
		std::cerr << "the directory must contain all directories of the different resolution\n";
		return -1;
	}
	
	/*
	std::string dirPath = argv[1];
	Sentinel sentinel(dirPath);
	auto resolutions = sentinel.get_all_files();
	
	//access images
	auto paths = resolutions["R60m"];
	
	// https://gisgeography.com/sentinel-2-bands-combinations/
	//  CIDCO-dev/SatelliteBathymetry/doc/Stumpf2003.pdf
	std::string blueBandPath = paths["B02"]; // blue band
	std::string greenBandPath = paths["B03"]; // green bad
	
	cv::Mat blueBand = cv::imread(blueBandPath, cv::IMREAD_LOAD_GDAL);
	cv::Mat greenBand = cv::imread(greenBandPath, cv::IMREAD_LOAD_GDAL);
	
	cv::Mat blueBandwater = sentinel.extract_water(blueBand);
	cv::Mat greenBandwater = sentinel.extract_water(greenBand);
	*/
	
	
	/*
	CIDCO-dev/SatelliteBathymetry/doc/Stumpf2003.pdf, p.4, 
	Coefficients m1 and m0 in Eq. 9 were obtained from a comparison of image-
	derived values with chart depths from the beach, three flat
	areas of different depths in Kure (3, 8, and 12 m) and one
	sloping area (at ;16 m).
	*/
	
	
	pcl::PointCloud<pcl::PointXYZ>::Ptr cloud (new pcl::PointCloud<pcl::PointXYZ>);
	
	readFileXYZ("../data/points/test.xyz", cloud);
	
	pcl::KdTreeFLANN<pcl::PointXYZ> kdtree;
	kdtree.setInputCloud (cloud);
	
	// get point with depth between 3m and 20m
	for(unsigned int i = 0; i < cloud->points.size(); i++){
		
		
		if(cloud->points[i].z >= 3 && cloud->points[i].z < 20){
			
			std::cout<<"depth : " << cloud->points[i].z <<"\n";
			
			std::vector<int> pointIndex;
			std::vector<float> distances; //squared
			
			if ( kdtree.nearestKSearch(cloud->points[i], 10, pointIndex, distances) > 0 ){
				// check if area is about flat
				double averageDepth = 0;
				for(int j = 0; j < pointIndex.size(); ++j){
					averageDepth += cloud->points[pointIndex[j]].z;
				}
				averageDepth = averageDepth/pointIndex.size();
				std::cout<<"avg : " << averageDepth<<"\n";
			}		
			
		}
		
	}
	
	
	//std::vector<std::vector<double>> xyzImage;
	//std::vector<double> xyz;
	
	/*
	if (blueBandwater.size != greenBandwater.size){
		std::cerr<< "water images are not the same size ! \n";
		return -1;
	}
	else{
		for(int row = 0; row < blueBandwater.rows; ++row){
			for(int col = 0; col < blueBandwater.cols; ++cols){
				
				uint16_t pixelBlueBandwater = blueBandwater.at(row, col);
				uint16_t pixelGreenBandwater = greenBandwater.at(row, col);
				
				if(pixelWater2 > 0 && pixelWater3 > 1){
					log(pixelWater2) / log(pixelWater3)
				}
				
			}
		}
		
	}
	*/
	
    return 0;
	
}
