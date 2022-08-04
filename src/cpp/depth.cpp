#include "SENTINEL.hpp"

#include <cmath>

#include <fstream>
#include <sstream>

#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/kdtree/kdtree_flann.h>

  // WGS84 ellipsoid Parameters

  /**WGS84 ellipsoid semi-major axis*/
  double a = 6378137.0;

  /**WGS84 ellipsoid first eccentricity squared*/
  double e2 = 0.081819190842622 * 0.081819190842622;

  /**WGS84 ellipsoid inverse flattening*/
  double f = 1.0 / 298.257223563;

  /**WGS84 ellipsoid semi-minor axis*/
  double b = a * (1-f); // semi-minor axis

  /**WGS84 ellipsoid second eccentricity squared*/
  double epsilon = e2 / (1.0 - e2); // second eccentricity squared
  
  double PI = 3.14159265358979323846;
  
  double R2D = ((double)180/(double)PI);


std::vector<double> convertECEFToLongitudeLatitudeElevation(Eigen::Vector3d & positionEcef) {
    double x = positionEcef(0);
    double y = positionEcef(1);
    double z = positionEcef(2);

    // Bowring (1985) algorithm
    double p2 = x * x + y*y;
    double r2 = p2 + z*z;
    double p = std::sqrt(p2);
    double r = std::sqrt(r2);

    double tanu = (1 - f) * (z / p) * (1 + epsilon * b / r);
    double tan2u = tanu * tanu;

    double cos2u = 1.0 / (1.0 + tan2u);
    double cosu = std::sqrt(cos2u);
    double cos3u = cos2u * cosu;

    double sinu = tanu * cosu;
    double sin2u = 1.0 - cos2u;
    double sin3u = sin2u * sinu;

    double tanlat = (z + epsilon * b * sin3u) / (p - e2 * a * cos3u);
    double tan2lat = tanlat * tanlat;
    double cos2lat = 1.0 / (1.0 + tan2lat);
    double sin2lat = 1.0 - cos2lat;

    double coslat = std::sqrt(cos2lat);
    double sinlat = tanlat * coslat;

    double longitude = std::atan2(y, x);
    double latitude = std::atan(tanlat);
    double height = p * coslat + z * sinlat - a * sqrt(1.0 - e2 * sin2lat);
    
    std::vector<double> positionGeographic{latitude*R2D, longitude*R2D, height};
    
    return positionGeographic;
    
  }


void readFileXYZ(std::string filename, pcl::PointCloud<pcl::PointXYZ>::Ptr &cloud){

	std::ifstream myfile (filename);
	
	std::string line;
	double x,y,z;
	Eigen::Vector3d positionEcef;
	
	if (myfile.is_open()){
		while ( getline (myfile,line) ) {
			std::istringstream ss(line);
			ss >> x >> y >> z;
			
			//std::cout<<x <<" "<<y <<" "<< z<<"\n";
			positionEcef(0) = x;
			positionEcef(1) = y;
			positionEcef(2) = z;
			
			std::vector<double> positionGeographic = convertECEFToLongitudeLatitudeElevation(positionEcef);
			
			//std::cout<< positionGeographic[0] <<" " <<positionGeographic[1] <<" " <<positionGeographic[2] << "\n";
			
			// lat lon depth
			cloud->push_back(pcl::PointXYZ(positionGeographic[0], positionGeographic[1], positionGeographic[2]) );
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
