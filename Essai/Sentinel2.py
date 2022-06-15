"""
Copyright 2022 © Centre Interdisciplinaire de développement en Cartographie des Océans (CIDCO), Tous droits réservés
@Samuel_Dubos
@Glm
"""

from geojson_algos import geojson_to_polygon, polygon_to_string
from sentinelsat import read_geojson
from bs4 import BeautifulSoup
import zipfile
import requests
import sys
import os


def get_xml(id, handle=True):

    path = f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}'
    full_path = f'{path}/{id}'
    if handle:
        handle = zipfile.ZipFile(f'{full_path}.zip')
        handle.extractall(full_path)
        handle.close()
        os.remove(f'{full_path}.zip')

    return f'{full_path}/{os.listdir(full_path)[0]}/MTD_MSIL2A.xml'
    

def get_percentage(xml, attribute):

    with open(xml, 'r') as f:
        doc = BeautifulSoup(f, 'xml')
    match attribute:
        case 'cloud':
            ans = doc.CLOUDY_PIXEL_OVER_LAND_PERCENTAGE.string
        case 'nodata':
            ans = doc.NODATA_PIXEL_PERCENTAGE.string
        case 'dark':
            ans = doc.DARK_FEATURES_PERCENTAGE.string
        case 'vegetation':
            ans = doc.VEGETATION_PERCENTAGE.string
        case 'water':
            ans = doc.WATER_PERCENTAGE.string
        case _:
            ans = f"The percentage of {attribute} is not a valid attribute."

    return float(ans)


class Sentinel2(object):

    def __init__(self, username, password):
        self.username = username
        self.password = password

    # def __repr__(self):
    #     return f"Satellite: {self.username}, {self.password}"

    def search(self, begin_date, end_date, geojson):

        ids = []
        for i in range(6):
            ids.append(f"\n\t{read_geojson(geojson)['features'][i]['properties']['NOM']}")
            polygon = geojson_to_polygon(geojson, i)
            footprint = polygon_to_string(polygon)
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
            answer = []
            for el in ids:
                if el not in answer:
                    answer.append(el)

        return answer

    def download(self, id):

        req = requests.get(f"https://scihub.copernicus.eu/dhus"
                     f"/odata/v1/Products('{id}')"
                     f"/$value",
                     auth=(self.username, self.password))

        if req.status_code == 200:
            #Save binary data to ZIP file
            path = f'{os.path.dirname(os.path.abspath(os.path.realpath(__file__)))}'
            f = open(f'{path}/{id}.zip', 'wb')
            f.write(req.content)
            f.close()

        else:
            sys.stderr.write(f"Error while fetching file search results: {req.status_code}\n")

        return 0

