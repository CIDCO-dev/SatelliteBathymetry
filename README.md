# SatelliteBathymetry
Satellite-Derived Bathymetry Toolkit

```
install dependencies 

mkdir build && cd build
cmake ..
make

```


global pipline pre-requisites registering here : https://scihub.copernicus.eu/dhus/#/self-registration

```
python3 scripts/pipeline username password workingDirectory
```


image processing developpement:

```
./visualize ../data/sat-imgs
./process ../data/sat-imgs
./getwater ../data/sat-imgs
./depth ../data/sat-imgs
```
