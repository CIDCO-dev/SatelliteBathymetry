from shapely.ops import polygonize
import matplotlib.pyplot as plt
from numpy import pi, cos, sin
from geojson_algos import *
from rdp import rdp
import numpy as np
from math import log, factorial
import sys


def circle(r, n, x0, y0):
    """Generates a quasi-circle of radius r, n points and origin [x0, y0]"""
    thetas = [2 * i * pi / n for i in range(n)] + [0]
    answer = []
    for theta in thetas:
        x = round(x0 + r * cos(theta), 5)
        y = round(y0 + r * sin(theta), 5)
        answer.append([x, y])

    return answer


def index_name(name_, geojson_):
    """Finds the index of a specified polygon in a GEOjson file."""
    geojson_file = read_geojson(geojson_)
    for i, zone in enumerate(geojson_file['features']):
        if zone['properties']['NOM'] == name_:
            return i
    sys.stderr.write(f'Incorrect name.')


def split(poly, splitter):
    """[Imitation of shapely] Splits a polygon with a LineString."""
    union = poly.boundary.union(splitter)

    return [pg for pg in polygonize(union) if poly.contains(pg.representative_point())]


def plot_polygon(polygon_, color='blue'):
    """"Plots a polygon using matplotlib.pyplot module"""
    xs, ys = [], []
    if type(polygon_) == Polygon:
        for point in polygon_.exterior.coords:
            xs.append(point[0])
            ys.append(point[1])
    else:
        xs, ys = zip(*polygon_)
    plt.plot(xs, ys, color=color)


def find_splitting_speed(polygon_, m):
    """Finds the minimum of rays in order to complete the polygon splitting."""
    k = len(polygon_.exterior.coords) / m
    i = 0
    while k > factorial(i):
        i += 1

    return i


def split_once(polygon_, n):
    """Splits a polygon into n polygons, using its centroid."""
    centroid = polygon_.centroid
    r = centroid.hausdorff_distance(polygon_.interiors)
    splitter = []
    thetas = [2 * pi * i / n for i in range(n)]
    for theta in thetas:
        x = centroid.x + r * cos(theta)
        y = centroid.y + r * sin(theta)
        # plt.plot(x, y, marker='*', color='blue')
        splitter.append(centroid)
        splitter.append(Point([x, y]))
    multipolygon_ = split(polygon_, LineString(splitter))

    clr = list(uniform(0, 1) for _ in range(3))
    for poly in multipolygon_:
        plot_polygon(Polygon(poly.buffer(0).exterior), color=clr)
    # plt.plot(centroid.x, centroid.y, marker='o', color='pink')
    # plot_polygon(Polygon(polygon_.buffer(0.2).exterior))

    return multipolygon_


def split_till_end(polygon_, m, n, q):
    """Splits a polygon recursively until all polygons have less than m vertices"""
    if len(polygon_.exterior.coords) < m:
        print(f'q = {q}')
        return None
    multipolygon = split_once(polygon_, n)
    vertices = [len(polygon.exterior.coords) for polygon in multipolygon]
    print(vertices)
    # if max(vertices) < m:
    #     return 0
    if max(vertices) < m:
        print(f'q = {q}')
        return None
    else:
        for polygon in multipolygon:
            if len(polygon.exterior.coords) > m:
                q += n
                split_till_end(polygon, m, n, q)


def safe_simplification(polygon_, n):
    """Simplifies a polygon by a representative epsilon."""
    shapely_polygon_ = Polygon(LinearRing(polygon_))
    perimeter = shapely_polygon_.length
    points = len(polygon_)
    distance = perimeter / (n * points)

    return rdp(polygon_, distance)


def loss_percentage(polygon_, n):
    """Displays the percentage of points lost during the simplification."""
    initial = len(polygon_)
    final = len(safe_simplification(polygon_, n))

    return round(100 - final / initial * 100, 2)


if __name__ == '__main__':

    # print(polygon)
    # plot_polygon(polygon)
    # simple_polygon = rdp(polygon, 0.0001)
    # print(simple_polygon)
    #
    # shapely_polygon = Polygon(LinearRing(simple_polygon))
    # print(list(shapely_polygon.exterior.coords))
    # plot_polygon(shapely_polygon)

    from time import time
    deb = time()

    k = 0.5
    m = 180
    bay = geojson_to_polygon('june10.geojson', 0)
    ref = [[10 * point[0], 10 * point[1]] for point in bay]
    plot_polygon(ref, 'black')
    simple_polygon = safe_simplification(bay, k)
    print(f'{loss_percentage(bay, k)}%')

    larger_polygon = [[10 * point[0], 10 * point[1]] for point in simple_polygon]
    polygon = Polygon(LinearRing(larger_polygon))
    speed = find_splitting_speed(polygon, m)
    split_till_end(polygon, m, speed, 0)
    end = time()
    print(len(bay))
    print(len(simple_polygon))
    print(f'Total time: {end - deb}')
    ####################################################################################################################

    # ZoneOfInterest = 'Golfe du Saint-Laurent / Gulf of St. Lawrence'
    # n = 70412
    # ZoneOfInterest = 'Skedans Islands'
    # n = 15552
    # n = index_name(ZoneOfInterest, 'canada.geojson')
    # print(n)
    # bay = geojson_to_polygon('canada.geojson', n)
    # bay = [[0, 0], [2, 0], [3, 1], [4, 1],
    #        [5, 0], [6, 1], [6, 2], [7, 3],
    #        [8, 4], [7, 5], [6, 3], [5, 3],
    #        [4, 4], [4, 5], [4, 6], [3, 6],
    #        [3, 5], [2, 4], [3, 3], [0, 0]]

    # for point in bay:
    #     point[0], point[1] = 1000 * (point[0] + 71), 1000 * (point[1] - 63)
    # bay = circle(100, 2500, 50, 50)

    plt.show()

    # from time import time
    # deb = time()
    # percentages1 = [[] for i in range(6)]
    # percentages2 = [[] for i in range(6)]
    # percentages3 = [[] for i in range(6)]
    # percentages4 = [[] for i in range(6)]
    # for i in range(250):
    #     polygon = geojson_to_polygon('canada.geojson', i)
    #     if True:
    #         print(f'\t> Polygon n°{i + 1} ({len(polygon)} points)')
    #         for j, k in enumerate([0.5, 1, 1.5, 2, 2.5, 3]):
    #             loss = loss_percentage(polygon, k)
    #             print(f'Percentage loss with k = {k}: {loss}%.')
    #             if len(polygon) < 10:
    #                 percentages1[j].append(loss)
    #             if 10 <= len(polygon) < 100:
    #                 percentages2[j].append(loss)
    #             if 100 <= len(polygon) < 500:
    #                 percentages3[j].append(loss)
    #             else:
    #                 percentages4[j].append(loss)
    # print(len(percentages1[0]))
    # print(len(percentages2[0]))
    # print(len(percentages3[0]))
    # print(len(percentages4[0]))
    # fig = plt.figure('Percentage loss with various k')
    # k = ['0.5', '1', '1.5', '2', '2.5', '3']
    # bar_width = 0.2
    # perc1 = [sum(percentages1[i]) / len(percentages1[i]) for i in range(6)]
    # perc2 = [sum(percentages2[i]) / len(percentages2[i]) for i in range(6)]
    # perc3 = [sum(percentages3[i]) / len(percentages3[i]) for i in range(6)]
    # perc4 = [sum(percentages4[i]) / len(percentages4[i]) for i in range(6)]
    # br1 = np.arange(len(perc1))
    # br2 = [x + bar_width for x in br1]
    # br3 = [x + bar_width for x in br2]
    # br4 = [x + bar_width for x in br3]
    # plt.bar(br1, perc1, color='royalblue', width=bar_width, label='< 10')
    # plt.bar(br2, perc2, color='blue', width=bar_width, label='< 100')
    # plt.bar(br3, perc3, color='mediumblue', width=bar_width, label='< 500')
    # plt.bar(br4, perc4, color='darkblue', width=bar_width, label='Others')
    # plt.xticks([r + bar_width for r in range(len(perc1))], k)
    # plt.legend()
    # end = time()
    # print(f'Total time: {end - deb}')
