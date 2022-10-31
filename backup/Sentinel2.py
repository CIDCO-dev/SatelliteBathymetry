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

    def search(self, begin_date, end_date, footprint):

        ids = []
        page = 0
        resultsPerPage = 30
        totalResults = 100 #anything gt resultsPerPage will do

        # get a page of search results
        while len(ids) < totalResults:
            req = requests.get(f'https://scihub.copernicus.eu/dhus'
                             f'/search?'
                             f'format=json'
                             f'&start={page * resultsPerPage}&rows={resultsPerPage}'
                             f'&q=(footprint:%22Intersects({footprint})%22)'
                             f'%20AND%20(beginPosition:[{begin_date}%20TO%20{end_date}])'
                             f'%20AND%20(platformname:Sentinel-2'
                             f'%20AND%20producttype:S2MSI2A)',
                             auth=(self.username, self.password))

            if req.status_code == 200:
                json_data = req.json()
                totalResults = int(json_data['feed']['opensearch:totalResults'])

                if totalResults != 0 and json_data['feed']['entry']:
                    # Process received data
                    list_dic = json_data['feed']['entry']
                    k = 0
                    flag = True
                    while k < len(list_dic) and flag:
                        (result, flag) = (list_dic['id'], False) if 'id' in list_dic else (list_dic[k]['id'], True)
                        ids.append(result)
                        k += 1

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
                 
