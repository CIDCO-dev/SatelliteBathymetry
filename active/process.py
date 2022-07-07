"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from matplotlib.pyplot import colorbar, figure, imshow
from cv2 import dilate, INTER_LINEAR, resize
from numpy import inf, ones, zeros
from math import log


def generate_water_mask(scl, dilatation, size):
    """Generate a water mask without dilated clouds and useless pixels."""
    cloud_mask, useless_mask, water_mask = [zeros(size) for _ in range(3)]
    for i, row_ in enumerate(scl):
        for j, pixel_ in enumerate(row_):
            if pixel_ in [8, 9, 10, 11]:
                cloud_mask[i, j] = inf
            if pixel_ in [0, 1, 2, 3, 4, 5, 7]:
                useless_mask[i, j] = inf
    cloud_mask = dilate(cloud_mask, ones((dilatation, dilatation)))
    for i, row_ in enumerate(scl):
        for j, pixel_ in enumerate(row_):
            if cloud_mask[i, j] == inf or useless_mask[i, j] == inf:
                water_mask[i, j] = inf
    return water_mask


def apply_mask(img_, mask_, size):
    """Keeps only the pixels on the background of the mask."""
    result = zeros(size)
    for i, row_ in enumerate(mask_):
        for j, pixel_ in enumerate(row_):
            if pixel_ == 0:
                result[i, j] = img_[i, j]
    return result


def ratio_transform(band1, band2, size):
    """Applies the Ratio Transform Algorithm to the bands band1 and band2."""
    result = zeros(size)
    for i, row_ in enumerate(band1):
        for j, pixel_ in enumerate(row_):
            blue, green = band1[i, j], band2[i, j]
            if pixel_ != 0 and blue > 0 and green > 0 and green != 1:
                result[i, j] = log(blue) / log(green)
    return result


def create_rta(scl, band1, band2, dilatation, scale=(False, None)):
    """Creates a new masked image with RTA value for each pixel."""
    if scale[0]:
        size = (int(band1.shape[0] / scale[1]), int(band1.shape[1] / scale[1]))
        scl = resize(scl, size, interpolation=INTER_LINEAR)
        band1 = resize(band1, size, interpolation=INTER_LINEAR)
        band2 = resize(band2, size, interpolation=INTER_LINEAR)
        water_mask = generate_water_mask(scl, dilatation, size)
        band1_m = apply_mask(band1, water_mask, size)
        band2_m = apply_mask(band2, water_mask, size)
    else:
        water_mask = generate_water_mask(scl, dilatation, scl.shape)
        water_mask = resize(water_mask, band1.shape, interpolation=INTER_LINEAR)
        band1_m = apply_mask(band1, water_mask, band1.shape)
        band2_m = apply_mask(band2, water_mask, band1.shape)
    rta_ = ratio_transform(band1_m, band2_m, band1.shape)
    for i, row_ in enumerate(rta_):
        for j, pixel_ in enumerate(row_):
            if pixel_ == 0:
                rta_[i, j] = inf
    return rta_


def convert_rta(rta, m0, m1, plot=(False, None, None)):
    """Converts each RTA value into a depth in meters."""
    for i, row in enumerate(rta):
        for j, pixel in enumerate(row):
            if pixel == 0:
                rta[i, j] = inf
            else:
                rta[i, j] = -(m1 * rta[i, j] - m0)
    if plot:
        figure(plot[1])
        imshow(rta, plot[2])
        colorbar()


if __name__ == '__main__':

    pass
