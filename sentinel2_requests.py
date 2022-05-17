"""

Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés

@Samuel_Dubos

"""

import requests as rq
import sys


class Sentinel2(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def search(self, date, footprint, length=10, step=1):

        ids = []
        for i in range(step):
            req = rq.get(f'https://scihub.copernicus.eu/dhus'
                         f'/search?'
                         f'format=json'
                         f'&start={i * length}&rows={length}'
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
                        ids.append(answer['id'])
                        print(f'{100*(i*length+j)/(step*length)}%')
                else:
                    return ids
            else:
                sys.stderr.write(f"Error while fetching file search results: {req.status_code}")

        return ids

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
    example_date = '2022-05-15T18:30:00.000Z'
    example_footprint = 'POLYGON((' \
                '-69.87041507596486 51.67827946383208,' \
                '-57.21416507596486 51.67827946383208,' \
                '-57.21416507596486 47.52343468727058,' \
                '-69.87041507596486 47.52343468727058,' \
                '-69.87041507596486 51.67827946383208))'
