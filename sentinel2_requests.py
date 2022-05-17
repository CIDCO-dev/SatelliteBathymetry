"""

Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Samuel_Dubos

"""

import requests as rq
import sys
import time


class Sentinel2(object):


    def __init__(self, username, password):
        self.username = username
        self.password = password


    def get_id(self, date, footprint, start=0, rows=10):

        self.__date = date
        self.__footprint = footprint
        self.__start = start
        self.__rows = rows

        req = rq.get(f'https://scihub.copernicus.eu/dhus'
                     f'/search?'
                     f'format=json'
                     f'&start={self.__start}&rows={self.__rows}'
                     f'&q=(footprint:%22Intersects({self.__footprint})%22)'
                     f'%20AND%20(beginPosition:[{self.__date}%20TO%20NOW])'
                     f'%20AND%20(platformname:Sentinel-2'
                     f'%20AND%20filename:S2A_*'
                     f'%20AND%20producttype:S2MSI2A)',
                     auth=(self.username, self.password))

        if req.status_code == 200:
            json_data = req.json()
            for i, answer in enumerate(json_data['feed']['entry']):
                print(f"{answer['id']}")
        else:
            json_data = rows_
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

        return 0


    def search(self, date, footprint, step=10, iter=1):

        self.__date = date
        self.__footprint = footprint
        self.__step = step
        self.__iter = iter

        for i in range(self.__iter):
            self.get_id(self.__date, self.__footprint, i * self.__step, self.__step)

        return 0


    def download(self, id):

        self.__id = id

        req = rq.get(f"https://scihub.copernicus.eu/dhus"
                     f"/odata/v1/Products('{self.__id}')"
                     f"/$value",
                     auth=(self.username, self.password))

        if req.status_code == 200:
            f = open(f'{self.__id}.zip', 'wb')
            f.write(req.content)
            f.close()
        else:
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

        return 0


if __name__ == "__main__":

    # Parameters definition as an example
    date = '2022-05-15T12:30:00.000Z'
    footprint = 'POLYGON((' \
                '-69.87041507596486 51.67827946383208,' \
                '-57.21416507596486 51.67827946383208,' \
                '-57.21416507596486 47.52343468727058,' \
                '-69.87041507596486 47.52343468727058,' \
                '-69.87041507596486 51.67827946383208))'
