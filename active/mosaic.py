"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
"""

from bs4 import BeautifulSoup


def give_bounds(xml_):

    with open(xml_, 'r') as f:
        doc = BeautifulSoup(f, 'xml')
        west_ = doc.westBoundLongitude.Decimal.string
        est_ = doc.eastBoundLongitude.Decimal.string
        south_ = doc.southBoundLatitude.Decimal.string
        north_ = doc.northBoundLatitude.Decimal.string
    return est_, west_, south_, north_


if __name__ == '__main__':

    pass
