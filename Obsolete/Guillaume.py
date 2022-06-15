"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
@Glm
"""

import requests
import sys
import os


class Sentinel2(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def search(self, date, footprint):

        ids = []
        page = 0
        resultsPerPage = 10
        totalResults = 100 #anything gt resultsPerPage will do

        # get a page of search results
        while len(ids) < totalResults:
                req = requests.get(f'https://scihub.copernicus.eu/dhus'
                             f'/search?'
                             f'format=json'
                             f'&start={page * resultsPerPage}&rows={resultsPerPage}'
                             f'&q=(footprint:%22Intersects({footprint})%22)'
                             f'%20AND%20(beginPosition:[{date}%20TO%20NOW])'
                             f'%20AND%20(platformname:Sentinel-2'
                             f'%20AND%20producttype:S2MSI2A)',
                             auth=(self.username, self.password))

                if req.status_code == 200:
                    json_data = req.json()
                    totalResults = int(json_data['feed']['opensearch:totalResults'])

                    if json_data['feed']['entry']:
                        # Process received data
                        for product in json_data['feed']['entry']:
                            ids.append(product['id'])

                        page += 1
                    else:
                        sys.stderr.write("Error: No entries in search results\n")
                        break

                else:
                    sys.stderr.write(f"Error while fetching file search results: {req.status_code}\n")
                    break

        return ids

    def download(self, id):

        req = requests.get(f"https://scihub.copernicus.eu/dhus"
                     f"/odata/v1/Products('{id}')"
                     f"/$value",
                     auth=(self.username, self.password))

        if req.status_code == 200:
            #Save binary data to ZIP file
            f = open(f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}/{id}.zip', 'wb')
            f.write(req.content)
            f.close()
        else:
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}\n")

        return req.content


# sat = Sentinel2('samueldubos', '5c6a7b54')
# example_date = '2022-05-15T00:00:00.000Z'
# example_footprint = 'POLYGON((' \
#                     '-69.87041507596486 51.67827946383208,' \
#                     '-57.21416507596486 51.67827946383208,' \
#                     '-57.21416507596486 47.52343468727058,' \
#                     '-69.87041507596486 47.52343468727058,' \
#                     '-69.87041507596486 51.67827946383208))'

