# SatelliteBathymetry
Satellite-Derived Bathymetry Toolkit

## build cpp
Install dependencies listed in DEPENDENCIES.TXT
```
mkdir build && cd build
cmake ..
make

```

## pipeline example
global pipline pre-requisites registering here : https://scihub.copernicus.eu/dhus/#/self-registration

```
python3 scripts/pipeline username password workingDirectory
```


## Satellite image processing developpement:

Visualize all satellite image of a sentinel2 product
```
./visualize ../data/sat-imgs
```
Computing MNDWI for sentinel2 images
```
./process ../data/sat-imgs
```
Extract water pixels
```
./getwater ../data/sat-imgs
```
Compute depth - not working yet
```
./depth ../data/sat-imgs
```
