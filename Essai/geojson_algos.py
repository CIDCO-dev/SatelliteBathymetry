from sentinelsat import read_geojson
from shapely.geometry import LinearRing, LineString, Polygon, Point
from shapely.ops import split
import matplotlib.pyplot as plt
from numpy import *
from random import uniform


def geojson_to_polygon(geojson_, n):

    geojson_file = read_geojson(geojson_)
    polygon_ = geojson_file['features'][0]['geometry']['coordinates'][0][n]

    return polygon_


def polygon_to_string(polygon_):

    string = 'POLYGON(('
    for i, point in enumerate(polygon_):
        string += f'{point[0]} {point[1]}, '
    string = string[:-2] + '))'

    return string


def plot_polygon(polygon_):

    xs, ys = [], []
    if type(polygon_) == Polygon:
        for point in polygon_.exterior.coords:
            xs.append(point[0])
            ys.append(point[1])
    else:
        xs, ys = zip(*polygon_)
    plt.plot(xs, ys)


if __name__ == '__main__':

    geojson_file = read_geojson('june10.geojson')
    polygon_ = geojson_file['features'][0]['geometry']['coordinates']
    for i in range(10):
        print(len(polygon_[0][i]))
