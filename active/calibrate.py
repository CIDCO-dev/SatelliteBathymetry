"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from matplotlib.pyplot import figure, imshow, show
from numpy import inf, ones, random, vstack, zeros
from shapely.geometry import Point, Polygon
from numpy.linalg import lstsq
from random import randint
from rasterio import open
from os import listdir


def generate_borders(mask_):
    """Generates the borders starting from North-West boundary, clockwise."""
    north_ = list(mask_[0])
    south_ = list(mask_[-1])
    west_ = list([row_[0] for row_ in mask_])
    est_ = list([row_[-1] for row_ in mask_])
    south_.reverse()
    west_.reverse()
    return [north_, est_, south_, west_]


def generate_dic(borders_):
    """Generates a dictionary where each key corresponds to a diagonal zone."""
    values = []
    for border_ in borders_:
        values += border_
    values = sorted(set(values))
    return dict(zip(values, [[] for _ in values]))


def border_coord(border_, k, borders_):
    """Returns the right coordinates format depending on the border."""
    north, est, south, west = [borders_[i] for i in range(4)]
    if border_ == north:
        return [k, 0]
    if border_ == south:
        return [len(border_) - k, len(border_)]
    if border_ == west:
        return [0, len(border_) - k]
    if border_ == est:
        return [len(border_), k]


def generate_measures(size_, measures_):
    """Generates random coordinates and depth measurements of the seafloor."""
    depths_, points_ = zeros((size_, size_)), []
    for i in range(measures_):
        x_, y_ = [randint(0, size_) for _ in range(2)]
        depths_[x_ - 1, y_ - 1] = randint(0, 50)
        points_.append(Point([x_, y_]))
    return depths_, points_


def update_vert_dic(border_, dic_, borders_):
    """Adds the vertices of each diagonal zone to the dictionary."""
    corner_ = border_[0]
    dic_[corner_].append(border_coord(border_, 0, borders_))
    for i, pixel_ in enumerate(border_[:-1]):
        next_ = border_[i + 1]
        if pixel_ != next_:
            dic_[pixel_].append(border_coord(border_, i, borders_))
            dic_[next_].append(border_coord(border_, i + 1, borders_))


def update_cons_dic(cons_dic, vert_dic, points_, points_dic_, depths_):
    """Computes the constants (m0, m1) with a linear regression for each diagonal zone."""
    for key in vert_dic.keys():
        vert_dic[key].append(vert_dic[key][0])
        for point in points_:
            x, y = point.x - 1, point.y - 1
            if Polygon(vert_dic[key]).contains(point) and RTA[int(x), int(y)] != inf:
                points_dic_[key].append([depths_[int(x), int(y)], RTA[int(x), int(y)]])
        dep = [point[0] for point in points_dic_[key]]
        rta = [point[1] for point in points_dic_[key]]
        a = vstack([rta, ones(len(rta))]).T
        m1_, m0_ = lstsq(a, dep, rcond=None)[0]
        cons_dic[key] = [m1_, m0_]


def generate_depths(size_, borders_mask_, cons_dic, rta):
    """Computes the depth for each pixel, depending on the associated constants (m0, m1)."""
    depths_calc_ = zeros((size_, size_))
    for i, row_ in enumerate(borders_mask_):
        for j, pixel_ in enumerate(row_):
            m0_, m1_ = cons_dic[int(pixel_)]
            if rta[i, j] != inf:
                depths_calc_[i, j] = m1_ * rta[i, j] + m0_
            else:
                depths_calc_[i, j] = inf
    return depths_calc_


def calibrate_rta(borders_mask_, size_, rta, measures_):
    """Calibrates a given RTA product."""
    borders = generate_borders(borders_mask_)
    vertices_dic, points_dic, constants_dic = [generate_dic(borders) for i in range(3)]
    for border in borders:
        update_vert_dic(border, vertices_dic, borders)
    depths, points = generate_measures(size_, measures_)
    update_cons_dic(constants_dic, vertices_dic, points, points_dic, depths)
    depths_calc = generate_depths(size_, borders_mask_, constants_dic, rta)
    figure('Seafloor Depth')
    imshow(depths_calc, 'ocean')


if __name__ == '__main__':

    base_path = f"/home/fundy/Documents/Constant"  # Directory containing the unzipped products
    product_index = 0
    product = f"{base_path}/{listdir(base_path)[product_index]}/GRANULE"
    directory = f"{product}/{listdir(product)[0]}"
    band = 'B01'
    borders_mask = open(f"{directory}/QI_DATA/MSK_DETFOO_{band}.jp2").read(1)
    size = borders_mask.shape[0]
    RTA = random.rand(size, size) + 0.7
    imshow(RTA, 'ocean')
    measures = 100

    calibrate_rta(borders_mask, size, RTA, measures)

    show()
