"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from matplotlib.pyplot import colorbar, figure, imshow
from cv2 import dilate, INTER_LINEAR, resize
from numpy import inf, ones, zeros
from math import log


def generate_mask_water(scl, dilatation, size):

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
    result = zeros(size)  # Create an empty image
    for i, row_ in enumerate(mask_):  # Browse the mask row after row
        for j, pixel_ in enumerate(row_):  # Browse rows pixel after pixel
            if pixel_ == 0:  # Pixel on the background
                result[i, j] = img_[i, j]  # Empty image updated
    return result


def ratio_transform(band1, band2, size):
    """Applies the Ratio Transform Algorithm to the bands band1 and band2."""
    result = zeros(size)  # Create an empty image
    for i, row_ in enumerate(band1):  # Browse the band row after row
        for j, pixel_ in enumerate(row_):  # Browse rows pixel after pixel
            blue, green = band1[i, j], band2[i, j]  # Define each band
            if pixel_ != 0 and blue > 0 and green > 0 and green != 1:  # Valid pixel (definition domain etc.)
                result[i, j] = log(blue) / log(green)  # Ratio Transform Algorithm
    return result


def create_rta(scl, band1, band2, dilatation, scale=(False, None)):
    """Creates a new masked image with RTA value for each pixel."""
    if scale[0]:  # Resizing requested
        size = scale[1]  # Define the size
        scl = resize(scl, size, interpolation=INTER_LINEAR)  # Resize SCL
        band1 = resize(band1, size, interpolation=INTER_LINEAR)  # Resize band1
        band2 = resize(band2, size, interpolation=INTER_LINEAR)  # Resize band2
        water_mask = generate_mask_water(scl, dilatation, size)
        band1_m = apply_mask(band1, water_mask, size)  # Mask out the invalid pixels
        band2_m = apply_mask(band2, water_mask, size)  # Mask out the invalid pixels
    else:  # Resizing not requested
        water_mask = generate_mask_water(scl, dilatation, scl.shape)
        water_mask = resize(water_mask, band1.shape, interpolation=INTER_LINEAR)
        band1_m = apply_mask(band1, water_mask, band1.shape)  # Mask out the invalid pixels
        band2_m = apply_mask(band2, water_mask, band1.shape)  # Mask out the invalid pixels
    return ratio_transform(band1_m, band2_m, band1.shape)  # Apply the Ratio Transform Algorithm


def convert_rta(rta, m0, m1, plot=(False, None, None)):
    """Converts each RTA value into a depth in meters."""
    for i, row in enumerate(rta):  # Browse the rta-image row after row
        for j, pixel in enumerate(row):  # Browse rows pixel after pixel
            if pixel == 0:  # Invalid pixel
                rta[i, j] = inf  # Remove pixel from final image
            else:  # Valid pixel
                rta[i, j] = -(m1 * rta[i, j] - m0)  # Convert the pixel
    if plot:  # Plotting requested
        figure(plot[1])  # Create new figure
        imshow(rta, plot[2])  # Plot the image
        colorbar()


if __name__ == '__main__':

    pass
