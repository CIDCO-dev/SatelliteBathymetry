from shapely.geometry import Point, Polygon
import matplotlib.pyplot as plt


def line(value_, length_):

    return [value_ for _ in range(length_)]


def choice(border_, k):

    if border_ == north:
        return [0, k]
    if border_ == south:
        return [len(border_), len(border_) - k]
    if border_ == west:
        return [len(border_) - k, 0]
    if border_ == est:
        return [k, len(border_)]


def update_dic(border_):

    corner_ = border_[0]
    dic[corner_].append(choice(border_, 0))
    for i, pixel_ in enumerate(border_[:-1]):
        next_ = border_[i + 1]
        if pixel_ != next_:
            dic[pixel_].append(choice(border_, i))
            dic[next_].append(choice(border_, i + 1))


def add_corners(borders_):

    for border_ in borders_:
        dic[border_[0]].append(choice(border_, 0))


def plot_polygon(polygon_, color_='blue'):
    """Plots a polygon using matplotlib.pyplot module."""
    xs, ys = [], []
    if isinstance(polygon_, Polygon):
        for point in polygon_.exterior.coords:
            xs.append(point[0])
            ys.append(point[1])
    else:
        xs, ys = zip(*polygon_)
    plt.plot(xs, ys, color=color_)


if __name__ == '__main__':

    north = line(0, 3) + line(1, 20) + line(2, 20) + line(3, 20) + line(4, 20) + line(5, 17)
    south = line(4, 19) + line(5, 20) + line(6, 20) + line(7, 20) + line(8, 20) + line(9, 1)
    west = line(0, 6) + line(1, 30) + line(2, 30) + line(3, 30) + line(4, 4)
    est = line(5, 2) + line(6, 30) + line(7, 30) + line(8, 30) + line(9, 8)

    south.reverse()
    west.reverse()

    borders = [north, est, south, west]

    dic = {0: [], 1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: []}

    for border in borders:
        update_dic(border)

    polygon = Polygon(dic[1])
    plot_polygon(polygon)
    point = Point([10, 8])
    plt.plot(point.x, point.y, 'ro')
    print(polygon.contains(point))

    # for key in dic.keys():
    #     dic[key].append(dic[key][0])
    #     plot_polygon(dic[key])

    plt.show()
