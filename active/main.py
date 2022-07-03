"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from matplotlib.pyplot import show
from acquire import Sentinel2
from rasterio import open
from process import *
from collect import *


if __name__ == '__main__':

    base_path = f"/home/fundy/Documents/MASS"
    subdirectories = ['zip_files', 'extracted_files']
    zip_path = f"{base_path}/{subdirectories[0]}"
    unzip_path = f"{base_path}/{subdirectories[1]}"
    # clear(base_path, subdirectories)

    # date = 'NOW-3DAYS'
    # sat = Sentinel2("samueldubos", "5c6a7b54")
    # footprint = 'POLYGON((-69 48, -58 48, -58 51, -69 51, -69 48))'
    # products = sat.search(date, footprint)

    # for product in products:
    #     sat.download(product, zip_path)

    # for product in listdir(zip_path):
    #     unzip(f"{zip_path}/{product}", unzip_path)

    from time import time
    beg = time()
    for product in listdir(unzip_path)[1:]:
        SCL, B2, B3, R10m, R20m = get_bands(product, unzip_path)
        SCL, B2, B3 = open(f"{R20m}/{SCL}").read(1), open(f"{R10m}/{B2}").read(1), open(f"{R10m}/{B3}").read(1)
        RTA = create_rta(SCL, B2, B3, dilatation=5, scale=(True, (500, 500)))
        convert_rta(RTA, m0=200, m1=200, plot=(True, f'{product}', 'ocean'))
    end = time()
    print(f'{round(end - beg, 2)} seconds.')
    show()
