"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from bs4 import BeautifulSoup


def get_bounds(xml_):
    """Gives the boundaries of a product."""
    with open(xml_, 'r') as f:
        doc = BeautifulSoup(f, 'xml')
        west_ = doc.westBoundLongitude.Decimal.string
        est_ = doc.eastBoundLongitude.Decimal.string
        south_ = doc.southBoundLatitude.Decimal.string
        north_ = doc.northBoundLatitude.Decimal.string
    return float(est_) - 360, float(west_) - 360, float(south_), float(north_)


def nodata_percentage(xml_):
    """Gives the percentage of pixels that contain no data."""
    with open(xml_, 'r') as f:
        doc = BeautifulSoup(f, 'xml')
        nodata = doc.NODATA_PIXEL_PERCENTAGE.string
    return round(float(nodata), 2)


def transform_c2p(lat_, lng_, borders_, size_):
    """Transforms a given location in Mercator-projection to (x, y) coordinates in a plan image."""
    est_, west_, south_, north_ = [borders_[i] for i in range(4)]
    x_ = int((lat_ - north_) / (south_ - north_) * size_[0])
    y_ = int((lng_ - west_) / (est_ - west_) * size_[1])
    return x_, y_


if __name__ == '__main__':

    pass
