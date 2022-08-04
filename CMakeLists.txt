cmake_minimum_required(VERSION 3.13)


project(prosatcimg VERSION 1.0.0)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/include)

add_executable(visualize src/cpp/visualize.cpp)
find_package(OpenCV 4.2 REQUIRED)
target_link_libraries(visualize PUBLIC ${OpenCV_LIBS} )

add_executable(process src/cpp/processing_MNWI.cpp)
target_link_libraries(process PUBLIC ${OpenCV_LIBS} )

add_executable(getwater src/cpp/applyMask2GetWater.cpp)
target_link_libraries(getwater PUBLIC ${OpenCV_LIBS} )

add_executable(depth src/cpp/depth.cpp)
find_package(PCL 1.3 REQUIRED)
include_directories(${PCL_INCLUDE_DIRS})
link_directories(${PCL_LIBRARY_DIRS})
add_definitions(${PCL_DEFINITIONS})
target_link_libraries(depth PUBLIC ${OpenCV_LIBS} ${PCL_LIBRARIES})

