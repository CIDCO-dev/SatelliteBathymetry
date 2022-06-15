"""

Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Samuel_Dubos

"""

import requests as rq
import sys
import numpy as np


class Sentinel2(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # def get_id(self, date, footprint, start=0, rows=10):
    #
    #     req = rq.get(f'https://scihub.copernicus.eu/dhus'
    #                  f'/search?'
    #                  f'format=json'
    #                  f'&start={start}&rows={rows}'
    #                  f'&q=(footprint:%22Intersects({footprint})%22)'
    #                  f'%20AND%20(beginPosition:[{date}%20TO%20NOW])'
    #                  f'%20AND%20(platformname:Sentinel-2'
    #                  f'%20AND%20filename:S2A_*'
    #                  f'%20AND%20producttype:S2MSI2A)',
    #                  auth=(self.username, self.password))
    #
    #     if req.status_code == 200:
    #         json_data = req.json()
    #         for i, answer in enumerate(json_data['feed']['entry']):
    #             print(f"{answer['id']}")
    #     else:
    #         sys.stderr.write(f"Error while fetching file search results: {req.status_code}")
    #
    #     return 0

    def search(self, date, footprint, length=10, step=1):

        ids = []
        for i in range(step):
            req = rq.get(f'https://scihub.copernicus.eu/dhus'
                         f'/search?'
                         f'format=json'
                         f'&start={1 + i * length}&rows={length}'
                         f'&q=(footprint:%22Intersects({footprint})%22)'
                         f'%20AND%20(beginPosition:[{date}%20TO%20NOW])'
                         f'%20AND%20(platformname:Sentinel-2'
                         f'%20AND%20filename:S2A_*'
                         f'%20AND%20producttype:S2MSI2A)',
                         auth=(self.username, self.password))

            if req.status_code == 200:
                json_data = req.json()
                if 'entry' in json_data['feed'].keys():
                    for j, answer in enumerate(json_data['feed']['entry']):
                        result = json_data['feed']['entry']['id'] \
                            if 'id' in json_data['feed']['entry'] \
                            else answer['id']
                        ids.append(result)
            else:
                sys.stderr.write(f'Error while fetching file search results: {req.status_code}.')

            # sys.stderr.write(f'{round(100 * len(ids) / (step * length), 1)}%\n')
            # sys.stderr.write(f'\n{round(100 * (i + 1) / step, 1)}%')

        return np.unique(np.array(ids))

    def download(self, id):

        req = rq.get(f"https://scihub.copernicus.eu/dhus"
                     f"/odata/v1/Products('{id}')"
                     f"/$value",
                     auth=(self.username, self.password))

        if req.status_code == 200:
            f = open(f'{id}.zip', 'wb')
            f.write(req.content)
            f.close()
        else:
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

        return 0


if __name__ == "__main__":

    # Parameters definition as an example
    example_date = '2022-05-15T10:00:00.000Z'
    example_footprint = 'POLYGON((' \
                '-69.87041507596486 51.67827946383208,' \
                '-57.21416507596486 51.67827946383208,' \
                '-57.21416507596486 47.52343468727058,' \
                '-69.87041507596486 47.52343468727058,' \
                '-69.87041507596486 51.67827946383208))'

    # Test
    sentinel = Sentinel2('samueldubos', '5c6a7b54')
    print(sentinel.search(example_date, example_footprint, length=20, step=8))
    # sentinel.download('3865564a-767e-4ffa-a119-8e6129e3aa2c')
