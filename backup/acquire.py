"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
@Glm
"""

import requests
import sys


class Sentinel2(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.results_per_page = 10

    def search(self, date1_, date2_, footprint_):
        """Searches the identifications of products added since a given date in a given footprint."""
        ids, page, total_results = [], 0, 100
        while len(ids) < total_results:
            req = requests.get(f'https://scihub.copernicus.eu/dhus'
                               f'/search?'
                               f'format=json'
                               f'&start={page * self.results_per_page}'
                               f'&rows={self.results_per_page}'
                               f'&q=(footprint:%22Intersects({footprint_})%22)'
                               f'%20AND%20(beginPosition:[{date1_}%20TO%20{date2_}])'
                               f'%20AND%20(platformname:Sentinel-2'
                               f'%20AND%20producttype:S2MSI2A)',
                               auth=(self.username, self.password))
            if req.status_code == 200:
                json_data = req.json()
                total_results = int(json_data['feed']['opensearch:totalResults'])
                if total_results != 0 and json_data['feed']['entry']:
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

    def download(self, id_, path_):
        """Downloads a product from its identification."""
        req = requests.get(f"https://scihub.copernicus.eu/dhus"
                           f"/odata/v1/Products('{id_}')"
                           f"/$value",
                           auth=(self.username, self.password))
        if req.status_code == 200:
            f = open(f'{path_}/{id_}.zip', 'wb')
            f.write(req.content)
            f.close()
        else:
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}\n")
        return 0


if __name__ == "__main__":

    pass
