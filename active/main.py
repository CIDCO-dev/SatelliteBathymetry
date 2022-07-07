"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from matplotlib.pyplot import show
from acquire import Sentinel2
from rasterio import open
from pyproj import Geod
from collect import *
from process import *
from mosaic import *

if __name__ == '__main__':

    # Initialize the paths
    base_path = f"/home/fundy/Documents/MASS"
    subdirectories = ['zip_files', 'extracted_files']
    zip_path = f"{base_path}/{subdirectories[0]}"
    unzip_path = f"{base_path}/{subdirectories[1]}"
    clear(base_path, subdirectories)

    # Parametrize - Set the parameters
    sat = Sentinel2("samueldubos", "5c6a7b54")
    date1 = 'NOW-7DAYS'
    date2 = 'NOW-2DAYS'
    footprint = 'POLYGON((-69 48, -58 48, -58 51, -69 51, -69 48))'
    resolution = 600

    # Acquire - Search, download and extract the products
    products = sat.search(date1, date2, footprint)
    for product in products:
        sat.download(product, zip_path)
    for product in listdir(zip_path):
        unzip(f"{zip_path}/{product}", unzip_path)

    # Process - Collect and process the products
    all_RTA = []
    geodesy = Geod(ellps="WGS84")
    bounds_dic = dict(zip([0, 1, 2, 3], [[] for i in range(4)]))
    for product in listdir(unzip_path):
        SCL, B2, B3, R10m, R20m = get_jp2_names(product, unzip_path)
        SCL, B2, B3 = open(f"{R20m}/{SCL}").read(1), open(f"{R10m}/{B2}").read(1), open(f"{R10m}/{B3}").read(1)
        RTA = create_rta(SCL, B2, B3, dilatation=5, scale=(True, 60))
        XML = f"{unzip_path}/{product}/INSPIRE.xml"
        borders = get_bounds(XML)
        all_RTA.append([RTA, borders])
        est, west, south, north = [borders[i] for i in range(4)]
        for i, border in enumerate(borders):
            bounds_dic[i].append(border)

    # Result - Generate the full size result product
    r_est = max(bounds_dic[0])
    r_west = min(bounds_dic[1])
    r_south = min(bounds_dic[2])
    r_north = max(bounds_dic[3])
    r_borders = [r_est, r_west, r_south, r_north]
    geodesic_length = geodesy.line_length([r_est, r_west], [r_north, r_north])
    geodesic_height = geodesy.line_length([r_west, r_west], [r_north, r_south])
    r_x, r_y = int(geodesic_height / resolution), int(geodesic_length / resolution)
    result = zeros((r_x, r_y))

    # Mosaic - Insert each product in the result product
    for RTA, borders in all_RTA:
        est, west, south, north = [borders[i] for i in range(4)]
        min_x, min_y = transform_c2p(north, west, r_borders, [r_x, r_y])
        max_x, max_y = transform_c2p(south, est, r_borders, [r_x, r_y])
        for i, row_ in enumerate(RTA):
            for j, pixel_ in enumerate(row_):
                if RTA[i, j] != inf:
                    if min_x + i < r_x and min_y + j < r_y:
                        if result[min_x + i, min_y + j] == 0:
                            result[min_x + i, min_y + j] = RTA[i, j]
                        else:
                            if result[min_x + i, min_y + j] > RTA[i, j]:
                                result[min_x + i, min_y + j] = RTA[i, j]

    # Clean-up - Clear the empty pixels
    for i, row_ in enumerate(result):
        for j, pixel_ in enumerate(row_):
            if pixel_ == 0:
                result[i, j] = inf

    # Plotting - Display the result
    figure('Result')
    imshow(result, 'ocean')
    colorbar()
    show()
